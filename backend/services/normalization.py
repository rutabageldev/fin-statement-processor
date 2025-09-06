"""Core business logic for normalizing financial statement data."""

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


logger = logging.getLogger(__name__)


def get_account_uuid(account_slug: str) -> UUID:
    """Get the UUID for an account by its slug.

    Args:
        account_slug: The account identifier (e.g., 'citi_cc')

    Returns:
        UUID of the account

    Raises:
        ValueError: If account_slug is not found in registry
    """
    registry = get_account_registry()
    if account_slug not in registry:
        error_msg = f"Unsupported account slug: {account_slug}"
        raise ValueError(error_msg)
    return UUID(registry[account_slug]["uuid"])


def normalize_statement_data(
    parsed_data: dict[str, Any],
    account_slug: str,
    file_url: str | None = None,
    uploaded_at: datetime | None = None,
) -> dict[str, Any]:
    """Normalize parsed statement data into structured models.

    Args:
        parsed_data: Raw parsed data from statement
        account_slug: Account identifier
        file_url: Optional URL to source file
        uploaded_at: Optional upload timestamp

    Returns:
        Dict containing StatementData and StatementDetails instances

    Raises:
        ValueError: If account or institution not found in registry
    """
    logger.debug("Normalizing statement data for account: %s", account_slug)
    account_registry = get_account_registry()
    institution_registry = get_institution_registry()

    institution_slug = account_registry[account_slug]["metadata"]["institution"]

    if institution_slug not in institution_registry:
        error_msg = f"Unsupported institution slug: {institution_slug}"
        raise ValueError(error_msg)

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

    logger.info("✅ Statement data normalized for statement_id: %s", statement_id)

    return {
        "statement_data": statement_data,
        "statement_details": statement_details,
    }


def normalize_debt_details(
    parsed_data: dict[str, Any],
    account_slug: str,
    statement_id: UUID,
) -> dict[str, Any]:
    """Normalize debt-related data from statement.

    Args:
        parsed_data: Raw parsed data containing debt information
        account_slug: Account identifier
        statement_id: UUID of the associated statement

    Returns:
        Dict containing DebtDetails instance
    """
    logger.debug(
        "Normalizing debt details for account: %s, statement_id: %s",
        account_slug,
        statement_id,
    )

    account_uuid = get_account_uuid(account_slug)

    debt_details = DebtDetails.from_dict(
        data=parsed_data,
        account_id=account_uuid,
        statement_id=statement_id,
    )

    logger.info("✅ Debt details normalized for statement_id: %s", statement_id)

    return {"debt_details": debt_details}


def normalize_cc_details(
    parsed_data: dict[str, Any],
    account_slug: str,
    statement_id: UUID,
) -> dict[str, Any]:
    """Normalize credit card specific data from statement.

    Args:
        parsed_data: Raw parsed data containing credit card information
        account_slug: Account identifier
        statement_id: UUID of the associated statement

    Returns:
        Dict containing CreditCardDetails instance
    """
    logger.debug(
        "Normalizing credit card details for account: %s, statement_id: %s",
        account_slug,
        statement_id,
    )

    account_uuid = get_account_uuid(account_slug)

    cc_details = CreditCardDetails.from_dict(
        data=parsed_data,
        account_id=account_uuid,
        statement_id=statement_id,
    )

    logger.info("✅ Credit card details normalized for statement_id: %s", statement_id)

    return {"credit_card_details": cc_details}


def normalize_transactions(
    parsed_data: list[dict[str, Any]],
    account_slug: str,
    statement_id: UUID,
) -> dict[str, list[Transaction]]:
    """Normalize transaction data from statement.

    Args:
        parsed_data: List of raw transaction data
        account_slug: Account identifier
        statement_id: UUID of the associated statement

    Returns:
        Dict containing list of Transaction instances
    """
    logger.debug(
        "Normalizing transactions for account: %s, statement_id: %s",
        account_slug,
        statement_id,
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
            logger.warning(
                "❌ Skipping invalid transaction row: %s — Reason: %s",
                transaction_data,
                e,
            )

    logger.info(
        "✅ %s transactions normalized for statement_id: %s",
        len(transactions),
        statement_id,
    )

    return {"transactions": transactions}
