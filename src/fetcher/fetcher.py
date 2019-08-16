import requests

# disable https certificate warnings
requests.packages.urllib3.disable_warnings()


class Fetcher:
    def __init__(self):
        pass

    def fetch(self, link, method="GET", data=None, timeout=10):
        try:
            if method == "GET":
                return requests.get(link, params=data, timeout=timeout, verify=False).text
            elif method == "POST":
                return requests.post(link, data=data, timeout=timeout).content
            else:
                raise FetchError(link, "Unknown method '" + str(method) + "'")
        except requests.RequestException as e:
            raise FetchError(link, e.message)


class FetchError(Exception):
    """Exception raised when fetch attempt failed.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, url, message):
        self.url = url
        self.message = message
