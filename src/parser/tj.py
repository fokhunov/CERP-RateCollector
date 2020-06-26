#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
from datetime import date

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from src.parser import base
from src.parser.internal import currency
from src.parser.internal import rate_helper as rate
from src.parser.internal import time_helper as time


class ParserTJ(base.Parser):
    country = "tj"

    def __init__(self, logger, fetcher):
        base.Parser.__init__(self, self.country, logger, fetcher)

    # 1. Parse Agroinvestbank (web page)
    def parse_agro(self):
        result = self.fetcher.fetch("http://www.agroinvestbank.tj/en/index.php")
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

    # 2. Parse Amonatbank (web page)
    def parse_amonat(self):
        result = self.fetcher.fetch("http://www.amonatbonk.tj/en/")
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

    # 3. Parse Tojiksodirot (web page)
    def parse_tsb(self):
        result = self.fetcher.fetch("http://www.tsb.tj/en/")
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

    # 4. Parse Eskhata (web page)
    def parse_eskhata(self):
        result = self.fetcher.fetch("http://www.eskhata.com/mobile/?nomobile=0")
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

    # 5. Parse Tawhidbank (web page)
    def parse_tawhidbank(self):
        result = self.fetcher.fetch("http://www.tawhidbank.tj/")
        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id='nbt'))
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates["usd_sale"] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue
                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates["eur_sale"] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue
                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates["rub_sale"] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue
                return rates
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 6. Parse First Microfinance (web page)
    def parse_fmfb(self):
        result = self.fetcher.fetch("https://fmfb.tj/en/")
        try:
            context = BeautifulSoup(result, "html.parser")
            context = context.findAll("div", {"class": "new-currency-last"})
            tags = context[0].find_all("div")
            if tags:
                return {
                    "usd_buy": rate.from_string(tags[3].getText()),
                    "usd_sale": rate.from_string(tags[7].getText()),
                    "eur_buy": rate.from_string(tags[4].getText()),
                    "eur_sale": rate.from_string(tags[8].getText()),
                    "rub_buy": rate.from_string(tags[5].getText()),
                    "rub_sale": rate.from_string(tags[9].getText()),
                }
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 7. Parse Tejaratbank (web page)
    def parse_tejaratbank(self):
        result = self.fetcher.fetch("http://tejaratbank.tj/en/")
        try:
            context = BeautifulSoup(result, "html.parser",
                                    parse_only=SoupStrainer(id='currencyconverter_minimalistic-2'))
            tags = context.find_all('span', {"class": "currencyconverter-minimalistic-currency-price"})
            if tags:
                return {
                    "usd_buy": rate.from_string(tags[0].getText()),
                    "usd_sale": rate.from_string(tags[0].getText()),
                    "eur_buy": rate.from_string(tags[1].getText()),
                    "eur_sale": rate.from_string(tags[1].getText()),
                    "rub_buy": rate.from_string(tags[2].getText()),
                    "rub_sale": rate.from_string(tags[2].getText()),
                }
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 8. Parse Halykbank (web page)
    def parse_halykbank(self):
        result = self.fetcher.fetch("https://halykbank.tj/en/exchange-rates")
        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id='category1'))
            tags = context.find_all('div', {"class": "currency__columns"})
            if tags:
                rates = {}
                for tag in tags:
                    values = tag.find_all('div', {"class": "currency__value"})

                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(values[0].getText())
                        rates["usd_sale"] = rate.from_string(values[1].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(values[0].getText())
                        rates["eur_sale"] = rate.from_string(values[1].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(values[0].getText())
                        rates["rub_sale"] = rate.from_string(values[1].getText())
                        continue

                return rates
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 9. Parse Arvand (web page)
    def parse_arvand(self):
        result = self.fetcher.fetch("http://www.arvand.tj/en/")
        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile('currencyContainer')})
            )
            context = context.find_all('table', {"class": "exrate"})
            context = context[1]
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.find_all('td')[1].getText())
                        rates["usd_sale"] = rate.from_string(tag.find_all('td')[2].getText())
                        continue

                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.find_all('td')[1].getText())
                        rates["eur_sale"] = rate.from_string(tag.find_all('td')[2].getText())
                        continue

                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.find_all('td')[1].getText())
                        rates["rub_sale"] = rate.from_string(tag.find_all('td')[2].getText())
                        continue

                return rates
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 10. Parse NBP Pakistan (web page)
    def parse_nbp(self):
        result = self.fetcher.fetch("http://www.nbp.tj/")
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

    # 11. Parse Spitamen Bank (web page)
    def parse_spitamen(self):
        result = self.fetcher.fetch("https://www.spitamenbank.tj/")
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

    # 12. Parse International Bank of Tajikistan (web page)
    def parse_ibt(self):
        result = self.fetcher.fetch("http://ibt.tj/")
        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id="ibt"))
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'USD', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates["usd_sale"] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue
                    if re.search(r'EUR', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates["eur_sale"] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue
                    if re.search(r'RUB', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.findChildren('td')[0].getText())
                        rates["rub_sale"] = rate.from_string(tag.findChildren('td')[1].getText())
                        continue
                return rates
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 13. Parse Commerce Bank of Tajikistan (web page)
    def parse_cbt(self):
        result = self.fetcher.fetch("https://cbt.tj/")
        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('tbody', {'class': re.compile(r'cbt-currency')})
            )
            tags = context.find_all('tr')
            if tags:
                rates = {}
                for tag in tags:
                    if re.search(r'Доллары', tag.text):
                        rates["usd_buy"] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates["usd_sale"] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue
                    if re.search(r'Евро', tag.text):
                        rates["eur_buy"] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates["eur_sale"] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue
                    if re.search(r'Рос', tag.text):
                        rates["rub_buy"] = rate.from_string(tag.findChildren('td')[1].getText())
                        rates["rub_sale"] = rate.from_string(tag.findChildren('td')[2].getText())
                        continue
                return rates
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # 14. Parse Alif Bank (web page)
    def parse_alif(self):
        currencies = ["usd", "eur", "rub"]
        now = time.now_date_key(self.country).split("-")
        param_date = now[0] + "-" + now[1] + "-" + now[2]
        endpoint = "https://alif.tj/api/currency/index.php?date=" + param_date + "&currency="
        rates = {}
        for c in currencies:
            result = self.fetcher.fetch(endpoint + c)
            try:
                result = json.loads(result)
                buy = rate.from_string(result.get("buy_value"))
                sale = rate.from_string(result.get("sell_value"))
                if c == "usd":
                    rates["usd_buy"] = buy
                    rates["usd_sale"] = sale
                if c == "eur":
                    rates["eur_buy"] = buy
                    rates["eur_sale"] = sale
                if c == "rub":
                    rates["rub_buy"] = buy
                    rates["rub_sale"] = sale
            except Exception as e:
                raise base.ParseError(e.message)
        return rates

    # 15. Parse National Bank of Tajikistan (api)
    def parse_nb(self):
        result = self.fetcher.fetch("http://nbt.tj/ru/kurs/export_xml.php?date=" + str(date.today()) + "&export=xmlout")
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
        result = self.fetcher.fetch("http://nbt.tj/ru/kurs/export_xml.php?date=" + str(date.today()) + "&export=xmlout")
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

    # 16. Parse Imon International (api)
    def parse_imonintl(self):
        result = self.fetcher.fetch("https://imon.tj/frontend/web/site/currency?lang=en-US")
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

    # 17. Parse Humo (web page)
    def parse_humo(self):
        result = self.fetcher.fetch("https://www.humo.tj/ru/")
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

    # 18. Parse Ardo Capital (web page)
    def parse_ardo(self):
        result = self.fetcher.fetch("http://ardocapital.tj/en/")
        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('div', {'class': re.compile('kursArdo')})
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

    # 19. Parse Finca (web page)
    def parse_finca(self):
        result = self.fetcher.fetch("https://www.finca.tj/en/")
        try:
            context = BeautifulSoup(
                result,
                "html.parser",
                parse_only=SoupStrainer('table', {'class': re.compile('exchange_rate_table')})
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

    # parse_all collects all rates for Tajikistan
    def parse_all(self):
        return self.handle_execute(
            {
                # "tj_agro": self.parse_agro, - bank in bankruptcy
                "tj_amonat": self.parse_amonat,
                # "tj_tsb": self.parse_tsb,   - bank in bankruptcy
                "tj_eskhata": self.parse_eskhata,
                "tj_tawhidbank": self.parse_tawhidbank,
                "tj_fmfb": self.parse_fmfb,
                "tj_parse_tejaratbank": self.parse_tejaratbank,
                "tj_halykbank": self.parse_halykbank,
                "tj_arvand": self.parse_arvand,
                "tj_nbp": self.parse_nbp,
                "tj_spitamen": self.parse_spitamen,
                "tj_ibt": self.parse_ibt,
                "tj_cbt": self.parse_cbt,
                "tj_alif": self.parse_alif,
                "tj_nbt": self.parse_nb,
                "tj_imonintl": self.parse_imonintl,
                "tj_humo": self.parse_humo,
                "tj_ardo": self.parse_ardo,
                "tj_finca": self.parse_finca,
            },
            self.parse_nb_all
        )
