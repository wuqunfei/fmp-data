# fmp_data/index/schema.py
from datetime import date

from pydantic import BaseModel, Field


class IndexSymbolArgs(BaseModel):
    """Arguments for index endpoints requiring a symbol"""

    symbol: str = Field(description="Index symbol (e.g., '^GSPC' for S&P 500)")


class IndexHistoricalArgs(IndexSymbolArgs):
    """Arguments for historical index data endpoints"""

    start_date: date | None = Field(
        None, description="Start date for historical data (format: YYYY-MM-DD)"
    )
    end_date: date | None = Field(
        None, description="End date for historical data (format: YYYY-MM-DD)"
    )


class IndexListArgs(BaseModel):
    """Arguments for listing endpoints that take no arguments"""

    pass
