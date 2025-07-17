import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

def plot_sounding_diagram(pressure_data, temperature_data, dewpoint_data, wind_data=None, 
                         humidity_data=None, title="", location="", date_time="", coords=""):
    """
    绘制完整的气象探空图（三列布局）
    
    Parameters:
    pressure_data: list - 气压数据 (hPa)
    temperature_data: list - 温度数据 (°C)
    dewpoint_data: list - 露点温度数据 (°C)
    wind_data: list - 风速数据 (m/s), 可选
    humidity_data: list - 相对湿度数据 (%), 可选
    title: str - 主标题
    location: str - 地点信息
    date_time: str - 日期时间
    coords: str - 坐标信息
    """
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图形和三个子图
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 10), sharey=True)
    
    # 设置总标题
    main_title = f"{location} {coords}"
    sub_title = date_time
    
    fig.suptitle(main_title, fontsize=16, fontweight='bold', y=0.95)
    if sub_title:
        fig.text(0.5, 0.92, sub_title, ha='center', fontsize=12)
    
    # 添加CMA-GFS图例
    fig.text(0.85, 0.92, "CMA-GFS", ha='center', fontsize=10, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
    
    # 设置所有子图的Y轴
    for ax in [ax1, ax2, ax3]:
        ax.set_yscale('log')
        ax.invert_yaxis()
        ax.set_ylim(550, 100)
        ax.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
        ax.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.5)
        
        # 设置Y轴刻度
        y_ticks = [100, 150, 200, 250, 300, 400, 500, 550]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y) for y in y_ticks])
    
    # 第一个子图：气象探空图（温度和露点温度）
    ax1.set_xlim(-120, 60)
    ax1.set_xlabel('温度 (°C)', fontsize=11)
    ax1.set_ylabel('气压 (hPa)', fontsize=11)
    
    # 绘制温度曲线（蓝色）
    temp_line = ax1.plot(temperature_data, pressure_data, 'b-', linewidth=2, label='温度')
    
    # 绘制露点温度曲线（红色）
    dewpoint_line = ax1.plot(dewpoint_data, pressure_data, 'r-', linewidth=2, label='露点温度')
    
    # 添加垂直参考线
    for temp in [-100, -80, -60, -40, -20, 0, 20, 40]:
        ax1.axvline(x=temp, color='gray', linestyle='--', alpha=0.3, linewidth=0.5)
    
    # 添加数据标签
    for i, (p, t, d) in enumerate(zip(pressure_data, temperature_data, dewpoint_data)):
        if i % 2 == 0:  # 每隔一个点显示标签
            ax1.text(t-5, p, f'{t:.1f}', color='blue', fontsize=8, ha='right')
            ax1.text(d+5, p, f'{d:.1f}', color='red', fontsize=8, ha='left')
    
    # 第二个子图：风速图
    ax2.set_xlim(0, 10)
    ax2.set_xlabel('风速 (m/s)', fontsize=11)
    ax2.set_xticks([0, 2, 4, 6, 8, 10])
    
    if wind_data is not None:
        # 绘制风速条形图
        for i, (p, w) in enumerate(zip(pressure_data, wind_data)):
            if w > 0:
                # 绘制水平条形图
                bar_height = 20  # 条形图高度
                ax2.barh(p, w, height=bar_height, alpha=0.8, color='black', align='center')
                # 添加数值标签
                ax2.text(w + 0.1, p, f'{w:.2f}', fontsize=8, va='center')
    
    # 第三个子图：相对湿度图
    ax3.set_xlim(0, 100)
    ax3.set_xlabel('相对湿度 (%)', fontsize=11)
    ax3.set_xticks([0, 20, 40, 60, 80, 100])
    
    if humidity_data is not None:
        # 绘制相对湿度曲线（绿色）
        humidity_line = ax3.plot(humidity_data, pressure_data, 'g-', linewidth=2, label='相对湿度')
        
        # 添加数据标签
        for i, (p, h) in enumerate(zip(pressure_data, humidity_data)):
            if i % 2 == 0:  # 每隔一个点显示标签
                ax3.text(h + 2, p, f'{h:.1f}', color='green', fontsize=8, ha='left')
    
    # 调整子图间距
    plt.tight_layout()
    plt.subplots_adjust(top=0.87)
    
    return fig, (ax1, ax2, ax3)

# 示例数据
def create_sample_data():
    """创建示例数据"""
    # 气压数据 (hPa)
    pressure = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    
    # 温度数据 (°C) - 模拟实际探空数据
    temperature = [-70.94, -54.5, -40.47, -23.35, -15.08, -6.69, -8.21, -9.61, -10.98, -12.24]
    
    # 露点温度数据 (°C) - 通常低于温度
    dewpoint = [-78.68, -58.46, -67.27, -81.64, -84.98, -8.19, -22.77, -26.3, -29.6, -32.0]
    
    # 风速数据 (m/s)
    wind_speed = [5.35, 2.81, 3.47, 0.97, 0.97, 0.97, 0.97, 0.96, 0.96, 0.96]
    
    # 相对湿度数据 (%)
    humidity = [61.91, 62.83, 66.48, 60.81, 51.56, 44.57, 39.14, 34.83, 31.34, 28.47]
    
    return pressure, temperature, dewpoint, wind_speed, humidity