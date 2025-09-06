import logging
from datetime import datetime
from typing import Any
from uuid import UUID
from uuid import uuid4

from models import CreditCardDetails
from models import DebtDetails
from models import StatementData
from models import StatementDetails
from models import Transaction
from registry.loader import get_account_registry
from registry.loader import get_institution_registry


def get_account_uuid(account_slug: str) -> UUID:
    registry = get_account_registry()
    if account_slug not in registry:
        raise ValueError(f"Unsupported account slug: {account_slug}")
    return UUID(registry[account_slug]["uuid"])


def normalize_statement_data(
    parsed_data: dict[str, Any],
    account_slug: str,
    file_url: str | None = None,
    uploaded_at: datetime | None = None,
) -> dict[str, Any]:
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
    parsed_data: dict[str, Any],
    account_slug: str,
    statement_id: UUID,
) -> dict[str, Any]:
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
    parsed_data: dict[str, Any],
    account_slug: str,
    statement_id: UUID,
) -> dict[str, Any]:
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


def normalize_transactions(
    parsed_data: list[dict[str, Any]],
    account_slug: str,
    statement_id: UUID,
) -> dict[str, list[Transaction]]:
    logging.debug(
        f"Normalizing transactions for account: {account_slug}, statement_id: {statement_id}"
    )

    account_uuid = get_account_uuid(account_slug)

    transactions = []

    for transaction_data in parsed_data:
        try:
            transaction = Transaction.from_dict(
                data=transaction_data,
                account_id=account_uuid,
                statement_id=statement_id,
            )
            transactions.append(transaction)
        except (ValueError, KeyError, TypeError) as e:
            logging.warning(
                f"❌ Skipping invalid transaction row: {transaction_data} — Reason: {e}"
            )

    logging.info(
        f"✅ {len(transactions)} transactions normalized for statement_id: {statement_id}"
    )

    return {"transactions": transactions}
