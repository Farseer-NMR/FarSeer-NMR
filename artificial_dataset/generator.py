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
    protein_fasta = "".join(protein)
    # breaking the protein sequence
    ## ++++++++++++++
    chunks, chunk_size = len(protein_fasta), len(protein_fasta)//4
    # generating a string with the broke protein sequence
    protein_fasta = '\n'.join(\
        [protein_fasta[i:i+chunk_size] for i in range(0, chunks, chunk_size)])
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
    
    return protein_fasta
    
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

def gen_str_values(pkl,
                   merit='1.0',
                   details='None',
                   fit='parabolic',
                   vol='box sum'):
    """
    Generates string values for information columns in peaklist
    
    returns
        :d: a dictionary
    """
    d = {
        '#':np.arange(pkl.shape[0]),
        'Number':np.arange(pkl.shape[0]),
        'Merit':merit,
        'Details':details,
        'Fit Method':parabolic,
        'Vol. Method':vbox
        }
    
    return d

def gen_init_values(plen):
    """
    Generates the initial values of a peaklist.
    
    return
        :d: a dictionary
    """
    
    # generates initial values
    d = {
    'Assign F1':gen_assign(protein, atom_type='H')
    'Assign F2':gen_assign(protein, atom_type='N')
    pos1 = gen_numbers(6, 10, plen)
    pos2 = gen_numbers(105, 135, plen)
    hig = gen_numbers(1, 100, plen, decimal=100000)
    vol = gen_numbers(1, 100, plen, decimal=100000)
    lw1 = gen_numbers(5, 50, plen, decimal=1000)
    lw2 = gen_numbers(5, 50, plen, decimal=1000)
    
    
    
    return pkl



if __name__ == '__main__':
    # generates protein sequence
    protein = gen_random_protein(length=int(sys.argv[1]))
    
    
















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
    
    
    
