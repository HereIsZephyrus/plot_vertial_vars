from pydantic import BaseModel, Field
from typing import List, Union
from datetime import datetime

class Wind(BaseModel):
    wind_speed: List[float]
    wind_direction: List[float]

class Normal(BaseModel):
    temperature: Union[List[float], None] = None
    dewpoint: Union[List[float], None] = None
    specific_humidity: Union[List[float], None] = None

class Humidity(BaseModel):
    relative_humidity: List[float]

class Variables(BaseModel):
    normal: Union[Normal, None] = None
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