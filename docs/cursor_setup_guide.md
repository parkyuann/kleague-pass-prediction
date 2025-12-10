# Cursor에서 K리그 패스 예측 프로젝트 시작하기 🚀

## 🎯 Cursor 최적화 프로젝트 구조

Cursor의 AI 기능을 최대한 활용하기 위한 프로젝트 설정입니다.

---

## 📋 Step-by-Step 실행 가이드

### Step 1: Cursor에서 프로젝트 열기

1. Cursor 실행
2. `File` → `Open Folder`
3. `E:\Dacon\open_track1` 선택

### Step 2: 터미널 열기 (Cursor 내장)

```
단축키: Ctrl + `  (백틱)
또는: View → Terminal
```

### Step 3: 프로젝트 초기화

터미널에서:
```bash
# 프로젝트 구조 생성
python setup_project.py

# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Cursor 터미널에서)
.\venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### Step 4: Python 인터프리터 설정

1. `Ctrl + Shift + P`
2. "Python: Select Interpreter" 입력
3. `.\venv\Scripts\python.exe` 선택

---

## 🎨 Cursor 추천 확장 프로그램

### 필수 Extensions

Cursor 좌측 사이드바 Extensions (Ctrl + Shift + X):

1. **Python** (Microsoft)
   - Python 언어 지원
   - 설치: `ext install ms-python.python`

2. **Jupyter** (Microsoft)
   - `.ipynb` 파일 Cursor에서 직접 실행
   - 설치: `ext install ms-toolsai.jupyter`

3. **Pylance** (Microsoft)
   - Python 자동완성 강화
   - 설치: `ext install ms-python.vscode-pylance`

4. **Error Lens**
   - 에러를 코드 라인에 바로 표시
   - 설치: `ext install usernamehw.errorlens`

### 선택 Extensions

5. **Better Comments**
   - 주석 색상 강조
   - 설치: `ext install aaron-bond.better-comments`

6. **indent-rainbow**
   - 들여쓰기 가독성 향상
   - 설치: `ext install oderwat.indent-rainbow`

---

## ⚙️ Cursor 설정 파일 (.vscode/settings.json)

프로젝트 루트에 `.vscode/settings.json` 생성:

```json
{
  // Python 설정
  "python.defaultInterpreterPath": "${workspaceFolder}\\venv\\Scripts\\python.exe",
  "python.terminal.activateEnvironment": true,
  
  // 자동 저장
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  
  // 포맷팅
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  
  // Linting
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Args": ["--max-line-length=100"],
  
  // 자동완성
  "editor.suggestSelection": "first",
  "editor.acceptSuggestionOnCommitCharacter": true,
  "editor.quickSuggestions": {
    "other": true,
    "comments": false,
    "strings": false
  },
  
  // Jupyter
  "jupyter.askForKernelRestart": false,
  "jupyter.interactiveWindow.textEditor.executeSelection": true,
  
  // 파일 탐색기 제외
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".ipynb_checkpoints": true,
    "**/.pytest_cache": true
  },
  
  // 인코딩
  "files.encoding": "utf8",
  
  // Git
  "git.enabled": true,
  "git.autofetch": true
}
```

---

## 📁 Cursor 작업 공간 구조

```
E:\Dacon\open_track1\
│
├── .vscode/                       # ✨ Cursor 설정
│   ├── settings.json              # 프로젝트 설정
│   ├── launch.json                # 디버그 설정
│   └── tasks.json                 # 작업 자동화
│
├── data/
│   └── raw/
│       ├── train.csv
│       └── ...
│
├── notebooks/                     # ✨ Cursor에서 직접 실행!
│   ├── 01_EDA.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   └── ...
│
├── src/
│   ├── data/
│   │   └── load_data.py
│   ├── features/
│   │   └── engineering.py        # ✨ implementation.py 복사
│   └── utils/
│       └── metrics.py
│
├── venv/                          # 가상환경
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🎯 Cursor에서 Jupyter Notebook 사용하기

### Option 1: Cursor 내장 Jupyter (추천!)

1. Jupyter extension 설치 확인
2. `.ipynb` 파일 생성 또는 열기
3. 우측 상단 "Select Kernel" 클릭
4. `venv` 환경의 Python 선택
5. 셀 실행: `Shift + Enter`

**장점:**
- Cursor AI 기능 사용 가능
- 코드 자동완성 지원
- 변수 검사기 사용 가능

### Option 2: 브라우저 Jupyter

```bash
# Cursor 터미널에서
jupyter notebook
```

---

## 🤖 Cursor AI 기능 활용법

### 1. Cursor Chat (Ctrl + L)

```
💬 활용 예시:

"이 데이터프레임에서 결측치를 처리하는 함수를 만들어줘"

"패스 거리를 계산하는 함수를 작성해줘. 시작점(start_x, start_y)과 
종료점(end_x, end_y)을 받아서 유클리드 거리를 반환하도록"

"이 코드에 주석을 추가해줘"

"이 에러를 어떻게 해결하지? [에러 메시지 붙여넣기]"
```

### 2. Cursor Composer (Ctrl + I)

**인라인 코드 생성:**
```python
# Ctrl + I 누르고
# "골대까지 거리를 계산하는 함수" 입력
# → AI가 자동으로 함수 생성

def calculate_distance_to_goal(start_x, start_y):
    # AI가 생성한 코드
    pass
```

### 3. Tab Autocomplete

타이핑하면 자동으로 코드 제안:
```python
def create_spatial_features(df):
    # "df['distance" 까지만 입력하면
    # → AI가 나머지 자동 완성 제안
```

### 4. @ 컨텍스트 참조

```
💬 Cursor Chat에서:

"@feature_engineering_implementation.py 이 파일의 
create_spatial_features 함수를 설명해줘"

"@data/raw/train.csv 이 데이터의 구조를 분석해줘"
```

---

## 📝 Cursor에서 효율적인 작업 흐름

### 1️⃣ 탐색 단계 (notebooks/01_EDA.ipynb)

```python
# %%
# 💡 Tip: 셀마다 # %% 로 구분하면 Cursor가 인식!

# Ctrl + L로 Chat 열고:
# "train 데이터의 기본 통계를 확인하는 코드를 작성해줘"

import pandas as pd
from src.data.load_data import load_train_data

train, match_info = load_train_data()
```

### 2️⃣ Feature Engineering (notebooks/03_Feature_Engineering.ipynb)

```python
# %%
# Cursor Composer (Ctrl + I) 활용:
# "공간 특성 함수를 만들어줘:
#  - 골대까지 거리
#  - 골대 각도
#  - 경기장 구역"

# %%
# feature_engineering_implementation.py 참조
# Ctrl + L → "@feature_engineering_implementation.py의 
#            create_spatial_features 함수를 여기에 적용해줘"
```

### 3️⃣ 디버깅

```python
# 에러 발생 시:
# 1. 에러 줄에 커서 두기
# 2. Ctrl + L
# 3. "이 에러를 해결해줘" + 에러 메시지 붙여넣기
```

---

## 🔧 Cursor 전용 추가 설정 파일

### .vscode/launch.json (디버깅 설정)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "Python: Train Model",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/train.py",
      "console": "integratedTerminal",
      "args": ["--model", "lgbm"]
    }
  ]
}
```

### .vscode/tasks.json (자동화 작업)

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run EDA",
      "type": "shell",
      "command": "jupyter nbconvert --execute --to notebook notebooks/01_EDA.ipynb",
      "problemMatcher": []
    },
    {
      "label": "Run All Preprocessing",
      "type": "shell",
      "command": "python scripts/preprocess_all.py",
      "problemMatcher": []
    }
  ]
}
```

---

## 🎨 Cursor 단축키 모음 (Windows)

| 기능 | 단축키 |
|------|--------|
| 터미널 열기/닫기 | `Ctrl + `` |
| Cursor Chat | `Ctrl + L` |
| Composer (인라인) | `Ctrl + I` |
| 명령 팔레트 | `Ctrl + Shift + P` |
| 파일 검색 | `Ctrl + P` |
| 전체 검색 | `Ctrl + Shift + F` |
| 사이드바 토글 | `Ctrl + B` |
| Split Editor | `Ctrl + \` |
| Jupyter 셀 실행 | `Shift + Enter` |
| 선택 영역 실행 | `Shift + Enter` |
| 변수 이름 바꾸기 | `F2` |
| 정의로 이동 | `F12` |
| 뒤로 가기 | `Alt + ←` |

---

## 💡 Cursor AI 활용 실전 팁

### Tip 1: 코드 리뷰 받기

```
# 함수 작성 후
# 선택하고 Ctrl + L

"이 코드를 리뷰해줘. 개선점을 알려줘"
```

### Tip 2: 주석 자동 생성

```python
def complex_function(df, param1, param2):
    # 복잡한 로직...
    pass

# 함수 선택 → Ctrl + L
# "이 함수에 docstring을 추가해줘"
```

### Tip 3: 테스트 코드 생성

```
# 함수 선택 → Ctrl + L
"이 함수의 단위 테스트를 작성해줘"
```

### Tip 4: 에러 해결

```
# 에러 발생 시
# Ctrl + L → "이 에러의 원인과 해결 방법을 알려줘"
# + 스택 트레이스 붙여넣기
```

---

## 🔥 Cursor에서 효율적인 Feature Engineering

### 1. 기본 템플릿으로 시작

`src/features/engineering.py` 생성:

```python
"""
Feature Engineering 모듈
Cursor AI를 활용하여 빠르게 개발
"""

import pandas as pd
import numpy as np
from typing import List

# Ctrl + L → "공간 특성 함수를 만들어줘"
def create_spatial_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    공간 기반 특성 생성
    
    Cursor Composer로 생성됨
    """
    # AI가 채워줄 부분
    pass
```

### 2. 점진적 개발

```python
# Step 1: 기본 함수 골격 (AI 생성)
# Step 2: 주석으로 요구사항 작성
# Step 3: Ctrl + I로 구현
# Step 4: 테스트

# 예시:
# "# TODO: 골대까지 거리 계산" → Ctrl + I
# → AI가 자동으로 코드 생성
```

### 3. feature_engineering_implementation.py 활용

```python
# Cursor Chat에서:
# "@feature_engineering_implementation.py를 src/features/engineering.py로 
#  리팩토링해줘. 모듈화하고 타입 힌트 추가"
```

---

## 🚨 Cursor에서 자주 발생하는 문제 해결

### 문제 1: Python 인터프리터 인식 안 됨

**해결:**
```
1. Ctrl + Shift + P
2. "Python: Select Interpreter"
3. venv 환경 선택
4. Cursor 재시작
```

### 문제 2: 모듈 import 오류

**해결:**
```python
# 노트북 최상단에 추가
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path.cwd().parent if 'notebooks' in str(Path.cwd()) else Path.cwd()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
```

또는 `.vscode/settings.json`에:
```json
{
  "python.analysis.extraPaths": [
    "${workspaceFolder}"
  ]
}
```

### 문제 3: Jupyter Kernel 연결 안 됨

**해결:**
```bash
# 터미널에서
pip install ipykernel
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

### 문제 4: 한글 깨짐

**해결:**
```python
# 노트북 최상단
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
```

---

## 📊 Cursor에서 권장하는 작업 흐름

### Morning Routine

```
1. Cursor 실행
2. Ctrl + ` (터미널 열기)
3. .\venv\Scripts\activate
4. git pull (팀 작업 시)
5. jupyter 확장 확인
6. 오늘의 노트북 열기
```

### Coding Flow

```
1. 노트북 셀에 주석으로 목표 작성
   # "패스 거리를 계산하고 싶음"

2. Ctrl + I → AI가 코드 생성

3. Shift + Enter로 실행

4. 결과 확인

5. 문제 있으면 Ctrl + L로 Chat에서 디버깅

6. 완성되면 src/ 모듈로 이동
```

### Evening Routine

```
1. 코드 정리 (Ctrl + L → "이 코드를 정리해줘")
2. 주석 추가 (Ctrl + L → "주석 추가해줘")
3. Git commit
4. README 업데이트
```

---

## 🎯 Cursor 최적화 체크리스트

설정 완료:
- [ ] Python extension 설치
- [ ] Jupyter extension 설치
- [ ] .vscode/settings.json 생성
- [ ] Python 인터프리터 venv로 설정
- [ ] 터미널에서 가상환경 활성화 확인

작업 준비:
- [ ] Ctrl + L (Chat) 작동 확인
- [ ] Ctrl + I (Composer) 작동 확인
- [ ] .ipynb 파일 실행 확인
- [ ] src/ 모듈 import 확인

---

## 🚀 지금 바로 시작하기

```bash
# 1. Cursor에서 폴더 열기
File → Open Folder → E:\Dacon\open_track1

# 2. 터미널 (Ctrl + `)
python setup_project.py
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 3. Python 인터프리터 설정 (Ctrl + Shift + P)
Python: Select Interpreter → venv

# 4. 첫 노트북 생성
notebooks/01_EDA.ipynb

# 5. Cursor AI 활용 시작!
Ctrl + L → "데이터를 로드하고 기본 통계를 보여줘"
```

---

**Cursor + AI의 힘으로 빠르게 개발하세요!** 🚀⚡

다음: notebooks/01_EDA.ipynb에서 `Ctrl + L` 눌러보기!
