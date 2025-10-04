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

- test_single_name_batch_usage_success → verifies a single name[] returns a valid response.
- test_multiple_names_batch_usage_success → verifies multiple names (≤10).
- test_no_name_parameter_negative → verifies behavior when name[] is missing.
- test_empty_name_parameter_edge → verifies empty name[] returns 200 with a well-formed item (echo "", structure valid).
- test_edge_names_are_handled → parametrized: special chars, digits, spaces, emoji, very long; expects 200 + valid structure + echo.
- test_max_names_batch_usage → verifies request with 10 names.
- test_exceed_max_names_batch_usage → 15 names: expects 422

## Future Enhancements
- Verify if `country` results are sorted by probability (descending). ?
- Check how the API handles repeated names in a single batch (returns duplicates or deduplicates) +
- час виконання заппрса
- Mock and test rate limit behavior (e.g., 100 names/day quota).

## Open Questions / Documentation Gaps

During testing, one gap in the official documentation of the **Batch Usage** endpoint was identified:

- The docs state: *“The API allows you to infer the nationality of up to ten names per request.”*
  However, it is not clearly specified what should happen if more than 10 names are provided:
- Option A: The API rejects the request with a `422 Unprocessable Content`.
- Option B: The API silently processes only the first 10 names and returns a `200 OK` with truncated results.

### Current Handling in Tests
Our test suite accepts both behaviors:
- If the API returns `422`, the test considers it valid.
- If the API returns `200 OK`, the test verifies that no more than 10 results are included in the response.

This dual-handling ensures that the test suite remains robust against both possible implementations until the API behavior is clarified.

### Recommendation
It would be beneficial to clarify this behavior in the official API documentation, so that test cases and client applications can rely on a well-defined contract.
