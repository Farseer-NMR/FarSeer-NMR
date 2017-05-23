import numpy as np
import pandas as pd
import random
import sys
def init_data_frame(protein_len=140):
    """
    Generates a data frame with the characteristics of a CCPNMRv2
    peaklist.
    """
    pklcolumns = ['Position F1',
                'Position F2',
                'Height',
                'Volume',
                'Line Width F1 (Hz)',
                'Line Width F2 (Hz)',
                'Fit Method',
                'Vol. Method',
                'Assign F1',
                'Assign F2',
                'Merit',
                'Details',
                '#',
                'index']
    resindex = range(protein_len)

    df = pd.DataFrame(columns=pklcolumns, index=resindex)
    df.loc[:,'Position F1'] = \
        np.random.random_integers(6000, high=10000, size=protein_len)/1000
    df.loc[:,'Position F2'] = \
        np.random.random_integers(100000, high=135000, size=protein_len)/1000

    random_protein = gen_random_protein(protein_len)
    df.loc[:,'Assign F1'] = \
        np.array(\
            assign_nomenclature(\
                random_protein,
                atom_type='H')
                )

    df.loc[:,'Assign F2'] = \
        np.array(\
            assign_nomenclature(\
                random_protein,
                atom_type='N')
                )

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
                         aal1tol3[random.choice(protein)],
                         atom_type)
        for i in range(1, len(protein)+1)]

    return list_of_residues

def gen_random_protein(length=140):
    aminoacids = 'ARNDCEQGHILKMFPSTWYV'
    protein = [random.choice(aminoacids) for i in range(1, length+1)]
    return protein

def add_noise(pkl, range=0.1, where='Position F1'):
    """Adds noise to a column of the peaklists"""
    noise = \
        range * np.random.random_sample(size=(pkl.iloc[:,0].size,)) - range/2

    pkl.loc[:,where] = pkl.loc[:,where].add(noise)
    return pkl

def change_details(pkl, n=5):

    details = ['overlapped',
               'review assignment',
               'low intensity']


    for i in range(n):
        row = random.choice(list(pkl.index))
        pkl.loc[row,'Details'] = random.choice(details)

    return pkl

def gen_titration(pkldict, dplist):
    dpprev = list(pkldict.keys())[0]
    for dp in dplist:
        #do
        # copies the previous peaklist
        pkldict[dp] = pkldict[dpprev]
        # drops some residues (they were lost)
        pkldict[dp].drop(random.choice(list(pkldict[dp].index)),
                         axis=0,
                         inplace=True)
        # adds 5% of noise
        for col in pkldict[dpprev].columns[:6]:
            #do
            pkldict[dp] = add_noise(\
                            pkldict[dp],
                            range=pkldict[dp].loc[:,col].max()/20,
                            where=col)

            #done

        # affects details
        pkldict[dp] = change_details(pkldict[dp])
        dpprev = dp
        #done

    return pkldict


def nested_dict(d):
  for k, v in d.items():
    if isinstance(v, dict):
      nested_dict(v)
    else:
      d[k].setdefault(v, {})

if __name__ == '__main__':
    protein_len = int(sys.argv[1])

    # list of data points for condition 1
    # this is, ligand:protein ranges
    # number_ is to order alphabetically
    list_of_cond1_datapoints = ['1_0125',
                                '2_025',
                                '3_05',
                                '4_1',
                                '5_2',
                                '6_4']

    list_of_cond2_datapoints = ['ligand1', 'ligand2', 'ligand3']

    list_of_cond3_datapoints = ['dia', 'para']

    # # initiates absolute reference peaklists
    # absolute_reference = init_data_frame(protein_len)
    #
    # # dictionary of peaklists
    # d = {}
    # for one in list_of_cond1_datapoints:
    #     d.setdefault(one, {})
    #     for two in list_of_cond2_datapoints:
    #         d[one].setdefault(two, {})
    #         for three in list_of_cond3_datapoints:
    #             d[one][two].setdefault(three, absolute_reference)



    ligand1 = {'0_ref': init_data_frame(protein_len)}
    ligand2 = {'0_ref': ligand1['0_ref'].copy()}
    ligand3 = {'0_ref': ligand1['0_ref'].copy()}

    # generates titrations
    ligand1 = gen_titration(ligand1, list_of_cond1_datapoints)
    ligand2 = gen_titration(ligand2, list_of_cond1_datapoints)
    ligand3 = gen_titration(ligand3, list_of_cond1_datapoints)



    #print(protein1['0_ref'].loc[:,'Position F1'].sub(protein1['0_01'].loc[:,'Position F1']))
