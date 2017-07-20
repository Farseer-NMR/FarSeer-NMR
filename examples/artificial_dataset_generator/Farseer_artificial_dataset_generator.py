import numpy as np
import itertools as it
from scipy import signal
import sys
import json
import os
import re


class artifset():
    """
    Artificial set of data.
    
    Considers a set of experiments where a protein is titrated with different
    ligands (L1, L2, L3...). There is a MTSL tag at a given position and the
    experiments are repeated for the diamagnetic and the paramagnetic
    conditions.
    
    The artificial data show:
    
    0) A randomly generated protein of length 'plen' is generated,
    where position 1 is always a Met residue.
    
    1) The evolution of the NMR chemical shifts according to the Hill
    equation along the x dimension (cond1 or points in xdata),
    in three different regions (r1, r2 and r3).
    1.1) Regions are different for each element of 'ydata' and those are
    user defined. 
    1.2) Evolution of r1 represents changes in Vmax, r2 reprensets changes in
    Kd and r3 changes in n. Shapes of regions are defined by gaussian functions
    
    
    2) No specific signal is applied along the 'ydata'. Only differences
    resulting of 1) are observed.
    
    3) Applies a magnetic signal along 'zdata'.
    3.1) an inverted gaussian function is centered at the 'tag_position' where
    the intensity is reduced to zero. This effect is the same in every 'xdata'
    point for the paramagnetic data.
    3.2) an inverted exponential function is added at a specific region for
    each data point in the 'ydata'. Here, the intensity of the signal is
    progressively lost as the concentration of the ligand increases (cond1).
    
    4) Prolines are removed
    
    5) 2 residues are comulatively randomly lost at each 'xdata' point.
    
    6) Sidechains are not considered.
    
    ***** Explanation of the .json input file:
    {
    "plen": 100, # length of the simulated protein
    "zdata": ["dia", "para"], # points in the z dimension (cond3)
    "ydata": ["L1", "L2", "L3"], # pont in the y dimension (cond2)
    "xdata": [0, 125, 250, 500, 1000, 2000, 4000], #xdimension as integers
    #
    # the regions where signal is applied. where r[0] is the central residue
    # of the region and r[1] is the range in residues where signal as effect.
    "regions" : {"L1":{"r1":[20,20],
                       "r2":[60,14],
                       "r3":[80,10]
                              },
                 "L2":{"r1":[5,10],
                       "r2":[30,14],
                       "r3":[75,10]
                       },
                 "L3":{"r1":[10,20],
                       "r2":[50,14],
                       "r3":[90,10]
                       }
                },
    "tag_position": 75,
    #
    # residues where the tag interaction is centered.
    "pre_interaction":{"L1":20,
                       "L2":30,
                       "L3":16},
    "tag_size": 40
    }
    
    
    João M.C. Teixeira
    20.06.2017
    """
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
        
        self.protein = self.gen_random_protein()
        
        self.resnum = np.arange(1, self.params['plen']+1, dtype=int)
        self.resnumsd = self.resnum  # help variable for sidechains
        
        self.res = np.array(list(self.protein))
        
        self.floatdata = self.gen_ref_data()
        
        self.strdata = self.gen_strdata()
        
        #self.add_sidechains()
        
        pass
    
    def read_params(self, pfile):
        """
        Reads parameters defined in a .json file.
        
        return: a dictionary
        """
        with open(pfile) as data_file:    
            params = json.load(data_file)
        return params
    
    def gen_random_protein(self):
        """
        Generates a random protein string.
        
        returns
            :protein: a string with the protein sequence
        """
        # possible aminoacids
        aminoacids = 'ARNDCEQGHILKMFPSTWYV'
        
        # starting methionine
        # the protein sequence in a list
        protein = 'M' + "".join(np.random.choice(list(aminoacids),
                                            self.params['plen']-1))
        # breaking the protein sequence
        
        print(protein)
        return protein
    
    def gen_strdata(self):
        """
        Generates a 5D np.array with the peaklist information corresponding
        to the dtype=str. Those are the columns:
        
        "Assign F1", "Assign F2", "Merit", "Details", "Fit Method",
        "Vol. Method", "Number", "#"
        
        Data is generated for the reference peaklist and is copied to
        all the other datapoints in the artificial experimental data set.
        
        returns
            np.array
        """
        
        a1 = ["{}{}H".format(i+1, self.aal1tol3[res]) \
               for i, res in enumerate(self.protein)]
        
        a2 = ["{}{}N".format(i+1, self.aal1tol3[res]) \
               for i, res in enumerate(self.protein)]
        
        merit = ['1.0']*len(self.protein)
        details = ['None']*len(self.protein)
        vol = ['box sum']*len(self.protein)
        fit = ['parabolic']*len(self.protein)
        number = list(range(1, len(self.protein)+1))
        
        sd = \
            np.array([a1, a2, merit, details, fit, vol, number, number]).T
        
        strmatrix = np.tile(sd, (len(self.params['zdata']),
                                 len(self.params['ydata']),
                                 len(self.params['xdata']),1,1))
        
        return strmatrix
    
    def gen_numbers(self, inf, sup, size, decimal=1000):
        """
        Generates a np.array of size <size> containing random float numbers 
        between <inf> and <sup> with 1/<decimal> decimals.
        
        returns
            np.array
        """
        numbers = np.random.randint(inf*decimal,
                                            high=sup*decimal,
                                            size=size
                                            )/decimal
        return numbers
    
    def gen_ref_data(self):
        """
        Generates a 5D np.array with the peaklist information corresponding
        to the dtype=float. Those are the columns:
        
        "Positifion F1", "Position F2", "Height", "Volume",
        "Line width F1", "Line width F2"
        
        Data is generated for the reference peaklist and is copied to
        all the other datapoints in the artificial experimental data set.
        
        returns
            np.array
        """
        
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
    
    def add_sidechains_res(self, restype, sdt):
        """
        Identifies residues of type <restype> present in the artificial
        dataset. Inserts the corresponding entries according to the
        nomenclature.
        
        AsnHd2a, AsnHd2b, GlnHe2a, GlnHe2b, TrpHe1a
        AsnNd2a, AsnNd2b, GlnNe2a, GlnNe2b, TrpNe1a
        """
        # Asn and Gln have 2 sidechains entries while Trp has only 1.
        resmult = len(sdt)
        
        #Where are the <restype> ?
        mask = np.core.defchararray.equal(self.res, restype)
        # how many there are?
        num_sd_entries = np.count_nonzero(mask)*resmult
        
        # concatenates the assignment column to the sidechains nomenclature
        # for example, 'd2a' and 'd2b' in the case of Asn.
        abcolh = \
            np.core.defchararray.add(\
                np.repeat(self.strdata[0,0,0,mask,0],resmult),
                np.tile(sdt, num_sd_entries//resmult))
        
        # same as above but for 'Position F2' col.
        abcoln = \
            np.core.defchararray.add(\
                np.repeat(self.strdata[0,0,0,mask,1],resmult),
                np.tile(sdt, num_sd_entries//resmult))
        
        
        ##str data to be inserted in sidechains
        merit = np.repeat('1.0', num_sd_entries)
        details = np.repeat('None', num_sd_entries)
        volm = np.repeat('box sum', num_sd_entries)
        fit = np.repeat('parabolic', num_sd_entries)
        number = np.arange(1, num_sd_entries+1)
        
        ##float data to be inserted in sidechains
        ## this example does not considered that W sidechains appear at
        ## about 10 and 130 ppm or that chemical shift is the same in the
        ## Position F2 dimension (Nitrogen)
        p1 = self.gen_numbers(6, 8, num_sd_entries)
        #nitro = self.gen_numbers(105, 115, num_sd_entries//2)
        p2 = self.gen_numbers(105, 115, num_sd_entries)
        hgt = self.gen_numbers(1, 100, num_sd_entries, decimal=100000)
        vol = self.gen_numbers(1, 100, num_sd_entries, decimal=100000)
        lw1 = self.gen_numbers(5, 50, num_sd_entries, decimal=1000)
        lw2 = self.gen_numbers(5, 50, num_sd_entries, decimal=1000)
        
        # generates a 2D array with the str related columns
        sdstr = np.array([abcolh, abcoln, merit, details,
                          fit, volm, number, number], dtype=str).T
        
        # generates a 2D array with the float related columns
        sdfloat = np.array([p1, p2, hgt, vol, lw1, lw2], dtype=float).T
        
        # sorts the arrays according to the numbers.
        # this is a "want to play safe" as these arrays shoulb be already
        # sorted by definition self.strdata and self.floatdata are sorted.
        # # generates the residue number of the sidechains
        rescol = np.repeat(self.resnumsd[mask], resmult)
        sort_mask = np.argsort(rescol)
        sdstr = sdstr[sort_mask]
        sdfloat = sdfloat[sort_mask]
        
        # expands the arrays to the dimensions of the artificial dataset
        sdstr = np.tile(sdstr, (len(self.params['zdata']),
                                len(self.params['ydata']),
                                len(self.params['xdata']),1,1))
        
        sdfloat = np.tile(sdfloat, (len(self.params['zdata']),
                                    len(self.params['ydata']),
                                    len(self.params['xdata']),1,1))
        
        # concatenates the sidechains residue numbers to the protein
        # residue numbers
        self.resnumsd = np.concatenate([self.resnumsd, rescol], axis=0)
        # generates a sort mask
        sort_mask = np.argsort(self.resnumsd)
        # sorts the residue numbers that also contains the sidechains numbers
        self.resnumsd = self.resnumsd[sort_mask]
        
        
        # concatenates residue types with sidechains res types array
        self.res = \
            np.concatenate([self.res,
                            np.repeat(restype, num_sd_entries*2)],
                            axis=0)
        
        # sortes it alike
        self.res = self.res[sort_mask]
        
        # concatenates str and float data, sidechains with backbone
        self.strdata = np.concatenate([self.strdata, sdstr], axis=3)
        self.floatdata = np.concatenate([self.floatdata, sdfloat], axis=3)
        
        # sortes alike
        self.strdata = self.strdata[:,:,:,sort_mask]
        self.floatdata = self.floatdata[:,:,:,sort_mask]
        
        return
    
    def add_sidechains(self):
        """
        General macro to add sidechains.
        """
        self.add_sidechains_res('N', ['d2a','d2b'])
        self.add_sidechains_res('Q', ['e2a','e2b'])
        self.add_sidechains_res('W', ['e1a'])
        self.strdata[:,:,:,:,6] = np.arange(1, self.resnumsd.size+1)
        self.strdata[:,:,:,:,7] = np.arange(1, self.resnumsd.size+1)
        
        return
    
    def add_noise(self):
        """
        Adds noise to every float value in the artificial data set.
        
        Percentage of noise depends on the nature of the NMR observable.
        """
        def noise(n, p=0.0001):
            """Generates noise vector"""
        
            return n + n * (np.random.normal(0, p, n.size))
        
        
        # adds noise to Chemical Shifts
        self.floatdata[:,:,:,:,0:2] = \
            np.apply_along_axis(noise, 3,
                                self.floatdata[:,:,:,:,0:2], p=0.0001)
        
        # adds noise to intensities
        self.floatdata[:,:,:,:,2:4] = \
            np.apply_along_axis(noise, 3,
                                self.floatdata[:,:,:,:,2:4], p=0.015)
        
        return
    
    def hill(self, data, vmax, kd, n, values):
        """
        Sums the changes generated by the Hill Equation to the experimental
        values
        """
        return data + (vmax*values**n)/(kd**n+values**n)
    
    def signal_cs(self, lig, idx, rcenter, rrange, vmax, kd, n, xvalues, vh):
        """
        Applies the chemical shift changes along the 'xdata' points for a
        <lig> 'ydata' point.
        
        The signal is centered in <rcenter> and as a range of <rrange>.
        """
        
        # defines the left boundary of the signal
        rl = rcenter-rrange//2
        
        # defines the right boundary of the signal
        rr = rcenter+rrange//2
        
        # applies the signal
        self.floatdata[:,lig,:,rl:rr,idx] = \
            vh(self.floatdata[:,lig,:,rl:rr,idx],
               vmax,
               kd,
               n,
               xvalues[:,rl:rr])
        
        return
    
    def add_signal_along_x(self):
        """
        Adds a Chemical Shift Perturbation signal along the 'xdata' points,
        according to the Hill Equation.
        """
        # vectorizes the hill equation funtion
        vh = np.vectorize(self.hill)
        
        sz = self.floatdata.shape[3]  #number of residues entries
        
        # ligand concentrations used experimentally
        # are necessary for the hill equation
        xvalues = np.tile(np.array(self.params['xdata']), (sz,1)).T
        
        # non-interaction vmax values
        vmaxh = 0.2
        vmaxn = 1
        
        minvmaxh = 0.01
        minvmaxn = 0.05
        
        # non-interaction kd values
        kdmin = self.params['xdata'][1]
        kdmax = self.params['xdata'][-1]
        
        # non-interaction n values
        nmax = 4
        nmin = 0.2
        ##
        
        # for each ligand probed ('ydata' point):
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
            
            if 'r2' in self.params['regions'][k].keys():
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
            
            if 'r3' in self.params['regions'][k].keys():
            
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
    
    def tag_PRE(self):
        """
        Defines the signal derived from the presence of the MTSL paramagnetic
        tag. PRE profiles normally obtained for an IDP
        using Flexible Meccano. 
        Is an inverted exponential centered at the 'tag_position'.
        
        return
            np.array
        """
        
        
        # signal that results from presence of tag
        sig = signal.exponential(self.floatdata.shape[3],
                                 center=self.params['tag_position']-1,
                                 tau=5, sym=False)*-1+1
        
        sig[self.params['tag_position']-3:\
            self.params['tag_position']+2] = 0.00001
        
        sig = np.tile(sig, (self.floatdata.shape[2], 1))
        
        self.write_theoretical_PRE(sig[0])
        
        return sig
    
    def pre_interaction(self, pre_interaction_site):
        """
        Defines the paramagnetic signal derived from a presence of a ligand
        when a paramagnetic tag is present.
        
        Applies an inverted exponential function centered at a user defined
        region.
        
        return
            np.array
        """
        
        # signal that results from presence of tag
        sig = signal.exponential(self.floatdata.shape[3],
                                 pre_interaction_site,
                                 self.floatdata.shape[3]//7,
                                 False)
        
        # copies this signal to all the 'xdata' points
        pre_int = np.tile(sig, (self.floatdata.shape[2],1))
        
        # applies a atenuation factor on the signal, where the attenuation
        # is released as titration progresses.
        factor = np.tile(np.linspace(0,-1,self.floatdata.shape[2]),
                        (self.floatdata.shape[3],1)).T
        
        pre_int = pre_int * factor + 1
        
        mask = np.less_equal(pre_int, 0)
        pre_int[mask] = 0.0001 # to avoid ZeroDivision error.
        
        return pre_int
    
    def add_signal_along_z(self):
        """
        Algorythm that adds an intensity decrease signal along the 'zdata'
        dimension.
        """
        
        def pre(data, signal):
            return data * signal
        
        vpre = np.vectorize(pre)
        
        tag_pre = self.tag_PRE()
        
        for i, k in enumerate(sorted(self.params['pre_interaction'].keys())):
            
            pre_int = self.pre_interaction(self.params['pre_interaction'][k])
            
            int_region_mask = np.less(pre_int, tag_pre)
            
            tag_pre[int_region_mask] = pre_int[int_region_mask]
            
            self.floatdata[1,i,:,:,2] = \
                vpre(self.floatdata[1,i,:,:,2], tag_pre)
            
            pass
        
        return
    
    def add_signal(self):
        
        self.add_signal_along_x()
        
        #self.add_signal_along_z()
        
        return
    
    def remove_prolines(self):
        """
        Removes proline entries in the whole dataset.
        """
        proline_mask = \
            np.logical_not(np.chararray.endswith(self.strdata[0,0,0,:,0],
                                                 'ProH'))
        
        self.floatdata = self.floatdata[:,:,:,proline_mask,:]
        self.strdata = self.strdata[:,:,:,proline_mask,:]
        
        return
    
    def remove_lost(self, array_s, array_f, idx):
        """
        Removes a set of rows in 2D arrays.
        """
        
        array_s = np.delete(array_s, idx, axis=0)
        array_f = np.delete(array_f, idx, axis=0)
        
        return array_s, array_f
    
    def write_data(self):
        """
        Writes data into .csv files using the folder structure
        
        spectra/zz/yy/xx.csv
        """
        
        def lost_region(yy):
            
            lost_res = np.random.choice(\
                            np.arange(self.params['regions'][yy]['r1'][0]-self.params['regions'][yy]['r1'][1]/2,
                                      self.params['regions'][yy]['r1'][0]+self.params['regions'][yy]['r1'][1]/2+1))
            
            return lost_res
        
        #https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file
        
        header = 'Assign F1,Assign F2,Merit,Details,Fit Method,Vol. Method,Number,#,Position F1,Position F2,Height,Volume,Line Width F1 (Hz),Line Width F2 (Hz)'
        
        self.remove_prolines()
        
        
        #for i, zz in enumerate(self.floatdata):
        for iy, yy in enumerate(self.params['ydata']):
                
            lost = []
                
            for ix, xx  in enumerate(self.params['xdata']):
                    
                for iz, zz in enumerate(self.params['zdata']):
                    
                    
                    
                    lost.append(lost_region(yy))
                        
                    
                    lost.append(lost_region(yy))
                    
                    array_s, array_f = self.strdata[iz,iy,ix], \
                                       self.floatdata[iz,iy,ix]
                    
                    array_s, array_f = self.remove_lost(array_s, array_f, lost)
                    
                    tmp = np.concatenate([array_s, array_f], axis = 1)
                    
                    
                    folder = 'spectra/{}/{}'.format(zz, yy)
                    if not(os.path.exists(folder)):
                        os.makedirs(folder)
                    
                    path = \
                        '{}/{}.csv'.format(folder, '{:0>4}'.format(xx))
                    
                    np.savetxt(path,
                               tmp,
                               header=header,
                               comments='',
                               delimiter=',',
                               fmt='%s')
                    
        return
    
    def write_protein_fasta(self):
        """
        :protein: str with the protein sequence
        """
        ## ++++++++++++++
        chunks, chunk_size = self.params['plen'], self.params['plen']//4
        # generating a string with the broke pseq sequence
        pseq_fasta = '\n'.join(\
            [self.protein[i:i+chunk_size] 
             for i in range(0, chunks, chunk_size)])
        ## ++++++++++++++
        
        # the string of the fasta file with the most difficult case
        pseq_fasta = \
    """>some random pseq
{}
""".format(pseq_fasta)
        
        for z, y in it.product(self.params['zdata'], self.params['ydata']):
        
            folder = 'spectra/{}/{}'.format(z, y)
            if not(os.path.exists(folder)):
                os.makedirs(folder)
            
            path = '{}/pseq.fasta'.format(folder)
        
            with open(path, 'w') as ff:
                ff.write(pseq_fasta)
        
        return


    def write_theoretical_PRE(self, sig):
        """
        Writes the theoretical PRE profiles normally obtained for an IDP
        using Flexible Meccano.
        """
        
        table = np.column_stack((self.resnum, sig))
    
        for z, y in it.product(self.params['zdata'][1:], self.params['ydata']):
        
            folder = 'spectra/{}/{}'.format(z, y)
            if not(os.path.exists(folder)):
                os.makedirs(folder)
            
            path = '{}/tag.pre'.format(folder)
            
            np.savetxt(path, table, fmt=('%d', '%s'), delimiter='\t',
                       header='{}'.format(self.params['tag_position']),
                       comments='#')
            
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
    af.write_protein_fasta()
    #af.write_theoretical_PRE()
    
    
