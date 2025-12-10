# 🚀 K리그 패스 예측 프로젝트 - GitHub 팀 협업 완벽 가이드

## 📋 목차
1. [GitHub 초기 설정 (리더용)](#1-github-초기-설정-리더용)
2. [팀원 합류 가이드](#2-팀원-합류-가이드)
3. [브랜치 전략](#3-브랜치-전략)
4. [협업 워크플로우](#4-협업-워크플로우)
5. [충돌 해결](#5-충돌-해결)
6. [프로젝트 관리](#6-프로젝트-관리)
7. [커밋 컨벤션](#7-커밋-컨벤션)
8. [트러블슈팅](#8-트러블슈팅)

---

## 1. GitHub 초기 설정 (리더용)

### Step 1-1: GitHub 저장소 생성

1. **GitHub 웹사이트 접속**
   - https://github.com 로그인
   
2. **새 저장소 생성**
   - 우측 상단 `+` → `New repository`
   - **Repository name**: `kleague-pass-prediction`
   - **Description**: `K리그 패스 도착 위치 예측 AI 경진대회`
   - **Private** 선택 (팀원만 접근)
   - **Add a README file** 체크 해제 (로컬에 이미 있음)
   - **Add .gitignore** 선택 → **Python** 선택
   - `Create repository` 클릭

### Step 1-2: 로컬 프로젝트를 GitHub에 연결

Cursor 터미널 (Ctrl + `)에서:

```bash
# 1. 프로젝트 폴더로 이동
cd E:\Dacon\open_track1

# 2. Git 초기화 (처음 한 번만)
git init

# 3. 원격 저장소 연결 (GitHub에서 복사한 URL 사용)
git remote add origin https://github.com/your-username/kleague-pass-prediction.git

# 4. .gitignore 생성 (이미 있다면 스킵)
# (아래 내용은 별도 섹션에서 복사)

# 5. 첫 커밋
git add .
git commit -m "Initial commit: 프로젝트 초기 설정"

# 6. GitHub에 푸시
git branch -M main
git push -u origin main
```

### Step 1-3: .gitignore 설정 (중요!)

프로젝트 루트에 `.gitignore` 파일 생성:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb_checkpoints

# 데이터 파일 (용량 큰 파일은 GitHub에 올리지 않음!)
data/raw/*.csv
data/raw/*.xlsx
data/processed/*.csv
data/interim/*.csv
*.csv
*.xlsx
*.h5
*.pkl
*.pickle

# 모델 파일 (용량 큰 파일)
models/*.h5
models/*.pkl
models/*.pt
models/*.pth
*.h5
*.pkl

# 제출 파일 (팀원마다 다를 수 있음)
data/submissions/submission_*.csv

# IDE 설정
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# 로그
logs/*.log
*.log

# 임시 파일
tmp/
temp/
*.tmp

# 환경 변수
.env
.env.local

# 테스트
.pytest_cache/
.coverage
htmlcov/
```

**중요!** 데이터 파일은 GitHub에 올리지 않습니다:
- 용량이 크면 GitHub 제한 초과
- 데이터는 Dacon에서 공식 다운로드

### Step 1-4: 팀원 초대

1. GitHub 저장소 페이지에서
2. `Settings` → `Collaborators` → `Add people`
3. 팀원의 GitHub username 또는 이메일 입력
4. 팀원이 이메일로 받은 초대 수락

---

## 2. 팀원 합류 가이드

### Step 2-1: 저장소 클론

```bash
# 1. 원하는 폴더로 이동
cd E:\Dacon

# 2. 저장소 클론
git clone https://github.com/your-username/kleague-pass-prediction.git

# 3. 프로젝트 폴더로 이동
cd kleague-pass-prediction

# 4. Cursor에서 폴더 열기
# File → Open Folder → E:\Dacon\kleague-pass-prediction
```

### Step 2-2: 환경 설정

```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
.\venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. Jupyter 커널 설치
python -m ipykernel install --user --name=venv
```

### Step 2-3: 데이터 파일 준비

**중요!** 데이터는 Git에 포함되지 않으므로 수동으로 추가:

```bash
# 1. Dacon에서 데이터 다운로드
# 2. data/raw/ 폴더에 복사
copy "C:\Downloads\train.csv" data\raw\
copy "C:\Downloads\test.csv" data\raw\
copy "C:\Downloads\match_info.csv" data\raw\
```

또는 팀 공유 드라이브 (Google Drive, OneDrive)에서 다운로드

---

## 3. 브랜치 전략

### 브랜치 구조 (Git Flow 간소화 버전)

```
main (배포용, 항상 안정)
│
├── develop (개발 통합 브랜치)
│   │
│   ├── feature/eda (탐색적 데이터 분석)
│   ├── feature/preprocessing (전처리)
│   ├── feature/feature-engineering (피처 엔지니어링)
│   ├── feature/model-lgbm (LightGBM 모델)
│   ├── feature/model-lstm (LSTM 모델)
│   └── feature/ensemble (앙상블)
```

### 브랜치 명명 규칙

```
feature/작업내용    # 새로운 기능 개발
fix/버그내용        # 버그 수정
docs/문서내용       # 문서 작성
refactor/내용       # 코드 리팩토링
```

**예시:**
- `feature/spatial-features`
- `feature/temporal-features`
- `fix/result-name-imputation`
- `docs/feature-engineering-guide`

### 브랜치 사용법

```bash
# 1. 최신 코드 받기
git checkout develop
git pull origin develop

# 2. 새 브랜치 생성
git checkout -b feature/spatial-features

# 3. 작업 진행...

# 4. 변경사항 커밋
git add .
git commit -m "feat: 공간 기반 피처 추가"

# 5. GitHub에 푸시
git push origin feature/spatial-features

# 6. Pull Request 생성 (GitHub 웹에서)
```

---

## 4. 협업 워크플로우

### 4-1. 매일 아침 루틴 (Daily Sync)

```bash
# 1. 최신 코드 받기
git checkout develop
git pull origin develop

# 2. 내 브랜치로 최신 코드 병합
git checkout feature/my-feature
git merge develop

# 3. 충돌 있으면 해결 (아래 섹션 참고)

# 4. 작업 시작!
```

### 4-2. 작업 중 저장 (Commit)

```bash
# 1. 변경 파일 확인
git status

# 2. 변경 파일 스테이징
git add src/features/spatial_features.py
git add notebooks/03_feature_engineering.ipynb

# 또는 모두 추가
git add .

# 3. 커밋
git commit -m "feat: 패스 거리 및 각도 피처 추가"

# 4. 주기적으로 푸시 (하루 1-2회)
git push origin feature/my-feature
```

### 4-3. Pull Request (PR) 생성

작업 완료 후 팀원들에게 코드 리뷰 요청:

**GitHub 웹에서:**

1. 저장소 페이지 → `Pull requests` → `New pull request`
2. **base**: `develop` ← **compare**: `feature/my-feature`
3. 제목: `[Feature] 공간 기반 피처 추가`
4. 설명 작성:
   ```markdown
   ## 변경 사항
   - 패스 거리 계산 함수 추가
   - 패스 각도 계산 함수 추가
   - 골대와의 거리 피처 추가
   
   ## 테스트
   - [x] notebooks/03_feature_engineering.ipynb 실행 확인
   - [x] 결측치 없음 확인
   
   ## 리뷰 포인트
   - 각도 계산 로직 검토 부탁드립니다
   ```
5. **Reviewers**: 팀원 지정
6. `Create pull request`

### 4-4. 코드 리뷰

**리뷰어 (팀원):**

1. PR 페이지에서 `Files changed` 탭
2. 코드 읽고 댓글 남기기
   - 👍 좋은 코드: "깔끔한 구현이네요!"
   - 🤔 질문: "이 부분 왜 이렇게 했나요?"
   - 💡 제안: "이렇게 하면 더 빠를 것 같아요"
   - 🐛 버그: "여기 NaN 체크 필요할 것 같아요"
3. 리뷰 완료: `Review changes` → `Approve`

**작성자:**

1. 댓글 읽고 코드 수정
2. 수정 후 커밋 & 푸시 (자동으로 PR 업데이트됨)
3. 모든 리뷰 승인되면 `Merge pull request`

### 4-5. 브랜치 병합

```bash
# PR이 승인되면 GitHub에서 Merge

# 로컬에서 최신 코드 받기
git checkout develop
git pull origin develop

# 작업 브랜치 삭제 (옵션)
git branch -d feature/my-feature
```

---

## 5. 충돌 해결

### 충돌이 발생하는 경우

- 두 명이 같은 파일의 같은 줄을 수정했을 때
- 예: `src/features/engineering.py` 동시 수정

### 충돌 해결 방법

#### 방법 1: Cursor에서 해결 (추천!)

```bash
# 1. develop 브랜치의 최신 코드 병합
git checkout feature/my-feature
git merge develop

# 충돌 메시지 표시
# CONFLICT (content): Merge conflict in src/features/engineering.py
```

Cursor에서 충돌 파일 열면:

```python
<<<<<<< HEAD (현재 브랜치)
def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
=======
def calculate_pass_distance(start_x, start_y, end_x, end_y):
    return math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
>>>>>>> develop (병합하려는 브랜치)
```

**해결:**
1. 어느 코드를 사용할지 결정
2. `<<<<<<<`, `=======`, `>>>>>>>` 마커 제거
3. 최종 코드만 남김:

```python
def calculate_distance(x1, y1, x2, y2):
    """두 점 사이의 유클리드 거리 계산"""
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```

4. 저장 후:
```bash
git add src/features/engineering.py
git commit -m "merge: develop 브랜치 병합 및 충돌 해결"
git push origin feature/my-feature
```

#### 방법 2: 충돌 회피 전략

**예방이 최선!**

1. **작은 단위로 자주 커밋**
2. **매일 아침 develop 브랜치 동기화**
3. **서로 다른 파일 작업** (역할 분담)
4. **작업 전 팀원과 소통**

---

## 6. 프로젝트 관리

### 6-1. GitHub Issues (작업 관리)

**이슈 생성:**

1. GitHub 저장소 → `Issues` → `New issue`
2. 템플릿:

```markdown
## 📋 작업 내용
공간 기반 피처 엔지니어링

## 🎯 목표
- [ ] 패스 거리 계산
- [ ] 패스 각도 계산
- [ ] 골대와의 거리 계산

## 📅 마감일
2025-12-15

## 👥 담당자
@username

## 🔗 관련 이슈
#12, #13
```

3. **Labels** 추가:
   - `enhancement` (새 기능)
   - `bug` (버그)
   - `documentation` (문서)
   - `priority: high` (긴급)

### 6-2. GitHub Projects (칸반 보드)

**프로젝트 보드 생성:**

1. 저장소 → `Projects` → `New project`
2. **Board** 선택
3. 컬럼 구성:
   ```
   📝 To Do (해야 할 일)
   🏃 In Progress (진행 중)
   👀 Review (리뷰 대기)
   ✅ Done (완료)
   ```

**카드 추가:**
- 이슈를 드래그하여 보드에 추가
- 작업 상태 변경 시 컬럼 이동

### 6-3. 역할 분담 예시

**팀 구성 (5인 기준):**

| 역할 | 담당자 | 주요 작업 |
|------|--------|-----------|
| **팀장/PM** | A | 전체 일정 관리, Git 관리, 통합 |
| **EDA/전처리** | B | 데이터 분석, 결측치 처리 |
| **Feature Engineering** | C | 공간 피처, 시간 피처 |
| **모델링 1** | D | LightGBM, XGBoost |
| **모델링 2** | E | LSTM, Ensemble |

**브랜치 할당:**
```
A: develop 관리, feature/integration
B: feature/eda, feature/preprocessing
C: feature/spatial-features, feature/temporal-features
D: feature/model-lgbm, feature/model-xgboost
E: feature/model-lstm, feature/ensemble
```

### 6-4. 주간 미팅

**매주 월요일 10:00 (예시):**

**아젠다:**
1. 지난 주 작업 리뷰
2. 이번 주 작업 계획
3. 블로커 (막힌 부분) 공유
4. 역할 재조정

**미팅 노트 (GitHub Discussion 활용):**
```markdown
## 주간 미팅 - 2025.12.09

### 참석자
@A, @B, @C, @D, @E

### 지난 주 완료
- [x] EDA 완료 (#12)
- [x] 전처리 파이프라인 구축 (#15)

### 이번 주 목표
- [ ] 공간 피처 추가 (@C)
- [ ] LightGBM 베이스라인 (@D)
- [ ] LSTM 실험 시작 (@E)

### 블로커
- 서버 GPU 메모리 부족 → 해결책: 배치 크기 감소

### 다음 미팅
2025.12.16 10:00
```

---

## 7. 커밋 컨벤션

### 커밋 메시지 규칙 (Conventional Commits)

**형식:**
```
<타입>: <제목>

<본문> (옵션)

<푸터> (옵션)
```

**타입:**
```
feat:     새로운 기능 추가
fix:      버그 수정
docs:     문서 수정
style:    코드 포맷팅 (기능 변경 없음)
refactor: 코드 리팩토링
test:     테스트 코드 추가
chore:    빌드/패키지 관련 수정
```

**예시:**

```bash
# 좋은 커밋 메시지 ✅
git commit -m "feat: 패스 거리 계산 함수 추가"
git commit -m "fix: result_name 결측치 처리 오류 수정"
git commit -m "docs: feature engineering 가이드 작성"

# 나쁜 커밋 메시지 ❌
git commit -m "수정"
git commit -m "버그 수정"
git commit -m "ㅁㄴㅇㄹ"
```

**본문 예시:**

```bash
git commit -m "feat: 공간 기반 피처 추가

- calculate_distance: 유클리드 거리 계산
- calculate_angle: 패스 각도 계산
- distance_to_goal: 골대까지 거리

Closes #23"
```

### 커밋 크기

**작은 단위로 자주 커밋!**

```bash
# 좋은 예 ✅
git commit -m "feat: 패스 거리 함수 추가"
git commit -m "feat: 패스 각도 함수 추가"
git commit -m "test: 피처 계산 테스트 추가"

# 나쁜 예 ❌
git commit -m "feat: 모든 피처 추가 및 모델 학습 및 테스트"
```

---

## 8. 트러블슈팅

### 문제 1: Push 거부됨

**에러:**
```
! [rejected] main -> main (fetch first)
```

**해결:**
```bash
# 1. 원격 변경사항 받기
git pull origin main

# 2. 충돌 해결 (있다면)

# 3. 다시 푸시
git push origin main
```

### 문제 2: 실수로 잘못된 커밋

**최근 커밋 취소 (아직 푸시 안 함):**
```bash
# 커밋 취소, 변경사항은 유지
git reset --soft HEAD~1

# 커밋 취소, 변경사항도 삭제 (주의!)
git reset --hard HEAD~1
```

**이미 푸시한 경우:**
```bash
# 되돌리기 커밋 생성
git revert HEAD
git push origin main
```

### 문제 3: 브랜치 잘못 만듦

```bash
# 브랜치 이름 변경
git branch -m old-name new-name

# 원격 브랜치 삭제
git push origin --delete old-name

# 새 브랜치 푸시
git push origin new-name
```

### 문제 4: 대용량 파일 업로드 실패

**에러:**
```
remote: error: File train.csv is 100MB; exceeds GitHub's file size limit
```

**해결:**
```bash
# 1. .gitignore에 추가
echo "data/raw/*.csv" >> .gitignore

# 2. Git 캐시에서 제거
git rm --cached data/raw/train.csv

# 3. 커밋
git commit -m "chore: 대용량 데이터 파일 제외"

# 4. 푸시
git push origin main
```

### 문제 5: 팀원이 내 브랜치를 볼 수 없음

```bash
# 브랜치를 원격에 푸시했는지 확인
git push origin feature/my-feature

# 팀원은 원격 브랜치 목록 갱신
git fetch origin

# 브랜치 목록 확인
git branch -a
```

---

## 9. Cursor에서 Git 사용하기

### GUI로 쉽게 사용

Cursor의 좌측 사이드바 → **Source Control** (Ctrl + Shift + G)

**변경사항 확인:**
- 수정된 파일 목록 표시
- `M` (Modified), `U` (Untracked), `D` (Deleted)

**스테이징:**
- 파일 옆 `+` 버튼 클릭
- 또는 "Stage All Changes"

**커밋:**
- 상단 입력창에 커밋 메시지 입력
- `Ctrl + Enter` 또는 체크 버튼

**푸시/풀:**
- 하단 상태바에서 `↑↓` 버튼 클릭
- 또는 `...` 메뉴 → `Push` / `Pull`

**브랜치 전환:**
- 하단 상태바에서 브랜치 이름 클릭
- 드롭다운에서 브랜치 선택

---

## 10. 실전 협업 시나리오

### 시나리오 1: 첫 작업 시작

**팀원 C (Feature Engineering 담당):**

```bash
# 1. 최신 코드 받기
git checkout develop
git pull origin develop

# 2. 새 브랜치 생성
git checkout -b feature/spatial-features

# 3. 작업 진행
# notebooks/03_feature_engineering.ipynb 작성
# src/features/spatial.py 작성

# 4. 커밋
git add .
git commit -m "feat: 공간 기반 피처 추가"

# 5. 푸시
git push origin feature/spatial-features

# 6. GitHub에서 PR 생성
```

### 시나리오 2: 코드 리뷰 받기

**PR 생성 후:**

1. **팀장 A가 리뷰:**
   ```
   💬 "distance_to_goal 함수에서 골대 좌표가 하드코딩되어 있네요.
       설정 파일로 빼는 게 어떨까요?"
   ```

2. **팀원 C가 수정:**
   ```bash
   # 코드 수정
   git add src/features/spatial.py
   git commit -m "refactor: 골대 좌표를 config로 이동"
   git push origin feature/spatial-features
   ```

3. **팀장 A가 승인:**
   ```
   ✅ "좋습니다! Approve"
   ```

4. **Merge:**
   - GitHub에서 `Merge pull request`
   - `feature/spatial-features` → `develop`

### 시나리오 3: 충돌 해결

**팀원 D와 E가 같은 파일 수정:**

**팀원 D:**
```python
# src/models/train.py
def train_model(X, y):
    model = LGBMRegressor(n_estimators=100)
    model.fit(X, y)
    return model
```

**팀원 E:**
```python
# src/models/train.py
def train_model(X_train, y_train, params):
    model = LGBMRegressor(**params)
    model.fit(X_train, y_train)
    return model
```

**팀원 E가 나중에 병합 시도:**

```bash
git checkout develop
git pull origin develop
git checkout feature/model-lstm
git merge develop

# CONFLICT! 발생
```

**해결:**

```python
# src/models/train.py (최종)
def train_model(X_train, y_train, params=None):
    """
    모델 학습
    
    Args:
        X_train: 학습 데이터
        y_train: 타겟 데이터
        params: 모델 파라미터 (dict)
    """
    if params is None:
        params = {'n_estimators': 100}
    
    model = LGBMRegressor(**params)
    model.fit(X_train, y_train)
    return model
```

```bash
git add src/models/train.py
git commit -m "merge: develop 병합 및 충돌 해결"
git push origin feature/model-lstm
```

---

## 11. 데이터 공유 전략

### 문제: 데이터는 Git에 올리지 않음

**해결책 1: 구글 드라이브 (추천)**

1. **팀 공유 폴더 생성**
   - Google Drive에 "K-League Data" 폴더
   - 팀원 모두 편집 권한

2. **README에 안내:**
   ```markdown
   ## 데이터 다운로드
   
   1. [구글 드라이브 링크](https://drive.google.com/...)에서 다운로드
   2. `data/raw/` 폴더에 압축 해제
   
   필요한 파일:
   - train.csv
   - test.csv
   - match_info.csv
   ```

**해결책 2: DVC (Data Version Control)**

전문적인 데이터 버전 관리 (고급):

```bash
# 설치
pip install dvc

# 초기화
dvc init

# 데이터 추적
dvc add data/raw/train.csv

# Git에 커밋
git add data/raw/train.csv.dvc .gitignore
git commit -m "chore: DVC로 train.csv 추적"

# 원격 스토리지 설정 (Google Drive)
dvc remote add -d myremote gdrive://[folder-id]

# 데이터 푸시
dvc push
```

---

## 12. 체크리스트

### 프로젝트 시작 전

- [ ] GitHub 저장소 생성 (리더)
- [ ] .gitignore 설정
- [ ] README.md 작성
- [ ] 팀원 초대
- [ ] 브랜치 전략 합의
- [ ] 커밋 컨벤션 합의
- [ ] 역할 분담

### 작업 시작 전

- [ ] `git pull origin develop` (최신 코드)
- [ ] 새 브랜치 생성
- [ ] GitHub Issue 생성

### 작업 완료 후

- [ ] 테스트 실행
- [ ] 커밋 (의미 있는 메시지)
- [ ] 푸시
- [ ] Pull Request 생성
- [ ] 리뷰어 지정

### 코드 리뷰 시

- [ ] 코드 로직 검토
- [ ] 주석 확인
- [ ] 테스트 확인
- [ ] 스타일 일관성 확인
- [ ] 피드백 남기기

### PR 병합 후

- [ ] 브랜치 삭제
- [ ] 로컬 develop 업데이트
- [ ] Issue 닫기

---

## 13. 빠른 명령어 참고

```bash
# === 일상 작업 ===
git status                          # 현재 상태 확인
git add .                           # 모든 변경사항 스테이징
git commit -m "메시지"              # 커밋
git push                            # 푸시

# === 브랜치 ===
git branch                          # 브랜치 목록
git checkout -b feature/new         # 새 브랜치 생성 & 전환
git checkout develop                # 브랜치 전환
git merge feature/new               # 브랜치 병합

# === 동기화 ===
git pull origin develop             # 원격 최신 코드 받기
git fetch origin                    # 원격 정보만 받기

# === 되돌리기 ===
git reset --soft HEAD~1             # 마지막 커밋 취소 (변경사항 유지)
git reset --hard HEAD~1             # 마지막 커밋 취소 (변경사항 삭제)
git revert HEAD                     # 되돌리기 커밋 생성

# === 정보 확인 ===
git log --oneline                   # 커밋 히스토리
git diff                            # 변경사항 비교
git remote -v                       # 원격 저장소 정보
```

---

## 14. 추가 리소스

### 학습 자료
- [Git 공식 문서 (한국어)](https://git-scm.com/book/ko/v2)
- [GitHub 가이드](https://guides.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/ko/v1.0.0/)

### Cursor 단축키
- `Ctrl + Shift + G`: Source Control 열기
- `Ctrl + K Ctrl + C`: 커밋
- `Ctrl + Shift + P`: 명령 팔레트
  - "Git: Pull"
  - "Git: Push"
  - "Git: Checkout to..."

---

## 🎯 성공하는 팀 협업의 핵심

1. **소통이 80%**: 막히면 바로 물어보기
2. **작은 단위로 자주**: 큰 작업은 작게 나누기
3. **리뷰는 빠르게**: 24시간 내 리뷰 완료
4. **테스트 필수**: 망가진 코드는 푸시하지 않기
5. **문서화**: README와 주석은 필수

---

**이제 GitHub 협업 준비 완료!** 🚀

팀원들과 함께 효율적으로 작업하세요!
