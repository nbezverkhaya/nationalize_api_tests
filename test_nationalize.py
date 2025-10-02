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
    params = {"name[]":name}
    r = api_client.get(base_url, params=params)
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(items) == 1
    assert items[0].name == name

    assert isinstance(items[0].country, list)
    for c in items[0].country:
        assert isinstance(c, Country)

def test_multiple_names_batch_ussage_success(api_client, base_url):
    names = ["metthew", "nataliie", "markus"]
    params = {"name[]": names}
    r = api_client.get(base_url, params=params)
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(names) == len(items)
    returned_names = {p.name for p in items}
    for name in names:
        assert name in returned_names

    print(returned_names)

def test_no_name_parameter_negative(api_client, base_url):
    r = api_client.get(base_url)
    assert r.status_code in (400, 422)
    body = r.json()
    assert isinstance(body, dict) and "error" in body