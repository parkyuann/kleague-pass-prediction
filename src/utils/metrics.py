"""평가 지표 모듈"""
import numpy as np

def euclidean_distance(y_true, y_pred):
    """유클리드 거리 계산"""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    distances = np.sqrt(
        (y_true[:, 0] - y_pred[:, 0])**2 + 
        (y_true[:, 1] - y_pred[:, 1])**2
    )
    return np.mean(distances)

def print_metrics(y_true, y_pred):
    """평가 지표 출력"""
    score = euclidean_distance(y_true, y_pred)
    print("=" * 60)
    print(f"📊 유클리드 거리: {score:.4f}m")
    print("=" * 60)
    return score
