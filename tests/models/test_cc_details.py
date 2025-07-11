import pytest
from uuid import uuid4
from models import CreditCardDetails


def test_credit_card_details_missing_required_field():
    data = {
        "available_credit": 4200.00,
        "points_earned": 500,
        "points_redeemed": 200,
        "cash_advances": 0.0,
        "fees": 0.0,
        "purchases": 250.0,
        "credits": 0.0,
    }

    with pytest.raises(KeyError, match="credit_limit"):
        CreditCardDetails.from_dict(
            data=data,
            account_id=uuid4(),
            statement_id=uuid4(),
        )


def test_credit_card_details_invalid_points_earned_type():
    data = {
        "credit_limit": 5000.0,
        "available_credit": 4200.00,
        "points_earned": "five hundred",
        "points_redeemed": 200,
        "cash_advances": 0.0,
        "fees": 0.0,
        "purchases": 250.0,
        "credits": 0.0,
    }

    with pytest.raises(ValueError):
        CreditCardDetails.from_dict(
            data=data,
            account_id=uuid4(),
            statement_id=uuid4(),
        )


def test_cc_details_optional_id():
    data = {
        "credit_limit": 5000.0,
        "available_credit": 4240.0,
        "points_earned": 500,
        "points_redeemed": 200,
        "cash_advances": 0.0,
        "fees": 0.0,
        "purchases": 250.0,
        "credits": 0.0,
    }

    obj = CreditCardDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert isinstance(obj.id, uuid4().__class__)


def test_cc_details_non_numeric_field_raises():
    data = {
        "credit_limit": "FIVE THOUSAND",
        "available_credit": 4240.0,
        "points_earned": 500,
        "points_redeemed": 200,
        "cash_advances": 0.0,
        "fees": 0.0,
        "purchases": 250.0,
        "credits": 0.0,
    }

    with pytest.raises(ValueError):
        CreditCardDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())


def test_cc_details_negative_rewards_values():
    data = {
        "credit_limit": 5000.0,
        "available_credit": 4240.0,
        "points_earned": -100,
        "points_redeemed": -50,
        "cash_advances": 0.0,
        "fees": 0.0,
        "purchases": 250.0,
        "credits": 0.0,
    }

    obj = CreditCardDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert obj.points_earned == -100
    assert obj.points_redeemed == -50


def test_cc_details_float_precision_edge_case():
    data = {
        "credit_limit": "5000.999999",
        "available_credit": "4240.000001",
        "points_earned": "500",
        "points_redeemed": "200",
        "cash_advances": "0.0",
        "fees": "0.0",
        "purchases": "250.0",
        "credits": "0.0",
    }

    obj = CreditCardDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert round(obj.credit_limit, 2) == 5001.00
    assert round(obj.available_credit, 2) == 4240.00
