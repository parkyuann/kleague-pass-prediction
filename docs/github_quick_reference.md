# 🚀 GitHub 협업 - 빠른 실행 가이드

## 📌 5분 셋업 (리더용)

### 1. GitHub 저장소 생성
```
1. github.com 로그인
2. New repository → kleague-pass-prediction
3. Private 선택
4. Python .gitignore 선택
5. Create
```

### 2. 로컬 연결
```bash
cd E:\Dacon\open_track1

git init
git remote add origin https://github.com/username/kleague-pass-prediction.git

# .gitignore 생성 (아래 코드 복사)
git add .
git commit -m "Initial commit"
git push -u origin main

# develop 브랜치 생성
git checkout -b develop
git push origin develop
```

### 3. .gitignore 필수!
```gitignore
# 가상환경
venv/
env/

# Python
__pycache__/
*.pyc

# 데이터 (중요!)
data/raw/*.csv
data/raw/*.xlsx
*.csv
*.xlsx
*.h5
*.pkl

# 노트북 체크포인트
.ipynb_checkpoints

# IDE
.vscode/
.idea/

# 로그
logs/*.log

# OS
.DS_Store
Thumbs.db
```

---

## 📥 팀원 합류 (5분)

### 1. 저장소 클론
```bash
cd E:\Dacon
git clone https://github.com/username/kleague-pass-prediction.git
cd kleague-pass-prediction
```

### 2. 환경 설정
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 데이터 복사
```bash
# Dacon에서 다운로드 후
copy "다운로드경로\train.csv" data\raw\
copy "다운로드경로\test.csv" data\raw\
copy "다운로드경로\match_info.csv" data\raw\
```

---

## 💼 매일 작업 루틴

### 아침 (작업 시작 전)
```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-work  # 또는 기존 브랜치로
git merge develop  # 최신 코드 반영
```

### 작업 중
```bash
# 파일 수정 후...
git status  # 변경사항 확인

git add .  # 또는 특정 파일만
git commit -m "feat: 기능 추가"

# 하루 1-2회 푸시
git push origin feature/my-work
```

### 저녁 (작업 완료)
```bash
# 마지막 커밋 & 푸시
git add .
git commit -m "feat: 오늘 작업 완료"
git push origin feature/my-work

# GitHub에서 Pull Request 생성
```

---

## 🔀 브랜치 전략 (간단 버전)

```
main (최종 제출용)
│
develop (개발 통합)
│
├── feature/eda (팀원 A)
├── feature/preprocessing (팀원 B)
├── feature/features (팀원 C)
├── feature/model-lgbm (팀원 D)
└── feature/model-lstm (팀원 E)
```

### 브랜치 명명
```bash
feature/spatial-features    # 새 기능
fix/result-name-bug        # 버그 수정
docs/readme-update         # 문서
```

---

## 📝 커밋 메시지 규칙

```bash
# 형식
<타입>: <제목>

# 타입
feat:     새 기능
fix:      버그 수정
docs:     문서
refactor: 리팩토링
test:     테스트
chore:    기타

# 예시
git commit -m "feat: 패스 거리 계산 함수 추가"
git commit -m "fix: result_name 결측치 처리 버그 수정"
git commit -m "docs: README 업데이트"
```

---

## 🔄 Pull Request 워크플로우

### 1. PR 생성 (GitHub 웹)
```
1. Pull requests → New pull request
2. base: develop ← compare: feature/my-work
3. 제목: [Feature] 공간 피처 추가
4. 설명 작성
5. Reviewers 지정
6. Create
```

### 2. 코드 리뷰 (팀원)
```
1. Files changed 확인
2. 댓글 남기기
3. Review changes → Approve
```

### 3. Merge (작성자)
```
1. 리뷰 승인 확인
2. Merge pull request
3. Delete branch (옵션)
```

### 4. 로컬 업데이트 (모두)
```bash
git checkout develop
git pull origin develop
```

---

## ⚠️ 충돌 해결

### 충돌 발생 시
```bash
git merge develop
# CONFLICT 메시지

# Cursor에서 파일 열기
# <<<<<<< HEAD
# 내 코드
# =======
# 다른 사람 코드
# >>>>>>> develop

# 하나 선택하고 마커 제거
git add 파일명
git commit -m "merge: 충돌 해결"
git push
```

### 충돌 예방
```
✅ 매일 아침 develop 동기화
✅ 작은 단위로 자주 커밋
✅ 다른 파일 작업 (역할 분담)
✅ 작업 전 팀원과 소통
```

---

## 🆘 자주 쓰는 명령어

```bash
# 현재 상태 확인
git status

# 변경사항 확인
git diff

# 커밋 히스토리
git log --oneline

# 브랜치 목록
git branch -a

# 브랜치 전환
git checkout develop

# 새 브랜치
git checkout -b feature/new-work

# 최신 코드 받기
git pull origin develop

# 푸시
git push origin 브랜치명

# 마지막 커밋 취소 (변경사항 유지)
git reset --soft HEAD~1

# 원격 브랜치 정보 갱신
git fetch origin
```

---

## 🎯 Cursor에서 Git 사용

### GUI 사용 (추천!)
```
Ctrl + Shift + G : Source Control 열기

변경 파일 확인 → + 버튼 (Stage)
메시지 입력 → Ctrl + Enter (Commit)
하단 상태바 → ↑↓ 버튼 (Push/Pull)
하단 브랜치명 클릭 → 브랜치 전환
```

### 단축키
```
Ctrl + Shift + G : Source Control
Ctrl + K Ctrl + C : 커밋
Ctrl + Shift + P : 명령 팔레트
  → Git: Pull
  → Git: Push
  → Git: Checkout
```

---

## 📋 역할 분담 템플릿

| 팀원 | 브랜치 | 작업 |
|------|--------|------|
| A (리더) | develop 관리 | Git 관리, 통합 |
| B | feature/eda | EDA, 전처리 |
| C | feature/features | 피처 엔지니어링 |
| D | feature/model-1 | LightGBM |
| E | feature/model-2 | LSTM |

---

## ✅ 데일리 체크리스트

### 작업 시작
- [ ] git pull origin develop
- [ ] 브랜치 확인/생성
- [ ] 최신 코드 반영

### 작업 중
- [ ] 의미 있는 단위로 커밋
- [ ] 커밋 메시지 규칙 준수
- [ ] 하루 1-2회 푸시

### 작업 종료
- [ ] 최종 커밋 & 푸시
- [ ] PR 생성 (완료 시)
- [ ] 팀 채널에 진행상황 공유

---

## 🐛 트러블슈팅

### Push 거부됨
```bash
git pull origin 브랜치명
# 충돌 해결
git push origin 브랜치명
```

### 실수로 잘못 커밋
```bash
# 아직 푸시 안 했으면
git reset --soft HEAD~1

# 이미 푸시했으면
git revert HEAD
git push
```

### 대용량 파일 에러
```bash
# .gitignore에 추가
echo "파일명" >> .gitignore
git rm --cached 파일명
git commit -m "chore: 대용량 파일 제거"
git push
```

---

## 📊 주간 미팅 템플릿

```markdown
## 주간 미팅 - 2025.12.XX

### 지난 주 완료
- [x] EDA 완료
- [x] 전처리 파이프라인

### 이번 주 목표
- [ ] 공간 피처 (@C)
- [ ] LightGBM 베이스라인 (@D)
- [ ] LSTM 실험 (@E)

### 블로커
- GPU 메모리 부족 → 배치 크기 조정

### 다음 액션
- 각자 브랜치에서 작업
- 목요일까지 PR 생성
```

---

## 💡 협업 꿀팁

### 1. 소통이 전부
```
✅ 막히면 바로 물어보기
✅ 팀 채널 활성화
✅ 진행상황 공유
```

### 2. 작은 단위로 자주
```
✅ 큰 작업은 작게 나누기
✅ 하루 2-3회 커밋
✅ 금요일에 큰 변경 ❌
```

### 3. 코드 리뷰 빠르게
```
✅ 24시간 내 리뷰
✅ 건설적인 피드백
✅ 칭찬도 함께!
```

### 4. 테스트는 필수
```
✅ 커밋 전 코드 실행
✅ 망가진 코드 푸시 ❌
✅ 노트북 전체 실행 확인
```

---

## 🎓 첫 PR 만들기 (실습)

### 팀원 C의 첫 작업 예시

```bash
# 1. 최신 코드
git checkout develop
git pull origin develop

# 2. 새 브랜치
git checkout -b feature/spatial-features

# 3. 작업: notebooks/03_features.ipynb 작성

# 4. 커밋
git add notebooks/03_features.ipynb
git commit -m "feat: 공간 피처 노트북 추가"

# 5. 푸시
git push origin feature/spatial-features

# 6. GitHub에서 PR 생성
#    - Title: [Feature] 공간 피처 추가
#    - Base: develop
#    - Reviewers: 팀원 A, D

# 7. 리뷰 받고 Merge!
```

---

## 📦 데이터 공유 방법

### 옵션 1: Google Drive (추천)
```
1. 팀 폴더 생성
2. 데이터 업로드
3. README에 링크 추가
4. 팀원들이 다운로드
```

### 옵션 2: 팀 공유 서버
```
회사/학교 서버 활용
```

### 중요!
```
❌ Git에 데이터 올리지 말기
✅ .gitignore에 추가
✅ README에 다운로드 방법 안내
```

---

## 🎯 최종 체크리스트

### 프로젝트 시작 전
- [ ] GitHub 저장소 생성
- [ ] .gitignore 설정
- [ ] 팀원 초대
- [ ] 브랜치 전략 합의
- [ ] 역할 분담

### 매일
- [ ] 아침: git pull
- [ ] 작업: commit & push
- [ ] 저녁: 진행상황 공유

### PR 생성 시
- [ ] 코드 테스트
- [ ] 커밋 메시지 확인
- [ ] 리뷰어 지정
- [ ] 설명 작성

---

**준비 완료! 이제 팀과 함께 시작하세요!** 🚀

막히면 이 문서 다시 보거나 팀원에게 물어보기!
