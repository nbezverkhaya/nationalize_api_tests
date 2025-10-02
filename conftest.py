import pytest
import requests

BASE_URL = "https://api.nationalize.io"

@pytest.fixture(scope="session")
def api_client() -> requests.Session:
    session = requests.Session()
    yield session
    session.close()

