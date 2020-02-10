#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from src.parser import base
from src.parser.internal import currency
from src.parser.internal import rate_helper as rate


class ParserUZ(base.Parser):
    country = "uz"

    def __init__(self, logger, fetcher):
        base.Parser.__init__(self, self.country, logger, fetcher)

    # 1. Parse Central Bank of Uzbekistan (web page)
    def parse_cbu(self):
        result = self.fetcher.fetch("http://www.cbu.uz/ru/")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer('div', {'class': re.compile(r'rates-list')})
            )
            tags = context.find_all('li')
            if tags:
                rates = {}
                for i in range(len(tags)):
                    parts = tags[i].getText().split()
                    code = parts[1]
                    value = rate.from_string(parts[3])
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

    # Parse Central Bank of Uzbekistan all rates (web page)
    def parse_cbu_all(self):
        result = self.fetcher.fetch("http://www.cbu.uz/ru/")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer('div', {'class': re.compile(r'rates-list')})
            )
            tags = context.find_all('li')
            if tags:
                rates = {}
                for i in range(len(tags)):
                    parts = tags[i].getText().split()
                    code = parts[1]
                    if code in currency.ALLOWED:
                        nominal = int(parts[0])
                        value = rate.from_string(parts[3])
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

    # 2. Parse National Bank of Uzbekistan (web page)
    def parse_nbu(self):
        result = self.fetcher.fetch("https://nbu.uz/en/exchange-rates/")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer('div', {'class': re.compile(r'kursdata')})
            )
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.find_all('td')[2].getText())
                        rates["usd_sale"] = rate.from_string(tag.find_all('td')[3].getText())
                        continue
                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.find_all('td')[2].getText())
                        rates["eur_sale"] = rate.from_string(tag.find_all('td')[3].getText())
                        continue
                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.find_all('td')[2].getText())
                        rates["rub_sale"] = rate.from_string(tag.find_all('td')[3].getText())
                        continue
                return rates
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 3. Parse KDB (web page)
    def parse_kdb(self):
        result = self.fetcher.fetch("https://kdb.uz/ru/interactive-services/exchange-rates")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer(id="kdb")
            )
            tags = context.find_all('td')
            if tags and len(tags) > 2:
                usd = tags[0].text.strip().split("/")
                eur = tags[1].text.strip().split("/")
                return {
                    "usd_buy": rate.from_string(usd[0]),
                    "usd_sale": rate.from_string(usd[1]),
                    "eur_buy": rate.from_string(eur[0]),
                    "eur_sale": rate.from_string(eur[1]),

                    # absent
                    # rates['rub_buy'] = string_to_int(tags.findChildren('td')[3].getText())
                    # rates['rub_sale'] = string_to_int(tags.findChildren('td')[4].getText())
                }
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 4. Parse XB (web page)
    def parse_xb(self):
        result = self.fetcher.fetch("http://www.xb.uz/ru")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer('div', {'class': re.compile(r'currency__table')})
            )
            tags = context.find_all('div', class_='currency__amount')
            if tags:
                buy = tags[0].find_all('div')
                sale = tags[1].find_all('div')
                return {
                    "usd_buy": rate.from_string(buy[2].getText()),
                    "usd_sale": rate.from_string(sale[2].getText()),
                    "eur_buy": rate.from_string(buy[1].getText()),
                    "eur_sale": rate.from_string(sale[1].getText()),
                    "rub_buy": rate.from_string(buy[5].getText()),
                    "rub_sale": rate.from_string(buy[5].getText()),
                }
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 5. Parse Mikrokreditbank (web page)
    def parse_mikrokreditbank(self):
        result = self.fetcher.fetch("https://mikrokreditbank.uz/ru/")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer('div', {'class': 'curs_block'})
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

    # 6. Parse Turonbank (web page)
    def parse_turonbank(self):
        result = self.fetcher.fetch("http://www.turonbank.uz/")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer('div', {'class': r'exchange-rates'})
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

    # 7. Parse Aloqabank (web page)
    def parse_aloqabank(self):
        result = self.fetcher.fetch("http://www.aloqabank.uz/ru/page/interactive/rates")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer(id="currencies-table")
            )
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates['usd_buy'] = rate.from_string(tag.findChildren('td')[5].getText())
                        rates['usd_sale'] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue
                    if re.search(r'EUR', tag.text):
                        rates['eur_buy'] = rate.from_string(tag.findChildren('td')[5].getText())
                        rates['eur_sale'] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue
                    if re.search(r'RUB', tag.text):
                        rates['rub_buy'] = rate.from_string(tag.findChildren('td')[5].getText())
                        rates['rub_sale'] = rate.from_string(tag.findChildren('td')[4].getText())
                        continue
                return rates
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 8. Parse Aab (web page)
    def parse_aab(self):
        result = self.fetcher.fetch("http://www.aab.uz/ru/")
        try:
            context = BeautifulSoup(
                result,
                'html.parser',
                parse_only=SoupStrainer('div', {'class': 'rates-list'})
            )
            tags = context.find_all('div', class_='col-xs-3')
            if tags:
                buy = tags[0].find_all('div', class_='item')
                sale = tags[1].find_all('div', class_='item')
                return {
                    'usd_buy': rate.from_string(buy[1].text),
                    'usd_sale': rate.from_string(sale[1].text),
                    'eur_buy': rate.from_string(buy[2].text),
                    'eur_sale': rate.from_string(sale[2].text),
                    'rub_buy': rate.from_string(buy[3].text),
                    'rub_sale': rate.from_string(sale[3].text),
                }
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 9. Parse Trustbank (web page)
    def parse_trustbank(self):
        result = self.fetcher.fetch("http://trustbank.uz/ru/services/exchange-rates/")
        try:
            context = BeautifulSoup(result, 'html.parser', parse_only=SoupStrainer(id='currency-archive'))
            tags = context.find_all('div', class_='col-xs-1')
            if tags:
                buy = tags[2].find_all('div', class_='item')
                sale = tags[3].find_all('div', class_='item')
                return {
                    'usd_buy': rate.from_string(buy[1].text),
                    'usd_sale': rate.from_string(sale[1].text),
                    'eur_buy': rate.from_string(buy[2].text),
                    'eur_sale': rate.from_string(sale[2].text),
                    'rub_buy': rate.from_string(buy[4].text),
                    'rub_sale': rate.from_string(sale[4].text),
                }
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 10. Parse Ipakyulibank (web page)
    def parse_ipakyulibank(self):
        result = self.fetcher.fetch("https://wi.ipakyulibank.uz/kurs/kurs4.php")
        try:
            context = BeautifulSoup(result, 'html.parser')
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

    # 11. Parse Savdogarbank (web page)
    def parse_savdogarbank(self):
        result = self.fetcher.fetch("http://www.savdogarbank.uz/ru/")
        try:
            context = BeautifulSoup(result, 'html.parser', parse_only=SoupStrainer('div', {'class': 'b-rates'}))
            tags = context.find_all('tr')
            if tags:
                buy = tags[2].find_all('td')
                sale = tags[3].find_all('td')
                return {
                    'usd_buy': rate.from_string(buy[1].text),
                    'usd_sale': rate.from_string(sale[1].text),
                    'eur_buy': rate.from_string(buy[2].text),
                    'eur_sale': rate.from_string(sale[2].text),
                    # absent
                    # rates['rub_buy'] = string_to_int(buy[4].text)
                    # rates['rub_sale'] = string_to_int(sale[4].text)
                }
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # parse_all collects all rates for Uzbekistan
    def parse_all(self):
        return self.handle_execute(
            {
                "uz_cbu": self.parse_cbu,
                "uz_nbu": self.parse_nbu,
                "uz_kdb": self.parse_kdb,
                "uz_xb": self.parse_xb,
                "uz_mikrokreditbank": self.parse_mikrokreditbank,
                "uz_turonbank": self.parse_turonbank,
                "uz_aloqabank": self.parse_aloqabank,
                "uz_aab": self.parse_aab,
                "uz_trustbank": self.parse_trustbank,
                "uz_ipakyulibank": self.parse_ipakyulibank,
                "uz_savdogarbank": self.parse_savdogarbank,
            },
            self.parse_cbu_all
        )
