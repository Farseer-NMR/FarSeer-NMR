import numpy as np
import pandas as pd
import random
import sys
import os

def gen_random_protein(length=140, path='spectra/298/L1'):
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
    
    
    return protein

def write_protein_fasta(protein, path):
    """
    :protein: str with the protein sequence
    """
    ## ++++++++++++++
    chunks, chunk_size = len(protein), len(protein)//4
    # generating a string with the broke protein sequence
    protein_fasta = '\n'.join(\
        [protein[i:i+chunk_size] for i in range(0, chunks, chunk_size)])
    ## ++++++++++++++
    
    # the string of the fasta file with the most difficult case
    protein_fasta = \
""">some random protein
{}
""".format(protein_fasta)
    
    print(protein_fasta)
    
    with open(path, 'w') as ff:
        ff.write(protein_fasta)
    return

def gen_assign(pseq, atom_type='H'):
    """
    :pseq: string with protein sequence
    
    return
        :aseq: assignment sequence
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

    aseq = \
        ["{}{}{}".format(i+1,
                         aal1tol3[res],
                         atom_type)
        for i, res in enumerate(protein)]
    
    return aseq

def gen_numbers(inf, sup, size, decimal=1000):
    numbers = np.random.random_integers(inf*decimal,
                                        high=sup*decimal,
                                        size=size
                                        )/decimal
    return numbers

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
    maskAG = pkl.loc[:,'Assign F1'].str[-4:].isin(['AsnH','GlnH'])
    maskW = pkl.loc[:,'Assign F1'].str[-4:].isin(['TrpH'])
    
    # temporary dataframes
    sd_df_2a = pkl.loc[maskAG,:]
    sd_df_2b = pkl.loc[maskAG,:]
    sd_df_1a = pkl.loc[maskW,:]
    
    # add the additional strings that identify the sidechain
    sd_df_2a.loc[:,'Assign F1'] += '2a'
    sd_df_2a.loc[:,'Assign F2'] += '2a'
    sd_df_2b.loc[:,'Assign F1'] += '2b'
    sd_df_2b.loc[:,'Assign F2'] += '2b'
    sd_df_1a.loc[:,'Assign F1'] += '1a'
    sd_df_1a.loc[:,'Assign F2'] += '1a'
    
    # nitrogen chemical shift is the same of 'a' and 'b'
    nitrogen = gen_numbers(105, 115, sd_df_2a.shape[0])
    sd_df_2a.loc[:,'Position F1'] = gen_numbers(6, 8, sd_df_2a.shape[0])
    sd_df_2a.loc[:,'Position F2'] = nitrogen
    sd_df_2b.loc[:,'Position F1'] = gen_numbers(6, 8, sd_df_2b.shape[0])
    sd_df_2b.loc[:,'Position F2'] = nitrogen
    sd_df_1a.loc[:,'Position F1'] = gen_numbers(9, 10, sd_df_1a.shape[0])
    sd_df_1a.loc[:,'Position F2'] = gen_numbers(130, 135, sd_df_1a.shape[0])
    
    # concatenates the tmp dataframes
    sd_df = pd.concat([sd_df_2a, sd_df_2b, sd_df_1a], ignore_index=True)
    
    # adds new values for the other parameters
    sdlen = sd_df.shape[0]  # number of rows
    sd_df.loc[:,'Height'] = gen_numbers(1, 100, sdlen, decimal=100000)
    sd_df.loc[:,'Volume'] = gen_numbers(1, 100, sdlen, decimal=100000)
    sd_df.loc[:,'Line Width F1 (Hz)'] = gen_numbers(5, 50, sdlen, decimal=1000)
    sd_df.loc[:,'Line Width F2 (Hz)'] = gen_numbers(5, 50, sdlen, decimal=1000)
    
    pkl = pd.concat([pkl, sd_df], ignore_index=True)
    
    pkl.loc[:,'Res#'] = pkl.loc[:,'Assign F1'].str.extract('([ab])?(\d+)', expand=False)[1]
    pkl.loc[:,'Res#'] = pkl.loc[:,'Res#'].astype(int)
    
    pkl.sort_values('Assign F1', inplace=True)
    pkl.reset_index(inplace=True)
    
    
    
    return pkl

def gen_refpkl_macro(protein):
    """ Generates reference pkl"""
    refpkl = pd.DataFrame({**gen_data_values(protein),
                           **gen_str_values(len(protein))})
    
    # remove prolines
    mask_no_pro = refpkl.loc[:,'Assign F1'].str[-4:] != 'ProH'
    
    refpkl = refpkl.loc[mask_no_pro,:]
    refpkl = add_sidechains(refpkl)
    
    return refpkl

def gen_t_dict(refpkl, data_points):
    """
    Generates a titration series in a pd.Panel that is a copy of the 
    reference peaklist.
    """
    
    ddf = {'0_ref':refpkl}
    
    for k in data_points:
        ddf.setdefault(k, refpkl)
    
    tp = pd.Panel(ddf)
    return tp

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

def add_noise(tp, col, percent):
    """
    Add noise to a column.
    
    cs p = 0.02
    intensity = 10
    lw = 1
    """
    
    tp.loc[:,:,col] = \
        tp.loc[:,:,col].apply(lambda x: noise(x, p=percent), axis=0)
        
    return tp

def add_noise_macro(tp):
    """
    Macro that adds noise to a given set of columns,
    along a titration Panel.
    """
    
    col_noise_dict = {'Position F1':0.02,
                      'Position F2':0.02,
                      'Height':10,
                      'Volume':10,
                      'Line Width F1 (Hz)':1,
                      'Line Width F2 (Hz)':1}
    
    for k, v in col_noise_dict.items():
        tp = add_noise(tp, k, v)
    
    return tp

def add_signal(series, signal):
    
    return series + signal
    

def def_signal_region(refpkl, first=1, last=10):
    """
    Defines the regions of signal.
    returns:
        bool vectors (masks)
    """
    
    reg = range(first, last)
    regmask = refpkl.loc[:,'Res#'].isin(list(reg))
    
    print("""******
range: {} :: {}
region: {}
region len: {}
bool mask:
{}""".format(first, last, list(refpkl.loc[regmask,'Res#']),
                        len(refpkl.loc[regmask,'Res#']),
                        regmask.value_counts()))
    
    return regmask

def init_Hill_signal(aalen=100,
                     vlen=20,
                     vmaxrange=[0.3],
                     kdrange=[1],
                     nrange=[1]):
    """
    Creates an array of values for vmax, kd and n to be passed
    to the Hill Equation for signal generation.
    """
    # a vector with base values with the length of the full peaklist
    # including sidechains
    
    
    # values for R1, fixed Kd and n, range Vmax -0.3 and 0.3
    vmax = np.random.choice(np.array(vmaxrange), size=(vlen,))
    kd = np.random.choice(np.array(kdrange), size=(vlen,))
    n = np.random.choice(np.array(nrange), size=(vlen,))
    
    vmax = np.sort(vmax) * np.random.choice([-1, 1], size=(vlen,))
    kd = np.sort(kd)
    n = np.sort(n)
    
    return vmax, kd, n

def acquire_signal_Hill(tp, col, vmax, kd, n, txv):
    """Adds the different signals to the different columns"""
    
    def hill_eq(L0, Vmax=1, Kd=1, n=1):
        y = (Vmax*L0**n)/(Kd**n+L0**n)
        print(list(y)[-1])
        return y
    
    tp.loc[:,:,col] = \
        tp.loc[:,:,col].\
            apply(lambda x: add_signal(x,
                                       hill_eq(txv,
                                                   Vmax=vmax[x.name],
                                                   Kd=kd[x.name],
                                                   n=n[x.name])),
                    axis=1)
    print('#################')
    return tp

def add_signal_macro(tp, protein, txv):
    """
    Macro that adds signal to the titration panel.
    """
    
    collist = ['Position F1']
    
    aarange = len(protein)
    
    # a dictionary of tuples of int values
    rlist = {'r1':(aarange//10, aarange//5),
             'r2':(aarange//3, aarange//3*2),
             'r3':(aarange//5*4, aarange)
            }
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # a ditionary of bool arrays
    # sets a bool arrays that define the regions where the signal will be 
    # added. Sidechains are included.
    region_bool_masks = {}
    for k in sorted(rlist.keys()):
    # define the region
        region_bool_masks[k] = def_signal_region(tp.iloc[0,:,:],
                                                 first=rlist[k][0],
                                                 last=rlist[k][1])
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # a dictionary of tuples of list of floats
    # sets which signal will be added to which region
    exp_values = \
            {'r1':(np.linspace(0.01, 0.2,
                               num=region_bool_masks['r1'].value_counts()[1]), 
                   txv[3], [1]),
            
            
             'r2':(np.array([0.1]*region_bool_masks['r2'].value_counts()[1]),
                   np.linspace(txv[1], txv[-1],
                               num=region_bool_masks['r2'].value_counts()[1]),
                   [1]),
            
            
             'r3':(np.array([0.1]*region_bool_masks['r3'].value_counts()[1]),
                   txv[3],
                   np.linspace(0.1,3,
                               num=region_bool_masks['r3'].value_counts()[1]))
            }
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # defines the base arrays of signal. Noise signal
    aalen=tp.iloc[0,:,0].size
    vmax_base = pd.Series(np.array([0.01]*aalen)\
                          *np.random.choice([-1, 1], size=(aalen,)))
    kd_base = pd.Series(np.array([txv[-1]]*aalen))
    n_base = pd.Series(np.array([1]*aalen))
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # prepares the arrays with the singal
    for k in sorted(exp_values.keys()):
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        vmax, kd, n = \
            init_Hill_signal(vlen=region_bool_masks[k].value_counts()[1],
                             vmaxrange=exp_values[k][0],
                             kdrange=exp_values[k][1],
                             nrange=exp_values[k][2])
        
        vmax_base.loc[region_bool_masks[k]] = vmax
        kd_base.loc[region_bool_masks[k]] = kd
        n_base.loc[region_bool_masks[k]] = n
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # adds the signal
    tp = acquire_signal_Hill(tp, 'Position F1', vmax_base, kd_base, n_base, txv)
    vmax_baseN = vmax_base*5
    tp = acquire_signal_Hill(tp, 'Position F2', vmax_baseN, kd_base, n_base, txv)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    return tp

def creates_titration(protein, refpkl, data_points, txv):
    ### create titration sequence
    # generate peaklists from refpkl adding noise to the data.
    tp = gen_t_dict(refpkl, data_points)
    
    # add noise
    tp = add_noise_macro(tp)
    
    # add signal
    tp = add_signal_macro(tp, protein, txv)
    
    return tp

if __name__ == '__main__':
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # general set up
    col_list=['Merit',
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
                         'Number',
            ]
    
    spectra_folder = 'spectra'
    
    zfolders = ['298']
    yfolders = ['L1']
    
    ## writes folders +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    for zf in zfolders:
        for yf in yfolders:
            folder = '{}/{}/{}'.format(spectra_folder, zf, yf)
            if not(os.path.exists(folder)):
                os.makedirs(folder)
    
    data_points = ['1_0125', '2_0250', '3_0500', '4_1000', '5_2000', '6_4000']
    txv = np.array([0, 125, 250, 500, 1000, 2000, 4000])
    
    
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # generates random protein sequence
    protein = gen_random_protein(length=int(sys.argv[1]), path=spectra_folder)

    # generates the reference peaklist
    refpkl = gen_refpkl_macro(protein)
    
    for zf in zfolders:
        for yf in yfolders:
            tp = creates_titration(protein, refpkl, data_points, txv)
    
            for df in tp.items:
                path = '{}/{}/{}'.format(spectra_folder, zf, yf)
                print(path)
                write_protein_fasta(protein, '{}/protein.fasta'.format(path))
                tp.loc[df,:,:].to_csv('{}/{}.csv'.format(path, df),
                                    index=False,
                                    index_label=False,
                                    columns=col_list)
 
