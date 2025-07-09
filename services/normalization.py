import logging

from typing import Any, Dict, Optional
from uuid import uuid4, UUID
from datetime import datetime

from models import StatementData, StatementDetails, DebtDetails, CreditCardDetails
from registry.loader import get_account_registry, get_institution_registry


def get_account_uuid(account_slug: str) -> UUID:
    registry = get_account_registry()
    if account_slug not in registry:
        raise ValueError(f"Unsupported account slug: {account_slug}")
    return UUID(registry[account_slug]["uuid"])


def normalize_statement_data(
    parsed_data: Dict[str, Any],
    account_slug: str,
    file_url: Optional[str] = None,
    uploaded_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    logging.debug(f"Normalizing statement data for account: {account_slug}")
    account_registry = get_account_registry()
    institution_registry = get_institution_registry()

    institution_slug = account_registry[account_slug]["metadata"]["institution"]

    if institution_slug not in institution_registry:
        raise ValueError(f"Unsupported institution slug: {institution_slug}")

    account_uuid = get_account_uuid(account_slug)
    institution_uuid = institution_registry[institution_slug]["uuid"]

    statement_id = uuid4()

    statement_data = StatementData.from_dict(
        data=parsed_data,
        institution_id=institution_uuid,
        account_id=account_uuid,
        file_url=file_url,
        uploaded_at=uploaded_at,
        statement_id=statement_id,
    )

    statement_details = StatementDetails.from_dict(
        data=parsed_data,
        statement_id=statement_id,
    )

    logging.info(f"✅ Statement data normalized for statement_id: {statement_id}")

    return {
        "statement_data": statement_data,
        "statement_details": statement_details,
    }


def normalize_debt_details(
    parsed_data: Dict[str, Any],
    account_slug: str,
    statement_id: UUID,
) -> Dict[str, Any]:
    logging.debug(
        f"Normalizing debt details for account: {account_slug}, statement_id: {statement_id}"
    )

    account_uuid = get_account_uuid(account_slug)

    debt_details = DebtDetails.from_dict(
        data=parsed_data,
        account_id=account_uuid,
        statement_id=statement_id,
    )

    logging.info(f"✅ Debt details normalized for statement_id: {statement_id}")

    return {"debt_details": debt_details}


def normalize_cc_details(
    parsed_data: Dict[str, Any],
    account_slug: str,
    statement_id: UUID,
) -> Dict[str, Any]:
    logging.debug(
        f"Normalizing credit card details for account: {account_slug}, statement_id: {statement_id}"
    )

    account_uuid = get_account_uuid(account_slug)

    cc_details = CreditCardDetails.from_dict(
        data=parsed_data,
        account_id=account_uuid,
        statement_id=statement_id,
    )

    logging.info(f"✅ Credit card details normalized for statement_id: {statement_id}")

    return {"credit_card_details": cc_details}
