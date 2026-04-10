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

    def test_get_sp500_constituents(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting S&P 500 constituents"""
        with vcr_instance.use_cassette("index/sp500_constituents.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_sp500_constituents)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexConstituent)

    def test_get_nasdaq_constituents(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting Nasdaq constituents"""
        with vcr_instance.use_cassette("index/nasdaq_constituents.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_nasdaq_constituents)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexConstituent)

    def test_get_dowjones_constituents(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting Dow Jones constituents"""
        with vcr_instance.use_cassette("index/dowjones_constituents.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_dowjones_constituents
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexConstituent)

    def test_get_historical_sp500(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting historical S&P 500 changes"""
        with vcr_instance.use_cassette("index/historical_sp500.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_historical_sp500)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], HistoricalIndexConstituent)

    def test_get_historical_nasdaq(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting historical Nasdaq changes"""
        with vcr_instance.use_cassette("index/historical_nasdaq.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_historical_nasdaq)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], HistoricalIndexConstituent)

    def test_get_historical_dowjones(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting historical Dow Jones changes"""
        with vcr_instance.use_cassette("index/historical_dowjones.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_historical_dowjones)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], HistoricalIndexConstituent)

    def test_get_indexes_list(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting list of all available market indexes"""
        with vcr_instance.use_cassette("index/indexes_list.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_indexes_list)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexInfo)

    def test_get_index_quote(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting a full quote for a specific market index"""
        with vcr_instance.use_cassette("index/index_quote.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_quote, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexQuote)

    def test_get_index_quote_short(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting a short quote for a specific market index"""
        with vcr_instance.use_cassette("index/index_quote_short.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_quote_short, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexQuoteShort)

    def test_get_all_index_quotes(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting quotes for all available market indexes"""
        with vcr_instance.use_cassette("index/all_index_quotes.yaml"):
            results = self._handle_rate_limit(fmp_client.index.get_all_index_quotes)
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexQuote)

    def test_get_index_historical(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting full historical price data for a market index"""
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
        """Test getting light historical price data for a market index"""
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
        """Test getting 1-minute intraday price data for a market index"""
        with vcr_instance.use_cassette("index/index_intraday_1min.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_intraday_1min, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexIntradayPrice)

    def test_get_index_intraday_5min(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting 5-minute intraday price data for a market index"""
        with vcr_instance.use_cassette("index/index_intraday_5min.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_intraday_5min, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexIntradayPrice)

    def test_get_index_intraday_1hour(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting 1-hour intraday price data for a market index"""
        with vcr_instance.use_cassette("index/index_intraday_1hour.yaml"):
            results = self._handle_rate_limit(
                fmp_client.index.get_index_intraday_1hour, "^GSPC"
            )
            assert isinstance(results, list)
            if results:
                assert isinstance(results[0], IndexIntradayPrice)
