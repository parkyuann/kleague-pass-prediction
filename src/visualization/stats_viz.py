import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_distance_distribution(pass_df):
    """
    패스 거리 분포
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # 전체 분포
    axes[0].hist(pass_df['distance'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    axes[0].axvline(pass_df['distance'].mean(), color='red', linestyle='--', linewidth=2, label=f'평균: {pass_df["distance"].mean():.2f}m')
    axes[0].set_xlabel('패스 거리 (m)', fontsize=12)
    axes[0].set_ylabel('빈도', fontsize=12)
    axes[0].set_title('패스 거리 분포', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # 성공 vs 실패
    success_dist = pass_df[pass_df['result_name'] == 'Successful']['distance']
    fail_dist = pass_df[pass_df['result_name'] == 'Unsuccessful']['distance']
    
    axes[1].hist(success_dist, bins=30, alpha=0.6, label='성공', color='green', edgecolor='black')
    axes[1].hist(fail_dist, bins=30, alpha=0.6, label='실패', color='red', edgecolor='black')
    axes[1].set_xlabel('패스 거리 (m)', fontsize=12)
    axes[1].set_ylabel('빈도', fontsize=12)
    axes[1].set_title('성공 vs 실패 패스 거리', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_zone_success_rate(pass_df):
    """
    구역별 성공률
    """
    # 구역별 통계
    zone_stats = []
    for zone in ['defensive', 'middle', 'attacking']:
        zone_data = pass_df[pass_df['zone_x'] == zone]
        success = (zone_data['result_name'] == 'Successful').sum()
        total = len(zone_data)
        rate = success / total * 100 if total > 0 else 0
        
        zone_stats.append({
            'zone': zone,
            'success_rate': rate,
            'total': total
        })
    
    stats_df = pd.DataFrame(zone_stats)
    
    # 그래프
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(stats_df['zone'], stats_df['success_rate'], 
                   color=['#3498db', '#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black')
    
    # 값 표시
    for i, (bar, row) in enumerate(zip(bars, stats_df.itertuples())):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%\n({row.total:,}개)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('필드 구역', fontsize=12)
    ax.set_ylabel('성공률 (%)', fontsize=12)
    ax.set_title('구역별 패스 성공률', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig