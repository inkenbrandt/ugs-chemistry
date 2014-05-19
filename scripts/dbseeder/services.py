"""the http query wrapper over requests for unit testing"""

import requests


class WebQuery(object):

    def chemistry(self, url):
        r = requests.get(url)

        return r.text.splitlines()
