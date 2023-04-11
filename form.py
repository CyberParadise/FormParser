import json
import random
import urllib.parse
from typing import Union
from bs4 import PageElement, BeautifulSoup


class Form(dict):
    def __init__(self, form: Union[str, PageElement]):
        super().__init__()
        if isinstance(form, str):
            form = BeautifulSoup(form, 'html.parser')

        self.action = form.get('action')
        self.method = form.get('method')
        for e in form.find_all('input'):
            if name := e.get('name'):
                if name is None:
                    continue

                if name.endswith('[]'):
                    self.setdefault(name[:-2], list()).append(e.get('value', ""))
                    continue

                if e.get('type') == 'radio':
                    self.setdefault(name, tuple())
                    if e.has_attr('checked'):
                        self[name] = (e.get('value', ""),) + self[name]
                    else:
                        self[name] += (e.get('value', ""),)

                    continue

            self[name] = e.get('value', "")

    def add(self, key, value):
        self.__setitem__(key, value)

    def get_inputs(self) -> list[tuple]:
        inputs = list()
        for key, value in self.items():
            if isinstance(value, list):
                for val in value:
                    inputs.append((key+'[]', val))
                continue

            if isinstance(value, tuple):
                inputs.append((key, random.choice(value)))
                continue

            inputs.append((key, value))

        return inputs

    def urlencode(self):
        return urllib.parse.urlencode(self.get_inputs())

    def json(self):
        inputs = dict()
        for key in self:
            if isinstance(self[key], tuple):
                inputs[key] = random.choice(self[key])
                continue

            inputs[key] = self[key]

        return json.dumps(inputs)

    def __setitem__(self, key, value):
        if isinstance(self.get(key), list):
            self[key].append(value)
            return

        super().__setitem__(key, value)

    def __str__(self):
        return f"Form(action='{self.action}', method='{self.method}', inputs='{self}')"
