from typing import Any, Dict, Optional
from uuid import uuid4, UUID
from datetime import datetime

from models.statement import StatementData, StatementDetails
from registry.loader import get_account_registry, get_institution_registry


def normalize_statement_data(
    parsed_data: Dict[str, Any],
    account_slug: str,
    file_url: Optional[str] = None,
    uploaded_at: Optional[datetime] = None,
) -> Dict[str, Any]:
    account_registry = get_account_registry()
    institution_registry = get_institution_registry()

    if account_slug not in account_registry:
        raise ValueError(f"Unsupported account slug: {account_slug}")

    account_info = account_registry[account_slug]
    institution_slug = account_registry[account_slug]["metadata"]["institution"]

    if institution_slug not in institution_registry:
        raise ValueError(f"Unsupported institution slug: {institution_slug}")

    account_uuid = account_info["uuid"]
    institution_uuid = institution_registry[institution_slug]["uuid"]

    statement_id = uuid4()

    statement_data = StatementData.from_dict(
        data=parsed_data,
        institution_id=UUID(institution_uuid),
        account_id=UUID(account_uuid),
        file_url=file_url,
        uploaded_at=uploaded_at,
        statement_id=statement_id,
    )

    statement_details = StatementDetails.from_dict(
        data=parsed_data,
        statement_id=statement_id,
    )

    return {
        "statement_data": statement_data,
        "statement_details": statement_details,
    }
