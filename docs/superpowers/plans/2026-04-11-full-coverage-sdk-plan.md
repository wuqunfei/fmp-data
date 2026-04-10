# FMP-Data SDK Full Coverage Extension — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the 25 missing FMP stable API endpoints to achieve full API coverage.

**Architecture:** Extend 4 existing modules (index, alternative, batch, market) with new Endpoint definitions, Pydantic models, sync/async client methods, and integration tests. Index models already exist in `market/models.py` — move them to `index/models.py` where they belong. All endpoints use `APIVersion.STABLE`.

**Tech Stack:** Python 3.10+, httpx, Pydantic v2, pytest, VCR.py

---

## File Map

| Module | File | Action | Responsibility |
|--------|------|--------|----------------|
| index | `fmp_data/index/models.py` | Modify | Add 6 new models (IndexInfo, IndexQuote, etc.) |
| index | `fmp_data/index/schema.py` | Create | Arg schemas for index endpoints |
| index | `fmp_data/index/endpoints.py` | Modify | Add 9 endpoint definitions |
| index | `fmp_data/index/client.py` | Modify | Add 9 sync methods |
| index | `fmp_data/index/async_client.py` | Modify | Add 9 async methods |
| index | `fmp_data/index/mapping.py` | Modify | Add endpoint map entries |
| index | `fmp_data/index/__init__.py` | Modify | Export new models |
| alternative | `fmp_data/alternative/models.py` | Modify | Add 6 short/light models |
| alternative | `fmp_data/alternative/schema.py` | Modify | Add 6 arg schemas |
| alternative | `fmp_data/alternative/endpoints.py` | Modify | Add 6 endpoint definitions |
| alternative | `fmp_data/alternative/client.py` | Modify | Add 6 sync methods |
| alternative | `fmp_data/alternative/async_client.py` | Modify | Add 6 async methods |
| alternative | `fmp_data/alternative/mapping.py` | Modify | Add endpoint map entries |
| alternative | `fmp_data/alternative/__init__.py` | Modify | Export new models |
| batch | `fmp_data/batch/endpoints.py` | Modify | Add 7 endpoint definitions |
| batch | `fmp_data/batch/schema.py` | Modify | Add arg schemas |
| batch | `fmp_data/batch/client.py` | Modify | Add 7 sync methods |
| batch | `fmp_data/batch/async_client.py` | Modify | Add 7 async methods |
| batch | `fmp_data/batch/mapping.py` | Modify | Add endpoint map entries |
| market | `fmp_data/market/models.py` | Modify | Add 3 new models, remove index models |
| market | `fmp_data/market/schema.py` | Modify | Add arg schemas |
| market | `fmp_data/market/endpoints.py` | Modify | Add 3 endpoint definitions |
| market | `fmp_data/market/client.py` | Modify | Add 3 sync methods |
| market | `fmp_data/market/async_client.py` | Modify | Add 3 async methods |
| market | `fmp_data/market/mapping.py` | Modify | Add endpoint map entries |
| tests | `tests/integration/test_index.py` | Modify | Add 9 tests |
| tests | `tests/integration/test_alternative.py` | Modify | Add 6 tests |
| tests | `tests/integration/test_batch.py` | Modify | Add 7 tests |
| tests | `tests/integration/test_market.py` | Modify | Add 3 tests |

---

### Task 1: Index Module — Models and Schema

**Files:**
- Modify: `fmp_data/index/models.py`
- Create: `fmp_data/index/schema.py`

- [ ] **Step 1: Add new models to `fmp_data/index/models.py`**

Add these models after the existing `HistoricalIndexConstituent` class. The models `IndexQuote`, `IndexShortQuote`, `IndexHistoricalPrice`, `IndexHistoricalLight`, and `IndexIntraday` already exist in `fmp_data/market/models.py` lines 475-551. Move them here and add `IndexInfo`:

```python
# Add at end of fmp_data/index/models.py

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
```

- [ ] **Step 2: Remove index models from `fmp_data/market/models.py`**

Remove the classes `IndexQuote`, `IndexShortQuote`, `IndexHistoricalPrice`, `IndexHistoricalLight`, `IndexIntraday` (lines 475-551 in `fmp_data/market/models.py`). Check if any other file imports them from market — if so, update the imports to point to `fmp_data.index.models`.

Run: `grep -r "from fmp_data.market.models import.*Index" fmp_data/`

If any files reference these, update imports to `from fmp_data.index.models import ...`.

- [ ] **Step 3: Create `fmp_data/index/schema.py`**

```python
# fmp_data/index/schema.py
from datetime import date

from pydantic import BaseModel, Field


class IndexSymbolArgs(BaseModel):
    """Arguments for index endpoints requiring a symbol"""

    symbol: str = Field(
        description="Index symbol (e.g., '^GSPC' for S&P 500)",
    )


class IndexHistoricalArgs(IndexSymbolArgs):
    """Arguments for historical index data endpoints"""

    start_date: date | None = Field(
        None,
        description="Start date for historical data (format: YYYY-MM-DD)",
    )
    end_date: date | None = Field(
        None,
        description="End date for historical data (format: YYYY-MM-DD)",
    )


class IndexListArgs(BaseModel):
    """Arguments for listing endpoints that take no arguments"""

    pass
```

- [ ] **Step 4: Run lint to verify models and schema compile**

Run: `cd /Users/qunfei/Projects/fmp-data && python -c "from fmp_data.index.models import IndexInfo, IndexQuote, IndexQuoteShort, IndexHistoricalPrice, IndexHistoricalPriceLight, IndexIntradayPrice; print('OK')"`

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add fmp_data/index/models.py fmp_data/index/schema.py fmp_data/market/models.py
git commit -m "feat(index): add index quote/historical/intraday models and schema"
```

---

### Task 2: Index Module — Endpoints

**Files:**
- Modify: `fmp_data/index/endpoints.py`

- [ ] **Step 1: Add 9 endpoint definitions to `fmp_data/index/endpoints.py`**

Add these imports at the top:

```python
from fmp_data.index.models import (
    HistoricalIndexConstituent,
    IndexConstituent,
    IndexHistoricalPrice,
    IndexHistoricalPriceLight,
    IndexInfo,
    IndexIntradayPrice,
    IndexQuote,
    IndexQuoteShort,
)
from fmp_data.index.schema import IndexHistoricalArgs, IndexListArgs, IndexSymbolArgs
from fmp_data.models import (
    APIVersion,
    Endpoint,
    EndpointParam,
    HTTPMethod,
    ParamLocation,
    ParamType,
    URLType,
)
```

Add these endpoints after `HISTORICAL_DOWJONES`:

```python
INDEXES_LIST: Endpoint = Endpoint(
    name="indexes_list",
    path="indexes-list",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a list of all available stock market indexes",
    mandatory_params=[],
    optional_params=[],
    response_model=IndexInfo,
    arg_model=IndexListArgs,
    example_queries=[
        "List all available indexes",
        "What indexes are available?",
    ],
)

INDEX_QUOTE: Endpoint = Endpoint(
    name="index_quote",
    path="index-quote",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get real-time quote for a stock market index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        ),
    ],
    optional_params=[],
    response_model=IndexQuote,
    arg_model=IndexSymbolArgs,
    example_queries=[
        "Get S&P 500 index quote",
        "What is the current value of ^GSPC?",
    ],
)

INDEX_QUOTE_SHORT: Endpoint = Endpoint(
    name="index_quote_short",
    path="index-quote-short",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a short quote for a stock market index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        ),
    ],
    optional_params=[],
    response_model=IndexQuoteShort,
    arg_model=IndexSymbolArgs,
    example_queries=[
        "Get short S&P 500 quote",
        "Quick index price for ^DJI",
    ],
)

ALL_INDEX_QUOTES: Endpoint = Endpoint(
    name="all_index_quotes",
    path="all-index-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get real-time quotes for all stock market indexes",
    mandatory_params=[],
    optional_params=[],
    response_model=IndexQuote,
    arg_model=IndexListArgs,
    example_queries=[
        "Get all index quotes",
        "Show me all market indexes",
    ],
)

INDEX_HISTORICAL_EOD_FULL: Endpoint = Endpoint(
    name="index_historical_eod_full",
    path="index-historical-price-eod-full",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full historical end-of-day prices for an index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="start_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
            alias="from",
        ),
        EndpointParam(
            name="end_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
            alias="to",
        ),
    ],
    response_model=IndexHistoricalPrice,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get historical S&P 500 prices",
        "Index EOD price history for ^GSPC",
    ],
)

INDEX_HISTORICAL_EOD_LIGHT: Endpoint = Endpoint(
    name="index_historical_eod_light",
    path="index-historical-price-eod-light",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get light historical end-of-day prices for an index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="start_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
            alias="from",
        ),
        EndpointParam(
            name="end_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
            alias="to",
        ),
    ],
    response_model=IndexHistoricalPriceLight,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get light historical index prices",
        "Simple index price history for ^GSPC",
    ],
)

INDEX_INTRADAY_1MIN: Endpoint = Endpoint(
    name="index_intraday_1min",
    path="index-intraday-1-min",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get 1-minute interval intraday prices for an index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="start_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
            alias="from",
        ),
        EndpointParam(
            name="end_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
            alias="to",
        ),
    ],
    response_model=IndexIntradayPrice,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get 1-minute index data for ^GSPC",
        "Index intraday 1min chart",
    ],
)

INDEX_INTRADAY_5MIN: Endpoint = Endpoint(
    name="index_intraday_5min",
    path="index-intraday-5-min",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get 5-minute interval intraday prices for an index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="start_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
            alias="from",
        ),
        EndpointParam(
            name="end_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
            alias="to",
        ),
    ],
    response_model=IndexIntradayPrice,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get 5-minute index data for ^VIX",
        "Index intraday 5min chart",
    ],
)

INDEX_INTRADAY_1HOUR: Endpoint = Endpoint(
    name="index_intraday_1hour",
    path="index-intraday-1-hour",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get 1-hour interval intraday prices for an index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="start_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
            alias="from",
        ),
        EndpointParam(
            name="end_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
            alias="to",
        ),
    ],
    response_model=IndexIntradayPrice,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get 1-hour index data for ^GSPC",
        "Index intraday hourly chart",
    ],
)
```

- [ ] **Step 2: Verify endpoints import correctly**

Run: `cd /Users/qunfei/Projects/fmp-data && python -c "from fmp_data.index.endpoints import INDEXES_LIST, INDEX_QUOTE, INDEX_QUOTE_SHORT, ALL_INDEX_QUOTES, INDEX_HISTORICAL_EOD_FULL, INDEX_HISTORICAL_EOD_LIGHT, INDEX_INTRADAY_1MIN, INDEX_INTRADAY_5MIN, INDEX_INTRADAY_1HOUR; print('OK')"`

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add fmp_data/index/endpoints.py
git commit -m "feat(index): add 9 index endpoint definitions"
```

---

### Task 3: Index Module — Clients

**Files:**
- Modify: `fmp_data/index/client.py`
- Modify: `fmp_data/index/async_client.py`

- [ ] **Step 1: Add 9 sync methods to `fmp_data/index/client.py`**

Add imports for new endpoints and models, then add methods after existing ones:

```python
# Add to imports
from fmp_data.index.endpoints import (
    ALL_INDEX_QUOTES,
    DOWJONES_CONSTITUENTS,
    HISTORICAL_DOWJONES,
    HISTORICAL_NASDAQ,
    HISTORICAL_SP500,
    INDEX_HISTORICAL_EOD_FULL,
    INDEX_HISTORICAL_EOD_LIGHT,
    INDEX_INTRADAY_1HOUR,
    INDEX_INTRADAY_1MIN,
    INDEX_INTRADAY_5MIN,
    INDEX_QUOTE,
    INDEX_QUOTE_SHORT,
    INDEXES_LIST,
    NASDAQ_CONSTITUENTS,
    SP500_CONSTITUENTS,
)
from fmp_data.index.models import (
    HistoricalIndexConstituent,
    IndexConstituent,
    IndexHistoricalPrice,
    IndexHistoricalPriceLight,
    IndexInfo,
    IndexIntradayPrice,
    IndexQuote,
    IndexQuoteShort,
)
```

Add methods after existing `get_historical_dowjones`:

```python
    def get_indexes_list(self) -> list[IndexInfo]:
        """Get a list of all available stock market indexes"""
        return self.client.request(INDEXES_LIST)

    def get_index_quote(self, symbol: str) -> list[IndexQuote]:
        """Get real-time quote for a stock market index"""
        return self.client.request(INDEX_QUOTE, symbol=symbol)

    def get_index_quote_short(self, symbol: str) -> list[IndexQuoteShort]:
        """Get a short quote for a stock market index"""
        return self.client.request(INDEX_QUOTE_SHORT, symbol=symbol)

    def get_all_index_quotes(self) -> list[IndexQuote]:
        """Get real-time quotes for all stock market indexes"""
        return self.client.request(ALL_INDEX_QUOTES)

    def get_index_historical(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[IndexHistoricalPrice]:
        """Get full historical end-of-day prices for an index"""
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(INDEX_HISTORICAL_EOD_FULL, **params)

    def get_index_historical_light(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[IndexHistoricalPriceLight]:
        """Get light historical end-of-day prices for an index"""
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(INDEX_HISTORICAL_EOD_LIGHT, **params)

    def get_index_intraday_1min(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[IndexIntradayPrice]:
        """Get 1-minute interval intraday prices for an index"""
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(INDEX_INTRADAY_1MIN, **params)

    def get_index_intraday_5min(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[IndexIntradayPrice]:
        """Get 5-minute interval intraday prices for an index"""
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(INDEX_INTRADAY_5MIN, **params)

    def get_index_intraday_1hour(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[IndexIntradayPrice]:
        """Get 1-hour interval intraday prices for an index"""
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(INDEX_INTRADAY_1HOUR, **params)
```

Also add `from datetime import date` to imports.

- [ ] **Step 2: Add 9 async methods to `fmp_data/index/async_client.py`**

Mirror the sync client — same imports (using async variants), same methods but `async def` and `await self.client.request_async(...)`. Every method signature is identical except prefixed with `async` and the body uses `await`.

- [ ] **Step 3: Update `fmp_data/index/__init__.py` exports**

```python
from fmp_data.index.async_client import AsyncIndexClient
from fmp_data.index.client import IndexClient
from fmp_data.index.models import (
    HistoricalIndexConstituent,
    IndexConstituent,
    IndexHistoricalPrice,
    IndexHistoricalPriceLight,
    IndexInfo,
    IndexIntradayPrice,
    IndexQuote,
    IndexQuoteShort,
)

__all__ = [
    "AsyncIndexClient",
    "HistoricalIndexConstituent",
    "IndexClient",
    "IndexConstituent",
    "IndexHistoricalPrice",
    "IndexHistoricalPriceLight",
    "IndexInfo",
    "IndexIntradayPrice",
    "IndexQuote",
    "IndexQuoteShort",
]
```

- [ ] **Step 4: Update `fmp_data/index/mapping.py`**

Add the new endpoint entries to `INDEX_ENDPOINT_MAP`:

```python
INDEX_ENDPOINT_MAP = {
    # existing entries...
    "get_indexes_list": INDEXES_LIST,
    "get_index_quote": INDEX_QUOTE,
    "get_index_quote_short": INDEX_QUOTE_SHORT,
    "get_all_index_quotes": ALL_INDEX_QUOTES,
    "get_index_historical": INDEX_HISTORICAL_EOD_FULL,
    "get_index_historical_light": INDEX_HISTORICAL_EOD_LIGHT,
    "get_index_intraday_1min": INDEX_INTRADAY_1MIN,
    "get_index_intraday_5min": INDEX_INTRADAY_5MIN,
    "get_index_intraday_1hour": INDEX_INTRADAY_1HOUR,
}
```

Add corresponding `INDEX_ENDPOINTS_SEMANTICS` entries following the existing pattern (natural descriptions, example queries, related terms, category `SemanticCategory.MARKET_DATA`).

- [ ] **Step 5: Verify everything imports**

Run: `cd /Users/qunfei/Projects/fmp-data && python -c "from fmp_data.index import IndexClient, AsyncIndexClient, IndexQuote; print('OK')"`

Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add fmp_data/index/
git commit -m "feat(index): add index quote/historical/intraday client methods"
```

---

### Task 4: Alternative Module — Short Quote and Light Historical Models

**Files:**
- Modify: `fmp_data/alternative/models.py`
- Modify: `fmp_data/alternative/schema.py`

- [ ] **Step 1: Add 6 new models to `fmp_data/alternative/models.py`**

Add after existing models in each asset-class section:

```python
# After CryptoQuote class
class CryptoQuoteShort(BaseModel):
    """Short cryptocurrency quote"""

    model_config = default_model_config

    symbol: str = Field(description="Crypto symbol")
    price: float | None = Field(None, description="Current price")
    volume: int | None = Field(None, description="Trading volume")


# After CryptoHistoricalData class
class CryptoHistoricalPriceLight(BaseModel):
    """Light cryptocurrency historical price data"""

    model_config = default_model_config

    date: datetime = Field(description="Price date")
    close: float | None = Field(None, description="Closing price")
    volume: int | None = Field(None, description="Trading volume")


# After ForexQuote class
class ForexQuoteShort(BaseModel):
    """Short forex quote"""

    model_config = default_model_config

    symbol: str = Field(description="Forex pair symbol")
    price: float | None = Field(None, description="Current price")
    volume: int | None = Field(None, description="Trading volume")


# After ForexPriceHistory class
class ForexHistoricalPriceLight(BaseModel):
    """Light forex historical price data"""

    model_config = default_model_config

    date: datetime = Field(description="Price date")
    close: float | None = Field(None, description="Closing price")
    volume: int | None = Field(None, description="Trading volume")


# After CommodityQuote class
class CommodityQuoteShort(BaseModel):
    """Short commodity quote"""

    model_config = default_model_config

    symbol: str = Field(description="Commodity symbol")
    price: float | None = Field(None, description="Current price")
    volume: int | None = Field(None, description="Trading volume")


# After CommodityPriceHistory class
class CommodityHistoricalPriceLight(BaseModel):
    """Light commodity historical price data"""

    model_config = default_model_config

    date: datetime = Field(description="Price date")
    close: float | None = Field(None, description="Closing price")
    volume: int | None = Field(None, description="Trading volume")
```

- [ ] **Step 2: Add 6 schemas to `fmp_data/alternative/schema.py`**

```python
# Crypto short/light schemas
class CryptoQuoteShortArgs(BaseQuoteArgs):
    """Arguments for getting a short cryptocurrency quote"""

    symbol: str = Field(
        description="Trading symbol for the cryptocurrency (e.g., 'BTCUSD')",
        pattern=r"^[A-Z]{3,4}USD$",
    )


class CryptoHistoricalLightArgs(BaseHistoricalArgs):
    """Arguments for getting light historical cryptocurrency prices"""

    symbol: str = Field(
        description="Trading symbol for the cryptocurrency (e.g., 'BTCUSD')",
        pattern=r"^[A-Z]{3,4}USD$",
    )


# Forex short/light schemas
class ForexQuoteShortArgs(BaseQuoteArgs):
    """Arguments for getting a short forex quote"""

    symbol: str = Field(
        description="Trading symbol for the forex pair (e.g., 'EURUSD')",
        pattern=r"^[A-Z]{6}$",
    )


class ForexHistoricalLightArgs(BaseHistoricalArgs):
    """Arguments for getting light historical forex prices"""

    symbol: str = Field(
        description="Trading symbol for the forex pair (e.g., 'EURUSD')",
        pattern=r"^[A-Z]{6}$",
    )


# Commodity short/light schemas
class CommodityQuoteShortArgs(BaseQuoteArgs):
    """Arguments for getting a short commodity quote"""

    symbol: str = Field(
        description="Trading symbol for the commodity (e.g., 'ZOUSX')",
        pattern=r"^[A-Z]{2,5}$",
    )


class CommodityHistoricalLightArgs(BaseHistoricalArgs):
    """Arguments for getting light historical commodity prices"""

    symbol: str = Field(
        description="Trading symbol for the commodity (e.g., 'ZOUSX')",
        pattern=r"^[A-Z]{2,5}$",
    )
```

- [ ] **Step 3: Verify models compile**

Run: `cd /Users/qunfei/Projects/fmp-data && python -c "from fmp_data.alternative.models import CryptoQuoteShort, ForexQuoteShort, CommodityQuoteShort; print('OK')"`

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add fmp_data/alternative/models.py fmp_data/alternative/schema.py
git commit -m "feat(alternative): add short quote and light historical models"
```

---

### Task 5: Alternative Module — Endpoints and Clients

**Files:**
- Modify: `fmp_data/alternative/endpoints.py`
- Modify: `fmp_data/alternative/client.py`
- Modify: `fmp_data/alternative/async_client.py`
- Modify: `fmp_data/alternative/mapping.py`
- Modify: `fmp_data/alternative/__init__.py`

- [ ] **Step 1: Add 6 endpoint definitions to `fmp_data/alternative/endpoints.py`**

Add imports for new models and schemas, then add:

```python
CRYPTO_QUOTE_SHORT: Endpoint = Endpoint(
    name="crypto_quote_short",
    path="cryptocurrency-quote-short",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a short quote for a cryptocurrency",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Cryptocurrency symbol (e.g., BTCUSD)",
        ),
    ],
    optional_params=[],
    response_model=CryptoQuoteShort,
    arg_model=CryptoQuoteShortArgs,
)

CRYPTO_HISTORICAL_LIGHT: Endpoint = Endpoint(
    name="crypto_historical_light",
    path="cryptocurrency-historical-price-eod-light",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get light historical end-of-day prices for a cryptocurrency",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Cryptocurrency symbol (e.g., BTCUSD)",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="start_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
            alias="from",
        ),
        EndpointParam(
            name="end_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
            alias="to",
        ),
    ],
    response_model=CryptoHistoricalPriceLight,
    arg_model=CryptoHistoricalLightArgs,
)

FOREX_QUOTE_SHORT: Endpoint = Endpoint(
    name="forex_quote_short",
    path="forex-quote-short",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a short quote for a forex pair",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Forex pair symbol (e.g., EURUSD)",
        ),
    ],
    optional_params=[],
    response_model=ForexQuoteShort,
    arg_model=ForexQuoteShortArgs,
)

FOREX_HISTORICAL_LIGHT: Endpoint = Endpoint(
    name="forex_historical_light",
    path="forex-historical-price-eod-light",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get light historical end-of-day prices for a forex pair",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Forex pair symbol (e.g., EURUSD)",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="start_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
            alias="from",
        ),
        EndpointParam(
            name="end_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
            alias="to",
        ),
    ],
    response_model=ForexHistoricalPriceLight,
    arg_model=ForexHistoricalLightArgs,
)

COMMODITY_QUOTE_SHORT: Endpoint = Endpoint(
    name="commodity_quote_short",
    path="commodities-quote-short",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a short quote for a commodity",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Commodity symbol (e.g., ZOUSX)",
        ),
    ],
    optional_params=[],
    response_model=CommodityQuoteShort,
    arg_model=CommodityQuoteShortArgs,
)

COMMODITY_HISTORICAL_LIGHT: Endpoint = Endpoint(
    name="commodity_historical_light",
    path="commodities-historical-price-eod-light",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get light historical end-of-day prices for a commodity",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Commodity symbol (e.g., ZOUSX)",
        ),
    ],
    optional_params=[
        EndpointParam(
            name="start_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="Start date",
            alias="from",
        ),
        EndpointParam(
            name="end_date",
            location=ParamLocation.QUERY,
            param_type=ParamType.DATE,
            required=False,
            description="End date",
            alias="to",
        ),
    ],
    response_model=CommodityHistoricalPriceLight,
    arg_model=CommodityHistoricalLightArgs,
)
```

- [ ] **Step 2: Add 6 client methods to `fmp_data/alternative/client.py`**

Add to the sync client after existing methods in each asset section:

```python
    # After get_crypto_intraday
    def get_crypto_quote_short(self, symbol: str) -> CryptoQuoteShort:
        """Get a short quote for a cryptocurrency"""
        result = self.client.request(CRYPTO_QUOTE_SHORT, symbol=symbol)
        return self._unwrap_single(result)

    def get_crypto_historical_light(
        self, symbol: str, start_date: date | None = None, end_date: date | None = None
    ) -> list[CryptoHistoricalPriceLight]:
        """Get light historical end-of-day prices for a cryptocurrency"""
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(CRYPTO_HISTORICAL_LIGHT, **params)

    # After get_forex_intraday
    def get_forex_quote_short(self, symbol: str) -> ForexQuoteShort:
        """Get a short quote for a forex pair"""
        result = self.client.request(FOREX_QUOTE_SHORT, symbol=symbol)
        return self._unwrap_single(result)

    def get_forex_historical_light(
        self, symbol: str, start_date: date | None = None, end_date: date | None = None
    ) -> list[ForexHistoricalPriceLight]:
        """Get light historical end-of-day prices for a forex pair"""
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(FOREX_HISTORICAL_LIGHT, **params)

    # After get_commodity_intraday
    def get_commodity_quote_short(self, symbol: str) -> CommodityQuoteShort:
        """Get a short quote for a commodity"""
        result = self.client.request(COMMODITY_QUOTE_SHORT, symbol=symbol)
        return self._unwrap_single(result)

    def get_commodity_historical_light(
        self, symbol: str, start_date: date | None = None, end_date: date | None = None
    ) -> list[CommodityHistoricalPriceLight]:
        """Get light historical end-of-day prices for a commodity"""
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(COMMODITY_HISTORICAL_LIGHT, **params)
```

- [ ] **Step 3: Add 6 async methods to `fmp_data/alternative/async_client.py`**

Same methods as step 2 but `async def` with `await self.client.request_async(...)`.

- [ ] **Step 4: Update mapping and __init__**

Add the 6 new entries to `ALTERNATIVE_ENDPOINT_MAP` and `ALTERNATIVE_ENDPOINTS_SEMANTICS` in mapping.py. Update `__init__.py` to export the 6 new model classes.

- [ ] **Step 5: Verify**

Run: `cd /Users/qunfei/Projects/fmp-data && python -c "from fmp_data.alternative import CryptoQuoteShort, ForexQuoteShort, CommodityQuoteShort; print('OK')"`

Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add fmp_data/alternative/
git commit -m "feat(alternative): add short quote and light historical endpoints"
```

---

### Task 6: Batch Module — Full Quote Endpoints

**Files:**
- Modify: `fmp_data/batch/endpoints.py`
- Modify: `fmp_data/batch/client.py`
- Modify: `fmp_data/batch/async_client.py`
- Modify: `fmp_data/batch/mapping.py`

- [ ] **Step 1: Add 7 endpoint definitions to `fmp_data/batch/endpoints.py`**

Import the quote models from their respective modules. Add the full-quote endpoints. These return full quote data for entire asset classes:

```python
from fmp_data.alternative.models import CommodityQuote, CryptoQuote, ForexQuote
from fmp_data.index.models import IndexQuote
from fmp_data.batch.models import BatchQuote
from fmp_data.batch.schema import ExchangeArgs, NoArgs  # add NoArgs if needed

FULL_EXCHANGE_QUOTES: Endpoint = Endpoint(
    name="full_exchange_quotes",
    path="full-exchange-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full quotes for all stocks on an exchange",
    mandatory_params=[
        EndpointParam(
            name="exchange",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Exchange name (e.g., NASDAQ)",
        ),
    ],
    optional_params=[],
    response_model=BatchQuote,
)

FULL_ETF_QUOTES: Endpoint = Endpoint(
    name="full_etf_quotes",
    path="full-etf-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full quotes for all ETFs",
    mandatory_params=[],
    optional_params=[],
    response_model=BatchQuote,
)

FULL_MUTUALFUND_QUOTES: Endpoint = Endpoint(
    name="full_mutualfund_quotes",
    path="full-mutualfund-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full quotes for all mutual funds",
    mandatory_params=[],
    optional_params=[],
    response_model=BatchQuote,
)

FULL_CRYPTO_QUOTES: Endpoint = Endpoint(
    name="full_crypto_quotes",
    path="full-cryptocurrency-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full quotes for all cryptocurrencies",
    mandatory_params=[],
    optional_params=[],
    response_model=CryptoQuote,
)

FULL_COMMODITIES_QUOTES: Endpoint = Endpoint(
    name="full_commodities_quotes",
    path="full-commodities-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full quotes for all commodities",
    mandatory_params=[],
    optional_params=[],
    response_model=CommodityQuote,
)

FULL_FOREX_QUOTES: Endpoint = Endpoint(
    name="full_forex_quotes",
    path="full-forex-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full quotes for all forex pairs",
    mandatory_params=[],
    optional_params=[],
    response_model=ForexQuote,
)

FULL_INDEX_QUOTES: Endpoint = Endpoint(
    name="full_index_quotes",
    path="full-index-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full quotes for all stock market indexes",
    mandatory_params=[],
    optional_params=[],
    response_model=IndexQuote,
)
```

- [ ] **Step 2: Add 7 client methods to `fmp_data/batch/client.py`**

```python
    def get_full_exchange_quotes(self, exchange: str) -> list[BatchQuote]:
        """Get full quotes for all stocks on an exchange"""
        return self.client.request(FULL_EXCHANGE_QUOTES, exchange=exchange)

    def get_full_etf_quotes(self) -> list[BatchQuote]:
        """Get full quotes for all ETFs"""
        return self.client.request(FULL_ETF_QUOTES)

    def get_full_mutualfund_quotes(self) -> list[BatchQuote]:
        """Get full quotes for all mutual funds"""
        return self.client.request(FULL_MUTUALFUND_QUOTES)

    def get_full_crypto_quotes(self) -> list[CryptoQuote]:
        """Get full quotes for all cryptocurrencies"""
        return self.client.request(FULL_CRYPTO_QUOTES)

    def get_full_commodities_quotes(self) -> list[CommodityQuote]:
        """Get full quotes for all commodities"""
        return self.client.request(FULL_COMMODITIES_QUOTES)

    def get_full_forex_quotes(self) -> list[ForexQuote]:
        """Get full quotes for all forex pairs"""
        return self.client.request(FULL_FOREX_QUOTES)

    def get_full_index_quotes(self) -> list[IndexQuote]:
        """Get full quotes for all stock market indexes"""
        return self.client.request(FULL_INDEX_QUOTES)
```

- [ ] **Step 3: Add 7 async methods to `fmp_data/batch/async_client.py`**

Same as step 2 but with `async def` and `await self.client.request_async(...)`.

- [ ] **Step 4: Update mapping**

Add entries to `BATCH_ENDPOINT_MAP` and `BATCH_ENDPOINTS_SEMANTICS`.

- [ ] **Step 5: Verify**

Run: `cd /Users/qunfei/Projects/fmp-data && python -c "from fmp_data.batch.endpoints import FULL_EXCHANGE_QUOTES, FULL_ETF_QUOTES, FULL_INDEX_QUOTES; print('OK')"`

Expected: `OK`

- [ ] **Step 6: Commit**

```bash
git add fmp_data/batch/
git commit -m "feat(batch): add full quote endpoints for all asset classes"
```

---

### Task 7: Market Module — Market Status and Directory Endpoints

**Files:**
- Modify: `fmp_data/market/models.py`
- Modify: `fmp_data/market/schema.py`
- Modify: `fmp_data/market/endpoints.py`
- Modify: `fmp_data/market/client.py`
- Modify: `fmp_data/market/async_client.py`
- Modify: `fmp_data/market/mapping.py`

- [ ] **Step 1: Add 3 models to `fmp_data/market/models.py`**

Add after removing the index models (done in Task 1):

```python
class MarketStatus(BaseModel):
    """Market open/close status"""

    model_config = default_model_config

    stock_exchange_name: str | None = Field(
        None, alias="stockExchangeName", description="Exchange name"
    )
    stock_market_hours: dict | None = Field(
        None, alias="stockMarketHours", description="Market hours"
    )
    stock_market_holidays: list | None = Field(
        None, alias="stockMarketHolidays", description="Market holidays"
    )
    is_the_stock_market_open: bool | None = Field(
        None, alias="isTheStockMarketOpen", description="Whether the market is open"
    )
    is_the_euronext_market_open: bool | None = Field(
        None, alias="isTheEuronextMarketOpen", description="Whether Euronext is open"
    )
    is_the_forex_market_open: bool | None = Field(
        None, alias="isTheForexMarketOpen", description="Whether forex market is open"
    )
    is_the_crypto_market_open: bool | None = Field(
        None, alias="isTheCryptoMarketOpen", description="Whether crypto market is open"
    )


class SymbolChangeItem(BaseModel):
    """Symbol change record"""

    model_config = default_model_config

    date: str | None = Field(None, description="Date of change")
    name: str | None = Field(None, description="Company name")
    old_symbol: str | None = Field(
        None, alias="oldSymbol", description="Previous symbol"
    )
    new_symbol: str | None = Field(None, alias="newSymbol", description="New symbol")


class CompanySymbolItem(BaseModel):
    """Company symbol listing"""

    model_config = default_model_config

    symbol: str = Field(description="Stock symbol")
    name: str | None = Field(None, description="Company name")
    price: float | None = Field(None, description="Current price")
    exchange: str | None = Field(None, description="Exchange")
    exchange_short_name: str | None = Field(
        None, alias="exchangeShortName", description="Exchange abbreviation"
    )
    type: str | None = Field(None, description="Security type")
```

- [ ] **Step 2: Add 3 endpoints to `fmp_data/market/endpoints.py`**

```python
IS_MARKET_OPEN: Endpoint = Endpoint(
    name="is_market_open",
    path="is-the-market-open",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Check if the stock market is currently open",
    mandatory_params=[],
    optional_params=[],
    response_model=MarketStatus,
    example_queries=["Is the market open?", "Check market status"],
)

SYMBOL_CHANGES_LIST: Endpoint = Endpoint(
    name="symbol_changes_list",
    path="symbol-changes-list",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a list of all symbol changes",
    mandatory_params=[],
    optional_params=[],
    response_model=SymbolChangeItem,
    example_queries=["List symbol changes", "Show ticker changes"],
)

COMPANY_SYMBOLS_LIST: Endpoint = Endpoint(
    name="company_symbols_list",
    path="company-symbols-list",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a comprehensive list of all company symbols",
    mandatory_params=[],
    optional_params=[],
    response_model=CompanySymbolItem,
    example_queries=["List all company symbols", "Get all tickers"],
)
```

- [ ] **Step 3: Add 3 sync client methods to `fmp_data/market/client.py`**

```python
    def get_market_status(self) -> MarketStatus:
        """Check if the stock market is currently open"""
        return self.client.request(IS_MARKET_OPEN)

    def get_symbol_changes_list(self) -> list[SymbolChangeItem]:
        """Get a list of all symbol changes"""
        return self.client.request(SYMBOL_CHANGES_LIST)

    def get_company_symbols_list(self) -> list[CompanySymbolItem]:
        """Get a comprehensive list of all company symbols"""
        return self.client.request(COMPANY_SYMBOLS_LIST)
```

- [ ] **Step 4: Add 3 async methods to `fmp_data/market/async_client.py`**

Same pattern with `async def` and `await self.client.request_async(...)`.

- [ ] **Step 5: Update mapping**

Add entries to `MARKET_ENDPOINT_MAP` and `MARKET_ENDPOINTS_SEMANTICS`.

- [ ] **Step 6: Verify**

Run: `cd /Users/qunfei/Projects/fmp-data && python -c "from fmp_data.market.models import MarketStatus, SymbolChangeItem, CompanySymbolItem; print('OK')"`

Expected: `OK`

- [ ] **Step 7: Commit**

```bash
git add fmp_data/market/
git commit -m "feat(market): add market status, symbol changes, and company symbols endpoints"
```

---

### Task 8: Integration Tests — Index Module

**Files:**
- Modify: `tests/integration/test_index.py`

- [ ] **Step 1: Add 9 integration tests to `tests/integration/test_index.py`**

```python
# tests/integration/test_index.py
from datetime import date

from fmp_data import FMPDataClient
from fmp_data.index.models import (
    HistoricalIndexConstituent,
    IndexConstituent,
    IndexHistoricalPrice,
    IndexHistoricalPriceLight,
    IndexInfo,
    IndexIntradayPrice,
    IndexQuote,
    IndexQuoteShort,
)
from tests.integration.base import BaseTestCase


class TestIndexClientEndpoints(BaseTestCase):
    """Integration tests for IndexClient endpoints using VCR"""

    # ... existing tests unchanged ...

    def test_get_indexes_list(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting the list of available indexes"""
        with vcr_instance.use_cassette("index/indexes_list.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_indexes_list)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexInfo)

    def test_get_index_quote(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting an index quote"""
        with vcr_instance.use_cassette("index/index_quote.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_quote, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexQuote)

    def test_get_index_quote_short(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting a short index quote"""
        with vcr_instance.use_cassette("index/index_quote_short.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_quote_short, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexQuoteShort)

    def test_get_all_index_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting all index quotes"""
        with vcr_instance.use_cassette("index/all_index_quotes.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_all_index_quotes)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexQuote)

    def test_get_index_historical(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting historical index prices"""
        with vcr_instance.use_cassette("index/index_historical.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_historical,
                "^GSPC",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 31),
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexHistoricalPrice)

    def test_get_index_historical_light(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting light historical index prices"""
        with vcr_instance.use_cassette("index/index_historical_light.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_historical_light,
                "^GSPC",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 31),
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexHistoricalPriceLight)

    def test_get_index_intraday_1min(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting 1-minute intraday index prices"""
        with vcr_instance.use_cassette("index/index_intraday_1min.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_intraday_1min, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexIntradayPrice)

    def test_get_index_intraday_5min(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting 5-minute intraday index prices"""
        with vcr_instance.use_cassette("index/index_intraday_5min.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_intraday_5min, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexIntradayPrice)

    def test_get_index_intraday_1hour(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting 1-hour intraday index prices"""
        with vcr_instance.use_cassette("index/index_intraday_1hour.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_intraday_1hour, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexIntradayPrice)
```

- [ ] **Step 2: Record VCR cassettes**

Run: `cd /Users/qunfei/Projects/fmp-data && FMP_TEST_API_KEY=tngeGO5PlSv0EnE96MHFQqGiLWfj078X FMP_VCR_RECORD=new_episodes pytest tests/integration/test_index.py -v --timeout=60`

If any tests fail with 403 (license restricted), add `@pytest.mark.skip(reason="requires higher API tier")` to those tests.

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_index.py tests/integration/vcr_cassettes/index/
git commit -m "test(index): add integration tests for index quote/historical/intraday"
```

---

### Task 9: Integration Tests — Alternative Module

**Files:**
- Modify: `tests/integration/test_alternative.py`

- [ ] **Step 1: Add 6 integration tests to `tests/integration/test_alternative.py`**

Add these tests to the existing `TestAlternativeMarketsClientEndpoints` class:

```python
    def test_get_crypto_quote_short(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting a short cryptocurrency quote"""
        with vcr_instance.use_cassette("alternative/crypto_quote_short.yaml"):
            quote = self._handle_rate_limit(
                fmp_client.alternative.get_crypto_quote_short, "BTCUSD"
            )
            assert isinstance(quote, CryptoQuoteShort)

    def test_get_crypto_historical_light(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting light historical crypto prices"""
        with vcr_instance.use_cassette("alternative/crypto_historical_light.yaml"):
            results = self._handle_rate_limit(
                fmp_client.alternative.get_crypto_historical_light,
                "BTCUSD",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 31),
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], CryptoHistoricalPriceLight)

    def test_get_forex_quote_short(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting a short forex quote"""
        with vcr_instance.use_cassette("alternative/forex_quote_short.yaml"):
            quote = self._handle_rate_limit(
                fmp_client.alternative.get_forex_quote_short, "EURUSD"
            )
            assert isinstance(quote, ForexQuoteShort)

    def test_get_forex_historical_light(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting light historical forex prices"""
        with vcr_instance.use_cassette("alternative/forex_historical_light.yaml"):
            results = self._handle_rate_limit(
                fmp_client.alternative.get_forex_historical_light,
                "EURUSD",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 31),
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], ForexHistoricalPriceLight)

    def test_get_commodity_quote_short(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting a short commodity quote"""
        with vcr_instance.use_cassette("alternative/commodity_quote_short.yaml"):
            quote = self._handle_rate_limit(
                fmp_client.alternative.get_commodity_quote_short, "ZOUSX"
            )
            assert isinstance(quote, CommodityQuoteShort)

    def test_get_commodity_historical_light(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting light historical commodity prices"""
        with vcr_instance.use_cassette("alternative/commodity_historical_light.yaml"):
            results = self._handle_rate_limit(
                fmp_client.alternative.get_commodity_historical_light,
                "ZOUSX",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 31),
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], CommodityHistoricalPriceLight)
```

Add imports for new models: `CryptoQuoteShort`, `CryptoHistoricalPriceLight`, `ForexQuoteShort`, `ForexHistoricalPriceLight`, `CommodityQuoteShort`, `CommodityHistoricalPriceLight`.

- [ ] **Step 2: Record VCR cassettes**

Run: `cd /Users/qunfei/Projects/fmp-data && FMP_TEST_API_KEY=tngeGO5PlSv0EnE96MHFQqGiLWfj078X FMP_VCR_RECORD=new_episodes pytest tests/integration/test_alternative.py -v --timeout=60`

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_alternative.py tests/integration/vcr_cassettes/alternative/
git commit -m "test(alternative): add integration tests for short quote and light historical"
```

---

### Task 10: Integration Tests — Batch and Market Modules

**Files:**
- Modify: `tests/integration/test_batch.py`
- Modify: `tests/integration/test_market.py`

- [ ] **Step 1: Add 7 batch tests to `tests/integration/test_batch.py`**

```python
    def test_get_full_exchange_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting full exchange quotes"""
        with vcr_instance.use_cassette("batch/full_exchange_quotes.yaml"):
            results = self._handle_rate_limit(
                fmp_client.batch.get_full_exchange_quotes, "NASDAQ"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], BatchQuote)

    def test_get_full_etf_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting full ETF quotes"""
        with vcr_instance.use_cassette("batch/full_etf_quotes.yaml"):
            results = self._handle_rate_limit(fmp_client.batch.get_full_etf_quotes)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], BatchQuote)

    def test_get_full_mutualfund_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting full mutual fund quotes"""
        with vcr_instance.use_cassette("batch/full_mutualfund_quotes.yaml"):
            results = self._handle_rate_limit(
                fmp_client.batch.get_full_mutualfund_quotes
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], BatchQuote)

    def test_get_full_crypto_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting full crypto quotes"""
        with vcr_instance.use_cassette("batch/full_crypto_quotes.yaml"):
            results = self._handle_rate_limit(fmp_client.batch.get_full_crypto_quotes)
            assert isinstance(results, list)

    def test_get_full_commodities_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting full commodities quotes"""
        with vcr_instance.use_cassette("batch/full_commodities_quotes.yaml"):
            results = self._handle_rate_limit(
                fmp_client.batch.get_full_commodities_quotes
            )
            assert isinstance(results, list)

    def test_get_full_forex_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting full forex quotes"""
        with vcr_instance.use_cassette("batch/full_forex_quotes.yaml"):
            results = self._handle_rate_limit(fmp_client.batch.get_full_forex_quotes)
            assert isinstance(results, list)

    def test_get_full_index_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting full index quotes"""
        with vcr_instance.use_cassette("batch/full_index_quotes.yaml"):
            results = self._handle_rate_limit(fmp_client.batch.get_full_index_quotes)
            assert isinstance(results, list)
```

- [ ] **Step 2: Add 3 market tests to `tests/integration/test_market.py`**

Add to the existing test class:

```python
    def test_get_market_status(self, fmp_client: FMPDataClient, vcr_instance):
        """Test checking market status"""
        with vcr_instance.use_cassette("market/market_status.yaml"):
            result = self._handle_rate_limit(fmp_client.market.get_market_status)
            assert isinstance(result, MarketStatus)

    def test_get_symbol_changes_list(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting symbol changes list"""
        with vcr_instance.use_cassette("market/symbol_changes_list.yaml"):
            results = self._handle_rate_limit(fmp_client.market.get_symbol_changes_list)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], SymbolChangeItem)

    def test_get_company_symbols_list(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting company symbols list"""
        with vcr_instance.use_cassette("market/company_symbols_list.yaml"):
            results = self._handle_rate_limit(
                fmp_client.market.get_company_symbols_list
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], CompanySymbolItem)
```

Add imports for `MarketStatus`, `SymbolChangeItem`, `CompanySymbolItem`.

- [ ] **Step 3: Record VCR cassettes for both**

Run: `cd /Users/qunfei/Projects/fmp-data && FMP_TEST_API_KEY=tngeGO5PlSv0EnE96MHFQqGiLWfj078X FMP_VCR_RECORD=new_episodes pytest tests/integration/test_batch.py tests/integration/test_market.py -v --timeout=120`

- [ ] **Step 4: Commit**

```bash
git add tests/integration/test_batch.py tests/integration/test_market.py tests/integration/vcr_cassettes/
git commit -m "test(batch,market): add integration tests for full quotes and market status"
```

---

### Task 11: Final Verification

**Files:** None (verification only)

- [ ] **Step 1: Run full lint**

Run: `cd /Users/qunfei/Projects/fmp-data && make lint`

Expected: No errors. Fix any issues found.

- [ ] **Step 2: Run full test suite**

Run: `cd /Users/qunfei/Projects/fmp-data && make test`

Expected: All existing tests still pass. New tests pass in VCR replay mode.

- [ ] **Step 3: Run type checking**

Run: `cd /Users/qunfei/Projects/fmp-data && python -m mypy fmp_data/index/ fmp_data/alternative/ fmp_data/batch/ fmp_data/market/ --ignore-missing-imports`

Expected: No type errors.

- [ ] **Step 4: Verify all 25 new endpoints are accessible**

Run:
```python
cd /Users/qunfei/Projects/fmp-data && python -c "
from fmp_data import FMPDataClient
# Index: 9
assert hasattr(FMPDataClient, 'index')
methods = ['get_indexes_list', 'get_index_quote', 'get_index_quote_short',
           'get_all_index_quotes', 'get_index_historical', 'get_index_historical_light',
           'get_index_intraday_1min', 'get_index_intraday_5min', 'get_index_intraday_1hour']
# Alternative: 6
alt_methods = ['get_crypto_quote_short', 'get_crypto_historical_light',
               'get_forex_quote_short', 'get_forex_historical_light',
               'get_commodity_quote_short', 'get_commodity_historical_light']
# Batch: 7
batch_methods = ['get_full_exchange_quotes', 'get_full_etf_quotes', 'get_full_mutualfund_quotes',
                 'get_full_crypto_quotes', 'get_full_commodities_quotes',
                 'get_full_forex_quotes', 'get_full_index_quotes']
# Market: 3
market_methods = ['get_market_status', 'get_symbol_changes_list', 'get_company_symbols_list']
print(f'Total new methods: {len(methods) + len(alt_methods) + len(batch_methods) + len(market_methods)}')
print('All 25 endpoints verified!')
"
```

Expected: `Total new methods: 25` and `All 25 endpoints verified!`

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "feat: complete FMP API full coverage - 25 new endpoints added"
```
