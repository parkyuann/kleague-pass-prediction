import sys
from pathlib import Path

# 프로젝트 루트 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from src.features.sequence_features import (
    analyze_episode_structure,
    analyze_action_sequence,
    create_all_sequence_features
)

print("="*70)
print("시퀀스 Feature 적용")
print("="*70)

# 1. 방법 A 데이터 로드
print("\n[방법 A 처리]")
train_a = pd.read_csv(project_root / 'data/processed/train_method_a_featured.csv')
print(f"로드: {train_a.shape}")

# 2. 에피소드 구조 분석
episode_stats = analyze_episode_structure(train_a)

# 3. 액션 시퀀스 분석
train_a_seq = analyze_action_sequence(train_a)

# 4. 시퀀스 Feature 생성
train_a_final = create_all_sequence_features(train_a)

# 5. 저장
output_path = project_root / 'data/processed/train_method_a_with_sequence.csv'
train_a_final.to_csv(output_path, index=False)
print(f"\n✓ 저장: {output_path}")

print("\n" + "="*70)

# 6. 방법 B도 동일하게
print("\n[방법 B 처리]")
train_b = pd.read_csv(project_root / 'data/processed/train_method_b_featured.csv')
train_b_final = create_all_sequence_features(train_b)
output_path_b = project_root / 'data/processed/train_method_b_with_sequence.csv'
train_b_final.to_csv(output_path_b, index=False)
print(f"✓ 저장: {output_path_b}")

print("\n" + "="*70)
print("✅ 시퀀스 Feature 적용 완료!")
print("="*70)