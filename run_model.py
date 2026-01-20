"""
K리그 패스 예측 - V8 Pipeline (Tuned Version)
===========================================================
[적용된 튜닝 사항]
1. 하이퍼파라미터 강화 (Numbers Tuned):
   - Learning Rate: 0.03 -> 0.01 (더 꼼꼼하게 학습)
   - Estimators/Iterations: 1000 -> 3000 (더 오래 학습)
   - Model Depth/Leaves: 복잡도 증가 (더 똑똑하게)
2. Feature Engineering:
   - 직전 패스 거리(prev1_dist) 포함
3. 기본 설정:
   - AppleGothic 폰트 적용
   - 메타 파일 자동 로딩
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
import matplotlib.pyplot as plt
import warnings
import os 
import sys

# 경고 무시
warnings.filterwarnings('ignore')

# --- 폰트 설정 (맥북용) ---
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# --- 상수 설정 ---
FIELD_LENGTH = 105.0
FIELD_WIDTH = 68.0
GOAL_X = 105.0
GOAL_Y = 34.0

EVENT_TYPE_DX_MEAN = {
    'Carry': 17.54, 'Pass': 12.48, 'Recovery': 9.36, 'Tackle': 7.23,
    'Throw-In': 4.00, 'Interception': 8.08, 'Duel': 1.25,
    'Pass_Corner': -3.46, 'Cross': 0.82, 'Pass_Freekick': 12.27,
    'Goal Kick': 16.89, 'Catch': 49.04, 'Intervention': 22.06,
    'Clearance': 62.42, 'Block': 0.0,
}

# --- 헬퍼 함수 ---

def check_and_fix_columns(df, name="Data"):
    """컬럼 이름 진단 및 자동 수정 함수"""
    rename_map = {
        'x': 'start_x', 'X': 'start_x', 'location_x': 'start_x',
        'y': 'start_y', 'Y': 'start_y', 'location_y': 'start_y',
        'Time': 'play_time', 'time': 'play_time'
    }
    actual_rename = {k: v for k, v in rename_map.items() if k in df.columns and v not in df.columns}
    if actual_rename:
        print(f"   👉 [{name}] 컬럼 이름 자동 변경: {actual_rename}")
        df = df.rename(columns=actual_rename)
    return df

def load_raw_data():
    """Load raw data with Metadata Handling"""
    if os.path.exists('train.csv') and os.path.exists('test.csv'):
        base_path = './'
        print("📂 현재 폴더에서 데이터를 찾았습니다.")
    else:
        
        base_path = '/Users/chaeyoung/kleague-pass-prediction/2 step/'
        print(f"📂 지정된 경로({base_path})에서 데이터를 찾습니다.")

    print("⏳ 데이터 로딩 중...")
    try:
        try:
            train = pd.read_csv(f'{base_path}train.csv', engine='pyarrow')
        except:
            train = pd.read_csv(f'{base_path}train.csv')
        print(f"   -> Train 로드 완료 ({len(train)} rows)")

        match_info = pd.read_csv(f'{base_path}match_info.csv')

        try:
            test_temp = pd.read_csv(f'{base_path}test.csv')
        except FileNotFoundError:
            print(f"❌ 에러: test.csv 파일을 찾을 수 없습니다. 경로: {base_path}")
            raise

        if 'start_x' in test_temp.columns:
            print("   -> Test 파일이 단일 데이터 파일입니다.")
            test = test_temp
        else:
            print("   -> 📂 'test.csv'는 메타 파일입니다. 개별 CSV 로딩 중...")
            if 'path' not in test_temp.columns:
                raise ValueError("test.csv에 'path' 컬럼이 없습니다.")
            
            # 경로 수정 및 파일 로드
            file_paths = [os.path.join(base_path, p.replace('./', '')) for p in test_temp['path']]
            dfs = []
            
            # 진행률 표시를 위해 tqdm 사용
            for p in tqdm(file_paths, desc="   Reading CSVs"):
                try:
                    dfs.append(pd.read_csv(p))
                except:
                    pass
            
            if len(dfs) == 0: raise ValueError("Test 파일들을 하나도 로드하지 못했습니다.")
            test = pd.concat(dfs, ignore_index=True)
            print(f"   -> Test 병합 완료 ({len(test)} rows)")
            
    except Exception as e:
        print(f"\n❌ 데이터 로드 중 오류: {e}")
        raise

    train = check_and_fix_columns(train, "Train")
    test = check_and_fix_columns(test, "Test")

    if 'result_name' in train.columns: train['result_name'] = train['result_name'].fillna('None')
    if 'result_name' in test.columns: test['result_name'] = test['result_name'].fillna('None')

    if 'action_id' not in train.columns: train['action_id'] = train.index
    if 'action_id' not in test.columns: test['action_id'] = test.index
    
    return train, test, match_info, base_path

def extract_episode_features_v8(df: pd.DataFrame, is_test: bool = False) -> pd.DataFrame:
    features_list = []
    episodes = df['game_episode'].unique()

    if 'start_x' not in df.columns: raise KeyError("'start_x' 컬럼 없음")

    for ep in tqdm(episodes, desc="Extracting Features"):
        ep_data = df[df['game_episode'] == ep].sort_values('action_id')
        if len(ep_data) == 0: continue
            
        last_row = ep_data.iloc[-1]
        n_events = len(ep_data)
        game_id = last_row.get('game_id', 0) 

        feat = {'game_episode': ep, 'game_id': game_id}

        # 1. Position features
        feat['last_start_x'] = last_row['start_x']
        feat['last_start_y'] = last_row['start_y']
        feat['last_start_x_norm'] = last_row['start_x'] / FIELD_LENGTH
        feat['last_start_y_norm'] = last_row['start_y'] / FIELD_WIDTH

        # 2. Context features
        feat['last_dist_from_center'] = abs(last_row['start_y'] - GOAL_Y)
        feat['last_goal_angle'] = np.arctan2(GOAL_Y - last_row['start_y'], GOAL_X - last_row['start_x'])
        feat['pressure_score'] = last_row['start_x'] / FIELD_LENGTH
        feat['side_position'] = abs(last_row['start_y'] - GOAL_Y) / GOAL_Y

        # 3. Previous event
        if n_events >= 2:
            prev_row = ep_data.iloc[-2]
            feat['prev1_type'] = prev_row.get('type_name', 'None')
            feat['prev1_expected_dx'] = EVENT_TYPE_DX_MEAN.get(feat['prev1_type'], 13.53)

            if 'end_x' in prev_row and pd.notna(prev_row['end_x']) and pd.notna(prev_row['end_y']):
                dx = prev_row['end_x'] - prev_row['start_x']
                dy = prev_row['end_y'] - prev_row['start_y']
                feat['prev1_dx'] = dx
                feat['prev1_dy'] = dy
                # ★ [New] 직전 패스 거리 추가 (거리 정보 강화)
                feat['prev1_dist'] = np.sqrt(dx**2 + dy**2)
                feat['prev1_angle'] = np.arctan2(dy, dx) if (dx != 0 or dy != 0) else 0
                feat['prev1_forward'] = int(dx > 2)
            else:
                feat['prev1_dx'] = 0
                feat['prev1_dy'] = 0
                feat['prev1_dist'] = 0
                feat['prev1_angle'] = 0
                feat['prev1_forward'] = 0

            curr_type = last_row.get('type_name', 'None')
            prev_type = prev_row.get('type_name', 'None')
            feat['prev_type_match'] = int(prev_type == curr_type)
        else:
            feat['prev1_type'] = 'None'
            feat['prev1_expected_dx'] = 13.53
            feat['prev1_dx'] = 0
            feat['prev1_dy'] = 0
            feat['prev1_dist'] = 0
            feat['prev1_angle'] = 0
            feat['prev1_forward'] = 0
            feat['prev_type_match'] = 0

        # 4. Interaction
        feat['pos_x_prev_dx'] = feat['last_start_x_norm'] * feat['prev1_dx']

        # 6. Target
        if not is_test:
            feat['target_dx'] = last_row['end_x'] - last_row['start_x']
            feat['target_dy'] = last_row['end_y'] - last_row['start_y']
            feat['target_x'] = last_row['end_x']
            feat['target_y'] = last_row['end_y']

        features_list.append(feat)

    result = pd.DataFrame(features_list)
    result = result.fillna(0)
    return result

def encode_categoricals(train_df, test_df):
    type_cols = ['prev1_type']
    type_mapping = {}
    for col in type_cols:
        if col in train_df.columns:
            all_types = pd.concat([train_df[col], test_df[col]]).unique()
            type_mapping[col] = {v: i for i, v in enumerate(all_types)}
            train_df[col] = train_df[col].map(type_mapping[col])
            test_df[col] = test_df[col].map(type_mapping[col])
    return train_df, test_df, type_mapping

def clip_to_field(x, y):
    x = np.clip(x, 0, FIELD_LENGTH)
    y = np.clip(y, 0, FIELD_WIDTH)
    return x, y

def train_models_multi_seed(X, y, feature_cols, seeds=[42, 123, 456, 789, 1004]):
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

            # ------------------------------------------------
            # ★ [Tuning] LightGBM 파라미터 강화
            # ------------------------------------------------
            lgb_params = {
                'objective': 'regression', 'metric': 'rmse', 'verbosity': -1, 'seed': seed,
                'num_leaves': 63,        # 기존 31 -> 63 (더 똑똑하게)
                'max_depth': -1,         # 깊이 제한 해제
                'learning_rate': 0.01,   # 기존 0.03 -> 0.01 (더 꼼꼼하게)
                'n_estimators': 3000,    # 기존 1000 -> 3000 (더 오래)
                'min_data_in_leaf': 50, 'lambda_l2': 1.0,
                'feature_fraction': 0.8, 'bagging_fraction': 0.8, 'bagging_freq': 5
            }
            # num_boost_round는 params가 아니라 train 함수 인자로 전달
            train_data = lgb.Dataset(X_train, label=y_train)
            val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
            
            model_lgb = lgb.train(lgb_params, train_data, num_boost_round=3000, 
                                valid_sets=[val_data], 
                                callbacks=[lgb.early_stopping(200), lgb.log_evaluation(0)]) # early_stopping 여유 있게
            models['lgb'].append(model_lgb)

            # ------------------------------------------------
            # ★ [Tuning] XGBoost 파라미터 강화
            # ------------------------------------------------
            xgb_params = {
                'objective': 'reg:squarederror', 'verbosity': 0, 'seed': seed,
                'max_depth': 6,          # 기존 5 -> 6 (약간 더 깊게)
                'learning_rate': 0.01,   # 기존 0.03 -> 0.01
                'n_estimators': 3000,    # 기존 1000 -> 3000
                'subsample': 0.8, 'colsample_bytree': 0.8,
                'min_child_weight': 5, 'reg_lambda': 1.0, 'reg_alpha': 0.1
            }
            dtrain = xgb.DMatrix(X_train, label=y_train)
            dval = xgb.DMatrix(X_val, label=y_val)
            model_xgb = xgb.train(xgb_params, dtrain, num_boost_round=3000, 
                                evals=[(dval, 'val')], early_stopping_rounds=200, verbose_eval=False)
            models['xgb'].append(model_xgb)

            # ------------------------------------------------
            # ★ [Tuning] CatBoost 파라미터 강화
            # ------------------------------------------------
            cat_params = {
                'iterations': 3000,      # 기존 1000 -> 3000
                'learning_rate': 0.01,   # 기존 0.03 -> 0.01
                'depth': 6,              # 기존 5 -> 6
                'l2_leaf_reg': 5, 'min_data_in_leaf': 50, 'random_seed': seed, 
                'verbose': False, 'early_stopping_rounds': 200
            }
            model_cat = CatBoostRegressor(**cat_params)
            model_cat.fit(X_train, y_train, eval_set=(X_val, y_val))
            models['cat'].append(model_cat)

            # Ensemble (가중 평균 예시: LGBM이 보통 성능이 좋으므로 가중치를 조금 더 줌)
            p_lgb = model_lgb.predict(X_val)
            p_xgb = model_xgb.predict(xgb.DMatrix(X_val))
            p_cat = model_cat.predict(X_val)
            
            # 성능에 따라 가중치 조절 가능 (현재는 안전하게 1:1:1)
            oof_pred[val_idx] = (p_lgb + p_xgb + p_cat) / 3

        all_oof.append(oof_pred)
        all_models.append(models)
    return all_oof, all_models

def main():
    print("=" * 60)
    print("K-League Pass Prediction - V8 Pipeline (Tuned)")
    print("=" * 60)

    # 1. Load Data
    train, test, match_info, base_path_str = load_raw_data()
    print(f"Train rows: {len(train)}, Test rows: {len(test)}")

    # 2. Extract Features
    print("\nExtracting features...")
    train_features = extract_episode_features_v8(train, is_test=False)
    test_features = extract_episode_features_v8(test, is_test=True)
    
    train_features, test_features, _ = encode_categoricals(train_features, test_features)

    # 3. Prepare Training
    exclude_cols = ['game_episode', 'game_id', 'target_dx', 'target_dy', 'target_x', 'target_y', 'action_id', 'result_name']
    feature_cols = [c for c in train_features.columns if c not in exclude_cols]
    
    X = train_features[feature_cols].values
    y_dx = train_features['target_dx'].values
    y_dy = train_features['target_dy'].values
    starts = train_features[['last_start_x', 'last_start_y']].values
    
    print(f"\nFeature count: {len(feature_cols)}")
    seeds = [42, 123, 456, 789, 1004]

    # 4. Train
    print("\n=== dx Training ===")
    all_oof_dx, all_models_dx = train_models_multi_seed(X, y_dx, feature_cols, seeds=seeds)
    print("\n=== dy Training ===")
    all_oof_dy, all_models_dy = train_models_multi_seed(X, y_dy, feature_cols, seeds=seeds)

    # 5. Predict & Submit
    ensemble_dx = np.mean(all_oof_dx, axis=0)
    ensemble_dy = np.mean(all_oof_dy, axis=0)
    
    pred_x_oof, pred_y_oof = clip_to_field(starts[:,0] + ensemble_dx, starts[:,1] + ensemble_dy)
    true_x = starts[:,0] + y_dx
    true_y = starts[:,1] + y_dy
    score = np.sqrt((pred_x_oof - true_x)**2 + (pred_y_oof - true_y)**2).mean()
    print(f"\n" + "="*40)
    print(f"✅ V8 OOF Score (Tuned): {score:.4f}")
    print("="*40)

    # Test Prediction
    print("\nPredicting test set...")
    X_test = test_features[feature_cols].values
    test_starts = test_features[['last_start_x', 'last_start_y']].values
    
    final_test_dx = np.zeros(len(X_test))
    final_test_dy = np.zeros(len(X_test))
    
    for i in range(len(seeds)):
        seed_dx = np.zeros(len(X_test))
        seed_dy = np.zeros(len(X_test))
        for fold in range(5):
            # dx
            p_lgb = all_models_dx[i]['lgb'][fold].predict(X_test)
            p_xgb = all_models_dx[i]['xgb'][fold].predict(xgb.DMatrix(X_test))
            p_cat = all_models_dx[i]['cat'][fold].predict(X_test)
            seed_dx += (p_lgb + p_xgb + p_cat) / 3
            # dy
            p_lgb = all_models_dy[i]['lgb'][fold].predict(X_test)
            p_xgb = all_models_dy[i]['xgb'][fold].predict(xgb.DMatrix(X_test))
            p_cat = all_models_dy[i]['cat'][fold].predict(X_test)
            seed_dy += (p_lgb + p_xgb + p_cat) / 3
            
        final_test_dx += seed_dx / 5
        final_test_dy += seed_dy / 5
        
    final_test_dx /= len(seeds)
    final_test_dy /= len(seeds)
    
    test_end_x, test_end_y = clip_to_field(test_starts[:,0] + final_test_dx, test_starts[:,1] + final_test_dy)

    # Save
    base_path = Path(base_path_str) if base_path_str else Path('.')
    submission_dir = base_path / 'submissions'
    submission_dir.mkdir(exist_ok=True, parents=True)
    
    try:
        sample_sub_path = base_path / 'sample_submission.csv'
        if not sample_sub_path.exists():
             sample_sub_path = Path('/Users/chaeyoung/kleague-pass-prediction/2 step/sample_submission.csv')
        
        sample_sub = pd.read_csv(sample_sub_path)
    except:
        print("⚠️ Warning: sample_submission.csv를 찾을 수 없어 제출 파일을 생성하지 못했습니다.")
        return

    sub_df = pd.DataFrame({'game_episode': test_features['game_episode'], 'end_x': test_end_x, 'end_y': test_end_y})
    final_sub = sample_sub[['game_episode']].merge(sub_df, on='game_episode', how='left')
    
    if final_sub.isna().sum().sum() > 0:
        final_sub = final_sub.fillna({'end_x': test_end_x.mean(), 'end_y': test_end_y.mean()})

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_path = submission_dir / f'submission_v8_tuned_{ts}.csv'
    final_sub.to_csv(save_path, index=False)
    print(f"\n📂 Submission Saved to: {save_path}")

if __name__ == "__main__":
    main()