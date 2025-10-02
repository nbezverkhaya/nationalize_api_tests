from typing import List, Optional

from pydantic import BaseModel, Field

class Country(BaseModel):
    country_id: str
    probability: float

