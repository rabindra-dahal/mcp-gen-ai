from pydantic import BaseModel, Field
from typing import Literal

class FinancialAuditQuery(BaseModel):
    account_id: str = Field(
        ..., 
        description="The unique alphanumeric identifier of the corporate bank account (e.g., ACC-12345).",
        min_length=8,
        max_length=12
    )
    timeframe: Literal["30d", "90d", "YTD"] = Field(
        "30d", 
        description="The relative retrogressive time delta constraint window for transaction evaluation."
    )
    max_amount: float = Field(
        10000.0,
        description="An upper numeric threshold filter to surface anomalous transactions flag.",
        gt=0
    )
