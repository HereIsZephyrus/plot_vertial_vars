import matplotlib.pyplot as plt
from typing import List
from style import VariableStyle, AxisStyle
from style import PLOT_STYLE, PLOT_VARIABLE_STYLE, ELEMENT_STYLE, FIGURE_STYLE, AX_STYLE
from interface import Variables, SampleInfo, Data

def init_plot():
    # 使用经过测试的中文字体，优先使用Unifont和Noto Sans CJK JP
    plt.rcParams['font.sans-serif'] = ['Unifont', 'Noto Sans CJK JP', 'DejaVu Sans']
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

def plot_warpper(fig, pressure: List[float], subplot_index: int, subplot_count: int, ax_style: AxisStyle):
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
        ax = fig.add_subplot(1, subplot_count, subplot_index)
        ax.invert_yaxis()
        ax.set_ylim(ax_style.y_lim)
        ax.grid(True, which='major', linestyle=ax_style.grid_line_style, linewidth=ax_style.grid_line_width, alpha=ax_style.grid_line_alpha, color=ax_style.grid_line_color)
        ax.set_yticks(ax_style.y_ticks)
        ax.set_yticklabels([str(y) for y in ax_style.y_ticks])
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
            params.append( {key: value for key, value in plot_content.items() if value is not None} )
            index += 1
    return func, params

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
            bbox=dict(boxstyle="round,pad=0.3"))
    plt.tight_layout()
    plt.subplots_adjust(top=0.87, wspace=0.3)