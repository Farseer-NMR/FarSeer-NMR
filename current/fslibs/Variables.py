import json

class Variables(dict):
    _vars = {}

    def __new__(cls, *args, **kwargs):
        ob = super().__new__(cls, *args, **kwargs)
        ob.__dict__ = cls._vars
        return ob

    def read(self, fname):
        variables = json.load(open(fname, 'r'))
        self._vars.update(variables)

    def write(self, fout):
        json.dump(self._vars, fout, indent=4)

