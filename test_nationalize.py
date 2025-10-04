import pytest
from pydantic import ValidationError
from models import NationalityResponse, NationalityPrediction

def _validate_response(data) -> list[NationalityPrediction]:
    try:
        vr = NationalityResponse.model_validate(data)
    except ValidationError as e:
        pytest.fail(f"Pydentic validation failed: {e}")
    return vr.root


def test_single_name_in_batch_success(api_client, base_url):
    name = "Jonas"
    params = {"name[]":name}
    r = api_client.get(base_url, params=params)
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(items) == 1
    assert items[0].name == name

    assert "application/json" in r.headers.get("Content-Type", "")


def test_no_name_parameter_negative(api_client, base_url):
    r = api_client.get(base_url)
    assert r.status_code == 422

    body = r.json()
    assert isinstance(body, dict) and "error" in body


def test_empty_name_parameter_success(api_client, base_url):
    r = api_client.get(base_url, params={"name[]": ""})
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(items) == 1
    assert items[0].name == ""


@pytest.mark.xfail(reason="Docs don’t specify deduplication in batch; this test encodes a proposed behavior.")
def test_duplicate_names_remain_in_batch_success(api_client, base_url):
    names = ["anna", "anna", "bob"]
    r = api_client.get(base_url, params={"name[]": names})
    assert r.status_code == 200

    items = _validate_response(r.json())
    returned_names = [it.name for it in items]

    assert len(items) == len(names)
    assert returned_names.count("anna") == 2


def test_max_names_batch_success(api_client, base_url):
    names = [f"name{i}" for i in range(1, 11)]
    r = api_client.get(base_url, params={"name[]": names})
    assert r.status_code == 200

    items = _validate_response(r.json())
    assert len(items) == len(names)

    returned_names = {it.name for it in items}
    assert returned_names == set(names)


@pytest.mark.xfail(reason="API docs do not clarify behavior for >10 names in a batch;"
                          "this test assumes server should reject or truncate input.")
def test_exceed_max_names_batch_negative(api_client, base_url):
    names = [f"name{i}" for i in range(1, 15)]
    r = api_client.get(base_url, params={"name[]": names})

    if r.status_code == 422:
        return

    assert r.status_code == 200
    items = _validate_response(r.json())
    assert len(items) <= 10