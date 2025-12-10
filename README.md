# 🏆 K리그 패스 예측 프로젝트

> K리그 실제 경기 데이터를 기반으로 패스 도착 위치를 예측하는 AI 모델 개발

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Private-red.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In_Progress-yellow.svg)](https://github.com/parkyuann/kleague-pass-prediction)

---

## 📋 프로젝트 소개

현대 축구에서 승패는 개별 선수의 기량을 넘어, 보이지 않는 공간을 창출하고 유기적인 팀 패턴을 만드는 능력에서 갈립니다.

이 프로젝트는 K리그의 실제 경기 데이터를 활용하여, 특정 상황에서 최적의 패스 도착 위치를 AI가 예측하는 것을 목표로 합니다.

### 🎯 목표
- 패스 도착 위치 예측 (end_x, end_y)
- 유클리드 거리 기반 평가
- 데이터 기반 전술 분석 가능성 탐색

---

## 🚀 팀원 빠른 시작 가이드

### 1️⃣ 저장소 클론 (2분)

```bash
# 원하는 폴더로 이동
cd E:\Dacon

# 저장소 클론
git clone https://github.com/parkyuann/kleague-pass-prediction.git

# 프로젝트 폴더로 이동
cd kleague-pass-prediction
```

### 2️⃣ 환경 설정 (5분)

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
.\venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# Jupyter 커널 설치
python -m ipykernel install --user --name=venv
```

### 3️⃣ 데이터 준비 (3분)

**데이터 파일은 Git에 포함되지 않습니다!**

1. **Dacon 경진대회 페이지**에서 다운로드:
   - `train.csv`
   - `test.csv`
   - `match_info.csv`
   - `sample_submission.csv`

2. **파일 복사:**
   ```bash
   # Windows
   copy "다운로드경로\train.csv" data\raw\
   copy "다운로드경로\test.csv" data\raw\
   copy "다운로드경로\match_info.csv" data\raw\
   ```

### 4️⃣ Cursor IDE 설정 (5분)

1. **Cursor에서 폴더 열기**
   - File → Open Folder → `kleague-pass-prediction`

2. **Python 인터프리터 설정**
   - `Ctrl + Shift + P`
   - "Python: Select Interpreter" 입력
   - `.\venv\Scripts\python.exe` 선택

3. **노트북 테스트**
   - `notebooks/01_EDA.ipynb` 열기
   - 첫 셀 실행 (`Shift + Enter`)

✅ **설정 완료!**

---

## 📚 필독 가이드 (중요!)

모든 가이드는 **`docs/`** 폴더에 있습니다:

### 🔥 필수 (반드시 읽기!)

1. **[docs/TEAM_START_GUIDE.md](docs/TEAM_START_GUIDE.md)** ⭐⭐⭐
   - 팀원용 종합 가이드
   - 처음부터 끝까지 모든 내용

2. **[docs/github_quick_reference.md](docs/github_quick_reference.md)** ⭐⭐⭐
   - Git/GitHub 5분 퀵 가이드
   - 매일 참고할 명령어

3. **[docs/cursor_quick_start.md](docs/cursor_quick_start.md)** ⭐⭐⭐
   - Cursor IDE 5분 셋업
   - 트러블슈팅 포함

### 📖 추천 (시간 날 때)

4. **[docs/cursor_setup_guide.md](docs/cursor_setup_guide.md)**
   - Cursor AI 기능 100% 활용
   - 단축키, 확장 프로그램

5. **[docs/github_collaboration_guide.md](docs/github_collaboration_guide.md)**
   - Git 협업 완벽 가이드
   - 브랜치 전략, PR 워크플로우

6. **[docs/github_roles_guide.md](docs/github_roles_guide.md)**
   - 역할별 상세 가이드
   - PM, EDA, 피처, 모델링

### 📊 참고 자료

7. **[docs/feature_engineering_guide.md](docs/feature_engineering_guide.md)**
   - 피처 엔지니어링 이론
   - 공간/시간/팀 피처

8. **[docs/feature_engineering_quick_reference.md](docs/feature_engineering_quick_reference.md)**
   - 피처 개발 빠른 참조

---

## 🏗️ 프로젝트 구조

```
kleague-pass-prediction/
├── data/                      # 데이터 폴더 (Git 제외)
│   ├── raw/                   # 원본 데이터
│   │   ├── train.csv
│   │   ├── test.csv
│   │   └── match_info.csv
│   ├── processed/             # 전처리된 데이터
│   └── submissions/           # 제출 파일
│
├── notebooks/                 # Jupyter 노트북
│   ├── 01_EDA.ipynb          # 탐색적 데이터 분석
│   ├── 02_preprocessing.ipynb
│   └── 03_feature_engineering.ipynb
│
├── src/                       # 소스 코드
│   ├── data/                  # 데이터 로딩
│   ├── features/              # 피처 엔지니어링
│   ├── models/                # 모델 코드
│   ├── pipeline/              # 전체 파이프라인
│   └── utils/                 # 유틸리티
│
├── models/                    # 학습된 모델 저장 (Git 제외)
├── logs/                      # 로그 파일
├── configs/                   # 설정 파일
│
├── docs/                      # 📚 프로젝트 문서 (필독!)
│   ├── TEAM_START_GUIDE.md   # 👈 여기서 시작!
│   ├── cursor_quick_start.md
│   ├── github_quick_reference.md
│   └── ...
│
├── setup_project_cursor.py    # 프로젝트 구조 자동 생성
├── requirements.txt           # Python 패키지
├── .gitignore                 # Git 제외 파일
└── README.md                  # 이 파일
```

---

## 👥 팀 구성 및 역할

| 역할 | 담당자 | 브랜치 | 주요 작업 |
|------|--------|--------|-----------|
| **팀장/PM** | ? | `develop` 관리 | Git 관리, 전체 조율, 통합 |
| **EDA/전처리** | ? | `feature/eda` | 데이터 분석, 전처리 파이프라인 |
| **피처 엔지니어링** | ? | `feature/features` | 공간/시간/팀 피처 개발 |
| **모델링 1** | ? | `feature/model-lgbm` | LightGBM, XGBoost |
| **모델링 2** | ? | `feature/model-lstm` | LSTM, 앙상블 |

> 💡 **역할 분담은 팀 미팅에서 결정하세요!**

---

## 🔄 Git 협업 워크플로우

### 📅 매일 루틴

**아침 (작업 시작 전)**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-work  # 또는 기존 브랜치
```

**작업 중**
```bash
git add .
git commit -m "feat: 작업 내용"
git push origin feature/my-work
```

**저녁 (작업 완료)**
- GitHub에서 Pull Request 생성
- 팀원에게 리뷰 요청

### 🌿 브랜치 전략

```
main (최종 제출)
│
develop (개발 통합) ← 여기서 작업!
│
├── feature/eda
├── feature/preprocessing
├── feature/features
├── feature/model-lgbm
└── feature/model-lstm
```

### 📝 커밋 메시지 규칙

```bash
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
refactor: 코드 리팩토링
test: 테스트 추가
chore: 기타 변경
```

**예시:**
```bash
git commit -m "feat: 공간 기반 피처 추가"
git commit -m "fix: result_name 결측치 처리 버그 수정"
git commit -m "docs: README 업데이트"
```

---

## 🛠️ 기술 스택

### 언어 & 프레임워크
- **Python 3.8+**
- **Jupyter Notebook**
- **Pandas**, **NumPy**

### 머신러닝
- **LightGBM** - Gradient Boosting
- **XGBoost** - Gradient Boosting
- **PyTorch** - 딥러닝 (LSTM, Transformer)
- **Scikit-learn** - 전처리, 평가

### 시각화
- **Matplotlib**
- **Seaborn**
- **Plotly**

### 협업 도구
- **Git/GitHub** - 버전 관리
- **Cursor IDE** - AI 코드 에디터
- **Slack/Discord** - 팀 커뮤니케이션

---

## 📊 평가 지표

**유클리드 거리 (Euclidean Distance)**

```python
import numpy as np

def euclidean_distance(y_true_x, y_true_y, y_pred_x, y_pred_y):
    """
    Args:
        y_true_x, y_true_y: 실제 좌표
        y_pred_x, y_pred_y: 예측 좌표
    
    Returns:
        평균 유클리드 거리
    """
    distances = np.sqrt(
        (y_true_x - y_pred_x)**2 + 
        (y_true_y - y_pred_y)**2
    )
    return np.mean(distances)
```

---

## ⚠️ 중요 규칙

### ✅ DO (꼭 지키기!)

1. **매일 아침 `git pull origin develop`**
2. **작은 단위로 자주 커밋**
3. **의미 있는 커밋 메시지**
4. **PR에는 설명 필수**
5. **24시간 내 코드 리뷰**

### ❌ DON'T (절대 금지!)

1. **데이터 파일 Git에 올리지 말 것!** (`.gitignore` 확인)
2. **`main` 브랜치에 직접 푸시 금지**
3. **테스트 안 된 코드 푸시 금지**
4. **의미 없는 커밋 금지** (예: "수정", "ㅁㄴㅇㄹ")

---

## 🐛 트러블슈팅

### 문제 1: 모듈 import 오류
```bash
pip install -r requirements.txt
python -m ipykernel install --user --name=venv
```

### 문제 2: 데이터 파일 못 찾음
```python
# notebooks/01_EDA.ipynb
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent))

from src.data.load_data import load_train_data
train, match_info = load_train_data()
```

### 문제 3: Git 충돌
```bash
git checkout develop
git pull origin develop
git checkout feature/my-work
git merge develop
# 충돌 파일 수정
git add .
git commit -m "merge: 충돌 해결"
git push
```

### 문제 4: Push 거부됨
```bash
git pull origin feature/my-work
# 충돌 해결
git push origin feature/my-work
```

---

## 📞 문의 및 지원

### 질문하기
1. **팀 채널** (Slack/Discord)
2. **GitHub Issues** - 버그 리포트
3. **GitHub Discussions** - 일반 질문

### 도움 요청
- 막히면 바로 물어보기!
- 혼자 고민하지 말기
- 서로 도우면서 성장 💪

---

## 📅 프로젝트 일정

### Week 1: 환경 설정 & EDA
- [x] 프로젝트 초기 설정
- [ ] 팀 역할 분담
- [ ] 데이터 탐색 (EDA)
- [ ] 전처리 전략 수립

### Week 2: 피처 엔지니어링
- [ ] 공간 기반 피처
- [ ] 시간 기반 피처
- [ ] 팀/선수 컨텍스트 피처

### Week 3: 모델링
- [ ] LightGBM 베이스라인
- [ ] LSTM 모델
- [ ] 하이퍼파라미터 튜닝

### Week 4: 앙상블 & 최적화
- [ ] 모델 앙상블
- [ ] 최종 제출 준비
- [ ] 코드 정리 및 문서화

---

## 🎯 성공을 위한 팁

### 1. 소통이 80%
```
✅ 막히면 바로 물어보기
✅ 진행 상황 공유
✅ 아이디어 적극 제안
```

### 2. 작은 단위로 자주
```
✅ 큰 작업은 작게 나누기
✅ 하루 2-3회 커밋
✅ 금요일 큰 변경 지양
```

### 3. 리뷰는 빠르게
```
✅ 24시간 내 리뷰
✅ 건설적인 피드백
✅ 칭찬도 함께!
```

### 4. 테스트는 필수
```
✅ 커밋 전 코드 실행
✅ 노트북 전체 실행 확인
✅ 결측치/오류 체크
```

---

## 📄 라이선스

Private - 팀원만 접근 가능

---

## 🙏 Acknowledgments

- **Dacon** - 경진대회 주최
- **K리그** - 데이터 제공
- **팀원 모두** - 최고! 💪

---

## 📚 추가 리소스

### 공식 문서
- [Dacon 경진대회 페이지](https://dacon.io/)
- [Git 공식 문서 (한국어)](https://git-scm.com/book/ko/v2)
- [GitHub 가이드](https://guides.github.com/)

### 내부 문서
- [Feature Engineering Guide](docs/feature_engineering_guide.md)
- [Cursor Setup Guide](docs/cursor_setup_guide.md)
- [GitHub Collaboration Guide](docs/github_collaboration_guide.md)

---

## ✨ 시작하기

```bash
# 1. 저장소 클론
git clone https://github.com/parkyuann/kleague-pass-prediction.git
cd kleague-pass-prediction

# 2. 가이드 읽기
cat docs/TEAM_START_GUIDE.md

# 3. 환경 설정
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 4. 작업 시작!
```

**Let's win this! 🏆**

---

**마지막 업데이트:** 2025-12-10  
**버전:** 1.0  
**작성자:** Team K-League Pass Prediction
