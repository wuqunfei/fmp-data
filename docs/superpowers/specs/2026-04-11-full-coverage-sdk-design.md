# FMP-Data SDK Full Coverage Extension

**Date:** 2026-04-11
**Status:** Approved
**Approach:** Extend existing SDK (Option A)

## Goal

Add the ~25 missing FMP stable API endpoints to achieve full API coverage across index data, alternative asset quote/historical variants, full batch quotes, and market status endpoints.

## Current State

The SDK implements **~297 endpoints** across 13 domain modules using the FMP stable API (`/stable/` prefix). Architecture is mature: httpx + Pydantic v2 + sync/async clients + tenacity retries + rate limiting + caching.

## Missing Endpoints (25 total)

### 1. Index Module (`fmp_data/index/`) - 9 endpoints

| Endpoint Path | Description | New Model |
|---|---|---|
| `indexes-list` | List all available indexes | `IndexInfo` |
| `index-quote` | Full index quote by symbol | `IndexQuote` |
| `index-quote-short` | Short index quote | `IndexQuoteShort` |
| `all-index-quotes` | All index quotes batch | reuse `IndexQuote` |
| `index-historical-price-eod-full` | Full historical index EOD | `IndexHistoricalPrice` |
| `index-historical-price-eod-light` | Light historical index EOD | `IndexHistoricalPriceLight` |
| `index-intraday-1-min` | 1-minute intraday index | `IndexIntradayPrice` |
| `index-intraday-5-min` | 5-minute intraday index | reuse `IndexIntradayPrice` |
| `index-intraday-1-hour` | 1-hour intraday index | reuse `IndexIntradayPrice` |

**New files:** None (extend existing `endpoints.py`, `models.py`, `schema.py`, `client.py`, `async_client.py`, `mapping.py`)

**New models:** `IndexInfo`, `IndexQuote`, `IndexQuoteShort`, `IndexHistoricalPrice`, `IndexHistoricalPriceLight`, `IndexIntradayPrice`

**New schemas:** `IndexQuoteArgs`, `IndexQuoteShortArgs`, `AllIndexQuotesArgs`, `IndexHistoricalArgs`, `IndexHistoricalLightArgs`, `IndexIntradayArgs`

### 2. Alternative Module (`fmp_data/alternative/`) - 6 endpoints

| Endpoint Path | Description | New Model |
|---|---|---|
| `cryptocurrency-quote-short` | Short crypto quote | `CryptoQuoteShort` |
| `cryptocurrency-historical-price-eod-light` | Light crypto historical | `CryptoHistoricalPriceLight` |
| `forex-quote-short` | Short forex quote | `ForexQuoteShort` |
| `forex-historical-price-eod-light` | Light forex historical | `ForexHistoricalPriceLight` |
| `commodities-quote-short` | Short commodity quote | `CommodityQuoteShort` |
| `commodities-historical-price-eod-light` | Light commodity historical | `CommodityHistoricalPriceLight` |

**New models:** 6 (short quote + light historical for each asset class)

**New schemas:** `CryptoQuoteShortArgs`, `CryptoHistoricalLightArgs`, `ForexQuoteShortArgs`, `ForexHistoricalLightArgs`, `CommodityQuoteShortArgs`, `CommodityHistoricalLightArgs`

### 3. Batch Module (`fmp_data/batch/`) - 7 endpoints

| Endpoint Path | Description | New Model |
|---|---|---|
| `full-exchange-quotes` | Full quotes for an exchange | reuse existing quote models |
| `full-etf-quotes` | Full ETF quotes | reuse existing quote models |
| `full-mutualfund-quotes` | Full mutual fund quotes | reuse existing quote models |
| `full-cryptocurrency-quotes` | Full crypto quotes | reuse `CryptoQuote` |
| `full-commodities-quotes` | Full commodity quotes | reuse `CommodityQuote` |
| `full-forex-quotes` | Full forex quotes | reuse `ForexQuote` |
| `full-index-quotes` | Full index quotes | reuse `IndexQuote` |

**New models:** 0 (reuse from respective modules)

**New schemas:** `FullExchangeQuotesArgs` (needs exchange param), rest are parameterless

### 4. Market Module (`fmp_data/market/`) - 3 endpoints

| Endpoint Path | Description | New Model |
|---|---|---|
| `is-the-market-open` | Check if market is currently open | `MarketStatus` |
| `symbol-changes-list` | List all symbol changes | `SymbolChangeItem` |
| `company-symbols-list` | List all company symbols | `CompanySymbolItem` |

**New models:** `MarketStatus`, `SymbolChangeItem`, `CompanySymbolItem`

**New schemas:** None (no params) or minimal args models

## Implementation Pattern

Each endpoint follows the established pattern:

```python
# 1. endpoints.py - Endpoint definition
INDEX_QUOTE: Endpoint = Endpoint(
    name="index_quote",
    path="index-quote",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get real-time index quote",
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
    arg_model=IndexQuoteArgs,
)

# 2. models.py - Pydantic response model
class IndexQuote(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")
    symbol: str
    name: str | None = None
    price: float | None = None
    change: float | None = None
    changes_percentage: float | None = Field(None, alias="changesPercentage")
    # ... etc

# 3. schema.py - Request schema
class IndexQuoteArgs(BaseArgs):
    symbol: str

# 4. client.py - Sync method
def get_index_quote(self, symbol: str) -> IndexQuote:
    return self._get(INDEX_QUOTE, symbol=symbol)

# 5. async_client.py - Async method
async def get_index_quote(self, symbol: str) -> IndexQuote:
    return await self._get(INDEX_QUOTE, symbol=symbol)
```

## Integration Testing Strategy

- **Test key:** `FMP_TEST_API_KEY` environment variable
- **Location:** `tests/integration/` alongside existing test files
- **Framework:** pytest with `@pytest.mark.integration` marker
- **Per-endpoint tests:**
  - Call the endpoint with a known symbol
  - Assert response is non-empty
  - Assert response matches expected Pydantic model
- **License-gated endpoints:** Mark with `@pytest.mark.skip(reason="requires higher API tier")` if 403 returned
- **Test files:**
  - `tests/integration/test_index_endpoints.py` (extend existing)
  - `tests/integration/test_alternative_endpoints.py` (extend existing)
  - `tests/integration/test_batch_endpoints.py` (extend existing)
  - `tests/integration/test_market_endpoints.py` (extend existing)

## What Does NOT Change

- Base client (`base.py`), config, rate limiting, caching infrastructure
- Existing endpoint definitions or models
- LangChain or MCP integrations
- No refactoring of existing code

## Success Criteria

1. All 25 new endpoints defined with proper Endpoint objects
2. All new Pydantic models validate real API responses
3. Both sync and async client methods added
4. Integration tests written for every new endpoint
5. `make lint` and `make test` pass
6. Type checking passes (`mypy`)
