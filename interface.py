from pydantic import BaseModel, Field
import json
from typing import List, Union
from datetime import datetime

class Wind(BaseModel):
    wind_speed: List[float]
    wind_direction: List[float]

class Temperature(BaseModel):
    temperature: Union[List[float], None] = None
    dewpoint: Union[List[float], None] = None
    specific_humidity: Union[List[float], None] = None

class Humidity(BaseModel):
    relative_humidity: Union[List[float], None] = None

class Variables(BaseModel):
    temperature: Union[Temperature, None] = None
    wind: Union[Wind, None] = None
    humidity: Union[Humidity, None] = None

class SampleInfo(BaseModel):
    province: Union[str, None] = None
    location: str
    time: datetime = Field(default_factory=datetime.now)
    latitude: float
    longitude: float
    source: str = Field(default="CMA-GFS")

class Data(BaseModel):
    info: SampleInfo
    variables: Variables
    pressure: List[float]
    show_digit: bool = False

def construct_data(data_json: str) -> Data:
    data = json.loads(data_json)
    if "show_digit" in data:
        show_digit = data["show_digit"]
    else:
        show_digit = False
    return Data(
        info=SampleInfo(**data["info"]),
        variables=Variables(**data["variables"]),
        pressure=data["pressure"],
        show_digit=show_digit
    )