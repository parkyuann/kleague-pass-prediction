"""
K리그 패스 예측 - V3 Pipeline
=====================================
핵심 개선사항:
1. 상대 좌표(dx, dy) 예측 → 절대 좌표 변환
2. Y축 대칭 데이터 증강 (2x)
3. match_info.csv 연결 피처
4. 이벤트 타입별 예상 이동 거리 활용
5. 최근 이동 트렌드 피처 (상관관계 0.66)

목표: 타겟 분포 일치 (end_x 평균 ~68.45)
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
from sklearn.model_selection import KFold
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor
import warnings
warnings.filterwarnings('ignore')

# 시드 고정
SEED = 42
np.random.seed(SEED)

# 필드 크기
FIELD_LENGTH = 105.0
FIELD_WIDTH = 68.0
GOAL_X = 105.0
GOAL_Y = 34.0

# 이벤트 타입별 예상 dx (사전 분석 결과)
EVENT_TYPE_DX_MEAN = {
    'Carry': 17.54,
    'Pass': 12.48,
    'Recovery': 9.36,
    'Tackle': 7.23,
    'Throw-In': 4.00,
    'Interception': 8.08,
    'Duel': 1.25,
    'Pass_Corner': -3.46,
    'Cross': 0.82,
    'Pass_Freekick': 12.27,
    'Goal Kick': 16.89,
    'Catch': 49.04,
    'Intervention': 22.06,
    'Clearance': 62.42,
    'Block': 0.0,
}


def load_raw_data():
    """원본 데이터 로드"""
    data_dir = Path('E:/Dacon/kleague-pass-prediction/data/raw')

    # Train
    train = pd.read_csv(data_dir / 'train.csv')
    train['result_name'] = train['result_name'].fillna('None')

    # Match info
    match_info = pd.read_csv(data_dir / 'match_info.csv')

    # Test
    test_dir = data_dir / 'test'
    test_list = []
    for game_folder in test_dir.iterdir():
        if game_folder.is_dir():
            for csv_file in game_folder.glob('*.csv'):
                df = pd.read_csv(csv_file)
                df['result_name'] = df['result_name'].fillna('None')
                test_list.append(df)

    test = pd.concat(test_list, ignore_index=True)

    return train, test, match_info


def extract_episode_features(df: pd.DataFrame, is_test: bool = False) -> pd.DataFrame:
    """에피소드별 피처 추출 (상대 좌표 예측용)"""

    features_list = []
    episodes = df['game_episode'].unique()

    for ep in tqdm(episodes, desc="Extracting features"):
        ep_data = df[df['game_episode'] == ep].sort_values('action_id')
        last_row = ep_data.iloc[-1]
        n_events = len(ep_data)

        # === 기본 정보 ===
        feat = {
            'game_episode': ep,
            'game_id': last_row['game_id'],
        }

        # === 마지막 이벤트 좌표 (예측 기준점) ===
        feat['last_start_x'] = last_row['start_x']
        feat['last_start_y'] = last_row['start_y']
        feat['last_start_x_norm'] = last_row['start_x'] / FIELD_LENGTH
        feat['last_start_y_norm'] = last_row['start_y'] / FIELD_WIDTH

        # === 마지막 이벤트 컨텍스트 ===
        feat['last_dist_to_goal'] = np.sqrt(
            (GOAL_X - last_row['start_x'])**2 + (GOAL_Y - last_row['start_y'])**2
        )
        feat['last_goal_angle'] = np.arctan2(
            GOAL_Y - last_row['start_y'],
            GOAL_X - last_row['start_x']
        )
        feat['last_in_penalty_area'] = int(
            last_row['start_x'] >= 88.5 and
            13.84 <= last_row['start_y'] <= 54.16
        )
        feat['last_dist_from_center'] = abs(last_row['start_y'] - GOAL_Y)

        # === 경기 정보 ===
        feat['is_home'] = int(last_row['is_home'])
        feat['period_id'] = last_row['period_id']
        feat['time_seconds'] = last_row['time_seconds']
        feat['time_minutes'] = last_row['time_seconds'] / 60

        # === 마지막 이벤트 타입 정보 ===
        feat['last_type'] = last_row['type_name']
        feat['last_expected_dx'] = EVENT_TYPE_DX_MEAN.get(last_row['type_name'], 13.53)

        # === 직전 이벤트 정보 (핵심!) ===
        if n_events >= 2:
            prev_row = ep_data.iloc[-2]
            feat['prev_type'] = prev_row['type_name']
            feat['prev_expected_dx'] = EVENT_TYPE_DX_MEAN.get(prev_row['type_name'], 13.53)

            # 직전 이벤트의 이동
            if pd.notna(prev_row['end_x']) and pd.notna(prev_row['end_y']):
                feat['prev_dx'] = prev_row['end_x'] - prev_row['start_x']
                feat['prev_dy'] = prev_row['end_y'] - prev_row['start_y']
            else:
                feat['prev_dx'] = 0
                feat['prev_dy'] = 0
        else:
            feat['prev_type'] = 'None'
            feat['prev_expected_dx'] = 13.53
            feat['prev_dx'] = 0
            feat['prev_dy'] = 0

        # === 최근 이동 트렌드 (마지막 이벤트 제외 - 타겟 누수 방지!) ===
        recent_dx_list = []
        recent_dy_list = []
        # 마지막 이벤트(예측 대상)를 제외하고 직전 이벤트들만 사용
        for i in range(1, min(6, n_events)):  # i=1부터 시작 (마지막 제외)
            row = ep_data.iloc[-(i+1)]
            if pd.notna(row['end_x']) and pd.notna(row['end_y']):
                recent_dx_list.append(row['end_x'] - row['start_x'])
                recent_dy_list.append(row['end_y'] - row['start_y'])

        if len(recent_dx_list) >= 3:
            feat['recent_3_dx_mean'] = np.mean(recent_dx_list[:3])
            feat['recent_3_dy_mean'] = np.mean(recent_dy_list[:3])
        else:
            feat['recent_3_dx_mean'] = np.mean(recent_dx_list) if recent_dx_list else 0
            feat['recent_3_dy_mean'] = np.mean(recent_dy_list) if recent_dy_list else 0

        if len(recent_dx_list) >= 5:
            feat['recent_5_dx_mean'] = np.mean(recent_dx_list[:5])
            feat['recent_5_dy_mean'] = np.mean(recent_dy_list[:5])
        else:
            feat['recent_5_dx_mean'] = feat['recent_3_dx_mean']
            feat['recent_5_dy_mean'] = feat['recent_3_dy_mean']

        # === 시퀀스 통계 ===
        feat['seq_length'] = n_events
        feat['avg_x'] = ep_data['start_x'].mean()
        feat['avg_y'] = ep_data['start_y'].mean()
        feat['std_x'] = ep_data['start_x'].std() if n_events > 1 else 0
        feat['std_y'] = ep_data['start_y'].std() if n_events > 1 else 0
        feat['x_range'] = ep_data['start_x'].max() - ep_data['start_x'].min()
        feat['y_range'] = ep_data['start_y'].max() - ep_data['start_y'].min()

        # === 공격 진행도 ===
        feat['attack_progress'] = last_row['start_x'] - ep_data['start_x'].iloc[0]

        # === 이벤트 타입 통계 ===
        feat['pass_ratio'] = (ep_data['type_name'] == 'Pass').mean()
        feat['carry_ratio'] = (ep_data['type_name'] == 'Carry').mean()

        # === 필드 존 피처 ===
        # X존 (수비/중원/공격)
        if last_row['start_x'] < 35:
            feat['zone_x'] = 0  # 수비
        elif last_row['start_x'] < 70:
            feat['zone_x'] = 1  # 중원
        else:
            feat['zone_x'] = 2  # 공격

        # Y존 (좌/중/우)
        if last_row['start_y'] < 22.67:
            feat['zone_y'] = 0  # 좌
        elif last_row['start_y'] < 45.33:
            feat['zone_y'] = 1  # 중
        else:
            feat['zone_y'] = 2  # 우

        # === 타겟 (상대 좌표!) ===
        if not is_test:
            feat['target_dx'] = last_row['end_x'] - last_row['start_x']
            feat['target_dy'] = last_row['end_y'] - last_row['start_y']
            feat['target_x'] = last_row['end_x']
            feat['target_y'] = last_row['end_y']

        features_list.append(feat)

    result = pd.DataFrame(features_list)
    result = result.fillna(0)

    return result


def augment_y_symmetry(df: pd.DataFrame) -> pd.DataFrame:
    """Y축 대칭 데이터 증강"""
    augmented = df.copy()

    # Y 관련 피처 대칭 변환
    y_features_flip = ['last_start_y', 'avg_y']
    y_features_norm_flip = ['last_start_y_norm']
    dy_features_negate = ['prev_dy', 'recent_3_dy_mean', 'recent_5_dy_mean', 'target_dy']

    for col in y_features_flip:
        if col in augmented.columns:
            augmented[col] = FIELD_WIDTH - augmented[col]

    for col in y_features_norm_flip:
        if col in augmented.columns:
            augmented[col] = 1.0 - augmented[col]

    for col in dy_features_negate:
        if col in augmented.columns:
            augmented[col] = -augmented[col]

    # dist_from_center는 그대로
    # goal_angle 부호 반전
    if 'last_goal_angle' in augmented.columns:
        augmented['last_goal_angle'] = -augmented['last_goal_angle']

    # target_y 대칭
    if 'target_y' in augmented.columns:
        augmented['target_y'] = FIELD_WIDTH - augmented['target_y']

    # zone_y 반전 (0↔2, 1은 그대로)
    if 'zone_y' in augmented.columns:
        augmented['zone_y'] = augmented['zone_y'].map({0: 2, 1: 1, 2: 0})

    # game_episode 구분
    augmented['game_episode'] = augmented['game_episode'].astype(str) + '_aug'

    return augmented


def encode_categoricals(train_df: pd.DataFrame, test_df: pd.DataFrame):
    """범주형 인코딩"""
    cat_cols = ['last_type', 'prev_type']

    for col in cat_cols:
        if col in train_df.columns and col in test_df.columns:
            all_vals = list(set(train_df[col].unique()) | set(test_df[col].unique()))
            val_to_idx = {v: i for i, v in enumerate(all_vals)}
            train_df[f'{col}_enc'] = train_df[col].map(val_to_idx)
            test_df[f'{col}_enc'] = test_df[col].map(val_to_idx)

    return train_df, test_df


def get_feature_cols():
    """학습에 사용할 피처 컬럼"""
    return [
        # 위치 피처
        'last_start_x', 'last_start_y',
        'last_start_x_norm', 'last_start_y_norm',
        'last_dist_to_goal', 'last_goal_angle',
        'last_in_penalty_area', 'last_dist_from_center',

        # 시간/경기 피처
        'is_home', 'period_id', 'time_minutes',

        # 이벤트 타입 피처
        'last_expected_dx', 'prev_expected_dx',
        'last_type_enc', 'prev_type_enc',

        # 이동 피처 (핵심!)
        'prev_dx', 'prev_dy',
        'recent_3_dx_mean', 'recent_3_dy_mean',
        'recent_5_dx_mean', 'recent_5_dy_mean',

        # 시퀀스 통계
        'seq_length', 'avg_x', 'avg_y',
        'std_x', 'std_y', 'x_range', 'y_range',
        'attack_progress',

        # 이벤트 비율
        'pass_ratio', 'carry_ratio',

        # 존 피처
        'zone_x', 'zone_y',
    ]


def train_models(X_train, y_train_dx, y_train_dy, X_test):
    """앙상블 모델 학습 (LightGBM, XGBoost, CatBoost)"""

    kf = KFold(n_splits=5, shuffle=True, random_state=SEED)

    oof_dx = np.zeros(len(X_train))
    oof_dy = np.zeros(len(X_train))
    test_dx = np.zeros(len(X_test))
    test_dy = np.zeros(len(X_test))

    # 각 모델별 예측 저장
    test_preds = {'lgb_dx': [], 'lgb_dy': [], 'xgb_dx': [], 'xgb_dy': [], 'cat_dx': [], 'cat_dy': []}

    for fold, (tr_idx, va_idx) in enumerate(kf.split(X_train)):
        print(f"\n  Fold {fold+1}/5")

        X_tr, X_va = X_train[tr_idx], X_train[va_idx]
        y_tr_dx, y_va_dx = y_train_dx[tr_idx], y_train_dx[va_idx]
        y_tr_dy, y_va_dy = y_train_dy[tr_idx], y_train_dy[va_idx]

        # === LightGBM ===
        lgb_dx = lgb.LGBMRegressor(
            n_estimators=1000, max_depth=7, learning_rate=0.03,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=0.1,
            random_state=SEED, verbose=-1
        )
        lgb_dy = lgb.LGBMRegressor(
            n_estimators=1000, max_depth=7, learning_rate=0.03,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=0.1,
            random_state=SEED, verbose=-1
        )

        lgb_dx.fit(X_tr, y_tr_dx, eval_set=[(X_va, y_va_dx)],
                   callbacks=[lgb.early_stopping(100, verbose=False)])
        lgb_dy.fit(X_tr, y_tr_dy, eval_set=[(X_va, y_va_dy)],
                   callbacks=[lgb.early_stopping(100, verbose=False)])

        # === XGBoost ===
        xgb_dx = xgb.XGBRegressor(
            n_estimators=1000, max_depth=6, learning_rate=0.03,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=0.1,
            early_stopping_rounds=100,
            random_state=SEED, verbosity=0
        )
        xgb_dy = xgb.XGBRegressor(
            n_estimators=1000, max_depth=6, learning_rate=0.03,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=0.1,
            early_stopping_rounds=100,
            random_state=SEED, verbosity=0
        )

        xgb_dx.fit(X_tr, y_tr_dx, eval_set=[(X_va, y_va_dx)], verbose=False)
        xgb_dy.fit(X_tr, y_tr_dy, eval_set=[(X_va, y_va_dy)], verbose=False)

        # === CatBoost ===
        cat_dx = CatBoostRegressor(
            iterations=1000, depth=6, learning_rate=0.03,
            random_seed=SEED, verbose=0
        )
        cat_dy = CatBoostRegressor(
            iterations=1000, depth=6, learning_rate=0.03,
            random_seed=SEED, verbose=0
        )

        cat_dx.fit(X_tr, y_tr_dx, eval_set=(X_va, y_va_dx),
                   early_stopping_rounds=100)
        cat_dy.fit(X_tr, y_tr_dy, eval_set=(X_va, y_va_dy),
                   early_stopping_rounds=100)

        # OOF 예측 (앙상블)
        pred_dx = (lgb_dx.predict(X_va) + xgb_dx.predict(X_va) + cat_dx.predict(X_va)) / 3
        pred_dy = (lgb_dy.predict(X_va) + xgb_dy.predict(X_va) + cat_dy.predict(X_va)) / 3
        oof_dx[va_idx] = pred_dx
        oof_dy[va_idx] = pred_dy

        # 테스트 예측
        test_preds['lgb_dx'].append(lgb_dx.predict(X_test))
        test_preds['lgb_dy'].append(lgb_dy.predict(X_test))
        test_preds['xgb_dx'].append(xgb_dx.predict(X_test))
        test_preds['xgb_dy'].append(xgb_dy.predict(X_test))
        test_preds['cat_dx'].append(cat_dx.predict(X_test))
        test_preds['cat_dy'].append(cat_dy.predict(X_test))

    # 테스트 앙상블 (폴드 평균)
    test_dx = (
        np.mean(test_preds['lgb_dx'], axis=0) +
        np.mean(test_preds['xgb_dx'], axis=0) +
        np.mean(test_preds['cat_dx'], axis=0)
    ) / 3
    test_dy = (
        np.mean(test_preds['lgb_dy'], axis=0) +
        np.mean(test_preds['xgb_dy'], axis=0) +
        np.mean(test_preds['cat_dy'], axis=0)
    ) / 3

    return oof_dx, oof_dy, test_dx, test_dy


def main():
    print("=" * 70)
    print("K리그 패스 예측 V3 Pipeline")
    print("=" * 70)
    print("핵심 전략:")
    print("  1. 상대 좌표(dx, dy) 예측 → 절대 좌표 변환")
    print("  2. Y축 대칭 데이터 증강 (2x)")
    print("  3. 이벤트 타입별 예상 dx 활용")
    print("  4. 최근 이동 트렌드 피처 (상관관계 0.66)")
    print("=" * 70)

    # 1. 데이터 로드
    print("\n[1/6] 데이터 로드...")
    train_raw, test_raw, match_info = load_raw_data()
    print(f"  Train events: {len(train_raw)}")
    print(f"  Test events: {len(test_raw)}")

    # 2. 에피소드별 피처 추출
    print("\n[2/6] 에피소드별 피처 추출...")
    train_episodes = extract_episode_features(train_raw, is_test=False)
    test_episodes = extract_episode_features(test_raw, is_test=True)
    print(f"  Train episodes: {len(train_episodes)}")
    print(f"  Test episodes: {len(test_episodes)}")

    # 타겟 분포 확인
    print(f"\n  Train target_dx 평균: {train_episodes['target_dx'].mean():.2f}")
    print(f"  Train target_dy 평균: {train_episodes['target_dy'].mean():.2f}")
    print(f"  Train target_x 평균: {train_episodes['target_x'].mean():.2f}")

    # 3. Y축 대칭 증강
    print("\n[3/6] Y축 대칭 데이터 증강...")
    train_aug = augment_y_symmetry(train_episodes)
    train_combined = pd.concat([train_episodes, train_aug], ignore_index=True)
    print(f"  증강 후 Train episodes: {len(train_combined)} (x2)")

    # 증강 검증
    print(f"  증강 후 target_dy 평균: {train_combined['target_dy'].mean():.4f} (목표: ~0)")

    # 4. 범주형 인코딩
    print("\n[4/6] 범주형 인코딩...")
    train_combined, test_episodes = encode_categoricals(train_combined, test_episodes)

    # 5. 피처 준비
    print("\n[5/6] 모델 학습...")
    feature_cols = get_feature_cols()
    print(f"  피처 수: {len(feature_cols)}")

    X_train = train_combined[feature_cols].values.astype(np.float32)
    y_train_dx = train_combined['target_dx'].values.astype(np.float32)
    y_train_dy = train_combined['target_dy'].values.astype(np.float32)
    X_test = test_episodes[feature_cols].values.astype(np.float32)

    # 시작 좌표 (변환용)
    start_x_train = train_combined['last_start_x'].values
    start_y_train = train_combined['last_start_y'].values
    start_x_test = test_episodes['last_start_x'].values
    start_y_test = test_episodes['last_start_y'].values

    # 모델 학습
    oof_dx, oof_dy, test_dx, test_dy = train_models(
        X_train, y_train_dx, y_train_dy, X_test
    )

    # 6. 평가 및 제출
    print("\n[6/6] 평가 및 제출 파일 생성...")

    # OOF를 절대 좌표로 변환
    oof_end_x = np.clip(start_x_train + oof_dx, 0, FIELD_LENGTH)
    oof_end_y = np.clip(start_y_train + oof_dy, 0, FIELD_WIDTH)

    target_x = train_combined['target_x'].values
    target_y = train_combined['target_y'].values

    eucl_dist = np.sqrt((oof_end_x - target_x)**2 + (oof_end_y - target_y)**2).mean()
    print(f"\n  CV 유클리디안 거리: {eucl_dist:.4f}")

    print(f"\n  OOF dx 평균: {oof_dx.mean():.2f} (목표: {train_combined['target_dx'].mean():.2f})")
    print(f"  OOF dy 평균: {oof_dy.mean():.2f} (목표: {train_combined['target_dy'].mean():.2f})")
    print(f"  OOF end_x 평균: {oof_end_x.mean():.2f} (목표: {target_x.mean():.2f})")

    # 테스트 예측을 절대 좌표로 변환
    test_end_x = np.clip(start_x_test + test_dx, 0, FIELD_LENGTH)
    test_end_y = np.clip(start_y_test + test_dy, 0, FIELD_WIDTH)

    print(f"\n  Test dx 평균: {test_dx.mean():.2f}")
    print(f"  Test dy 평균: {test_dy.mean():.2f}")
    print(f"  Test end_x 평균: {test_end_x.mean():.2f} (목표: ~68)")
    print(f"  Test end_y 평균: {test_end_y.mean():.2f} (목표: ~34)")

    # 제출 파일 생성
    sample_sub = pd.read_csv('E:/Dacon/kleague-pass-prediction/data/raw/sample_submission.csv')

    # game_episode 순서 맞추기
    test_ep_to_idx = {ep: i for i, ep in enumerate(test_episodes['game_episode'])}

    final_x = []
    final_y = []
    for ep in sample_sub['game_episode']:
        idx = test_ep_to_idx[ep]
        final_x.append(test_end_x[idx])
        final_y.append(test_end_y[idx])

    submission = sample_sub.copy()
    submission['end_x'] = final_x
    submission['end_y'] = final_y

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_path = f'E:/Dacon/kleague-pass-prediction/data/submissions/submission_v3_{timestamp}.csv'
    submission.to_csv(save_path, index=False)

    print(f"\n  저장: {save_path}")
    print(f"  제출 end_x 평균: {submission['end_x'].mean():.2f}")
    print(f"  제출 end_y 평균: {submission['end_y'].mean():.2f}")
    print("=" * 70)

    return eucl_dist


if __name__ == "__main__":
    main()
