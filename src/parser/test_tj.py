import logging
import unittest

from src.fetcher import Fetcher
from src.parser import ParserTJ


class TestParsingTajikistan(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()
        logger.setLevel("DEBUG")

        self.parser = ParserTJ(logger, Fetcher())

    # Parse Amonatbank (web page)
    def test_parse_amonat(self):
        rates = self.parser.parse_amonat()
        self.assert_rates("amonat", rates)

    # Parse Eskhata (web page)
    def test_parse_eskhata(self):
        rates = self.parser.parse_eskhata()
        self.assert_rates("eskhata", rates)

    # Parse First Microfinance (web page)
    def test_parse_fmfb(self):
        rates = self.parser.parse_fmfb()
        self.assert_rates("fmfb", rates)

    # Parse Tejaratbank (web page)
    def test_parse_tejaratbank(self):
        rates = self.parser.parse_tejaratbank()
        print("tejaratbank:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])

    # Parse Halykbank (web page)
    def test_parse_halykbank(self):
        rates = self.parser.parse_halykbank()
        self.assert_rates("halykbank", rates)

    # Parse Spitamen Bank (web page)
    def test_parse_spitamen(self):
        rates = self.parser.parse_spitamen()
        self.assert_rates("spitamen", rates)

    # Parse International Bank of Tajikistan (web page)
    def test_parse_ibt(self):
        rates = self.parser.parse_ibt()
        self.assert_rates("ibt", rates)

    # Parse Alif Bank (api)
    def test_parse_alif(self):
        rates = self.parser.parse_alif()
        self.assert_rates("alif", rates)

    # Parse National Bank of Tajikistan (api)
    def test_parse_nb(self):
        rates = self.parser.parse_nb()
        self.assert_rates("nb", rates)

    # Parse Humo (web page)
    def test_parse_humo(self):
        rates = self.parser.parse_humo()
        self.assert_rates("humo", rates)

    # Parse Finca (web page)
    def test_parse_finca(self):
        rates = self.parser.parse_finca()
        self.assert_rates("finca", rates)

    def assert_rates(self, bank, rates):
        print(bank + ":", rates)
        self.assertGreater(rates['usd_buy'], 0)
        self.assertGreater(rates['usd_sale'], 0)
        self.assertGreater(rates['eur_buy'], 0)
        self.assertGreater(rates['eur_sale'], 0)
        self.assertGreater(rates['rub_buy'], 0)
        self.assertGreater(rates['rub_sale'], 0)


if __name__ == "__main__":
    TestParsingTajikistan()
