import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import seaborn as sns

def draw_football_field(ax = None) :
    if ax is None :
        fig, ax = plt.subplots(figsize = (12, 8))

    # 필드 외곽선
    field = patches.Rectangle(
        (0, 0), 105, 68,
        linewidth = 2, edgecolor = 'white', facecolor = 'green', alpha = 0.3
    )
    ax.add_patch(field)

    # 중앙선
    ax.plot([52.5, 52.5], [0, 68], color = 'white', linewidth = 2)

    # 중앙 서클
    center_circle = patches.Circle(
        (52.5, 34), 9.15,
        linewidth=2, edgecolor='white', facecolor='none'
    )
    ax.add_patch(center_circle)
    
    # 페널티 박스 (왼쪽)
    penalty_left = patches.Rectangle(
        (0, 13.84), 16.5, 40.32,
        linewidth=2, edgecolor='white', facecolor='none'
    )
    ax.add_patch(penalty_left)
    
    # 페널티 박스 (오른쪽)
    penalty_right = patches.Rectangle(
        (88.5, 13.84), 16.5, 40.32,
        linewidth=2, edgecolor='white', facecolor='none'
    )
    ax.add_patch(penalty_right)
    
    # 골 에리어 (왼쪽)
    goal_left = patches.Rectangle(
        (0, 24.84), 5.5, 18.32,
        linewidth=2, edgecolor='white', facecolor='none'
    )
    ax.add_patch(goal_left)
    
    # 골 에리어 (오른쪽)
    goal_right = patches.Rectangle(
        (99.5, 24.84), 5.5, 18.32,
        linewidth=2, edgecolor='white', facecolor='none'
    )
    ax.add_patch(goal_right)
    
    ax.set_xlim(-5, 110)
    ax.set_ylim(-5, 73)
    ax.set_aspect('equal')
    ax.axis('off')
    
    return ax

def plot_pass_heatmap(pass_df, title="Pass 시작 위치 히트맵"):
    """
    패스 시작 위치 히트맵 그리기
    
    어디서 패스가 가장 많이 일어나는가?
    """
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # 축구장 그리기
    draw_football_field(ax)
    
    # 히트맵 생성
    heatmap, xedges, yedges = np.histogram2d(
        pass_df['start_x'], 
        pass_df['start_y'],
        bins=[21, 14],  # 5m × 5m 그리드
        range=[[0, 105], [0, 68]]
    )
    
    # 히트맵 표시
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    im = ax.imshow(
        heatmap.T, 
        extent=extent, 
        origin='lower',
        cmap='YlOrRd', 
        alpha=0.7,
        aspect='auto'
    )
    
    # 컬러바
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('패스 빈도', rotation=270, labelpad=20, fontsize=12)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('X 좌표 (m)', fontsize=12)
    ax.set_ylabel('Y 좌표 (m)', fontsize=12)
    
    plt.tight_layout()
    return fig


def plot_pass_destination_heatmap(pass_df, title="Pass 도착 위치 히트맵"):
    """
    패스 도착 위치 히트맵
    
    패스가 주로 어디로 향하는가?
    """
    fig, ax = plt.subplots(figsize=(14, 9))
    
    draw_football_field(ax)
    
    heatmap, xedges, yedges = np.histogram2d(
        pass_df['end_x'], 
        pass_df['end_y'],
        bins=[21, 14],
        range=[[0, 105], [0, 68]]
    )
    
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    im = ax.imshow(
        heatmap.T, 
        extent=extent, 
        origin='lower',
        cmap='Blues', 
        alpha=0.7,
        aspect='auto'
    )
    
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('패스 빈도', rotation=270, labelpad=20, fontsize=12)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('X 좌표 (m)', fontsize=12)
    ax.set_ylabel('Y 좌표 (m)', fontsize=12)
    
    plt.tight_layout()
    return fig

def plot_success_vs_fail_comparison(pass_df):
    """
    성공 패스 vs 실패 패스 비교
    
    2개 필드를 나란히 그려서 차이점 확인
    """
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    # 성공 패스
    success_df = pass_df[pass_df['result_name'] == 'Successful']
    draw_football_field(axes[0])
    
    heatmap_s, xedges, yedges = np.histogram2d(
        success_df['start_x'], 
        success_df['start_y'],
        bins=[21, 14],
        range=[[0, 105], [0, 68]]
    )
    
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    im1 = axes[0].imshow(
        heatmap_s.T, 
        extent=extent, 
        origin='lower',
        cmap='Greens', 
        alpha=0.7,
        aspect='auto'
    )
    axes[0].set_title('✅ 성공 패스 위치', fontsize=14, fontweight='bold')
    plt.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)
    
    # 실패 패스
    fail_df = pass_df[pass_df['result_name'] == 'Unsuccessful']
    draw_football_field(axes[1])
    
    heatmap_f, xedges, yedges = np.histogram2d(
        fail_df['start_x'], 
        fail_df['start_y'],
        bins=[21, 14],
        range=[[0, 105], [0, 68]]
    )
    
    im2 = axes[1].imshow(
        heatmap_f.T, 
        extent=extent, 
        origin='lower',
        cmap='Reds', 
        alpha=0.7,
        aspect='auto'
    )
    axes[1].set_title('❌ 실패 패스 위치', fontsize=14, fontweight='bold')
    plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    return fig

def plot_pass_arrows(pass_df, sample_size=500, title="패스 방향 샘플"):
    """
    패스 방향을 화살표로 시각화
    
    너무 많으면 복잡하니 샘플링
    """
    fig, ax = plt.subplots(figsize=(14, 9))
    
    draw_football_field(ax)
    
    # 샘플링
    if len(pass_df) > sample_size:
        sample = pass_df.sample(n=sample_size, random_state=42)
    else:
        sample = pass_df
    
    # 성공/실패 구분
    success = sample[sample['result_name'] == 'Successful']
    fail = sample[sample['result_name'] == 'Unsuccessful']
    
    # 성공 패스 (초록)
    for _, row in success.iterrows():
        ax.arrow(
            row['start_x'], row['start_y'],
            row['end_x'] - row['start_x'],
            row['end_y'] - row['start_y'],
            head_width=1.5, head_length=1,
            fc='green', ec='green', alpha=0.3, linewidth=0.5
        )
    
    # 실패 패스 (빨강)
    for _, row in fail.iterrows():
        ax.arrow(
            row['start_x'], row['start_y'],
            row['end_x'] - row['start_x'],
            row['end_y'] - row['start_y'],
            head_width=1.5, head_length=1,
            fc='red', ec='red', alpha=0.5, linewidth=0.8
        )
    
    # 범례
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='green', lw=2, label=f'성공 ({len(success)})'),
        Line2D([0], [0], color='red', lw=2, label=f'실패 ({len(fail)})')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    return fig