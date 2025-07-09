from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class CreditCardDetails(BaseModel):
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
        cc_detail_id: Optional[UUID] = None,
    ) -> "CreditCardDetails":
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
