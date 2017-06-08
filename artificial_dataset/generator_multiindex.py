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

def write_protein_fasta(pseq, zz, yy):
    """
    :protein: str with the protein sequence
    """
    ## ++++++++++++++
    chunks, chunk_size = len(pseq), len(pseq)//4
    # generating a string with the broke pseq sequence
    pseq_fasta = '\n'.join(\
        [pseq[i:i+chunk_size] for i in range(0, chunks, chunk_size)])
    ## ++++++++++++++
    
    # the string of the fasta file with the most difficult case
    pseq_fasta = \
""">some random pseq
{}
""".format(pseq_fasta)
    
    for z, y in it.product(zz, yy):
    
        folder = 'spectra/{}/{}'.format(z, y)
        if not(os.path.exists(folder)):
            os.makedirs(folder)
        
        path = '{}/pseq.fasta'.format(folder)
    
        with open(path, 'w') as ff:
            ff.write(pseq_fasta)
    
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


def hill(vmax, kd, n, values):
    return (vmax*values**n)/(kd**n+values**n)

def add_signal_x(midf, p):
    
    for zz, yy, res in it.product(midf.index.levels[0],
                                  midf.index.levels[1],
                                  midf.index.levels[3]):
        
        # adds chemical shift signal
        ## adds to H1
        midf.loc[(zz, yy, slice(None), res), 'Position F1'] =\
            midf.loc[(zz, yy, slice(None), res), 'Position F1'].values\
            + hill(midf.loc[(zz, yy, '0000', res), 'VmaxH'],
                   midf.loc[(zz, yy, '0000', res), 'kd'],
                   midf.loc[(zz, yy, '0000', res), 'n'],
                   np.array(p['xdata']))
        
        ## adds to N
        
        
        # adds intensities
        
    
    
    
    return midf


def init_signal_regions(midf, p, kd=4000.0, n=1.0):
    
    
    
    for mag, lig, conc in it.product(midf.index.levels[0],
                                     midf.index.levels[1],
                                     midf.index.levels[2]):
        
        vlen = midf.loc[(mag, lig, conc)].shape[0]
        
        mvh = np.random.choice([-0.01, 0.01], size=(vlen,))
        mvn = np.random.choice([-0.05, 0.05], size=(vlen,))
        mkd = np.repeat(kd, vlen)
        mn = np.repeat(n, vlen)
        mres = midf.loc[(mag, lig, conc, slice(None)), 'Res#'].values
        
        
        # do this because pandas does not allow bool indexing more than
        # level 0
        r1 = p['regions'][mag][lig]['r1']
        r2 = p['regions'][mag][lig]['r2']
        r3 = p['regions'][mag][lig]['r3']
        
        maskr1 = np.in1d(mres, np.arange(r1[0], r1[1]+1))
        maskr2 = np.in1d(mres, np.arange(r2[0], r2[1]+1))
        maskr3 = np.in1d(mres, np.arange(r3[0], r3[1]+1))
        
        mvh[maskr1] = np.linspace(0.01,0.2, num=np.sum(maskr1))\
            * np.random.choice([-1, 1], size=np.sum(maskr1))
        mvn[maskr1] = np.linspace(0.01,1.0, num=np.sum(maskr1))\
            * np.random.choice([-1, 1], size=np.sum(maskr1))
        
        mvh[maskr2] = 0.2\
            * np.random.choice([-1, 1], size=np.sum(maskr2))
        mvn[maskr2] = 1.0\
            * np.random.choice([-1, 1], size=np.sum(maskr2))
        mkd[maskr2] = np.linspace(p['xdata'][1],
                                  p['xdata'][-1],
                                  num=np.sum(maskr2))
        
        
        
        mvh[maskr3] = 0.2 \
            * np.random.choice([-1, 1], size=np.sum(maskr3))
        mvn[maskr3] = 1.0 \
            * np.random.choice([-1, 1], size=np.sum(maskr3))
        mkd[maskr3] = p['xdata'][4]
        mn[maskr3] = np.linspace(0.1, 3.0, num=np.sum(maskr3))
        
        midf.loc[(mag, lig, conc), 'VmaxH'] = mvh
        midf.loc[(mag, lig, conc), 'VmaxN'] = mvn
        midf.loc[(mag, lig, conc), 'kd'] = mkd
        midf.loc[(mag, lig, conc), 'n'] = mn
        
            
    return midf

def add_signal_macro(midf, p):
    
    midf = init_signal_regions(midf, p)
    
    midf = add_signal_x(midf, p)
    
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
    
    exp = add_signal_macro(exp, p)
    
    write_titration(exp)
    
    write_protein_fasta(protein, p['zdata'], p['ydata'])
    



if __name__ == "__main__":
    run_generator(sys.argv[1])
