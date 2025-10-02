from typing import List, Optional

from pydantic import BaseModel, RootModel, constr, confloat

class Country(BaseModel):
    country_id: constr(min_length=2, max_length=2)
    probability: confloat(ge=0.0, le=1.0)

class NationalityPrediction(BaseModel):
    count: int
    name:str
    country: List[Country]

class NationalityResponse(RootModel[List[NationalityPrediction]]):
    pass