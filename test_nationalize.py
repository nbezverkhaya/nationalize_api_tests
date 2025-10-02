import pytest
from pydantic import ValidationError
from models import NationalityResponse, NationalityPrediction, Country

def _validate_response(data) -> list[NationalityPrediction]:
    try:
        vr = NationalityResponse.model_validate(data)
    except ValidationError as e:
        pytest.fail(f"Pydentic validation failed: {e}")
    return vr.root
