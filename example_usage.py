#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整气象探空图绘制 - 使用示例
包含：温度露点图、风速图、相对湿度图
"""

from main import plot_sounding_diagram

# 你的实际数据示例
def your_data_example():
    """
    替换为你的实际数据
    所有列表长度必须相同
    """
    # 气压数据 (hPa) - 从高空到地面
    pressure = [100, 150, 200, 250, 300, 400, 500, 550]
    
    # 温度数据 (°C) - 对应各气压层的温度
    temperature = [-70.94, -54.5, -40.47, -23.35, -15.08, -8.21, -10.98, -12.24]
    
    # 露点温度数据 (°C) - 对应各气压层的露点温度
    dewpoint = [-78.68, -58.46, -67.27, -81.64, -84.98, -22.77, -29.6, -32.0]
    
    # 风速数据 (m/s) - 可选
    wind_speed = [5.35, 2.81, 3.47, 0.97, 0.97, 0.97, 0.96, 0.96]
    
    # 相对湿度数据 (%) - 可选
    humidity = [61.91, 62.83, 66.48, 60.81, 51.56, 39.14, 31.34, 28.47]
    
    return pressure, temperature, dewpoint, wind_speed, humidity

# 最简单的使用方式
if __name__ == "__main__":
    # 获取你的数据
    p_data, t_data, d_data, w_data, h_data = your_data_example()
    
    # 绘制完整的三列气象探空图
    fig, axes = plot_sounding_diagram(
        pressure_data=p_data,
        temperature_data=t_data,
        dewpoint_data=d_data,
        wind_data=w_data,          # 风速数据，可选
        humidity_data=h_data,      # 相对湿度数据，可选
        title="",                  # 主标题（可选）
        location="青海省：海西蒙古族藏族自治州都兰县",
        date_time="MOAP 2025-07-17T08:024    2025-07-18T08",
        coords="坐标：[96.68E,35.61N]"
    )
    
    # 显示图表
    import matplotlib.pyplot as plt
    plt.show()
    
    print("完整气象探空图已显示！")
    print("\n图表包含三个部分：")
    print("1. 左侧：温度和露点温度曲线")
    print("2. 中间：风速条形图")
    print("3. 右侧：相对湿度曲线")

# 仅显示温度和露点的简化版本
def simple_example():
    """
    如果你只有温度和露点数据
    """
    pressure = [100, 150, 200, 250, 300, 400, 500, 550]
    temperature = [-70, -55, -40, -25, -15, -8, -11, -12]
    dewpoint = [-78, -58, -67, -81, -85, -23, -30, -32]
    
    fig, axes = plot_sounding_diagram(
        pressure_data=pressure,
        temperature_data=temperature,
        dewpoint_data=dewpoint,
        wind_data=None,           # 不显示风速
        humidity_data=None,       # 不显示相对湿度
        location="你的地点",
        date_time="2025-07-17 08:00",
        coords="坐标：[经度,纬度]"
    )
    
    import matplotlib.pyplot as plt
    plt.show()

# 如果你想运行简化版本，取消下面的注释
# simple_example() 