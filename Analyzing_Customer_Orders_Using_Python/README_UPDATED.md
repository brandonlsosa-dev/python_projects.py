# Analyzing Customer Orders Using Python

A compact example demonstrating simple analysis of customer orders in Python.
The project provides small, testable functions to compute per-customer spending,
classify customers by spend, and aggregate revenue by product category.

Features
- Compute total spent per customer and classify customers by spend level.
- Aggregate revenue per product category.
- Find unique products and list customers by category.
- Small, importable functions with unit tests.

Prerequisites
- Python 3.8+ recommended.
- (Optional) `pytest` for running tests (listed in `requirements.txt`).

Quickstart (Windows PowerShell)

1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install test dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the demonstration script:

```powershell
python analyze_customer_orders.py
```

4. Run the unit tests with `pytest`:

```powershell
pytest -q
```

Files
- `analyze_customer_orders.py` — Main analysis functions and `main()` demo.
- `tests/test_analyze_orders.py` — Unit tests for key behaviors.
- `requirements.txt` — Test dependency (`pytest`).

Usage / Examples

Import and call functions from `analyze_customer_orders.py` in your own code:

```python
from analyze_customer_orders import analyze_orders, category_revenue

analysis, spending, categories, orders_by_customer, product_map = analyze_orders(ORDER_DETAILS)
print(category_revenue(ORDER_DETAILS))
```

Extending
- Replace the `ORDER_DETAILS` list with data loaded from CSV or a database.
- Add command-line arguments (using `argparse`) to accept input files and
  output formats (CSV/JSON).

Testing
- Tests are located in `tests/` and use `pytest`.
- Run `pytest -q` to execute the test suite.

License & Attribution
This repository contains example code; add a license file if you plan to reuse
or publish it.

---

If you want, I can also:
- Add CSV input support and a small CLI.
- Improve classification thresholds or make them configurable.
