from typing import List
from pydantic import BaseModel, RootModel, constr, confloat, Field

class Country(BaseModel):
    country_id: constr(min_length=2, max_length=2, pattern="^[A-Za-z]{2}$")
    probability: confloat(ge=0.0, le=1.0)

class NationalityPrediction(BaseModel):
    count: int
    name: str
    country: List[Country] = Field(default_factory=list, min_length=0, max_length=5)

class NationalityResponse(RootModel[list[NationalityPrediction]]):
    pass