import pytest
from pydantic import ValidationError
from models import NationalityResponse, NationalityPrediction, Country

def _validate_response(data) -> list[NationalityPrediction]:
    try:
        vr = NationalityResponse.model_validate(data)
    except ValidationError as e:
        pytest.fail(f"Pydentic validation failed: {e}")
    return vr.root

def test_single_name_batch_usage_success(api_client, base_url):
    name = "Jonas"
    params = {"name[]":name}
    r = api_client.get(base_url, params=params)
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(items) == 1
    assert items[0].name == name

    assert isinstance(items[0].country, list)
    for c in items[0].country:
        assert isinstance(c, Country)

@pytest.mark.parametrize("names", [
    ["Theo", "matthew", "jane"],
    ["José", "Chloë", "Zoë"],
    ["Наталія", "Олександр", "Андрій"],
    ["李", "王伟", "张伟"],
])
def test_multiple_names_batch_usage_success(api_client, base_url, names):
    params = {"name[]": names}
    r = api_client.get(base_url, params=params)
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(names) == len(items)
    returned_names = {p.name for p in items}
    for name in names:
        assert name in returned_names

def test_no_name_parameter_negative(api_client, base_url):
    r = api_client.get(base_url)
    assert r.status_code == 422
    body = r.json()
    assert isinstance(body, dict) and "error" in body

def test_empty_name_parameter_edge(api_client, base_url):
    r = api_client.get(base_url, params={"name[]": ""})
    assert r.status_code == 200
    items = _validate_response(r.json())
    assert len(items) == 1
    assert items[0].name == ""

@pytest.mark.parametrize("name", [
    "john$doe!",
    "name123",
    "spaces are ok",
    "emoji🙂",
    "very-very-long-" + "a"*80,
])
def test_edge_names_are_handled(api_client, base_url, name):
    r = api_client.get(base_url, params={"name[]": name})
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(items) == 1
    assert items[0].name == name
    assert isinstance(items[0].country, list)

def test_max_names_batch_usage(api_client, base_url):
    names = [f"name{i}" for i in range(1, 11)]
    r = api_client.get(base_url, params={"name[]": names})
    assert r.status_code == 200
    items = _validate_response(r.json())
    assert len(items) == 10

def test_exceed_max_names_batch_usage(api_client, base_url):
    all_names = [f"name{i}" for i in range(1, 15)]
    r = api_client.get(base_url, params={"name[]": all_names})

    if r.status_code == 422:
        return

    assert r.status_code == 200
    items = _validate_response(r.json())
    assert len(items) <= 10