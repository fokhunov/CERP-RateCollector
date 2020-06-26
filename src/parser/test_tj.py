import logging
import unittest

from src.fetcher import Fetcher
from src.parser import ParserTJ


class TestParsingTajikistan(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()
        logger.setLevel("DEBUG")

        self.parser = ParserTJ(logger, Fetcher())

    @unittest.skip("Agroinvestbank rates")
    # 1. Parse Agroinvestbank (web page)
    def test_parse_agro(self):
        rates = self.parser.parse_agro()
        self.assert_rates("agro", rates)

    # 2. Parse Amonatbank (web page)
    @unittest.skip("Amonatbank rates")
    def test_parse_amonat(self):
        rates = self.parser.parse_amonat()
        self.assert_rates("amonat", rates)

    @unittest.skip("Tojiksodirot rates")
    # 3. Parse Tojiksodirot (web page)
    def test_parse_tsb(self):
        rates = self.parser.parse_tsb()
        print("tsb:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])

    # 4. Parse Eskhata (web page)
    def test_parse_eskhata(self):
        rates = self.parser.parse_eskhata()
        self.assert_rates("eskhata", rates)

    # 5. Parse Tawhidbank (web page)
    def test_parse_tawhidbank(self):
        rates = self.parser.parse_tawhidbank()
        self.assert_rates("tawhidbank", rates)

    # 6. Parse First Microfinance (web page)
    def test_parse_fmfb(self):
        rates = self.parser.parse_fmfb()
        self.assert_rates("fmfb", rates)

    # 7. Parse Tejaratbank (web page)
    @unittest.skip("Tejaratbank rates")
    def test_parse_tejaratbank(self):
        rates = self.parser.parse_tejaratbank()
        self.assert_rates("tejaratbank", rates)

    # 8. Parse Halykbank (web page)
    def test_parse_halykbank(self):
        rates = self.parser.parse_halykbank()
        self.assert_rates("halykbank", rates)

    # 9. Parse Arvand (web page)
    def test_parse_arvand(self):
        rates = self.parser.parse_arvand()
        self.assert_rates("arvand", rates)

    # 10. Parse NBP Pakistan (web page)
    def test_parse_nbp(self):
        rates = self.parser.parse_nbp()
        print("nbp:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])

    # 11. Parse Spitamen Bank (web page)
    def test_parse_spitamen(self):
        rates = self.parser.parse_spitamen()
        self.assert_rates("spitamen", rates)

    # 12. Parse International Bank of Tajikistan (web page)
    def test_parse_ibt(self):
        rates = self.parser.parse_ibt()
        self.assert_rates("ibt", rates)

    # 13. Parse Commerce Bank of Tajikistan (web page)
    def test_parse_cbt(self):
        rates = self.parser.parse_cbt()
        self.assert_rates("cbt", rates)

    # 14. Parse Alif Bank (web page)
    def test_parse_alif(self):
        rates = self.parser.parse_alif()
        self.assert_rates("alif", rates)

    # 15. Parse National Bank of Tajikistan (api)
    def test_parse_nb(self):
        rates = self.parser.parse_nb()
        self.assert_rates("nb", rates)

    # 16. Parse Imon International (api)
    def test_parse_imonintl(self):
        rates = self.parser.parse_imonintl()
        self.assert_rates("imonintl", rates)

    # 17. Parse Humo (web page)
    def test_parse_humo(self):
        rates = self.parser.parse_humo()
        self.assert_rates("humo", rates)

    # 18. Parse Ardo Capital (web page)
    def test_parse_ardo(self):
        rates = self.parser.parse_ardo()
        self.assert_rates("ardo", rates)

    # 19. Parse Finca (web page)
    def test_parse_finca(self):
        rates = self.parser.parse_finca()
        self.assert_rates("finca", rates)

    def assert_rates(self, bank, rates):
        print(bank + ":", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])


if __name__ == "__main__":
    TestParsingTajikistan()
