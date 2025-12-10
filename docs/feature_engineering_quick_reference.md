# Feature Engineering 핵심 요약 - 빠른 참조 가이드 ⚡

## 🎯 목표
K리그 경기에서 **"다음 패스는 어디로?"**를 예측하기 위해 필요한 핵심 Feature들

---

## 📊 Feature 우선순위 체크리스트

### ⭐⭐⭐ 1순위 - 반드시 포함 (Top 10)

```python
필수_피처 = {
    # 공간 특성
    'distance_to_goal': '골대까지 거리 (가장 중요!)',
    'angle_to_goal': '골대 각도',
    'zone_x': '경기장 X구역 (수비/중앙/공격)',
    'zone_y': '경기장 Y구역 (좌/중앙/우)',
    
    # 패스 특성
    'pass_distance': '패스 거리',
    'forward_progress': '전진성 (+ = 공격, - = 후방)',
    'pass_success_rate': '패스 성공률',
    
    # 시퀀스 특성
    'sequence_position': '시퀀스 내 위치 (0~1)',
    'actions_remaining': '종료까지 남은 액션',
    'pass_count': '패스 횟수'
}
```

**이 10개만으로도 베이스라인 모델은 충분합니다!**

---

### ⭐⭐ 2순위 - 성능 향상 (Top 20)

```python
중요_피처 = {
    # 상대 위치
    'distance_from_prev': '이전 액션과의 거리',
    'lateral_movement': '측면 이동',
    
    # 시간
    'time_gap': '액션 간 시간 간격',
    'elapsed_time': '에피소드 경과 시간',
    
    # 맥락
    'pressure_intensity': '상대 압박 강도',
    'possession_ratio': '볼 소유 액션 비율',
    'offensiveness': '공격성 지표',
    
    # 네트워크
    'max_pass_chain': '최대 패스 체인',
    'unique_players': '참여 선수 수',
    
    # 롤링 통계
    'avg_pass_dist_last_5': '최근 5개 평균 패스 거리',
    'avg_forward_last_5': '최근 5개 평균 전진성'
}
```

---

### ⭐ 3순위 - 정교화 (추가 개선)

```python
유용_피처 = {
    'spatial_coverage': '공간 활용도',
    'pass_speed': '패스 속도',
    'energy_cost': '에너지 소모',
    'movement_efficiency': '움직임 효율성',
    'avg_direction_change': '방향 변화'
}
```

---

## 🔥 Feature 카테고리별 핵심 코드

### 1️⃣ 공간 (5분이면 구현!)

```python
# 골대까지 거리 (최우선!)
df['distance_to_goal'] = np.sqrt(
    (105 - df['start_x'])**2 + (34 - df['start_y'])**2
)

# 구역 인코딩
df['zone_x'] = pd.cut(df['start_x'], bins=[0, 35, 70, 105], labels=[0,1,2])
df['zone_y'] = pd.cut(df['start_y'], bins=[0, 22.67, 45.33, 68], labels=[0,1,2])

# 패스 거리
df['pass_distance'] = np.sqrt(
    (df['end_x'] - df['start_x'])**2 + 
    (df['end_y'] - df['start_y'])**2
)
```

### 2️⃣ 시간 (3분!)

```python
# 그룹별 처리 필수
def add_temporal_features(group):
    group['time_gap'] = group['time_seconds'].diff().fillna(0)
    group['elapsed_time'] = group['time_seconds'] - group['time_seconds'].iloc[0]
    group['sequence_position'] = np.arange(len(group)) / max(len(group)-1, 1)
    return group

df = df.groupby('game_episode').apply(add_temporal_features)
```

### 3️⃣ 맥락 (7분!)

```python
def add_context_features(group):
    total = len(group)
    
    # 액션 카운트
    group['pass_count'] = (group['type_name'] == 'Pass').sum()
    group['pass_ratio'] = group['pass_count'] / total
    
    # 성공률
    pass_mask = group['type_name'] == 'Pass'
    if pass_mask.sum() > 0:
        success_rate = (group[pass_mask]['result_name'] == 'Successful').mean()
        group['pass_success_rate'] = success_rate
    else:
        group['pass_success_rate'] = 0
    
    # 압박 강도
    defensive = ['Interception', 'Tackle', 'Block']
    group['pressure_intensity'] = group['type_name'].isin(defensive).sum() / total
    
    return group

df = df.groupby('game_episode').apply(add_context_features)
```

### 4️⃣ 롤링 통계 (5분!)

```python
def add_rolling_features(group, window=5):
    # 최근 N개 평균
    group['avg_pass_dist_last_5'] = group['pass_distance'].rolling(
        window=window, min_periods=1
    ).mean()
    
    group['avg_forward_last_5'] = group['forward_progress'].rolling(
        window=window, min_periods=1
    ).mean()
    
    return group

df = df.groupby('game_episode').apply(add_rolling_features)
```

---

## ⚡ 빠른 시작 템플릿 (복사해서 사용!)

```python
import pandas as pd
import numpy as np

def create_essential_features(df):
    """
    20분이면 끝! 핵심 Feature만 빠르게 생성
    """
    # 1. 정렬 (필수!)
    df = df.sort_values(['game_episode', 'time_seconds']).reset_index(drop=True)
    
    # 2. 공간 특성
    df['distance_to_goal'] = np.sqrt((105-df['start_x'])**2 + (34-df['start_y'])**2)
    df['zone_x'] = pd.cut(df['start_x'], bins=[0,35,70,105], labels=[0,1,2]).astype(int)
    df['zone_y'] = pd.cut(df['start_y'], bins=[0,22.67,45.33,68], labels=[0,1,2]).astype(int)
    
    # 3. 그룹별 특성
    def group_features(g):
        total = len(g)
        
        # 패스 거리
        g['pass_distance'] = np.sqrt(
            (g['end_x']-g['start_x'])**2 + (g['end_y']-g['start_y'])**2
        )
        
        # 전진성
        g['forward_progress'] = g['end_x'] - g['start_x']
        
        # 시간
        g['time_gap'] = g['time_seconds'].diff().fillna(0)
        g['sequence_position'] = np.arange(total) / max(total-1, 1)
        
        # 통계
        g['pass_count'] = (g['type_name']=='Pass').sum()
        pass_mask = g['type_name']=='Pass'
        if pass_mask.sum() > 0:
            g['pass_success_rate'] = (g[pass_mask]['result_name']=='Successful').mean()
        else:
            g['pass_success_rate'] = 0
        
        return g
    
    df = df.groupby('game_episode', group_keys=False).apply(group_features)
    
    # 4. 결측치 처리
    df = df.fillna(0)
    
    return df

# 사용
train_features = create_essential_features(train_df)
```

---

## 🎓 Feature 선택 가이드

### 어떤 Feature를 선택할까?

```python
# 1. 간단한 상관관계 분석
import seaborn as sns

# 타겟과의 상관계수
correlations = train_features.corr()[['end_x', 'end_y']].abs()
top_features = correlations.sum(axis=1).sort_values(ascending=False).head(20)
print("타겟과 상관관계 높은 Feature:")
print(top_features)
```

```python
# 2. Feature Importance (모델 학습 후)
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor()
model.fit(X_train, y_train)

importance_df = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("중요도 Top 20:")
print(importance_df.head(20))
```

---

## 💡 실전 팁

### Tip 1: 처음부터 모든 Feature를 만들지 마세요!

```
1단계: 핵심 10개로 베이스라인 구축
   ↓
2단계: Feature Importance 확인
   ↓
3단계: 중요한 Feature 중심으로 파생 Feature 추가
   ↓
4단계: 성능 향상 확인 후 반복
```

### Tip 2: 그룹별 처리는 필수!

```python
# ❌ 잘못된 예
df['time_gap'] = df['time_seconds'].diff()  # 에피소드 경계 무시!

# ✅ 올바른 예
df = df.groupby('game_episode').apply(
    lambda g: g.assign(time_gap=g['time_seconds'].diff().fillna(0))
)
```

### Tip 3: Data Leakage 주의!

```python
# ❌ 미래 정보 사용
df['avg_future_x'] = df.groupby('game_episode')['end_x'].transform('mean')

# ✅ 과거 정보만 사용
df['avg_past_x'] = df.groupby('game_episode')['end_x'].expanding().mean()
```

---

## 📈 성능 기대치

```
Feature 수 → 성능 (유클리드 거리)

기본 (원본 그대로):     ~10.0m
필수 10개:              ~7.0m  (30% 개선)
중요 20개 추가:         ~5.0m  (50% 개선)
롤링 + 고급:            ~4.0m  (60% 개선)
앙상블 + 튜닝:          ~3.0m  (70% 개선)
```

---

## 🚀 다음 단계

1. **이 템플릿으로 빠르게 베이스라인 구축**
2. **Feature Importance로 중요 Feature 파악**
3. **중요한 Feature 중심으로 확장**
4. **모델 앙상블로 최종 성능 향상**

---

## 📚 참고 파일

- `feature_engineering_guide.md` - 상세한 설명과 이론
- `feature_engineering_implementation.py` - 전체 구현 코드
- `result_name_imputation_guide.md` - 결측치 처리 전략

---

**"좋은 Feature는 모델의 90%를 결정합니다!"** 🎯

시작은 간단하게, 개선은 점진적으로! 
