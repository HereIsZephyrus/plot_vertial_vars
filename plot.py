import matplotlib.pyplot as plt
from typing import List
from style import VariableStyle
from style import PLOT_STYLE, PLOT_VARIABLE_STYLE, ELEMENT_STYLE, FIGURE_STYLE, AX_STYLE
from interface import Variables, SampleInfo, Data

def init_plot():
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return plt.figure(**FIGURE_STYLE)

def add_plot(ax, pressure: List[float], data: List[float], style: VariableStyle):
    """
    添加绘图函数

    Parameters:
    ax - 坐标轴对象
    pressure: List[float] - 自变量(气压数据)
    data: List[float] - 因变量
    style: VariableStyle - 样式
    """
    for function in style.function:
        if function == "line":
            ax.plot(pressure, data, **PLOT_STYLE["line"], color=style.color)
        elif function == "marker":
            ax.plot(pressure, data, **PLOT_STYLE["marker"], color=style.color)
        elif function == "bar":
            ax.bar(pressure, data, **PLOT_STYLE["bar"], color=style.color)

def plot_warpper(fig, pressure: List[float], subplot_index: int, subplot_count: int, ax_style: dict):
    """
    探空子图生成器

    Parameters:
    fig - 图形对象
    pressure: List[float] - 气压数据 (hPa)
    subplot_index: int - 子图索引
    subplot_count: int - 子图数量

    Returns:
    plot_func: 子图生成函数
    """
    def plot_func(variable : dict[str, List[float]]):
        ax = fig.add_subplot(1, subplot_count, subplot_index, sharey=True)
        ax.invert_yaxis()
        ax.set_ylim(ax_style["y_lim"])
        ax.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.6, color='gray')
        ax.grid(True, which='minor', linestyle='-', linewidth=0.4, alpha=0.3, color='gray')
        y_ticks = [100, 150, 200, 250, 300, 400, 500, 550]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y) for y in y_ticks])
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        for key, value in variable.items():
            add_plot(ax, pressure, value, PLOT_VARIABLE_STYLE[key])
        return ax
    return plot_func

def generate_ax_func(fig, pressure: List[float], variables: Variables):
    """
    计算需要绘制的子图

    Parameters:
    fig - 图形对象
    pressure: List[float] - 气压数据 (hPa)
    variables: Variables - 变量

    Returns:
    func: 子图生成函数
    params: 子图参数
    """
    func = []
    params = []
    index = 1
    variable_table = variables.model_dump()
    axnum = sum(1 for _ in variable_table.values() if _ is not None)
    for plot_name, plot_content in variable_table.items():
        if plot_content is not None:
            func.append(plot_warpper(fig, pressure, index, axnum, AX_STYLE[plot_name]))
            raw_data = plot_content.model_dump()
            params.append( {key: value for key, value in raw_data.items() if value is not None} )
            index += 1
    return func, params


def plot_window_elements(fig, infos: SampleInfo):
    """
    绘制气象探空图的窗口
    
    Parameters:
    fig - 图形对象
    infos: SampleInfo - 样本信息
    """
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    title = f"{infos.province}：{infos.location} 坐标：[{infos.latitude},{infos.longitude}]"
    subtitle = f"{infos.time.strftime('%Y-%m-%dT%H')}"
    fig.suptitle(title,
                    fontsize=ELEMENT_STYLE["title"].size, 
                    fontweight=ELEMENT_STYLE["title"].weight,
                    color=ELEMENT_STYLE["title"].color,
                    y=ELEMENT_STYLE["title"].y,
                    ha=ELEMENT_STYLE["title"].location)
    fig.text(0.5, 0.92, subtitle,
                    ha=ELEMENT_STYLE["subtitle"].location,
                    color=ELEMENT_STYLE["subtitle"].color,
                    fontsize=ELEMENT_STYLE["subtitle"].size,
                    y=ELEMENT_STYLE["subtitle"].y)
    fig.text(0.5, 0.90, infos.source,
                    ha=ELEMENT_STYLE["source"].location,
                    fontsize=ELEMENT_STYLE["source"].size,
                    bbox=dict(boxstyle="round,pad=0.3"))
    plt.tight_layout()
    plt.subplots_adjust(top=0.87, wspace=0.3)

def main(data: Data):
    fig = init_plot()
    funcs, params = generate_ax_func(fig, data.pressure, data.variables)
    
    for func, param in zip(funcs, params):
        func(param)
    
    plot_window_elements(fig, data.info)
    plt.show()

def plot_sounding_diagram(pressure_data, temperature_data, dewpoint_data, wind_data=None, 
                         humidity_data=None, location="", date_time="", coords=""):
    """
    绘制完整的气象探空图（三列布局）
    
    Parameters:
    pressure_data: list - 气压数据 (hPa)
    temperature_data: list - 温度数据 (°C)
    dewpoint_data: list - 露点温度数据 (°C)
    wind_data: list - 风速数据 (m/s), 可选
    humidity_data: list - 相对湿度数据 (%), 可选
    location: str - 地点信息
    date_time: str - 日期时间
    coords: str - 坐标信息
    """
    
    # 设置所有子图的Y轴
    for ax in [ax1, ax2, ax3]:
        
    
    # 第一个子图：气象探空图（温度和露点温度）
    ax1.set_xlim(-120, 60)
    ax1.set_xlabel('(°C)', fontsize=12)
    ax1.set_ylabel('(hPa)', fontsize=12)
    
    # 绘制温度曲线（蓝色实线）
    ax1.plot(temperature_data, pressure_data, 'b-', linewidth=2.5, label='温度')
    
    # 绘制露点温度曲线（红色实线）
    ax1.plot(dewpoint_data, pressure_data, 'r-', linewidth=2.5, label='露点温度')
    
    # 添加垂直参考线（虚线）
    for temp in range(-120, 61, 20):
        ax1.axvline(x=temp, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
    
    # 添加温度数据标签
    for i, (p, t) in enumerate(zip(pressure_data, temperature_data)):
        ax1.text(t-3, p, f'{t:.2f}', color='blue', fontsize=8, ha='right', va='center')
    
    # 添加露点温度数据标签
    for i, (p, d) in enumerate(zip(pressure_data, dewpoint_data)):
        ax1.text(d+3, p, f'{d:.2f}', color='red', fontsize=8, ha='left', va='center')
    
    # 第二个子图：风速图
    ax2.set_xlim(0, 10)
    ax2.set_xlabel('(m/s)', fontsize=12)
    ax2.set_xticks(range(0, 11, 2))
    
    if wind_data is not None:
        # 绘制风速条形图
        for i, (p, w) in enumerate(zip(pressure_data, wind_data)):
            # 绘制水平条形图（黑色）
            bar_height = 25
            ax2.barh(p, w, height=bar_height, alpha=0.8, color='black', 
                    align='center', edgecolor='black', linewidth=0.5)
            
            # 添加数值标签
            if w > 0:
                ax2.text(w + 0.1, p, f'{w:.2f}', fontsize=8, va='center', ha='left')
    
    # 第三个子图：相对湿度图
    ax3.set_xlim(0, 100)
    ax3.set_xlabel('(%)', fontsize=12)
    ax3.set_xticks(range(0, 101, 20))
    
    if humidity_data is not None:
        # 绘制相对湿度曲线（绿色实线）
        ax3.plot(humidity_data, pressure_data, 'g-', linewidth=2.5, label='相对湿度')
        
        # 添加数据标签
        for i, (p, h) in enumerate(zip(pressure_data, humidity_data)):
            ax3.text(h + 1, p, f'{h:.2f}', color='green', fontsize=8, ha='left', va='center')
    
    return fig, (ax1, ax2, ax3)