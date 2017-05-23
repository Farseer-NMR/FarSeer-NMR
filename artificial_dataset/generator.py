import numpy as np
import pandas as pd
import random

def init_data_frame(protein_len=140):
    """
    Generates a data frame with the characteristics of a CCPNMRv2
    peaklist.
    """
    pklcolumns = ['Merit',
                'Position F1',
                'Position F2',
                'Height',
                'Volume',
                'Line Width F1 (Hz)',
                'Line Width F2 (Hz)',
                'Fit Method',
                'Vol. Method',
                'Assign F1',
                'Assign F2',
                'Details',
                '#',
                'index']
    resindex = range(protein_len)

    df = pd.DataFrame(columns=pklcolumns, index=resindex)
    df.loc[:,'Position F1'] = \
        np.random.random_integers(6000, high=10000, size=protein_len)/1000
    df.loc[:,'Position F2'] = \
        np.random.random_integers(100000, high=135000, size=protein_len)/1000

    df.loc[:,'Assign F1'] = \
        np.array(assign_nomenclature(protein_len, atom_type='H'))
    df.loc[:,'Assign F2'] = \
        np.array(assign_nomenclature(protein_len, atom_type='N'))

    df.loc[:,'Merit'] = '1.0'
    df.loc[:,'Details'] = 'None'
    df.loc[:,'#'] = np.arange(protein_len)
    df.loc[:,'index'] = np.arange(protein_len)
    df.loc[:,'Fit Method'] = 'parabolic'
    df.loc[:,'Vol. Method'] = 'box sum'

    df.loc[:,'Line Width F1 (Hz)'] = \
        np.random.random_integers(10000, high=50000, size=protein_len)/1000
    df.loc[:,'Line Width F2 (Hz)'] = \
        np.random.random_integers(10000, high=50000, size=protein_len)/1000

    df.loc[:,'Height'] = \
        np.random.random_integers(9000, high=10000, size=protein_len)
    df.loc[:,'Volume'] = \
        np.random.random_integers(9000, high=10000, size=protein_len)
    return df

def assign_nomenclature(protein, atom_type='H'):
    """
    Generates a list of artifical assignments.
    """
    aal3tol1 = {"Ala": "A",
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

    list_of_residues = \
        ["{}{}{}".format(i,
                         aal1tol3[random.choice(list(aal1tol3.keys()))],
                         atom_type)
        for i in range(1, protein+1)]

    return list_of_residues

if __name__ == '__main__':

    dfa = init_data_frame()
    print(dfa)
