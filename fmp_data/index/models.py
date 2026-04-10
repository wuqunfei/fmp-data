# fmp_data/index/models.py
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

default_model_config = ConfigDict(
    populate_by_name=True,
    validate_assignment=True,
    str_strip_whitespace=True,
    extra="allow",
    alias_generator=to_camel,
)


class IndexConstituent(BaseModel):
    """Index constituent information"""

    model_config = default_model_config

    symbol: str = Field(description="Stock symbol")
    name: str | None = Field(None, description="Company name")
    sector: str | None = Field(None, description="Company sector")
    sub_sector: str | None = Field(None, alias="subSector", description="Sub-sector")
    headquarter: str | None = Field(
        None, alias="headQuarter", description="Company headquarters"
    )
    date_first_added: datetime | None = Field(
        None, alias="dateFirstAdded", description="Date added to index"
    )
    cik: str | None = Field(None, description="CIK number")
    founded: str | None = Field(None, description="Year founded")


class HistoricalIndexConstituent(BaseModel):
    """Historical index constituent change information"""

    model_config = default_model_config

    date: datetime = Field(description="Date of change")
    symbol: str | None = Field(None, description="Stock symbol")
    date_added: str | None = Field(
        None, alias="dateAdded", description="Human-readable date added"
    )
    added_security: str | None = Field(
        None, alias="addedSecurity", description="Added security symbol"
    )
    removed_security: str | None = Field(
        None, alias="removedSecurity", description="Removed security symbol"
    )
    removed_ticker: str | None = Field(
        None, alias="removedTicker", description="Removed ticker symbol"
    )
    added_ticker: str | None = Field(
        None, alias="addedTicker", description="Added ticker symbol"
    )
    reason: str | None = Field(None, description="Reason for the change")


class IndexInfo(BaseModel):
    """Index listing information"""

    model_config = default_model_config

    symbol: str = Field(description="Index symbol")
    name: str | None = Field(None, description="Index name")
    currency: str | None = Field(None, description="Currency")
    stock_exchange: str | None = Field(
        None, alias="stockExchange", description="Stock exchange"
    )
    exchange_short_name: str | None = Field(
        None, alias="exchangeShortName", description="Exchange abbreviation"
    )
    exchange: str | None = Field(None, description="Exchange identifier")


class IndexQuote(BaseModel):
    """Index quote information"""

    model_config = default_model_config

    symbol: str = Field(description="Index symbol")
    name: str | None = Field(None, description="Index name")
    price: float | None = Field(None, description="Current index value")
    changes_percentage: float | None = Field(
        None, alias="changesPercentage", description="Price change percentage"
    )
    change: float | None = Field(None, description="Price change")
    day_low: float | None = Field(None, alias="dayLow", description="Day low")
    day_high: float | None = Field(None, alias="dayHigh", description="Day high")
    year_high: float | None = Field(None, alias="yearHigh", description="52-week high")
    year_low: float | None = Field(None, alias="yearLow", description="52-week low")
    timestamp: int | None = Field(None, description="Quote timestamp")


class IndexQuoteShort(BaseModel):
    """Index short quote information"""

    model_config = default_model_config

    symbol: str = Field(description="Index symbol")
    price: float | None = Field(None, description="Current index value")
    volume: int | None = Field(None, description="Trading volume")


class IndexHistoricalPrice(BaseModel):
    """Historical index price data (full)"""

    model_config = default_model_config

    date: datetime = Field(description="Price date")
    open: float | None = Field(None, description="Opening price")
    high: float | None = Field(None, description="High price")
    low: float | None = Field(None, description="Low price")
    close: float | None = Field(None, description="Closing price")
    adj_close: float | None = Field(
        None, alias="adjClose", description="Adjusted closing price"
    )
    volume: int | None = Field(None, description="Trading volume")
    unadjusted_volume: int | None = Field(
        None, alias="unadjustedVolume", description="Unadjusted volume"
    )
    change: float | None = Field(None, description="Price change")
    change_percent: float | None = Field(
        None, alias="changePercent", description="Price change percentage"
    )
    vwap: float | None = Field(None, description="Volume weighted average price")
    label: str | None = Field(None, description="Date label")
    change_over_time: float | None = Field(
        None, alias="changeOverTime", description="Change over time"
    )


class IndexHistoricalPriceLight(BaseModel):
    """Light historical index price data"""

    model_config = default_model_config

    date: datetime = Field(description="Price date")
    close: float | None = Field(None, description="Closing price")
    volume: int | None = Field(None, description="Trading volume")


class IndexIntradayPrice(BaseModel):
    """Intraday index price data"""

    model_config = default_model_config

    date: datetime = Field(description="Price timestamp")
    open: float | None = Field(None, description="Opening price")
    high: float | None = Field(None, description="High price")
    low: float | None = Field(None, description="Low price")
    close: float | None = Field(None, description="Closing price")
    volume: int | None = Field(None, description="Trading volume")
