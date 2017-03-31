import collections
import os
import numpy as np
import pandas as pd
import farseer_user_variables as fsuv
import fslibs.Titration as fsT
import fslibs.utils as fsut

class FarseerSet:
    """
    FarseerSet contains all the information regarding all the titration
    experiments. The FarseerSet object contains several nested dictionaries
    that have the same hierarchy of the spectra/ folder and store the information
    on the .csv and .fasta files, which are loaded as pd.DataFrames.
    
    There are three nested dictionaries:
        -allpeaklists - stores .csv peaklists regarding backbone peaks
        -allsidechains - contains .csv peaklists data for sidechains that
                         was extrated from allpeaklists
        -allFASTA - stores information on the FASTA sequence referent
                    to that titration experiment
    """
    def __init__(self, spectra_path, has_sidechains=False,
                                     applyFASTA=False,
                                     FASTAstart=1):
        """
        Initiates the object,
        
        :spectra_path: the path where the spectra (.csv files) are located.
                       spectra/ folder has to have the titration logical hirarchy
        :has_sidechains: bool whether the .csv contain information on sidechains residues
        :applyFASTA: bool whether to complete the sequence according to a FASTA file
        :FASTAstart: the number of the first residue in the FASTA file
        """
        
        # Decomposed the spectra/ path
        # self.paths will be used in load_experiments()
        # http://stackoverflow.com/questions/14798220/how-can-i-search-sub-folders-using-glob-glob-module-in-python
        self.paths = sorted([os.path.join(dirpath, f) \
                            for dirpath, dirnames, files \
                            in os.walk(spectra_path) \
                            for f in files])
        
        # Initiates the different nested dictionaries
        self.allpeaklists = {}
        self.allsidechains = {}
        self.allFASTA = {}
        
        # Initiates helper variables
        self.trikeys = []
        self.tmp_vars = {}
        
        # loads information into the object
        self.has_sidechains = has_sidechains
        self.applyFASTA = applyFASTA
        self.FASTAstart = FASTAstart
        
        # lists the names of the different axes point names which are given by 
        # the spectra/ folder hierarchy
        self.zzcoords = None
        self.yycoords = None
        self.xxcoords = None
        
        # Flags if there are more than 1 data point in each axis (a.k.a. titration condition)
        # if no more than 1 data point is found, there is no activity on that dimension
        self.haszz = False
        self.hasyy = False
        self.hasxx = False
        
        # Runs __init__ functions
        self.load_experiments()
        self.coordinates_list()
    
    def load_experiments(self):
        """
        Loads the .csv and .fasta files in the spectra/ folder into nested
        dictionaries as pd.DataFrames.
        """
        
        # logs activity
        str2write = \
'''{}{}
{}
'''.format(fsut.write_title('READS INPUT DATA',onlytitle=True),
           '\n'.join(self.paths),
           fsut.titlesperator)
        fsut.write_log(str2write)
        #
        
        # loads files in nested dictionaries
        # piece of code found in stackoverflow
        for p in self.paths:
            parts = p.split('/')
            branch = self.allpeaklists
            brench = self.allsidechains
            brinch = self.allFASTA
            for part in parts[1:-1]:
                branch = branch.setdefault(part, {})
                brench = brench.setdefault(part, {})
                brinch = brinch.setdefault(part, {})
            # reads the .csv file to a pd.DataFrame removes
            # the '.csv' from the key name to increase asthetics in output
            if parts[-1].endswith('.csv'):
                lessparts = parts[-1][:-4]
                branch[lessparts] = branch.get(parts[-1], pd.read_csv(p))
                # sets sidechains to 0
                brench[lessparts] = brench.get(parts[-1], 0)
                
                fsut.write_log('===> file read :: {}\n'.format(p))
                
            elif parts[-1].endswith('.fasta'):
                lessparts = parts[-1][:-4]
                brinch[lessparts] = brinch.get(parts[-1], 
                                               self.read_FASTA(p,
                                                         start=self.FASTAstart))
                fsut.write_log('===> file read :: {}\n'.format(p))
        
        fsut.write_log(fsut.titlesperator)
    
    def read_FASTA(self, FASTApath, start=1):
        """
         str -> pd.DataFrame

        :param FASTApath: the FASTA file path
        :param start: the residue number of the first residue in the FASTA file
        :param logfilename: the log file name
        :return: pd.DataFrame containing the information in the FASTA file

        PROCEDURE:

        Reads the FASTA file and generates a 5 column DataFrame with the
        information on the FASTA file ready to be incorporated in the peaklists
        dataframes.

        """
        # Opens the FASTA file, which is a string of capital letters
        # 1-letter residue code that can be split in several lines.
        FASTAfile = open(FASTApath, 'r')
        FASTA = FASTAfile.readlines()
        
        # Generates a single string from the FASTA file
        FASTA = "".join(FASTA).replace(' ', '').replace('\n', '').upper()
        FASTAfile.close()

        # Res# is kept as str() to allow reindexing
        # later on the seq_expand function.
        #
        dd = {}
        dd["Res#"] = [str(i) for i in range(start, (start + len(FASTA)))]
        dd["1-letter"] = list(FASTA)
        # aal1tol3 dictionary is defined at the end of this module
        dd["3-letter"] = [fsut.aal1tol3[i] for i in FASTA]
        #
        # Assign F1 is generated here because it will serve in future
        # functions.
        dd["Assign F1"] = [str(i + j) for i, j in zip(dd["Res#"], 
                                                      dd["3-letter"])]
        # Details set to 'None' as it is by default in CCPNMRv2 peaklists
        dd['Details'] = ['None' for i in FASTA]

        df = pd.DataFrame(dd, 
                          columns=['Res#', 
                                   '3-letter', 
                                   '1-letter', 'Assign F1', 'Details'])

        logstring = "*** Input FASTA Sequence {}:\t{}-{}-{}\n"\
                    .format(FASTApath, 
                            dd['Res#'][0], FASTA, dd['Res#'][-1])
        
        fsut.write_log(logstring)
        
        return df
    
    def coordinates_list(self):
        """
        Identifies the points in each dimension of the titration. In othe words:
        How many conditions must be analysed.
        
        It is a necessary condition that the names of the data points for
        one dimension (condition) are the same in the other dimensions.
        
        Example of a seq file mandatory hierarchy:
        
        :3rd dimension: para/ and dia/ 
        :2nd dimension: 278/, 285/ and 298/
        :1st dimension: l1.csv, l2.csv, ..., seq.fasta
        
        para/
        -> 278/
        ---> l1.csv
        ---> l2.csv
        ---> l3.csv
        ---> l4.csv
        ---> seq.fasta
        -> 285/
        ---> l1.csv
        ---> l2.csv
        ---> l3.csv
        ---> l4.csv
        ---> seq.fasta
        -> 298/
        ---> l1.csv
        ---> l2.csv
        ---> l3.csv
        ---> l4.csv
        ---> seq.fasta
        
        dia/
        -> 278/
        ---> l1.csv
        ---> l2.csv
        ---> l3.csv
        ---> l4.csv
        ---> seq.fasta
        -> 285/
        ---> l1.csv
        ---> l2.csv
        ---> l3.csv
        ---> l4.csv
        ---> seq.fasta
        -> 298/
        ---> l1.csv
        ---> l2.csv
        ---> l3.csv
        ---> l4.csv
        ---> seq.fasta
        
        """
        
        # keys for all the conditions in the 3rd dimension - higher level
        self.zzcoords = sorted(self.allpeaklists)
        self.zzref = self.zzcoords[0]
        # identifies if there is information in this dimension
        if len(self.zzcoords) > 1:
            self.haszz = True
        
        # keys for all the conditions in the 2nd dimension - middle level
        self.yycoords = sorted(self.allpeaklists[self.zzcoords[0]])
        self.yyref = self.yycoords[0]
        if len(self.yycoords) > 1:
            self.hasyy = True
        
        # keys for all the conditions in the 1st dimension - lowest level
        self.xxcoords = sorted(self.allpeaklists[self.zzcoords[0]][self.yycoords[0]])
        self.xxref = self.xxcoords[0]
        if len(self.xxcoords) > 1:
            self.hasxx = True
        
        # logs activity, which keys where found in each dimension
        str2write = \
'''{}> zz keys: {}
> yy keys: {}
> xx keys: {}
{}
'''.format(fsut.write_title('AXES NAMES IDENTIFIED', onlytitle=True),
           self.zzcoords, self.yycoords, self.xxcoords, fsut.titlesperator)

        fsut.write_log(str2write)
    
    def tricicle(self, zz, yy, xx, exec_func, args=[], kwargs={}):
        """
        Executes a function over the nested dictionary. FarseerSet() functions
        operate on each pd.DataFrame (loaded .csv), therefore tricicle() is a
        way to perform an action over all the DataFrames (spectra).
        
        :zz, yy, xx: the lists of dimension points
        :exec_func: the name of the function to executed
        :args: a list to be passed as *args to the exec_func
        :kwargs: a dict to be passed as *kwargs to the exec_func
        
        All functions in FarseerSet() are writen such that tricicle() can
        operate them.
        """
        # helper variable. Some function return variables that are used in the
        # next cycle.
        tmp_vars = {}
        
        for z in zz:
            fsut.write_log(fsut.dim_sperator(z, 'top'))
            for y in yy:
                fsut.write_log(fsut.dim_sperator(y, 'midle'))
                for x in xx:
                    fsut.write_log(fsut.dim_sperator(x, 'own'))
                    # tmp_vars is a helper variable that is useful for
                    # some functions
                    #
                    #The exec_func operated on the pd.DataFrame, therefore, x, y and x are
                    #passed to the function so that the pd.DataFrame can be indexed in the
                    #dictionary.
                    tmp_vars = exec_func(z, y, x, tmp_vars, *args, **kwargs)


    def split_res_info(self, z, y ,x, tmp_vars):
        """
        This function receives a DataFrame with the original information
        of the peaklist and adds four columns to this DataFrame:

        ['Res#', '1-letter', '3-letter', 'Peak Status']

        where:
        - 'Res#' is the residue number
        - '1-letter', is the 1-letter code residue name
        - '3-letter', is the 3-letter code residue name
          if the assignment belongs to a side-chain resonance, a character
          'a' or 'b' is added to the '1-letter' and '3-letter' codes.
        - 'Peak Status', assigns string 'measured' to identify the
          peaks present in this peaklist as experimentally measured.

        PROCEDURE:

        1. Extracts residue information from 'Assigned F1' column,
        separating the residue name from the residue number. This creates
        a new pd.DataFrame with column names 'Res#' and '3-letter'.

            '1MetH' -> '1' and 'Met'

        2. Generates the 1-letter column code from the 3-letter code column.
        In the same pd.DataFrame. 
        
        3. Concatenates the new generated pd.DataFrame with the input
        peaklist pd.Dataframe. And adds columns 'Peak Status' with value
        'measured'.
        
        4. Sorts the peaklist according to 'Res#' just in case the original
        .CSV file was not sorted. For correct sorting 'Res#' as to be set astype
        int and returned back to str.

        (conditional). If sidechains are present in the peaklist:
        identifies the sidechains entries (rows) and counts the number of
        sidechain entries. Adds the letter 'a' or 'b' to the columns
        '1-letter' and '3-letter' to identify the two sidechains resonances.
        """
        
        # Step 1)
        # extracts residue information from "Assign F1" column.
        resInfo = self.allpeaklists[z][y][x].\
            loc[:,'Assign F1'].str.extract('(\d+)(.{3})', expand=True)
        
        resInfo.columns = ['Res#', '3-letter']

        # Step 2)
        # generates 1-letter code column
        resInfo.loc[:,'1-letter'] = resInfo.loc[:,"3-letter"].map(fsut.aal3tol1.get)
        
        # Step 3)
        # concatenates the original peaklist DataFrame and the new
        # generated dataframe contained the information
        # ['Res#', '1-letter', '3-letter']
        self.allpeaklists[z][y][x] = pd.concat([self.allpeaklists[z][y][x],\
                                                resInfo], axis=1)
        
        # Adds the 'Peak Status' Column. All the peaks in the peaklist
        # at this stage are peaks that have been measured and are
        # identified in the NMR spectrum. Therefore all the peaks here
        # are labeled as 'measured'. On later stages of the script
        # peaks not identified will be added to the peaklist, and those
        # peaks will be label as 'lost' or 'unassigned'.
        self.allpeaklists[z][y][x].loc[:,'Peak Status'] = 'measured'
        
        # Step 6)
        # sorts the peaklist.
        # just in case the original .csv file was created unsorted.
        self.allpeaklists[z][y][x].loc[:,'Res#'] = \
        self.allpeaklists[z][y][x]['Res#'].astype(int)
        
        self.allpeaklists[z][y][x].sort_values(by='Res#', inplace=True)
        
        self.allpeaklists[z][y][x].loc[:,'Res#'] = \
        self.allpeaklists[z][y][x].loc[:,'Res#'].astype(str)
        
        self.allpeaklists[z][y][x].reset_index(inplace=True)
        
        # sidechains entries always end with an 'a' or 'b' in the AssignF1
        # use of regex: http://www.regular-expressions.info/tutorial.html
        # identify the sidechain rows
        sidechains_bool = self.allpeaklists[z][y][x].loc[:,'Assign F1'].str.match('\w+[ab]$')
        
        # initiates SD counter
        sd_count = {True:0}
        
        if self.has_sidechains and (True in sidechains_bool.value_counts()):
            # two condition are evaluated in case the user has set sidechains
            # to True but there are actually no sidechains.
            
            sd_count = sidechains_bool.value_counts()
            
            # DataFrame with side chains
            self.allsidechains[z][y][x] = \
                self.allpeaklists[z][y][x].loc[sidechains_bool,:]
            
            # sorts
            #self.allsidechains[z][y][x].sort_values(by='Assign F1', inplace=True)
            
            # adds 'a' or 'b'
            self.allsidechains[z][y][x].loc[:,'Res#'] = \
                self.allsidechains[z][y][x].loc[:,'Res#'] + \
                self.allsidechains[z][y][x].loc[:,'Assign F1'].str[-1]
            
            # creates backbone peaklist without sidechains
            self.allpeaklists[z][y][x] = \
                self.allpeaklists[z][y][x].loc[-sidechains_bool,:]
        
        # Writes sanity check
        if {'1-letter', 'Res#', '3-letter', 'Peak Status'}.\
           issubset(self.allpeaklists[z][y][x].columns):
            columns_OK = 'OK'
        
        # the script does not correct for the fact that the user set no sidechains
        # but that actually are sidechains, though the log file register such occurrence.
        str2write = '*** new columns inserted:  {}  *** sidechains user setting: {} ** sidechains identified: {} ** SD count: {}.\n'.\
            format(columns_OK, self.has_sidechains, (True in sd_count), sd_count[True])
        fsut.write_log(str2write)
    
    def correct_shifts(self, z, y, x, ref_data, ref_res='1'):
        """
        Corrects Chemical Shifts in a peaklist DataFrame according
        to an internal reference peak which is chosen by user. This
        function operates only in the first dimension (xx).
        
        :ref_res: string with the number of the reference residue
        """
        
        pt_res_mask = self.allpeaklists[z][y][x].loc[:,'Res#'] == ref_res
        pt_F1_cs = self.allpeaklists[z][y][x].loc[pt_res_mask,'Position F1']
        pt_F2_cs = self.allpeaklists[z][y][x].loc[pt_res_mask,'Position F2']
        
        # Reads the information of the selected peak in the reference spectrum
        if x == self.xxref:
            
            # loads the chemical shift for F1 of the ref res
            ref_data['F1_cs'] = \
                self.allpeaklists[z][y][x].loc[pt_res_mask,'Position F1']
            
            # loads the chemical shift for the F2 of the ref res
            ref_data['F2_cs'] = \
                self.allpeaklists[z][y][x].loc[pt_res_mask,'Position F2']
            
            # copies the chemical shift values to a new column
            self.allpeaklists[z][y][x].loc[:,'Position F1 original'] =\
                self.allpeaklists[z][y][x].loc[:,'Position F1']
        
        # calculates the difference between the reference chemical shift and the
        # chemical shift of the reference residue in the present spectrum
        # in case we are analysing the refence spectrum this operation shoul
        # return 0.
        F1_cs_diff = float(pt_F1_cs) - float(ref_data['F1_cs'])
        F2_cs_diff = float(pt_F2_cs) - float(ref_data['F2_cs'])
        
        # copies the chemical shift data to a backup column
        self.allpeaklists[z][y][x].loc[:,'Position F1 original'] =\
            self.allpeaklists[z][y][x].loc[:,'Position F1']
        
        self.allpeaklists[z][y][x].loc[:,'Position F2 original'] =\
            self.allpeaklists[z][y][x].loc[:,'Position F2']
        
        # records the used correction factor
        self.allpeaklists[z][y][x].loc[:,'Pos F1 correction'] = F1_cs_diff
        self.allpeaklists[z][y][x].loc[:,'Pos F2 correction'] = F2_cs_diff
        
        # corrects the chemical shift by applying a subtration
        self.allpeaklists[z][y][x].loc[:,'Position F1'] = \
                self.allpeaklists[z][y][x].loc[:,'Position F1'].sub(F1_cs_diff)
        self.allpeaklists[z][y][x].loc[:,'Position F2'] = \
                self.allpeaklists[z][y][x].loc[:,'Position F2'].sub(F2_cs_diff)
        
        # logs the operation
        str2write = '''
> F1 ref data :: {:.4f} :: correction {:.4f}
> F2 ref data :: {:.4f} :: correction {:.4f}
'''.format(float(ref_data['F1_cs']), F1_cs_diff,
           float(ref_data['F2_cs']), F2_cs_diff)
        fsut.write_log(str2write)
        
        # returns a dictionary containing the infomation on the reference
        # chemical shift
        return ref_data
    
    def seq_expand(self, z, y, x, tmp_vars, ref_seq_dict, target_seq_dict,
                   fillna_dict, refscoords=None):
        """
        Expands the 'Res#' columns of a target peaklist (seq)
        according to a reference peaklist (seq). Usually, the reference peaklist
        is the reference experiment.
        
        This function is used to identify the lost residues. That is, residues
        that are in the reference peaklists but not in the target peaklist.
        
        It can also be used to expand the target peaklist to the complete
        FASTA sequence to identify the unassigned residues.
        """
        # expanding to other dimensions
        if tmp_vars == 'expanding':
            refcz = refscoords['z']
            refcy = refscoords['y']
            
        else:
            refcz = z
            refcy = y
            
        
        ref_key = sorted(ref_seq_dict[refcz][refcy].keys())[0]
        
        ind = ref_seq_dict[refcz][refcy][ref_key].loc[:,'Res#']
        length_ind = ind.size  # stores size of new index
        
        length_target_init = target_seq_dict[z][y][x].shape[0]
        
        target_seq_dict[z][y][x] = target_seq_dict[z][y][x].set_index('Res#').\
                            reindex(ind).reset_index().fillna(fillna_dict)
    
        length_target_final = target_seq_dict[z][y][x].shape[0]
    
        target_seq_dict[z][y][x].loc[:,'3-letter'] = \
            ref_seq_dict[refcz][refcy][ref_key].loc[:,'3-letter']
        
        target_seq_dict[z][y][x].loc[:,'1-letter'] = \
            ref_seq_dict[refcz][refcy][ref_key].loc[:,'1-letter']
        
        target_seq_dict[z][y][x].loc[:,'Assign F1'] = \
            ref_seq_dict[refcz][refcy][ref_key].loc[:,'Assign F1']
            
        str2write = \
""" > Template Length[{}|{}|{}] :: {} | Target Initial Length[{}|{}|{}] :: {} | Target final length :: {}
""".format(refcz, refcy, ref_key, length_ind, z, y, x, length_target_init, length_target_final)
    
        fsut.write_log(str2write)
    
    def column_organizor(self, z, y, x, tmp_vars, peaklist,
                         performed_cs_correction=False):
        """
        pd.DataFrame -> pd.DataFrame(ordered columns):

        Receives a pd.dataframe and organizes the columns for better visualization.

        Returns the organized dataframe.
        """
        if performed_cs_correction:
            col_order = ['Res#',
                         '1-letter',
                         '3-letter',
                         'Peak Status',
                         'Merit',
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
                         'Number',
                         '#',
                         'index',
                         'Position F1 original',
                         'Position F2 original',
                         'Pos F1 correction',
                         'Pos F2 correction']
                         #                         'index',
        else:
            col_order = ['Res#',
                 '1-letter',
                 '3-letter',
                 'Peak Status',
                 'Merit',
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
                 'Number',
                 '#',
                 'index']
        
        print(peaklist[z][y][x].columns)
        peaklist[z][y][x] = peaklist[z][y][x][col_order]
        str2write = '> Columns organized :: [{}|{}|{}]\n'.format(z, y, x)
        fsut.write_log(str2write)
    
    def gen_Farseer_cube(self, use_sidechains=False):
        Panel5D = pd.core.panelnd.create_nd_panel_factory(klass_name='Panel5D',
                                                  orders=['cool', 'labels', 'items', 'major_axis', 'minor_axis'],
                                                  slices={'labels': 'labels',
                                                          'items': 'items',
                                                          'major_axis': 'major_axis',
                                                          'minor_axis': 'minor_axis'},
                                                  slicer=pd.Panel4D,
                                                  aliases={'major': 'index', 'minor': 'minor_axis'},
                                                  stat_axis=2)

        # creates a Panel5D with the information of all the parsed peaklists
        # from this panel, the information will be accessed and used for the calculation
        # routines
        self.peaklists_p5d = Panel5D(self.allpeaklists)
        
        if use_sidechains:
            self.sidechains_p5d = Panel5D(self.allsidechains)
            
        fsut.write_log('OK!')
    
    def write_parsed_pkl(self, z, y, x, tmp_vars, peaklists, tsv_path='Backbone/parsed_peaklists'):
        """
        Writes the parsed peaklists to .tsv files.
        """
        tsv_path += '/{}/{}'.format(z, y)
        tsv_file = tsv_path + '/{}.tsv'.format(x)
        
        if not os.path.exists(tsv_path):
            os.makedirs(tsv_path)
        
        tsv_output = open(tsv_file, 'w')
        
        tsv_output.write(\
            peaklists[z][y][x].to_csv(sep="\t", na_rep='NaN', float_format='%.4f', index=False))
        
        fsut.write_log('> writen: {}\n'.format(tsv_file))
                
        tsv_output.close()
    
    def gen_titration(self, titpanel, D_attributes):
            tmp = fsT.Titration(np.array(titpanel),
                 items=titpanel.items,
                 minor_axis=titpanel.minor_axis,
                 major_axis=titpanel.major_axis)
            tmp.create_titration_attributes(**D_attributes)
            #tmp.resonance_type = res_type
            return tmp
    
    def gen_titration_dict(self, panelT, tittype, owndims, nextdims1, nextdims2, reso_type):
        '''
        Generates a dictionary that stores the titrations corresponding to the
        analysis of a given condition. The generated dictionary has main key
        equal to the 2nd next dimension, subkey equal to the next dimension
        and stores a Titration object (an inherited pd.Panel that stores the
        titration experiments peaklists as Items.
        '''
        
        D = {}
        D_attributes = {}
        D_attributes['resonance_type'] = reso_type
        D_attributes['tittype'] = tittype
        D_attributes['owndims'] = owndims
        for nextdim2 in nextdims2:
            fsut.write_log(fsut.dim_sperator(nextdim2, 'top'))
            D.setdefault(nextdim2, {})
            for nextdim1 in nextdims1:
                fsut.write_log(fsut.dim_sperator(nextdim1, 'midle'))
                D_attributes['nextdim2'] = nextdim2
                D_attributes['nextdim1'] = nextdim1
                D[nextdim2][nextdim1] = \
                    self.gen_titration(panelT.loc[nextdim2, nextdim1, :, :, :],
                                    D_attributes)
                fsut.write_log(str(D[nextdim2][nextdim1])+'\n')
        return D
    
    

if __name__ == '__main__':
    #x = ExperimentSet(ppp, **user_dict)
    #x.load_peaklists()
    #x.coordinates_list()
    #x.tricicle(x.zz, x.xx, x.yy, x.printt)
    #a = x.xx
    #print(x.paths)
    #print(x.zzref)
    #print(x.ww)
    print(a)
