from main import main
import json
from interface import construct_data
# 生成若干组样例数据
data_length = 10
pressure = [980, 925, 850, 775, 700, 625, 550, 475, 400, 290]
temperature = [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
dewpoint = [18, 16, 14, 12, 10, 8, 6, 4, 2, 0]
relative_humidity = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
specific_humidity = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

test_info = {
    "province": "武汉",
    "location": "湖北气象信息大厦",
    "time": "2025-07-18 00:00:00",
    "latitude": 30.58,
    "longitude": 114.31,
    "source": "CMA-GFS"
}

data1 = {
    "info": test_info,
    "variables": {
        "temperature": {
            "temperature": temperature,
            "dewpoint": dewpoint,
            "specific_humidity": specific_humidity
        },
        "wind": None,
        "humidity": None
    },
    "pressure": pressure
}

data2 = {
    "info": test_info,
    "variables": {
        "temperature": {
            "temperature": temperature,
            "dewpoint": dewpoint,
            "specific_humidity": specific_humidity
        },
        "wind": None,
        "humidity": {
            "relative_humidity": relative_humidity
        }
    },
    "pressure": pressure
}

main(construct_data(json.dumps(data1)), "test1.png")
main(construct_data(json.dumps(data2)), "test2.png")