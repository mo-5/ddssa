import requests as requests


def query():
    """ Toy example of a CPE database query
    """
    url = "https://services.nvd.nist.gov/rest/json/cpes/1.0/"
    default_params = {
        "addOns": "cves",
        "keyword": "log4j2 2.16",
        "resultsPerPage": 2000,
        "startIndex": 0,
        "includeDeprecated": True
    }
    r = requests.get(url, params=default_params)
    print(r.json())


if __name__ == '__main__':
    query()
