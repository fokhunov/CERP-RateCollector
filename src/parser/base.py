from time import time

from internal import rate_helper as rate
from internal import time_helper as custom_time


class Parser:
    def __init__(self, country, logger, fetcher):
        self.country = country
        self.log = logger
        self.fetcher = fetcher

    def handle_execute(self, b_rate_functions, nb_rate_function):
        self.debug("start parsing")

        start = time()
        result = {
            "country": self.country,
            "date_key": custom_time.now_date_key(self.country),
            "timestamp": custom_time.now_in_utc(),
            "bank_rates": {},
            "all_rates": {}
        }

        # collect bank rates (USD, EUR, RUB)
        for bank_id in b_rate_functions:
            result["bank_rates"][bank_id] = self.safe_parsing(b_rate_functions[bank_id], bank_id)

        # remove failed and empty rates
        self.remove_nones(result["bank_rates"])

        # collect national bank rates (all rates)
        result["all_rates"] = self.safe_parsing(nb_rate_function, "all_rates")

        # calculate execution time
        execution_time = time() - start
        if execution_time > 60:
            self.log.warn('execution took ' + str(execution_time) + ' sec')

        return result

    def safe_parsing(self, func, bank_id):
        try:
            result = func()
            if rate.is_empty(result):
                raise ParseError("rates are empty")

            return result

        except Exception as e:
            self.log.error({
                "msg": e.message,
                "country": self.country,
                "bank_id": bank_id,
            })
            return None

    def remove_nones(self, rates):
        ids = []

        for i in rates:
            if rates[i] is None:
                ids.append(i)
                continue

        for i in ids:
            del rates[i]

        return rates

    def __log_body__(self, msg):
        return {
            "msg": msg,
            "country": self.country
        }

    def debug(self, msg):
        self.log.debug(self.__log_body__(msg))

    def info(self, msg):
        self.log.info(self.__log_body__(msg))

    def warn(self, msg):
        self.log.warning(self.__log_body__(msg))

    def error(self, msg):
        self.log.error(self.__log_body__(msg))


class ParseError(Exception):
    """Exception raised when parsing process failed.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
