from typing import Literal
from citi_cc_parser import parse as parse_citi_cc

# from ms_checking_parser import parse as parse_ms_checking

# Explicit list of supported statement types
StatementType = Literal["CITI_CC"]


def route_to_parser(file_bytes: bytes, statement_type: StatementType) -> dict:
    if statement_type == "CITI_CC":
        return parse_citi_cc(file_bytes)

    raise ValueError(f"Unsupported statement type: {statement_type}")
