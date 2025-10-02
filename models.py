from typing import List, Optional

from pydantic import BaseModel, Field

class Country(BaseModel):
    country_id: str
    probability: float

class NationalityPrediction(BaseModel):
    count: int
    name:str
    country: List[Country]

