import csv
from datetime import datetime
from typing import Any, Dict, List, TextIO


def parse_citi_cc_csv(csv_file: TextIO) -> List[Dict[str, Any]]:
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
                continue  # skip rows with no amount

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

        except Exception as e:
            print(f"⚠️ Skipping row due to error: {e}\nRow: {row}")

    return transactions
