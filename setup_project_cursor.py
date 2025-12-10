"""
K리그 패스 예측 프로젝트 - Cursor 최적화 초기화 스크립트
========================================================

사용법:
    Cursor에서 E:\Dacon\open_track1\ 열기
    터미널(Ctrl + `)에서 실행: python setup_project_cursor.py

기능:
    1. 프로젝트 디렉토리 구조 생성
    2. 기존 데이터 파일 정리
    3. Cursor 최적화 설정 파일 생성 (.vscode/)
    4. 필수 모듈 파일 생성
    5. 예제 노트북 템플릿 생성
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def create_project_structure():
    """Cursor 최적화 프로젝트 구조 생성"""
    
    print("=" * 70)
    print("🚀 K리그 패스 예측 프로젝트 초기화 (Cursor 최적화)")
    print("=" * 70)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"작업 디렉토리: {Path.cwd()}")
    print()
    
    base_path = Path('.')
    
    # Step 1: 기본 디렉토리 생성
    print("📁 Step 1: 디렉토리 구조 생성")
    print("-" * 70)
    create_directories(base_path)
    
    # Step 2: 데이터 파일 정리
    print("\n📊 Step 2: 데이터 파일 정리")
    print("-" * 70)
    organize_data_files(base_path)
    
    # Step 3: Cursor/VSCode 설정
    print("\n⚙️  Step 3: Cursor 설정 파일 생성")
    print("-" * 70)
    create_vscode_settings(base_path)
    
    # Step 4: 기본 파일들
    print("\n📝 Step 4: 기본 설정 파일 생성")
    print("-" * 70)
    create_config_files(base_path)
    
    # Step 5: 모듈 파일
    print("\n💻 Step 5: 소스 코드 모듈 생성")
    print("-" * 70)
    create_source_modules(base_path)
    
    # Step 6: 예제 노트북
    print("\n📓 Step 6: 예제 노트북 생성")
    print("-" * 70)
    create_example_notebooks(base_path)
    
    # 완료 메시지
    print_completion_message()


def create_directories(base_path):
    """디렉토리 생성"""
    directories = [
        '.vscode',  # Cursor 설정
        'data/raw',
        'data/processed',
        'data/interim',
        'data/submissions',
        'notebooks',
        'src/data',
        'src/features',
        'src/models',
        'src/utils',
        'src/pipeline',
        'models',
        'configs',
        'logs',
        'docs',
        'scripts',
        'tests',
    ]
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}/")
        
        # src 하위에는 __init__.py 생성
        if directory.startswith('src/'):
            init_file = dir_path / '__init__.py'
            if not init_file.exists():
                init_file.write_text('"""모듈 초기화 파일"""\n', encoding='utf-8')


def organize_data_files(base_path):
    """데이터 파일 정리"""
    data_files = [
        'train.csv',
        'test.csv',
        'match_info.csv',
        'sample_submission.csv',
        'data_description.xlsx',
        'example_train.csv'
    ]
    
    raw_data_path = base_path / 'data' / 'raw'
    moved_count = 0
    
    for file in data_files:
        src = base_path / file
        if src.exists():
            dst = raw_data_path / file
            if not dst.exists():
                try:
                    shutil.copy2(src, dst)
                    print(f"  ✓ 복사: {file} → data/raw/")
                    moved_count += 1
                except Exception as e:
                    print(f"  ✗ 실패: {file} ({e})")
    
    # test 폴더
    test_folder = base_path / 'test'
    if test_folder.exists() and test_folder.is_dir():
        dst = raw_data_path / 'test'
        if not dst.exists():
            try:
                shutil.copytree(test_folder, dst)
                print(f"  ✓ 복사: test/ → data/raw/test/")
                moved_count += 1
            except Exception as e:
                print(f"  ✗ 실패: test/ ({e})")
    
    if moved_count == 0:
        print("  ℹ️  이동할 파일 없음 (이미 정리됨)")


def create_vscode_settings(base_path):
    """Cursor/VSCode 설정 파일 생성"""
    vscode_path = base_path / '.vscode'
    
    # settings.json
    settings = {
        "python.defaultInterpreterPath": "${workspaceFolder}\\venv\\Scripts\\python.exe",
        "python.terminal.activateEnvironment": True,
        "python.analysis.extraPaths": ["${workspaceFolder}", "${workspaceFolder}/src"],
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        "files.encoding": "utf8",
        "editor.formatOnSave": True,
        "python.formatting.provider": "black",
        "python.linting.enabled": True,
        "python.linting.flake8Enabled": True,
        "jupyter.askForKernelRestart": False,
        "files.exclude": {
            "**/__pycache__": True,
            "**/*.pyc": True,
            "**/.ipynb_checkpoints": True
        },
        "[python]": {
            "editor.defaultFormatter": "ms-python.black-formatter",
            "editor.formatOnSave": True
        }
    }
    
    settings_file = vscode_path / 'settings.json'
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    print(f"  ✓ .vscode/settings.json")
    
    # launch.json (디버깅)
    launch = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal",
                "cwd": "${workspaceFolder}"
            }
        ]
    }
    
    launch_file = vscode_path / 'launch.json'
    with open(launch_file, 'w', encoding='utf-8') as f:
        json.dump(launch, f, indent=2)
    print(f"  ✓ .vscode/launch.json")
    
    # extensions.json (권장 확장)
    extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "ms-toolsai.jupyter",
            "ms-python.black-formatter",
            "usernamehw.errorlens",
            "aaron-bond.better-comments"
        ]
    }
    
    ext_file = vscode_path / 'extensions.json'
    with open(ext_file, 'w', encoding='utf-8') as f:
        json.dump(extensions, f, indent=2)
    print(f"  ✓ .vscode/extensions.json")


def create_config_files(base_path):
    """기본 설정 파일 생성"""
    
    # .gitignore
    gitignore_content = """# 데이터
data/raw/*
data/processed/*
data/interim/*
*.csv
*.xlsx

# 모델
models/*.pkl
models/*.h5

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/

# 환경
venv/
.env

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# 로그
logs/*
"""
    (base_path / '.gitignore').write_text(gitignore_content, encoding='utf-8')
    print(f"  ✓ .gitignore")
    
    # requirements.txt
    requirements = """pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
lightgbm>=4.0.0
xgboost>=1.7.0
matplotlib>=3.7.0
seaborn>=0.12.0
jupyter>=1.0.0
ipykernel>=6.25.0
pyyaml>=6.0.0
openpyxl>=3.1.0
black>=23.0.0
flake8>=6.0.0
"""
    (base_path / 'requirements.txt').write_text(requirements, encoding='utf-8')
    print(f"  ✓ requirements.txt")
    
    # README.md
    readme = """# K리그 패스 좌표 예측 AI 모델 ⚽

## 🚀 Cursor에서 시작하기

### 1. 터미널 열기 (Ctrl + `)
```bash
python -m venv venv
.\\venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Python 인터프리터 설정
- `Ctrl + Shift + P`
- "Python: Select Interpreter"
- `venv` 선택

### 3. 노트북 시작
- `notebooks/01_EDA.ipynb` 열기
- `Shift + Enter`로 실행

## 🤖 Cursor AI 활용
- `Ctrl + L`: Cursor Chat
- `Ctrl + I`: Composer (인라인)

## 📂 프로젝트 구조
```
open_track1/
├── data/raw/          # 원본 데이터
├── notebooks/         # 실험 노트북
├── src/              # 소스 코드
└── models/           # 학습된 모델
```

## 📊 진행 상황
- [ ] EDA 완료
- [ ] Feature Engineering 완료
- [ ] 베이스라인 모델
- [ ] 최종 제출
"""
    (base_path / 'README.md').write_text(readme, encoding='utf-8')
    print(f"  ✓ README.md")


def create_source_modules(base_path):
    """소스 코드 모듈 생성"""
    
    # src/data/load_data.py
    load_data_code = '''"""데이터 로딩 모듈"""
import pandas as pd
from pathlib import Path

def load_train_data():
    """학습 데이터 로드"""
    data_path = Path('data/raw')
    
    train = pd.read_csv(data_path / 'train.csv')
    match_info = pd.read_csv(data_path / 'match_info.csv')
    
    print(f"✓ 학습 데이터: {len(train):,} 행")
    print(f"✓ 경기 정보: {len(match_info):,} 행")
    
    return train, match_info

def load_test_data():
    """테스트 데이터 로드"""
    data_path = Path('data/raw')
    test = pd.read_csv(data_path / 'test.csv')
    print(f"✓ 테스트 데이터: {len(test):,} 행")
    return test
'''
    (base_path / 'src/data/load_data.py').write_text(load_data_code, encoding='utf-8')
    print(f"  ✓ src/data/load_data.py")
    
    # src/utils/metrics.py
    metrics_code = '''"""평가 지표 모듈"""
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
'''
    (base_path / 'src/utils/metrics.py').write_text(metrics_code, encoding='utf-8')
    print(f"  ✓ src/utils/metrics.py")


def create_example_notebooks(base_path):
    """예제 노트북 생성"""
    notebooks_path = base_path / 'notebooks'
    
    # 01_EDA.ipynb
    eda_notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# K리그 패스 예측 - EDA\n", "\n", "**목표:** 데이터 구조 이해 및 기본 통계 확인"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# 모듈 경로 설정\n",
                    "import sys\n",
                    "from pathlib import Path\n",
                    "\n",
                    "project_root = Path.cwd().parent\n",
                    "if str(project_root) not in sys.path:\n",
                    "    sys.path.insert(0, str(project_root))\n",
                    "\n",
                    "print(f\"✓ 프로젝트 루트: {project_root}\")"
                ],
                "outputs": []
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# 라이브러리 임포트\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "\n",
                    "# 한글 폰트 설정\n",
                    "plt.rcParams['font.family'] = 'Malgun Gothic'\n",
                    "plt.rcParams['axes.unicode_minus'] = False\n",
                    "\n",
                    "print(\"✓ 라이브러리 로드 완료\")"
                ],
                "outputs": []
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# 데이터 로드\n",
                    "from src.data.load_data import load_train_data\n",
                    "\n",
                    "train, match_info = load_train_data()"
                ],
                "outputs": []
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Cursor AI에게 물어보기 (Ctrl + L):\n",
                    "# \"train 데이터의 기본 정보를 출력하는 코드를 작성해줘\"\n",
                    "\n",
                    "print(\"데이터 미리보기:\")\n",
                    "display(train.head())\n",
                    "\n",
                    "print(\"\\n기본 정보:\")\n",
                    "print(train.info())"
                ],
                "outputs": []
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## 💡 Cursor AI 활용 팁\n", "\n", "- `Ctrl + L`: 전체 Chat 열기\n", "- `Ctrl + I`: 인라인 코드 생성\n", "- `@train.csv`: 파일 참조"]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.9.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    import json
    eda_file = notebooks_path / '01_EDA.ipynb'
    with open(eda_file, 'w', encoding='utf-8') as f:
        json.dump(eda_notebook, f, indent=2, ensure_ascii=False)
    print(f"  ✓ notebooks/01_EDA.ipynb")


def print_completion_message():
    """완료 메시지"""
    print("\n" + "=" * 70)
    print("✅ Cursor 최적화 프로젝트 초기화 완료!")
    print("=" * 70)
    print()
    print("🎯 다음 단계:")
    print()
    print("1️⃣  Python 인터프리터 설정")
    print("   - Ctrl + Shift + P")
    print("   - 'Python: Select Interpreter' 입력")
    print("   - venv 환경 선택")
    print()
    print("2️⃣  터미널에서 패키지 설치")
    print("   - Ctrl + ` (터미널 열기)")
    print("   - .\\venv\\Scripts\\activate")
    print("   - pip install -r requirements.txt")
    print()
    print("3️⃣  예제 노트북 열기")
    print("   - notebooks/01_EDA.ipynb")
    print("   - Shift + Enter로 셀 실행")
    print()
    print("4️⃣  Cursor AI 활용 시작!")
    print("   - Ctrl + L: Cursor Chat")
    print("   - Ctrl + I: Composer")
    print()
    print("📚 참고 문서:")
    print("   - cursor_setup_guide.md: Cursor 활용법")
    print("   - feature_engineering_quick_reference.md: Feature 가이드")
    print()
    print("=" * 70)


if __name__ == "__main__":
    try:
        create_project_structure()
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("\n문제가 지속되면 수동으로 설정해주세요.")
        print("또는 cursor_setup_guide.md를 참조하세요.")
