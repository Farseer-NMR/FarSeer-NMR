import numpy as np
import pandas as pd
import random
import sys
def init_data_frame(protein_len=140):
    """
    Generates a data frame with the characteristics of a CCPNMRv2
    peaklist.
    """
    pklcolumns = ['#',
                 'index',
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
                 'Merit',
                 'Details'
                  ]
    resindex = range(protein_len)
    
    # creates a random protein
    random_protein = gen_random_protein(protein_len)
    
    dfdict = {
        'Position F1': \
            np.random.random_integers(6000, high=10000, size=protein_len)/1000,
        'Position F2': \
            np.random.random_integers(100000, high=135000, size=protein_len)/1000,
        'Assign F1': \
            np.array(assign_nomenclature(random_protein,atom_type='H')),
        'Assign F2': \
            np.array(assign_nomenclature(random_protein,atom_type='N')),
        'Line Width F1 (Hz)': \
            np.random.random_integers(10000, high=50000, size=protein_len)/1000,
        'Line Width F2 (Hz)': \
            np.random.random_integers(10000, high=50000, size=protein_len)/1000,
        'Height': \
            np.random.random_integers(9000, high=10000, size=protein_len),
        'Volume': \
            np.random.random_integers(9000, high=10000, size=protein_len)
            }
    
    
    
    dfbb = pd.DataFrame(dfdict)
    
    # prepare sidechains
    
    sd_mask = dfbb.loc[:,'Assign F1'].str[-4:].isin(['AsnH','GlnH', 'TrpH'])
    sdbase = dfbb.loc[sd_mask,:]
    sdsize = sdbase.shape[0]
    print(sdbase)
    
    dfsddict = {
        'Position F1': \
            np.random.random_integers(6000, high=7500, size=sdsize)/1000,
        'Position F2': \
            np.random.random_integers(100000, high=115000, size=sdsize)/1000,
        'Assign F1': \
            np.array(assign_nomenclature_sd(sdbase.loc[:,'Assign F1'])),
        'Assign F2': \
            np.array(assign_nomenclature_sd(sdbase.loc[:,'Assign F1'])),
        'Line Width F1 (Hz)': \
            np.random.random_integers(10000, high=50000, size=sdsize)/1000,
        'Line Width F2 (Hz)': \
            np.random.random_integers(10000, high=50000, size=sdsize)/1000,
        'Height': \
            np.random.random_integers(9000, high=10000, size=sdsize),
        'Volume': \
            np.random.random_integers(9000, high=10000, size=sdsize)
            }
    
    sdbase = pd.DataFrame(dfsddict)
    
    
    sd_mask = dfbb.loc[:,'Assign F1'].str[-4:].isin(['AsnH','GlnH'])
    sdbase2 = dfbb.loc[sd_mask,:]
    sdsize2 = dfbb.loc[sd_mask,:].shape[0]
    
    dfsddict2 = {
        'Position F1': \
            np.random.random_integers(6000, high=7500, size=sdsize2)/1000,
        'Position F2': \
            np.random.random_integers(100000, high=115000, size=sdsize2)/1000,
        'Assign F1': \
            np.array(assign_nomenclature_sd(sdbase2.loc[:,'Assign F1'], atom='b')),
        'Assign F2': \
            np.array(assign_nomenclature_sd(sdbase2.loc[:,'Assign F1'], atom='b')),
        'Line Width F1 (Hz)': \
            np.random.random_integers(10000, high=50000, size=sdsize2)/1000,
        'Line Width F2 (Hz)': \
            np.random.random_integers(10000, high=50000, size=sdsize2)/1000,
        'Height': \
            np.random.random_integers(9000, high=10000, size=sdsize2),
        'Volume': \
            np.random.random_integers(9000, high=10000, size=sdsize2)
            }
    sdbase2 = pd.DataFrame(dfsddict2)
    
    pkl = pd.concat((dfbb, sdbase, sdbase2), axis=0, ignore_index=True, copy=True)
    #print(pkl)
    #
    pkl.sort_values('Assign F1', inplace=True)
    
    pkl.loc[:,'Merit'] = '1.0'
    pkl.loc[:,'Detail'] = 'None'
    pkl.loc[:,'Volume'] = 'box sum'
    pkl.loc[:,'Fit. Method'] = 'parabolic'
    pkl.loc[:,'#'] = np.arange(pkl.shape[0])
    pkl.loc[:,'Number'] = np.arange(pkl.shape[0])
    
    #print(dfsd)
    return pkl

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
        ["{}{}{}".format(i+1,
                         aal1tol3[res],
                         atom_type)
        for i, res in enumerate(protein)]
    
    print(list_of_residues)
    return list_of_residues

def assign_nomenclature_sd(listofres, atom='a'):
    
    sddict = {
        'Asn':'d',
        'Gln':'e',
        'Trp':'e'
             }
    def addsd(s):
        if s[:-1][-3:] in ['Asn', 'Gln']:
            return s + sddict[s[:-1][-3:]] + '2' + atom
        elif s[:-1][-3:] == 'Trp': 
            return s+sddict['Trp']+'1' + atom
    
    listofsd = [addsd(res) for res in listofres]
    
    return listofsd

def gen_random_protein(length=140):
    aminoacids = 'ARNDCEQGHILKMFPSTWYV'
    protein =['M']
    protein += [random.choice(aminoacids) for i in range(1, length)]
    print(protein)
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

    ref = init_data_frame(protein_len)
    ref.to_csv('reference.csv', index=False)


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



    # ligand1 = {'0_ref': init_data_frame(protein_len)}
    # ligand2 = {'0_ref': ligand1['0_ref'].copy()}
    # ligand3 = {'0_ref': ligand1['0_ref'].copy()}
    #
    # # generates titrations
    # ligand1 = gen_titration(ligand1, list_of_cond1_datapoints)
    # ligand2 = gen_titration(ligand2, list_of_cond1_datapoints)
    # ligand3 = gen_titration(ligand3, list_of_cond1_datapoints)



    #print(protein1['0_ref'].loc[:,'Position F1'].sub(protein1['0_01'].loc[:,'Position F1']))
