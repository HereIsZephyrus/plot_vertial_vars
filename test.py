from main import main
import json
from interface import construct_data
# 生成若干组样例数据
data_length = 10
pressure = [980, 925, 850, 775, 700, 625, 550, 475, 400, 290]
temperature = [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
dewpoint = [18, 16, 14, 12, 10, 8, 6, 4, 2, 0]
relative_humidity = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

data = {
    "info": {
        "province": "北京",
        "location": "北京",
        "time": "2021-01-01 00:00:00",
        "latitude": 39.90,
        "longitude": 116.40,
        "source": "CMA-GFS"
    },
    "variables": {
        "normal": {
            "temperature": temperature,
            "dewpoint": dewpoint,
            "specific_humidity": None
        },
        "wind": None,
        "humidity": {
            "relative_humidity": relative_humidity
        }
    },
    "pressure": pressure
}

main(construct_data(json.dumps(data)))