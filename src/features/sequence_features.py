import pandas as pd
import numpy as np

def analyze_episode_structure(df):
    """
    에피소드의 기본 구조 분석
    
    확인 사항:
    1. 에피소드당 평균 액션 수
    2. 에피소드 내 Pass 비율
    3. 에피소드 길이 분포
    """
    print("="*70)
    print("에피소드 구조 분석")
    print("="*70)
    
    # 1. 에피소드별 통계
    episode_stats = df.groupby('game_episode').agg({
        'action_id': 'count',  # 액션 수
        'time_seconds': ['min', 'max'],  # 시간 범위
        'type_name': lambda x: (x == 'Pass').sum()  # Pass 개수
    }).reset_index()
    
    episode_stats.columns = ['game_episode', 'total_actions', 
                             'start_time', 'end_time', 'pass_count']
    
    # 에피소드 지속 시간
    episode_stats['duration'] = episode_stats['end_time'] - episode_stats['start_time']
    
    # Pass 비율
    episode_stats['pass_ratio'] = episode_stats['pass_count'] / episode_stats['total_actions']
    
    print(f"\n📊 에피소드 통계:")
    print(f"  총 에피소드 수: {len(episode_stats):,}개")
    print(f"\n  액션 수:")
    print(f"    평균: {episode_stats['total_actions'].mean():.1f}개")
    print(f"    중앙값: {episode_stats['total_actions'].median():.0f}개")
    print(f"    최소: {episode_stats['total_actions'].min()}개")
    print(f"    최대: {episode_stats['total_actions'].max()}개")
    
    print(f"\n  지속 시간:")
    print(f"    평균: {episode_stats['duration'].mean():.1f}초")
    print(f"    중앙값: {episode_stats['duration'].median():.1f}초")
    
    print(f"\n  Pass 비율:")
    print(f"    평균: {episode_stats['pass_ratio'].mean():.1%}")
    print(f"    중앙값: {episode_stats['pass_ratio'].median():.1%}")
    
    # 2. 에피소드 길이별 분포
    print(f"\n📏 에피소드 길이 분포:")
    length_bins = [0, 5, 10, 20, 50, 100, 1000]
    length_labels = ['1-5', '6-10', '11-20', '21-50', '51-100', '100+']
    episode_stats['length_range'] = pd.cut(
        episode_stats['total_actions'], 
        bins=length_bins, 
        labels=length_labels
    )
    
    print(episode_stats['length_range'].value_counts().sort_index())
    
    return episode_stats


def analyze_action_sequence(df):
    """
    에피소드 내 액션 시퀀스 패턴 분석
    
    예: Pass → Pass → Pass (연속 패스)
         Pass → Carry → Pass (드리블 포함)
    """
    print("\n" + "="*70)
    print("액션 시퀀스 패턴 분석")
    print("="*70)
    
    # 다음 액션 타입 추가
    df_seq = df.copy()
    df_seq['next_type'] = df_seq.groupby('game_episode')['type_name'].shift(-1)
    
    # Pass 이후 나오는 액션
    print(f"\n🔄 Pass 다음에 오는 액션:")
    pass_next = df_seq[df_seq['type_name'] == 'Pass']['next_type'].value_counts()
    print(pass_next.head(10))
    
    # 2-gram 패턴 (연속된 2개 액션)
    print(f"\n📊 가장 흔한 2-gram 패턴 (상위 10개):")
    df_seq['action_pair'] = df_seq['type_name'] + ' → ' + df_seq['next_type'].fillna('END')
    print(df_seq['action_pair'].value_counts().head(10))
    
    return df_seq

def create_temporal_features(df):
    """
    시간 흐름 기반 Feature
    
    비유:
    - 축구는 리듬의 게임
    - 빠른 연속 패스 = 빠른 템포 (역습)
    - 느린 패스 = 느린 템포 (점유율 플레이)
    """
    print("\n" + "="*70)
    print("시간 기반 Feature 생성")
    print("="*70)
    
    df_temp = df.copy()
    
    # 1. 이전 액션과의 시간 차이
    df_temp['time_since_prev'] = df_temp.groupby('game_episode')['time_seconds'].diff()
    df_temp['time_since_prev'] = df_temp['time_since_prev'].fillna(0)
    
    print(f"✓ time_since_prev: 이전 액션과의 시간 차이")
    print(f"  평균: {df_temp['time_since_prev'].mean():.2f}초")
    
    # 2. 다음 액션까지의 시간 (예측 시 사용 불가, 분석용)
    df_temp['time_to_next'] = -df_temp.groupby('game_episode')['time_seconds'].diff(-1)
    df_temp['time_to_next'] = df_temp['time_to_next'].fillna(0)
    
    # 3. 에피소드 시작부터 경과 시간
    df_temp['time_from_start'] = df_temp.groupby('game_episode')['time_seconds'].transform(
        lambda x: x - x.min()
    )
    
    print(f"✓ time_from_start: 에피소드 시작부터 경과 시간")
    
    # 4. 에피소드 내 상대적 시간 (0~1)
    df_temp['episode_time_ratio'] = df_temp.groupby('game_episode')['time_seconds'].transform(
        lambda x: (x - x.min()) / (x.max() - x.min() + 1e-8)
    )
    
    print(f"✓ episode_time_ratio: 에피소드 진행도 (0~1)")
    
    # 5. 롤링 템포 (최근 3개 액션의 평균 시간 간격)
    df_temp['tempo_rolling_3'] = df_temp.groupby('game_episode')['time_since_prev'].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )
    
    print(f"✓ tempo_rolling_3: 최근 템포")
    print(f"  빠른 템포 (< 2초): {(df_temp['tempo_rolling_3'] < 2).sum():,}개")
    print(f"  느린 템포 (> 5초): {(df_temp['tempo_rolling_3'] > 5).sum():,}개")
    
    return df_temp

def create_previous_action_features(df):
    """
    이전 액션들의 정보를 현재 액션에 추가
    
    비유:
    - 축구는 연결의 게임
    - 이전에 뭘 했는지가 다음 선택에 영향
    - 예: 이전에 긴 패스 → 다음은 짧은 패스 조정
    """
    print("\n" + "="*70)
    print("이전 액션 Context Feature 생성")
    print("="*70)
    
    df_prev = df.copy()
    
    # 1. 이전 액션 타입
    df_prev['prev_type_1'] = df_prev.groupby('game_episode')['type_name'].shift(1)
    df_prev['prev_type_2'] = df_prev.groupby('game_episode')['type_name'].shift(2)
    df_prev['prev_type_3'] = df_prev.groupby('game_episode')['type_name'].shift(3)
    
    print(f"✓ prev_type_1/2/3: 이전 1/2/3번째 액션 타입")
    
    # 2. 이전 패스 거리 (distance가 있을 경우)
    if 'distance' in df_prev.columns:
        df_prev['prev_distance_1'] = df_prev.groupby('game_episode')['distance'].shift(1)
        df_prev['prev_distance_2'] = df_prev.groupby('game_episode')['distance'].shift(2)
        
        # 이전 2개 패스의 평균 거리
        df_prev['avg_prev_2_distance'] = (
            df_prev['prev_distance_1'] + df_prev['prev_distance_2']
        ) / 2
        
        print(f"✓ prev_distance: 이전 패스 거리")
    
    # 3. 이전 위치
    df_prev['prev_start_x'] = df_prev.groupby('game_episode')['start_x'].shift(1)
    df_prev['prev_start_y'] = df_prev.groupby('game_episode')['start_y'].shift(1)
    
    # 이전 위치에서 현재 위치까지 이동 거리
    df_prev['movement_from_prev'] = np.sqrt(
        (df_prev['start_x'] - df_prev['prev_start_x'])**2 +
        (df_prev['start_y'] - df_prev['prev_start_y'])**2
    )
    
    print(f"✓ movement_from_prev: 이전 위치에서 이동 거리")
    print(f"  평균: {df_prev['movement_from_prev'].mean():.2f}m")
    
    # 4. 연속 Pass 카운트
    df_prev['is_pass'] = (df_prev['type_name'] == 'Pass').astype(int)
    
    consecutive_passes = []
    for episode in df_prev['game_episode'].unique():
        episode_mask = df_prev['game_episode'] == episode
        episode_passes = df_prev.loc[episode_mask, 'is_pass'].values
        
        count = 0
        counts = []
        for is_pass in episode_passes:
            if is_pass:
                count += 1
            else:
                count = 0
            counts.append(count)
        
        consecutive_passes.extend(counts)
    
    df_prev['consecutive_passes'] = consecutive_passes
    
    print(f"✓ consecutive_passes: 연속 패스 수")
    print(f"  최대 연속: {df_prev['consecutive_passes'].max()}개")
    
    return df_prev

def create_cumulative_features(df):
    """
    에피소드 내 누적 통계
    
    비유:
    - "지금까지 이 에피소드에서 얼마나 많이 패스했나?"
    - "전진하고 있나, 횡패스만 하고 있나?"
    """
    print("\n" + "="*70)
    print("누적 통계 Feature 생성")
    print("="*70)
    
    df_cum = df.copy()
    
    # 1. 에피소드 내 액션 순서
    df_cum['action_order'] = df_cum.groupby('game_episode').cumcount() + 1
    
    print(f"✓ action_order: 에피소드 내 순서")
    
    # 2. 지금까지 Pass 개수
    df_cum['cumsum_passes'] = df_cum.groupby('game_episode')['is_pass'].cumsum()
    
    print(f"✓ cumsum_passes: 누적 Pass 수")
    
    # 3. 지금까지 전진한 거리 (X축 진행)
    if 'delta_x' in df_cum.columns:
        df_cum['cumsum_forward'] = df_cum.groupby('game_episode')['delta_x'].cumsum()
        
        print(f"✓ cumsum_forward: 누적 전진 거리")
        print(f"  평균: {df_cum['cumsum_forward'].mean():.2f}m")
    
    # 4. 평균 X 위치 (에피소드 내)
    df_cum['avg_x_so_far'] = df_cum.groupby('game_episode')['start_x'].transform(
        lambda x: x.expanding().mean()
    )
    
    print(f"✓ avg_x_so_far: 에피소드 평균 X 위치")
    
    # 5. 필드 진행 속도
    df_cum['field_progress_rate'] = df_cum['cumsum_forward'] / df_cum['action_order']
    
    print(f"✓ field_progress_rate: 액션당 평균 전진 거리")
    
    return df_cum

def create_all_sequence_features(df):
    """
    모든 시퀀스 Feature를 한번에 생성
    """
    print("\n" + "="*70)
    print("시퀀스 Feature 생성 시작")
    print("="*70)
    
    # 순차 적용
    print("\n[1/4] 시간 기반 Feature...")
    df = create_temporal_features(df)
    
    print("\n[2/4] 이전 액션 Feature...")
    df = create_previous_action_features(df)
    
    print("\n[3/4] 누적 통계 Feature...")
    df = create_cumulative_features(df)
    
    print("\n" + "="*70)
    print("✅ 시퀀스 Feature 생성 완료!")
    print("="*70)
    
    # 추가된 Feature 목록
    new_features = [
        'time_since_prev', 'time_to_next', 'time_from_start', 
        'episode_time_ratio', 'tempo_rolling_3',
        'prev_type_1', 'prev_type_2', 'prev_type_3',
        'prev_distance_1', 'prev_distance_2', 'avg_prev_2_distance',
        'prev_start_x', 'prev_start_y', 'movement_from_prev',
        'consecutive_passes',
        'action_order', 'cumsum_passes', 'cumsum_forward',
        'avg_x_so_far', 'field_progress_rate'
    ]
    
    print(f"\n📊 생성된 시퀀스 Feature ({len(new_features)}개):")
    for i, feat in enumerate(new_features, 1):
        if feat in df.columns:
            print(f"  {i}. {feat}")
    
    print(f"\n💾 최종 데이터 크기: {df.shape}")
    
    return df