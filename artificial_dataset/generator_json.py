import json
import sys
import os
import pandas as pd
import numpy as np
import random
import scipy.signal as signal

def prints_log(string):
    print(\
"""****************
{}
****************

""".format(string))
    return

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
    numbers = np.random.random_integers(inf*decimal,
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
    
    # 'Res#' column identifies the residue number. So it repeats for
    # sidechains.
    pkl.loc[:,'Res#'] = \
        pkl.loc[:,'Assign F1'].str.extract('([ab])?(\d+)', expand=False)[1]
    
    # 'Res#' is int() to help in future functions.
    pkl.loc[:,'Res#'] = pkl.loc[:,'Res#'].astype(int)
    
    pkl.sort_values('Res#', inplace=True)
    pkl.reset_index(inplace=True)
    
    return pkl

def gen_refpkl_macro(protein):
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
    
    return refpkl

def gen_titration_panel(refpkl, data):
    """
    Generates a titration panel by copying the refpeaklist
    a <data> number of times.
    """
    d = {}
    counter = 0
    for dpoint in data:
        key = '{}_{:0>4}'.format(counter, dpoint)
        d.setdefault(key, refpkl)
    
    tp = pd.Panel(d)
    
    s2w = \
"""Generates Titration Panel
{}
{}""".format(sorted(d.keys()), tp)
    prints_log(s2w)
    
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

def add_noise(tp):
    """
    Macro that adds noise to a given set of columns,
    along a titration Panel.
    """
    
    col_noise_percent = {'Position F1':0.02,
                         'Position F2':0.02,
                         'Height':10,
                         'Volume':10,
                         'Line Width F1 (Hz)':1,
                         'Line Width F2 (Hz)':1}
    
    for k, v in col_noise_percent.items():
        tp.loc[:,:,k] = \
            tp.loc[:,:,k].apply(lambda x: noise(x, p=v), axis=0)
    
    return tp

def gen_signal_regs(tp, r):
    """
    Generates a bool array where True meets the user defined
    regions.
    
    :r: a dict with keys 'r1', 'r2', 'r3'.
    
    return a dictionary with bool arrays for each region.
    """
    
    bool_dict = {}
    
    for k,v  in r.items():
        bool_array = tp.ix[0,:,'Res#'].isin(list(range(v[0], v[1])))
        bool_dict.setdefault(k, bool_array)
    
    
        prints_log(\
"""range: {} :: {}
region: {}
region len: {}
bool mask:
{}""".format(v[0], v[1], list(tp.ix[0,bool_array,'Res#']),
                        len(tp.ix[0,bool_array,'Res#']),
                        bool_array.value_counts()))
    
    return bool_dict

def init_cs_signal_vectors(vlen, kd=4000, n=1):
    """
    A base signal of very few intensity. Simulates
    regions where no perturbation occurs.
    Considers Hill Equation for signal generation.
    """
    
    vmax_base = pd.Series(np.array([0.01]*vlen)\
                    *np.random.choice([-1, 1], size=(vlen,)))
    
    kd_base = pd.Series(np.array([kd]*vlen))
    
    n_base = pd.Series(np.array([n]*vlen))
    
    prints_log(\
"""Init CS Signal Vectors
len {}""".format(len(vmax_base)))
    
    return vmax_base, kd_base, n_base

def init_int_signal_vector(vlen):
    
    intensities = pd.Series(np.random.choice(\
                                np.linspace(3,5,num=12),
                                size=vlen)
                           )
    
    return intensities

def count_trues(reg_dict):
    # this step is performed to avoid BREAK when the region
    # selected by the user is outside the protein length
    # that is, when True is not index of v.value_counts()
    dcounts = {}
    for k, v in reg_dict.items():
        if len(list(v.value_counts().index)) == 1:
            dcounts.setdefault(k, 1)
            prints_log("Not a valid region {}".format(k))
        else:
            dcounts.setdefault(k, v.value_counts()[1])
    return dcounts

def gen_cs_experimental_values(reg_dict, txv):
    
    dcounts = count_trues(reg_dict)
    
    exp_values = \
        {'r1':(np.linspace(0.01, 0.2, num=dcounts['r1']) \
                * np.random.choice([-1, 1], size=(dcounts['r1'],)), 
               np.repeat(txv[3], dcounts['r1']),
               np.repeat(1, dcounts['r1'])
               ),
            
            
         'r2':(np.repeat(0.1, dcounts['r2']) \
                * np.random.choice([-1, 1], size=(dcounts['r2'],)),
               np.linspace(txv[1], txv[-1], num=dcounts['r2']),
               np.repeat(1, dcounts['r2'])
               ),
            
            
         'r3':(np.repeat(0.1, dcounts['r3']) \
                * np.random.choice([-1, 1], size=(dcounts['r3'],)),
               np.repeat(txv[3], dcounts['r3']),
               np.linspace(0.1, 3, num=dcounts['r3'])
               )
        }
    
    return exp_values

def gen_int_experimental_values(reg_dict):
    """
    Generates the shape of the signal of a region.
    A Gaussian function along the region
    """
    dcounts = count_trues(reg_dict)
    
    exp_values = \
        {'r1':1-signal.gaussian(dcounts['r1'], std=dcounts['r1']//3)+0.7,
         
         'r2':1-signal.gaussian(dcounts['r2'], std=dcounts['r2']//3)+0.3,
         
         'r3':1-signal.gaussian(dcounts['r3'], std=dcounts['r3']//3)
        }
    
    return exp_values

def hill_eq(xvalues, Vmax=1, Kd=1, n=1):
        y = (Vmax*xvalues**n)/(Kd**n+xvalues**n)
        return y

def exp_decay(xvalues, vlen, tau):
    
    expdecay = signal.exponential(vlen, center=0, tau=vlen*tau, sym=False)
    
    return xvalues * expdecay

def add_signal(series, signal):
    return series + signal

def apply_signal(tp, regs_param, txv):
    """
    Adds a signal to specfici regions along a titration panel.
    """
    
    # bool dict defines the regions where signal will be applied
    regs_bool = gen_signal_regs(tp, regs_param)
    
    # initiates signal vectors
    vmax, kd, n = init_cs_signal_vectors(tp.shape[1],
                                         kd=txv[-1])
    
    intensity = init_int_signal_vector(tp.shape[1])
    
    # generates values for the different regions
    cs_exp_values = gen_cs_experimental_values(regs_bool, txv)
    int_exp_values = gen_int_experimental_values(regs_bool)
    
    # merges signal vectors
    for k, v in cs_exp_values.items():
        # to the chemical shifts
        if not(np.any(regs_bool[k])):
            continue
        
        vmax.loc[regs_bool[k]] = v[0]
        kd.loc[regs_bool[k]] = v[1]
        n.loc[regs_bool[k]] = v[2]
    
    # to the intensity
    for k, v in int_exp_values.items():
        if not(np.any(regs_bool[k])):
            continue
        
        intensity[regs_bool[k]] = v
    
    
    # apply signal to chemical shifts
    tp.loc[:,:,'Position F1'] = \
        tp.loc[:,:,'Position F1'].\
            apply(lambda x: add_signal(x,
                                       hill_eq(txv,
                                               Vmax=vmax[x.name],
                                               Kd=kd[x.name],
                                               n=n[x.name])),
                    axis=1)
    
    vmaxn = vmax * 5
    tp.loc[:,:,'Position F2'] = \
        tp.loc[:,:,'Position F2'].\
            apply(lambda x: add_signal(x,
                                       hill_eq(txv,
                                               Vmax=vmaxn[x.name],
                                               Kd=kd[x.name],
                                               n=n[x.name])),
                    axis=1)
    
    # apply signal to the intensities
    
    tp.loc[:,:,'Height'] = \
        tp.loc[:,:,'Height'].\
            apply(lambda x: exp_decay(x, x.size, intensity[x.name]),
                  axis=1)
    
    tp.loc[:,:,'Volume'] = \
        tp.loc[:,:,'Volume'].\
            apply(lambda x: exp_decay(x, x.size, intensity[x.name]),
                  axis=1)
    
    return tp

def gen_exp_titration(refpkl, params, zz='dia', yy='L1'):
    """
    Generates an experimental titration simulating a given signal
    that occurs in particular regions previously defined in the json
    file.
    """
    
    tp = gen_titration_panel(refpkl, params['xdata'])
    
    tp = add_noise(tp)
    
    tp = apply_signal(tp, params['data'][zz][yy], params['xdata'])
    
    return tp

def write_titration(tp, zz, yy):
    """
    Saves a titration series to csv files.
    """
    
    col_list=['Merit', 'Position F1', 'Position F2', 'Height', 'Volume', 
              'Line Width F1 (Hz)', 'Line Width F2 (Hz)', 'Fit Method',
              'Vol. Method', 'Assign F1', 'Assign F2', 'Details', '#',
              'Number']
    
    for item in tp.items:
        folder = 'spectra/{}/{}'.format(zz, yy)
        if not(os.path.exists(folder)):
            os.makedirs(folder)
        
        path = '{}/{}.csv'.format(folder, item)
        
        tp.loc[item,:,:].to_csv(path, index=False,
                                      index_label=False,
                                      columns=col_list
                                )
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
    
    folder = 'spectra/{}/{}'.format(zz, yy)
    if not(os.path.exists(folder)):
        os.makedirs(folder)
        
    path = '{}/pseq.fasta'.format(folder)
    
    with open(path, 'w') as ff:
        ff.write(pseq_fasta)
    
    prints_log(pseq_fasta)
    
    return

def run_generator(jpath):
    p = read_params(jpath)  # p of params
    
    # generates protein
    protein = gen_random_protein(p["protein_length"])
    
    # generates reference peaklist based on a protein
    refpkl = gen_refpkl_macro(protein)
    
    for zz in sorted(p['data'].keys()):
        for yy in sorted(p['data'][zz].keys()):
            prints_log("{} ** {}".format(zz, yy))
            
            tp = gen_exp_titration(refpkl, p, zz=zz, yy=yy)
            
            write_protein_fasta(protein, zz, yy)
            write_titration(tp, zz, yy)
    
    return

if __name__ == "__main__":
    
    run_generator(sys.argv[1])
