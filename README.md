# Smart Expense Tracker API

REST API to track personal expenses — add expenses, retrieve all of them, filter by category, calculate sums (overall and per category),
and delete. Made with FastAPI; in-memory storage is used.


## What I built

- `POST /expenses` – add an expense (title, amount, category, date)
- `GET /expenses` – get all expenses
- `GET /expenses?category=food` – filter expenses by category (parameter in URL, not a new endpoint — filtration is a variation of "get all", not a new resource)
- `GET /expenses/total` – total amount of all expenses
- `GET /expenses/total?category=food` – total amount for one category
- `DELETE /expenses/{id}` – delete an expense (returns 404 if such id doesn't exist)
- Validation of input data using Pydantic: amount must be positive, title/category cannot be an empty string, date must be valid
- API documentation auto-generated at `/docs` and `/redoc` endpoints (Swagger UI)

All the data is stored in memory (as a Python dict where
expense id is used as a key). So all the data is erased
on server restart. Database was not necessary for this task,
so in-memory storage simplified the implementation.

### Install

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Start server

```bash
uvicorn src.main:app --reload
```

Your API is now up and running on `http://localhost:8000`.
docs: `http://localhost:8000/docs`

### Running the tests(open another terminal while server is running)

```bash
pytest tests/ -v
```
Your terminal will output something like that,
All 6 tests should pass.

## Example usage

```bash

# Add an expense
Invoke-RestMethod -Uri "http://localhost:8000/expenses" -Method Post -ContentType "application/json" -Body '{"title":"Groceries","amount":45.50,"category":"food","date":"2026-08-01"}'

# List all expenses
Invoke-RestMethod -Uri "http://localhost:8000/expenses" -Method Get

# Filter by category
Invoke-RestMethod -Uri "http://localhost:8000/expenses?category=food" -Method Get

# Total overall
Invoke-RestMethod -Uri "http://localhost:8000/expenses/total" -Method Get

# Total for one category
Invoke-RestMethod -Uri "http://localhost:8000/expenses/total?category=food" -Method Get

# Delete an expense
Invoke-RestMethod -Uri "http://localhost:8000/expenses/<id>" -Method Delete

```

## Project Structure

```
expense-tracker-api/
  README.md
  AI_NOTES.md
  requirements.txt
  pytest.ini
  src/
    __init__.py
    main.py       # FastAPI app + endpoints
    models.py     # Pydantic data models
    storage.py    # in-memory data store
  tests/
    test_expenses.py
```
  ## Design notes 

- IDs are UUIDs, not auto-incrementing integers — prevents id conflicts
  should expenses be ever added simultaneously, and does not expose the number
  of expenses that have ever been created.
- The storage uses a dict mapped by ID, not a list — deletes and  
  searches
  will be O(1) rather than scanning through all expenses.
- Filters and total amount per category are query parameters on
  existing
  routes, not additional routes — this follows REST principles (filtering the
  list is still the "list resource", not a different resource).
