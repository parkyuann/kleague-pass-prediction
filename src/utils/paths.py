"""
경로 관리 유틸리티
================
프로젝트 내 모든 경로를 자동으로 관리합니다.
"""

from pathlib import Path
from typing import Optional


def find_project_root(marker_files: Optional[list] = None) -> Path:
    """
    프로젝트 루트 디렉토리를 찾습니다.
    
    마치 GPS가 현재 위치를 찾듯이, 특정 파일(마커)을 기준으로
    프로젝트의 루트를 찾아냅니다.
    
    Args:
        marker_files: 프로젝트 루트를 식별할 파일 목록
                     (기본값: ['configs', 'src', 'data'])
    
    Returns:
        프로젝트 루트 경로
    
    Raises:
        RuntimeError: 프로젝트 루트를 찾을 수 없는 경우
    
    예시:
        >>> root = find_project_root()
        >>> print(root)
        E:\Dacon\open_track1
    """
    if marker_files is None:
        marker_files = ['configs', 'src', 'data']
    
    current = Path.cwd().resolve()
    
    # 최대 10단계 위까지 탐색
    for _ in range(10):
        # 마커 파일들이 모두 존재하는지 확인
        if all((current / marker).exists() for marker in marker_files):
            return current
        
        # 상위 디렉토리로 이동
        if current.parent == current:
            # 루트 디렉토리에 도달 (더 이상 올라갈 수 없음)
            break
        current = current.parent
    
    raise RuntimeError(
        f"프로젝트 루트를 찾을 수 없습니다. "
        f"다음 디렉토리들이 있는지 확인하세요: {marker_files}"
    )


# 전역 프로젝트 루트
_project_root: Optional[Path] = None


def get_project_root() -> Path:
    """
    프로젝트 루트를 가져옵니다 (캐싱).
    
    처음 호출 시에만 탐색하고, 이후에는 캐싱된 값을 반환합니다.
    
    Returns:
        프로젝트 루트 경로
    """
    global _project_root
    
    if _project_root is None:
        _project_root = find_project_root()
    
    return _project_root


def get_data_dir(subdir: str = 'raw') -> Path:
    """
    데이터 디렉토리 경로를 가져옵니다.
    
    Args:
        subdir: 하위 디렉토리 ('raw', 'processed', 'interim', 'submissions')
    
    Returns:
        데이터 디렉토리 경로
    
    예시:
        >>> raw_path = get_data_dir('raw')
        >>> print(raw_path)
        E:\Dacon\open_track1\data\raw
    """
    root = get_project_root()
    data_path = root / 'data' / subdir
    
    # 디렉토리가 없으면 생성
    data_path.mkdir(parents=True, exist_ok=True)
    
    return data_path


def get_models_dir() -> Path:
    """모델 저장 디렉토리를 가져옵니다."""
    root = get_project_root()
    models_path = root / 'models'
    models_path.mkdir(parents=True, exist_ok=True)
    return models_path


def get_logs_dir() -> Path:
    """로그 디렉토리를 가져옵니다."""
    root = get_project_root()
    logs_path = root / 'logs'
    logs_path.mkdir(parents=True, exist_ok=True)
    return logs_path


def get_notebooks_dir() -> Path:
    """노트북 디렉토리를 가져옵니다."""
    root = get_project_root()
    return root / 'notebooks'


def get_configs_dir() -> Path:
    """설정 파일 디렉토리를 가져옵니다."""
    root = get_project_root()
    return root / 'configs'


# 데이터 파일 경로 헬퍼 함수들
def get_train_path() -> Path:
    """학습 데이터 경로"""
    return get_data_dir('raw') / 'train.csv'


def get_test_ref_path() -> Path:
    """테스트 참조 파일 경로"""
    return get_data_dir('raw') / 'test.csv'


def get_test_dir() -> Path:
    """테스트 에피소드 디렉토리"""
    return get_data_dir('raw') / 'test'


def get_match_info_path() -> Path:
    """경기 정보 파일 경로"""
    return get_data_dir('raw') / 'match_info.csv'


def get_sample_submission_path() -> Path:
    """샘플 제출 파일 경로"""
    return get_data_dir('raw') / 'sample_submission.csv'


def get_submission_path(filename: str = 'submission.csv') -> Path:
    """
    제출 파일 경로를 생성합니다.
    
    Args:
        filename: 제출 파일명
    
    Returns:
        제출 파일 전체 경로
    """
    return get_data_dir('submissions') / filename


def get_model_path(filename: str) -> Path:
    """
    모델 파일 경로를 생성합니다.
    
    Args:
        filename: 모델 파일명
    
    Returns:
        모델 파일 전체 경로
    """
    return get_models_dir() / filename


# 디버깅 및 테스트용
if __name__ == "__main__":
    print("=" * 60)
    print("경로 관리 유틸리티 테스트")
    print("=" * 60)
    
    try:
        # 프로젝트 루트 찾기
        root = get_project_root()
        print(f"\n✅ 프로젝트 루트: {root}")
        
        # 주요 디렉토리
        print(f"\n📁 주요 디렉토리:")
        print(f"  Data (raw): {get_data_dir('raw')}")
        print(f"  Data (processed): {get_data_dir('processed')}")
        print(f"  Models: {get_models_dir()}")
        print(f"  Logs: {get_logs_dir()}")
        print(f"  Notebooks: {get_notebooks_dir()}")
        
        # 데이터 파일
        print(f"\n📄 데이터 파일:")
        print(f"  Train: {get_train_path()}")
        print(f"  Test: {get_test_ref_path()}")
        print(f"  Match Info: {get_match_info_path()}")
        
        # 파일 존재 확인
        print(f"\n🔍 파일 존재 여부:")
        print(f"  train.csv: {'✅' if get_train_path().exists() else '❌'}")
        print(f"  test.csv: {'✅' if get_test_ref_path().exists() else '❌'}")
        print(f"  match_info.csv: {'✅' if get_match_info_path().exists() else '❌'}")
        
    except RuntimeError as e:
        print(f"\n❌ 오류: {e}")
        print("\n💡 해결 방법:")
        print("  1. 프로젝트 루트 디렉토리에서 실행하세요")
        print("  2. configs/, src/, data/ 폴더가 있는지 확인하세요")