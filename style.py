ELEMENT_STYLE = {
    "title": {
        "font_size": 16,
        "font_weight": "bold",
        "color": "#8D666B",
        "font_family": "SimHei",
        "location": "center",
        "y": 0.95,
    },
    "subtitle": {
        "font_size": 10,
        "color": "#8D666B",
        "font_family": "SimHei",
        "location": "center",
        "y": 0.90,
    },
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

PLOT_VARIABLE_STYLE = {
    "temperature": {
        "color": "#FF0000",
        "label": "温度",
        "function": ["line", "marker"]
    },
    "dewpoint": {
        "color": "#0000FF",
        "label": "露点温度",
        "function": ["line", "marker"]
    },
    "specific_humidity": {
        "color": "#008000",
        "label": "比湿",
        "function": ["line", "marker"]
    },
    "wind": {
        "color": "#000000",
        "label": "风速",
        "function": ["bar", "wind"]
    },
    "relative_humidity": {
        "color": "#008000",
        "label": "相对湿度",
        "function": ["line", "marker"]
    }
}

FIGURE_STYLE = {
    "figure_size": (12, 8),
}