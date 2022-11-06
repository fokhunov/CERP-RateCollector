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

    # Parse Amonatbank (web page)
    def parse_amonat(self):
        result = self.fetcher.fetch("https://www.amonatbonk.tj/bitrix/templates/amonatbonk/ajax/ambApi.php")
        try:
            result = json.loads(result)
            result = result["individuals"]
            return {
                "usd_buy": rate.from_string(result["USD"]["buy"]),
                "usd_sale": rate.from_string(result["USD"]["sell"]),
                "eur_buy": rate.from_string(result["EUR"]["buy"]),
                "eur_sale": rate.from_string(result["EUR"]["sell"]),
                "rub_buy": rate.from_string(result["RUB"]["buy"]),
                "rub_sale": rate.from_string(result["RUB"]["sell"]),
            }
        except Exception as e:
            raise base.ParseError(e.message)

    # Parse Eskhata (web page)
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

    # Parse First Microfinance (web page)
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

    # Parse Tejaratbank (web page)
    def parse_tejaratbank(self):
        result = self.fetcher.fetch("http://tejaratbank.tj/en/#exchange")
        try:
            context = BeautifulSoup(result, "html.parser", parse_only=SoupStrainer(id='currency'))
            buys = context.find(id='text-3').get_text(separator='\n', strip=True).split()
            sales = context.find(id='text-4').get_text(separator='\n', strip=True).split()
            if buys and sales:
                return {
                    "usd_buy": rate.from_string(buys[0]),
                    "usd_sale": rate.from_string(sales[0]),
                    "eur_buy": rate.from_string(buys[1]),
                    "eur_sale": rate.from_string(sales[1]),
                    "rub_buy": rate.from_string(buys[2]),
                    "rub_sale": rate.from_string(sales[2]),
                }
            else:
                raise base.ParseError("rates not found")
        except Exception as e:
            raise base.ParseError(e.message)

    # Parse Halykbank (web page)
    def parse_halykbank(self):
        result = self.fetcher.fetch("https://halykbank.tj/en/exchange-rates")
        try:
            context = BeautifulSoup(result, "html.parser")
            context = context.findAll("div", {"class": "exchange_rates"})[0]
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

    # Parse Spitamen Bank (web page)
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

    # Parse International Bank of Tajikistan (web page)
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

    # Parse Alif Bank (api)
    def parse_alif(self):
        result = self.fetcher.fetch("https://alif.tj/api/currency/index.php")
        try:
            result = json.loads(result)
            return {
                "usd_buy": rate.from_string(result["USD"]["buy_value"]),
                "usd_sale": rate.from_string(result["USD"]["sell_value"]),
                "eur_buy": rate.from_string(result["EUR"]["buy_value"]),
                "eur_sale": rate.from_string(result["EUR"]["sell_value"]),
                "rub_buy": rate.from_string(result["RUB"]["buy_value"]),
                "rub_sale": rate.from_string(result["RUB"]["sell_value"]),
            }
        except Exception as e:
            raise base.ParseError(e.message)

    # Parse National Bank of Tajikistan (api)
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

    # Parse Humo (web page)
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

    # Parse Finca (web page)
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
                "tj_amonat": self.parse_amonat,
                "tj_eskhata": self.parse_eskhata,
                "tj_fmfb": self.parse_fmfb,
                "tj_tejaratbank": self.parse_tejaratbank,
                "tj_halykbank": self.parse_halykbank,
                "tj_spitamen": self.parse_spitamen,
                "tj_ibt": self.parse_ibt,
                "tj_alif": self.parse_alif,
                "tj_nbt": self.parse_nb,
                "tj_humo": self.parse_humo,
                "tj_finca": self.parse_finca,
            },
            self.parse_nb_all
        )
