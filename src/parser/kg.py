#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from src.parser import base
from src.parser.internal import currency
from src.parser.internal import rate_helper as rate


class ParserKG(base.Parser):
    country = "kg"

    def __init__(self, logger, fetcher):
        base.Parser.__init__(self, self.country, logger, fetcher)

    # 1. Parse National Bank of Kyrgystan (api)
    def parse_nbkr(self, for_all=False):
        result = self.fetcher.fetch(
            "http://www.nbkr.kg/XML/daily.xml"
        )

        try:
            context = BeautifulSoup(result, 'html.parser')
            tags = context.find_all('currency')
            if tags:
                rates = {}
                for i in range(len(tags)):
                    item = tags[i]
                    code = item['isocode']
                    value = rate.from_string(item.find('value').getText())

                    if for_all:
                        nominal = int(item.find('nominal').getText())

                        rates[code] = {
                            "code": code,
                            "nominal": nominal,
                            "value": value
                        }

                    else:
                        if code == "USD":
                            rates['usd_buy'] = rates['usd_sale'] = value
                        elif code == "EUR":
                            rates['eur_buy'] = rates['eur_sale'] = value
                        elif code == "RUB":
                            rates['rub_buy'] = rates['rub_sale'] = value
                        elif code == "KZT":
                            rates['kzt_buy'] = rates['kzt_sale'] = value

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    def parse_nbkr_all(self):
        # first get USD, EUR, RUB & KZT currencies
        rates = self.parse_nbkr(for_all=True)

        result = self.fetcher.fetch(
            "http://www.nbkr.kg/XML/weekly.xml"
        )

        try:
            context = BeautifulSoup(result, 'html.parser')
            tags = context.find_all('currency')
            if tags:
                for i in range(len(tags)):
                    item = tags[i]
                    code = item['isocode']

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

    # 2. Parse BTA Bank (web page)
    def parse_bta(self):
        result = self.fetcher.fetch(
            "http://www.btabank.kg/ru/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('tbody', {'class': re.compile(r'js-rates-cash')})
            )
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 3. Parse Demir Bank (web page)
    def parse_demir(self):
        result = self.fetcher.fetch(
            "http://www.demirbank.kg/ru/retail/home"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile(r'pricing-table')})
            )
            script = context.find("script").text
            pattern = re.compile("var currencies = (.*);")
            m = pattern.search(script).groups()[0]
            tags = json.loads(m)
            rates = {}
            for tag in tags:
                if tag['currency'] == 'USD':
                    rates['usd_buy'] = rate.from_string(tag['buy'])
                    rates['usd_sale'] = rate.from_string(tag['sell'])
                    continue

                if tag['currency'] == 'EUR':
                    rates['eur_buy'] = rate.from_string(tag['buy'])
                    rates['eur_sale'] = rate.from_string(tag['sell'])
                    continue

                if tag['currency'] == 'RUB':
                    rates['rub_buy'] = rate.from_string(tag['buy'])
                    rates['rub_sale'] = rate.from_string(tag['sell'])
                    continue

                if tag['currency'] == 'KZT':
                    rates['kzt_buy'] = rate.from_string(tag['buy'])
                    rates['kzt_sale'] = rate.from_string(tag['sell'])
                    continue

            return rates

        except Exception as e:
            raise base.ParseError(e.message)

    # 4. Parse Baitushum Bank (web page)
    def parse_baitushum(self):
        result = self.fetcher.fetch(
            "http://www.baitushum.kg/en/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="rates-widget"))
            tags = context.find_all('div', {'class': re.compile(r'rates')})[0]
            tags = tags.find_all('li')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('span')[0].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('span')[1].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('span')[0].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('span')[1].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('span')[0].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('span')[1].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('span')[0].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('span')[1].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 5. Parse Bank Asia (web page)
    def parse_bankasia(self):
        result = self.fetcher.fetch(
            "http://www.bankasia.kg/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="home"))
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 6. Parse Bank Kicb (web page)
    def parse_kicb(self):
        result = self.fetcher.fetch(
            "http://en.kicb.net/curency"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="head"))
            tags = context.find_all('tr')[2].find_all('td')[0].find_all('table')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 7. Parse Ail Bank (web page)
    def parse_ab(self):
        result = self.fetcher.fetch(
            "http://www.ab.kg/ru/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="tab1"))
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 8. Parse Capital bank (web page)
    def parse_capitalbank(self):
        result = self.fetcher.fetch(
            "http://www.capitalbank.kg/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer(id="block-views-arhiv-kursov-valyut-block-1")
            )
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue

                    if re.search(r'RUR', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[2].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 9. Parse Doscredobank (web page)
    def parse_doscredo(self):
        result = self.fetcher.fetch(
            "http://www.doscredobank.kg/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('table', {'class': re.compile(r'b-currency-rates')})
            )
            tags = context.find('table')
            tags = tags.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 10. Parse Сbk bank (web page)
    def parse_cbk(self):
        result = self.fetcher.fetch(
            "http://www.cbk.kg/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="rates-table"))
            usd = context.find_all("tr", class_="usd")[0].findChildren('td')
            eur = context.find_all("tr", class_="euro")[0].findChildren('td')
            rub = context.find_all("tr", class_="rub")[0].findChildren('td')
            kzt = context.find_all("tr", class_="kzt")[0].findChildren('td')

            return {
                'usd_buy': rate.from_string(usd[1].getText()),
                'usd_sale': rate.from_string(usd[2].getText()),
                'eur_buy': rate.from_string(eur[1].getText()),
                'eur_sale': rate.from_string(eur[2].getText()),
                'rub_buy': rate.from_string(rub[1].getText()),
                'rub_sale': rate.from_string(rub[2].getText()),
                'kzt_buy': rate.from_string(kzt[1].getText()),
                'kzt_sale': rate.from_string(kzt[2].getText()),
            }

        except Exception as e:
            raise base.ParseError(e.message)

    # 11. Parse Rsk bank (web page)
    def parse_rsk(self):
        result = self.fetcher.fetch(
            "http://www.rsk.kg/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile(r'course-item')})
            )
            tags = context.find_all('div')[0]
            tags = tags.find_all("div", class_="item")
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('div')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('div')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('div')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('div')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('div')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('div')[2].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('div')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('div')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 12. Parse Optima bank (web page)
    def parse_optimabank(self):
        result = self.fetcher.fetch(
            "https://www.optimabank.kg/en/currency-rates.html?view=default"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('table', {'class': 'currency_table'})
            )
            tags = context.find_all()
            tags = tags[0].find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'Доллар', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'Евро', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'рубль', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'тенге', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 13. Parse Rib (web page)
    def parse_rib(self):
        result = self.fetcher.fetch(
            "http://www.rib.kg/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="rosin"))
            tags = context.find_all("tr")
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 14. Parse Kkb bank (web page)
    def parse_kkb(self):
        result = self.fetcher.fetch(
            "http://kkb.kg/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="tab1"))
            tags = context.find_all("tr")
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 15. Parse Kompanion bank (web page)
    def parse_kompanion(self):
        result = self.fetcher.fetch(
            "http://www.kompanion.kg/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="nal"))
            tags = context.find_all("tr")
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                    if re.search(r'KZT', tag.text):
                        rates['kzt_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['kzt_sale'] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # parse_all collects all rates for Kyrgystan
    def parse_all(self):
        return self.handle_execute(
            {
                "kg_nbkr": self.parse_nbkr,
                "kg_bta": self.parse_bta,
                "kg_demir": self.parse_demir,
                "kg_baitushum": self.parse_baitushum,
                "kg_bankasia": self.parse_bankasia,
                "kg_kicb": self.parse_kicb,
                "kg_ab": self.parse_ab,
                "kg_capital": self.parse_capitalbank,
                "kg_doscredo": self.parse_doscredo,
                "kg_cbk": self.parse_cbk,
                "kg_rsk": self.parse_rsk,
                "kg_optimabank": self.parse_optimabank,
                "kg_rib": self.parse_rib,
                "kg_kkb": self.parse_kkb,
                "kg_kompanion": self.parse_kompanion,
            },
            self.parse_nbkr_all
        )
