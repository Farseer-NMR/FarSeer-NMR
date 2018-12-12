"""
Copyright © 2017-2018 Farseer-NMR
João M.C. Teixeira and Simon P. Skinner

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

Farseer-NMR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Farseer-NMR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
"""
#import logging
#import logging.config
import os
import numpy as np
import pandas as pd
import itertools as it

import core.fslibs.Logger as Logger
from core.utils import aal1tol3, aal3tol1
from core.fslibs.WetHandler import WetHandler as fsw
from core.fslibs.FastaHandler import FastaHandler

class FarseerCube:
    """
    The Farseer-NMR Data set.
    
    Reads all the experimental input peaklists to a hierarchical nested
    dictionary where the hierarchy is dictated by the acquisition
    schedule of the different measured variables (temperature,
    ligand ratio, etc...).
    Peaklists should be stored in a 'spectra' folder.
    
    Peaklists in dictionary are read as pd.DataFrames.
    
    Formats all the peaklists to the same size.
    
    Generates the Farseer-NMR Cube: a 5-dimension Panel containing the
    whole data set.
    
    Parameters:
        paths (list): absolute paths of all the input peaklists
        
        allpeaklists (dict): nested dictionary created from 'spectra'.
            Stores all the peaklists (.csv) in pd.DataFrame format.
            Only data regarding Backbone atoms.
        
        allsidechains (dict): same as allpeaklists but only Sidechains
            parsed data.
        
        allfasta (dict): nested dictionary containing the FASTA
            information for each Y data point as a pd.DataFrame.
        
        FASTAstart (int): The number of the first residue of the FASTA
            secuence.
        
        has_sidechains (bool): True if input peaklists have Sidechains
            information.
        
        xxcoords, yycoords, zzcoords (list): the Farseer-NMR Cube axes 
            coordinate names.
        
        xxref, yyref, zzref (str): the names of the first data point
            for eachdimension. Created in .init_coords_names().
        
        hasxx, hasyy, haszz (bool): True if there are more than one data
            point along that dimension. False otherwise (default).
        
        p5d (pandas.Panel): a 5-dimension pandas.Panel.
    
        tmp_vars (dict): stored temporary variables for functions.
    """
    def __init__(
            self, spectra_path,
            has_sidechains=False,
            applyFASTA=False,
            FASTAstart=1):
        """
        Initiates the object,
        
        spectra_path (str): the path where the spectra (.csv files)
            are located.
        
        has_sidechains (bool): True if the peaklists contain information 
            on Sidechains residues. False otherwise (default).
        
        applyFASTA (bool): True to complete sequence with FASTA
            information. Defaults to False.
        
        FASTAstart (int): The first residue in the FASTA file.
        """
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        #logging.config.dictConfig(fslogconf.farseer_log_config)
        self.logger.debug('logger initiated')
        
        # Decomposing the 'spectra' path
        # self.paths will be used in load_experiments()
        # http://stackoverflow.com/questions/14798220/how-can-i-search-sub-folders-using-glob-glob-module-in-python
        self.paths = \
            sorted(
                [os.path.join(dirpath, f) 
                    for dirpath, dirnames, files in os.walk(spectra_path) 
                        for f in files]
                )
        # Initiates the different nested dictionaries
        self.allpeaklists = {}
        self.allsidechains = {}
        self.allfasta = {}
        # Initiates dictionary for helper variables
        self.tmp_vars = {}
        # loads user input information into the instance
        self.has_sidechains = has_sidechains
        self.FASTAstart = FASTAstart
        self.applyFASTA = applyFASTA
        # lists that contain axes datapoint names
        self.zzcoords = None
        self.yycoords = None
        self.xxcoords = None
        # Bool. True if axis has more than one datapoint.
        # False if axis has only one data point.
        # evaluated in .init_coords_names()
        self.haszz = False
        self.hasyy = False
        self.hasxx = False
        # writes to log
        self.logs('Initiates Farseer Set', istitle=True)
        input_log = \
"""Path to peaklists dataset: {}  
User states peaklists contain sidechain information: {}  
FASTA starting residue: {}  """.\
            format(
                spectra_path,
                self.has_sidechains,
                self.FASTAstart
                )
        self.logs(input_log)
        # initiates panel 5D object to initiate Farseer-NMR Cube
        # in .init_Farseer_cube()
        self.p5d = pd.core.panelnd.create_nd_panel_factory(
            klass_name='Panel5D',
            orders=['cool', 'labels', 'items', 'major_axis', 'minor_axis'],
            slices={
                'labels': 'labels',
                'items': 'items',
                'major_axis': 'major_axis',
                'minor_axis': 'minor_axis'
                },
            slicer=pd.Panel4D,
            aliases={'major': 'index', 'minor': 'minor_axis'},
            stat_axis=2
            )
        
    
    def _abort(self, wet):
        """
        Aborts run with message. Writes message to log.
        
        Parameters:
            - wet (WetHandler)
        """
        self.logs(wet.wet)
        self.logs(wet.abort_msg())
        wet.abort()
        
        return None
    
    def _check_ref_res(self, series, ref_res):
        """
        Checks if the reference residue is part of the protein sequence.
        
        Parameters:
            series (pd.Series): the protein primary sequence.
            
            ref_res (int): the residue number.
        """
        
        if any(series.isin([ref_res])):
            return None
        
        else:
            msg = \
'The reference residue you selected, {}, is not part of the protein sequence \
or is an <unassigned> or <missing> residue. \
Correct the reference residue in the Settings Menu.'.\
                format(ref_res)
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=16))
        
        return None
    
    def _checks_posf1_posf2_nuclei(self, target):
        """
        Confirms coherency between Columns label and nuclei type.
        
        Demmands that cols "Position F1" and "Assign F1" refer to 1H
        and "Position F2" and "Assign F2" to 15N.
        
        Must be called after self.init_coord_names()
        
        Parameters:
            target: Nested Dictionary of pd.DatFrame containing
                the peaklist information.
        """
        
        for z, y, x in it.product(self.zzcoords, self.yycoords, self.xxcoords):
            
            if not(0 < target[z][y][x].loc[:,'Position F1'].mean() < 20):
                msg = 'Peaklist [{}][{}][{}] "Position F1" values do not \
correspond to proton chemical shift values.'.format(z, y, x)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=25))
            
            if not(target[z][y][x].ix[0,'Assign F1'].endswith('H')):
                msg = 'Peaklist [{}][{}][{}] "Assign F1" values do not \
correspond to proton assignment labels.'.format(z, y, x)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=25))
            
            if not(80 < target[z][y][x].loc[:,'Position F2'].mean() < 150):
                msg = 'Peaklist [{}][{}][{}] "Position F2" values do not \
correspond to nitrogen chemical shift values.'.format(z, y, x)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=25))
            
            if not(target[z][y][x].ix[0,'Assign F2'].endswith('N')):
                msg = 'Peaklist [{}][{}][{}] "Assign F2" values do not \
correspond to nitrogen assignment labels.'.format(z, y, x)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=25))
        
        return None
    
    def _checks_filetype(self, filetype):
        """
        Confirms that file type exists in 'spectra' before loading.
        
        If not, call WET#9.
        
        If file not .csv or .fasta, call WET#13.
        
        Parameters:
            filytype (str): {'.csv', '.fasta'}
        """
        
        # check filetype fits usable formats
        if not(filetype in ['.csv', '.fasta']):
            msg = \
"File type {} not recognized. Why you want to read these files \
if Farseer-NMR can't do nothing with them? :-)".\
                format(filetype)
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=13))
        
        # checks if files exists
        if not(any([p.endswith(filetype) for p in self.paths])):
            msg = "There are no files in 'spectra' folder with extension {}".\
                format(filetype)
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=9))
            
        return None
    
    def _checks_xy_datapoints_coherency(self, target, filetype):
        """
        Confirms axis names along Y folders and X files.
        
        Confirms Y folder names are equal accross every Z folder.
        Raises WET#11 otherwise.
        
        Confirms each Y folder has one and ONLY on .fasta file.
        Raises WET#12 otherwise.
        
        Confirms wether the number of files of <filetype> is the same
        in every subdirectory of 'spectra'.
        Raises WET#8 otherwise.
        
        Confirms that the files of <filetype> have the same names in all
        the Y datapoints subfolders.
        Raises names mismatches with WET#10.
        
        Parameters:
            target (dict): nested dictionary representing the
                folder tree in 'spectra'
            
            filetype (str): {'.csv', '.fasta'}
        """
        
        zkeys = list(target.keys())
        ykeys = list(target[zkeys[0]].keys())
        xkeys = list(target[zkeys[0]][ykeys[0]].keys())
        key_len = len(zkeys) * len(ykeys) * len(xkeys)
        self.logger.debug("x: {}, y: {}, z: {}".format(xkeys, ykeys, zkeys))
        self.logger.debug("key_len: {}".format(key_len))
        ### Checks coherency of y folders
        all_y_folders = \
            set([os.path.split(os.path.split(y)[0])[1]
                for y in self.paths if y.endswith(filetype)])
        
        self.logger.debug("all_y_folders: {}".format(all_y_folders))
        
        if len(set(all_y_folders)) > len(ykeys):
            msg = \
"Y axis folder names are not coherent. \
Names must be equal accross every Z axis datapoint folder."
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=11))
        
        if filetype == '.fasta':
            all_fasta_files = \
                [os.path.basename(x) for x in self.paths if x.endswith(filetype)]
            
            
            if len(all_fasta_files) != (len(ykeys) * len(zkeys)):
                msg = \
"There are too many or missing {0} files. \
Confirm there is only ONE {0} file for each Y datapoint folder.".\
                    format(filetype)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=12))
        
        ### Checks coherency of x files
        elif filetype == '.csv':
            if key_len \
                    != len([x for x in self.paths if x.endswith(filetype)]):
                msg =  \
'The no. of files of type {} is not the same for every series folder. \
Check for the missing ones!'.\
                    format(filetype)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=8))
            
            x_files_names = set(
                [os.path.basename(x) for x in self.paths if x.endswith(filetype)]
                )
            
            if (len(x_files_names) > len(xkeys)):
                msg = \
"X axis datapoints file names are not coherent. \
Names must be equal accross every Y axis datapoint folder.".\
                    format(filetype)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=10))
        
        # writes confirmation message
        self.logs('> All <{}> files found and correct - OK!'.format(filetype))
        
        return None
    
    def _checks_fasta_start_number(self):
        """
        Confirms if the start or end number of the fasta file 
        won't result in protein truncation in the peaklist.
        
        This occurs when first fasta residue is > first protein residue.
        This occurs when last fasta residue is < last protein residue.
        
        Raises WET#22 otherwise.
        """
        
        if not(self.applyFASTA):
            return None
        
        if not(self.zzcoords and self.allfasta):
            msg = \
"Operation cannot complete because Cube coordinates have not been set \
or fasta files have not yet been read."
            print(msg)
            
            return None
        
        for z, y, x in it.product(self.zzcoords, self.yycoords, self.xxcoords):
            # name of the fasta file being read
            f = list(self.allfasta[z][y].keys())[0]
            peaklist_first_residue = \
                int(self.allpeaklists[z][y][x].loc[:,'ResNo'].head(n=1))
            peaklist_last_residue = \
                int(self.allpeaklists[z][y][x].loc[:,'ResNo'].tail(n=1))
            fasta_first_residue = \
                int(self.allfasta[z][y][f].loc[:,'ResNo'].head(n=1))
            fasta_last_residue = \
                int(self.allfasta[z][y][f].loc[:,'ResNo'].tail(n=1))
            
            if fasta_first_residue <= peaklist_first_residue \
                    and fasta_last_residue >= peaklist_last_residue:
                continue
            
            elif fasta_first_residue > peaklist_first_residue:
                msg = \
"The first residue of your fasta file is greater than your protein first \
residue for FASTA file [{0}][{1}][{3}] and peaklist [{0}][{1}][{2}], \
which will results in peaklist truncation. \
You should verify that your start Fasta residue number is correct.".\
                    format(z, y, x, f)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=22))
            
            elif fasta_last_residue < peaklist_last_residue:
                msg = \
"The last residue of your fasta file is minor than your protein \
last residue for FASTA file [{0}][{1}][{3}] and peaklist [{0}][{1}][{2}], \
which will results in peaklist truncation. \
You should verify that your start Fasta residue number is correct.".\
                    format(z, y, x, f)
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=22))
            
            else:
                msg = 'Something is wrong in ._checks_fasta_start_number()'
                self._abort(fsw.gen_wet('DEVELOPER ISSUE', msg, -1))
            
        else:
            msg = "> FASTA files starting number is consistent with peaklists"
            self.logs(msg)
        
        return None
    
    def _check_res_duplicates(self, df, z, y, x):
        """
        Checks if there are duplicated residue entries in peaklists.
        
        Parameters:
            - df (pd.DataFrame): the peaklist dataframe to investigate
        """
        where_duplicates = df[z][y][x].loc[:,'ResNo'].duplicated(keep=False)
        
        if where_duplicates.any():
            msg = "The peaklist [{}][{}][{}] contains repeated residue entries \
in lines: {}.".format(
                z,
                y,
                x,
                [2+int(i) for i in \
                    where_duplicates.index[where_duplicates].tolist()]
                )
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=24))
        
        return None
    
    def _checks_misleading_chars(self, z, y, x):
        """
        Checks for the presence misleading characters in the DataFrame.
        This may come from entries of unassigned residues
        that were not removed.
        """
        # for assignment cols
        ## empty
        empty_cells_f1 = self.allpeaklists[z][y][x].loc[:,'Assign F1'].isnull()
        empty_cells_f2 = self.allpeaklists[z][y][x].loc[:,'Assign F2'].isnull()
        
        if empty_cells_f1.values.any() or empty_cells_f2.values.any():
            rows_bool = empty_cells_f1 | empty_cells_f2
            msg = "The peaklist [{}][{}][{}] contains no assignment \
information in lines {}. Please review that peaklist.".format(
                z,
                y,
                x,
                [2+int(i) for i in rows_bool.index[rows_bool].tolist()]
                )
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=29))
        
        ## misleading chars
        non_digit_f1 = \
            self.allpeaklists[z][y][x].loc[:,'Assign F1'].\
                str.strip().str.contains('\W', regex=True)
        
        non_digit_f2 = \
            self.allpeaklists[z][y][x].loc[:,'Assign F2'].\
                str.strip().str.contains('\W', regex=True)
        
        if  non_digit_f1.any() or non_digit_f2.any():
            rows_bool = non_digit_f1 | non_digit_f2
            msg = "The peaklist [{}][{}][{}] contains misleading \
charaters in Assignment columns in line {}.".format(
                z,
                y,
                x,
                [2+int(i) for i in rows_bool.index[rows_bool].tolist()]
                )
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=29))
        
        ## for other cols.
        cols = [
            'Position F1',
            'Position F2',
            'Height',
            'Volume',
            'Line Width F1 (Hz)',
            'Line Width F2 (Hz)',
            'Merit'
            ]
        
        for col in cols:
            non_digit = self.allpeaklists[z][y][x].loc[:,col].\
                astype(str).str.strip().str.contains(
                    '[\!\"\#\$\%\&\\\'\(\)\*\,\-\/\:\;\<\=\>\?\@\[\]\^\_\`\{\|\}\~]',
                    regex=True
                    )
            if non_digit.any():
                msg = "The peaklist [{}][{}][{}] contains misleading \
charaters in line {} of column [{}].".format(
                    z,
                    y,
                    x,
                    [2+int(i) for i in non_digit.index[non_digit].tolist()],
                    col
                    )
                self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=29))
        
        return None
    
    def _compare_fastas(self):
        """
        Compares all .fasta files to confirm they have the same size.
        Farseer cannot operate FASTA of different lengths if analysing
        on the y dimension.
        """
        
        if not(self.applyFASTA):
            return None
        
        l = []
        is_bigger = False

        for z in self.zzcoords:
            for y in self.yycoords:
                key = list(self.allfasta[z][y].keys())[0]
                l.append(self.allfasta[z][y][key].shape[0])
            
            if len(set(l)) > 1:
                is_bigger = True
            
            l = []
        
        if is_bigger:
            msg = \
'.fasta files have not the same size and they should have the same size \
when performing calculations along the Y axis. \
Please correct your .fasta files.'
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=21))
        
        return None
    
    def _compare_peaklists_length(self, dp1, dp2, axis, df_dict):
        """
        Verifies if all peaklists in a series have the same number of 
        residues before a FarseerSeries object is created.
        
        Parameters:
            - dp1 (str): datapoint name on the next dimension.
            
            - dp2 (str): datapoint name on the previous dimension.
            
            - axis (str): the axis long which the series will be generated.
            
            - df_dict (dict:pd.DataFrame): A dictionary containing
                pd.DataFrames corresponding to peaklists.
        """
        
        pkl_lengths = []
        
        for key, peaklist in df_dict.items():
            pkl_lengths.append(peaklist.shape[0])
        
        if not(len(set(pkl_lengths))) == 1:
            msg = "Peaklists proposed for series [{}][{}] along {} axis have \
different lengths.".\
                format(dp2, dp1, axis[-1].upper())
            self._abort(fsw(msg_title="ERROR", msg=msg, wet_num=28))
        
        return None
    
    def logs(self, logstr, istitle=False):
        """
        Registers activity to the log string and prints it.
        
        logstr (str): the string to be registered in the log.
        istitle (bool): flag to format logstr as a title.
        """
        # formats logstr
        if istitle:
            logstr = \
"""
{0}  
{1}  
{0}  
""".\
                format('*'*79, logstr.upper())
        
        self.logger.info(logstr)
        
        return None
    
    def _init_coords_names(self):
        """
        Identifies coordinate names (conditions measured) for the
        Farseer-NMR Cube.
        
        Modify:
            self.xxcoords
            self.yycoords
            self.zzcoords
            self.xxref (str): the name of the first axis datapoint.
            self.yyref (str): idem
            self.zzref (str): idem
        """
        
        self.logs('IDENTIFIED FARSEER CUBE VARIABLES', istitle=True)
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
        
        logs = \
"""
* Farseer Cube X axis variables (along_x): {}
* Farseer Cube Y axis variables (along_y): {}
* Farseer Cube Z axis variables (along_z): {}
""".\
            format(self.xxcoords, self.yycoords, self.zzcoords)
        self.logs(logs)
        
        return None
    
    def _transfer_coords_names(self):
        """
        Transfer coordinate names from allpeaklists to allsidechains.
        """
        for z in self.allpeaklists.keys():
            self.allsidechains.setdefault(z, {})
            
            for y in self.allpeaklists[z].keys():
                self.allsidechains[z].setdefault(y, {})
                
                for x in self.allpeaklists[z][y].keys():
                    self.allpeaklists[z][y].setdefault(x, None)
        
        
        self.logger.debug("allpeaklists keys transferred to allsidechains")
        
        return
    
    def split_res_info(self):
        """
        Splits assignment information.
        
        Receives a DataFrame with the original assignment information
        (AssignF1) and adds four columns to the DataFrame:

        ['ResNo', '1-letter', '3-letter', 'Peak Status']

        where:
        'ResNo' is the residue number
        '1-letter', is the 1-letter code residue name
        '3-letter', is the 3-letter code residue name if the assignment
            belongs to a side-chain resonance, a character 'a' or 'b'
            is added to the '1-letter' and '3-letter' codes.
        'Peak Status', assigns string 'measured' to identify the peaks
            present in this peaklist as experimentally measured.
        
        Procedure:
        
        1. Extracts residue information from 'Assigned F1' column,
        separating the residue name from the residue number. This
        creates a new pd.DataFrame with column names 'ResNo' and
        '3-letter'.
        
            '1MetH' -> '1' and 'Met'
        
        2. Generates the 1-letter column code from the 3-letter code
        column. In the same pd.DataFrame. 
        
        3. Concatenates the new generated pd.DataFrame with the input
        peaklist pd.Dataframe. And adds column 'Peak Status' with value
        'measured'.
        
            3.1 if peaklist is empty adds all dummy rows of type <missing>.
        
        4. Sorts the peaklist according to 'ResNo' just in case the
        original .CSV file was not sorted. For correct sorting 'ResNo'
        as to be set astype int and returned back to str.

        (conditional). If sidechains are present in the peaklist:
        identifies the sidechains entries (rows) and counts the number
        of sidechain entries. Adds the letter 'a' or 'b' to new column
        'ATOM' to identify the two sidechains resonances.
        """
        
        title = 'IDENTIFIES RESIDUE INFORMATION FROM ASSIGNMENT COLUMN'
        self.logs(title, istitle=True)
        
        for z, y, x in it.product(self.zzcoords, self.yycoords, self.xxcoords):
            
            # checks misleading chars
            self._checks_misleading_chars(z, y, x)
            
            # Step 1
            resInfo = \
                self.allpeaklists[z][y][x].\
                    loc[:,'Assign F1'].str.extract('(\d+)(.{3})', expand=True)
            resInfo.columns = ['ResNo', '3-letter']
            
            # Step 2
            resInfo.loc[:,'1-letter'] = \
                resInfo.loc[:,"3-letter"].map(aal3tol1.get)
            
            # Step 3
            self.allpeaklists[z][y][x] = \
                pd.concat([self.allpeaklists[z][y][x], resInfo], axis=1)
            
            # Adds the 'Peak Status' Column. All the peaks in the peaklist
            # at this stage are peaks that have been measured and are
            # identified in the NMR spectrum. Therefore all the peaks here
            # are labeled as 'measured'. On later stages of the script
            # peaks not identified will be added to the peaklist, and those
            # peaks will be label as 'missing' or 'unassigned'.
            try:
                self.allpeaklists[z][y][x].loc[:,'Peak Status'] = 'measured'
            
            except ValueError:
                # if the peaklist is an empty file containing only the header.
                self.allpeaklists[z][y][x] = \
                    self.allpeaklists[z][y][self.xxref].copy()
                self.allpeaklists[z][y][x].\
                    loc[:,[
                        'Peak Status',
                        'Merit',
                        'Position F1',
                        'Position F2',
                        'Height',
                        'Volume',
                        'Line Width F1 (Hz)',
                        'Line Width F2 (Hz)'
                        ]
                    ] = [
                            'missing',
                            np.nan,
                            np.nan,
                            np.nan,
                            np.nan,
                            np.nan,
                            np.nan,
                            np.nan
                            ]
            
            # sidechains entries always end with an 'a' or 'b' in the AssignF1
            # use of regex: http://www.regular-expressions.info/tutorial.html
            # identify the sidechain rows
            sidechains_bool = \
                self.allpeaklists[z][y][x].\
                    loc[:,'Assign F1'].str.contains('[^HN]$')
            self.has_sidechains = any(sidechains_bool)
            
            self.logger.debug("sidechains_bool.value_counts(): {}".format(
                sidechains_bool.value_counts()
                ))
            self.logger.debug("Any? {}".format(self.has_sidechains))
            # initiates SD counter
            sd_count = {True:0}
            
            # if the user says it has sidechains and there are actually sidechains.
            
            if self.has_sidechains:
                
                self.logger.debug("<has_sidechains> set to: {}".format(self.has_sidechains))
                self.logger.debug("Is self.allsidechains? {}".format(bool(self.allsidechains)))
                
                # two condition are evaluated in case the user has set 
                #sidechains to True but there are actually no sidechains.
                sd_count = sidechains_bool.value_counts()
                # DataFrame with side chains
                self.allsidechains[z][y][x] = \
                    self.allpeaklists[z][y][x].loc[sidechains_bool,:]
                # adds sidechain nomenclature
                self.allsidechains[z][y][x].loc[:,'ATOM'] = \
                    self.allsidechains[z][y][x].loc[:,'Assign F1'].\
                        str.split('[HN]', expand=True).loc[:,1]
                # resets index
                self.allsidechains[z][y][x].reset_index(inplace=True)
                # ResNo column to int preparing for reindex
                self.allsidechains[z][y][x].loc[:,'ResNo'] = \
                    self.allsidechains[z][y][x]['ResNo'].astype(int)
                # sorted dataframe based on ResNo and ATOM 'a' 'b' type
                self.allsidechains[z][y][x].\
                    sort_values(by=['ResNo','ATOM'] , inplace=True)
                # revers ResNo to string
                self.allsidechains[z][y][x].loc[:,'ResNo'] = \
                    self.allsidechains[z][y][x]['ResNo'].astype(str)
                # creates backbone peaklist without sidechains
                self.allpeaklists[z][y][x] = \
                    self.allpeaklists[z][y][x].loc[-sidechains_bool,:]
            
            # Step 4
            self._check_res_duplicates(self.allpeaklists, z, y, x)
            self.allpeaklists[z][y][x].loc[:,'ResNo'] = \
                self.allpeaklists[z][y][x]['ResNo'].astype(int)
            self.allpeaklists[z][y][x].sort_values(by='ResNo', inplace=True)
            self.allpeaklists[z][y][x].loc[:,'ResNo'] = \
                self.allpeaklists[z][y][x].loc[:,'ResNo'].astype(str)
            self.allpeaklists[z][y][x].reset_index(inplace=True)
            
            # Writes sanity check
            if {'1-letter', 'ResNo', '3-letter', 'Peak Status'}.\
                    issubset(self.allpeaklists[z][y][x].columns):
                columns_OK = 'OK'
            
            # the script does not correct for the fact that the user sets
            # no sidechains but that actually are sidechains, 
            # though the log file register such occurrence.
            logs = \
'**[{}][{}][{}]** new columns inserted:  {}  \
| sidechains user setting: {} \
| sidechains identified: {} | SD count: {}'.\
                format(
                    z,
                    y,
                    x,
                    columns_OK,
                    self.has_sidechains,
                    (True in sidechains_bool.value_counts()),
                    sd_count[True]
                    )
            
            self.logs(logs)
            
        # confirms F1 and F2 coherency with nuclei
        self._checks_posf1_posf2_nuclei(self.allpeaklists)
        
        return None
    
    def correct_shifts_backbone(self, ref_res):
        """
        Corrects Chemical Shifts in a peaklist according to an internal 
        reference peak.
        
        This function operates only along the X axis and for Backbone.
        Cycles over all the Z and Y data points.
        
        Parameters:
            ref_res (int): the reference residue number.
        """
        
        # confirms correct input
        if isinstance(ref_res, int):
            ref_res = str(ref_res)
        
        else:
            msg = \
'Argument ref_res for method .correct_shifts_backbone() must be of type <int>.'
            self.logs(msg)
            
            return
        
        self._check_ref_res(
            self.allpeaklists[self.zzref][self.yyref][self.xxref].\
                loc[:,'ResNo'],
            ref_res
            )
        title = 'CORRECTS BACKBONE CHEMICAL SHIFTS BASED ON A RESIDUE {}'.\
            format(ref_res)
        self.logs(title, istitle=True)
        ref_data = {}
        
        for z, y, x in it.product(self.zzcoords, self.yycoords, self.xxcoords):
            dp_res_mask = \
                self.allpeaklists[z][y][x].loc[:,'ResNo'] == ref_res
            dp_F1_cs = \
                self.allpeaklists[z][y][x].loc[dp_res_mask,'Position F1']
            dp_F2_cs = \
                self.allpeaklists[z][y][x].loc[dp_res_mask,'Position F2']
            
            # Reads the information of the selected peak in the reference
            # spectrum
            if x == self.xxref:
                # loads the chemical shift for F1 of the ref res
                ref_data['F1_cs'] = dp_F1_cs
                # loads the chemical shift for the F2 of the ref res
                ref_data['F2_cs'] = dp_F2_cs
            
            # For the reference residue, calculates the difference between the 
            # chemical shift in the reference and the current spectra. If 
            # current == reference, difference should yield 0.
            F1_cs_diff = float(dp_F1_cs) - float(ref_data['F1_cs'])
            F2_cs_diff = float(dp_F2_cs) - float(ref_data['F2_cs'])
            # copies the chemical shift data to a backup column
            self.allpeaklists[z][y][x].loc[:,'Position F1 original'] = \
                self.allpeaklists[z][y][x].loc[:,'Position F1']
            self.allpeaklists[z][y][x].loc[:,'Position F2 original'] = \
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
            logs = \
'**[{}][{}][{}]** | F1: {:.4f}-{:.4f}={:.4f} | F2: {:.4f}-{:.4f}={:.4f}'.\
                format(
                    z,
                    y,
                    x,
                    float(dp_F1_cs), float(ref_data['F1_cs']), F1_cs_diff, 
                    float(dp_F2_cs), float(ref_data['F2_cs']), F2_cs_diff
                    )
            self.logs(logs)
        
        return None
    
    def correct_shifts_sidechains(self):
        """
        Corrects Chemical Shifts to a reference peak in ref spectrum.
        
        Can only be performed after .correct_shifts_backbone().
        
        This function operates only along the X axis and for Backbone.
        Cycles over all the Z and Y data points.
        """
        
        title = \
'CORRECTS SIDECHAINS CHEMICAL SHIFTS BASED ON Previous backbone correction'
        self.logs(title, istitle=True)
        
        for z, y, x in it.product(self.zzcoords, self.yycoords, self.xxcoords):
            self.allsidechains[z][y][x].loc[:,'Position F1'] = \
                self.allsidechains[z][y][x].loc[:,'Position F1'].\
                    sub(self.allpeaklists[z][y][x].loc[0,'Pos F1 correction'])
            self.allsidechains[z][y][x].loc[:,'Position F2'] = \
                self.allsidechains[z][y][x].loc[:,'Position F2'].\
                    sub(self.allpeaklists[z][y][x].loc[0,'Pos F2 correction'])
            s2w = \
'**[{}][{}][{}]** Corrected chemical shift fot sidechain residues.'.\
                format(z, y, x)
            self.logs(s2w)
        
        return None
    
    def seq_expand(self, ref_pkl, target_pkl, resonance_type, fillna):
        """
        Expands a <target> peaklist to the size of the <reference>.
        Adds rows of missing residues.
        
        Parameters:
            ref_pkl (pd.DataFrame): the reference peaklist
            
            target_pkl (pd.DataFrame): the target peaklist
            
            resonance_type (str): {'Backbone'. 'Sidechain'}
            
            fillna (dict): a dictionary of kwargs that define the column
                values of the newly generated rows. Example:
                    {'Peak Status': <missing>,
                     'Merit': 0.0,
                     'Details': 'None'}
        
        Returns:
            The expanded pd.DataFrame
            A list with information on the peaklist length evolution
                [target initial length, ref length, target final length]
        """
        # merges ResNo and ATOM cols to keep sorted
        if resonance_type=='Sidechains':
            ref_pkl.loc[:,'ResNo'] = \
                ref_pkl.loc[:,['ResNo', 'ATOM']].\
                    apply(lambda x: ''.join(x), axis=1)
            target_pkl.loc[:,'ResNo'] = \
                target_pkl.loc[:,['ResNo', 'ATOM']].\
                    apply(lambda x: ''.join(x), axis=1)
        
        # creates an index based on the residue numbers of the reference
        # peaklist
        ind = ref_pkl.loc[:,'ResNo']
        # reads size of reference index
        length_ind = ind.size 
        # reads size of target peaklist
        target_ind_init_len = target_pkl.shape[0]
        # expands the target peaklist to the new index
        try:
            target_pkl = \
                target_pkl.set_index('ResNo').\
                    reindex(ind).reset_index().fillna(fillna)
        except ValueError:
            msg = "Farseer-NMR could not reindex this peaklist. There are \
several input errors that may occur in this case. Read the Documentation for \
more details." 
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=24))
        
        # reads length of the expanded peaklist
        target_ind_final_len = target_pkl.shape[0]
        # transfers information of the different columns
        # from the reference to the expanded peaklist
        target_pkl.loc[:,'3-letter'] = ref_pkl.loc[:,'3-letter']
        target_pkl.loc[:,'1-letter'] = ref_pkl.loc[:,'1-letter']
        target_pkl.loc[:,'Assign F1'] = ref_pkl.loc[:,'Assign F1']
        target_pkl.loc[:,'Assign F2'] = ref_pkl.loc[:,'Assign F2']
        
        # reverts previous merge
        if resonance_type=='Sidechains':
            target_pkl.loc[:,'ATOM'] = ref_pkl.loc[:,'ATOM']
            target_pkl.loc[:,'ResNo'] = ref_pkl.loc[:,'ResNo'].str.extract('(\d+)', expand=False)
            ref_pkl.loc[:,'ResNo'] = ref_pkl.loc[:,'ResNo'].str.extract('(\d+)', expand=False)
        
        tmp_list = [
                target_ind_init_len, 
                length_ind, 
                target_ind_final_len
                ]
        
        return target_pkl, tmp_list
    
    def compares_references(
            self,
            fillna_dict,
            along_axis='z',
            resonance_type='Backbone'
            ):
        """
        Assigns missing residues for reference of Y and Z based on X.
        
        
        Compares reference experiments along Y and Z axis and adds
        missing residues considering [xxref][yyref][zzref] as the main
        reference.
        
        Uses .seq_expand().
        
        Parameters:
            fillna_dict (dict): a dictionary of kwargs that define
                values of the newly generated rows. Example:
                    {'Peak Status': <missing>,
                     'Merit': 0.0,
                     'Details': 'None'}
            
            along_axis (str): {'y', 'z'}, defaults 'z'.
            
            resonance_type (str): {'Backbone', 'Sidechains'}, defaults 
                'Backbone'.
        
        Modifies:
            The values in self.allpeaklists or self.allsidechains.
        """
        title = 'adds missing residues along axis {}'.format(along_axis)
        self.logs(title, istitle=True)
        
        if resonance_type == 'Backbone':
            target = self.allpeaklists
        
        elif resonance_type == 'Sidechains':
            target = self.allsidechains
        
        else:
            msg = 'Argument <resonance_type> is not valid.'
            self.logs(msg)
            return
        
        if not(along_axis in ['y', 'z']):
            msg = 'Argument <along_axis> is not valid.'
            self.logs(msg)
            return
        
        elif (along_axis == 'y' and not(self.hasyy)) \
                or (along_axis == 'z' and not(self.haszz)):
            # DO
            msg = \
'There are no data points along dimension {}. This function has no effect.'.\
                format(along_axis.upper())
            wet19 = fsw(msg_title='NOTE', msg=msg, wet_num=19)
            self.logs(wet19.wet)
            return
            
        elif along_axis == 'z':
            for y, z in it.product(self.yycoords, self.zzcoords):
                if z == self.zzref:
                    ref_pkl = target[z][y][self.xxref]
                    refz = z
                    refy = y
                
                target[z][y][self.xxref], popi = \
                    self.seq_expand(
                        ref_pkl.copy(), 
                        target[z][y][self.xxref].copy(),
                        resonance_type,
                        fillna_dict
                        )
                logs = \
"**[{}][{}][{}]** vs. [{}][{}][{}] \
| Target Initial Length :: {} \
| Template Length :: {} \
| Target final length :: {}".\
                    format(
                        z,
                        y,
                        self.xxref,
                        refz,
                        refy,
                        self.xxref,
                        popi[0],
                        popi[1],
                        popi[2]
                        )
                self.logs(logs)
        
        elif along_axis == 'y':
            for z, y in it.product(self.zzcoords, self.yycoords):
                if y == self.yyref:
                    ref_pkl = target[z][y][self.xxref]
                    refz = z
                    refy = y
        
                target[z][y][self.xxref], popi = \
                    self.seq_expand(
                        ref_pkl.copy(),
                        target[z][y][self.xxref].copy(),
                        resonance_type,
                        fillna_dict
                        )
                logs = \
"**[{}][{}][{}]** vs. [{}][{}][{}] \
| Target Initial Length :: {} \
| Template Length :: {} \
| Target final length :: {}".\
                    format(
                        z,
                        y,
                        self.xxref,
                        refz,
                        refy,
                        self.xxref,
                        popi[0],
                        popi[1],
                        popi[2]
                        )
                self.logs(logs)
        
        return None
    
    def finds_missing(
            self,
            fillna_dict, 
            missing='missing',
            resonance_type='Backbone'
            ):
        """
        Finds missing residues.
        
        Runs over each X axis series and finds the missing residues
        comparing each data point to the reference experiment on that
        series.
        
        Missing residues can be of type 'missing' or 'unassigned'.
        
        Parameters:
            fillna_dict (dict): a dictionary of kwargs that define
                values of the newly generated rows. Example:
                    {'Peak Status': <missing>,
                     'Merit': 0.0,
                     'Details': 'None'}
            
            missing (str): {'missing', 'unassigned'}
            
            resonance_type (str): {'Backbone', 'Sidechains'}
        
        Modifies:
            The values in self.allpeaklists or self.allsidechains.
        """
        
        title = 'Searches for {} residues'.format(missing)
        self.logs(title, istitle=True)
        
        if not(missing in ['missing', 'unassigned']):
            msg = "<missing> argument must be 'missing' or 'unassigned'."
            self.logs(msg)
            return
        
        # before expanding the peaklists to the fasta file to identify the 
        # unassigned residues, it confirms the integrity of the fasta Starting
        # number.
        if missing == 'unassigned':
            self._checks_fasta_start_number()
        
        if resonance_type == 'Backbone':
            target = self.allpeaklists
        
        elif resonance_type == 'Sidechains':
            target = self.allsidechains
        
        else:
            msg = \
"<resonance_type> argument must be 'Backbone' or 'Sidechains'."
            self.logs(msg)
            return
        
        for z, y, x in it.product(self.zzcoords, self.yycoords, self.xxcoords):
            # sets the reference peaklist
            if x == self.xxref and missing == 'missing':
                ref_pkl = target[z][y][x]
                refz = z
                refy = y
                refx = x
            
            elif x == self.xxref and missing == 'unassigned':
                ref_fasta_key = list(self.allfasta[z][y].keys())[0]
                ref_pkl = self.allfasta[z][y][ref_fasta_key]
                refz = z
                refy = y
                refx = ref_fasta_key
            
            target[z][y][x], popi = \
                self.seq_expand(
                    ref_pkl.copy(),
                    target[z][y][x].copy(),
                    resonance_type,
                    fillna_dict
                    )
            
            logs = \
"**[{}][{}][{}]** vs. [{}][{}][{}] \
| Target Initial Length :: {} \
| Template Length :: {} \
| Target final length :: {}".\
                format(
                    z,
                    y,
                    x,
                    refz,
                    refy,
                    refx,
                    popi[0],
                    popi[1],
                    popi[2]
                    )
            self.logs(logs)
            
        return None
    
    def organize_cols(
            self,
            performed_cs_correction=False,
            resonance_type='Backbone'
            ):
        """
        Orders columns in DataFrames for better visualization.
        
        Parameters:
            performed_cs_correction (bool): whether .correct_shift_*()
                was previously executed.
        
        resonance_type (str): {'Backbone','Sidechains'}.
        """
        
        if resonance_type == 'Backbone':
            target = self.allpeaklists
        
        elif resonance_type == 'Sidechains':
            target = self.allsidechains
        
        else:
            msg = \
"<resonance_type> argument must be 'Backbone' or 'Sidechains'."
            self.logs(msg)
            return
        
        if performed_cs_correction and resonance_type=='Backbone':
            col_order = [
                'ResNo',
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
                'Pos F2 correction'
                ]
                #                         'index',
        elif performed_cs_correction and resonance_type=='Sidechains':
            col_order = [
                'ResNo',
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
                'Pos F2 correction'
                ]
        
        elif not(performed_cs_correction) and resonance_type=='Backbone':
            col_order = [
                'ResNo',
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
                'index'
                ]
        
        elif not(performed_cs_correction) and resonance_type=='Sidechains':
            col_order = [
                'ResNo',
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
                'index'
                ]
        
        title = "ORGANIZING PEAKLIST COLUMNS' ORDER for {}".\
            format(resonance_type)
        self.logs(title, istitle=True)
        
        for z, y, x in it.product(self.zzcoords, self.yycoords, self.xxcoords):
            # arranges cols
            target[z][y][x] = target[z][y][x][col_order]
            #logs
            self.logs(
                '**[{}][{}][{}]** Columns organized :: OK'.format(z,y,x)
                )
        
        return None
    
    def init_Farseer_cube(self, use_sidechains=False):
        """
        Initiates the 5D Farseer-NMR Cube.
        
        Uses self.p5d to create a 5D matrix with the information of all
        the peaklists in the experimental dataset. The Cube will be
        accessed and used later to create the FarseerSeries objects,
        upon each the Farseer Analysis routines will be performed.
        
        If there are sidechains, creates a Panel5D for the sidechains,
        which are treated separately from the backbone residues.
        
        Generates:
            - self.peaklists_p5d
            - self.sidechains_p5d
        """
        
        self.logs('INITIATING FARSEER CUBE', istitle=True)
        ## .copy() is used to solve issue_86
        self.peaklists_p5d = self.p5d(self.allpeaklists.copy())
        self.logs('> Created cube for all the backbone peaklists - OK!')
        
        if use_sidechains:
            self.sidechains_p5d = self.p5d(self.allsidechains.copy())
            self.logs('> Created cube for all the sidechains peaklists - OK!')
        
        return None
    
    def export_series_dict_over_axis(
            self, series_class,
            along_axis='x',
            resonance_type='Backbone',
            series_kwargs={}
            ):
        """
        Creates a nested dictionary containing all the experimental
        series along a given Farseer-NMR Cube axis.
        
        Nested dictionary contains <series_class> instances from
        FarseerSeries, representing each series.
        
        Example:
        
            If along_axis='x', the nested dictionary will contain first
            level keys zzcoods and second level keys yycoords,
            and values FarseerSeries.
        
        Parameters:
            series_class (class): Farseer Series class.
            
            along_axis (str): {'x', 'y', 'z'} the axis along which
                series will be generated.
            
            series_kwargs (dict): kwargs to be passed to the 
                series_class.__init__.
        
            resonance_type (str): {'Backbone', 'Sidechains'}
        
        Returns:
            The nested dictionary of Farseer Series objects.
        """
        
        if resonance_type == 'Backbone':
            fscube = self.peaklists_p5d
        
        elif resonance_type == 'Sidechains':
            fscube = self.sidechains_p5d
        
        else:
            raise ValueError('Not a valid <resonance_type> option.')
        
        # transposes the Farseer-NMR cube according to the desired axis
        if along_axis=='x':
            series_type='along_x'
            owndim_pts=self.xxcoords
            next_axis = self.yycoords
            next_axis_2 = self.zzcoords
        
        elif along_axis=='y':
            self._compare_fastas()
            series_type='along_y'
            fscube = fscube.transpose(2,0,1,3,4, copy=True)
            owndim_pts=self.yycoords
            next_axis = self.zzcoords
            next_axis_2 = self.xxcoords
        
        elif along_axis=='z':
            series_type='along_z'
            fscube = fscube.transpose(1,2,0,3,4, copy=True)
            owndim_pts=self.zzcoords
            next_axis = self.xxcoords
            next_axis_2 = self.yycoords
        
        else:
            raise ValueError('Not a valid <along_axis> option.')
        
        self.logs(
            'GENERATING DICTIONARY OF SERIES FOR {}'.format(series_type), 
            istitle=True
            )
        # builds kwargs
        series_kwargs['series_axis'] = series_type
        series_kwargs['series_dps'] = owndim_pts
        # prepares dictionary
        series_dct = {}
        # assembles dictionary       
        for dp2, dp1 in it.product(next_axis_2, next_axis):
            series_dct.setdefault(dp2, {})
            # builds kwargs
            series_kwargs['prev_dim'] = dp2
            series_kwargs['next_dim'] = dp1
            # initiates series
            ## intermediate step to remove rows with NaN in ResNo column
            ## this is necessary to solve issue_86 where NaN rows
            ## are added if no fasta file is used to complete the residue
            ## list and when different constrcuts are used along y
            ## which may lead to different number of rows when generating
            ## the 5D panel - creating NaN rows that later conflict with
            ## parameter calculation.
            dfdict = {}
            
            for item in fscube.loc[dp2, dp1, :, :, :].items:
                df = fscube.loc[dp2, dp1, item, :, :]
                df.dropna(axis=0, how='any', subset=['ResNo'], inplace=True)
                dfdict[item] = df
            
            self._compare_peaklists_length(dp1, dp2, series_type, dfdict)
            
            series_panel_NaN_filtered = pd.Panel.from_dict(dfdict)
            series_dct[dp2][dp1] = \
                self.gen_series(
                    series_panel_NaN_filtered,
                    series_class,
                    series_kwargs
                    )
            # writes to log
            self.logs(
                '**Experimental Series [{}][{}] ** with data points {}'.\
                    format(dp2, dp1, list(series_dct[dp2][dp1].items))
                )
        
        return series_dct
    
    def gen_series(self, series_panel, series_class, sc_kwargs):
        """
        Creates a Series object of class <series_class>.
        
        Argument initiation has to be synchronized with the class needs.
        
        Parameters:
            series_panel (pd.Panel): contains the series to be converted
                to series_class instance.
            
            series_class (class): Farseer Series class.
            
            series_kwargs (dict): kwargs to be passed to the 
                series_class.__init__.
        
        Returns:
            The series_class object.
        """
        
        series_panel = \
            series_class(
                np.array(series_panel),
                items=series_panel.items,
                minor_axis=series_panel.minor_axis,
                major_axis=series_panel.major_axis
                )
        # activates the series attibutes
        series_panel.create_attributes(**sc_kwargs)
        
        return series_panel
    
    def exports_parsed_pkls(self):
        """Exports the parsed peaklists of the whole dataset."""
        
        title = 'EXPORTS PARSED PEAKLISTS FROM FARSEER-NMR CUBE'
        self.logs(title, istitle=True)
        
        for z, y, x in it.product(self.zzcoords, self.yycoords, self.xxcoords):
            folder = os.path.join('spectra_parsed', z, y)
            
            if not(os.path.exists(folder)):
                os.makedirs(folder)
            
            fpath = os.path.join(folder, x + '.csv')
            fileout = open(fpath, 'w')
            fileout.write(
                self.allpeaklists[z][y][x].to_csv(
                    sep=',',
                    index=False,
                    na_rep='NaN',
                    float_format='%.4f')
                )
            fileout.close()
            msg = "**Saved:** {}".format(fpath)
            self.logs(msg)
        
            if self.has_sidechains:
                folder = os.path.join('spectra_SD_parsed', z, y)
                
                if not(os.path.exists(folder)):
                    os.makedirs(folder)
                
                fpath = os.path.join(folder, x + '.csv')
                fileout = open(fpath, 'w')
                fileout.write(
                    self.allsidechains[z][y][x].to_csv(
                        sep=',',
                        index=False,
                        na_rep='NaN',
                        float_format='%.4f')
                    )
                fileout.close()
                msg = "**Saved:** {}".format(fpath)
                self.logs(msg)
        
        return None
    
    def load_experiments(self, filetype='.csv', resonance_type='Backbone'):
        """
        Loads the <filetype> files in self.paths into nested
        dictionaries as pd.DataFrames.
        
        Datapoint names should be singular for each dimension.
        
        Parameters:
            filetype (str): {'.csv', '.fasta'}
            
            resonance_type (str): {'Backbone', 'Sidechains'}.
                'Sidechains' only available for '.csv' <filetype>.
        
        If filetype='.csv' and resonance_type='Backbone' executes
        self.init_coords_names()
        
        Example of a mandatory hierarchy folder:
        
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
        # writes title to log
        title = \
            'READING INPUT FILES ({}) for {}'.format(filetype, resonance_type)
        self.logs(title, istitle=True)
        self._checks_filetype(filetype)
        main_peaklists=False
        
        # defines functions to use and target storage dictionaries
        if filetype == '.csv' and resonance_type == 'Backbone':
            f = pd.read_csv
            target = self.allpeaklists
            main_peaklists=True
            
        elif filetype == '.fasta' and resonance_type == 'Backbone':
            #if not(any([self.hasxx, self.hasyy, self.haszz])):
                #msg = 'Do not attempt to load the .fasta files prior to the peaklist .csv files, please :-)'
                #self.logs(fsw.gen_wet('ERROR', msg, 21))
                #self._abort()
            target = self.allfasta
            
        elif filetype == '.csv' and resonance_type == 'Sidechains':
            f = str  # dummy function
            target = self.allsidechains
            
        else:
            self.logs(
'Arguments passed for <filetype> and/or <resonance_type> do not match \
the possible options.'
                )
            return None
        
        # loads files in nested dictionaries
        # piece of code found in stackoverflow, reference missing
        
        for p in self.paths:
            #https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
            
            x_file = os.path.split(p)[1]
            y_dir = os.path.split(os.path.split(p)[0])[1]
            z_dir = os.path.split(os.path.split(os.path.split(p)[0])[0])[1]
            
            #self.logger.debug("dirname: {}".format(os.path.dirname(p)))
            self.logger.debug("p: {}".format(p))
            #self.logger.debug("dirs: {}".format(dirs))
            self.logger.debug("x file:{}".format(x_file))
            self.logger.debug("y folder: {}".format(y_dir))
            self.logger.debug("z folder: {}".format(z_dir))
            
            parts = [z_dir, y_dir]
            self.logger.debug("parts: {}".format(parts))
            
            branch = target
            
            if not x_file.endswith(filetype):
                continue
            
            for part in parts:
                
                branch = branch.setdefault(part, {})
            
            # reads the .csv file to a pd.DataFrame removes
            # the '.csv' from the key name to increase asthetics in output
            if x_file.lower().endswith(filetype):
                self.logs('* {}'.format(p))
                lessparts = x_file.split('.')[0]
                
                try:
                    if filetype == '.csv':
                        branch[lessparts] = branch.get(x_file, f(p))
                    elif filetype == '.fasta':
                        fh = FastaHandler(
                                fasta_file_path=p,
                                fasta_start_num=self.FASTAstart
                                )
                        fh.reads_fasta_to_dataframe(reads_from_file=True)
                        branch[lessparts] = branch.get(x_file, fh.fasta_df)
                
                except pd.errors.EmptyDataError:
                    msg = \
"The file {} is empty. To introduce an empty data point, add the header.".\
                        format(filetype)
                    self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=14))
        
        self._checks_xy_datapoints_coherency(target, filetype)
        
        if main_peaklists:
            self._init_coords_names()
            self._transfer_coords_names()
        
        return None
