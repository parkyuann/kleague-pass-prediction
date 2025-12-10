# 🚀 Cursor에서 지금 바로 시작하기! (5분 완성)

## ✅ 준비물 체크리스트

- [x] Windows 10/11
- [x] Cursor 설치됨
- [x] Python 3.8+ 설치됨
- [x] 프로젝트 폴더: `E:\Dacon\open_track1\`
- [x] 다운로드한 파일들 저장됨

---

## 🎬 Step-by-Step 실행 (따라만 하면 됨!)

### Step 1: Cursor에서 프로젝트 폴더 열기

```
1. Cursor 실행
2. File → Open Folder (또는 Ctrl + K, Ctrl + O)
3. E:\Dacon\open_track1 선택
4. "Open" 클릭
```

**확인:** 좌측 Explorer에 파일 목록이 보이면 성공! ✅

---

### Step 2: 터미널 열기

```
방법 1: Ctrl + ` (백틱, 키보드 왼쪽 위)
방법 2: View → Terminal
방법 3: 상단 메뉴 → Terminal → New Terminal
```

**확인:** 하단에 터미널 창이 열리면 성공! ✅

---

### Step 3: 프로젝트 초기화 (중요!)

터미널에 **한 줄씩** 입력:

```bash
# 1. 현재 위치 확인
cd

# 2. 프로젝트 초기화 (자동으로 폴더 생성)
python setup_project_cursor.py
```

**예상 출력:**
```
======================================================================
🚀 K리그 패스 예측 프로젝트 초기화 (Cursor 최적화)
======================================================================

📁 Step 1: 디렉토리 구조 생성
----------------------------------------------------------------------
  ✓ .vscode/
  ✓ data/raw/
  ✓ notebooks/
  ...

✅ Cursor 최적화 프로젝트 초기화 완료!
```

**트러블슈팅:**
```
오류 발생 시:
- "python: command not found" → python3 setup_project_cursor.py 시도
- "파일을 찾을 수 없습니다" → 파일이 E:\Dacon\open_track1\ 에 있는지 확인
```

---

### Step 4: 가상환경 생성

터미널에 입력:

```bash
# 가상환경 생성 (1분 소요)
python -m venv venv
```

**확인:** 좌측 Explorer에 `venv` 폴더가 생기면 성공! ✅

---

### Step 5: 가상환경 활성화

터미널에 입력:

```bash
# Windows PowerShell 또는 cmd
.\venv\Scripts\activate
```

**확인:** 터미널 앞에 `(venv)` 표시되면 성공! ✅

```
예시:
(venv) PS E:\Dacon\open_track1>
```

**트러블슈팅 - PowerShell 실행 정책 오류:**
```powershell
# 오류 발생 시 (빨간 글씨로 "cannot be loaded..." 나오면)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 다시 활성화
.\venv\Scripts\activate
```

---

### Step 6: 패키지 설치 (2-3분 소요)

터미널에 입력:

```bash
# pip 업그레이드 (선택)
python -m pip install --upgrade pip

# 필수 패키지 설치
pip install -r requirements.txt
```

**확인:** 오류 없이 설치 완료되면 성공! ✅

---

### Step 7: Python 인터프리터 설정 (중요!)

```
1. Ctrl + Shift + P (명령 팔레트)
2. "Python: Select Interpreter" 타이핑
3. Enter 키
4. "Python 3.x.x ('venv': venv)" 선택
   (경로: .\venv\Scripts\python.exe)
```

**확인:** 우측 하단 상태바에 "Python 3.x.x ('venv')" 표시되면 성공! ✅

---

### Step 8: 첫 번째 노트북 열기

```
1. 좌측 Explorer에서 notebooks 폴더 펼치기
2. 01_EDA.ipynb 클릭
3. 우측 상단 "Select Kernel" 클릭
4. "Python Environments..." 선택
5. "Python 3.x.x venv" 선택
```

**확인:** 노트북이 열리고 셀을 실행할 수 있으면 성공! ✅

---

### Step 9: 첫 번째 셀 실행 테스트

노트북에서 첫 번째 셀 클릭 후:

```
Shift + Enter (또는 좌측 ▶️ 버튼 클릭)
```

**확인:** "✓ 프로젝트 루트: ..." 출력되면 완벽! 🎉

---

## 🎯 완료! 이제 시작할 준비 완료

### 현재 상태 확인

```
✅ Cursor에 프로젝트 열림
✅ 프로젝트 구조 생성됨
✅ 가상환경 활성화됨
✅ 패키지 설치 완료
✅ Python 인터프리터 설정됨
✅ 노트북 실행 가능
```

---

## 🤖 Cursor AI 기능 사용해보기

### 1. Cursor Chat 열기

```
Ctrl + L
```

**Chat 창에 입력:**
```
"train 데이터를 로드하고 기본 정보를 출력하는 코드를 작성해줘"
```

### 2. Composer 사용

```
Ctrl + I
```

**프롬프트 입력:**
```
"패스 거리를 계산하는 함수를 만들어줘"
```

### 3. 파일 참조

Chat에서:
```
"@01_EDA.ipynb의 코드를 설명해줘"
```

---

## 📁 생성된 파일 구조 확인

좌측 Explorer에서:

```
E:\Dacon\open_track1\
├── .vscode/              ✨ Cursor 설정 (자동 생성됨!)
│   ├── settings.json
│   ├── launch.json
│   └── extensions.json
│
├── data/
│   └── raw/              ✨ 데이터 파일 (자동 이동됨!)
│       ├── train.csv
│       ├── test.csv
│       └── ...
│
├── notebooks/            ✨ 여기서 작업!
│   └── 01_EDA.ipynb     (자동 생성됨)
│
├── src/                  ✨ 모듈 코드
│   ├── data/
│   │   └── load_data.py  (자동 생성됨)
│   └── utils/
│       └── metrics.py    (자동 생성됨)
│
├── venv/                 ✨ 가상환경
├── .gitignore           ✨ (자동 생성됨)
├── requirements.txt     ✨ (자동 생성됨)
└── README.md            ✨ (자동 생성됨)
```

---

## 🎨 추천 Cursor 확장 프로그램 설치

터미널에서 또는 Extensions (Ctrl + Shift + X):

```bash
# 자동으로 설치 (선택)
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension ms-python.vscode-pylance
```

**또는 수동 설치:**
1. Ctrl + Shift + X
2. 검색:
   - "Python" (Microsoft)
   - "Jupyter" (Microsoft)
   - "Pylance" (Microsoft)

---

## 💡 자주 사용하는 Cursor 단축키

| 기능 | 단축키 | 설명 |
|------|--------|------|
| 터미널 토글 | `Ctrl + `` | 터미널 열기/닫기 |
| Cursor Chat | `Ctrl + L` | AI Chat 열기 |
| Composer | `Ctrl + I` | 인라인 코드 생성 |
| 명령 팔레트 | `Ctrl + Shift + P` | 모든 명령 검색 |
| 파일 검색 | `Ctrl + P` | 파일 빠르게 찾기 |
| 사이드바 토글 | `Ctrl + B` | 좌측 Explorer 토글 |
| 저장 | `Ctrl + S` | 파일 저장 |
| 노트북 셀 실행 | `Shift + Enter` | 현재 셀 실행 |

---

## 🚨 문제 해결 (FAQ)

### Q1: "python: command not found"
```bash
# python3로 시도
python3 setup_project_cursor.py
python3 -m venv venv
```

### Q2: 가상환경 활성화 안 됨
```powershell
# PowerShell에서
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\activate
```

### Q3: 모듈 import 오류
```python
# 노트북 최상단에 추가
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent))
```

### Q4: Jupyter Kernel 연결 안 됨
```bash
# 터미널에서
pip install ipykernel
python -m ipykernel install --user --name=venv
```

### Q5: 한글 깨짐
```python
# 노트북에 추가
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
```

---

## 🎯 다음 단계

### 1. EDA 노트북 완성하기

`notebooks/01_EDA.ipynb`에서:

```python
# Ctrl + L (Chat)에 물어보기:
"train 데이터의 결측치를 확인하는 코드를 작성해줘"
"액션 타입별 분포를 막대그래프로 그려줘"
"경기장 좌표를 scatter plot으로 시각화해줘"
```

### 2. Feature Engineering 시작

`cursor_setup_guide.md` 읽고:
- Cursor AI 활용법 학습
- Feature 생성 전략 이해

`feature_engineering_quick_reference.md` 참고:
- 필수 Feature 10개 구현
- 빠른 참조용

### 3. 모델링

`notebooks/04_Baseline_Model.ipynb` 생성:
- LightGBM 베이스라인
- 평가 지표 확인

---

## 📚 제공된 파일 활용법

### Cursor 전용 파일 (우선 읽기!)

1. **`cursor_setup_guide.md`** ⭐⭐⭐
   - Cursor AI 100% 활용법
   - 단축키, 팁, 트릭

2. **`setup_project_cursor.py`** ⭐⭐⭐
   - 방금 실행한 파일
   - 자동 프로젝트 구조 생성

3. **`vscode_settings.json`**
   - 상세 설정 (필요시 참고)
   - `.vscode/settings.json`에 적용

### Feature Engineering 파일

4. **`feature_engineering_quick_reference.md`** ⭐⭐⭐
   - 20분이면 구현 가능
   - 코딩 시 옆에 두고 참조

5. **`feature_engineering_implementation.py`**
   - 복사해서 사용할 코드
   - `src/features/` 로 이동

### 기타 가이드

6. **`project_structure_guide.md`**
   - 프로젝트 구조 상세 설명

7. **`quick_start_guide.md`**
   - 일반 환경 시작 가이드

---

## ✅ 최종 체크리스트

시작 전:
- [x] Cursor에 프로젝트 열림
- [x] setup_project_cursor.py 실행
- [x] 가상환경 활성화 `(venv)` 표시 확인
- [x] pip install 완료
- [x] Python 인터프리터 venv 설정
- [x] 01_EDA.ipynb 셀 실행 확인

Cursor AI 테스트:
- [x] Ctrl + L (Chat) 작동
- [x] Ctrl + I (Composer) 작동
- [x] @ 파일 참조 작동

---

## 🎉 축하합니다!

**모든 설정이 완료되었습니다!**

이제 `Ctrl + L`을 눌러서:
```
"K리그 패스 예측 프로젝트를 시작하려고 해. 
첫 번째로 무엇을 해야 할까?"
```

라고 물어보세요! 🚀

---

**Cursor + AI로 빠르게 개발하세요!** ⚡⚽
