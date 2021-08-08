#!/usr/bin/python3.7

import json
import os
import requests
import sys

from bs4 import BeautifulSoup
from icecream import ic
from jsonschema import validate, Draft4Validator
from src.logger import Logger
from src.models.program_list import ProgramListModel
from src.models.program import ProgramModel
from src.program import Program


class ProgramList:

    headers = {
        'user-agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/92.0.4515.131'
        ' Safari/537.36',
        'referer':
        'https://www.openbugbounty.org/bugbounty-list/',
        'accept':
        'application/json'
    }

    base_url = 'https://www.openbugbounty.org'

    url = 'https://www.openbugbounty.org/bugbounty-list/ajax.php'

    list_schema = 'data/list_schema.json'

    output_data = []
    output_file = 'data/openbugbounty-program-details.json'

    def __init__(self):
        self.logger = Logger()
        self.program_list = ProgramListModel()

    def get(self, offset=0, page_size=50):

        self.output_data = []

        data = {'start': offset, 'length': page_size}

        try:
            req = requests.post(self.url,
                                data=data,
                                headers=self.headers,
                                timeout=15)

            resp = json.loads(req.text)

            self.logger.debug(resp)
        except Exception as e:
            self.logger.error('get program list failed: {0}'.format(e))
            sys.exit(1)

        with open(self.list_schema) as schema:
            try:
                schema = json.load(schema)
                Draft4Validator.check_schema(schema)
                validate(instance=resp, schema=schema)
            except Exception as e:
                self.logger.error(
                    'get program list response is not valid: {0}'.format(e))
                sys.exit(1)

        self.program_list.recordsTotal = resp['recordsTotal']

        for item in resp['data']:

            if item[0]:
                soup = BeautifulSoup(item[0], 'lxml')

                model = ProgramModel()
                model.name = soup.a.get_text()
                model.url = self.base_url + soup.a['href']

                program = Program(model.name, model.url)
                details = program.get()

                model.checked_at = details[0]
                model.scope = details[1]

                self.program_list.programs.append(model)

                data = json.dumps(model.__dict__)
                self.output_data.append(data)

        self.logger.info('downloaded {0} programs with offset={1}'.format(
            page_size, offset))
        self.save()
        return self.program_list

    def save(self):
        if os.path.isfile(
                self.output_file) and os.stat(self.output_file).st_size > 0:
            self.output_data = [','] + self.output_data

        with open(self.output_file, 'a+') as file:
            file.write(','.join(self.output_data))
