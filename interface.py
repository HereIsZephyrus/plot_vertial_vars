from pydantic import BaseModel, Field
from typing import List, Union
from datetime import datetime

class Wind(BaseModel):
    speed: List[float]
    direction: List[float]

class Variables(BaseModel):
    temperature: Union[List[float], None] = None
    dewpoint: Union[List[float], None] = None
    wind: Union[Wind, None] = None
    specific_humidity: Union[List[float], None] = None
    relative_humidity: Union[List[float], None] = None

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