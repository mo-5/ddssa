import certifi as certifi
import urllib3
import json

from furl import furl

http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())


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
    url = str(furl(url).add(default_params))
    print(url)
    r = http.request("GET", url)
    print(json.loads(r.data))


if __name__ == '__main__':
    query()
