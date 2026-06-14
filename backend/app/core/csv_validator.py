"""CSV parsing, validation, and quality scoring.

Turns an uploaded CSV into: a typed column manifest, a row-level payload list,
a quality score (0-100), and human-readable warnings. Hard failures raise
ValidationFailed with the documented details payload.
"""
from io import BytesIO

import pandas as pd

from app.core.errors import ValidationFailed


def _is_textual(series: pd.Series) -> bool:
    """True for object/string columns (pandas 2.2 may infer 'str', not object)."""
    return not (
        pd.api.types.is_numeric_dtype(series)
        or pd.api.types.is_datetime64_any_dtype(series)
        or pd.api.types.is_bool_dtype(series)
    )


def _dtype_name(series: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"
    if pd.api.types.is_integer_dtype(series):
        return "integer"
    if pd.api.types.is_float_dtype(series):
        return "float"
    if pd.api.types.is_bool_dtype(series):
        return "bool"
    return "string"


def parse_and_validate(raw: bytes) -> dict:
    if not raw:
        raise ValidationFailed([{"issue": "Empty file"}])

    try:
        df = pd.read_csv(BytesIO(raw))
    except Exception as exc:  # noqa: BLE001
        raise ValidationFailed([{"issue": f"Unparseable CSV: {exc}"}]) from exc

    if df.empty or len(df.columns) == 0:
        raise ValidationFailed([{"issue": "CSV has no data rows"}])

    # Attempt to coerce obvious date columns so dtype reporting is accurate.
    for col in df.columns:
        if _is_textual(df[col]):
            coerced = pd.to_datetime(df[col], errors="coerce", format="mixed")
            if coerced.notna().mean() > 0.8:
                df[col] = coerced

    details: list[dict] = []
    warnings: list[str] = []
    columns: list[dict] = []
    total = len(df)

    for col in df.columns:
        null_pct = round(float(df[col].isna().mean() * 100), 2)
        columns.append(
            {"name": str(col), "dtype": _dtype_name(df[col]), "null_pct": null_pct}
        )
        if 0 < null_pct:
            warnings.append(f"Column '{col}' has {null_pct:.0f}% missing values")
        # Business rule: revenue-like numeric columns must be non-negative.
        if "revenue" in str(col).lower() and pd.api.types.is_numeric_dtype(df[col]):
            neg = df[df[col] < 0]
            for idx in neg.index[:5]:
                details.append({"row": int(idx), "issue": "Negative revenue value"})

    if details:
        raise ValidationFailed(details)

    # Quality score: penalise missingness and duplicate rows.
    avg_null = float(df.isna().mean().mean()) * 100
    dup_pct = float(df.duplicated().mean()) * 100
    quality_score = round(max(0.0, 100.0 - avg_null - dup_pct), 2)

    # Build JSON-safe row payloads: datetimes -> ISO strings (round-trip on load).
    rows_df = df.copy()
    for col in rows_df.columns:
        if pd.api.types.is_datetime64_any_dtype(rows_df[col]):
            rows_df[col] = rows_df[col].dt.strftime("%Y-%m-%d")
    rows = rows_df.where(pd.notna(rows_df), None).to_dict(orient="records")

    return {
        "dataframe": df,
        "columns": columns,
        "row_count": total,
        "quality_score": quality_score,
        "warnings": warnings,
        "rows": rows,
    }
