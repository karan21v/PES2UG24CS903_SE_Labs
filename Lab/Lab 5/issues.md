# Lab 5 - Static Analysis: Issues and Fixes

**Program:** Car Rental System  
**Original script:** `car_rental_original.py`  
**Corrected script:** `car_rental.py` (copied from the completed `car_rental_final.py`)

The line references below are from the original script. Findings are based on the original Pylint, Bandit and Flake8 reports and the corrected code.

| Issue | Type / tool | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| SQL injection in customer registration | Security / Bandit B608 | 23 | SQL inserted untrusted values through string formatting. | Use SQLite parameter placeholders (`?`) and parameter tuples. |
| SQL injection in customer lookup | Security / Bandit B608 | 26-27 | User-controlled name was concatenated into SQL. | Use a parameterized `SELECT` statement. |
| Executing a user-supplied promotion rule | Security / Pylint W0122, Bandit | 50-54 | `exec()` could evaluate arbitrary Python code. | Replace it with strict pattern matching and numeric multiplication. |
| Insecure temporary receipt handling | Security / Bandit | 62-68 | Predictable temporary filename and world-writable (`0777`) file. | Use `NamedTemporaryFile` and restricted permissions (`0600`). |
| Weak hashing of driving-licence data | Security / Bandit | 47-48 | SHA-1 is considered cryptographically weak. | Use SHA-256. |
| Weak randomness for booking codes | Security / Bandit B311 | 44-45 | `random.randint()` is not a secure random generator. | Use `secrets.randbelow()`. |
| Mutable default list | Correctness / Pylint W0102 | 16 | `features=[]` shares state across calls. | Default to `None` and construct a fresh list inside the function. |
| Bare exception handling | Correctness / Pylint W0702, Flake8 E722 | 36-42 | Catch-all `except` silently suppressed errors. | Check whether the vehicle exists and handle the expected case explicitly. |
| Hard-coded administrator password | Security / Bandit | 70-73 | Admin secret was embedded in code. | Load it from an environment variable and compare it safely. |
| Formatting and naming violations | Style / Pylint, Flake8 | Various | CamelCase functions, missing docstrings, unused imports, and excessive line lengths. | Use snake_case, add docstrings, remove unused imports, and follow formatting conventions. |

## Verification against saved reports

- **Pylint (after):** 10.00/10.
- **Bandit (after):** No issues identified; no high, medium or low findings.
- **Flake8 (after):** Empty output, indicating no reported violations for that run.

The corrected program also includes changes beyond the minimum four issues required in the lab handout.
