import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from typing import List
from style import VariableStyle, AxisStyle
from style import PLOT_STYLE, PLOT_VARIABLE_STYLE, ELEMENT_STYLE, FIGURE_STYLE, AX_STYLE
from interface import Variables, SampleInfo, Data

def init_plot():
    # 使用经过测试的中文字体，优先使用Unifont和Noto Sans CJK JP
    plt.rcParams['font.sans-serif'] = ['Unifont', 'Noto Sans CJK JP', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return plt.figure(figsize=FIGURE_STYLE["figsize"])

def add_plot(ax, pressure: List[float], data: List[float], style: VariableStyle):
    """
    添加绘图函数

    Parameters:
    ax - 坐标轴对象
    pressure: List[float] - 自变量(气压数据)
    data: List[float] - 因变量
    style: VariableStyle - 样式
    """
    if not data or not pressure or len(data) != len(pressure):
        print(f"Warning: Invalid data for {style.label}")
        return

    for function in style.function:
        if function == "line":
            # 气象探空图：x轴是数据值，y轴是气压值
            ax.plot(data, pressure, **PLOT_STYLE["line"], color=style.color, label=style.label)
        elif function == "bar":
            # 条形图
            ax.bar(data, pressure, **PLOT_STYLE["bar"], color=style.color, label=style.label)
        elif function == "wind":
            # 风向图（待实现）
            pass

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
    min_ytick = int((min(pressure) // 50) * 50)
    max_ytick = int(((max(pressure) + 49) // 50) * 50)
    y_lim = [min_ytick, max_ytick]
    y_ticks = list(range(min_ytick, max_ytick + 1, 100))
    def plot_func(variable : dict[str, List[float]], gs=None):
        if gs is not None:
            ax = fig.add_subplot(gs[0, subplot_index-1])
        else:
            ax = fig.add_subplot(1, subplot_count, subplot_index)
        
        ax.invert_yaxis()
        ax.grid(True, which='major', linestyle=ax_style.grid_line_style, linewidth=ax_style.grid_line_width, alpha=ax_style.grid_line_alpha, color=ax_style.grid_line_color)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.set_xlim(ax_style.x_lim)
        ax.set_xlabel(ax_style.x_label)
        ax.set_ylim(y_lim)
        ax.set_yticks(y_ticks)
        ax.set_yticklabels([str(y) for y in y_ticks])
        if subplot_index == 1:
            ax.set_ylabel("(hPa)")
        if subplot_count > 1 and subplot_index == subplot_count:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            ax.yaxis.set_label_coords(1.05, 0.5)

        for key, value in variable.items():
            add_plot(ax, pressure, value, PLOT_VARIABLE_STYLE[key])

        ax.legend(loc='best')
        
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
    remain_with += (axnum - 1) * 2
    remain_with = FIGURE_STYLE["figsize"][0] - remain_with
    for plot_name, plot_content in variable_table.items():
        if plot_content is not None:
            if AX_STYLE[plot_name].figure_width is not None:
                width_ratios.append(AX_STYLE[plot_name].figure_width)
            else:
                width_ratios.append(remain_with)
            func.append(plot_warpper(fig, pressure, index, axnum, AX_STYLE[plot_name]))
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
            bbox=dict(boxstyle="round,pad=0.3"))
    plt.tight_layout()
    plt.subplots_adjust(top=0.87, wspace=0.1)