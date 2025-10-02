import pytest
from pydantic import ValidationError
from models import NationalityResponse, NationalityPrediction, Country

def _validate_response(data) -> list[NationalityPrediction]:
    try:
        vr = NationalityResponse.model_validate(data)
    except ValidationError as e:
        pytest.fail(f"Pydentic validation failed: {e}")
    return vr.root

def test_single_name_batch_ussage_success(api_client, base_url):
    name = "michael"
    params = {"name":name}
    r = api_client.get(base_url, params=params)
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(items) == 1
    assert items[0].name == name

    assert isinstance(items[0].country, list)
    for c in items[0].country:
        assert isinstance(c, Country)
