import requests

# disable https certificate warnings
requests.packages.urllib3.disable_warnings()

headers_mobile = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}


class Fetcher:
    def __init__(self):
        pass

    def fetch(self, link, method="GET", data=None, timeout=10, mobile=False):
        try:
            if method == "GET":
                if mobile:
                    return requests.get(link, params=data, timeout=timeout, verify=False, headers=headers_mobile).text
                else:
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
