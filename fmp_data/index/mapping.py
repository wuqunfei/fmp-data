# fmp_data/index/mapping.py
from __future__ import annotations

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
from fmp_data.lc.models import EndpointSemantics, SemanticCategory

# Index endpoints mapping
INDEX_ENDPOINT_MAP = {
    "get_sp500_constituents": SP500_CONSTITUENTS,
    "get_nasdaq_constituents": NASDAQ_CONSTITUENTS,
    "get_dowjones_constituents": DOWJONES_CONSTITUENTS,
    "get_historical_sp500": HISTORICAL_SP500,
    "get_historical_nasdaq": HISTORICAL_NASDAQ,
    "get_historical_dowjones": HISTORICAL_DOWJONES,
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

# Complete semantic definitions for all endpoints
INDEX_ENDPOINTS_SEMANTICS = {
    "sp500_constituents": EndpointSemantics(
        client_name="index",
        method_name="get_sp500_constituents",
        natural_description=(
            "Get current S&P 500 index constituents. "
            "Returns list of companies currently included in the S&P 500 index."
        ),
        example_queries=[
            "Get S&P 500 constituents",
            "List companies in the S&P 500",
            "What stocks are in the S&P 500?",
            "Show me S&P 500 members",
            "S&P 500 component companies",
        ],
        related_terms=[
            "S&P 500",
            "SPX",
            "index constituents",
            "index members",
            "S&P components",
            "large cap index",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={},
        response_hints={},
        use_cases=["Financial analysis", "Investment research"],
    ),
    "nasdaq_constituents": EndpointSemantics(
        client_name="index",
        method_name="get_nasdaq_constituents",
        natural_description=(
            "Get current NASDAQ index constituents. "
            "Returns companies currently in the NASDAQ composite index."
        ),
        example_queries=[
            "Get NASDAQ constituents",
            "List companies in NASDAQ",
            "What stocks are in the NASDAQ index?",
            "Show me NASDAQ members",
            "NASDAQ component companies",
        ],
        related_terms=[
            "NASDAQ",
            "NASDAQ composite",
            "tech index",
            "index constituents",
            "index members",
            "NASDAQ components",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={},
        response_hints={},
        use_cases=["Financial analysis", "Investment research"],
    ),
    "dowjones_constituents": EndpointSemantics(
        client_name="index",
        method_name="get_dowjones_constituents",
        natural_description=(
            "Get current Dow Jones Industrial Average constituents. "
            "Returns list of 30 companies currently included in the DJIA."
        ),
        example_queries=[
            "Get Dow Jones constituents",
            "List Dow 30 companies",
            "What stocks are in the Dow Jones?",
            "Show me DJIA members",
            "Dow Jones Industrial Average components",
        ],
        related_terms=[
            "Dow Jones",
            "DJIA",
            "Dow 30",
            "blue chip stocks",
            "index constituents",
            "Dow components",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={},
        response_hints={},
        use_cases=["Financial analysis", "Investment research"],
    ),
    "historical_sp500": EndpointSemantics(
        client_name="index",
        method_name="get_historical_sp500",
        natural_description=(
            "Get historical S&P 500 constituent changes. "
            "Returns list of additions and removals from the S&P 500 over time."
        ),
        example_queries=[
            "Get S&P 500 historical changes",
            "Show me S&P 500 additions and removals",
            "Historical S&P 500 constituent changes",
            "When was Tesla added to S&P 500?",
            "S&P 500 index rebalancing history",
        ],
        related_terms=[
            "index changes",
            "index rebalancing",
            "constituent additions",
            "constituent removals",
            "S&P 500 history",
            "index composition changes",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={},
        response_hints={},
        use_cases=["Financial analysis", "Investment research"],
    ),
    "historical_nasdaq": EndpointSemantics(
        client_name="index",
        method_name="get_historical_nasdaq",
        natural_description=(
            "Get historical NASDAQ constituent changes. "
            "Returns list of additions and removals from the NASDAQ index over time."
        ),
        example_queries=[
            "Get NASDAQ historical changes",
            "Show me NASDAQ additions and removals",
            "Historical NASDAQ constituent changes",
            "NASDAQ index rebalancing history",
            "Track NASDAQ composition changes",
        ],
        related_terms=[
            "index changes",
            "index rebalancing",
            "constituent additions",
            "constituent removals",
            "NASDAQ history",
            "index composition changes",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={},
        response_hints={},
        use_cases=["Financial analysis", "Investment research"],
    ),
    "historical_dowjones": EndpointSemantics(
        client_name="index",
        method_name="get_historical_dowjones",
        natural_description=(
            "Get historical Dow Jones constituent changes. "
            "Returns list of additions and removals from the DJIA over time."
        ),
        example_queries=[
            "Get Dow Jones historical changes",
            "Show me Dow 30 additions and removals",
            "Historical DJIA constituent changes",
            "Dow Jones index rebalancing history",
            "Track Dow component changes",
        ],
        related_terms=[
            "index changes",
            "index rebalancing",
            "constituent additions",
            "constituent removals",
            "Dow Jones history",
            "DJIA composition changes",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={},
        response_hints={},
        use_cases=["Financial analysis", "Investment research"],
    ),
    "indexes_list": EndpointSemantics(
        client_name="index",
        method_name="get_indexes_list",
        natural_description=(
            "Get a list of all available market indexes. "
            "Returns index symbols, names, and exchange information."
        ),
        example_queries=[
            "List all available indexes",
            "Show me all market indexes",
            "What indexes are available?",
            "Get index directory",
            "All tradable indexes",
        ],
        related_terms=[
            "index list",
            "market indexes",
            "available indexes",
            "index directory",
            "index symbols",
            "stock indexes",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={},
        response_hints={},
        use_cases=["Market overview", "Index discovery"],
    ),
    "index_quote": EndpointSemantics(
        client_name="index",
        method_name="get_index_quote",
        natural_description=(
            "Get a full quote for a specific market index. "
            "Returns current value, change, day range, and 52-week range."
        ),
        example_queries=[
            "Get quote for S&P 500 index",
            "What is the current value of ^GSPC?",
            "Show me the Dow Jones index quote",
            "NASDAQ index current price",
            "Index quote for ^DJI",
        ],
        related_terms=[
            "index quote",
            "index price",
            "index value",
            "market index",
            "current index level",
            "index performance",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={"symbol": "Index symbol like ^GSPC, ^DJI, ^IXIC"},
        response_hints={},
        use_cases=["Market monitoring", "Portfolio tracking"],
    ),
    "index_quote_short": EndpointSemantics(
        client_name="index",
        method_name="get_index_quote_short",
        natural_description=(
            "Get a short quote for a specific market index. "
            "Returns price and volume only."
        ),
        example_queries=[
            "Get short quote for S&P 500",
            "Quick index price for ^DJI",
            "Short quote for NASDAQ index",
            "Fast index price lookup",
            "Brief index quote",
        ],
        related_terms=[
            "short quote",
            "quick quote",
            "index price",
            "brief quote",
            "fast quote",
            "index snapshot",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={"symbol": "Index symbol like ^GSPC, ^DJI, ^IXIC"},
        response_hints={},
        use_cases=["Quick market check", "Dashboard display"],
    ),
    "all_index_quotes": EndpointSemantics(
        client_name="index",
        method_name="get_all_index_quotes",
        natural_description=(
            "Get quotes for all available market indexes at once. "
            "Returns current values and changes for every index."
        ),
        example_queries=[
            "Get all index quotes",
            "Show me all market index prices",
            "List quotes for every index",
            "All index values today",
            "Market indexes overview",
        ],
        related_terms=[
            "all indexes",
            "market overview",
            "index quotes",
            "all market indexes",
            "index prices",
            "market summary",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={},
        response_hints={},
        use_cases=["Market overview", "Broad market monitoring"],
    ),
    "index_historical_eod_full": EndpointSemantics(
        client_name="index",
        method_name="get_index_historical",
        natural_description=(
            "Get full historical end-of-day price data for a market index. "
            "Returns OHLCV data with adjusted close and change metrics."
        ),
        example_queries=[
            "Get historical prices for S&P 500",
            "Show me ^GSPC price history",
            "Historical end-of-day data for Dow Jones index",
            "Index historical prices with volume",
            "Past index performance data",
        ],
        related_terms=[
            "historical prices",
            "index history",
            "price history",
            "EOD data",
            "OHLCV",
            "historical performance",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={
            "symbol": "Index symbol like ^GSPC, ^DJI, ^IXIC",
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
        },
        response_hints={},
        use_cases=["Backtesting", "Historical analysis", "Charting"],
    ),
    "index_historical_eod_light": EndpointSemantics(
        client_name="index",
        method_name="get_index_historical_light",
        natural_description=(
            "Get light historical end-of-day price data for a market index. "
            "Returns close price and volume only for faster retrieval."
        ),
        example_queries=[
            "Get light historical prices for S&P 500",
            "Show me ^GSPC closing price history",
            "Light historical data for NASDAQ index",
            "Index close prices over time",
            "Quick historical price lookup",
        ],
        related_terms=[
            "historical close",
            "light history",
            "closing prices",
            "price series",
            "index close history",
            "lightweight data",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={
            "symbol": "Index symbol like ^GSPC, ^DJI, ^IXIC",
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
        },
        response_hints={},
        use_cases=["Quick analysis", "Time series", "Performance tracking"],
    ),
    "index_intraday_1min": EndpointSemantics(
        client_name="index",
        method_name="get_index_intraday_1min",
        natural_description=(
            "Get 1-minute intraday price data for a market index. "
            "Returns granular intraday OHLCV data at 1-minute intervals."
        ),
        example_queries=[
            "Get 1-minute intraday data for S&P 500",
            "Show me ^GSPC 1-min chart data",
            "1-minute index prices for Dow Jones",
            "Intraday 1-min index data",
            "Minute-by-minute index prices",
        ],
        related_terms=[
            "intraday",
            "1-minute",
            "tick data",
            "minute bars",
            "real-time data",
            "intraday chart",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={
            "symbol": "Index symbol like ^GSPC, ^DJI, ^IXIC",
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
        },
        response_hints={},
        use_cases=["Day trading", "Intraday analysis", "Real-time charting"],
    ),
    "index_intraday_5min": EndpointSemantics(
        client_name="index",
        method_name="get_index_intraday_5min",
        natural_description=(
            "Get 5-minute intraday price data for a market index. "
            "Returns intraday OHLCV data at 5-minute intervals."
        ),
        example_queries=[
            "Get 5-minute intraday data for S&P 500",
            "Show me ^GSPC 5-min chart data",
            "5-minute index prices for NASDAQ",
            "Intraday 5-min index data",
            "Five-minute interval index prices",
        ],
        related_terms=[
            "intraday",
            "5-minute",
            "5-min bars",
            "intraday chart",
            "short-term data",
            "intraday intervals",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={
            "symbol": "Index symbol like ^GSPC, ^DJI, ^IXIC",
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
        },
        response_hints={},
        use_cases=["Day trading", "Intraday analysis", "Short-term charting"],
    ),
    "index_intraday_1hour": EndpointSemantics(
        client_name="index",
        method_name="get_index_intraday_1hour",
        natural_description=(
            "Get 1-hour intraday price data for a market index. "
            "Returns intraday OHLCV data at hourly intervals."
        ),
        example_queries=[
            "Get 1-hour intraday data for S&P 500",
            "Show me ^GSPC hourly chart data",
            "Hourly index prices for Dow Jones",
            "Intraday hourly index data",
            "One-hour interval index prices",
        ],
        related_terms=[
            "intraday",
            "hourly",
            "1-hour bars",
            "hourly chart",
            "intraday hourly",
            "hour intervals",
        ],
        category=SemanticCategory.MARKET_DATA,
        parameter_hints={
            "symbol": "Index symbol like ^GSPC, ^DJI, ^IXIC",
            "start_date": "Start date in YYYY-MM-DD format",
            "end_date": "End date in YYYY-MM-DD format",
        },
        response_hints={},
        use_cases=["Swing trading", "Intraday analysis", "Hourly charting"],
    ),
}
