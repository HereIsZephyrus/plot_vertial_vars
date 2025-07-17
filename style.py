from pydantic import BaseModel

class Font(BaseModel):
    size: int
    weight: str
    color: str
    family: str
    location: str
    y: float

class VariableStyle(BaseModel):
    color: str
    label: str
    function: list[str]

class AxisStyle(BaseModel):
    width : float

ELEMENT_STYLE = {
    "title": Font(size=16, weight="bold", color="#8D666B", family="SimHei", location="center", y=0.95),
    "subtitle": Font(size=10, weight="normal", color="#8D666B", family="SimHei", location="center", y=0.90),
    "label": Font(size=10, weight="normal", color="#8D666B", family="SimHei", location="center", y=0.90),
}

PLOT_VARIABLE_STYLE = {
    "temperature": VariableStyle(color="#FF0000", label="温度", function=["line", "marker"]),
    "dewpoint": VariableStyle(color="#0000FF", label="露点温度", function=["line", "marker"]),
    "specific_humidity": VariableStyle(color="#008000", label="比湿", function=["line", "marker"]),
    "wind": VariableStyle(color="#000000", label="风速", function=["bar", "wind"]),
    "relative_humidity": VariableStyle(color="#008000", label="相对湿度", function=["line", "marker"]),
}

PLOT_STYLE = {
    "line":{
        "line_style": "-",
        "line_width": 2
    },
    "marker":{
        "marker_size": 5,
        "marker_style": "o",
    },
    "bar":{
        "bar_width": 0.5
    },
    "wind":{
        
    }
}

FIGURE_STYLE = {
    "figsize": (12, 8),
}

AX_STYLE = {
    "plot": {

    },
    "wind": {

    },
    "humidity": {

    },
}