#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from src.parser import base
from src.parser.internal import currency
from src.parser.internal import rate_helper as rate


class ParserKZ(base.Parser):
    country = "kz"

    def __init__(self, logger, fetcher):
        base.Parser.__init__(self, self.country, logger, fetcher)

    # 1. Parse National Bank of Kazakhstan (api)
    def parse_nbk(self):
        result = self.fetcher.fetch(
            "http://www.nationalbank.kz/rss/rates_all.xml"
        )

        try:
            context = BeautifulSoup(result, 'html.parser')
            tags = context.find_all('item')
            if tags:
                rates = {}
                for i in range(len(tags)):
                    item = tags[i]
                    code = item.find('title').getText()
                    value = rate.from_string(item.find('description').getText())

                    if code == "USD":
                        rates['usd_buy'] = rates['usd_sale'] = value
                    elif code == "EUR":
                        rates['eur_buy'] = rates['eur_sale'] = value
                    elif code == "RUB":
                        rates['rub_buy'] = rates['rub_sale'] = value

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    def parse_nbk_all(self):
        result = self.fetcher.fetch(
            "http://www.nationalbank.kz/rss/rates_all.xml"
        )

        try:
            context = BeautifulSoup(result, 'html.parser')
            tags = context.find_all('item')
            if tags:
                rates = {}
                for i in range(len(tags)):
                    item = tags[i]
                    code = item.find('title').getText()

                    if code in currency.ALLOWED:
                        nominal = int(item.find('quant').getText())
                        value = rate.from_string(item.find('description').getText())

                        rates[code] = {
                            'code': code,
                            'nominal': nominal,
                            'value': value
                        }

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 2. Parse Asiacreditbank (web page)
    def parse_asiacreditbank(self):
        result = self.fetcher.fetch(
            "http://www.asiacreditbank.kz/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="exchange-11"))
            tags = context.find_all('tr')
            if tags:

                return {
                    'usd_buy': rate.from_string(tags[1].find_all('td')[1].getText()),
                    'usd_sale': rate.from_string(tags[1].find_all('td')[3].getText()),
                    'eur_buy': rate.from_string(tags[2].find_all('td')[1].getText()),
                    'eur_sale': rate.from_string(tags[2].find_all('td')[3].getText()),
                    'rub_buy': rate.from_string(tags[3].find_all('td')[1].getText()),
                    'rub_sale': rate.from_string(tags[3].find_all('td')[3].getText()),
                }

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 3. Parse Deltabank (api)
    def parse_deltabank(self):
        result = self.fetcher.fetch(
            "http://www.deltabank.kz/ajax_get_rates.php"
        )

        try:
            context = BeautifulSoup(result, "html.parser")
            usd = context.find_all('usd')
            eur = context.find_all('eur')
            rub = context.find_all('rur')

            return {
                'usd_buy': rate.from_string(usd[0].text),
                'usd_sale': rate.from_string(usd[1].text),
                'eur_buy': rate.from_string(eur[0].text),
                'eur_sale': rate.from_string(eur[1].text),
                'rub_buy': rate.from_string(rub[0].text),
                'rub_sale': rate.from_string(rub[1].text),
            }

        except Exception as e:
            raise base.ParseError(e.message)

    # 4. Parse Qazaqbanki (web page)
    def parse_qazaqbanki(self):
        result = self.fetcher.fetch(
            "http://qazaqbanki.kz/rus/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="currency-41"))
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

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 5. Parse Atfbank (web page)
    def parse_atfbank(self):
        result = self.fetcher.fetch(
            "https://www.atfbank.kz/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('table', {'class': re.compile(r'rate-tb')})
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

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 6. Parse RBK Bank (web page)
    def parse_bankrbk(self):
        result = self.fetcher.fetch(
            "https://www.bankrbk.kz/rus"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile(r'exchange')})
            )
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[3].getText())
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 7. Parse Bankastana (web page)
    def parse_bankastana(self):
        result = self.fetcher.fetch(
            "https://www.bankastana.kz/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="exchange_21"))
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    parts = tag.text.split()
                    if parts[0] == "USD":
                        rates['usd_buy'] = rate.from_string(parts[1])
                        rates['usd_sale'] = rate.from_string(parts[2])
                        continue

                    if parts[0] == "EUR":
                        rates['eur_buy'] = rate.from_string(parts[1])
                        rates['eur_sale'] = rate.from_string(parts[2])
                        continue

                    if parts[0] == "RUB":
                        rates['rub_buy'] = rate.from_string(parts[1])
                        rates['rub_sale'] = rate.from_string(parts[2])
                        continue

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 8. Parse Bcc (web page) todo: is it alive ?
    def parse_bcc(self):
        result = self.fetcher.fetch(
            "https://www.bcc.kz/about/kursy-valyut/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile(r'bcc_full')})
            )
            tags = context.find_all('tr')
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

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 9. Parse Expocredit Bank (web page) todo: is it alive ?
    def parse_expocredit(self):
        result = self.fetcher.fetch(
            "http://expocredit.kz/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="quotes_tab_1"))
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

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 10. Parse Eubank (web page)
    def parse_eubank(self):
        result = self.fetcher.fetch(
            "https://www.eubank.kz/"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile(r'exchange')})
            )
            tags = context.find_all('table')[0].find_all('tr')
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

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 11. Parse Qazkom Bank (web page)
    def parse_qazkom(self):
        result = self.fetcher.fetch(
            "http://www.qazkom.kz/"
        )

        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="KAZKOM"))
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

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 12. Parse Tsb Bank (web page)
    def parse_tsb(self):
        result = self.fetcher.fetch(
            "https://www.tsb.kz/ajax_get_tsbrates.php?type=tsb"
        )

        try:
            context = BeautifulSoup(result, 'html.parser')

            return {
                'usd_buy': rate.from_string(context.find('usd_buy').text),
                'usd_sale': rate.from_string(context.find('usd_sell').text),
                'eur_buy': rate.from_string(context.find('eur_buy').text),
                'eur_sale': rate.from_string(context.find('eur_sell').text),
                'rub_buy': rate.from_string(context.find('rub_buy').text),
                'rub_sale': rate.from_string(context.find('rub_sell').text),
            }

        except Exception as e:
            raise base.ParseError(e.message)

    # 13. Parse Capitalbank (web page)
    def parse_capitalbank(self):
        result = self.fetcher.fetch(
            "http://www.capitalbank.kz/ru/kursy_valyut"
        )

        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile(r'kursy_valyut')})
            )
            tags = context.find_all("div", class_="row")[1].find_all('ul')
            if tags:
                rates = {}
                buy = tags[0].find_all('li')
                sale = tags[1].find_all('li')

                for r in buy:
                    parts = r.text.split()
                    if len(parts) != 2:
                        continue
                    if parts[0] == "USD":
                        rates['usd_buy'] = rate.from_string(parts[1])
                    elif parts[0] == "EUR":
                        rates['eur_buy'] = rate.from_string(parts[1])
                    elif parts[0] == "RUB":
                        rates['rub_buy'] = rate.from_string(parts[1])

                for r in sale:
                    parts = r.text.split()
                    if len(parts) != 2:
                        continue
                    if parts[0] == "USD":
                        rates['usd_sale'] = rate.from_string(parts[1])
                    elif parts[0] == "EUR":
                        rates['eur_sale'] = rate.from_string(parts[1])
                    elif parts[0] == "RUB":
                        rates['rub_sale'] = rate.from_string(parts[1])

                return rates

            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # parse_all collects all rates for Tajikistan
    def parse_all(self):
        return self.handle_execute(
            {
                "kz_nbk": self.parse_nbk,
                "kz_asiacreditbank": self.parse_asiacreditbank,
                "kz_deltabank": self.parse_deltabank,
                "kz_qazaqbanki": self.parse_qazaqbanki,
                "kz_atfbank": self.parse_atfbank,
                "kz_bankrbk": self.parse_bankrbk,
                "kz_bankastana": self.parse_bankastana,
                "kz_bcc": self.parse_bcc,
                "kz_eubank": self.parse_eubank,
                "kz_qazkom": self.parse_qazkom,
                "kz_tsb": self.parse_tsb,
                "kz_capitalbank": self.parse_capitalbank,
                "kz_expocredit": self.parse_expocredit,
            },
            self.parse_nbk_all
        )
