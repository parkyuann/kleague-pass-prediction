# 👥 역할별 GitHub 협업 가이드

## 🎯 역할 소개

프로젝트를 효율적으로 진행하기 위한 5가지 역할과 각 역할별 구체적인 작업 가이드입니다.

---

## 1️⃣ 팀장/프로젝트 매니저 (PM)

### 🎖️ 주요 책임
- 전체 일정 관리
- Git 저장소 관리
- 팀원 조율 및 통합
- 코드 리뷰 최종 승인

### 📅 첫 날 해야 할 일

```bash
# 1. GitHub 저장소 생성
# github.com → New repository → kleague-pass-prediction

# 2. 로컬 프로젝트 연결
cd E:\Dacon\open_track1
git init
git remote add origin https://github.com/username/kleague-pass-prediction.git

# 3. .gitignore 설정 (중요!)
# (별도 파일 참조)

# 4. 첫 커밋
git add .
git commit -m "Initial commit: 프로젝트 초기 설정"
git push -u origin main

# 5. develop 브랜치 생성
git checkout -b develop
git push origin develop

# 6. 브랜치 보호 규칙 설정 (GitHub 웹)
# Settings → Branches → Add rule
# - Branch name pattern: main
# - Require pull request reviews before merging ✓
```

### 📋 GitHub Project 설정

```
1. Projects → New project → Board
2. 컬럼 생성:
   - 📝 To Do
   - 🏃 In Progress
   - 👀 Review
   - ✅ Done

3. 초기 이슈 생성:
   #1: EDA 및 데이터 분석
   #2: 데이터 전처리 파이프라인
   #3: 피처 엔지니어링
   #4: 베이스라인 모델 (LightGBM)
   #5: 딥러닝 모델 (LSTM)
   #6: 앙상블 및 최적화
```

### 🔄 일일 루틴

```bash
# 아침
- [ ] 팀원 PR 확인
- [ ] 긴급 이슈 체크
- [ ] 프로젝트 보드 업데이트

# 작업 중
- [ ] PR 리뷰 (24시간 내)
- [ ] 충돌 발생 시 팀원 지원
- [ ] 진행 상황 모니터링

# 저녁
- [ ] develop 브랜치 상태 확인
- [ ] 내일 작업 계획
- [ ] 팀 채널 공지
```

### 🔍 코드 리뷰 체크리스트

```markdown
## 코드 품질
- [ ] 코드가 실행되는가?
- [ ] 주석이 적절한가?
- [ ] 변수명이 명확한가?

## 프로젝트 통합
- [ ] 다른 모듈과 충돌 없는가?
- [ ] 디렉토리 구조 준수했는가?
- [ ] requirements.txt 업데이트 필요한가?

## 데이터 규칙
- [ ] 대용량 파일 포함 안 했는가?
- [ ] 경로가 상대 경로인가?
- [ ] .gitignore 규칙 준수했는가?
```

### 📊 주간 미팅 진행

```markdown
## 주간 미팅 - Week 1

### 목표 (이번 주)
- [ ] EDA 완료 (@팀원B)
- [ ] 전처리 파이프라인 (@팀원B)
- [ ] 공간 피처 구현 (@팀원C)

### 진행 상황
- ✅ 프로젝트 환경 설정 완료
- 🏃 EDA 진행 중 (50%)
- 📝 전처리 계획 수립

### 블로커
- 서버 GPU 부족 → 배치 크기 조정으로 해결
- result_name 결측치 → 규칙 기반 대체

### 다음 주 계획
- 피처 엔지니어링 본격 시작
- 베이스라인 모델 실험
```

---

## 2️⃣ EDA/전처리 담당

### 📊 주요 책임
- 데이터 탐색 및 시각화
- 결측치 처리 전략
- 데이터 전처리 파이프라인 구축

### 🚀 작업 시작

```bash
# 브랜치 생성
git checkout develop
git pull origin develop
git checkout -b feature/eda

# 노트북 작성
notebooks/01_EDA.ipynb
notebooks/02_preprocessing.ipynb
```

### 📝 EDA 체크리스트

```python
# notebooks/01_EDA.ipynb

## 1. 데이터 로드 및 기본 정보
- [ ] train.csv 로드
- [ ] match_info.csv 로드
- [ ] 데이터 형태 확인 (shape, dtypes)
- [ ] 결측치 확인
- [ ] 중복 데이터 확인

## 2. 기술 통계
- [ ] 수치형 변수 분포
- [ ] 범주형 변수 빈도
- [ ] 타겟 변수 (end_x, end_y) 분포

## 3. 시각화
- [ ] 패스 위치 히트맵
- [ ] 패스 방향 벡터 플롯
- [ ] 시간대별 패턴
- [ ] 팀별 패턴

## 4. 인사이트 도출
- [ ] 주요 발견사항 정리
- [ ] 이상치 분석
- [ ] 전처리 전략 제안
```

### 🔧 전처리 파이프라인

```python
# src/data/preprocessing.py

"""
데이터 전처리 모듈
작성자: 팀원 B
"""

import pandas as pd
import numpy as np

class DataPreprocessor:
    """데이터 전처리 파이프라인"""
    
    def __init__(self):
        self.fitted = False
    
    def fit_transform(self, df):
        """학습 데이터 전처리"""
        df = df.copy()
        
        # 1. 결측치 처리
        df = self._handle_missing_values(df)
        
        # 2. 이상치 처리
        df = self._handle_outliers(df)
        
        # 3. 타입 변환
        df = self._convert_types(df)
        
        self.fitted = True
        return df
    
    def transform(self, df):
        """테스트 데이터 전처리"""
        if not self.fitted:
            raise ValueError("먼저 fit_transform을 호출하세요")
        
        df = df.copy()
        df = self._handle_missing_values(df)
        df = self._handle_outliers(df)
        df = self._convert_types(df)
        
        return df
    
    def _handle_missing_values(self, df):
        """결측치 처리"""
        # result_name 결측치는 'Unknown'으로
        if 'result_name' in df.columns:
            df['result_name'] = df['result_name'].fillna('Unknown')
        
        return df
    
    def _handle_outliers(self, df):
        """이상치 처리"""
        # 필드 범위 벗어난 좌표 클리핑
        if 'start_x' in df.columns:
            df['start_x'] = df['start_x'].clip(0, 105)
        if 'start_y' in df.columns:
            df['start_y'] = df['start_y'].clip(0, 68)
        
        return df
    
    def _convert_types(self, df):
        """데이터 타입 변환"""
        # 범주형 변수
        cat_cols = ['type_name', 'result_name']
        for col in cat_cols:
            if col in df.columns:
                df[col] = df[col].astype('category')
        
        return df
```

### 📤 작업 완료 후

```bash
# 커밋
git add .
git commit -m "feat: EDA 및 전처리 파이프라인 완료"

# 푸시
git push origin feature/eda

# PR 생성 (GitHub)
# Title: [Feature] EDA 및 전처리 완료
# Description:
# - 데이터 기본 분석 완료
# - 결측치 처리 전략 수립
# - 전처리 파이프라인 구현
# - 주요 인사이트 문서화
```

---

## 3️⃣ 피처 엔지니어링 담당

### 🛠️ 주요 책임
- 공간 기반 피처 생성
- 시간 기반 피처 생성
- 팀/선수 컨텍스트 피처

### 🚀 작업 시작

```bash
# 브랜치 생성
git checkout develop
git pull origin develop
git checkout -b feature/feature-engineering
```

### 📝 피처 개발 체크리스트

```python
# src/features/engineering.py

## 공간 피처 (Spatial Features)
- [ ] pass_distance: 패스 거리
- [ ] pass_angle: 패스 각도
- [ ] distance_to_goal: 골대까지 거리
- [ ] position_type: 위치 타입 (수비/중원/공격)

## 시간 피처 (Temporal Features)
- [ ] time_in_period: 피리어드 내 시간
- [ ] sequence_length: 에피소드 길이
- [ ] action_interval: 이전 액션과의 시간 간격

## 팀 피처 (Team Features)
- [ ] possession_time: 점유 시간
- [ ] pass_success_rate: 패스 성공률 (과거)
- [ ] team_score_diff: 득점 차이

## 에피소드 피처 (Episode Features)
- [ ] episode_momentum: 에피소드 진행 방향
- [ ] pressure_score: 상대 압박 수준
```

### 💻 구현 예시

```python
# src/features/spatial.py

"""
공간 기반 피처 엔지니어링
작성자: 팀원 C
"""

import numpy as np
import pandas as pd

def calculate_distance(x1, y1, x2, y2):
    """두 점 사이의 유클리드 거리"""
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_angle(x1, y1, x2, y2):
    """패스 각도 (라디안)"""
    return np.arctan2(y2 - y1, x2 - x1)

def distance_to_goal(x, y, goal_x=105, goal_y=34):
    """골대 중앙까지의 거리"""
    return np.sqrt((goal_x - x)**2 + (goal_y - y)**2)

def create_spatial_features(df):
    """공간 피처 생성"""
    df = df.copy()
    
    # 패스 거리
    df['pass_distance'] = calculate_distance(
        df['start_x'], df['start_y'],
        df['end_x'], df['end_y']
    )
    
    # 패스 각도
    df['pass_angle'] = calculate_angle(
        df['start_x'], df['start_y'],
        df['end_x'], df['end_y']
    )
    
    # 시작 위치에서 골대까지 거리
    df['start_dist_to_goal'] = distance_to_goal(
        df['start_x'], df['start_y']
    )
    
    # 위치 타입 (수비/중원/공격)
    df['position_type'] = pd.cut(
        df['start_x'],
        bins=[0, 35, 70, 105],
        labels=['defensive', 'midfield', 'attacking']
    )
    
    return df
```

### 🧪 테스트 코드

```python
# notebooks/03_feature_engineering.ipynb

# 테스트
from src.features.spatial import create_spatial_features

# 샘플 데이터로 테스트
sample = train.head(100)
sample_with_features = create_spatial_features(sample)

# 확인
print("생성된 피처:")
print(sample_with_features.columns.tolist())

print("\n결측치 확인:")
print(sample_with_features.isnull().sum())

print("\n피처 통계:")
print(sample_with_features[['pass_distance', 'pass_angle', 
                             'start_dist_to_goal']].describe())
```

---

## 4️⃣ 모델링 담당 1 (전통적 ML)

### 🤖 주요 책임
- LightGBM, XGBoost 모델 구현
- 하이퍼파라미터 튜닝
- 베이스라인 구축

### 🚀 작업 시작

```bash
git checkout develop
git pull origin develop
git checkout -b feature/model-lgbm
```

### 📝 모델링 체크리스트

```python
## 베이스라인 모델
- [ ] LightGBM 구현
- [ ] 기본 파라미터로 학습
- [ ] CV 스코어 확인

## 피처 중요도 분석
- [ ] 중요도 시각화
- [ ] 불필요한 피처 제거

## 하이퍼파라미터 튜닝
- [ ] Grid Search
- [ ] Optuna 자동 튜닝

## 앙상블
- [ ] K-Fold CV
- [ ] 예측값 평균
```

### 💻 모델 구현

```python
# src/models/lgbm_model.py

"""
LightGBM 모델
작성자: 팀원 D
"""

import lightgbm as lgb
from sklearn.model_selection import KFold
import numpy as np

class LGBMModel:
    """LightGBM 회귀 모델"""
    
    def __init__(self, params=None):
        self.params = params or self._default_params()
        self.models = []
        self.feature_importance = None
    
    def _default_params(self):
        """기본 하이퍼파라미터"""
        return {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': -1
        }
    
    def train(self, X, y, n_splits=5):
        """K-Fold Cross Validation 학습"""
        kfold = KFold(n_splits=n_splits, shuffle=True, random_state=42)
        
        for fold, (train_idx, val_idx) in enumerate(kfold.split(X)):
            print(f"Fold {fold + 1}/{n_splits}")
            
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            train_data = lgb.Dataset(X_train, label=y_train)
            val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
            
            model = lgb.train(
                self.params,
                train_data,
                num_boost_round=1000,
                valid_sets=[train_data, val_data],
                callbacks=[
                    lgb.early_stopping(stopping_rounds=50),
                    lgb.log_evaluation(period=100)
                ]
            )
            
            self.models.append(model)
        
        # 피처 중요도 집계
        self._aggregate_feature_importance()
        
        return self
    
    def predict(self, X):
        """예측 (모델 평균)"""
        predictions = np.zeros(len(X))
        
        for model in self.models:
            predictions += model.predict(X) / len(self.models)
        
        return predictions
    
    def _aggregate_feature_importance(self):
        """피처 중요도 집계"""
        importances = []
        for model in self.models:
            importances.append(model.feature_importance(importance_type='gain'))
        
        self.feature_importance = np.mean(importances, axis=0)
```

### 📊 실험 노트북

```python
# notebooks/04_baseline_model.ipynb

from src.models.lgbm_model import LGBMModel
from src.utils.metrics import euclidean_distance

# 1. 데이터 준비
X = train_features
y_x = train['end_x']
y_y = train['end_y']

# 2. X 좌표 모델
print("=== X 좌표 예측 모델 ===")
model_x = LGBMModel()
model_x.train(X, y_x, n_splits=5)

# 3. Y 좌표 모델
print("\n=== Y 좌표 예측 모델 ===")
model_y = LGBMModel()
model_y.train(X, y_y, n_splits=5)

# 4. 검증
pred_x = model_x.predict(X_val)
pred_y = model_y.predict(X_val)

score = euclidean_distance(
    y_val_x, y_val_y,
    pred_x, pred_y
)

print(f"\n검증 스코어: {score:.4f}")
```

---

## 5️⃣ 모델링 담당 2 (딥러닝)

### 🧠 주요 책임
- LSTM, Transformer 모델 구현
- 시퀀스 데이터 처리
- 앙상블 전략

### 🚀 작업 시작

```bash
git checkout develop
git pull origin develop
git checkout -b feature/model-lstm
```

### 📝 딥러닝 체크리스트

```python
## LSTM 모델
- [ ] 시퀀스 데이터 준비
- [ ] LSTM 아키텍처 설계
- [ ] 학습 파이프라인 구축

## Attention 메커니즘
- [ ] Self-Attention 추가
- [ ] 성능 비교

## 앙상블
- [ ] LightGBM + LSTM 앙상블
- [ ] 가중 평균 최적화
```

### 💻 LSTM 구현

```python
# src/models/lstm_model.py

"""
LSTM 시퀀스 모델
작성자: 팀원 E
"""

import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader

class PassDataset(Dataset):
    """패스 시퀀스 데이터셋"""
    
    def __init__(self, sequences, targets):
        self.sequences = torch.FloatTensor(sequences)
        self.targets = torch.FloatTensor(targets)
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        return self.sequences[idx], self.targets[idx]


class LSTMModel(nn.Module):
    """LSTM 회귀 모델"""
    
    def __init__(self, input_size, hidden_size=128, num_layers=2):
        super().__init__()
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 2)  # (end_x, end_y)
        )
    
    def forward(self, x):
        # LSTM
        lstm_out, _ = self.lstm(x)
        
        # 마지막 타임스텝 출력
        last_output = lstm_out[:, -1, :]
        
        # 완전연결층
        output = self.fc(last_output)
        
        return output


class LSTMTrainer:
    """LSTM 학습 파이프라인"""
    
    def __init__(self, model, device='cuda'):
        self.model = model.to(device)
        self.device = device
        self.optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
    
    def train_epoch(self, train_loader):
        """1 에폭 학습"""
        self.model.train()
        total_loss = 0
        
        for sequences, targets in train_loader:
            sequences = sequences.to(self.device)
            targets = targets.to(self.device)
            
            # Forward
            outputs = self.model(sequences)
            loss = self.criterion(outputs, targets)
            
            # Backward
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(train_loader)
    
    def validate(self, val_loader):
        """검증"""
        self.model.eval()
        total_loss = 0
        
        with torch.no_grad():
            for sequences, targets in val_loader:
                sequences = sequences.to(self.device)
                targets = targets.to(self.device)
                
                outputs = self.model(sequences)
                loss = self.criterion(outputs, targets)
                
                total_loss += loss.item()
        
        return total_loss / len(val_loader)
    
    def train(self, train_loader, val_loader, epochs=50):
        """전체 학습"""
        best_val_loss = float('inf')
        
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            val_loss = self.validate(val_loader)
            
            print(f"Epoch {epoch+1}/{epochs}")
            print(f"  Train Loss: {train_loss:.4f}")
            print(f"  Val Loss: {val_loss:.4f}")
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(self.model.state_dict(), 
                          'models/lstm_best.pth')
                print("  ✓ 모델 저장")
```

---

## 🔄 팀 간 협업 시나리오

### 시나리오 1: 피처 → 모델링

**팀원 C (피처):**
```bash
# 피처 완성
git add src/features/spatial.py
git commit -m "feat: 공간 피처 완료"
git push origin feature/feature-engineering

# PR 생성
# Reviewers: 팀원 A, D
```

**팀원 D (모델링):**
```bash
# PR 확인 후 Approve

# develop에 병합되면
git checkout develop
git pull origin develop

# 내 브랜치에 반영
git checkout feature/model-lgbm
git merge develop

# 새 피처로 실험
python notebooks/04_baseline_model.ipynb
```

### 시나리오 2: 버그 발견 시

**팀원 E:**
```markdown
GitHub Issue 생성:

Title: 🐛 [Bug] result_name 결측치 처리 오류
Labels: bug, priority: high
Assigned: 팀원 B

## 문제
전처리 후에도 result_name에 NaN이 남아있음

## 재현 방법
```python
from src.data.preprocessing import DataPreprocessor
preprocessor = DataPreprocessor()
df = preprocessor.fit_transform(train)
print(df['result_name'].isna().sum())  # 1523 (예상: 0)
```

## 기대 결과
모든 NaN이 'Unknown'으로 대체되어야 함
```

**팀원 B:**
```bash
# 버그 수정
git checkout -b fix/result-name-nan
# 코드 수정...
git add src/data/preprocessing.py
git commit -m "fix: result_name 결측치 처리 버그 수정"
git push origin fix/result-name-nan

# PR 생성 및 병합
```

---

## 📊 성과 측정

### 개인별 기여도 확인

```bash
# 커밋 수
git shortlog -sn --all

# 라인 수 (참고용)
git log --author="팀원A" --pretty=tformat: --numstat | \
  awk '{ add += $1; subs += $2; loc += $1 - $2 } END \
  { printf "추가: %s, 삭제: %s, 총: %s\n", add, subs, loc }'
```

### 팀 대시보드

```markdown
## 프로젝트 진행 현황

### 완료된 작업
- ✅ EDA (@팀원B)
- ✅ 전처리 파이프라인 (@팀원B)
- ✅ 공간 피처 (@팀원C)
- ✅ LightGBM 베이스라인 (@팀원D)

### 진행 중
- 🏃 LSTM 모델 (@팀원E) - 80%
- 🏃 앙상블 전략 (@팀원A) - 60%

### 계획 중
- 📝 하이퍼파라미터 튜닝 (@팀원D)
- 📝 최종 제출 준비 (@팀원A)

### 스코어 추이
- Week 1: 0.XXX (베이스라인)
- Week 2: 0.YYY (피처 추가)
- Week 3: 0.ZZZ (앙상블)
```

---

## 🎯 각 역할별 성공 지표

### 팀장/PM
- [ ] 모든 PR을 24시간 내 리뷰
- [ ] 주간 미팅 4회 진행
- [ ] 팀원 간 충돌 0건

### EDA/전처리
- [ ] EDA 문서화 완료
- [ ] 전처리 파이프라인 동작
- [ ] 결측치 0%

### 피처 엔지니어링
- [ ] 10개 이상 피처 생성
- [ ] 피처 중요도 상위 5개 기여
- [ ] 문서화 완료

### 모델링 1
- [ ] 베이스라인 구축
- [ ] CV 스코어 안정적
- [ ] 하이퍼파라미터 튜닝 완료

### 모델링 2
- [ ] LSTM 모델 동작
- [ ] 앙상블로 성능 향상
- [ ] 최종 제출 완료

---

**팀워크가 최고의 전략입니다!** 💪

각자의 역할에 충실하면서 서로 도우며 진행하세요!
