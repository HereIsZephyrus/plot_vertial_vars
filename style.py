from pydantic import BaseModel
from typing import List, Union

class Font(BaseModel):
    size: int
    weight: str
    color: str
    location: str
    x: float
    y: float

class VariableStyle(BaseModel):
    color: str
    label: str
    function: list[str]

class AxisStyle(BaseModel):
    grid_line_width : float = 0.8
    grid_line_color : str = "gray"
    grid_line_alpha : float = 0.6
    grid_line_style : str = "-"
    x_lim : List[float]
    x_label : str
    figure_width : Union[float, None] = None
    
ELEMENT_STYLE = {
    "title": Font(size=16, weight="bold", color="#8D666B", location="center", x=0.5, y=0.95),
    "subtitle": Font(size=10, weight="normal", color="#8D666B", location="center", x=0.5, y=0.90),
    "source": Font(size=10, weight="normal", color="#8D666B", location="center", x=0.90, y=0.90),
}

PLOT_VARIABLE_STYLE = {
    "temperature": VariableStyle(color="#FF0000", label="温度", function=["line"]),
    "dewpoint": VariableStyle(color="#0000FF", label="露点温度", function=["line"]),
    "specific_humidity": VariableStyle(color="#008000", label="比湿", function=["line"]),
    "wind_speed": VariableStyle(color="#000000", label="风速", function=["bar"]),
    "wind_direction": VariableStyle(color="#000000", label="风向", function=["wind"]),
    "relative_humidity": VariableStyle(color="#008000", label="相对湿度", function=["line"]),
}

PLOT_STYLE = {
    "line":{
        "linestyle": "-",
        "linewidth": 2,
        "markersize": 5,
        "marker": "o",
        "markerfacecolor": "white",     # 设置为白色填充
        "markeredgewidth": 1.5,         # 设置边框宽度
    },
    "bar":{
        "width": 0.5
    },
    "wind":{
        
    }
}

FIGURE_STYLE = {
    "figsize": (8, 8),
}

AX_STYLE = {
    "temperature": AxisStyle(x_lim=[-120, 40], x_label="(°C)", figure_width=None),
    "wind": AxisStyle(x_lim=[0, 10], x_label="(m/s)", figure_width=1),
    "humidity": AxisStyle(x_lim=[0, 100], x_label="(%)", figure_width=1.2),
}