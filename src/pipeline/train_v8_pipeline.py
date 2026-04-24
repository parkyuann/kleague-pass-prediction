"""
K리그 패스 예측 - V8 Pipeline
=====================================
과적합 완화 전략:
1. 과적합 위험 피처 제거 (prev1_dist, angle_to_goal_diff, prev2_dy, goal_angle_x_prev_dy, last_dist_to_goal)
2. 정규화 강화 (num_leaves 감소, max_depth 감소, l2_leaf_reg 증가)
3. Y-flip 증강 제거 (dy 예측 방해 가능성)
4. 피처 상호작용 단순화

실행:
    python -m src.pipeline.train_v8_pipeline
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

# Field dimensions
FIELD_LENGTH = 105.0
FIELD_WIDTH = 68.0
GOAL_X = 105.0
GOAL_Y = 34.0

# Event type expected dx
EVENT_TYPE_DX_MEAN = {
    'Carry': 17.54, 'Pass': 12.48, 'Recovery': 9.36, 'Tackle': 7.23,
    'Throw-In': 4.00, 'Interception': 8.08, 'Duel': 1.25,
    'Pass_Corner': -3.46, 'Cross': 0.82, 'Pass_Freekick': 12.27,
    'Goal Kick': 16.89, 'Catch': 49.04, 'Intervention': 22.06,
    'Clearance': 62.42, 'Block': 0.0,
}


def load_raw_data():
    """Load raw data"""
    data_dir = Path('E:/Dacon/kleague-pass-prediction/data/raw')

    train = pd.read_csv(data_dir / 'train.csv')
    train['result_name'] = train['result_name'].fillna('None')

    match_info = pd.read_csv(data_dir / 'match_info.csv')

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


def extract_episode_features_v8(df: pd.DataFrame, is_test: bool = False) -> pd.DataFrame:
    """
    V8 Feature Extraction - Overfitting Mitigation

    Removed features (overfit risk):
    - prev1_dist (high dist shift + high importance)
    - angle_to_goal_diff (high dist shift + high importance)
    - prev2_dy (high dist shift)
    - goal_angle_x_prev_dy (high dist shift)
    - last_dist_to_goal (high dist shift)

    Simplified interactions:
    - Removed pos_x_prev_angle, pos_y_prev_dy

    Core stable features:
    - Position: last_start_x, last_start_y, normalized versions
    - Context: last_dist_from_center, last_goal_angle, pressure_score, side_position
    - Prev1 event: type, expected_dx, dx, dy, angle, forward, type_match
    - Interaction: pos_x_prev_dx only
    """

    features_list = []
    episodes = df['game_episode'].unique()

    for ep in tqdm(episodes, desc="Extracting V8 features"):
        ep_data = df[df['game_episode'] == ep].sort_values('action_id')
        last_row = ep_data.iloc[-1]
        n_events = len(ep_data)
        game_id = last_row['game_id']

        feat = {'game_episode': ep, 'game_id': game_id}

        # ============================================
        # 1. Position features (stable)
        # ============================================
        feat['last_start_x'] = last_row['start_x']
        feat['last_start_y'] = last_row['start_y']
        feat['last_start_x_norm'] = last_row['start_x'] / FIELD_LENGTH
        feat['last_start_y_norm'] = last_row['start_y'] / FIELD_WIDTH

        # ============================================
        # 2. Context features (stable)
        # ============================================
        feat['last_dist_from_center'] = abs(last_row['start_y'] - GOAL_Y)
        feat['last_goal_angle'] = np.arctan2(
            GOAL_Y - last_row['start_y'],
            GOAL_X - last_row['start_x']
        )
        # REMOVED: last_dist_to_goal (overfit risk)

        feat['pressure_score'] = last_row['start_x'] / FIELD_LENGTH
        feat['side_position'] = abs(last_row['start_y'] - GOAL_Y) / GOAL_Y

        # ============================================
        # 3. Previous event features - prev1 only (stable)
        # ============================================
        if n_events >= 2:
            prev_row = ep_data.iloc[-2]
            feat['prev1_type'] = prev_row['type_name']
            feat['prev1_expected_dx'] = EVENT_TYPE_DX_MEAN.get(prev_row['type_name'], 13.53)

            if pd.notna(prev_row['end_x']) and pd.notna(prev_row['end_y']):
                dx = prev_row['end_x'] - prev_row['start_x']
                dy = prev_row['end_y'] - prev_row['start_y']
                feat['prev1_dx'] = dx
                feat['prev1_dy'] = dy

                # Direction angle (stable)
                feat['prev1_angle'] = np.arctan2(dy, dx) if (dx != 0 or dy != 0) else 0

                # REMOVED: prev1_dist (overfit risk)
                # REMOVED: angle_to_goal_diff (overfit risk)

                # Forward flag (stable)
                feat['prev1_forward'] = int(dx > 2)
            else:
                feat['prev1_dx'] = 0
                feat['prev1_dy'] = 0
                feat['prev1_angle'] = 0
                feat['prev1_forward'] = 0

            # Type match (stable)
            feat['prev_type_match'] = int(prev_row['type_name'] == last_row['type_name'])
        else:
            feat['prev1_type'] = 'None'
            feat['prev1_expected_dx'] = 13.53
            feat['prev1_dx'] = 0
            feat['prev1_dy'] = 0
            feat['prev1_angle'] = 0
            feat['prev1_forward'] = 0
            feat['prev_type_match'] = 0

        # ============================================
        # 4. Interaction features (simplified)
        # ============================================
        # pos_x_prev_dx only (most stable interaction)
        feat['pos_x_prev_dx'] = feat['last_start_x_norm'] * feat['prev1_dx']

        # REMOVED: goal_angle_x_prev_dy (overfit risk)
        # REMOVED: pos_x_prev_angle (low importance)
        # REMOVED: pos_y_prev_dy (low importance)

        # ============================================
        # 5. prev2 - REMOVED (overfit risk)
        # ============================================
        # REMOVED: prev2_type, prev2_dy

        # ============================================
        # 6. Target
        # ============================================
        if not is_test:
            feat['target_dx'] = last_row['end_x'] - last_row['start_x']
            feat['target_dy'] = last_row['end_y'] - last_row['start_y']
            feat['target_x'] = last_row['end_x']
            feat['target_y'] = last_row['end_y']

        features_list.append(feat)

    result = pd.DataFrame(features_list)
    result = result.fillna(0)

    return result


def encode_categoricals(train_df: pd.DataFrame, test_df: pd.DataFrame):
    """Encode categorical variables"""
    type_cols = ['prev1_type']  # Only prev1_type (prev2_type removed)
    type_mapping = {}

    for col in type_cols:
        if col in train_df.columns:
            all_types = pd.concat([train_df[col], test_df[col]]).unique()
            type_mapping[col] = {v: i for i, v in enumerate(all_types)}
            train_df[col] = train_df[col].map(type_mapping[col])
            test_df[col] = test_df[col].map(type_mapping[col])

    return train_df, test_df, type_mapping


def calculate_euclidean_distance(pred_x, pred_y, true_x, true_y):
    return np.sqrt((pred_x - true_x)**2 + (pred_y - true_y)**2)


def clip_to_field(x, y):
    x = np.clip(x, 0, FIELD_LENGTH)
    y = np.clip(y, 0, FIELD_WIDTH)
    return x, y


def train_models_multi_seed(X, y, feature_cols, seeds=[42, 123, 456, 789, 1004]):
    """Multi-seed ensemble training with stronger regularization"""
    all_oof = []
    all_models = []

    for seed in seeds:
        print(f"\n=== Seed {seed} ===")
        kf = KFold(n_splits=5, shuffle=True, random_state=seed)

        oof_pred = np.zeros_like(y)
        models = {'lgb': [], 'xgb': [], 'cat': []}

        for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]

            # LightGBM - Stronger regularization
            lgb_params = {
                'objective': 'regression',
                'metric': 'rmse',
                'boosting_type': 'gbdt',
                'num_leaves': 31,  # V7: 63 -> V8: 31
                'max_depth': 5,    # Added explicit depth limit
                'learning_rate': 0.03,  # V7: 0.05 -> V8: 0.03 (slower)
                'feature_fraction': 0.8,  # V7: 0.9 -> V8: 0.8
                'bagging_fraction': 0.8,  # V7: 0.9 -> V8: 0.8
                'bagging_freq': 5,
                'min_data_in_leaf': 50,   # Added min samples
                'lambda_l2': 1.0,         # Added L2 regularization
                'verbose': -1,
                'seed': seed
            }

            train_data = lgb.Dataset(X_train, label=y_train)
            val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

            model_lgb = lgb.train(
                lgb_params, train_data,
                num_boost_round=1000,  # More rounds with slower LR
                valid_sets=[val_data],
                callbacks=[lgb.early_stopping(100), lgb.log_evaluation(0)]
            )
            models['lgb'].append(model_lgb)

            # XGBoost - Stronger regularization
            xgb_params = {
                'objective': 'reg:squarederror',
                'max_depth': 5,           # V7: 6 -> V8: 5
                'learning_rate': 0.03,    # V7: 0.05 -> V8: 0.03
                'subsample': 0.8,         # V7: 0.9 -> V8: 0.8
                'colsample_bytree': 0.8,  # V7: 0.9 -> V8: 0.8
                'min_child_weight': 5,    # Added
                'reg_lambda': 1.0,        # Added L2
                'reg_alpha': 0.1,         # Added L1
                'seed': seed,
                'verbosity': 0
            }

            dtrain = xgb.DMatrix(X_train, label=y_train)
            dval = xgb.DMatrix(X_val, label=y_val)

            model_xgb = xgb.train(
                xgb_params, dtrain,
                num_boost_round=1000,
                evals=[(dval, 'val')],
                early_stopping_rounds=100,
                verbose_eval=False
            )
            models['xgb'].append(model_xgb)

            # CatBoost - Stronger regularization
            cat_params = {
                'iterations': 1000,
                'learning_rate': 0.03,    # V7: 0.05 -> V8: 0.03
                'depth': 5,               # V7: 6 -> V8: 5
                'l2_leaf_reg': 5,         # V7: 3 -> V8: 5
                'min_data_in_leaf': 50,   # Added
                'random_seed': seed,
                'verbose': False,
                'early_stopping_rounds': 100
            }

            model_cat = CatBoostRegressor(**cat_params)
            model_cat.fit(X_train, y_train, eval_set=(X_val, y_val))
            models['cat'].append(model_cat)

            # Ensemble prediction
            pred_lgb = model_lgb.predict(X_val)
            pred_xgb = model_xgb.predict(xgb.DMatrix(X_val))
            pred_cat = model_cat.predict(X_val)

            oof_pred[val_idx] = (pred_lgb + pred_xgb + pred_cat) / 3

        all_oof.append(oof_pred)
        all_models.append(models)

    return all_oof, all_models


def main():
    print("=" * 60)
    print("K-League Pass Prediction - V8 Pipeline")
    print("Overfitting Mitigation Strategy")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    train, test, match_info = load_raw_data()
    print(f"Train rows: {len(train)}, Test rows: {len(test)}")

    # Feature extraction (V8: simplified features)
    print("\nExtracting V8 features...")
    train_features = extract_episode_features_v8(train, is_test=False)
    test_features = extract_episode_features_v8(test, is_test=True)

    print(f"Train episodes: {len(train_features)}")
    print(f"Test episodes: {len(test_features)}")

    # Categorical encoding
    train_features, test_features, _ = encode_categoricals(train_features, test_features)

    # NO DATA AUGMENTATION (Y-flip removed to prevent dy prediction interference)
    print("\nNo data augmentation (Y-flip removed)")
    train_combined = train_features.copy()

    # Feature/Target split
    exclude_cols = ['game_episode', 'game_id', 'target_dx', 'target_dy', 'target_x', 'target_y']
    feature_cols = [c for c in train_combined.columns if c not in exclude_cols]

    X = train_combined[feature_cols].values
    y_dx = train_combined['target_dx'].values
    y_dy = train_combined['target_dy'].values
    starts = train_combined[['last_start_x', 'last_start_y']].values

    print(f"\nFeature count: {len(feature_cols)} (V7: 22 -> V8: {len(feature_cols)})")
    print(f"\nFeatures used:")
    for i, col in enumerate(feature_cols):
        print(f"  {i+1}. {col}")

    # Training
    seeds = [42, 123, 456, 789, 1004, 2024, 3333]  # 7 seeds for more diversity
    print(f"\nTraining (Seeds: {seeds})...")

    # dx training
    print("\n=== dx Training ===")
    all_oof_dx, all_models_dx = train_models_multi_seed(X, y_dx, feature_cols, seeds)

    # dy training
    print("\n=== dy Training ===")
    all_oof_dy, all_models_dy = train_models_multi_seed(X, y_dy, feature_cols, seeds)

    # Ensemble OOF
    ensemble_oof_dx = np.mean(all_oof_dx, axis=0)
    ensemble_oof_dy = np.mean(all_oof_dy, axis=0)

    # Evaluate (no augmentation, so all data is original)
    pred_x = starts[:, 0] + ensemble_oof_dx
    pred_y = starts[:, 1] + ensemble_oof_dy
    pred_x, pred_y = clip_to_field(pred_x, pred_y)

    true_x = starts[:, 0] + y_dx
    true_y = starts[:, 1] + y_dy

    distances = calculate_euclidean_distance(pred_x, pred_y, true_x, true_y)
    cv_score = distances.mean()

    print("\n" + "=" * 40)
    print(f"V8 OOF Score: {cv_score:.4f}")
    print("=" * 40)

    # Test prediction
    print("\nPredicting test data...")
    X_test = test_features[feature_cols].values
    test_starts = test_features[['last_start_x', 'last_start_y']].values

    all_test_dx = []
    all_test_dy = []

    for seed_idx, (models_dx, models_dy) in enumerate(zip(all_models_dx, all_models_dy)):
        seed_pred_dx = []
        seed_pred_dy = []

        for fold in range(5):
            # dx
            pred_lgb = models_dx['lgb'][fold].predict(X_test)
            pred_xgb = models_dx['xgb'][fold].predict(xgb.DMatrix(X_test))
            pred_cat = models_dx['cat'][fold].predict(X_test)
            seed_pred_dx.append((pred_lgb + pred_xgb + pred_cat) / 3)

            # dy
            pred_lgb = models_dy['lgb'][fold].predict(X_test)
            pred_xgb = models_dy['xgb'][fold].predict(xgb.DMatrix(X_test))
            pred_cat = models_dy['cat'][fold].predict(X_test)
            seed_pred_dy.append((pred_lgb + pred_xgb + pred_cat) / 3)

        all_test_dx.append(np.mean(seed_pred_dx, axis=0))
        all_test_dy.append(np.mean(seed_pred_dy, axis=0))

    test_pred_dx = np.mean(all_test_dx, axis=0)
    test_pred_dy = np.mean(all_test_dy, axis=0)

    test_end_x = test_starts[:, 0] + test_pred_dx
    test_end_y = test_starts[:, 1] + test_pred_dy
    test_end_x, test_end_y = clip_to_field(test_end_x, test_end_y)

    # Save submission
    data_dir = Path('E:/Dacon/kleague-pass-prediction/data/raw')
    submission_dir = Path('E:/Dacon/kleague-pass-prediction/data/submissions')
    submission_dir.mkdir(exist_ok=True, parents=True)

    sample_submission = pd.read_csv(data_dir / 'sample_submission.csv')
    submission_df = pd.DataFrame({
        'game_episode': test_features['game_episode'],
        'end_x': test_end_x,
        'end_y': test_end_y
    })

    submission = sample_submission[['game_episode']].merge(
        submission_df, on='game_episode', how='left'
    )

    nan_count = submission[['end_x', 'end_y']].isna().sum().sum()
    if nan_count > 0:
        print(f"Warning: {nan_count} NaN values!")
        submission['end_x'] = submission['end_x'].fillna(test_end_x.mean())
        submission['end_y'] = submission['end_y'].fillna(test_end_y.mean())

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    submission_path = submission_dir / f'submission_v8_pipeline_{timestamp}.csv'
    submission.to_csv(submission_path, index=False)

    print(f"\nSubmission saved: {submission_path}")
    print(f"\nFinal Results:")
    print(f"  - Feature count: {len(feature_cols)} (V7: 22 -> V8: {len(feature_cols)})")
    print(f"  - Regularization: num_leaves=31, max_depth=5, l2_leaf_reg=5")
    print(f"  - Data augmentation: None (Y-flip removed)")
    print(f"  - Seeds: {len(seeds)}")
    print(f"  - CV Score: {cv_score:.4f}")

    return cv_score


if __name__ == "__main__":
    main()
