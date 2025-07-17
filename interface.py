from pydantic import BaseModel
from typing import List, Union
from datetime import datetime

class Variables(BaseModel):
    temperature: List[float]
    humidity: List[float]
    wind_speed: List[float]
    wind_direction: List[float]
    specific_humidity: List[float]
    relative_humidity: List[float]

class SampleInfo(BaseModel):
    province: Union[str, None]
    location: str
    time: datetime
    latitude: float
    longitude: float
    source: str

class Data(BaseModel):
    info: SampleInfo
    variables: Variables
    pressure: List[float]