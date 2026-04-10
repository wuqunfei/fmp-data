# fmp_data/index/client.py
from datetime import date

from fmp_data.base import EndpointGroup
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


class IndexClient(EndpointGroup):
    """Client for market index endpoints

    Provides methods to retrieve index constituents, historical changes,
    quotes, historical prices, and intraday data.
    """

    def get_sp500_constituents(self) -> list[IndexConstituent]:
        """Get current S&P 500 index constituents

        Returns:
            List of S&P 500 constituent companies
        """
        return self.client.request(SP500_CONSTITUENTS)

    def get_nasdaq_constituents(self) -> list[IndexConstituent]:
        """Get current NASDAQ index constituents

        Returns:
            List of NASDAQ constituent companies
        """
        return self.client.request(NASDAQ_CONSTITUENTS)

    def get_dowjones_constituents(self) -> list[IndexConstituent]:
        """Get current Dow Jones Industrial Average constituents

        Returns:
            List of Dow Jones constituent companies
        """
        return self.client.request(DOWJONES_CONSTITUENTS)

    def get_historical_sp500(self) -> list[HistoricalIndexConstituent]:
        """Get historical S&P 500 constituent changes

        Returns:
            List of historical constituent additions and removals
        """
        return self.client.request(HISTORICAL_SP500)

    def get_historical_nasdaq(self) -> list[HistoricalIndexConstituent]:
        """Get historical NASDAQ constituent changes

        Returns:
            List of historical constituent additions and removals
        """
        return self.client.request(HISTORICAL_NASDAQ)

    def get_historical_dowjones(self) -> list[HistoricalIndexConstituent]:
        """Get historical Dow Jones constituent changes

        Returns:
            List of historical constituent additions and removals
        """
        return self.client.request(HISTORICAL_DOWJONES)

    def get_indexes_list(self) -> list[IndexInfo]:
        """Get a list of all available market indexes

        Returns:
            List of available market indexes
        """
        return self.client.request(INDEXES_LIST)

    def get_index_quote(self, symbol: str) -> list[IndexQuote]:
        """Get a full quote for a specific market index

        Args:
            symbol: Index symbol (e.g., '^GSPC' for S&P 500)

        Returns:
            List of index quote data
        """
        return self.client.request(INDEX_QUOTE, symbol=symbol)

    def get_index_quote_short(self, symbol: str) -> list[IndexQuoteShort]:
        """Get a short quote for a specific market index

        Args:
            symbol: Index symbol (e.g., '^GSPC' for S&P 500)

        Returns:
            List of short index quote data
        """
        return self.client.request(INDEX_QUOTE_SHORT, symbol=symbol)

    def get_all_index_quotes(self) -> list[IndexQuote]:
        """Get quotes for all available market indexes

        Returns:
            List of quotes for all indexes
        """
        return self.client.request(ALL_INDEX_QUOTES)

    def get_index_historical(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[IndexHistoricalPrice]:
        """Get full historical end-of-day price data for a market index

        Args:
            symbol: Index symbol (e.g., '^GSPC')
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            List of historical index price data
        """
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
        """Get light historical end-of-day price data for a market index

        Args:
            symbol: Index symbol (e.g., '^GSPC')
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            List of light historical index price data
        """
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
        """Get 1-minute intraday price data for a market index

        Args:
            symbol: Index symbol (e.g., '^GSPC')
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            List of 1-minute intraday index price data
        """
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
        """Get 5-minute intraday price data for a market index

        Args:
            symbol: Index symbol (e.g., '^GSPC')
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            List of 5-minute intraday index price data
        """
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
        """Get 1-hour intraday price data for a market index

        Args:
            symbol: Index symbol (e.g., '^GSPC')
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            List of 1-hour intraday index price data
        """
        params: dict[str, str] = {"symbol": symbol}
        if start_date:
            params["start_date"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end_date"] = end_date.strftime("%Y-%m-%d")
        return self.client.request(INDEX_INTRADAY_1HOUR, **params)
