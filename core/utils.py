# variables necessary for the functions

from functools import reduce
import os

aal3tol1 = {
"Ala": "A",
"Arg": "R",
"Asn": "N",
"Asp": "D",
"Cys": "C",
"Glu": "E",
"Gln": "Q",
"Gly": "G",
"His": "H",
"Ile": "I",
"Leu": "L",
"Lys": "K",
"Met": "M",
"Phe": "F",
"Pro": "P",
"Ser": "S",
"Thr": "T",
"Trp": "W",
"Tyr": "Y",
"Val": "V"}

aal1tol3 = {
"A": "Ala",
"R": "Arg",
"N": "Asn",
"D": "Asp",
"C": "Cys",
"E": "Glu",
"Q": "Gln",
"G": "Gly",
"H": "His",
"I": "Ile",
"L": "Leu",
"K": "Lys",
"M": "Met",
"F": "Phe",
"P": "Pro",
"S": "Ser",
"T": "Thr",
"W": "Trp",
"Y": "Tyr",
"V": "Val"}

def combine_dicts(dictionaries):
    tmp_dict = {}
    for dictionary in dictionaries:
        tmp_dict.update(dictionary)
    return tmp_dict

def exp_set_is_valid(variables):
    if not variables["experimental_dataset"]:
        return False
    else:
        if variables["conditions"]["z"] in list(variables["experimental_dataset"].keys()):
            if all(variables["conditions"]["y"] in list(variables["experimental_dataset"][z].keys()) for z in variables["conditions"]["z"]):
                if all(variables["conditions"]["x"] in list(variables["experimental_dataset"][z][y].keys()) for z in variables["conditions"]["y"]):
                    return True

def get_nested_value(dictionary, *keys):
    return reduce(lambda dct, key: dct.get(key, None) if isinstance(dct,
                                            dict) else None, *keys, dictionary)

def get_default_config_path():
    current_path = os.path.dirname(__file__)
    default_path = os.path.join(current_path, 'default_config.json')
    return default_path