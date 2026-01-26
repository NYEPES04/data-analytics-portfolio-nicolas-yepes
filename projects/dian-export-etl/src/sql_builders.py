# src/sql_builders.py
from __future__ import annotations

def build_cast_select(schema: dict[str, str], src_alias: str = "g") -> str:
    """
    Builds a SQL SELECT fragment that applies explicit CASTs
    to each column defined in the provided schema.

    Notes:
    - Numeric types use TRY_CAST to prevent query failures due to invalid values.
    - Non-numeric types use CAST to preserve values as-is.
    - The output is intended to be embedded directly into a larger SQL query.
    """
    lines: list[str] = []

    for col, typ in schema.items():
        if typ.upper() in {"DOUBLE", "INTEGER", "BIGINT", "DECIMAL"}:
            # Notes: TRY_CAST avoids failing on malformed numeric values
            lines.append(f"TRY_CAST({src_alias}.{col} AS {typ}) AS {col}")
        else:
            # Notes: Regular CAST is safe for categorical/text fields
            lines.append(f"CAST({src_alias}.{col} AS {typ}) AS {col}")

    # Notes: Joined with commas and line breaks for readable SQL generation
    return ",\n      ".join(lines)
