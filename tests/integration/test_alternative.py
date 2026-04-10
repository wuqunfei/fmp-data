# tests/test_alternative_markets_client.py

from datetime import date

import pytest
import vcr

from fmp_data import FMPDataClient
from fmp_data.alternative.models import (
    Commodity,
    CommodityHistoricalPrice,
    CommodityHistoricalPriceLight,
    CommodityIntradayPrice,
    CommodityQuote,
    CommodityQuoteShort,
    CryptoHistoricalPrice,
    CryptoHistoricalPriceLight,
    CryptoIntradayPrice,
    CryptoPair,
    CryptoQuote,
    CryptoQuoteShort,
    ForexHistoricalPrice,
    ForexHistoricalPriceLight,
    ForexIntradayPrice,
    ForexPair,
    ForexQuote,
    ForexQuoteShort,
)

from .base import BaseTestCase


class TestAlternativeMarketsClientEndpoints(BaseTestCase):
    """Integration tests for AlternativeMarketsClient endpoints using VCR"""

    def test_get_crypto_list(self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR):
        """Test getting the list of cryptocurrencies"""
        with vcr_instance.use_cassette("alternative/crypto_list.yaml"):
            crypto_list = self._handle_rate_limit(
                fmp_client.alternative.get_crypto_list
            )
            assert isinstance(crypto_list, list)
            if crypto_list:
                assert all(isinstance(item, CryptoPair) for item in crypto_list)

    def test_get_crypto_quotes(self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR):
        """Test getting cryptocurrency quotes"""
        with vcr_instance.use_cassette("alternative/crypto_quotes.yaml"):
            quotes = self._handle_rate_limit(fmp_client.alternative.get_crypto_quotes)

            assert isinstance(quotes, list)
            if quotes:
                assert all(isinstance(quote, CryptoQuote) for quote in quotes)

    def test_get_crypto_quote(self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR):
        """Test getting a specific cryptocurrency quote"""
        with vcr_instance.use_cassette("alternative/crypto_quote.yaml"):
            quote = fmp_client.alternative.get_crypto_quote("BTCUSD")

            assert isinstance(quote, CryptoQuote)
            assert quote.symbol == "BTCUSD"

    def test_get_crypto_historical(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting cryptocurrency historical prices"""
        with vcr_instance.use_cassette("alternative/crypto_historical.yaml"):
            response = self._handle_rate_limit(
                fmp_client.alternative.get_crypto_historical,
                "BTCUSD",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 31),
            )
            historical_prices = response.historical
            assert isinstance(historical_prices, list)
            if historical_prices:
                assert all(
                    isinstance(price, CryptoHistoricalPrice)
                    for price in historical_prices
                )

    def test_get_crypto_intraday(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting cryptocurrency intraday prices"""
        with vcr_instance.use_cassette("alternative/crypto_intraday.yaml"):
            intraday_prices = self._handle_rate_limit(
                fmp_client.alternative.get_crypto_intraday, "BTCUSD", interval="5min"
            )
            assert isinstance(intraday_prices, list)
            if intraday_prices:
                assert all(
                    isinstance(price, CryptoIntradayPrice) for price in intraday_prices
                )

    def test_get_forex_list(self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR):
        """Test getting the list of forex pairs"""
        with vcr_instance.use_cassette("alternative/forex_list.yaml"):
            forex_list = self._handle_rate_limit(fmp_client.alternative.get_forex_list)

            assert isinstance(forex_list, list)
            if forex_list:
                assert all(isinstance(pair, ForexPair) for pair in forex_list)

    def test_get_forex_quotes(self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR):
        """Test getting forex quotes"""
        with vcr_instance.use_cassette("alternative/forex_quotes.yaml"):
            quotes = self._handle_rate_limit(fmp_client.alternative.get_forex_quotes)

            assert isinstance(quotes, list)
            if quotes:
                assert all(isinstance(quote, ForexQuote) for quote in quotes)

    def test_get_forex_quote(self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR):
        """Test getting a specific forex quote"""
        with vcr_instance.use_cassette("alternative/forex_quote.yaml"):
            quote = self._handle_rate_limit(
                fmp_client.alternative.get_forex_quote, "EURUSD"
            )

            assert isinstance(quote, ForexQuote)
            assert quote.symbol == "EURUSD"

    def test_get_forex_historical(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting forex historical prices"""
        with vcr_instance.use_cassette("alternative/forex_historical.yaml"):
            response = self._handle_rate_limit(
                fmp_client.alternative.get_forex_historical,
                "EURUSD",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 31),
            )
            historical_prices = response.historical

            assert isinstance(historical_prices, list)
            if historical_prices:
                assert all(
                    isinstance(price, ForexHistoricalPrice)
                    for price in historical_prices
                )

    def test_get_forex_intraday(self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR):
        """Test getting forex intraday prices"""
        with vcr_instance.use_cassette("alternative/forex_intraday.yaml"):
            intraday_prices = self._handle_rate_limit(
                fmp_client.alternative.get_forex_intraday, "EURUSD", interval="5min"
            )

            assert isinstance(intraday_prices, list)
            if intraday_prices:
                assert all(
                    isinstance(price, ForexIntradayPrice) for price in intraday_prices
                )

    def test_get_commodities_list(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting the list of commodities"""
        with vcr_instance.use_cassette("alternative/commodities_list.yaml"):
            commodities_list = self._handle_rate_limit(
                fmp_client.alternative.get_commodities_list,
            )

            assert isinstance(commodities_list, list)
            if commodities_list:
                assert all(
                    isinstance(commodity, Commodity) for commodity in commodities_list
                )

    def test_get_commodities_quotes(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting commodities quotes"""
        with vcr_instance.use_cassette("alternative/commodities_quotes.yaml"):
            quotes = self._handle_rate_limit(
                fmp_client.alternative.get_commodities_quotes,
            )

            assert isinstance(quotes, list)
            if quotes:
                assert all(isinstance(quote, CommodityQuote) for quote in quotes)

    def test_get_commodity_quote(self, fmp_client: FMPDataClient, vcr_instance):
        """Test getting a specific commodity quote"""
        with vcr_instance.use_cassette("alternative/commodity_quote.yaml"):
            quote = self._handle_rate_limit(
                fmp_client.alternative.get_commodity_quote, "ZOUSX"
            )

            assert isinstance(quote, CommodityQuote)
            assert quote.symbol == "ZOUSX"

    def test_get_commodity_historical(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ):
        """Test getting commodity historical prices"""
        with vcr_instance.use_cassette("alternative/commodity_historical.yaml"):
            response = self._handle_rate_limit(
                fmp_client.alternative.get_commodity_historical,
                "ZOUSX",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 1, 31),
            )
            historical_prices = response.historical

            assert isinstance(historical_prices, list)
            if historical_prices:
                assert all(
                    isinstance(price, CommodityHistoricalPrice)
                    for price in historical_prices
                )

    def test_get_commodity_intraday(
        self, fmp_client: FMPDataClient, vcr_instance: vcr.VCR
    ) -> None:
        """Test getting commodity intraday prices"""
        with vcr_instance.use_cassette("alternative/commodity_intraday.yaml"):
            intraday_prices = self._handle_rate_limit(
                fmp_client.alternative.get_commodity_intraday, "ZOUSX", interval="5min"
            )

            assert isinstance(intraday_prices, list)
            if intraday_prices:
                assert all(
                    isinstance(price, CommodityIntradayPrice)
                    for price in intraday_prices
                )

    @pytest.mark.skip(reason="endpoint returns 404 - requires higher API tier")
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
        """Test getting light cryptocurrency historical prices"""
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

    @pytest.mark.skip(reason="endpoint returns 404 - requires higher API tier")
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
        """Test getting light forex historical prices"""
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

    @pytest.mark.skip(reason="endpoint returns 404 - requires higher API tier")
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
        """Test getting light commodity historical prices"""
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
