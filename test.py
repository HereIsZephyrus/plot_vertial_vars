from main import main
import json
from interface import construct_data
# 生成若干组样例数据
data_length = 10
pressure = [550, 500, 450, 400, 350, 300, 250, 200, 150, 100]
temperature = [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
dewpoint = [18, 16, 14, 12, 10, 8, 6, 4, 2, 0]
relative_humidity = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
specific_humidity = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
wind_speed = [1, 4, 10, 23, 5, 20, 17, 4, 3, 9]
wind_direction = [0, 45, 90, 135, 180, 225, 270, 315, 360, 45]

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
            "temperature": None,
            "dewpoint": None,
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
        "temperature": None,
        "wind": {
            "wind_speed": wind_speed,
            "wind_direction": wind_direction
        },
        "humidity": None
    },
    "pressure": pressure
}

data3 = {
    "info": test_info,
    "variables": {
        "temperature": None,
        "wind": None,
        "humidity": {
            "relative_humidity": relative_humidity
        }
    },
    "pressure": pressure
}

data4 = {
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

data5 = {
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

data6 = {
    "info": test_info,
    "variables": {
        "temperature": {
            "temperature": temperature,
            "dewpoint": dewpoint,
            "specific_humidity": specific_humidity
        },
        "wind": {
            "wind_speed": wind_speed,
            "wind_direction": wind_direction
        },
        "humidity": None
    },
    "pressure": pressure
}


data7 = {
    "info": test_info,
    "variables": {
        "temperature": None,
        "wind": {
            "wind_speed": wind_speed,
            "wind_direction": wind_direction
        },
        "humidity": {
            "relative_humidity": relative_humidity
        }
    },
    "pressure": pressure
}

data8 = {
    "info": test_info,
    "variables": {
        "temperature": {
            "temperature": temperature,
            "dewpoint": dewpoint,
            "specific_humidity": specific_humidity
        },
        "wind": {
            "wind_speed": wind_speed,
            "wind_direction": wind_direction
        },
        "humidity": {
            "relative_humidity": relative_humidity
        }
    },
    "pressure": pressure
}

main(construct_data(json.dumps(data1)), "test单图单要素温湿.png")
main(construct_data(json.dumps(data2)), "test单图单要素风力.png")
main(construct_data(json.dumps(data3)), "test单图单要素湿度.png")
main(construct_data(json.dumps(data4)), "test单图多要素温湿.png")
main(construct_data(json.dumps(data5)), "test温湿湿度双图.png")
main(construct_data(json.dumps(data6)), "test温湿风力双图.png")
main(construct_data(json.dumps(data7)), "test风力湿度双图.png")
main(construct_data(json.dumps(data8)), "test全三图.png")