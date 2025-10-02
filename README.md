# Nationalize.io API Tests

## Description
This project contains **automated API tests** for [Nationalize.io](https://nationalize.io/documentation), a service that predicts nationality based on a given name.

The focus is on the **Batch Usage** endpoint (`GET https://api.nationalize.io?name[]=...`).

The tests cover:
- Positive scenarios (single name, multiple names, country_id)
- Negative scenarios (missing parameter, more than 10 names)
- Edge cases (empty name, special characters, digits, long name, exactly 10 names)

---

## Project Structure
├── conftest.py # Pytest fixtures (api_client, base_url)
├── models.py # Pydantic models for API response validation
├── test_nationalize.py # Main test suite
├── requirements.txt # Dependencies list
└── README.md # This file


---

## Requirements
- Python 3.9+
- requests
- pytest
- pydantic

---

## Setup & Run
1. Clone the repository and navigate into the project:
   ```bash
   git clone ...
   cd nationalize_api_tests

2. Create and activate a virtual environment:
   ```bash
    python -m venv .venv
    source .venv/bin/activate   # Linux / macOS
    .venv\Scripts\activate      # Windows

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Run the tests:
    ```bash
    pytest -v

---

## Scenarios

test_single_name_batch_usage_success → verifies a single name[] returns a valid response.
test_multiple_names_batch_usage_success → verifies multiple names (≤10).
test_no_name_parameter_negative → verifies behavior when name[] is missing.
test_exceed_max_names_batch_usage → verifies request with 15 names (should return ≤10 or an error).
test_long_name_edge → verifies very long name returns a valid response with count=0.

## Future Enhancements
- Verify if `country` results are sorted by probability (descending).
- Add Unicode names (Cyrillic, Chinese) to expand test coverage.
- Mock and test rate limit behavior (e.g., 100 names/day quota).
