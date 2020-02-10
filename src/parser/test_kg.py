import logging
import unittest

from src.fetcher import Fetcher
from src.parser import ParserKG


class TestParsingKyrgyzstan(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()
        logger.setLevel("DEBUG")

        self.parser = ParserKG(logger, Fetcher())

    # 1. Parse National Bank of Kyrgystan (api)
    def test_parse_nbkr(self, for_all=False):
        rates = self.parser.parse_nbkr()
        self.assert_rates("nbkr", rates)

    # 2. TODO: FIX Parse BTA Bank (web page)
    def test_parse_bta(self):
        rates = self.parser.parse_bta()
        self.assert_rates("bta", rates)

    # 3. Parse Demir Bank (web page)
    def test_parse_demir(self):
        rates = self.parser.parse_demir()
        self.assert_rates("demir", rates)

    # 4. Parse Baitushum Bank (web page)
    def test_parse_baitushum(self):
        rates = self.parser.parse_baitushum()
        self.assert_rates("baitushum", rates)

    # 5. Parse Bank Asia (web page)
    def test_parse_bankasia(self):
        rates = self.parser.parse_bankasia()
        self.assert_rates("bankasia", rates)

    # 6. Parse Bank Kicb (web page)
    def test_parse_kicb(self):
        rates = self.parser.parse_kicb()
        self.assert_rates("kicb", rates)

    # 7. Parse Ail Bank (web page)
    def test_parse_ab(self):
        rates = self.parser.parse_ab()
        self.assert_rates("ab", rates)

    # 8. Parse Capital bank (web page)
    def test_parse_capitalbank(self):
        rates = self.parser.parse_capitalbank()
        self.assert_rates("capitalbank", rates)

    # 9. Parse Doscredobank (web page)
    def test_parse_doscredo(self):
        rates = self.parser.parse_doscredo()
        self.assert_rates("doscredo", rates)

    # 10. Parse Сbk bank (web page)
    def test_parse_cbk(self):
        rates = self.parser.parse_cbk()
        self.assert_rates("cbk", rates)

    # 11. Parse Rsk bank (web page)
    def test_parse_rsk(self):
        rates = self.parser.parse_rsk()
        self.assert_rates("rsk", rates)

    # 12. Parse Optima bank (web page)
    def test_parse_optimabank(self):
        rates = self.parser.parse_optimabank()
        self.assert_rates("optimabank", rates)

    # 13. Parse Rib (web page)
    def test_parse_rib(self):
        rates = self.parser.parse_rib()
        self.assert_rates("rib", rates)

    # 14. Parse Kkb bank (web page)
    def test_parse_kkb(self):
        rates = self.parser.parse_kkb()
        self.assert_rates("kkb", rates)

    # 15. TODO: FIX Parse Kompanion bank (web page)
    def test_parse_kompanion(self):
        rates = self.parser.parse_kompanion()
        self.assert_rates("kompanion", rates)

    def assert_rates(self, bank, rates):
        print(bank + ":", rates)
        self.assertIsNotNone(rates['usd_buy'])
        self.assertIsNotNone(rates['usd_sale'])
        self.assertIsNotNone(rates['eur_buy'])
        self.assertIsNotNone(rates['eur_sale'])
        self.assertIsNotNone(rates['rub_buy'])
        self.assertIsNotNone(rates['rub_sale'])


if __name__ == "__main__":
    TestParsingKyrgyzstan()
