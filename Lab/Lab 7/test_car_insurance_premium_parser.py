"""Lab 7: Hypothesis fuzz tests and input-validation checks.

Matches the nine test categories shown in the original Lab 7 report.
"""

import pytest
from hypothesis import given, strategies as st

from car_insurance_premium_parser import (
    normalize_registration,
    total_claim_amount,
    driver_age,
)


@given(st.text() | st.none())
def test_normalize_registration_no_crash(s):
    try:
        normalize_registration(s)
    except Exception as exc:
        pytest.fail(f"Registration parser crashed for {s!r}: {exc}")


@given(st.text() | st.none())
def test_total_claim_amount_no_crash(s):
    try:
        total_claim_amount(s)
    except Exception as exc:
        pytest.fail(f"Claim amount parser crashed for {s!r}: {exc}")


@given(st.text() | st.none())
def test_driver_age_no_crash(s):
    try:
        driver_age(s)
    except Exception as exc:
        pytest.fail(f"Date of birth parser crashed for {s!r}: {exc}")


def test_valid_registration_normalize():
    assert normalize_registration("ka 01 ab 1234") == "KA01AB1234"
    assert normalize_registration("ka-01.ab.1234") == "KA01AB1234"


def test_invalid_registration():
    assert normalize_registration(None) == ""
    assert normalize_registration("KA01@AB1234") == ""


def test_valid_claim_amounts():
    assert total_claim_amount("12000;4500;800") == 17300
    assert total_claim_amount("0; 10 ;20") == 30


def test_invalid_claim_amounts():
    assert total_claim_amount(None) is None
    assert total_claim_amount("") is None
    assert total_claim_amount("100;invalid;200") is None
    assert total_claim_amount("100;-5") is None


def test_valid_driver_age():
    assert driver_age("14/08/1999") == 27
    assert driver_age("01/01/2000", current_year=2026) == 26


def test_invalid_driver_age():
    assert driver_age(None) is None
    assert driver_age("31/02/1999") is None
    assert driver_age("01/01/2030") is None
