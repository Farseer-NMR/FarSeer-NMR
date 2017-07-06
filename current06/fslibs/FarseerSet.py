import os
import numpy as np
import pandas as pd
from current06.fslibs import wet as fsw

class FarseerSet:
    """
    FarseerSet contains the information regarding all the titration
    experiments. The FarseerSet object contains several nested
    dictionaries that have the same hierarchy of the spectra/ folder
    and store the information on the .csv and .fasta files,
    which are loaded as pd.DataFrames.
    
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
                       spectra/ folder has to have the titration logical
                       hirarchy
        :has_sidechains: bool whether the .csv contain information on
                         sidechains residues
        :applyFASTA: bool whether to complete the sequence according to
                     a FASTA file
        :FASTAstart: the number of the first residue in the FASTA file
        """
        
        # Decomposing the spectra/ path
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
        self.FASTAstart = FASTAstart
        
        # lists the names of the different axes point names which are given by 
        # the spectra/ folder hierarchy
        self.zzcoords = None
        self.yycoords = None
        self.xxcoords = None
        
        # Flags if there are more than 1 data point in each axis
        # (a.k.a. titration condition)
        # if no more than 1 data point is found,
        # there is no activity on that dimension
        self.haszz = False
        self.hasyy = False
        self.hasxx = False
        
        self.log = ''  # all log goes here
        
        #self.log_t('Farseer Set initiated in {}'.format(spectra_path))
        self.log_t('Initiates Farseer Set')
        input_log = \
"""
path: {}
side chains: {}
FASTA starting residue: {}
""".format(spectra_path, self.has_sidechains, self.FASTAstart)
        
        self.log_r(input_log)
        
        # Runs __init__ functions
        #self.load_experiments()
        #self.coordinates_list()
        
        self.p5d = pd.core.panelnd.create_nd_panel_factory(\
            klass_name='Panel5D',
            orders=['cool', 'labels', 'items', 'major_axis', 'minor_axis'],
            slices={'labels': 'labels',
                    'items': 'items',
                    'major_axis': 'major_axis',
                    'minor_axis': 'minor_axis'},
            slicer=pd.Panel4D,
            aliases={'major': 'index', 'minor': 'minor_axis'},
            stat_axis=2)
        
        self.aal3tol1 = {"Ala": "A",
                        "Arg": "R",
                        "Asn": "N",
                        "Asp": "D",
                        "Cys": "C",
                        "Glu": "E",
                        "Gln": "Q",
                        "Gly": "G",
                        "His": "H",
                        "Ile": "I",
                        "Leu": "L",
                        "Lys": "K",
                        "Met": "M",
                        "Phe": "F",
                        "Pro": "P",
                        "Ser": "S",
                        "Thr": "T",
                        "Trp": "W",
                        "Tyr": "Y",
                        "Val": "V"}
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
    
    def log_t(self, titlestr):
        """Formats a title for log."""
        log_title = '\n\n{0}\n{1:^79}\n{0}\n'.format('*'*79, titlestr)
        self.log_r(log_title)
        return
    
    def log_r(self, logstr):
        """
        Registers the log and prints to the user.
        
        :logstring: the string to be registered in the log
        """
        print(logstr)
        self.log += logstr+'\n'
        return
    
    def write_log(self, mod='a', path='farseer.log'):
        with open(path, mod) as logfile:
            logfile.write(self.log)
        return
    
    def load_experiments(self,
                         target=None,
                         filetype='.csv',
                         f=pd.read_csv):
        """
        Loads the <filetype> files in self.paths folder into nested
        dictionaries as pd.DataFrames.
        
        It is necessary that the names of the data points for
        one dimension (condition) are the same in the other dimensions.
        
        Example of a mandatory file hierarchy:
        
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
        
        self.log_t('READING INPUT FILES *{}*'.format(filetype))
        
        if not(any([p.endswith(filetype) for p in self.paths])):
            self.log_r(fsw.wet9(filetype))
            self.log_r(fsw.end_bad())
        
        
        # loads files in nested dictionaries
        # piece of code found in stackoverflow
        for p in self.paths:
            parts = p.split('spectra')[-1].split('/')
            branch = target
            for part in parts[1:-1]:
                branch = branch.setdefault(part, {})
            # reads the .csv file to a pd.DataFrame removes
            # the '.csv' from the key name to increase asthetics in output
            if parts[-1].lower().endswith(filetype):
                self.log_r(p)
                lessparts = parts[-1].split('.')[0]
                branch[lessparts] = branch.get(parts[-1], f(p))
        
        ############ WET #8
        zkeys = list(target.keys())
        ykeys = list(target[zkeys[0]].keys())
        xkeys = list(target[zkeys[0]][ykeys[0]].keys())
        
        if not(len(zkeys) * len(ykeys) * len(xkeys) == \
            len([x for x in self.paths if x.endswith(filetype)])):
            #DO
            str1 = ''
            for z, vz in target.items():
                str1 += z+'/\n'
                for y, vy in target[z].items():
                    str1 += \
                        "\t{}/\t{}\n".format(y, "\t".join(sorted(vy.keys())))
            
            self.log_r(fsw.wet8(filetype, str1))
        else:
            self.log_r('> No file of type <{}> missing - OK'.format(filetype))
        ############
        
        return
    
    
    def read_FASTA(self, FASTApath):
        """
         str -> pd.DataFrame

        :param FASTApath: the FASTA file path
        :param start: the residue number of the first residue in the
                      FASTA file
        :return: pd.DataFrame containing the information in
                 the FASTA file

        PROCEDURE:

        Reads the FASTA file and generates a 5 column DataFrame
        with the information ready to be incorporated in the peaklists
        dataframes.

        """
        # Opens the FASTA file, which is a string of capital letters
        # 1-letter residue code that can be split in several lines.
        FASTAfile = open(FASTApath, 'r')
        fl = FASTAfile.readlines()
        
        # Generates a single string from the FASTA file
        FASTA = ''
        for i in fl:
            if i.startswith('>'):
                continue
            else:
                FASTA += i.replace(' ', '').replace('\n', '').upper()
        
        FASTAfile.close()

        # Res# is kept as str() to allow reindexing
        # later on the seq_expand function.
        #
        dd = {}
        dd["Res#"] = [str(i) for i in range(self.FASTAstart,
                                           (self.FASTAstart + len(FASTA)))]
        dd["1-letter"] = list(FASTA)
        # aal1tol3 dictionary is defined at the end of this module
        dd["3-letter"] = [self.aal1tol3[i] for i in FASTA]
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
        
        logs = '{}-{}-{}'.format(self.FASTAstart, FASTA, dd['Res#'][-1])
        
        self.log_r(logs)
        
        return df
    
    
    def init_conditions(self):
        """
        Identifies the data points for each titration condition.
        Configures the conditions to be analyzed.
        
        returns: output log string.
        """
        
        self.log_t('IDENTIFIED TITRATION VARIABLES')
        
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
        self.xxcoords = \
            sorted(self.allpeaklists[self.zzcoords[0]][self.yycoords[0]])
        self.xxref = self.xxcoords[0]
        if len(self.xxcoords) > 1:
            self.hasxx = True
        
        logs = '''\
> 1st titration variables (cond1): {}
> 2nd titration variables (cond2): {}
> 3rd titration variables (cond3): {}
'''.format(self.xxcoords, self.yycoords, self.zzcoords)
        
        self.log_r(logs)
        
        return
    
    def tricicle(self, zz, yy, xx, exec_func, args=[],
                 title='TRICILES', kwargs={}):
        """
        Executes a function over the nested dictionary.
        FarseerSet() functions operate on each pd.DataFrame,
        therefore tricicle() is a way to perform an action over
        all the DataFrames (spectra).
        
        :zz, yy, xx: the lists of condition data points
        :exec_func: the name of the function to executed
        :args: a list to be passed as *args to the exec_func
        :kwargs: a dict to be passed as *kwargs to the exec_func
        
        All functions in FarseerSet() are writen such that tricicle() can
        operate them.
        """
        # helper variable. Some function return variables that are used in the
        # next cycle.
        tmp_vars = {}
        self.log_t(title)
        
        for z in zz:
            for y in yy:
                for x in xx:
                    # tmp_vars is a helper variable that is useful for
                    # some functions
                    #
                    # The exec_func that operates on the pd.DataFrame,
                    # therefore, x, y and x are
                    # passed to the function so that the pd.DataFrame
                    # can be indexed in the dictionary.
                    tmp_vars = exec_func(z, y, x, tmp_vars, *args, **kwargs)
        
        return

    def split_res_info(self, z, y ,x, tmp_vars):
        """
        Receives a DataFrame with the original information
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
        .CSV file was not sorted. For correct sorting 'Res#' as to be set
        astype int and returned back to str.

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
        resInfo.loc[:,'1-letter'] = \
            resInfo.loc[:,"3-letter"].map(self.aal3tol1.get)
        
        # Step 3)
        # concatenates the original peaklist DataFrame and the new
        # generated dataframe contained the information
        # ['Res#', '1-letter', '3-letter']
        self.allpeaklists[z][y][x] = \
            pd.concat([self.allpeaklists[z][y][x], resInfo], axis=1)
        
        # Adds the 'Peak Status' Column. All the peaks in the peaklist
        # at this stage are peaks that have been measured and are
        # identified in the NMR spectrum. Therefore all the peaks here
        # are labeled as 'measured'. On later stages of the script
        # peaks not identified will be added to the peaklist, and those
        # peaks will be label as 'lost' or 'unassigned'.
        try:
            self.allpeaklists[z][y][x].loc[:,'Peak Status'] = 'measured'
        except ValueError:
            self.allpeaklists[z][y][x] = self.allpeaklists[z][y][self.xxref].copy()
            self.allpeaklists[z][y][x].loc[:,['Peak Status',
                                              'Merit',
                                              'Position F1',
                                              'Position F2',
                                              'Height',
                                              'Volume',
                                              'Line Width F1 (Hz)',
                                              'Line Width F2 (Hz)']] =\
                ['lost',np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
            #print(self.allpeaklists[z][y][x])
            #input('')
        
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
        sidechains_bool = \
            self.allpeaklists[z][y][x].loc[:,'Assign F1'].str.match('\w+[ab]$')
        
        # initiates SD counter
        sd_count = {True:0}
        
        # if the user says it has sidechains and there are actually sidechains.
        if self.has_sidechains and (True in sidechains_bool.value_counts()):
            # two condition are evaluated in case the user has set sidechains
            # to True but there are actually no sidechains.
            
            sd_count = sidechains_bool.value_counts()
            
            # DataFrame with side chains
            self.allsidechains[z][y][x] = \
                self.allpeaklists[z][y][x].loc[sidechains_bool,:]

            # adds 'a' or 'b'
            self.allsidechains[z][y][x].loc[:,'ATOM'] = \
                self.allsidechains[z][y][x].loc[:,'Assign F1'].str[-1]
            
            
            self.allsidechains[z][y][x].reset_index(inplace=True)
            
            self.allsidechains[z][y][x].loc[:,'Res#'] = \
                self.allsidechains[z][y][x]['Res#'].astype(int)
            
            self.allsidechains[z][y][x].\
                sort_values(by=['Res#','ATOM'] , inplace=True)
            
            self.allsidechains[z][y][x].loc[:,'Res#'] = \
                self.allsidechains[z][y][x]['Res#'].astype(str)
            
            # creates backbone peaklist without sidechains
            self.allpeaklists[z][y][x] = \
                self.allpeaklists[z][y][x].loc[-sidechains_bool,:]
        
        # Writes sanity check
        if {'1-letter', 'Res#', '3-letter', 'Peak Status'}.\
           issubset(self.allpeaklists[z][y][x].columns):
            columns_OK = 'OK'
        
        # the script does not correct for the fact that the user sets
        # no sidechains but that actually are sidechains, 
        # though the log file register such occurrence.
        logs = '[{}][{}][{}] | * new columns inserted:  {}  \
* sidechains user setting: {} \
* sidechains identified: {} ** SD count: {}'.\
            format(z,y,x,columns_OK,
            self.has_sidechains,
            (True in sidechains_bool.value_counts()),
            sd_count[True])
        
        self.log_r(logs)
        
        return

    def correct_shifts_backbone(self, z, y, x, ref_data,
                       ref_res='1'):
        """
        Corrects Chemical Shifts in a peaklist DataFrame according
        to an internal reference peak which is chosen by user. This
        function operates only in the first dimension (xx).
        
        :ref_res: string with the number of the reference residue
        """
        
        dp_res_mask = self.allpeaklists[z][y][x].loc[:,'Res#'] == ref_res
        dp_F1_cs = self.allpeaklists[z][y][x].loc[dp_res_mask,'Position F1']
        dp_F2_cs = self.allpeaklists[z][y][x].loc[dp_res_mask,'Position F2']
        
        # Reads the information of the selected peak in the reference spectrum
        if x == self.xxref:
            
            # loads the chemical shift for F1 of the ref res
            ref_data['F1_cs'] = dp_F1_cs
            
            # loads the chemical shift for the F2 of the ref res
            ref_data['F2_cs'] = dp_F2_cs
        
        # calculates the difference between the reference chemical shift the
        # chemical shift of the reference residue in the present spectrum
        # in case we are analysing the refence spectrum this operation should
        # return 0.
        F1_cs_diff = float(dp_F1_cs) - float(ref_data['F1_cs'])
        F2_cs_diff = float(dp_F2_cs) - float(ref_data['F2_cs'])
        
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
        logs = '[{}][{}][{}] | * On residue {} * F1 ref {:.4f} \
:: correction factor {:.4f} \
* F2 ref {:.4f} \
:: correction factor {:.4f}'\
        .format(z,y,x, ref_res,
                float(ref_data['F1_cs']), F1_cs_diff, 
                float(ref_data['F2_cs']), F2_cs_diff)
        
        self.log_r(logs)
        
        # returns a dictionary containing the infomation on the reference
        # chemical shift
        return ref_data
    
    def correct_shifts_sidechains(self):
        """
        Corrects the chemical shifts of the sidechains residues
        based on the correction values previously obtained for the
        backbone residues.
        """
        self.allsidechains[z][y][x].loc[:,'Position F1'] = \
            self.allsidechains[z][y][x].loc[:,'Position F1'].sub(\
                self.allpeaklists[z][y][x].loc[0,'Pos F1 correction'])
        
        self.allsidechains[z][y][x].loc[:,'Position F2'] = \
            self.allsidechains[z][y][x].loc[:,'Position F2'].sub(\
                self.allpeaklists[z][y][x].loc[0,'Pos F2 correction'])
        
        s2w = 'Corrected sidechain shifts based on reference.'
        return None, s2w
    
    def seq_expand(self, z, y, x, tmp_vars,
                         ref_seq_dict,
                         target_seq_dict,
                         fillna_dict,
                         refscoords=None,
                         atomtype='Backbone'):
        """
        Expands the 'Res#' columns of a target peaklist (seq)
        according to a reference peaklist (seq).
        Usually, the reference peaklist is the reference experiment.
        
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
        
        # reads the reference key
        ref_key = sorted(ref_seq_dict[refcz][refcy].keys())[0]
        
        if atomtype=='Sidechain':
            print('HEREEEEEEEEEE')
            
            ref_seq_dict[z][y][ref_key].loc[:,'Res#'] = \
                ref_seq_dict[z][y][ref_key].loc[:,['Res#', 'ATOM']].\
                    apply(lambda x: ''.join(x), axis=1)
            
            
            target_seq_dict[z][y][x].loc[:,'Res#'] = \
                target_seq_dict[z][y][x].loc[:,['Res#', 'ATOM']].\
                    apply(lambda x: ''.join(x), axis=1)
        
        
        
        # reads new index from the Res# column of the reference peaklist
        ind = ref_seq_dict[refcz][refcy][ref_key].loc[:,'Res#']
        
        # stores size of new index
        length_ind = ind.size 
        
        # stores initial size of the target peaklist
        length_target_init = target_seq_dict[z][y][x].shape[0]
        
        # expands the target peaklist to the new index
        target_seq_dict[z][y][x] = \
            target_seq_dict[z][y][x].set_index('Res#').\
                                     reindex(ind).\
                                     reset_index().\
                                     fillna(fillna_dict)
    
        # reads length of the expanded peaklist
        length_target_final = target_seq_dict[z][y][x].shape[0]
        
        # transfers information of the different columns
        # from the reference to the expanded peaklist
        target_seq_dict[z][y][x].loc[:,'3-letter'] = \
            ref_seq_dict[refcz][refcy][ref_key].loc[:,'3-letter']
        
        target_seq_dict[z][y][x].loc[:,'1-letter'] = \
            ref_seq_dict[refcz][refcy][ref_key].loc[:,'1-letter']
        
        target_seq_dict[z][y][x].loc[:,'Assign F1'] = \
            ref_seq_dict[refcz][refcy][ref_key].loc[:,'Assign F1']
        
        if atomtype=='Sidechain':
            
            target_seq_dict[z][y][x].loc[:,'ATOM'] = \
                ref_seq_dict[refcz][refcy][ref_key].loc[:,'ATOM']
            
            
            target_seq_dict[z][y][x].loc[:,'Res#'] = \
                target_seq_dict[z][y][x].loc[:,'Res#'].str[:-1]
            
            ref_seq_dict[z][y][ref_key].loc[:,'Res#'] = \
                ref_seq_dict[z][y][ref_key].loc[:,'Res#'].str[:-1]
                
        
        logs = "[{}][{}][{}] vs. [{}][{}][{}] |\
 Target Initial Length :: {} \
* Template Length :: {} \
* Target final length :: {}".format(z,y,x,
                                    refcz, refcy, ref_key,
                                    length_target_init,
                                    length_ind,
                                    length_target_final)
        
        self.log_r(logs)
        
        return
        
    def organize_cols(self, z, y, x, tmp_vars, peaklist,
                         performed_cs_correction=False,
                         sidechains=False):
        """
        pd.DataFrame -> pd.DataFrame(ordered columns):

        Receives a pd.dataframe and
        organizes the columns for better visualization.

        Returns the organized dataframe.
        """
        
        if performed_cs_correction and not(sidechains):
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
                         '#',
                         'Number',
                         'index',
                         'Position F1 original',
                         'Position F2 original',
                         'Pos F1 correction',
                         'Pos F2 correction']
                         #                         'index',
        elif performed_cs_correction and sidechains:
            col_order = ['Res#',
                         'ATOM',
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
                         '#',
                         'Number',
                         'index',
                         'Position F1 original',
                         'Position F2 original',
                         'Pos F1 correction',
                         'Pos F2 correction']
        
        elif not(performed_cs_correction) and not(sidechains):
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
        
        elif not(performed_cs_correction) and sidechains:
            col_order = ['Res#',
                         'ATOM',
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
        
        
        peaklist[z][y][x] = peaklist[z][y][x][col_order]
        self.log_r('[{}][{}][{}] | Columns organized :: OK'.format(z,y,x))
        return
    
    def init_Farseer_cube(self, use_sidechains=False):
        """
        Creates a pd.Panel5D with the information of all
        the parsed peaklists from this panel, the information will
        be accessed and used to create the titration objects,
        upon each the calculations will be performed.
        
        If there are sidechains, creates a Panel5D for the sidechains, which
        are treated separately from the backbone atoms.
        """
        
        self.log_t('INITIATING FARSEER CUBE')
        self.peaklists_p5d = self.p5d(self.allpeaklists)
        self.log_r('** Created cube for all the backbone peaklists')
        
        if use_sidechains:
            self.sidechains_p5d = self.p5d(self.allsidechains)
            self.log_r('** Created cube for all the sidechains peaklists')
            
        return
    
    def gen_titration(self, titration_panel, titration_class, titration_kwargs):
        """Creates a titration object fsT.Titration."""
        
        titration_panel = \
            titration_class(np.array(titration_panel),
                            items=titration_panel.items,
                            minor_axis=titration_panel.minor_axis,
                            major_axis=titration_panel.major_axis)
             
        # activates the titration attibutes
        titration_panel.create_titration_attributes(**titration_kwargs)
        #
        return titration_panel
    
    def gen_titration_dict(self, panelT,
                                 titration_type,
                                 owndim_pts,
                                 nextdims1,
                                 nextdims2,
                                 titration_class,
                                 titration_kwargs):
        '''
        :panelT: the pd.Panel5D storing all the information of the
                 titration set transposed so that the items are the
                 observed dimension.
        :tittype: defines whether we are analysing the first,
                  the 2nd o the 3rd dim/condition.
        :owndim_pts: the points in the titype dimension.
        :nextdims1: the points in the next dimension of the titype.
        :nextdims2: the points in the 2nd next dimension.
        :res_type: whether is backbone or sidechain.
        
        
        Generates a dictionary that stores the titrations corresponding to the
        analysis of a given condition (1D, 2D or 3D).
        The generated dictionary has main key equal to the 2nd next dimension,
        subkey equal to the next dimension and stores a Titration object fsT.
        
        Therefore the dictionary[1D] stores all the experiments along the first
        dimension/condition.
        '''
        
        self.log_t(\
            'GENERATING DICTIONARY OF TITRATIONS FOR {}'.format(\
                titration_type))
        
        # initiates dictionary
        D = {}
        
        # initiates attributes that will be pased as kwargs
        titration_kwargs['titration_type'] = titration_type
        titration_kwargs['owndim_pts'] = owndim_pts
        
        for dim2_pts in nextdims2:
            #fsut.write_log(fsut.dim_sperator(dim2_pts, 'top'))
            D.setdefault(dim2_pts, {})
            for dim1_pts in nextdims1:
                #fsut.write_log(fsut.dim_sperator(dim1_pts, 'midle'))
                titration_kwargs['dim2_pts'] = dim2_pts
                titration_kwargs['dim1_pts'] = dim1_pts
                D[dim2_pts][dim1_pts] = \
                    self.gen_titration(panelT.loc[dim2_pts, dim1_pts, :, :, :],
                                       titration_class, titration_kwargs)
                #
                self.log_r('Generated titration [{}][{}] | \
with points {}'.format(dim2_pts,
                         dim1_pts,
                         list(D[dim2_pts][dim1_pts].items)))
                
                #fsut.write_log(str(D[dim2_pts][dim1_pts])+'\n')
        
        return D
    
    def exports_parsed_pkls(self, z, y, x, args):
        """
        Exports the parsed peaklists.
        """
        folder = 'spectra_parsed/{}/{}'.format(z,y)
        if not(os.path.exists(folder)):
            os.makedirs(folder)
        fpath = '{}/{}.csv'.format(folder, x)
        fileout = open(fpath, 'w')
        fileout.write(self.allpeaklists[z][y][x].to_csv(sep=',',
                                                index=False,
                                                na_rep='NaN',
                                                float_format='%.4f'))
        
        if self.has_sidechains:
            folder = 'spectra_SD_parsed/{}/{}'.format(z,y)
            if not(os.path.exists(folder)):
                os.makedirs(folder)
            fpath = '{}/{}.csv'.format(folder, x)
            fileout = open(fpath, 'w')
            fileout.write(self.allsidechains[z][y][x].to_csv(sep=',',
                                                    index=False,
                                                    na_rep='NaN',
                                                    float_format='%.4f'))
            
            fileout.close()
        return
