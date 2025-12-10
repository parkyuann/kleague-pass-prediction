# 🚀 팀원 시작 가이드 (TEAM START GUIDE)

> **처음 이 프로젝트에 참여하는 팀원을 위한 완벽한 가이드**

이 문서 하나만 따라하면 **30분 안에** 프로젝트를 시작할 수 있습니다! 💪

---

## 📋 목차

1. [환경 설정 (10분)](#1-환경-설정-10분)
2. [데이터 준비 (5분)](#2-데이터-준비-5분)
3. [Cursor IDE 설정 (5분)](#3-cursor-ide-설정-5분)
4. [Git 기본 사용법 (5분)](#4-git-기본-사용법-5분)
5. [첫 작업 시작 (5분)](#5-첫-작업-시작-5분)
6. [필독 문서](#6-필독-문서)
7. [트러블슈팅](#7-트러블슈팅)

---

## 1. 환경 설정 (10분)

### Step 1-1: Git 설치 확인

```bash
# Git 버전 확인
git --version

# 없으면 설치: https://git-scm.com/download/win
```

### Step 1-2: Python 확인

```bash
# Python 버전 확인 (3.8 이상)
python --version
```

### Step 1-3: 저장소 클론

```bash
# 작업할 폴더로 이동
cd E:\Dacon

# 저장소 클론
git clone https://github.com/parkyuann/kleague-pass-prediction.git

# 프로젝트 폴더로 이동
cd kleague-pass-prediction
```

**예상 출력:**
```
Cloning into 'kleague-pass-prediction'...
remote: Enumerating objects: 20, done.
remote: Counting objects: 100% (20/20), done.
...
```

### Step 1-4: 가상환경 생성

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
.\venv\Scripts\activate

# 활성화 확인 (프롬프트 앞에 (venv) 표시)
# (venv) PS E:\Dacon\kleague-pass-prediction>
```

**PowerShell 실행 정책 오류 발생 시:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\activate
```

### Step 1-5: 패키지 설치

```bash
# requirements.txt에서 패키지 설치
pip install -r requirements.txt

# Jupyter 커널 설치
python -m ipykernel install --user --name=venv
```

**예상 소요 시간:** 2-3분

### ✅ 환경 설정 완료 확인

```bash
# Python 패키지 확인
pip list

# 주요 패키지 있는지 확인:
# - pandas
# - numpy
# - lightgbm
# - scikit-learn
# - jupyter
```

---

## 2. 데이터 준비 (5분)

### Step 2-1: 데이터 다운로드

**중요!** 데이터 파일은 Git에 포함되지 않습니다.

1. **Dacon 경진대회 페이지** 접속
2. **다운로드 섹션**에서 다음 파일 다운로드:
   - `train.csv` (약 XX MB)
   - `test.csv` (약 XX MB)
   - `match_info.csv` (약 XX MB)
   - `sample_submission.csv`

### Step 2-2: 데이터 복사

#### Windows 명령어:
```bash
# data/raw 폴더가 있는지 확인
dir data\raw

# 다운로드한 파일 복사
copy "C:\Users\사용자명\Downloads\train.csv" data\raw\
copy "C:\Users\사용자명\Downloads\test.csv" data\raw\
copy "C:\Users\사용자명\Downloads\match_info.csv" data\raw\
copy "C:\Users\사용자명\Downloads\sample_submission.csv" data\raw\
```

#### 또는 파일 탐색기 사용:
1. 다운로드 폴더에서 파일 선택
2. `Ctrl + C` (복사)
3. `kleague-pass-prediction/data/raw/` 폴더 열기
4. `Ctrl + V` (붙여넣기)

### Step 2-3: 데이터 확인

```bash
# 파일 목록 확인
dir data\raw

# 예상 출력:
# train.csv
# test.csv
# match_info.csv
# sample_submission.csv
```

---

## 3. Cursor IDE 설정 (5분)

### Step 3-1: Cursor 설치

1. https://cursor.com 접속
2. 다운로드 & 설치
3. 실행

### Step 3-2: 프로젝트 폴더 열기

```
Cursor 메뉴:
File → Open Folder
→ kleague-pass-prediction 선택
```

### Step 3-3: Python 인터프리터 설정

```
1. Ctrl + Shift + P (명령 팔레트)
2. "Python: Select Interpreter" 입력
3. venv 선택:
   .\venv\Scripts\python.exe
```

### Step 3-4: 확장 프로그램 설치 (자동)

프로젝트를 열면 Cursor가 자동으로 추천합니다:
- ✅ Python
- ✅ Jupyter
- ✅ Pylance

**"Install" 버튼 클릭**

### Step 3-5: 노트북 테스트

```
1. notebooks/01_EDA.ipynb 열기
2. 우측 상단에서 커널 선택: venv
3. 첫 번째 셀 실행: Shift + Enter
```

**성공 출력:**
```
✓ 학습 데이터: XXX,XXX 행
✓ 경기 정보: XXX 행
```

---

## 4. Git 기본 사용법 (5분)

### 🌿 브랜치 개념 이해

```
main (최종 제출)
│
develop (개발 통합) ← 여기서 작업!
│
├── feature/eda (당신의 브랜치)
├── feature/preprocessing
└── feature/model-lgbm
```

### 📅 매일 사용할 명령어

#### 아침 (작업 시작 전)
```bash
# 1. develop 브랜치로 전환
git checkout develop

# 2. 최신 코드 받기
git pull origin develop

# 3. 내 작업 브랜치 생성 (첫 날만)
git checkout -b feature/내이름-작업내용

# 또는 기존 브랜치로 전환
git checkout feature/내이름-작업내용

# 4. develop의 최신 코드 반영
git merge develop
```

#### 작업 중
```bash
# 변경사항 확인
git status

# 모든 변경사항 스테이징
git add .

# 커밋 (의미 있는 메시지!)
git commit -m "feat: 작업 내용 설명"

# 원격 저장소에 푸시 (하루 1-2회)
git push origin feature/내이름-작업내용
```

#### 저녁 (작업 완료)
```bash
# 마지막 커밋 & 푸시
git add .
git commit -m "feat: 오늘 작업 완료"
git push origin feature/내이름-작업내용

# GitHub에서 Pull Request 생성 (완료 시)
```

### 📝 커밋 메시지 규칙

```bash
# 좋은 예 ✅
git commit -m "feat: 공간 피처 추가 (거리, 각도)"
git commit -m "fix: result_name 결측치 처리 버그 수정"
git commit -m "docs: EDA 노트북 주석 추가"

# 나쁜 예 ❌
git commit -m "수정"
git commit -m "작업중"
git commit -m "ㅁㄴㅇㄹ"
```

### 🔧 Cursor에서 Git 사용 (더 쉬움!)

```
1. Ctrl + Shift + G (Source Control)
2. 변경된 파일 확인
3. + 버튼 (Stage)
4. 메시지 입력
5. Ctrl + Enter (Commit)
6. ... 메뉴 → Push
```

---

## 5. 첫 작업 시작 (5분)

### Step 5-1: 브랜치 생성

```bash
# 최신 코드 받기
git checkout develop
git pull origin develop

# 내 브랜치 생성 (예: EDA 담당)
git checkout -b feature/김철수-eda
```

### Step 5-2: 노트북 작성

```
1. Cursor에서 notebooks/ 폴더 열기
2. 01_EDA.ipynb 또는 새 노트북 생성
3. 코드 작성 시작
```

### Step 5-3: Cursor AI 활용

```python
# 주석으로 목표 작성
# "train 데이터의 기본 통계를 보여줘"

# Ctrl + I (Composer) 누르면 AI가 코드 생성!
```

```python
# 또는 Ctrl + L (Chat)로 물어보기
# "패스 거리를 계산하는 함수가 필요해"
```

### Step 5-4: 커밋 & 푸시

```bash
# 작업 후
git add notebooks/01_EDA.ipynb
git commit -m "feat: EDA 노트북 초안 작성"
git push origin feature/김철수-eda
```

### Step 5-5: Pull Request 생성

**작업 완료되면 GitHub에서:**

```
1. 저장소 페이지 접속
2. "Pull requests" 탭
3. "New pull request" 버튼
4. base: develop ← compare: feature/김철수-eda
5. 제목: [Feature] EDA 분석 완료
6. 설명 작성:
   - 변경 사항
   - 주요 발견사항
   - 리뷰 포인트
7. Reviewers 지정 (팀장 등)
8. "Create pull request"
```

---

## 6. 필독 문서

### 🔥 지금 바로 읽기 (10분)

1. **[github_quick_reference.md](github_quick_reference.md)** ⭐⭐⭐
   - Git 명령어 빠른 참조
   - 매일 사용할 내용
   - **꼭 읽기!**

2. **[cursor_quick_start.md](cursor_quick_start.md)** ⭐⭐⭐
   - Cursor 5분 셋업
   - 단축키 정리
   - **꼭 읽기!**

### 📖 여유 있을 때 읽기 (30분)

3. **[cursor_setup_guide.md](cursor_setup_guide.md)**
   - Cursor AI 100% 활용
   - 고급 기능

4. **[github_collaboration_guide.md](github_collaboration_guide.md)**
   - Git 협업 상세 가이드
   - 브랜치 전략

5. **[github_roles_guide.md](github_roles_guide.md)**
   - 역할별 가이드
   - 자기 역할 부분 읽기

### 📊 피처 개발할 때 읽기

6. **[feature_engineering_guide.md](feature_engineering_guide.md)**
   - 피처 엔지니어링 이론

7. **[feature_engineering_quick_reference.md](feature_engineering_quick_reference.md)**
   - 피처 개발 빠른 참조

---

## 7. 트러블슈팅

### 문제 1: 가상환경 활성화 오류

**에러:**
```
.\venv\Scripts\activate : 이 시스템에서 스크립트를 실행할 수 없습니다
```

**해결:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\activate
```

---

### 문제 2: 모듈 import 오류

**에러:**
```python
ModuleNotFoundError: No module named 'pandas'
```

**해결:**
```bash
# 가상환경 활성화 확인
# (venv) 표시 있는지 확인

# 패키지 재설치
pip install -r requirements.txt
```

---

### 문제 3: 데이터 파일 못 찾음

**에러:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data\\raw\\train.csv'
```

**해결:**

**방법 1: 노트북에서 직접 로드 (빠름)**
```python
import pandas as pd
from pathlib import Path

# 프로젝트 루트 찾기
project_root = Path.cwd().parent
data_path = project_root / 'data' / 'raw'

# 데이터 로드
train = pd.read_csv(data_path / 'train.csv')
```

**방법 2: 데이터 파일 위치 확인**
```bash
# 파일 있는지 확인
dir data\raw\train.csv

# 없으면 Dacon에서 다운로드 후 복사
copy "다운로드경로\train.csv" data\raw\
```

---

### 문제 4: Jupyter Kernel 연결 안 됨

**에러:**
```
Jupyter kernel not found
```

**해결:**
```bash
# Jupyter 커널 재설치
pip install ipykernel
python -m ipykernel install --user --name=venv

# Cursor 재시작
```

---

### 문제 5: Git Push 거부됨

**에러:**
```
! [rejected] feature/my-work -> feature/my-work (fetch first)
```

**해결:**
```bash
# 원격 변경사항 받기
git pull origin feature/my-work

# 충돌 있으면 해결 후
git add .
git commit -m "merge: 충돌 해결"
git push origin feature/my-work
```

---

### 문제 6: 한글 깨짐 (matplotlib)

**증상:**
```python
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.xlabel('시간')  # 한글이 ㅁㅁㅁ로 표시
```

**해결:**
```python
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호

# 이제 한글 표시됨
plt.xlabel('시간')
```

---

## 8. 자주 묻는 질문 (FAQ)

### Q1: 브랜치 이름은 어떻게 짓나요?

```bash
# 형식: feature/이름-작업내용
feature/김철수-eda
feature/이영희-preprocessing
feature/박민수-spatial-features
feature/최지훈-lgbm-model
```

### Q2: 매일 얼마나 커밋해야 하나요?

```
✅ 추천: 하루 2-5회 커밋
✅ 작은 단위로 자주 커밋
❌ 한 번에 큰 작업 커밋하지 말기
```

### Q3: 코드 리뷰는 언제 하나요?

```
✅ PR 생성 후 24시간 내
✅ 팀원 2명 이상 승인
✅ 긍정적이고 건설적인 피드백
```

### Q4: 데이터는 어떻게 공유하나요?

```
❌ Git에 올리지 말 것! (용량 제한)
✅ 구글 드라이브 공유 폴더
✅ 팀 서버 (있다면)
```

### Q5: 충돌(Conflict)이 무서워요

```
💡 충돌은 자연스러운 현상!

예방:
✅ 매일 아침 git pull
✅ 작은 단위로 작업
✅ 다른 파일 작업 (역할 분담)

해결:
1. Cursor에서 충돌 파일 열기
2. <<<<<<< HEAD 부분 확인
3. 어느 코드 사용할지 선택
4. 마커 제거
5. 저장 & 커밋
```

### Q6: Cursor AI는 어떻게 사용하나요?

```python
# 방법 1: 주석으로 요청
# "패스 거리를 계산하는 함수 작성"
# Ctrl + I 누르면 코드 생성!

# 방법 2: Chat으로 물어보기
# Ctrl + L → "이 에러를 해결해줘"

# 방법 3: 파일 참조
# "@src/features/spatial.py의 함수를 개선해줘"
```

### Q7: 제 코드가 망가뜨릴까봐 걱정돼요

```
💡 걱정하지 마세요!

✅ develop 브랜치는 보호됨
✅ PR 승인 없이 병합 안 됨
✅ 언제든지 되돌릴 수 있음 (git revert)
✅ 팀원들이 리뷰해줌

🎯 실수하면서 배우는 게 정상!
```

---

## 9. 팀 규칙 (중요!)

### ✅ 꼭 지키기

1. **매일 아침**: `git pull origin develop`
2. **작은 단위**: 자주 커밋 (하루 2-5회)
3. **의미 있는 메시지**: "feat: XXX 추가"
4. **테스트 필수**: 커밋 전 코드 실행 확인
5. **24시간 리뷰**: PR 생성 후 빠르게 리뷰
6. **소통**: 막히면 바로 물어보기!

### ❌ 절대 금지

1. **데이터 파일 Git 업로드**: `.gitignore` 확인
2. **main 직접 푸시**: PR을 통해서만
3. **의미 없는 커밋**: "수정", "ㅁㄴㅇㄹ"
4. **테스트 안 된 코드**: 망가진 코드 푸시
5. **큰 파일 업로드**: 모델 파일, 로그 파일

---

## 10. 다음 단계

### ✅ 완료한 것

- [x] 환경 설정
- [x] 데이터 준비
- [x] Cursor 설정
- [x] Git 기본 사용법 학습
- [x] 첫 브랜치 생성

### 🎯 이제 할 일

1. **역할 확인**
   - 팀 미팅에서 역할 결정
   - `docs/github_roles_guide.md` 자기 역할 부분 읽기

2. **작업 시작**
   - 첫 번째 작업 선택
   - 노트북/코드 작성
   - 커밋 & 푸시

3. **팀원과 소통**
   - 진행 상황 공유
   - 막히는 부분 질문
   - 서로 도우기

---

## 11. 체크리스트

### 환경 설정
- [ ] Git 설치 확인
- [ ] Python 설치 확인
- [ ] 저장소 클론
- [ ] 가상환경 생성 & 활성화
- [ ] 패키지 설치
- [ ] Jupyter 커널 설치

### 데이터
- [ ] Dacon에서 데이터 다운로드
- [ ] data/raw/ 폴더에 복사
- [ ] 파일 목록 확인

### Cursor
- [ ] Cursor 설치
- [ ] 프로젝트 폴더 열기
- [ ] Python 인터프리터 설정
- [ ] 확장 프로그램 설치
- [ ] 노트북 테스트 실행

### Git
- [ ] develop 브랜치 확인
- [ ] 내 브랜치 생성
- [ ] 첫 커밋 성공
- [ ] 첫 푸시 성공

### 문서
- [ ] TEAM_START_GUIDE.md 읽기 (이 문서)
- [ ] github_quick_reference.md 읽기
- [ ] cursor_quick_start.md 읽기

---

## 12. 도움 받기

### 🆘 막혔을 때

1. **가이드 문서 확인**
   - 트러블슈팅 섹션
   - FAQ 섹션

2. **팀 채널에 질문**
   - Slack/Discord/카카오톡
   - 스크린샷 첨부

3. **GitHub Issues**
   - 버그 리포트
   - 기능 제안

4. **Cursor AI 활용**
   - Ctrl + L: "이 에러 해결 방법"
   - AI가 도와줌!

### 💬 질문 템플릿

```markdown
## 문제 상황
[무엇을 하려고 했는지]

## 에러 메시지
```
[에러 메시지 복사]
```

## 시도한 방법
1. [시도 1]
2. [시도 2]

## 환경
- OS: Windows 11
- Python: 3.10
- Cursor: Latest
```

---

## 🎉 시작 준비 완료!

모든 단계를 완료했다면:

```
✅ 환경 설정 완료
✅ 데이터 준비 완료
✅ Cursor 설정 완료
✅ Git 기본 사용법 숙지
✅ 첫 작업 준비 완료
```

**이제 팀원들과 함께 멋진 모델을 만들어봅시다!** 🚀

---

## 📞 연락처

- **팀 채널**: [Slack/Discord/카카오톡]
- **GitHub**: https://github.com/parkyuann/kleague-pass-prediction
- **프로젝트 리더**: [이름/연락처]

---

**Let's go! 💪**

화이팅! 🏆
