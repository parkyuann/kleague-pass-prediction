# 축구 패스 좌표 예측을 위한 Feature Engineering 완벽 가이드 ⚽

## 📌 핵심 철학: "축구는 공간과 시간의 게임이다"

축구를 비유하자면:
- **체스**: 각 기물(선수)의 위치와 움직임이 중요
- **음악**: 리듬(시간)과 하모니(공간 조화)가 결합
- **전쟁**: 공격/수비의 밸런스와 전술적 판단

---

## 🎯 Feature Engineering 전략 맵

```
Raw Data → [공간 특성] → [시간 특성] → [맥락 특성] → [고급 특성] → Model
              ↓             ↓             ↓             ↓
          "어디서?"      "언제?"       "무엇을?"      "왜?"
```

---

## 1️⃣ 공간 특성 (Spatial Features) - "어디서?"

### 1.1 절대 위치 기반

```python
# 비유: 체스판에서 각 칸이 가진 전략적 가치

def create_position_features(df):
    """
    경기장을 구역으로 나누어 전술적 의미 부여
    """
    # 1. 수직 구역 (공격 방향)
    # 105m 경기장을 3등분: 수비진영(0-35), 중앙(35-70), 공격진영(70-105)
    df['zone_x'] = pd.cut(df['start_x'], 
                          bins=[0, 35, 70, 105], 
                          labels=['defensive', 'middle', 'offensive'])
    
    # 2. 수평 구역 (좌우 측면)
    # 68m 경기장을 3등분: 좌측, 중앙, 우측
    df['zone_y'] = pd.cut(df['start_y'], 
                          bins=[0, 22.67, 45.33, 68], 
                          labels=['left', 'center', 'right'])
    
    # 3. 골대까지 거리 (핵심!)
    # 상대 골대 위치 (105, 34) 기준
    df['distance_to_goal'] = np.sqrt(
        (105 - df['start_x'])**2 + (34 - df['start_y'])**2
    )
    
    # 4. 골대 각도 (중요!)
    # 골대를 향한 각도가 좁을수록 슈팅이 어려움
    df['angle_to_goal'] = np.arctan2(
        abs(df['start_y'] - 34),  # 골대 중앙(y=34)으로부터의 거리
        105 - df['start_x']        # 골라인까지의 거리
    ) * 180 / np.pi
    
    # 5. 중앙선으로부터의 거리
    df['distance_from_center'] = abs(df['start_y'] - 34)
    
    # 6. 터치라인까지의 거리 (최소값)
    df['distance_to_sideline'] = df['start_y'].apply(
        lambda y: min(y, 68 - y)
    )
    
    return df

# 왜 중요한가?
# → 골대 근처에서의 패스는 "득점 기회"를 만들려는 의도
# → 측면에서의 패스는 "크로스" 또는 "돌파" 전술
# → 중앙에서의 패스는 "빌드업" 또는 "템포 조절"
```

### 1.2 상대 위치 기반 (Relative Position)

```python
def create_relative_features(group):
    """
    에피소드 내에서 이전 액션과의 관계
    """
    # 1. 이동 거리 (Pass의 경우)
    group['pass_distance'] = np.sqrt(
        (group['end_x'] - group['start_x'])**2 + 
        (group['end_y'] - group['start_y'])**2
    )
    
    # 2. 이동 방향 (각도)
    group['pass_angle'] = np.arctan2(
        group['end_y'] - group['start_y'],
        group['end_x'] - group['start_x']
    ) * 180 / np.pi
    
    # 3. 전진성 (Forward Progress)
    # 양수: 상대 골대에 가까워짐, 음수: 후방 패스
    group['forward_progress'] = group['end_x'] - group['start_x']
    
    # 4. 측면 이동 (Lateral Movement)
    group['lateral_movement'] = abs(group['end_y'] - group['start_y'])
    
    # 5. 이전 액션과의 거리
    group['distance_from_prev'] = np.sqrt(
        (group['start_x'] - group['end_x'].shift(1))**2 + 
        (group['start_y'] - group['end_y'].shift(1))**2
    ).fillna(0)
    
    return group

# 왜 중요한가?
# → 전진 패스 vs 후방 패스는 전혀 다른 의도
# → 짧은 패스 체인 vs 롱패스는 다른 전술
```

---

## 2️⃣ 시간 특성 (Temporal Features) - "언제?"

### 2.1 시간 흐름

```python
def create_temporal_features(group):
    """
    시간의 흐름에 따른 경기 맥락
    """
    # 1. 시간 간격 (액션 사이의 시간)
    group['time_gap'] = group['time_seconds'].diff().fillna(0)
    
    # 2. 누적 시간 (에피소드 시작부터)
    group['elapsed_time'] = group['time_seconds'] - group['time_seconds'].iloc[0]
    
    # 3. 시간 가속도 (플레이 속도 변화)
    group['time_acceleration'] = group['time_gap'].diff().fillna(0)
    
    # 4. 액션 밀도 (단위 시간당 액션 수)
    window_size = 5  # 최근 5초
    group['action_density'] = group['time_seconds'].rolling(
        window=5, min_periods=1
    ).count() / window_size
    
    # 5. 경기 페이즈 (초반/중반/후반)
    # 실제 경기 시간에서 추출 (period_id 활용)
    total_time = group['time_seconds'].max()
    group['game_phase'] = pd.cut(
        group['time_seconds'], 
        bins=[0, total_time*0.33, total_time*0.67, total_time],
        labels=['early', 'middle', 'late']
    )
    
    return group

# 왜 중요한가?
# → 빠른 템포의 공격 vs 느린 빌드업은 다른 패스 패턴
# → 경기 막판의 역전 시도는 더 공격적인 패스
```

### 2.2 시퀀스 위치

```python
def create_sequence_features(group):
    """
    시퀀스 내에서의 위치 정보
    """
    total_actions = len(group)
    
    # 1. 시퀀스 내 위치 (정규화)
    group['sequence_position'] = np.arange(total_actions) / total_actions
    
    # 2. 시퀀스 종료까지 남은 액션 수
    group['actions_remaining'] = total_actions - np.arange(total_actions)
    
    # 3. 패스 순서 (패스만 카운트)
    group['pass_order'] = (group['type_name'] == 'Pass').cumsum()
    
    # 4. 마지막 패스로부터의 거리
    last_pass_idx = group[group['type_name'] == 'Pass'].index[-1] if any(group['type_name'] == 'Pass') else 0
    group['steps_from_last_pass'] = group.index - last_pass_idx
    
    return group

# 왜 중요한가?
# → 시퀀스 초반은 "빌드업", 후반은 "마무리"
# → 마지막 패스는 예측 타겟이므로 그 전 패스들의 패턴이 중요
```

---

## 3️⃣ 맥락 특성 (Contextual Features) - "무엇을?"

### 3.1 액션 타입 통계

```python
def create_action_statistics(group):
    """
    에피소드 내 액션 패턴 분석
    """
    # 1. 액션 타입별 카운트
    action_counts = group.groupby('type_name').size().to_dict()
    group['pass_count'] = action_counts.get('Pass', 0)
    group['carry_count'] = action_counts.get('Carry', 0)
    group['duel_count'] = action_counts.get('Duel', 0)
    group['interception_count'] = action_counts.get('Interception', 0)
    
    # 2. 액션 타입 비율
    total = len(group)
    group['pass_ratio'] = group['pass_count'] / total
    group['possession_actions'] = (group['pass_count'] + group['carry_count']) / total
    
    # 3. 패스 성공률 (현재까지)
    pass_data = group[group['type_name'] == 'Pass']
    if len(pass_data) > 0:
        success_rate = (pass_data['result_name'] == 'Successful').sum() / len(pass_data)
        group['pass_success_rate'] = success_rate
    else:
        group['pass_success_rate'] = 0
    
    # 4. 압박 강도 (상대의 수비 액션)
    defensive_actions = ['Interception', 'Tackle', 'Block', 'Clearance']
    group['pressure_intensity'] = group['type_name'].isin(defensive_actions).sum() / total
    
    # 5. 공격성 지표
    offensive_actions = ['Shot', 'Cross', 'Pass']
    group['offensiveness'] = group['type_name'].isin(offensive_actions).sum() / total
    
    return group

# 왜 중요한가?
# → 패스 위주 vs 드리블 위주는 다른 공격 스타일
# → 상대 압박이 강하면 안전한 패스 선택
# → 공격적인 에피소드는 골대 근처로 패스
```

### 3.2 팀 & 선수 특성

```python
def create_team_player_features(group):
    """
    팀과 선수의 특성
    """
    # 1. 홈/원정 팀
    group['is_attacking_team'] = group['is_home'].mode()[0] if len(group) > 0 else True
    
    # 2. 고유 선수 수 (볼 소유 선수의 다양성)
    group['unique_players'] = group['player_id'].nunique()
    
    # 3. 선수 변경 빈도 (패스 네트워크의 복잡도)
    group['player_changes'] = (group['player_id'] != group['player_id'].shift(1)).sum()
    
    # 4. 팀 변경 여부 (볼 소유권 전환)
    group['possession_changes'] = (group['team_id'] != group['team_id'].shift(1)).sum()
    
    return group

# 왜 중요한가?
# → 여러 선수가 터치하면 "조직적인 공격"
# → 한 선수가 계속 소유하면 "개인기 위주"
```

---

## 4️⃣ 고급 특성 (Advanced Features) - "왜?"

### 4.1 롤링 윈도우 통계

```python
def create_rolling_features(group, windows=[3, 5, 7]):
    """
    최근 N개 액션의 트렌드 파악
    """
    for w in windows:
        # 1. 최근 N개 액션의 평균 이동 거리
        group[f'avg_distance_last_{w}'] = group['pass_distance'].rolling(
            window=w, min_periods=1
        ).mean()
        
        # 2. 최근 N개 액션의 평균 전진성
        group[f'avg_forward_last_{w}'] = group['forward_progress'].rolling(
            window=w, min_periods=1
        ).mean()
        
        # 3. 최근 N개 액션의 X좌표 변동성 (공간 활용도)
        group[f'std_x_last_{w}'] = group['start_x'].rolling(
            window=w, min_periods=1
        ).std().fillna(0)
        
        # 4. 최근 N개 액션의 Y좌표 변동성
        group[f'std_y_last_{w}'] = group['start_y'].rolling(
            window=w, min_periods=1
        ).std().fillna(0)
        
        # 5. 최근 N개 액션의 성공률
        group[f'success_rate_last_{w}'] = (
            group['result_name'] == 'Successful'
        ).rolling(window=w, min_periods=1).mean()
    
    return group

# 왜 중요한가?
# → 트렌드 파악: "공격이 가속화되고 있다"
# → 패턴 인식: "계속 전진하다가 갑자기 측면으로"
```

### 4.2 패스 네트워크 특성

```python
def create_network_features(group):
    """
    패스 네트워크 구조 분석
    """
    # 1. 패스 체인 길이
    pass_chain = 0
    max_chain = 0
    for action in group['type_name']:
        if action == 'Pass':
            pass_chain += 1
            max_chain = max(max_chain, pass_chain)
        else:
            pass_chain = 0
    group['max_pass_chain'] = max_chain
    
    # 2. 패스 방향 변화
    pass_angles = group[group['type_name'] == 'Pass']['pass_angle']
    if len(pass_angles) > 1:
        angle_changes = pass_angles.diff().abs()
        group['avg_direction_change'] = angle_changes.mean()
    else:
        group['avg_direction_change'] = 0
    
    # 3. 공간 커버리지 (경기장 활용도)
    x_range = group['start_x'].max() - group['start_x'].min()
    y_range = group['start_y'].max() - group['start_y'].min()
    group['spatial_coverage'] = x_range * y_range
    
    return group

# 왜 중요한가?
# → 긴 패스 체인 = 조직적인 공격
# → 방향 변화가 많으면 = 돌파 시도
# → 넓은 공간 커버 = 측면 활용 전술
```

### 4.3 물리적 제약 기반 특성

```python
def create_physics_features(group):
    """
    축구의 물리적 제약 반영
    """
    # 1. 속도 (거리 / 시간)
    distance = group['pass_distance']
    time_gap = group['time_gap'].replace(0, 0.1)  # 0 방지
    group['pass_speed'] = distance / time_gap
    
    # 2. 가속도 (속도 변화)
    group['acceleration'] = group['pass_speed'].diff().fillna(0)
    
    # 3. 실현 가능성 (물리적으로 가능한 패스인가?)
    # 예: 60m를 1초에 패스하는 것은 비현실적
    group['is_realistic'] = (group['pass_speed'] < 30).astype(int)  # 30m/s 이하
    
    # 4. 에너지 소모 추정
    # 거리가 길고 빠른 패스일수록 에너지 소모 큼
    group['energy_cost'] = group['pass_distance'] * group['pass_speed']
    
    return group

# 왜 중요한가?
# → 비현실적인 패스는 오류 가능성
# → 속도 변화는 전술 변화의 신호
```

---

## 5️⃣ 타겟 엔지니어링 (Target Feature)

### 최종 패스 좌표 예측을 위한 힌트 생성

```python
def create_target_hints(group):
    """
    타겟(최종 패스)과 관련된 힌트 생성
    """
    # 1. 현재까지의 평균 도착 지점
    group['avg_end_x_so_far'] = group['end_x'].expanding().mean()
    group['avg_end_y_so_far'] = group['end_y'].expanding().mean()
    
    # 2. 공격 방향 벡터 (전체 에피소드의 방향성)
    start_x, start_y = group['start_x'].iloc[0], group['start_y'].iloc[0]
    end_x, end_y = group['end_x'].iloc[-1], group['end_y'].iloc[-1]
    group['attack_direction_x'] = end_x - start_x
    group['attack_direction_y'] = end_y - start_y
    
    # 3. 목표 지점까지의 예상 거리
    # (현재 위치에서 목표까지 남은 거리)
    group['expected_remaining_distance'] = np.sqrt(
        (105 - group['start_x'])**2 + (34 - group['start_y'])**2
    )
    
    return group
```

---

## 📊 Feature 우선순위 (중요도 순)

### ⭐⭐⭐ 필수 (Must Have)
```python
1. distance_to_goal          # 골대까지 거리
2. pass_distance             # 패스 거리
3. forward_progress          # 전진성
4. zone_x, zone_y            # 경기장 구역
5. pass_count, pass_ratio    # 패스 통계
6. time_gap, elapsed_time    # 시간 정보
7. sequence_position         # 시퀀스 위치
```

### ⭐⭐ 중요 (Should Have)
```python
8. angle_to_goal             # 골대 각도
9. distance_from_prev        # 이전 액션과의 거리
10. pass_success_rate        # 성공률
11. pressure_intensity       # 압박 강도
12. max_pass_chain          # 패스 체인
13. avg_distance_last_5     # 최근 트렌드
```

### ⭐ 유용 (Nice to Have)
```python
14. spatial_coverage         # 공간 활용
15. unique_players          # 선수 다양성
16. pass_speed              # 패스 속도
17. action_density          # 액션 밀도
```

---

## 🔧 실전 구현 예제

```python
def full_feature_engineering(df):
    """
    전체 Feature Engineering 파이프라인
    """
    # 1. 기본 전처리
    df = df.sort_values(['game_episode', 'time_seconds']).reset_index(drop=True)
    
    # 2. 그룹별 처리
    feature_df = df.groupby('game_episode', group_keys=False).apply(
        lambda group: (
            create_position_features(group)
            .pipe(create_relative_features)
            .pipe(create_temporal_features)
            .pipe(create_sequence_features)
            .pipe(create_action_statistics)
            .pipe(create_team_player_features)
            .pipe(create_rolling_features, windows=[3, 5])
            .pipe(create_network_features)
            .pipe(create_physics_features)
        )
    )
    
    return feature_df

# 사용법
train_features = full_feature_engineering(train_df)
```

---

## ⚠️ 주의사항

### 1. Data Leakage 방지
```python
# ❌ 잘못된 예: 미래 정보 사용
df['target_x'] = df.groupby('game_episode')['end_x'].transform('last')

# ✅ 올바른 예: 과거 정보만 사용
df['prev_end_x'] = df.groupby('game_episode')['end_x'].shift(1)
```

### 2. 결측치 처리
```python
# result_name 결측치는 'NotApplicable'로 채우기
df['result_name'] = df['result_name'].fillna('NotApplicable')

# 또는 type_name 기반으로 채우기
def fill_result_name(row):
    if pd.isna(row['result_name']):
        if row['type_name'] in ['Carry', 'Recovery', 'Interception']:
            return 'NotApplicable'
        elif row['type_name'] == 'Pass':
            return 'Successful'  # 또는 ML 모델로 예측
    return row['result_name']

df['result_name'] = df.apply(fill_result_name, axis=1)
```

### 3. 스케일링
```python
from sklearn.preprocessing import StandardScaler, RobustScaler

# 거리/좌표 피처는 스케일링 필수
scaler = RobustScaler()  # 이상치에 강건
features_to_scale = ['distance_to_goal', 'pass_distance', 'forward_progress']
df[features_to_scale] = scaler.fit_transform(df[features_to_scale])
```

---

## 💡 핵심 인사이트

### "좋은 Feature란?"
1. **해석 가능**: "이 Feature가 왜 중요한지" 설명 가능
2. **도메인 지식**: 축구를 아는 사람이 "맞아, 이게 중요해!"라고 동의
3. **변별력**: 타겟과 강한 상관관계
4. **안정성**: 다른 에피소드에서도 일관성 유지

### 실험 프로세스
```
1. 기본 Feature로 베이스라인 구축
   ↓
2. Feature 중요도 분석 (SHAP, Feature Importance)
   ↓
3. 중요한 Feature 중심으로 파생 Feature 추가
   ↓
4. 성능 향상 확인 후 반복
```

---

## 📈 Feature 효과 측정

```python
from sklearn.ensemble import RandomForestRegressor
import shap

# 1. Feature Importance
model = RandomForestRegressor()
model.fit(X_train, y_train)
importances = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

# 2. SHAP 분석
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train)
shap.summary_plot(shap_values, X_train)
```

---

**Feature Engineering은 "데이터와의 대화"입니다!** 
계속 실험하고 검증하면서 최적의 조합을 찾으세요! 🚀
