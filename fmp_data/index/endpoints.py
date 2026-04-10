# fmp_data/index/endpoints.py
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

SP500_CONSTITUENTS: Endpoint = Endpoint(
    name="sp500_constituents",
    path="sp500-constituent",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get current S&P 500 index constituents",
    mandatory_params=[],
    optional_params=[],
    response_model=IndexConstituent,
    example_queries=[
        "Get S&P 500 components",
        "List all S&P 500 stocks",
        "S&P 500 constituents",
    ],
)

NASDAQ_CONSTITUENTS: Endpoint = Endpoint(
    name="nasdaq_constituents",
    path="nasdaq-constituent",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get current NASDAQ index constituents",
    mandatory_params=[],
    optional_params=[],
    response_model=IndexConstituent,
    example_queries=[
        "Get NASDAQ components",
        "List all NASDAQ stocks",
        "NASDAQ constituents",
    ],
)

DOWJONES_CONSTITUENTS: Endpoint = Endpoint(
    name="dowjones_constituents",
    path="dowjones-constituent",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get current Dow Jones Industrial Average constituents",
    mandatory_params=[],
    optional_params=[],
    response_model=IndexConstituent,
    example_queries=[
        "Get Dow Jones components",
        "List all Dow 30 stocks",
        "DJIA constituents",
    ],
)

HISTORICAL_SP500: Endpoint = Endpoint(
    name="historical_sp500",
    path="historical-sp500-constituent",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get historical S&P 500 constituent changes",
    mandatory_params=[],
    optional_params=[],
    response_model=HistoricalIndexConstituent,
    example_queries=[
        "Historical S&P 500 changes",
        "S&P 500 additions and removals",
        "S&P 500 constituent history",
    ],
)

HISTORICAL_NASDAQ: Endpoint = Endpoint(
    name="historical_nasdaq",
    path="historical-nasdaq-constituent",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get historical NASDAQ constituent changes",
    mandatory_params=[],
    optional_params=[],
    response_model=HistoricalIndexConstituent,
    example_queries=[
        "Historical NASDAQ changes",
        "NASDAQ additions and removals",
        "NASDAQ constituent history",
    ],
)

HISTORICAL_DOWJONES: Endpoint = Endpoint(
    name="historical_dowjones",
    path="historical-dowjones-constituent",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get historical Dow Jones constituent changes",
    mandatory_params=[],
    optional_params=[],
    response_model=HistoricalIndexConstituent,
    example_queries=[
        "Historical Dow Jones changes",
        "DJIA additions and removals",
        "Dow Jones constituent history",
    ],
)

# --- New index quote, historical, and intraday endpoints ---

INDEXES_LIST: Endpoint = Endpoint(
    name="indexes_list",
    path="indexes-list",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a list of all available market indexes",
    mandatory_params=[],
    optional_params=[],
    response_model=IndexInfo,
    arg_model=IndexListArgs,
    example_queries=[
        "List all available indexes",
        "Show me all market indexes",
        "What indexes are available?",
    ],
)

INDEX_QUOTE: Endpoint = Endpoint(
    name="index_quote",
    path="index-quote",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a full quote for a specific market index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        )
    ],
    optional_params=[],
    response_model=IndexQuote,
    arg_model=IndexSymbolArgs,
    example_queries=[
        "Get quote for S&P 500 index",
        "What is the current value of ^GSPC?",
        "Show me the Dow Jones index quote",
    ],
)

INDEX_QUOTE_SHORT: Endpoint = Endpoint(
    name="index_quote_short",
    path="index-quote-short",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get a short quote for a specific market index",
    mandatory_params=[
        EndpointParam(
            name="symbol",
            location=ParamLocation.QUERY,
            param_type=ParamType.STRING,
            required=True,
            description="Index symbol (e.g., ^GSPC)",
        )
    ],
    optional_params=[],
    response_model=IndexQuoteShort,
    arg_model=IndexSymbolArgs,
    example_queries=[
        "Get short quote for S&P 500",
        "Quick index price for ^DJI",
        "Short quote for NASDAQ index",
    ],
)

ALL_INDEX_QUOTES: Endpoint = Endpoint(
    name="all_index_quotes",
    path="all-index-quotes",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get quotes for all available market indexes",
    mandatory_params=[],
    optional_params=[],
    response_model=IndexQuote,
    arg_model=IndexListArgs,
    example_queries=[
        "Get all index quotes",
        "Show me all market index prices",
        "List quotes for every index",
    ],
)

_historical_symbol_param = EndpointParam(
    name="symbol",
    location=ParamLocation.QUERY,
    param_type=ParamType.STRING,
    required=True,
    description="Index symbol (e.g., ^GSPC)",
)

_historical_date_params = [
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
]

INDEX_HISTORICAL_EOD_FULL: Endpoint = Endpoint(
    name="index_historical_eod_full",
    path="index-historical-price-eod-full",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get full historical end-of-day price data for a market index",
    mandatory_params=[_historical_symbol_param],
    optional_params=_historical_date_params,
    response_model=IndexHistoricalPrice,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get historical prices for S&P 500",
        "Show me ^GSPC price history",
        "Historical end-of-day data for Dow Jones index",
    ],
)

INDEX_HISTORICAL_EOD_LIGHT: Endpoint = Endpoint(
    name="index_historical_eod_light",
    path="index-historical-price-eod-light",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get light historical end-of-day price data for a market index",
    mandatory_params=[_historical_symbol_param],
    optional_params=_historical_date_params,
    response_model=IndexHistoricalPriceLight,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get light historical prices for S&P 500",
        "Show me ^GSPC closing price history",
        "Light historical data for NASDAQ index",
    ],
)

INDEX_INTRADAY_1MIN: Endpoint = Endpoint(
    name="index_intraday_1min",
    path="index-intraday-1-min",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get 1-minute intraday price data for a market index",
    mandatory_params=[_historical_symbol_param],
    optional_params=_historical_date_params,
    response_model=IndexIntradayPrice,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get 1-minute intraday data for S&P 500",
        "Show me ^GSPC 1-min chart data",
        "1-minute index prices for Dow Jones",
    ],
)

INDEX_INTRADAY_5MIN: Endpoint = Endpoint(
    name="index_intraday_5min",
    path="index-intraday-5-min",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get 5-minute intraday price data for a market index",
    mandatory_params=[_historical_symbol_param],
    optional_params=_historical_date_params,
    response_model=IndexIntradayPrice,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get 5-minute intraday data for S&P 500",
        "Show me ^GSPC 5-min chart data",
        "5-minute index prices for NASDAQ",
    ],
)

INDEX_INTRADAY_1HOUR: Endpoint = Endpoint(
    name="index_intraday_1hour",
    path="index-intraday-1-hour",
    version=APIVersion.STABLE,
    url_type=URLType.API,
    method=HTTPMethod.GET,
    description="Get 1-hour intraday price data for a market index",
    mandatory_params=[_historical_symbol_param],
    optional_params=_historical_date_params,
    response_model=IndexIntradayPrice,
    arg_model=IndexHistoricalArgs,
    example_queries=[
        "Get 1-hour intraday data for S&P 500",
        "Show me ^GSPC hourly chart data",
        "Hourly index prices for Dow Jones",
    ],
)
