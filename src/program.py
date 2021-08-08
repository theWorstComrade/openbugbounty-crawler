#!/usr/bin/python3.7

import requests

from bs4 import BeautifulSoup
from datetime import datetime
from icecream import ic
from src.logger import Logger


class Program:

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/92.0.4515.131'
                      ' Safari/537.36',
        'referer': 'https://www.openbugbounty.org/bugbounty-list/'
    }

    def __init__(self, name, url):
        self.logger = Logger()
        self.name = name
        self.url = url

    def get(self):

        try:
            req = requests.get(self.url,
                               headers=self.headers,
                               timeout=35)
        except Exception as e:
            self.logger.error(
                'get program {0} details failed: {0}'.format(self.name, e))

        soup = BeautifulSoup(req.text, 'lxml')

        today = datetime.today().strftime("%Y-%m-%d %H:%M")

        scope = list()
        scope_table = soup.select_one('.wishlist.open-bounty')

        for cell in scope_table.findAll('td'):
            scope.append(cell.text)

        return [today, scope]
