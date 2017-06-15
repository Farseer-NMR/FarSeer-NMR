import numpy as np
import itertools as it
from scipy import signal
import sys
import json
import random
import os
import re

"""
arrays legends

strdata
cols:
0 - Assign F1
1 - Assign F2
2 - Merit
3 - Details
4 - Fit Method
5 - Vol. Method
6 - Number
7 - #

floatdata
cols:
0 - Position F1
1 - Position F2
2 - Height
3 - Volume
4 - Line Width F1 (Hz)
5 - Line Width F1 (Hz)

"""

class artifset():
    def __init__(self, fjson):
        
        self.aal1tol3 = {
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
        
        self.params = self.read_params(fjson)
        
        self.protein = self.gen_random_protein(self.params['plen'])
        
        self.res = np.arange(1, self.params['plen']+1)
        
        self.floatdata = self.gen_ref_data()
        
        self.strdata = self.gen_strdata()
        
        pass

    def read_params(self, pfile):
        """
        Reads parameters defined in a .json file.
        
        return: a dictionary
        """
        with open(pfile) as data_file:    
            params = json.load(data_file)
        return params

    def gen_random_protein(self, plen):
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
        protein += [random.choice(aminoacids) for i in range(1, plen)]
        # the protein sequence in a string
        protein = "".join(protein)
        # breaking the protein sequence
        
        print(protein)
        return protein
    
    def gen_strdata(self):
        
        a1 = ["{}{}H".format(i+1, self.aal1tol3[res]) \
               for i, res in enumerate(self.protein)]
        
        a2 = ["{}{}N".format(i+1, self.aal1tol3[res]) \
               for i, res in enumerate(self.protein)]
        
        merit = ['1.0']*len(self.protein)
        details = ['None']*len(self.protein)
        vol = ['box sum']*len(self.protein)
        fit = ['parabolic']*len(self.protein)
        number = list(range(1, len(self.protein)+1))
        
        sd = np.array([a1, a2, merit, details, fit, vol, number, number]).T
        
        strmatrix = np.tile(sd, (len(self.params['zdata']),
                                 len(self.params['ydata']),
                                 len(self.params['xdata']),1,1))
        
        return strmatrix

    def gen_numbers(self, inf, sup, size, decimal=1000):
        """
        Generates an array of random float numbers of size <size>
        between <inf> and <sup> with 1/<decimal> decimals.
        """
        numbers = np.random.randint(inf*decimal,
                                            high=sup*decimal,
                                            size=size
                                            )/decimal
        return numbers

    def gen_ref_data(self):
        
        p1 = self.gen_numbers(6, 10, self.params['plen'])
        p2 = self.gen_numbers(105, 135, self.params['plen'])
        hgt = self.gen_numbers(1, 100, self.params['plen'], decimal=100000)
        vol = self.gen_numbers(1, 100, self.params['plen'], decimal=100000)
        lw1 = self.gen_numbers(5, 50, self.params['plen'], decimal=1000)
        lw2 = self.gen_numbers(5, 50, self.params['plen'], decimal=1000)
        
        fd = np.array([p1, p2, hgt, vol, lw1, lw2]).T
        
        fmatrix = np.tile(fd, (len(self.params['zdata']),
                               len(self.params['ydata']),
                               len(self.params['xdata']),1,1))
        
        return fmatrix

    def write_data(self):
        #https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
        
        header = 'Assign F1,Assign F2,Merit,Details,Fit Method,Vol. Method,Number,#,Position F1,Position F2,Height,Volume,Line Width F1 (Hz),Line Width F2 (Hz)'
        
        for i, zz in enumerate(self.floatdata):
            for k, yy in enumerate(self.floatdata[i]):
                for j, xx  in enumerate(self.floatdata[i,k]):
                    tmp = np.concatenate([self.strdata[i,k,j],
                                          self.floatdata[i,k,j]],
                                          axis = 1)
                    
                    
                    folder = 'spectra/{}/{}'.format(self.params["zdata"][i],
                                                    self.params["ydata"][k])
                    if not(os.path.exists(folder)):
                        os.makedirs(folder)
                    
                    path = \
                        '{}/{}.csv'.format(folder,
                                           '{:0>4}'.\
                                            format(self.params["xdata"][j]))
                    
                    np.savetxt(path,
                               tmp,
                               header=header,
                               comments='',
                               delimiter=',',
                               fmt='%s')
        return

    def add_noise(self):
        
        def noise(n, p=0.0001):
            """Generates noise vector"""
        
            return n + n * (np.random.normal(0, p, n.size))
        
        self.floatdata[:,:,:,:,0:2] = \
            np.apply_along_axis(noise, 3,
                                self.floatdata[:,:,:,:,0:2], p=0.0001)
        
        self.floatdata[:,:,:,:,2:4] = \
            np.apply_along_axis(noise, 3,
                                self.floatdata[:,:,:,:,2:4], p=0.015)
        
        return
    
    def hill(self, data, vmax, kd, n, values):
        return data + (vmax*values**n)/(kd**n+values**n)
    
    def signal_cs(self, lig, idx, rcenter, rrange, vmax, kd, n, xvalues, vh):
        
        rl = rcenter-rrange//2
        rr = rcenter+rrange//2
        
        
        self.floatdata[:,lig,:,rl:rr,idx] = \
            vh(self.floatdata[:,lig,:,rl:rr,idx],
               vmax,
               kd,
               n,
               xvalues[:,rl:rr])
        
        return
    
    def add_signal_along_x(self):
        # adds signal according to the hill equation.
        vh = np.vectorize(self.hill)
        
        sz = self.floatdata.shape[3]  #number of residues entries
        
        # xvalues are necessary for the hill equation
        xvalues = np.tile(np.array(self.params['xdata']), (sz,1)).T
        
        ###
        vmaxh = 0.2
        vmaxn = 1
        
        minvmaxh = 0.01
        minvmaxn = 0.05
        
        kdmin = self.params['xdata'][1]
        kdmax = self.params['xdata'][-1]
        
        nmax = 4
        nmin = 0.2
        ##
        
        
        for i, k in enumerate(sorted(self.params['regions'].keys())):
            
            v = self.params['regions'][k]
            
            # region 1, range of vmax
            
            vvmaxh = \
                np.tile(\
                    signal.gaussian(v['r1'][1] , v['r1'][1]//5, True)\
                    *vmaxh+minvmaxh,
                    (self.floatdata.shape[2], 1)) \
                    * np.random.choice([-1, 1], 
                                       size=(v['r1'][1]))
            
            vvmaxn = \
                np.tile(\
                    signal.gaussian(v['r1'][1] , v['r1'][1]//5, True)\
                    *vmaxn+minvmaxn,
                    (self.floatdata.shape[2], 1)) \
                    * np.random.choice([-1, 1], 
                                       size=(v['r1'][1]))
            
            self.signal_cs(i, 0, v['r1'][0], v['r1'][1],
                           vvmaxh, kdmax, 1,   xvalues, vh)
            self.signal_cs(i, 1, v['r1'][0], v['r1'][1],
                           vvmaxn, kdmax, 1,   xvalues, vh)
            
            # region 2 range of kd
            
            vmaxhh = np.random.choice([-vmaxh, vmaxh], size=v['r2'][1])
            vmaxnn = np.random.choice([-vmaxn, vmaxn], size=v['r2'][1])
            
            
            vvkd = np.tile(\
                    (signal.gaussian(v['r2'][1] , v['r2'][1]//2, True)**8)    
                      * kdmax + kdmin,
                    (self.floatdata.shape[2], 1))
            
            self.signal_cs(i, 0, v['r2'][0], v['r2'][1],
                           vmaxhh,  vvkd,  1,   xvalues, vh)
            self.signal_cs(i, 1, v['r2'][0], v['r2'][1],
                           vmaxnn,  vvkd,  1,   xvalues, vh)
            
            #ragion 3 range of n
            vvn = np.tile(\
                    (signal.gaussian(v['r3'][1] , v['r3'][1]//2, True)**8)\
                           * nmax + nmin,
                          (self.floatdata.shape[2], 1))
            
            vmaxhh = np.random.choice([-vmaxh, vmaxh], size=v['r3'][1])
            vmaxnn = np.random.choice([-vmaxn, vmaxn], size=v['r3'][1])
            
            
            
            self.signal_cs(i, 0, v['r3'][0], v['r3'][1],
                           vmaxhh,  kdmax, vvn, xvalues, vh)
            self.signal_cs(i, 1, v['r3'][0], v['r3'][1],
                           vmaxnn,  kdmax, vvn, xvalues, vh)
        
        
        return
    
    def add_signal(self):
        
        self.add_signal_along_x()
        
        
        return


if __name__ == '__main__':
    
    """
arrays legends

strdata
cols:
0 - Assign F1
1 - Assign F2
2 - Merit
3 - Details
4 - Fit Method
5 - Vol. Method
6 - Number
7 - #

floatdata
cols:
0 - Position F1
1 - Position F2
2 - Height
3 - Volume
4 - Line Width F1 (Hz)
5 - Line Width F1 (Hz)

"""
    af = artifset(sys.argv[1])
    af.add_noise()
    af.add_signal()
    af.write_data()
    
    
