# 大气垂直廓线绘图工具

一个用于绘制大气垂直廓线图的Python工具，支持温度、湿度、风力等多种气象要素以支持单图、双图、三图等多种布局方式可视化,同时支持json和Pydantic两种数据格式。
使用依赖注入的方式，将绘图逻辑逐层分离分离，方便扩展和维护。

## 项目结构

```
plot_vertial_vars/
├── main.py           # 主程序入口
├── plot.py          # 核心绘图功能
├── interface.py     # 数据接口定义
├── style.py         # 样式配置
├── test.py          # 测试示例
├── list_font.py     # 字体列表工具
├── requirements.txt # 依赖配置
├── figures/         # 示例输出图片
└── README.md        # 项目说明
```

## 数据格式

### 输入JSON结构

```json
{
    "info": {
        "province": <省份名称>,
        "location": <站点名称>,
        "time": <请求时间>,
        "latitude": <纬度>,
        "longitude": <经度>,
        "source": <数据来源>
    },
    "variables": {
        "temperature": {
            "temperature": <温度列表> | None,
            "dewpoint": <露点温度列表> | None,
            "specific_humidity": <比湿列表> | None
        },
        "wind": {
            "wind_speed": <风速列表> | None,
            "wind_direction": <风向列表> | None
        },
        "humidity": {
            "relative_humidity": <相对湿度列表> | None
        }
    },
    "pressure": <气压层次列表>,
    "show_digit": <是否显示数值>
}
```

### 字段说明

- **info**: 站点信息
  - `province`: 省份名称（可选）
  - `location`: 站点名称
  - `time`: 观测时间
  - `latitude`: 纬度
  - `longitude`: 经度
  - `source`: 数据源（默认为CMA-GFS）

- **variables**: 气象要素数据
  - `temperature`: 温度相关数据
    - `temperature`: 温度（°C）
    - `dewpoint`: 露点温度（°C）
    - `specific_humidity`: 比湿（g/kg）
  - `wind`: 风力数据
    - `wind_speed`: 风速（m/s）
    - `wind_direction`: 风向（°）
  - `humidity`: 湿度数据
    - `relative_humidity`: 相对湿度（%）

- **pressure**: 气压层次（hPa）
- **show_digit**: 是否显示数值（布尔值）

## 示例输出

![](https://cdn.jsdelivr.net/gh/HereIsZephyrus/zephyrus.img/images/blog/test_vert3digit.png)


## 自定义配置

### 样式配置

可以通过修改 `style.py` 文件来自定义：
- 颜色方案
- 字体大小
- 图表布局
- 坐标轴样式

### 添加新的气象要素

1. 在 `interface.py` 中添加新的数据模型
2. 在 `style.py` 中配置相应的样式