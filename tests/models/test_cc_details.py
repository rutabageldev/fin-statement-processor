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
