"""데이터 로딩 모듈"""
import pandas as pd
from pathlib import Path

def get_project_root():
    """프로젝트 루트 찾기"""
    current = Path(__file__).resolve()
    return current.parent.parent.parent

def load_train_data():
    """학습 데이터 로드"""
    project_root = get_project_root()
    data_path = project_root / 'data' / 'raw'
    
    train = pd.read_csv(data_path / 'train.csv')
    match_info = pd.read_csv(data_path / 'match_info.csv')
    
    print(f"✓ 학습 데이터: {len(train):,} 행")
    print(f"✓ 경기 정보: {len(match_info):,} 행")
    
    return train, match_info

def load_test_data():
    """테스트 데이터 로드"""
    project_root = get_project_root()
    data_path = project_root / 'data' / 'raw'
    
    test = pd.read_csv(data_path / 'test.csv')
    print(f"✓ 테스트 데이터: {len(test):,} 행")
    return test