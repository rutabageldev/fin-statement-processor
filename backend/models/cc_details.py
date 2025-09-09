"""Credit card specific detail models."""

from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class CreditCardDetails(BaseModel):
    """Credit card specific details from statements.

    Contains credit limit, available credit, points, and other
    credit card specific information.
    """

    id: UUID
    account_id: UUID
    statement_id: UUID
    credit_limit: float
    available_credit: float
    points_earned: int
    points_redeemed: int
    cash_advances: float
    fees: float
    purchases: float
    credits: float

    @classmethod
    def from_dict(
        cls,
        data: dict[str, object],
        account_id: UUID,
        statement_id: UUID,
        cc_detail_id: UUID | None = None,
    ) -> "CreditCardDetails":
        """Create CreditCardDetails from parsed credit card data.

        Args:
            data: Parsed statement data containing credit card details
            account_id: UUID of the account
            statement_id: UUID of the associated statement
            cc_detail_id: Optional UUID for the details (generates new if None)

        Returns:
            CreditCardDetails instance with credit card data
        """
        return cls(
            id=cc_detail_id or uuid4(),
            account_id=account_id,
            statement_id=statement_id,
            credit_limit=float(data["credit_limit"]),  # type: ignore[arg-type]
            available_credit=float(data["available_credit"]),  # type: ignore[arg-type]
            points_earned=int(data["points_earned"])  # type: ignore[call-overload]
            if data["points_earned"] is not None
            else 0,
            points_redeemed=int(data["points_redeemed"])  # type: ignore[call-overload]
            if data["points_redeemed"] is not None
            else 0,
            cash_advances=float(data["cash_advances"]),  # type: ignore[arg-type]
            fees=float(data["fees"]),  # type: ignore[arg-type]
            purchases=float(data["purchases"]),  # type: ignore[arg-type]
            credits=float(data["credits"]),  # type: ignore[arg-type]
        )
