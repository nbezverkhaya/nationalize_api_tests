# Nationalize.io API Tests

## Description
This project contains **automated API tests** for [Nationalize.io](https://nationalize.io/documentation), a service that predicts nationality based on a given name.

The focus is on the **Batch Usage** endpoint (`GET https://api.nationalize.io?name[]=...`).

## Test Scenarios

| #  | Test Name                                | Description                                                                 | Expected Result                                  | Notes / Docs Coverage               |
|----|------------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------|-------------------------------------|
| 1  | `test_single_name_in_batch_success`      | Single name in batch request.                                               | Response contains exactly 1 prediction for name. | Covered in docs (Batch Usage).      |
| 2  | `test_no_name_parameter_negative`        | No `name[]` parameter.                                                      | Returns `422` with error message.               | Covered in docs.                     |
| 3  | `test_empty_name_parameter_success`      | Empty name in batch.                                                        | Returns valid schema with empty string name.    | Docs unclear, behavior observed.     |
| 4  | `test_max_names_batch_success`           | Batch with exactly 10 names.                                                | Returns results for all 10 names.               | Covered in docs (Batch Usage).      |
| 5  | `test_exceed_max_names_batch_negative`   | Batch with more than 10 names (e.g. 15).                                    | Either `422` error or ≤10 names processed.      | **Docs missing, xfail for discussion**. |
| 6  | `test_duplicate_names_remain_in_batch_success` | Batch with duplicate names.                                           | Either duplicates preserved or deduped.         | **Docs missing, xfail for discussion**. |
| 7  | `test_country_probabilities_sorted`      | Verify if `country` list is sorted by `probability` (descending).           | Countries sorted in descending probability.     | **Docs missing, xfail for discussion**. |

---

## Future Enhancements

   **Mock and test rate limit behavior**
   For example, 100 names/day quota → sending a batch after exceeding should return `429 Too Many Requests`.
   Cannot be tested reliably now without isolated environment / API key.

---

## Project Structure

├── .gitignore

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