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
        data: dict,
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
            credit_limit=float(data["credit_limit"]),
            available_credit=float(data["available_credit"]),
            points_earned=int(data["points_earned"]),
            points_redeemed=int(data["points_redeemed"]),
            cash_advances=float(data["cash_advances"]),
            fees=float(data["fees"]),
            purchases=float(data["purchases"]),
            credits=float(data["credits"]),
        )
