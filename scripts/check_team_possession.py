import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np

print("="*70)
print("팀별 소유 분석")
print("="*70)

# 데이터 로드
df = pd.read_csv(project_root / 'data/processed/train_method_a_with_sequence.csv')

# 하나의 에피소드 예시 분석
sample_episode = df['game_episode'].iloc[0]
episode_data = df[df['game_episode'] == sample_episode].copy()

print(f"\n📊 에피소드 예시: {sample_episode}")
print(f"총 액션: {len(episode_data)}개")

# 팀별 액션 수
print(f"\n팀별 액션 수:")
team_counts = episode_data['team_id'].value_counts()
print(team_counts)

# 연속된 액션 패턴 확인
print(f"\n🔄 액션 시퀀스 (처음 20개):")
print(episode_data[['action_order', 'team_id', 'type_name', 'delta_x', 'cumsum_forward']].head(20))

# 팀이 바뀐 횟수
team_changes = (episode_data['team_id'] != episode_data['team_id'].shift()).sum() - 1
print(f"\n🔀 팀 소유 전환 횟수: {team_changes}번")

# 전체 통계
print(f"\n" + "="*70)
print("전체 데이터 팀 소유 분석")
print("="*70)

# 에피소드별 팀 전환 횟수
episode_changes = []
for episode in df['game_episode'].unique():
    ep_data = df[df['game_episode'] == episode]
    changes = (ep_data['team_id'] != ep_data['team_id'].shift()).sum() - 1
    episode_changes.append(changes)

print(f"에피소드당 평균 팀 전환: {np.mean(episode_changes):.1f}번")
print(f"최소 팀 전환: {np.min(episode_changes)}번")
print(f"최대 팀 전환: {np.max(episode_changes)}번")

# 연속 소유 길이 분석
consecutive_lengths = []
for episode in df['game_episode'].unique()[:1000]:  # 샘플 1000개
    ep_data = df[df['game_episode'] == episode]
    teams = ep_data['team_id'].values
    
    current_team = teams[0]
    length = 1
    
    for team in teams[1:]:
        if team == current_team:
            length += 1
        else:
            consecutive_lengths.append(length)
            current_team = team
            length = 1
    consecutive_lengths.append(length)

print(f"\n🎯 연속 소유 통계:")
print(f"평균 연속 액션: {np.mean(consecutive_lengths):.1f}개")
print(f"중앙값: {np.median(consecutive_lengths):.0f}개")
print(f"최대: {np.max(consecutive_lengths)}개")

print("\n" + "="*70)
print("✅ 분석 완료!")
print("="*70)