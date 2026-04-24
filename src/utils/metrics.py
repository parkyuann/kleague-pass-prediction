"""
평가 지표 유틸리티
================
모델 성능을 측정하는 함수들을 제공합니다.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Union


def euclidean_distance(
    y_true: Union[np.ndarray, pd.DataFrame],
    y_pred: Union[np.ndarray, pd.DataFrame]
) -> float:
    """
    유클리드 거리 평균을 계산합니다.
    
    마치 축구장에서 두 지점 사이의 직선 거리를 재듯이,
    예측 좌표와 실제 좌표 사이의 거리를 계산합니다.
    
    공식:
        distance = sqrt((x_true - x_pred)² + (y_true - y_pred)²)
        score = mean(distances)
    
    Args:
        y_true: 실제 좌표 (N, 2) 형태 [end_x, end_y]
        y_pred: 예측 좌표 (N, 2) 형태 [end_x, end_y]
    
    Returns:
        평균 유클리드 거리
    
    예시:
        >>> y_true = np.array([[50, 34], [60, 40]])
        >>> y_pred = np.array([[52, 35], [58, 41]])
        >>> score = euclidean_distance(y_true, y_pred)
        >>> print(f"평균 거리: {score:.4f}m")
        평균 거리: 2.2361m
    """
    # DataFrame을 numpy array로 변환
    if isinstance(y_true, pd.DataFrame):
        y_true = y_true.values
    if isinstance(y_pred, pd.DataFrame):
        y_pred = y_pred.values
    
    # 배열로 변환
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # 2D 배열 확인
    if y_true.ndim == 1:
        y_true = y_true.reshape(-1, 2)
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape(-1, 2)
    
    # 유클리드 거리 계산
    distances = np.sqrt(
        (y_true[:, 0] - y_pred[:, 0]) ** 2 +
        (y_true[:, 1] - y_pred[:, 1]) ** 2
    )
    
    return float(np.mean(distances))


def rmse_per_coordinate(
    y_true: Union[np.ndarray, pd.DataFrame],
    y_pred: Union[np.ndarray, pd.DataFrame]
) -> Tuple[float, float]:
    """
    X, Y 좌표 각각의 RMSE를 계산합니다.
    
    Args:
        y_true: 실제 좌표 (N, 2)
        y_pred: 예측 좌표 (N, 2)
    
    Returns:
        (rmse_x, rmse_y) 튜플
    
    예시:
        >>> rmse_x, rmse_y = rmse_per_coordinate(y_true, y_pred)
        >>> print(f"X RMSE: {rmse_x:.4f}, Y RMSE: {rmse_y:.4f}")
    """
    # DataFrame to numpy
    if isinstance(y_true, pd.DataFrame):
        y_true = y_true.values
    if isinstance(y_pred, pd.DataFrame):
        y_pred = y_pred.values
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    if y_true.ndim == 1:
        y_true = y_true.reshape(-1, 2)
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape(-1, 2)
    
    # RMSE 계산
    rmse_x = float(np.sqrt(np.mean((y_true[:, 0] - y_pred[:, 0]) ** 2)))
    rmse_y = float(np.sqrt(np.mean((y_true[:, 1] - y_pred[:, 1]) ** 2)))
    
    return rmse_x, rmse_y


def combined_rmse(
    y_true: Union[np.ndarray, pd.DataFrame],
    y_pred: Union[np.ndarray, pd.DataFrame]
) -> float:
    """
    결합 RMSE를 계산합니다.
    
    공식:
        combined_rmse = sqrt((rmse_x² + rmse_y²) / 2)
    
    Args:
        y_true: 실제 좌표
        y_pred: 예측 좌표
    
    Returns:
        결합 RMSE
    """
    rmse_x, rmse_y = rmse_per_coordinate(y_true, y_pred)
    return float(np.sqrt((rmse_x ** 2 + rmse_y ** 2) / 2))


def mae_per_coordinate(
    y_true: Union[np.ndarray, pd.DataFrame],
    y_pred: Union[np.ndarray, pd.DataFrame]
) -> Tuple[float, float]:
    """
    X, Y 좌표 각각의 MAE(Mean Absolute Error)를 계산합니다.
    
    Args:
        y_true: 실제 좌표
        y_pred: 예측 좌표
    
    Returns:
        (mae_x, mae_y) 튜플
    """
    if isinstance(y_true, pd.DataFrame):
        y_true = y_true.values
    if isinstance(y_pred, pd.DataFrame):
        y_pred = y_pred.values
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    if y_true.ndim == 1:
        y_true = y_true.reshape(-1, 2)
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape(-1, 2)
    
    mae_x = float(np.mean(np.abs(y_true[:, 0] - y_pred[:, 0])))
    mae_y = float(np.mean(np.abs(y_true[:, 1] - y_pred[:, 1])))
    
    return mae_x, mae_y


def print_metrics(
    y_true: Union[np.ndarray, pd.DataFrame],
    y_pred: Union[np.ndarray, pd.DataFrame],
    prefix: str = ""
) -> dict:
    """
    모든 평가 지표를 계산하고 출력합니다.
    
    Args:
        y_true: 실제 좌표
        y_pred: 예측 좌표
        prefix: 출력 시 앞에 붙일 접두사 (예: "Train", "Valid")
    
    Returns:
        지표 딕셔너리
    
    예시:
        >>> metrics = print_metrics(y_true, y_pred, prefix="Validation")
        
        ============================================================
        Validation 성능 평가
        ============================================================
        📊 유클리드 거리 (대회 지표):  2.2361m
        📏 RMSE - X: 1.5000, Y: 1.6000, 결합: 1.5524
        📐 MAE  - X: 1.2000, Y: 1.3000
        ============================================================
    """
    # 지표 계산
    eucl_dist = euclidean_distance(y_true, y_pred)
    rmse_x, rmse_y = rmse_per_coordinate(y_true, y_pred)
    rmse_comb = combined_rmse(y_true, y_pred)
    mae_x, mae_y = mae_per_coordinate(y_true, y_pred)
    
    # 출력
    print("\n" + "=" * 60)
    print(f"{prefix} 성능 평가" if prefix else "성능 평가")
    print("=" * 60)
    print(f"📊 유클리드 거리 (대회 지표): {eucl_dist:7.4f}m")
    print(f"📏 RMSE - X: {rmse_x:.4f}, Y: {rmse_y:.4f}, 결합: {rmse_comb:.4f}")
    print(f"📐 MAE  - X: {mae_x:.4f}, Y: {mae_y:.4f}")
    print("=" * 60)
    
    # 딕셔너리 반환
    metrics = {
        'euclidean_distance': eucl_dist,
        'rmse_x': rmse_x,
        'rmse_y': rmse_y,
        'rmse_combined': rmse_comb,
        'mae_x': mae_x,
        'mae_y': mae_y
    }
    
    return metrics


def clip_predictions(
    predictions: Union[np.ndarray, pd.DataFrame],
    x_range: Tuple[float, float] = (0, 105),
    y_range: Tuple[float, float] = (0, 68)
) -> np.ndarray:
    """
    예측값을 유효한 범위로 클리핑합니다.
    
    마치 축구공이 필드 밖으로 나갈 수 없듯이,
    예측 좌표를 필드 범위 내로 제한합니다.
    
    Args:
        predictions: 예측 좌표 (N, 2)
        x_range: X 좌표 유효 범위 (min, max)
        y_range: Y 좌표 유효 범위 (min, max)
    
    Returns:
        클리핑된 예측값
    """
    if isinstance(predictions, pd.DataFrame):
        predictions = predictions.values
    
    predictions = np.array(predictions).copy()
    
    if predictions.ndim == 1:
        predictions = predictions.reshape(-1, 2)
    
    # 클리핑
    predictions[:, 0] = np.clip(predictions[:, 0], x_range[0], x_range[1])
    predictions[:, 1] = np.clip(predictions[:, 1], y_range[0], y_range[1])
    
    return predictions


# 테스트 코드
if __name__ == "__main__":
    print("=" * 60)
    print("평가 지표 유틸리티 테스트")
    print("=" * 60)
    
    # 테스트 데이터 생성
    np.random.seed(42)
    n_samples = 1000
    
    # 실제 좌표 (필드 중앙 부근)
    y_true = np.random.randn(n_samples, 2) * 10 + [52.5, 34]
    
    # 예측 좌표 (약간의 오차 추가)
    y_pred = y_true + np.random.randn(n_samples, 2) * 2
    
    # 지표 계산
    print("\n📊 테스트 결과:")
    metrics = print_metrics(y_true, y_pred, prefix="Test")
    
    # 클리핑 테스트
    print("\n🔧 클리핑 테스트:")
    y_pred_with_outliers = y_pred.copy()
    y_pred_with_outliers[0] = [-10, 150]  # 필드 밖 좌표
    
    print(f"  클리핑 전: {y_pred_with_outliers[0]}")
    y_pred_clipped = clip_predictions(y_pred_with_outliers)
    print(f"  클리핑 후: {y_pred_clipped[0]}")
    
    print("\n✅ 테스트 완료!")