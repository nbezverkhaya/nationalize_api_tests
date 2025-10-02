from typing import List, Optional

from pydantic import BaseModel, Field

class Country(BaseModel):
    country_id: str
    probability: float

class NationalityPrediction(BaseModel):
    count: int
    name:str
    country: List[Country]

class NationalityResponse(BaseModel):
    __root__: List[NationalityPrediction]
    def __iter__(self):
        return iter(self.__root__)
    def __getitem__(self, item):
        return self.__root__[item]
    def __len__(self):
        return len(self.__root__)