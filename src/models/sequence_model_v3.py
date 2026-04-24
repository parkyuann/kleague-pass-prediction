"""
K리그 패스 예측 - 시퀀스 모델 V3
================================
Raw 데이터에서 직접 로드하여 데이터 누수 방지

핵심 수정:
- Test 데이터를 parquet 대신 raw CSV에서 직접 로드
- 마지막 이벤트의 end_x, end_y가 NaN인 것을 보장
- 보조 과제 기반 멀티태스크 학습 유지
"""

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from tqdm import tqdm
from typing import Tuple, List, Dict, Optional
import json
import warnings
warnings.filterwarnings('ignore')

# 필드 크기
FIELD_LENGTH = 105.0
FIELD_WIDTH = 68.0

# 디바이스 설정
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class SequenceDatasetV3(Dataset):
    """향상된 시퀀스 데이터셋 - 보조 태스크 지원"""

    def __init__(self,
                 sequences: List[np.ndarray],
                 targets: np.ndarray = None,
                 start_coords: np.ndarray = None,
                 aux_targets: Dict[str, np.ndarray] = None,
                 max_len: int = 50,
                 augment: bool = False):
        self.sequences = sequences
        self.targets = targets
        self.start_coords = start_coords
        self.aux_targets = aux_targets
        self.max_len = max_len
        self.augment = augment
        self.n_original = len(sequences)

    def __len__(self):
        if self.augment and self.targets is not None:
            return self.n_original * 2
        return self.n_original

    def __getitem__(self, idx):
        is_augmented = False
        original_idx = idx

        if self.augment and idx >= self.n_original:
            is_augmented = True
            original_idx = idx - self.n_original

        seq = self.sequences[original_idx].copy()

        # Y축 대칭 증강 적용
        if is_augmented:
            seq = self._apply_y_augmentation(seq)

        # 패딩/트렁케이션
        if len(seq) > self.max_len:
            seq = seq[-self.max_len:]
        elif len(seq) < self.max_len:
            pad = np.zeros((self.max_len - len(seq), seq.shape[1]))
            seq = np.vstack([pad, seq])

        seq_tensor = torch.FloatTensor(seq)
        seq_len = min(len(self.sequences[original_idx]), self.max_len)

        if self.targets is not None:
            target = self.targets[original_idx].copy()
            start = self.start_coords[original_idx].copy()

            if is_augmented:
                target[1] = -target[1]  # dy 반전
                start[1] = FIELD_WIDTH - start[1]  # y 반전

            target_tensor = torch.FloatTensor(target)
            start_tensor = torch.FloatTensor(start)

            if self.aux_targets is not None:
                aux = {}
                for key, val in self.aux_targets.items():
                    aux_val = val[original_idx]
                    if is_augmented and key in ['next_dy', 'goal_angle']:
                        aux_val = -aux_val
                    aux[key] = torch.FloatTensor([aux_val]) if np.isscalar(aux_val) else torch.FloatTensor(aux_val)
                return seq_tensor, target_tensor, start_tensor, aux, seq_len

            return seq_tensor, target_tensor, start_tensor, seq_len
        else:
            start = self.start_coords[original_idx].copy()
            start_tensor = torch.FloatTensor(start)
            return seq_tensor, start_tensor, seq_len

    def _apply_y_augmentation(self, seq: np.ndarray) -> np.ndarray:
        """Y축 대칭 변환 - start_y, dy 관련 피처 반전"""
        seq = seq.copy()
        # 피처 순서: [start_x, start_y, time_seconds, is_home, period_id, ...]
        # y 관련 인덱스: 1 (start_y), 그리고 끝의 dy
        seq[:, 1] = 1.0 - seq[:, 1]  # start_y_norm 반전 (0~1 범위)
        seq[:, -1] = -seq[:, -1]  # dy_norm 반전
        return seq


class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 100):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))

        pe[:, 0::2] = torch.sin(position * div_term)
        if d_model % 2 == 0:
            pe[:, 1::2] = torch.cos(position * div_term)
        else:
            pe[:, 1::2] = torch.cos(position * div_term[:-1])

        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


class MultiTaskSequenceModelV3(nn.Module):
    """멀티태스크 시퀀스 모델 V3"""

    def __init__(self,
                 input_dim: int,
                 hidden_dim: int = 256,
                 num_layers: int = 4,
                 nhead: int = 8,
                 dropout: float = 0.3,
                 num_event_types: int = 10,
                 use_auxiliary: bool = True):
        super().__init__()

        self.use_auxiliary = use_auxiliary
        self.hidden_dim = hidden_dim

        # 입력 프로젝션
        self.input_proj = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout)
        )

        self.pos_encoder = PositionalEncoding(hidden_dim, dropout)

        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=nhead,
            dim_feedforward=hidden_dim * 4,
            dropout=dropout,
            batch_first=True,
            activation='gelu'
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        # BiLSTM Branch
        self.lstm = nn.LSTM(
            hidden_dim, hidden_dim // 2,
            num_layers=2,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0
        )

        # Attention
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )

        # Feature fusion
        self.fusion = nn.Sequential(
            nn.Linear(hidden_dim * 3, hidden_dim * 2),
            nn.LayerNorm(hidden_dim * 2),
            nn.GELU(),
            nn.Dropout(dropout)
        )

        # 메인 태스크 헤드: dx, dy 예측
        self.main_head = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.GELU(),
            nn.Dropout(dropout / 2),
            nn.Linear(hidden_dim // 2, 2)
        )

        if use_auxiliary:
            self.event_type_head = nn.Sequential(
                nn.Linear(hidden_dim * 2, hidden_dim // 2),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim // 2, num_event_types)
            )

            self.success_head = nn.Sequential(
                nn.Linear(hidden_dim * 2, hidden_dim // 4),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim // 4, 1)
            )

            self.distance_head = nn.Sequential(
                nn.Linear(hidden_dim * 2, hidden_dim // 4),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim // 4, 1)
            )

    def forward(self, x, seq_lens=None):
        batch_size, seq_len, _ = x.shape

        x = self.input_proj(x)
        x_pos = self.pos_encoder(x)
        transformer_out = self.transformer(x_pos)

        lstm_out, _ = self.lstm(x)

        combined = torch.cat([transformer_out, lstm_out], dim=-1)

        attn_scores = self.attention(combined)
        attn_weights = F.softmax(attn_scores, dim=1)
        context = torch.sum(attn_weights * combined, dim=1)

        transformer_last = transformer_out[:, -1, :]

        fused = torch.cat([context, transformer_last], dim=-1)
        fused = self.fusion(fused)

        main_out = self.main_head(fused)

        if self.use_auxiliary:
            aux_out = {
                'event_type': self.event_type_head(fused),
                'success': self.success_head(fused),
                'distance': self.distance_head(fused)
            }
            return main_out, aux_out

        return main_out


class MultiTaskLoss(nn.Module):
    def __init__(self, num_tasks: int = 4):
        super().__init__()
        self.log_vars = nn.Parameter(torch.zeros(num_tasks))

    def forward(self, main_pred, main_target, aux_preds=None, aux_targets=None):
        main_loss = F.mse_loss(main_pred, main_target)

        precision0 = torch.exp(-self.log_vars[0])
        total_loss = precision0 * main_loss + self.log_vars[0]

        if aux_preds is not None and aux_targets is not None:
            if 'event_type' in aux_preds and 'event_type' in aux_targets:
                event_loss = F.cross_entropy(
                    aux_preds['event_type'],
                    aux_targets['event_type'].long().squeeze()
                )
                precision1 = torch.exp(-self.log_vars[1])
                total_loss = total_loss + precision1 * event_loss + self.log_vars[1]

            if 'success' in aux_preds and 'success' in aux_targets:
                success_loss = F.binary_cross_entropy_with_logits(
                    aux_preds['success'],
                    aux_targets['success']
                )
                precision2 = torch.exp(-self.log_vars[2])
                total_loss = total_loss + precision2 * success_loss + self.log_vars[2]

            if 'distance' in aux_preds and 'distance' in aux_targets:
                dist_loss = F.mse_loss(
                    aux_preds['distance'],
                    aux_targets['distance']
                )
                precision3 = torch.exp(-self.log_vars[3])
                total_loss = total_loss + precision3 * dist_loss + self.log_vars[3]

        return total_loss, main_loss


def load_train_from_raw(raw_dir: Path) -> pd.DataFrame:
    """Raw train.csv에서 학습 데이터 로드"""
    train_df = pd.read_csv(raw_dir / 'train.csv')
    train_df['result_name'] = train_df['result_name'].fillna('None')
    return train_df


def load_test_from_raw(raw_dir: Path) -> Tuple[pd.DataFrame, List[str]]:
    """
    Raw test 데이터 로드 - 개별 CSV 파일에서 직접 로드
    데이터 누수 없이 원본 그대로 로드
    """
    test_meta = pd.read_csv(raw_dir / 'test.csv')

    all_episodes = []
    episode_order = []

    for _, row in tqdm(test_meta.iterrows(), total=len(test_meta), desc="Loading test episodes"):
        game_episode = row['game_episode']
        # 경로 수정: ./test/... -> raw_dir/test/...
        csv_path = raw_dir / row['path'].replace('./', '')

        if csv_path.exists():
            ep_df = pd.read_csv(csv_path)
            ep_df['result_name'] = ep_df['result_name'].fillna('None')
            all_episodes.append(ep_df)
            episode_order.append(game_episode)

    test_df = pd.concat(all_episodes, ignore_index=True)
    return test_df, episode_order


def prepare_sequence_data_v3(raw_dir: Path, is_test: bool = False) -> Tuple:
    """
    Raw 데이터에서 시퀀스 준비 - 데이터 누수 없음
    """
    # 이벤트 타입 인코딩 (train에서 생성)
    train_df = pd.read_csv(raw_dir / 'train.csv')
    train_df['result_name'] = train_df['result_name'].fillna('None')

    event_types = sorted(train_df['type_name'].unique())
    result_types = sorted(train_df['result_name'].unique())
    type_to_idx = {t: i for i, t in enumerate(event_types)}
    result_to_idx = {r: i for i, r in enumerate(result_types)}
    num_event_types = len(event_types)

    # 데이터 로드
    if is_test:
        df, episode_order = load_test_from_raw(raw_dir)
        episode_list = episode_order
    else:
        df = train_df
        episode_list = sorted(df['game_episode'].unique())

    sequences = []
    targets = []
    start_coords = []
    aux_targets = {'event_type': [], 'success': [], 'distance': []}
    episode_ids = []

    for ep in tqdm(episode_list, desc="Preparing sequences"):
        ep_data = df[df['game_episode'] == ep].sort_values('action_id')

        if len(ep_data) < 2:
            continue

        # 시퀀스 피처 생성
        seq_features = []
        for i, (_, row) in enumerate(ep_data.iterrows()):
            is_last = (i == len(ep_data) - 1)

            # 기본 피처
            feat = [
                row['start_x'] / FIELD_LENGTH,
                row['start_y'] / FIELD_WIDTH,
                row['time_seconds'] / 3000.0,
                float(row['is_home']),
                float(row['period_id']) / 2,
            ]

            # 이벤트 타입 인코딩 (one-hot 대신 label encoding)
            feat.append(type_to_idx.get(row['type_name'], 0) / num_event_types)
            feat.append(result_to_idx.get(row['result_name'], 0) / len(result_types))

            # 이전 이벤트와의 관계
            if i > 0:
                prev_row = ep_data.iloc[i-1]
                move_x = (row['start_x'] - prev_row['start_x']) / FIELD_LENGTH
                move_y = (row['start_y'] - prev_row['start_y']) / FIELD_WIDTH
                time_diff = (row['time_seconds'] - prev_row['time_seconds']) / 100.0
            else:
                move_x, move_y, time_diff = 0.0, 0.0, 0.0

            feat.extend([move_x, move_y, time_diff])

            # 필드 위치 피처
            dist_to_goal = np.sqrt((FIELD_LENGTH - row['start_x'])**2 + (FIELD_WIDTH/2 - row['start_y'])**2) / FIELD_LENGTH
            dist_from_center = abs(row['start_y'] - FIELD_WIDTH/2) / (FIELD_WIDTH/2)

            feat.extend([dist_to_goal, dist_from_center])

            # 이동량 (마지막 이벤트는 0으로 - 데이터 누수 방지!)
            if not is_last and pd.notna(row['end_x']) and pd.notna(row['end_y']):
                dx_norm = (row['end_x'] - row['start_x']) / FIELD_LENGTH
                dy_norm = (row['end_y'] - row['start_y']) / FIELD_WIDTH
            else:
                dx_norm, dy_norm = 0.0, 0.0

            feat.extend([dx_norm, dy_norm])
            seq_features.append(feat)

        sequences.append(np.array(seq_features, dtype=np.float32))

        # 마지막 이벤트 시작 좌표
        last_row = ep_data.iloc[-1]
        start_coords.append([last_row['start_x'], last_row['start_y']])
        episode_ids.append(ep)

        if not is_test:
            # 타겟: 마지막 이벤트의 end_x, end_y
            target_dx = last_row['end_x'] - last_row['start_x']
            target_dy = last_row['end_y'] - last_row['start_y']
            targets.append([target_dx, target_dy])

            # 보조 태스크 타겟
            aux_targets['event_type'].append(type_to_idx.get(last_row['type_name'], 0))
            aux_targets['success'].append(float(last_row['result_name'] == 'Successful'))
            aux_targets['distance'].append(np.sqrt(target_dx**2 + target_dy**2))

    input_dim = 14  # 피처 개수: 5 + 2 + 3 + 2 + 2 = 14

    if is_test:
        return sequences, np.array(start_coords), episode_ids, input_dim, num_event_types
    else:
        aux_targets = {k: np.array(v) for k, v in aux_targets.items()}
        return (sequences, np.array(targets), np.array(start_coords),
                aux_targets, episode_ids, input_dim, num_event_types)


def train_model_v3(
    train_sequences, train_targets, train_starts, train_aux,
    val_sequences=None, val_targets=None, val_starts=None, val_aux=None,
    input_dim: int = 14,
    num_event_types: int = 10,
    epochs: int = 100,
    batch_size: int = 64,
    lr: float = 1e-3,
    hidden_dim: int = 256,
    num_layers: int = 4,
    nhead: int = 8,
    dropout: float = 0.3,
    use_auxiliary: bool = True,
    augment: bool = True
):
    """시퀀스 모델 V3 학습"""

    print(f"Device: {DEVICE}")
    print(f"Input dim: {input_dim}, Event types: {num_event_types}")
    print(f"Train samples: {len(train_sequences)}, Augment: {augment}")

    # 데이터셋
    train_dataset = SequenceDatasetV3(
        train_sequences, train_targets, train_starts, train_aux,
        augment=augment
    )
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
        num_workers=0, pin_memory=True
    )

    if val_sequences is not None:
        val_dataset = SequenceDatasetV3(
            val_sequences, val_targets, val_starts, val_aux,
            augment=False
        )
        val_loader = DataLoader(val_dataset, batch_size=batch_size)

    # 모델
    model = MultiTaskSequenceModelV3(
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        num_layers=num_layers,
        nhead=nhead,
        dropout=dropout,
        num_event_types=num_event_types,
        use_auxiliary=use_auxiliary
    ).to(DEVICE)

    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # 손실 함수
    criterion = MultiTaskLoss(num_tasks=4) if use_auxiliary else nn.MSELoss()
    if use_auxiliary:
        criterion = criterion.to(DEVICE)

    # 옵티마이저
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)

    # 스케줄러
    warmup_epochs = 5
    scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer, T_0=20, T_mult=2, eta_min=1e-6
    )

    best_val_loss = float('inf')
    best_model_state = None
    patience = 15
    patience_counter = 0

    for epoch in range(epochs):
        # Warmup
        if epoch < warmup_epochs:
            warmup_lr = lr * (epoch + 1) / warmup_epochs
            for param_group in optimizer.param_groups:
                param_group['lr'] = warmup_lr

        # Training
        model.train()
        train_loss = 0
        train_main_loss = 0

        for batch in train_loader:
            if use_auxiliary:
                seq, target, start, aux, seq_len = batch
                seq = seq.to(DEVICE)
                target = target.to(DEVICE)
                aux_device = {k: v.to(DEVICE) for k, v in aux.items()}

                optimizer.zero_grad()
                main_pred, aux_pred = model(seq)
                loss, main_loss = criterion(main_pred, target, aux_pred, aux_device)
            else:
                seq, target, start, seq_len = batch
                seq = seq.to(DEVICE)
                target = target.to(DEVICE)

                optimizer.zero_grad()
                pred = model(seq)
                loss = criterion(pred, target)
                main_loss = loss

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            train_loss += loss.item()
            train_main_loss += main_loss.item()

        train_loss /= len(train_loader)
        train_main_loss /= len(train_loader)

        # Validation
        if val_sequences is not None:
            model.eval()
            val_loss = 0
            val_main_loss = 0

            with torch.no_grad():
                for batch in val_loader:
                    if use_auxiliary:
                        seq, target, start, aux, seq_len = batch
                        seq = seq.to(DEVICE)
                        target = target.to(DEVICE)
                        aux_device = {k: v.to(DEVICE) for k, v in aux.items()}

                        main_pred, aux_pred = model(seq)
                        loss, main_loss = criterion(main_pred, target, aux_pred, aux_device)
                    else:
                        seq, target, start, seq_len = batch
                        seq = seq.to(DEVICE)
                        target = target.to(DEVICE)

                        pred = model(seq)
                        loss = criterion(pred, target)
                        main_loss = loss

                    val_loss += loss.item()
                    val_main_loss += main_loss.item()

            val_loss /= len(val_loader)
            val_main_loss /= len(val_loader)

            if val_main_loss < best_val_loss:
                best_val_loss = val_main_loss
                best_model_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
                patience_counter = 0
            else:
                patience_counter += 1

            if (epoch + 1) % 5 == 0:
                print(f"  Epoch {epoch+1}/{epochs} - "
                      f"Train: {train_main_loss:.4f}, Val: {val_main_loss:.4f} "
                      f"(Best: {best_val_loss:.4f})")

            if patience_counter >= patience:
                print(f"  Early stopping at epoch {epoch+1}")
                break

        if epoch >= warmup_epochs:
            scheduler.step()

    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    return model


def predict_v3(model, sequences, starts, batch_size: int = 64, use_auxiliary: bool = True):
    """모델로 예측"""
    dataset = SequenceDatasetV3(sequences, start_coords=starts, augment=False)
    loader = DataLoader(dataset, batch_size=batch_size)

    model.eval()
    predictions = []

    with torch.no_grad():
        for batch in loader:
            seq, start, seq_len = batch
            seq = seq.to(DEVICE)

            if use_auxiliary:
                pred, _ = model(seq)
            else:
                pred = model(seq)

            predictions.append(pred.cpu().numpy())

    return np.vstack(predictions)


if __name__ == "__main__":
    print(f"Device: {DEVICE}")

    raw_dir = Path('E:/Dacon/kleague-pass-prediction/data/raw')

    print("Loading train data from raw...")
    result = prepare_sequence_data_v3(raw_dir, is_test=False)
    sequences, targets, starts, aux_targets, episode_ids, input_dim, num_types = result

    print(f"Sequences: {len(sequences)}")
    print(f"Input dim: {input_dim}")
    print(f"Target shape: {targets.shape}")
    print(f"Aux targets: {list(aux_targets.keys())}")

    print("\nLoading test data from raw...")
    test_result = prepare_sequence_data_v3(raw_dir, is_test=True)
    test_sequences, test_starts, test_episode_ids, test_input_dim, _ = test_result

    print(f"Test sequences: {len(test_sequences)}")
    print(f"Test input dim: {test_input_dim}")

    # 모델 테스트
    model = MultiTaskSequenceModelV3(
        input_dim=input_dim,
        hidden_dim=128,
        num_event_types=num_types
    ).to(DEVICE)

    dummy = torch.randn(4, 50, input_dim).to(DEVICE)
    main_out, aux_out = model(dummy)
    print(f"Main output shape: {main_out.shape}")
    print(f"Aux outputs: {[(k, v.shape) for k, v in aux_out.items()]}")
