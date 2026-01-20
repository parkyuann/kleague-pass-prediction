import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def get_zone(x):
    if x <= 40: return 'Defense'
    elif x <= 75: return 'Midfield'
    else: return 'Attack'

def train_zonal_calibrators(df):
    df['zone'] = df['start_x'].apply(get_zone)
    zones = ['Defense', 'Midfield', 'Attack']
    calibrators = {}

    for zone in zones:
        zone_data = df[(df['zone'] == zone) & (df['pred_dist'] > 22)]
        if len(zone_data) > 30:
            X = zone_data[['pred_dist']].values
            y = zone_data['target_dist'].values
            model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
            model.fit(X, y)
            calibrators[zone] = model
            print(f"✅ {zone} 보정 모델 학습 완료")
    
    return calibrators

def apply_calibration(row, calibrators):
    if row['pred_dist'] <= 22:
        return row['pred_dist']
    
    zone = get_zone(row['start_x'])
    if zone in calibrators:
        model = calibrators[zone]
        calibrated_val = model.predict([[row['pred_dist']]])[0]
        max_limit = row['pred_dist'] * 1.8 
        return min(max(row['pred_dist'], calibrated_val), max_limit)
    else:
        return row['pred_dist']