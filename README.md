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
test_empty_name_parameter_edge → verifies empty name[] returns 200 with a well-formed item (echo "", structure valid).
test_edge_names_are_handled → parametrized: special chars, digits, spaces, emoji, very long; expects 200 + valid structure + echo.
test_max_names_batch_usage → verifies request with 10 names.
test_exceed_max_names_batch_usage → 15 names: expects either 4xx

## Future Enhancements
- Verify if `country` results are sorted by probability (descending).
- Ensure that the API returns results in the same order as the names were requested.
- Check how the API handles repeated names in a single batch (returns duplicates or deduplicates)
- Mock and test rate limit behavior (e.g., 100 names/day quota).