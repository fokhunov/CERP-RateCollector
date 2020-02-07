import logging
import unittest

from src.fetcher import Fetcher
from src.parser import ParserTJ


class TestParsingTajikistan(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()
        logger.setLevel("DEBUG")

        self.parser = ParserTJ(logger, Fetcher())

    # 1. Parse Agroinvestbank (web page)
    def test_parse_agro(self):
        rates = self.parser.parse_agro()
        print("agro:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 2. Parse Amonatbank (web page)
    @unittest.skip("Amonatbank rates")
    def test_parse_amonat(self):
        rates = self.parser.parse_amonat()
        print("amonat:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

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
        print("eskhata:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 5. Parse Tawhidbank (web page)
    def test_parse_tawhidbank(self):
        rates = self.parser.parse_tawhidbank()
        print("tawhidbank:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 6. Parse First Microfinance (web page)
    def test_parse_fmfb(self):
        rates = self.parser.parse_fmfb()
        print("fmfb:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 7. Parse Tejaratbank (web page)
    @unittest.skip("Tejaratbank rates")
    def test_parse_tejaratbank(self):
        rates = self.parser.parse_tejaratbank()
        print("tejaratbank:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 8. Parse Kazkomercbank (web page)
    def test_parse_kkb(self):
        rates = self.parser.parse_kkb()
        print("kkb:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 9. Parse Arvand (web page)
    def test_parse_arvand(self):
        rates = self.parser.parse_arvand()
        print("arvand:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

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
        print("spitamen:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 12. Parse International Bank of Tajikistan (web page)
    def test_parse_ibt(self):
        rates = self.parser.parse_ibt()
        print("ibt:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 13. Parse Commerce Bank of Tajikistan (web page)
    def test_parse_cbt(self):
        rates = self.parser.parse_cbt()
        print("cbt:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 14. Parse Alif Bank (web page)
    def test_parse_alif(self):
        rates = self.parser.parse_alif()
        print("alif:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 15. Parse National Bank of Tajikistan (api)
    def test_parse_nb(self):
        rates = self.parser.parse_nb()
        print("nb:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 16. Parse Imon International (api)
    def test_parse_imonintl(self):
        rates = self.parser.parse_imonintl()
        print("imonintl:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])

    # 17. Parse Humo (web page)
    def test_parse_humo(self):
        rates = self.parser.parse_humo()
        print("humo:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])


if __name__ == "__main__":
    TestParsingTajikistan()
