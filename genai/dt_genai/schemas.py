from pydantic import BaseModel, Field
from typing import Literal, Optional

class ParsedQuery(BaseModel):

    decision_type: Literal[
    "price_change",
    "headcount",
    "marketing",
    "strategy",
    "other"
]

    parameter: str

    magnitude: float

    magnitude_type: Literal[
        "percentage",
        "absolute"
    ]

    target_metric: Optional[str] = None

    confidence: float = Field(ge=0, le=1)

    parser_used: Literal[
        "rules",
        "llm",
        "rules+llm"
    ]

    raw_query: str