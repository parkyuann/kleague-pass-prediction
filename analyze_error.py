import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches
from matplotlib.patches import Arc
import warnings

warnings.filterwarnings('ignore')
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
try:
    train = pd.read_csv('train.csv')
    oof = pd.read_csv('oof_v11_classifier_regressor.csv')
except:
    print("파일 경로를 확인해주세요.")

# 데이터 전처리
last_events_df = train.sort_values('action_id').groupby('game_episode').last().reset_index()
df = last_events_df[['game_episode', 'start_x', 'start_y', 'end_x', 'end_y']].copy()
df['target_dx'] = df['end_x'] - df['start_x']
df['target_dy'] = df['end_y'] - df['start_y']
df['target_dist'] = np.sqrt(df['target_dx']**2 + df['target_dy']**2)

df = df.merge(oof[['game_episode', 'pred_dx', 'pred_dy', 'error_dist']], on='game_episode', how='inner')
df['pred_dist'] = np.sqrt(df['pred_dx']**2 + df['pred_dy']**2)

# 1. 경기장 그리기 함수
def draw_pitch(ax, field_length=105, field_width=68, linecolor='black'):
    ax.set_facecolor('#3d8c40')
    ax.plot([0, 0], [0, field_width], color=linecolor, linewidth=2)
    ax.plot([0, field_length], [field_width, field_width], color=linecolor, linewidth=2)
    ax.plot([field_length, field_length], [field_width, 0], color=linecolor, linewidth=2)
    ax.plot([field_length, 0], [0, 0], color=linecolor, linewidth=2)
    ax.plot([field_length/2, field_length/2], [0, field_width], color=linecolor, linewidth=1.5)
    ax.add_patch(plt.Circle((field_length/2, field_width/2), 9.15, color=linecolor, fill=False))
    ax.set_xlim(-5, field_length+5)
    ax.set_ylim(-5, field_width+5)
    ax.set_aspect('equal')
    ax.axis('off')
    return ax

# 2. 에러 히트맵 시각화
def plot_error_heatmap():
    hard_cases = df[df['error_dist'] > 30]
    fig, ax = plt.subplots(figsize=(10, 6))
    draw_pitch(ax)
    hb = ax.hexbin(hard_cases['start_x'], hard_cases['start_y'], gridsize=15, cmap='Reds', mincnt=1, alpha=0.8)
    plt.colorbar(hb, label='Count of Severe Errors')
    plt.title('Error Heatmap: Where does the model fail?', fontsize=15, fontweight='bold')
    plt.show()

if __name__ == "__main__":
    plot_error_heatmap()