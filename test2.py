# -*- coding= utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from urllib.parse import urlparse
import cfscrape


def get_html(url, post=False):
    scraper = cfscrape.create_scraper()
    parsed = urlparse(url)
    if parsed.scheme == 'http':
        if post:
            res = scraper.post(url)
        else:
            res = scraper.get(url)
    else:
        if post:
            res = scraper.post(url, verify=False)
        else:
            res = scraper.get(url, verify=False)
    return res.text

if __name__ == "__main__":
    url = "http://www.mbn.co.kr/news/economy/"
    post = False

    html = get_html(url, post)
    print(html)