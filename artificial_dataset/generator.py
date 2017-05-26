import numpy as np
import pandas as pd
import random
import sys

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
    
    # writes the fasta
    with open('seq.fasta', 'w') as ff:
        ff.write(protein_fasta)
    
    return protein
    
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
    pkl.sort_values('Assign F1', inplace=True)
    pkl.reset_index(inplace=True)
    
    return pkl

def add_noise(series, p=0.1):
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

if __name__ == '__main__':
    
    
    col_list=['Number',
             '#',
             'Assign F1',
             'Assign F2',
             'Position F1',
             'Position F2',
             'Height',
             'Volume',
             'Line Width F1 (Hz)',
             'Line Width F2 (Hz)',
             'Merit',
             'Details',
             'Fit Method',
             'Vol. Method'
            ]
    
    
    spectra_folder = 'spectra/298/L1'
    
    data_points = ['1_0125', '2_0250', '3_0500', '4_1000', '5_2000', '6_4000']
    
    # generates random protein sequence
    if len(sys.argv) == 2:
        protein = gen_random_protein(length=int(sys.argv[1]))
    
        # generates the reference peaklist
        refpkl = pd.DataFrame({**gen_data_values(protein),
                               **gen_str_values(len(protein))})
        
        refpkl = add_sidechains(refpkl)
        
        
        
        #refpkl.to_csv('{}/0_ref.csv'.format(spectra_folder),
                      #index=False,
                      #index_label=False,
                      #columns=col_list)
    
    elif len(sys.argv) == 3:
        
        refpkl = pd.read_csv(sys.argv[2])
    
    ### create titration sequence
    # generate peaklists from refpkl adding noise to the data.
    
    ddf = {'0_ref':refpkl}
    for k in data_points:
        ddf.setdefault(k, refpkl)
    
    tp = pd.Panel(ddf)
    
    tp.loc[:,:,'Position F1'] = tp.loc[:,:,'Position F1'].apply(lambda x: add_noise(x, p=0.1), axis=0)
    tp.loc[:,:,'Position F2'] = tp.loc[:,:,'Position F2'].apply(lambda x: add_noise(x, p=0.02), axis=0)
    tp.loc[:,:,'Height'] = tp.loc[:,:,'Height'].apply(lambda x: add_noise(x, p=10), axis=0)
    tp.loc[:,:,'Volume'] = tp.loc[:,:,'Volume'].apply(lambda x: add_noise(x, p=10), axis=0)
    tp.loc[:,:,'Line Width F1 (Hz)'] = tp.loc[:,:,'Line Width F1 (Hz)'].apply(lambda x: add_noise(x, p=1), axis=0)
    tp.loc[:,:,'Line Width F2 (Hz)'] = tp.loc[:,:,'Line Width F2 (Hz)'].apply(lambda x: add_noise(x, p=1), axis=0)
    
    for df in tp.items:
        tp.loc[df,:,:].to_csv('{}/{}.csv'.format(spectra_folder, df),
                              index=False,
                              index_label=False,
                              columns=col_list)
    
    #apply(lambda x: self.csp_willi(x), axis=2)
    
    #pkl1 = add_noise_macro(refpkl)
    
    
    
    #pkl1.to_csv('{}/1_pkl.csv'.format(spectra_folder),
                      #index=False,
                      #index_label=False,
                      #columns=col_list)
















#def init_data_frame(protein_len=140):
    #"""
    #Generates a data frame with the characteristics of a CCPNMRv2
    #peaklist.
    #"""
    #resindex = range(protein_len)
    
    ## creates a random protein
    #random_protein = gen_random_protein(protein_len)
    
    #dfdict = {
        #'Position F1': \
            #np.random.random_integers(6000, high=10000, size=protein_len)/1000,
        #'Position F2': \
            #np.random.random_integers(100000, high=135000, size=protein_len)/1000,
        #'Assign F1': \
            #np.array(assign_nomenclature(random_protein,atom_type='H')),
        #'Assign F2': \
            #np.array(assign_nomenclature(random_protein,atom_type='N')),
        #'Line Width F1 (Hz)': \
            #np.random.random_integers(10000, high=50000, size=protein_len)/1000,
        #'Line Width F2 (Hz)': \
            #np.random.random_integers(10000, high=50000, size=protein_len)/1000,
        #'Height': \
            #np.random.random_integers(9000, high=10000, size=protein_len),
        #'Volume': \
            #np.random.random_integers(9000, high=10000, size=protein_len)
            #}
    
    
    
    #dfbb = pd.DataFrame(dfdict)
    
    ## prepare sidechains
    
    #sd_mask = dfbb.loc[:,'Assign F1'].str[-4:].isin(['AsnH','GlnH', 'TrpH'])
    #sdbase = dfbb.loc[sd_mask,:]
    #sdsize = sdbase.shape[0]
    #print(sdbase)
    
    #dfsddict = {
        #'Position F1': \
            #np.random.random_integers(6000, high=7500, size=sdsize)/1000,
        #'Position F2': \
            #np.random.random_integers(100000, high=115000, size=sdsize)/1000,
        #'Assign F1': \
            #np.array(assign_nomenclature_sd(sdbase.loc[:,'Assign F1'])),
        #'Assign F2': \
            #np.array(assign_nomenclature_sd(sdbase.loc[:,'Assign F1'])),
        #'Line Width F1 (Hz)': \
            #np.random.random_integers(10000, high=50000, size=sdsize)/1000,
        #'Line Width F2 (Hz)': \
            #np.random.random_integers(10000, high=50000, size=sdsize)/1000,
        #'Height': \
            #np.random.random_integers(9000, high=10000, size=sdsize),
        #'Volume': \
            #np.random.random_integers(9000, high=10000, size=sdsize)
            #}
    
    #sdbase = pd.DataFrame(dfsddict)
    
    
    #sd_mask = dfbb.loc[:,'Assign F1'].str[-4:].isin(['AsnH','GlnH'])
    #sdbase2 = dfbb.loc[sd_mask,:]
    #sdsize2 = dfbb.loc[sd_mask,:].shape[0]
    
    #dfsddict2 = {
        #'Position F1': \
            #np.random.random_integers(6000, high=7500, size=sdsize2)/1000,
        #'Position F2': \
            #np.random.random_integers(100000, high=115000, size=sdsize2)/1000,
        #'Assign F1': \
            #np.array(assign_nomenclature_sd(sdbase2.loc[:,'Assign F1'], atom='b')),
        #'Assign F2': \
            #np.array(assign_nomenclature_sd(sdbase2.loc[:,'Assign F1'], atom='b')),
        #'Line Width F1 (Hz)': \
            #np.random.random_integers(10000, high=50000, size=sdsize2)/1000,
        #'Line Width F2 (Hz)': \
            #np.random.random_integers(10000, high=50000, size=sdsize2)/1000,
        #'Height': \
            #np.random.random_integers(9000, high=10000, size=sdsize2),
        #'Volume': \
            #np.random.random_integers(9000, high=10000, size=sdsize2)
            #}
    #sdbase2 = pd.DataFrame(dfsddict2)
    
    #pkl = pd.concat((dfbb, sdbase, sdbase2), axis=0, ignore_index=True, copy=True)
    ##print(pkl)
    ##
    #pkl.sort_values('Assign F1', inplace=True)
    
    #pkl.loc[:,'Merit'] = '1.0'
    #pkl.loc[:,'Details'] = 'None'
    #pkl.loc[:,'Vol. Method'] = 'box sum'
    #pkl.loc[:,'Fit Method'] = 'parabolic'
    #pkl.loc[:,'#'] = np.arange(pkl.shape[0])
    #pkl.loc[:,'Number'] = np.arange(pkl.shape[0])
    
    #pkl.reset_index(inplace=True)
    #print(pkl)
    ##print(dfsd)
    #return pkl

#def assign_nomenclature(protein, atom_type='H'):
    #"""
    #Generates a list of artifical assignments.
    #"""

    #

#def assign_nomenclature_sd(listofres, atom='a'):
    
    #sddict = {
        #'Asn':'d',
        #'Gln':'e',
        #'Trp':'e'
             #}
    #def addsd(s):
        #if s[:-1][-3:] in ['Asn', 'Gln']:
            #return s + sddict[s[:-1][-3:]] + '2' + atom
        #elif s[:-1][-3:] == 'Trp': 
            #return s+sddict['Trp']+'1' + atom
    
    #listofsd = [addsd(res) for res in listofres]
    
    #return listofsd


#def add_noise(pkl, range=0.1, where='Position F1'):
    #"""Adds noise to a column of the peaklists"""
    #noise = \
        #range * np.random.random_sample(size=(pkl.iloc[:,0].size,)) - range/2

    #pkl.loc[:,where] = pkl.loc[:,where].add(noise)
    #return pkl

#def change_details(pkl, n=5):
    #"""
    #Simple function to change the Details columns based
    #on a list of options.
    #"""

    #details = ['overlapped',
               #'review assignment',
               #'low intensity']


    #for i in range(n):
        #row = random.choice(list(pkl.index))
        #pkl.loc[row,'Details'] = random.choice(details)

    #return pkl

#def gen_titration(pkls_dict, dplist):
    #"""
    #Generates a titration based on a list of points
    #by modifying the reference peaklists
    #according to a set of standard functions, which include:
    
    #* remove some residues randomly,
    #* add noise to the type float columns
    #* change details simmulating user notes
    #"""
    #dpprev = list(pkls_dict.keys())[0]
    #for dp in dplist:
        ##do
        ## copies the previous peaklist
        #pkls_dict[dp] = pkls_dict[dpprev].copy()
        
        ## drops some residues (they were lost)
        #for i in range(3):
            #pkls_dict[dp].drop(random.choice(list(pkls_dict[dp].index)),
                               #axis=0,
                               #inplace=True)
        
        ## adds 5% of noise
        #for col in ['Position F1',
                    #'Position F2']:
            ##do
            #pkls_dict[dp] = add_noise(\
                            #pkls_dict[dp],
                            #range=pkls_dict[dp].loc[:,col].astype(float).max()/2000,
                            #where=col)

            ##done

        ## affects details
        #pkls_dict[dp] = change_details(pkls_dict[dp])
        #dpprev = dp
        ##done

    #return pkls_dict


#def nested_dict(d):
  #for k, v in d.items():
    #if isinstance(v, dict):
      #nested_dict(v)
    #else:
      #d[k].setdefault(v, {})
















    ## list of data points for condition 1
    ## this is, ligand:protein ranges
    ## number_ is to order alphabetically
    #list_of_cond1_datapoints = ['1_0125',
                                #'2_025',
                                #'3_05',
                                #'4_1',
                                #'5_2',
                                #'6_4']

    #list_of_cond2_datapoints = ['ligand1', 'ligand2', 'ligand3']

    #list_of_cond3_datapoints = ['dia', 'para']

    #if len(sys.argv) == 2:
        #refpkl = init_data_frame(protein_len)
    #elif len(sys.argv) > 2:
        #refpkl = pd.read_csv(sys.argv[2])
    
    #pkls_dict = {'0_ref':refpkl}
    
    #pkls_dict = gen_titration(pkls_dict, list_of_cond1_datapoints)
    
    #columnslist=['Number',
             #'#',
             #'Position F1',
             #'Position F2',
             #'Assign F1',
             #'Assign F2',
             #'Height',
             #'Volume',
             #'Line Width F1 (Hz)',
             #'Line Width F2 (Hz)',
             #'Merit',
             #'Details',
             #'Fit Method',
             #'Vol. Method'
             #]
    #for k, v in pkls_dict.items():
        #v.to_csv('{}.csv'.format(k),
                 #columns=columnslist, index=False, index_label=False)
    
    
    
