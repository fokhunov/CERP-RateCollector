import logging
import unittest

from src.fetcher import Fetcher
from src.parser import ParserUZ


class TestParsingUzbekistan(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()
        logger.setLevel("DEBUG")

        self.parser = ParserUZ(logger, Fetcher())

    # 1. Parse Central Bank of Uzbekistan (web page)
    def test_parse_cbu(self):
        rates = self.parser.parse_cbu()
        self.assert_rates("cbu", rates)

    @unittest.skip("CBU all rates")
    def test_parse_cbu_all(self):
        rates = self.parser.parse_cbu_all()
        self.assert_rates("cbu_all", rates)

    # 2. Parse National Bank of Uzbekistan (web page)
    def test_parse_nbu(self):
        rates = self.parser.parse_nbu()
        self.assert_rates("nbu", rates)

    # 3. Parse KDB (web page)
    def test_parse_kdb(self):
        rates = self.parser.parse_kdb()
        print("kdb:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])

    # 4. Parse XB (web page)
    def test_parse_xb(self):
        rates = self.parser.parse_xb()
        self.assert_rates("xb", rates)

    @unittest.skip("Mikrokreditbank rates")
    # 5. INACTIVE: Parse Mikrokreditbank (web page)
    def test_parse_mikrokreditbank(self):
        rates = self.parser.parse_mikrokreditbank()
        self.assert_rates("mikrokreditbank", rates)

    # 6. Parse Turonbank (web page)
    def test_parse_turonbank(self):
        rates = self.parser.parse_turonbank()
        self.assert_rates("turonbank", rates)

    # 7. Parse Aloqabank (web page)
    def test_parse_aloqabank(self):
        rates = self.parser.parse_aloqabank()
        print("aloqabank:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])

    # 8. Parse Aab (web page)
    def test_parse_aab(self):
        rates = self.parser.parse_aab()
        self.assert_rates("aab", rates)

    # 9. Parse Trustbank (web page)
    def test_parse_trustbank(self):
        rates = self.parser.parse_trustbank()
        self.assert_rates("trustbank", rates)

    # 10. Parse Ipakyulibank (web page)
    def test_parse_ipakyulibank(self):
        rates = self.parser.parse_ipakyulibank()
        print("ipakyulibank:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])

    # 11. Parse Savdogarbank (web page)
    def test_parse_savdogarbank(self):
        rates = self.parser.parse_savdogarbank()
        print("savdogarbank:", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])

    def assert_rates(self, bank, rates):
        print(bank + ":", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])


if __name__ == "__main__":
    TestParsingUzbekistan()
