"""
K리그 패스 예측 - 시퀀스 모델 V3 학습 파이프라인
================================================
Raw 데이터에서 직접 로드하여 데이터 누수 방지

실행:
    python train_sequence_v3.py
"""

import numpy as np
import pandas as pd
import torch
from pathlib import Path
from sklearn.model_selection import KFold
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

from src.models.sequence_model_v3 import (
    prepare_sequence_data_v3,
    train_model_v3,
    predict_v3,
    MultiTaskSequenceModelV3,
    DEVICE,
    FIELD_LENGTH,
    FIELD_WIDTH
)


def calculate_euclidean_distance(pred_x, pred_y, true_x, true_y):
    """유클리디안 거리 계산"""
    return np.sqrt((pred_x - true_x)**2 + (pred_y - true_y)**2)


def clip_to_field(x, y):
    """필드 경계로 클리핑"""
    x = np.clip(x, 0, FIELD_LENGTH)
    y = np.clip(y, 0, FIELD_WIDTH)
    return x, y


def main():
    print("=" * 60)
    print("K리그 패스 예측 - 시퀀스 모델 V3 학습")
    print("=" * 60)
    print(f"Device: {DEVICE}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ========== 설정 ==========
    RAW_DIR = Path('E:/Dacon/kleague-pass-prediction/data/raw')
    SUBMISSION_DIR = Path('E:/Dacon/kleague-pass-prediction/data/submissions')
    MODEL_DIR = Path('E:/Dacon/kleague-pass-prediction/models')

    MODEL_DIR.mkdir(exist_ok=True)
    SUBMISSION_DIR.mkdir(exist_ok=True, parents=True)

    # 하이퍼파라미터
    CONFIG = {
        'n_folds': 5,
        'epochs': 100,
        'batch_size': 64,
        'lr': 1e-3,
        'use_auxiliary': True,
        'augment': True,
        'hidden_dim': 256,
        'num_layers': 4,
        'nhead': 8,
        'dropout': 0.3,
    }

    print(f"\nConfig: {CONFIG}")

    # ========== 데이터 로드 ==========
    print("\n" + "=" * 40)
    print("Raw 데이터에서 직접 로드 (데이터 누수 방지)")
    print("=" * 40)

    result = prepare_sequence_data_v3(RAW_DIR, is_test=False)
    sequences, targets, starts, aux_targets, episode_ids, input_dim, num_types = result

    print(f"Train sequences: {len(sequences)}")
    print(f"Input dimension: {input_dim}")
    print(f"Target shape: {targets.shape}")
    print(f"Number of event types: {num_types}")
    print(f"Aux targets: {list(aux_targets.keys())}")

    # 타겟 통계
    print(f"\nTarget dx - Mean: {targets[:, 0].mean():.2f}, Std: {targets[:, 0].std():.2f}")
    print(f"Target dy - Mean: {targets[:, 1].mean():.2f}, Std: {targets[:, 1].std():.2f}")

    # ========== Cross Validation ==========
    print("\n" + "=" * 40)
    print(f"{CONFIG['n_folds']}-Fold Cross Validation")
    print("=" * 40)

    kf = KFold(n_splits=CONFIG['n_folds'], shuffle=True, random_state=42)

    oof_predictions = np.zeros_like(targets)
    fold_scores = []
    models = []

    for fold, (train_idx, val_idx) in enumerate(kf.split(sequences)):
        print(f"\n--- Fold {fold + 1}/{CONFIG['n_folds']} ---")

        # 데이터 분할
        train_seq = [sequences[i] for i in train_idx]
        val_seq = [sequences[i] for i in val_idx]

        train_targets_fold = targets[train_idx]
        val_targets_fold = targets[val_idx]

        train_starts_fold = starts[train_idx]
        val_starts_fold = starts[val_idx]

        train_aux_fold = {k: v[train_idx] for k, v in aux_targets.items()}
        val_aux_fold = {k: v[val_idx] for k, v in aux_targets.items()}

        print(f"Train: {len(train_seq)}, Val: {len(val_seq)}")

        # 모델 학습
        model = train_model_v3(
            train_seq, train_targets_fold, train_starts_fold, train_aux_fold,
            val_seq, val_targets_fold, val_starts_fold, val_aux_fold,
            input_dim=input_dim,
            num_event_types=num_types,
            epochs=CONFIG['epochs'],
            batch_size=CONFIG['batch_size'],
            lr=CONFIG['lr'],
            hidden_dim=CONFIG['hidden_dim'],
            num_layers=CONFIG['num_layers'],
            nhead=CONFIG['nhead'],
            dropout=CONFIG['dropout'],
            use_auxiliary=CONFIG['use_auxiliary'],
            augment=CONFIG['augment']
        )

        models.append(model)

        # Validation 예측
        val_pred = predict_v3(model, val_seq, val_starts_fold,
                             use_auxiliary=CONFIG['use_auxiliary'])

        # dx, dy → end_x, end_y
        pred_end_x = val_starts_fold[:, 0] + val_pred[:, 0]
        pred_end_y = val_starts_fold[:, 1] + val_pred[:, 1]
        pred_end_x, pred_end_y = clip_to_field(pred_end_x, pred_end_y)

        true_end_x = val_starts_fold[:, 0] + val_targets_fold[:, 0]
        true_end_y = val_starts_fold[:, 1] + val_targets_fold[:, 1]

        # 점수 계산
        distances = calculate_euclidean_distance(pred_end_x, pred_end_y, true_end_x, true_end_y)
        fold_score = distances.mean()
        fold_scores.append(fold_score)

        print(f"  Fold {fold + 1} Score: {fold_score:.4f}")

        # OOF 저장
        oof_predictions[val_idx] = val_pred

        # 모델 저장
        model_path = MODEL_DIR / f'seq_v3_fold{fold + 1}.pt'
        torch.save({
            'model_state_dict': model.state_dict(),
            'config': CONFIG,
            'input_dim': input_dim,
            'num_event_types': num_types,
            'fold_score': fold_score
        }, model_path)

    # ========== CV 결과 ==========
    print("\n" + "=" * 40)
    print("Cross Validation 결과")
    print("=" * 40)

    cv_mean = np.mean(fold_scores)
    cv_std = np.std(fold_scores)

    print(f"Fold scores: {[f'{s:.4f}' for s in fold_scores]}")
    print(f"CV Mean: {cv_mean:.4f} +/- {cv_std:.4f}")

    # OOF 전체 점수
    pred_end_x = starts[:, 0] + oof_predictions[:, 0]
    pred_end_y = starts[:, 1] + oof_predictions[:, 1]
    pred_end_x, pred_end_y = clip_to_field(pred_end_x, pred_end_y)

    true_end_x = starts[:, 0] + targets[:, 0]
    true_end_y = starts[:, 1] + targets[:, 1]

    oof_distances = calculate_euclidean_distance(pred_end_x, pred_end_y, true_end_x, true_end_y)
    oof_score = oof_distances.mean()

    print(f"\nOOF Score: {oof_score:.4f}")

    # ========== Test 예측 ==========
    print("\n" + "=" * 40)
    print("Test 데이터 예측 (Raw CSV에서 직접 로드)")
    print("=" * 40)

    test_result = prepare_sequence_data_v3(RAW_DIR, is_test=True)
    test_sequences, test_starts, test_episode_ids, test_input_dim, _ = test_result

    print(f"Test sequences: {len(test_sequences)}")

    # 앙상블 예측
    test_predictions = []
    for fold, model in enumerate(models):
        print(f"  Predicting with fold {fold + 1} model...")
        pred = predict_v3(model, test_sequences, test_starts,
                         use_auxiliary=CONFIG['use_auxiliary'])
        test_predictions.append(pred)

    # 평균 앙상블
    test_pred_mean = np.mean(test_predictions, axis=0)

    # dx, dy → end_x, end_y
    test_end_x = test_starts[:, 0] + test_pred_mean[:, 0]
    test_end_y = test_starts[:, 1] + test_pred_mean[:, 1]
    test_end_x, test_end_y = clip_to_field(test_end_x, test_end_y)

    # 제출 파일 생성
    sample_submission = pd.read_csv(RAW_DIR / 'sample_submission.csv')

    # episode_id 매핑
    submission_df = pd.DataFrame({
        'game_episode': test_episode_ids,
        'end_x': test_end_x,
        'end_y': test_end_y
    })

    # sample_submission 순서에 맞춰 정렬
    submission = sample_submission[['game_episode']].merge(
        submission_df, on='game_episode', how='left'
    )

    # NaN 확인
    nan_count = submission[['end_x', 'end_y']].isna().sum().sum()
    if nan_count > 0:
        print(f"Warning: {nan_count} NaN values in submission!")
        submission['end_x'] = submission['end_x'].fillna(test_end_x.mean())
        submission['end_y'] = submission['end_y'].fillna(test_end_y.mean())

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    submission_path = SUBMISSION_DIR / f'submission_seq_v3_{timestamp}.csv'
    submission.to_csv(submission_path, index=False)

    print(f"\nSubmission saved: {submission_path}")
    print(f"Submission shape: {submission.shape}")

    # 예측 통계
    print(f"\nPredicted end_x - Mean: {test_end_x.mean():.2f}, Std: {test_end_x.std():.2f}")
    print(f"Predicted end_y - Mean: {test_end_y.mean():.2f}, Std: {test_end_y.std():.2f}")

    # ========== 결과 저장 ==========
    results = {
        'cv_mean': float(cv_mean),
        'cv_std': float(cv_std),
        'oof_score': float(oof_score),
        'fold_scores': [float(s) for s in fold_scores],
        'config': CONFIG,
        'timestamp': timestamp
    }

    results_path = MODEL_DIR / f'seq_v3_results_{timestamp}.json'
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved: {results_path}")

    print("\n" + "=" * 60)
    print("학습 완료!")
    print(f"CV Score: {cv_mean:.4f} +/- {cv_std:.4f}")
    print(f"OOF Score: {oof_score:.4f}")
    print("=" * 60)

    return cv_mean, oof_score


if __name__ == "__main__":
    main()
