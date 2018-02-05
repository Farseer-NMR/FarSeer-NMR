import json

class Variables(dict):
    _vars = {}

    def __new__(cls, *args, **kwargs):
        ob = super().__new__(cls, *args, **kwargs)
        ob.__dict__ = cls._vars
        return ob

    def read(self, fname):
        fin = open(fname, 'r')
        variables = json.load(fin)
        self._vars.update(variables)
        fin.close()

    def write(self, fout):
        json.dump(self._vars, fout, indent=4)
        fout.close()
