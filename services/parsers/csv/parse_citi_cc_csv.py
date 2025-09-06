import csv
import logging
from datetime import datetime
from typing import Any
from typing import TextIO
from uuid import UUID

from services.normalization import normalize_transactions


logger = logging.getLogger(__name__)


def parse_citi_cc_csv(
    csv_file: TextIO, statement_uuid: UUID, account_slug: str
) -> list[dict[str, Any]]:
    transactions = []
    reader = csv.DictReader(csv_file)

    for row in reader:
        try:
            date_str = row["Date"].strip()
            description = row["Description"].strip()
            debit = row["Debit"].strip()
            credit = row["Credit"].strip()

            # Parse date
            date = datetime.strptime(date_str, "%m/%d/%Y").date()

            # Determine amoutn and type
            if debit:
                amount = -float(debit.replace(",", ""))
                transaction_type = "debit"
            elif credit:
                amount = float(credit.replace(",", ""))
                desc_lower = description.lower()
                if "payment" in desc_lower:
                    transaction_type = "payment"
                elif "redeemed" in desc_lower or "thankyou" in desc_lower:
                    transaction_type = "credit"
                else:
                    transaction_type = "refund"
            else:
                logger.debug(f"Row {row} skipped: no debit or credit found.")
                continue

            transactions.append(
                {
                    "date": date.isoformat(),
                    "amount": amount,
                    "description": description,
                    "custom_description": None,
                    "category": None,
                    "type": transaction_type,
                }
            )

        except (ValueError, IndexError) as e:
            logger.warning(f"⚠️ Skipping row {row} due to error: {e}\nRow: {row}")

    normalized_transactions = normalize_transactions(
        parsed_data=transactions,
        account_slug=account_slug,
        statement_id=statement_uuid,
    )

    logger.info(f"✅ Parsed {len(transactions)} valid transactions from CSV.")
    logger.debug(
        f"Returning {len(normalized_transactions['transactions'])} normalized transactions"
    )
    return [txn.model_dump() for txn in normalized_transactions["transactions"]]
