#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
from datetime import date

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

import base
from internal import currency
from internal import rate_helper as rate
from internal import time_helper as time


class ParserTJ(base.Parser):
    country = "tj"

    def __init__(self, logger, fetcher):
        base.Parser.__init__(self, self.country, logger, fetcher)

    # 1. Parse National Bank of Tajikistan (api)
    def parse_nb(self):
        result = self.fetcher.fetch(
            "http://nbt.tj/ru/kurs/export_xml.php?date=" + str(date.today()) + "&export=xmlout"
        )

        try:
            context = BeautifulSoup(result, 'html.parser')
            tags = context.find_all('valute')
            if tags:
                rates = {}
                for i in range(len(tags)):
                    item = tags[i]
                    code = item.find('charcode').getText()
                    value = rate.from_string(item.find('value').getText())

                    if code == "USD":
                        rates["usd_buy"] = rates["usd_sale"] = value
                    elif code == "EUR":
                        rates["eur_buy"] = rates["eur_sale"] = value
                    elif code == "RUB":
                        rates["rub_buy"] = rates["rub_sale"] = value

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # Parse National Bank of Tajikistan all rates (api)
    def parse_nb_all(self):
        result = self.fetcher.fetch(
            "http://nbt.tj/ru/kurs/export_xml.php?date=" + str(date.today()) + "&export=xmlout"
        )

        try:
            context = BeautifulSoup(result, 'html.parser')
            tags = context.find_all('valute')
            if tags:
                rates = {}
                for i in range(len(tags)):
                    item = tags[i]
                    code = item.find('charcode').getText()

                    if code in currency.ALLOWED:
                        nominal = int(item.find('nominal').getText())
                        value = rate.from_string(item.find('value').getText())

                        rates[code] = {
                            "code": code,
                            "nominal": nominal,
                            "value": value
                        }

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 2. Parse Agroinvestbank (web page)
    def parse_agro(self):
        result = self.fetcher.fetch(
            "http://www.agroinvestbank.tj/en/index.php"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="currencybox"))
            tags = context.find_all('li', class_="currency_lvl-2")
            if tags:

                return {
                    "usd_buy": rate.from_string(tags[3].getText()),
                    "eur_buy": rate.from_string(tags[4].getText()),
                    "rub_buy": rate.from_string(tags[5].getText()),
                    "usd_sale": rate.from_string(tags[6].getText()),
                    "eur_sale": rate.from_string(tags[7].getText()),
                    "rub_sale": rate.from_string(tags[8].getText()),
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 3. Parse Kazkomercbank (web page)
    def parse_kkb(self):
        now = time.now_date_key(self.country).split("-")
        params = {
            'day': now[2],
            'month': now[1],
            'year': now[0],
            'view': "Показать"
        }

        result = self.fetcher.fetch(
            "http://www.kkb.tj/ru/page/RatesExchanges",
            method="POST",
            data=params,
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('table', {'class': re.compile(r'tbl_text')})
            )
            tags = context.find_all('tr')
            if tags:
                usd = tags[1].find_all('td')
                eur = tags[2].find_all('td')
                rub = tags[3].find_all('td')

                return {
                    "usd_buy": rate.from_string(usd[2].getText()),
                    "usd_sale": rate.from_string(usd[3].getText()),
                    "eur_buy": rate.from_string(eur[2].getText()),
                    "eur_sale": rate.from_string(eur[3].getText()),
                    "rub_buy": rate.from_string(rub[2].getText()) / 10,
                    "rub_sale": rate.from_string(rub[3].getText()) / 10,
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 4. Parse Amonatbank (web page)
    def parse_amonat(self):
        result = self.fetcher.fetch(
            "http://www.amonatbonk.tj/en/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="tab2"))
            tags = context.find_all("span", {"class": "coll3"})
            if tags:
                usd = tags[0].text.strip().split("|")
                eur = tags[1].text.strip().split("|")
                rub = tags[2].text.strip().split("|")

                return {
                    "usd_buy": rate.from_string(usd[0]),
                    "usd_sale": rate.from_string(usd[1]),
                    "eur_buy": rate.from_string(eur[0]),
                    "eur_sale": rate.from_string(eur[1]),
                    "rub_buy": rate.from_string(rub[0]),
                    "rub_sale": rate.from_string(rub[1]),
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 5. Parse First Microfinance (web page)
    def parse_fmfb(self):
        result = self.fetcher.fetch(
            "http://www.fmfb.com.tj/en/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="kurs-valuta"))
            tags = context.find_all("table")
            tags = tags[1].find_all('tr')
            if tags:
                usd = tags[1].find_all('td')
                eur = tags[2].find_all('td')
                rub = tags[3].find_all('td')

                return {
                    "usd_buy": rate.from_string(usd[1].getText()),
                    "usd_sale": rate.from_string(usd[2].getText()),
                    "eur_buy": rate.from_string(eur[1].getText()),
                    "eur_sale": rate.from_string(eur[2].getText()),
                    "rub_buy": rate.from_string(rub[1].getText()),
                    "rub_sale": rate.from_string(rub[2].getText()),
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 6. Parse Eskhata (web page)
    def parse_eskhata(self):
        result = self.fetcher.fetch(
            "http://www.eskhata.com/mobile/?nomobile=0"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id='currency'))
            tags = context.find_all('tr')
            if tags:
                usd = tags[6].find_all('td')
                eur = tags[7].find_all('td')
                rub = tags[8].find_all('td')

                return {
                    "usd_buy": rate.from_string(usd[2].getText()),
                    "usd_sale": rate.from_string(usd[3].getText()),
                    "eur_buy": rate.from_string(eur[1].getText()),
                    "eur_sale": rate.from_string(eur[2].getText()),
                    "rub_buy": rate.from_string(rub[1].getText()),
                    "rub_sale": rate.from_string(rub[2].getText()),
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 7. Parse Tojiksodirot (web page)
    def parse_tsb(self):
        result = self.fetcher.fetch(
            "http://www.tsb.tj/en/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile(r'cur_state tsb')})
            )
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["usd_sale"] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["eur_sale"] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["rub_sale"] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 8. Parse Sohibkorbank (web page)
    def parse_scb(self):
        result = self.fetcher.fetch(
            "http://www.scb.tj/ru"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer(id="block-views-exchange-rate-block")
            )
            usd = context.find('div', class_="rates-usd")
            usd = usd.find_all('span', class_="field-content")
            eur = context.find('div', class_="rates-eur")
            eur = eur.find_all('span', class_="field-content")
            rub = context.find('div', class_="rates-rub")
            rub = rub.find_all('span', class_="field-content")

            if usd is not None & eur is not None & rub is not None:
                return {
                    "usd_buy": rate.from_string(usd[1].getText()),
                    "usd_sale": rate.from_string(usd[2].getText()),
                    "eur_buy": rate.from_string(eur[1].getText()),
                    "eur_sale": rate.from_string(eur[2].getText()),
                    "rub_buy": rate.from_string(rub[1].getText()),
                    "rub_sale": rate.from_string(rub[2].getText()),
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 9. Parse NBP Pakistan (web page)
    def parse_nbp(self):
        result = self.fetcher.fetch(
            "http://www.nbp.tj/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="block-block-6"))
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["usd_sale"] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["eur_sale"] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["rub_sale"] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 10. Parse International Bank of Tajikistan (web page)
    def parse_ibt(self):
        result = self.fetcher.fetch(
            "http://ibt.tj/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="-2"))
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["usd_sale"] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["eur_sale"] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue

                    if re.search(r'RUR', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates["rub_sale"] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 11. Parse Bank Asia (web page)
    def parse_bankasia(self):
        result = self.fetcher.fetch(
            "http://bankasia.org/en/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="tablepress-8"))
            tags = context.find_all('tr')
            if tags:
                usd = tags[1].findChildren('td')
                eur = tags[2].findChildren('td')
                rub = tags[3].findChildren('td')

                return {
                    "usd_buy": rate.from_string(usd[1].getText()),
                    "usd_sale": rate.from_string(usd[2].getText()),
                    "eur_buy": rate.from_string(eur[1].getText()),
                    "eur_sale": rate.from_string(eur[2].getText()),
                    "rub_buy": rate.from_string(rub[1].getText()),
                    "rub_sale": rate.from_string(rub[2].getText()),
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 12. Parse Bank of Progress Tajikistan (web page)
    def parse_brt(self):
        result = self.fetcher.fetch(
            "http://www.brt.tj/en/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile(r'sidebar2')})
            )
            tags = context.find_all('tr')
            tags = tags[1].findChildren('tr')
            if tags:
                usd = tags[1].findChildren('td')
                eur = tags[2].findChildren('td')
                rub = tags[3].findChildren('td')

                return {
                    "usd_buy": rate.from_string(usd[1].getText()),
                    "usd_sale": rate.from_string(usd[2].getText()),
                    "eur_buy": rate.from_string(eur[1].getText()),
                    "eur_sale": rate.from_string(eur[2].getText()),
                    "rub_buy": rate.from_string(rub[1].getText()),
                    "rub_sale": rate.from_string(rub[2].getText()),
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 13. Parse Imon International (api)
    def parse_imonintl(self):
        result = self.fetcher.fetch(
            "https://imon.tj/frontend/web/site/currency?lang=en-US"
        )

        try:
            result = json.loads(result)
            buy = result.get("IMON")
            sale = result.get("IMON1")
            rates = {}
            for r1 in buy:
                if buy[r1]['currency_from'] == "USD":
                    rates["usd_buy"] = rate.from_string(buy[r1]['rate'])
                if buy[r1]['currency_from'] == "EUR":
                    rates["eur_buy"] = rate.from_string(buy[r1]['rate'])
                if buy[r1]['currency_from'] == "RUB":
                    rates["rub_buy"] = rate.from_string(buy[r1]['rate'])
            for r2 in sale:
                if sale[r2]['currency_to'] == "USD":
                    rates["usd_sale"] = rate.from_string(sale[r2]['rate'])
                if sale[r2]['currency_to'] == "EUR":
                    rates["eur_sale"] = rate.from_string(sale[r2]['rate'])
                if sale[r2]['currency_to'] == "RUB":
                    rates["rub_sale"] = rate.from_string(sale[r2]['rate'])

            return rates

        except Exception as e:
            raise base.ParseError(e.message)

    # 14. Parse Commerce Bank of Tajikistan (web page)
    def parse_cbt(self):
        result = self.fetcher.fetch(
            "https://www.cbt.tj/ru/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="my-id"))
            tags = context.findChildren('li')[1]
            tags = tags.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.findChildren('th')[1].getText())
                        rates["usd_sale"] = rate.from_string(tag.findChildren('th')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.findChildren('th')[1].getText())
                        rates["eur_sale"] = rate.from_string(tag.findChildren('th')[2].getText())
                        continue

                    if re.search(r'RUS', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.findChildren('th')[1].getText())
                        rates["rub_sale"] = rate.from_string(tag.findChildren('th')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 15. Parse Spitamen Bank (web page)
    def parse_spitamen(self):
        result = self.fetcher.fetch(
            "https://www.spitamenbank.tj/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('ul', {'class': re.compile(r'conversation__list')})
            )
            tags = context.findChildren('li')[1]
            tags = tags.find_all('div', {"class": "conversation__row"})
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.find_all('div')[1].getText())
                        rates["usd_sale"] = rate.from_string(tag.find_all('div')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.find_all('div')[1].getText())
                        rates["eur_sale"] = rate.from_string(tag.find_all('div')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.find_all('div')[1].getText())
                        rates["rub_sale"] = rate.from_string(tag.find_all('div')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 16. Parse Humo (web page)
    def parse_humo(self):
        result = self.fetcher.fetch(
            "https://www.humo.tj/ru/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile('kursHUMO')})
            )
            tags = context.find_all('div', {"class": "kursBody"})
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.find_all('div')[1].getText())
                        rates["usd_sale"] = rate.from_string(tag.find_all('div')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.find_all('div')[1].getText())
                        rates["eur_sale"] = rate.from_string(tag.find_all('div')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.find_all('div')[1].getText())
                        rates["rub_sale"] = rate.from_string(tag.find_all('div')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 17. Parse Arvand (web page)
    def parse_arvand(self):
        result = self.fetcher.fetch(
            "http://www.arvand.tj/en/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile('kurs-arvand')})
            )
            tags = context.find_all('li')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'US', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.find_all('span')[2].getText())
                        rates["usd_sale"] = rate.from_string(tag.find_all('span')[3].getText())
                        continue

                    if re.search(r'EURO', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.find_all('span')[2].getText())
                        rates["eur_sale"] = rate.from_string(tag.find_all('span')[3].getText())
                        continue

                    if re.search(r'Ruble', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.find_all('span')[2].getText())
                        rates["rub_sale"] = rate.from_string(tag.find_all('span')[3].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # parse_all collects all rates for Tajikistan
    def parse_all(self):
        return self.handle_execute(
            {
                "tj_nbt": self.parse_nb,
                "tj_kkb": self.parse_kkb,
                "tj_amonat": self.parse_amonat,
                "tj_tsb": self.parse_tsb,
                "tj_ibt": self.parse_ibt,
                "tj_imonintl": self.parse_imonintl,
                "tj_eskhata": self.parse_eskhata,
                "tj_cbt": self.parse_cbt,
                "tj_spitamen": self.parse_spitamen,
                "tj_humo": self.parse_humo,
                "tj_arvand": self.parse_arvand,
                "tj_nbp": self.parse_nbp,
                "tj_agro": self.parse_agro,
            },
            self.parse_nb_all
        )
        # "tj_fmfb":    self.safe_parsing(self.parse_fmfb, "tj_fmfb"),              # new website

        # not working:
        # "tj_brt": self.safe_parsing(self.parse_brt, "tj_brt"),                    # off website
        # "tj_scb":     self.safe_parsing(self.parse_scb, "tj_scb"),                # off website
        # "tj_bankasia":  self.safe_parsing(self.parse_bankasia, "tj_bankasia"),    # off website
