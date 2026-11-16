
import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# Tests for annual premium calculation

def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_young_driver():
    assert annual_premium("hatchback", 20, 1, True) == 11500


def test_senior_driver_multiple_claims():
    assert annual_premium("suv", 65, 3, False) == 34000


def test_regular_driver_with_anti_theft():
    assert annual_premium("suv", 40, 2, True) == 14500


def test_invalid_car_type():
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)


def test_underage_driver():
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)


# Tests for no claim bonus

def test_no_claim_free_years():
    assert no_claim_bonus(0) == 0


def test_one_claim_free_year():
    assert no_claim_bonus(1) == 20


def test_three_claim_free_years():
    assert no_claim_bonus(3) == 35


def test_five_claim_free_years():
    assert no_claim_bonus(5) == 50


def test_negative_claim_free_years():
    with pytest.raises(ValueError):
        no_claim_bonus(-1)


# Tests for claim payout

def test_negative_damage_cost():
    with pytest.raises(ValueError):
        claim_payout(-100, 10000, 500, False)


def test_total_loss():
    assert claim_payout(12000, 10000, 1000, True) == 10000


def test_damage_below_deductible():
    assert claim_payout(500, 10000, 1000, False) == 0


def test_normal_claim_payout():
    assert claim_payout(5000, 10000, 1000, False) == 4000


def test_claim_exceeds_insured_value():
    assert claim_payout(15000, 10000, 1000, False) == 10000


# Additional boundary tests for branch coverage

def test_driver_exactly_18():
    assert annual_premium("hatchback", 18, 1, False) == 12000


def test_driver_exactly_25():
    assert annual_premium("hatchback", 25, 1, False) == 8000


def test_driver_exactly_60():
    assert annual_premium("hatchback", 60, 1, False) == 10000


def test_claim_count_boundary():
    assert annual_premium("sedan", 30, 2, False) == 12000
    assert annual_premium("sedan", 30, 3, False) == 24000


def test_bonus_year_boundaries():
    assert no_claim_bonus(2) == 20
    assert no_claim_bonus(4) == 35


def test_damage_equals_deductible():
    assert claim_payout(1000, 10000, 1000, False) == 0


def test_negative_deductible():
    with pytest.raises(ValueError):
        claim_payout(5000, 10000, -100, False)
