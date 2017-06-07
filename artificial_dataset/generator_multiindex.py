import numpy as np
import pandas as pd
import itertools as it
import sys
import json
import random
import os

def read_params(pfile):
    """
    Reads parameters defined in a json file.
    """
    with open(pfile) as data_file:    
        params = json.load(data_file)
    
    return params

def gen_random_protein(length=140):
    """
    Generates a random protein FASTA file of length :length:
    
    returns
        :protein_fasta: a string with the protein sequence
    """
    # possible aminoacids
    aminoacids = 'ARNDCEQGHILKMFPSTWYV'
    # starting methionine
    protein =['M']
    # the protein sequence in a list
    protein += [random.choice(aminoacids) for i in range(1, length)]
    # the protein sequence in a string
    protein = "".join(protein)
    # breaking the protein sequence
    
    print(protein)
    
    return protein

def gen_assign(pseq, atom_type='H'):
    """
    :pseq: string with protein sequence
    
    return
        :aseq: assignment sequence
    """
    aal1tol3 = {"A": "Ala",
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

    aseq = \
        ["{}{}{}".format(i+1,
                         aal1tol3[res],
                         atom_type)
        for i, res in enumerate(pseq)]
    
    return aseq

def gen_numbers(inf, sup, size, decimal=1000):
    """
    Generates an array of random float numbers of size <size>
    between <inf> and <sup> with 1/<decimal> decimals.
    """
    numbers = np.random.randint(inf*decimal,
                                        high=sup*decimal,
                                        size=size
                                        )/decimal
    return numbers

def gen_data_values(protein):
    """
    Generates the initial values of a peaklist.
    
    :protein: str, protein sequence 'MGLW...'
    
    return
        :d: a dictionary
    """
    
    plen = len(protein)
    
    # generates initial values
    d = {
    'Res#':range(1, len(protein)+1),
    'Assign F1':gen_assign(protein, atom_type='H'),
    'Assign F2':gen_assign(protein, atom_type='N'),
    'Position F1':gen_numbers(6, 10, plen),
    'Position F2':gen_numbers(105, 135, plen),
    'Height':gen_numbers(1, 100, plen, decimal=100000),
    'Volume':gen_numbers(1, 100, plen, decimal=100000),
    'Line Width F1 (Hz)':gen_numbers(5, 50, plen, decimal=1000),
    'Line Width F2 (Hz)':gen_numbers(5, 50, plen, decimal=1000)
    }
    
    return d
    
def gen_str_values(plen,
                   merit='1.0',
                   details='None',
                   fit='parabolic',
                   vol='box sum'):
    """
    Generates string values for information columns in peaklist
    
    :plen: int, the length of the protein.
    
    returns
        :d: a dictionary
    """
    d = {
        '#':np.arange(plen),
        'Number':np.arange(plen),
        'Merit':merit,
        'Details':details,
        'Fit Method':fit,
        'Vol. Method':vol
        }
    
    return d

def add_sidechains(pkl):
    """
    Identifies all residues with NH sidechains and generates the
    sidechains entries in the dataframe
    
    according to nomenclature
    
    AsnH2a, AsnH2b, GlnH2a, GlnH2b, TrpH2a
    AsnN2a, AsnN2b, GlnN2a, GlnN2b, TrpN2a
    
    :pkl: pd.Dataframe, a peaklist without sidechains
    
    returns
        :pkl: pd.Dataframe, with added sidechains rows
    """
    # two types of side chains, Asn and Gln have two signals
    # Trp has only one
    maskA = pkl.loc[:,'Assign F1'].str[-4:].isin(['AsnH'])
    maskG = pkl.loc[:,'Assign F1'].str[-4:].isin(['GlnH'])
    maskW = pkl.loc[:,'Assign F1'].str[-4:].isin(['TrpH'])
    
    # temporary dataframes
    sd_df_d2a = pkl.loc[maskA,:]
    sd_df_d2b = pkl.loc[maskA,:]
    sd_df_e2a = pkl.loc[maskG,:]
    sd_df_e2b = pkl.loc[maskG,:]
    sd_df_e1a = pkl.loc[maskW,:]
    
    # add the additional strings that identify the sidechain
    sd_df_d2a.loc[:,['Assign F1', 'Assign F2']] += ['d2a']*2
    sd_df_d2b.loc[:,['Assign F1', 'Assign F2']] += ['d2b']*2
    sd_df_e2a.loc[:,['Assign F1', 'Assign F2']] += ['e2a']*2
    sd_df_e2b.loc[:,['Assign F1', 'Assign F2']] += ['e2b']*2
    sd_df_e1a.loc[:,['Assign F1', 'Assign F2']] += ['e1a']*2
    
    # nitrogen chemical shift is the same of 'a' and 'b'
    nitrogend = gen_numbers(105, 115, sd_df_d2a.shape[0])
    sd_df_d2a.loc[:,'Position F1'] = gen_numbers(6, 8, sd_df_d2a.shape[0])
    sd_df_d2a.loc[:,'Position F2'] = nitrogend
    
    sd_df_d2b.loc[:,'Position F1'] = gen_numbers(6, 8, sd_df_d2b.shape[0])
    sd_df_d2b.loc[:,'Position F2'] = nitrogend
    
    nitrogene = gen_numbers(105, 115, sd_df_e2a.shape[0])
    sd_df_e2a.loc[:,'Position F1'] = gen_numbers(6, 8, sd_df_e2a.shape[0])
    sd_df_e2a.loc[:,'Position F2'] = nitrogene
    
    sd_df_e2b.loc[:,'Position F1'] = gen_numbers(6, 8, sd_df_e2b.shape[0])
    sd_df_e2b.loc[:,'Position F2'] = nitrogene
    
    sd_df_e1a.loc[:,'Position F1'] = gen_numbers(9, 10, sd_df_e1a.shape[0])
    sd_df_e1a.loc[:,'Position F2'] = gen_numbers(130, 135, sd_df_e1a.shape[0])
    
    # concatenates the tmp dataframes
    sd_df = pd.concat([sd_df_d2a,
                       sd_df_d2b,
                       sd_df_e2a,
                       sd_df_e2b,
                       sd_df_e1a], ignore_index=True)
    
    # adds new values for the other parameters
    sdlen = sd_df.shape[0]  # number of rows
    sd_df.loc[:,'Height'] = gen_numbers(1, 100, sdlen, decimal=100000)
    sd_df.loc[:,'Volume'] = gen_numbers(1, 100, sdlen, decimal=100000)
    sd_df.loc[:,'Line Width F1 (Hz)'] = gen_numbers(5, 50, sdlen, decimal=1000)
    sd_df.loc[:,'Line Width F2 (Hz)'] = gen_numbers(5, 50, sdlen, decimal=1000)
    
    pkl = pd.concat([pkl, sd_df], ignore_index=True)
    
    # 'Res#' column identifies the residue number. So it repeats for
    # sidechains.
    pkl.loc[:,'Res#'] = \
        pkl.loc[:,'Assign F1'].str.extract('([ab])?(\d+)', expand=False)[1]
    
    # 'Res#' is int() to help in future functions.
    pkl.loc[:,'Res#'] = pkl.loc[:,'Res#'].astype(int)
    
    pkl.sort_values(['Res#','Assign F1'], inplace=True)
    pkl.reset_index(inplace=True, drop=True)
    
    return pkl

def gen_refpkl_macro(protein, col_list):
    """
    Generates reference pkl with random aminoacids and all the
    sidechains.
    """
    refpkl = pd.DataFrame({**gen_data_values(protein),
                           **gen_str_values(len(protein))})
    
    # remove prolines
    mask_no_pro = refpkl.loc[:,'Assign F1'].str[-4:] != 'ProH'
    
    refpkl = refpkl.loc[mask_no_pro,:]
    refpkl = add_sidechains(refpkl)
    
    refpkl = refpkl[col_list]
    
    return refpkl

def gen_multiindex_df(z, y, x, rnum, col_list):
    
    x = sorted(['{:0>4}'.format(i) for i in x])
    
    iterables = [z, y, x, list(range(rnum))]
    
    idn = ['mag', 'lig', 'conc', 'row']
    
    idxs = pd.MultiIndex.from_product(iterables, names=idn)
    
    midf = pd.DataFrame(np.zeros((len(idxs), len(col_list))),
                        index=idxs, columns=col_list).sort_index()
    
    return midf

def write_titration(midf):
    """
    Saves a titration series to csv files.
    """
    
    col_list=['Assign F1', 'Assign F2', 'Position F1', 'Position F2', 'Height', 'Volume', 
              'Line Width F1 (Hz)', 'Line Width F2 (Hz)', 'Fit Method',
              'Vol. Method', 'Merit', 'Details', '#',
              'Number']
    
    for (zz, yy, xx) in it.product(midf.index.levels[0],
                                   midf.index.levels[1],
                                   midf.index.levels[2]):
        
        folder = 'spectra/{}/{}'.format(zz, yy)
        if not(os.path.exists(folder)):
            os.makedirs(folder)
        
        path = '{}/{}.csv'.format(folder, xx)
        
        midf.loc[(zz, yy, xx)].to_csv(path, index=False,
                                      index_label=False,
                                      columns=col_list)
        
    return

def exp_populate(midf, refpkl):
    
    for (zz, yy, xx) in it.product(midf.index.levels[0],
                                   midf.index.levels[1],
                                   midf.index.levels[2]):
        
        
        midf.loc[(zz, yy, xx)] = refpkl.values
    
    return midf

def noise(series, p=0.1):
    """Generates noise vector"""
    
    # a given percent of the mean of the input data.    
    data_percent = series.mean() * p / 100
    
    # Three-by-two array of random numbers from [-5, 0):
    # >>> 5 * np.random.random_sample((3, 2)) - 5
    # noise [-data_percent/2, data_percent/2)
    noise = \
        data_percent \
        * np.random.random_sample(size=(series.size,))\
        - data_percent/2
    
    return series + noise

def add_noise(midf):
    
    col_noise_percent = {'Position F1':0.02,
                         'Position F2':0.02,
                         'Height':10,
                         'Volume':10,
                         'Line Width F1 (Hz)':1,
                         'Line Width F2 (Hz)':1}
    
    z0 = midf.index.levels[0][0]
    y0 = midf.index.levels[1][0]
    x0 = midf.index.levels[2][0]
    
    for (zz, yy, xx, col) in it.product(midf.index.levels[0],
                                        midf.index.levels[1],
                                        midf.index.levels[2],
                                        col_noise_percent.keys()):
    
        midf.loc[(zz, yy, xx), col ] = \
            midf.loc[(z0, y0, x0), col ].values \
            + (col_noise_percent[col] \
                * np.random.random_sample(size=(midf.loc[(zz, yy, xx), col ].size,))\
                - col_noise_percent[col]/2)
    
    return midf

def run_generator(jpath):
    
    col_list=['Res#', 'Merit', 'Position F1', 'Position F2', 'Height', 'Volume', 
              'Line Width F1 (Hz)', 'Line Width F2 (Hz)', 'Fit Method',
              'Vol. Method', 'Assign F1', 'Assign F2', 'Details', '#',
              'Number']
    
    p = read_params(jpath)  # p of params
    
    # generates protein
    protein = gen_random_protein(p["protein_length"])
    
    # generates reference peaklist based on a protein
    refpkl = gen_refpkl_macro(protein, col_list)
    
    exp = gen_multiindex_df(p['zdata'], 
                            p['ydata'],
                            p['xdata'],
                            refpkl.shape[0],
                            col_list)
    
    
    exp = exp_populate(exp, refpkl)
    
    exp = add_noise(exp)
    
    write_titration(exp)



if __name__ == "__main__":
    run_generator(sys.argv[1])
