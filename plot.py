import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from typing import List
from style import VariableStyle, AxisStyle
from style import PLOT_STYLE, PLOT_VARIABLE_STYLE, ELEMENT_STYLE, FIGURE_STYLE, AX_STYLE
from interface import Variables, SampleInfo, Data
import sys
import numpy as np
from functools import partial
from adjustText import adjust_text

def init_plot():
    if sys.platform == "win32":
        plt.rcParams['font.sans-serif'] = ['STSong', 'DejaVu Sans']
    elif sys.platform == "linux":
        plt.rcParams['font.sans-serif'] = ['Unifont', 'Noto Sans CJK JP', 'DejaVu Sans']
    elif sys.platform == "darwin":
        plt.rcParams['font.sans-serif'] = ['SimHei','DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return plt.figure(figsize=FIGURE_STYLE["figsize"])

def add_plot(ax, pressure: List[float], data: List[float], style: VariableStyle, show_digit: bool):
    """
    添加绘图函数

    Parameters:
    ax - 坐标轴对象
    pressure: List[float] - 自变量(气压数据)
    data: List[float] - 因变量
    style: VariableStyle - 样式
    show_digit: bool - 是否显示数字
    """
    if not data or not pressure or len(data) != len(pressure):
        raise ValueError(f"Invalid data for {style.label}")

    x_range = max(data) - min(data)
    y_range = max(pressure) - min(pressure)
    for function in style.function:
        if function == "line":
            ax.plot(data, pressure, **PLOT_STYLE["line"], color=style.color, label=style.label)
            if show_digit:
                
                for x, y in zip(data, pressure):
                    x_offset = x_range * style.x_offset
                    y_offset = y_range * style.y_offset
                    
                    ax.text(x - x_offset, y - y_offset, f"{x:.1f}", 
                            color=style.color,
                           ha='left', va='center', fontsize=8,
                           bbox=dict(boxstyle="round,pad=0.2", 
                                    facecolor='white', alpha=0.9, edgecolor='none'))

        elif function == "bar":
            ax.barh(pressure, data, **PLOT_STYLE["bar"], color=style.color, label=style.label)
            if show_digit:
                max_value = max(data)
                for x, y in zip(data, pressure):
                    x_offset = x_range * style.x_offset
                    y_offset = y_range * style.y_offset
                    if x == max_value:
                        x_offset = x_range * style.x_offset * 2
                        y_offset = y_range * style.y_offset * 2
                    ax.text(x + x_offset, y - y_offset, f"{x:.1f}", 
                            color=style.color,
                            ha='left', va='center', fontsize=8,
                            bbox=dict(boxstyle="round,pad=0.2", 
                                        facecolor='white', alpha=0.9, edgecolor='none'))
        elif function == "wind":
            pass # 在add_wind_plot中绘制

def draw_wind_barb(ax, x, y, wind_speed, wind_direction, length, pivot='middle'):
    """
    绘制单个风矢
    
    Parameters:
    ax - 坐标轴对象
    x, y - 风矢的位置
    wind_speed - 风速 (m/s)
    wind_direction - 风向 (度，0度为北风)
    length - 风矢长度
    pivot - 风矢的锚点位置
    """
    # 转换风向：(1)气象风向是指风的来向，matplotlib需要的是去向；(2)气象风向0度为北风，matplotlib 0度为东风
    wind_direction_rad = np.radians(wind_direction + 180)
    u = wind_speed * np.sin(wind_direction_rad)
    v = wind_speed * np.cos(wind_direction_rad)
    ax.barbs(x, y, u, v, length=length, pivot=pivot, 
             barbcolor='black', flagcolor='red', linewidth=1, clip_on=False)

def add_wind_plot(ax, pressure: List[float], wind_speed: List[float], 
                  wind_direction: List[float], is_first: bool):
    """
    添加风矢图
    
    Parameters:
    ax - 坐标轴对象
    pressure - 气压数据
    wind_speed - 风速数据
    wind_direction - 风向数据
    style - 样式
    """
    if not wind_speed or not wind_direction or not pressure:
        raise ValueError(f"Invalid wind data")
    
    x_pos = 3 if is_first else -5
    y_bias = 8 if is_first else 2
    length = 5 if is_first else 6
    for (ws, wd, p) in zip(wind_speed, wind_direction, pressure):
        if ws is not None and wd is not None and ws > 0:
            draw_wind_barb(ax, x_pos, p + y_bias, ws, wd, length)
            y_bias += 1

def plot_warpper(fig, pressure: List[float], subplot_index: int, subplot_count: int, plot_name: str, show_digit: bool):
    """
    探空子图生成器

    Parameters:
    fig - 图形对象
    pressure: List[float] - 气压数据 (hPa)
    subplot_index: int - 子图索引
    subplot_count: int - 子图数量
    show_digit: bool - 是否显示数字

    Returns:
    plot_func: 子图生成函数
    """
    ax_style : AxisStyle = AX_STYLE[plot_name]
    min_ytick = int((min(pressure) // 50) * 50)
    max_ytick = int(((max(pressure) + 49) // 50) * 50)
    y_lim = [min_ytick - 10, max_ytick + 10]
    y_ticks = list(range(min_ytick, max_ytick + 1, 100))
    plot_generator = partial(add_plot, show_digit=show_digit)
    def plot_func(variable : dict[str, List[float]], gs=None):
        if gs is not None:
            ax = fig.add_subplot(gs[0, subplot_index-1])
        else:
            ax = fig.add_subplot(1, subplot_count, subplot_index)
        
        ax.grid(True, which='major', linestyle=ax_style.grid_line_style, linewidth=ax_style.grid_line_width, alpha=ax_style.grid_line_alpha, color=ax_style.grid_line_color)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.set_xlim(ax_style.x_lim)
        ax.set_xlabel(ax_style.x_label)
        if subplot_index == 1:
            ax.set_ylabel("(hPa)")
            ax.set_ylim(y_lim)
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(y) for y in y_ticks])
        elif subplot_count > 1 and subplot_index == subplot_count:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            ax.yaxis.set_label_coords(1.05, 0.5)
            ax.set_ylim(y_lim)
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([str(y) for y in y_ticks])
        else:
            ax.set_yticklabels([])

        if plot_name == "wind": # 风图的一些特殊处理
            xlim = ax_style.x_lim
            if xlim[1] < max(variable["wind_speed"]):
                xlim[1] = max(variable["wind_speed"]) + 1
            ax.set_xlim(xlim)
            add_wind_plot(ax, pressure, variable["wind_speed"], variable["wind_direction"], subplot_index == 1)

        for key, value in variable.items():
            plot_generator(ax, pressure, value, PLOT_VARIABLE_STYLE[key])
            if (key == "specific_humidity"): # 比湿额外增加x轴标签
                ax.text(0.82, -0.05, "(g/kg)", transform=ax.transAxes, ha='center', va='center')

        ax.invert_yaxis()
        ax.legend(loc=ax_style.label_location,framealpha=0.5, facecolor="none")
        
        return ax
    return plot_func

def generate_ax_func(fig, pressure: List[float], variables: Variables, show_digit: bool):
    """
    计算需要绘制的子图

    Parameters:
    fig - 图形对象
    pressure: List[float] - 气压数据 (hPa)
    variables: Variables - 变量
    show_digit: bool - 是否显示数字

    Returns:
    func: 子图生成函数
    params: 子图参数
    gs: GridSpec对象
    """
    func = []
    params = []
    width_ratios = []
    index = 1
    variable_table = variables.model_dump()
    axnum = 0
    remain_with = 0
    for name,data in variable_table.items():
        if data is not None:
            axnum += 1
            remain_with += AX_STYLE[name].figure_width or 0
    remain_with = FIGURE_STYLE["figsize"][0] - remain_with
    for plot_name, plot_content in variable_table.items():
        if plot_content is not None:
            if AX_STYLE[plot_name].figure_width is not None:
                width_ratios.append(AX_STYLE[plot_name].figure_width)
            else:
                width_ratios.append(remain_with)
            func.append(plot_warpper(fig, pressure, index, axnum, plot_name, show_digit))
            params.append( {key: value for key, value in plot_content.items() if value is not None} )
            index += 1
    gs = gridspec.GridSpec(1, axnum, width_ratios=width_ratios)
    return func, params, gs

def plot_window_elements(fig, infos: SampleInfo):
    """
    绘制气象探空图的窗口
    
    Parameters:
    fig - 图形对象
    infos: SampleInfo - 样本信息
    """

    title = f"{infos.province}：{infos.location} 坐标：[{infos.latitude},{infos.longitude}]"
    subtitle = f"{infos.time.strftime('%Y-%m-%dT%H')}"
    fig.suptitle(title,
                    fontsize=ELEMENT_STYLE["title"].size, 
                    fontweight=ELEMENT_STYLE["title"].weight,
                    color=ELEMENT_STYLE["title"].color,
                    y=ELEMENT_STYLE["title"].y,
                    ha=ELEMENT_STYLE["title"].location)
    fig.text(x=ELEMENT_STYLE["subtitle"].x,
            y=ELEMENT_STYLE["subtitle"].y,
            s=subtitle,
            ha=ELEMENT_STYLE["subtitle"].location,
            color=ELEMENT_STYLE["subtitle"].color,
            fontsize=ELEMENT_STYLE["subtitle"].size,)
    fig.text(x=ELEMENT_STYLE["source"].x,
            y=ELEMENT_STYLE["source"].y,
            s=infos.source,
            ha=ELEMENT_STYLE["source"].location,
            fontsize=ELEMENT_STYLE["source"].size,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black"))
    plt.tight_layout()
    plt.subplots_adjust(top=0.87, wspace=0.1)