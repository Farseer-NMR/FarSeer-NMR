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
import pandas as pd
import os

from core.fslibs.WetHandler import WetHandler as fsw
import core.fslibs.Logger as Logger
from core.utils import aal1tol3, aal3tol1

class FastaHandler:
    """
    Handles FASTA files.
    """
    def __init__(self, fasta_file_path, fasta_start_num):
        
        # activates logging
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug('FastaHandler initiated')
        
        # FASTA file path
        if os.path.exists(fasta_file_path):
            self.fasta_path = fasta_file_path
            self.logger.debug("FASTA file path OK: {}".format(self.fasta_path))
        else:
            msg = "The path provided for the FASTA file does not exist.\
None assigned"
            wet37 = fsw(msg_title='ERROR', msg=msg, wet_num=37)
            self.logger.info(wet37.wet)
            self.fasta_path = None
            
        self.fasta_start_num = fasta_start_num
        self.logger.debug('FASTA start number: {}'.format(self.fasta_start_num))
        
        self.fasta_string = None
        self.fasta_df = None
        
    def _check_wrong_aminoacid_codes(self, fasta_string, fasta_path=''):
        """
        Checks the presence of wrong a.a. codes in the FASTA string.
        
        If found user is prompt if to abort or parse them out.
        
        Parameters:
            - fasta_string (str): the fasta string
            - fasta_path (opt, str): path to fasta file, serves log purposes
        
        Returns:
            FASTA without digits (user choice)
        """
        self.logger.debug('Entered check wrong a.a.')
        
        if ''.join(c for c in fasta_string if c not in aal1tol3.keys()):
            msg = \
'We found wrong aminoacids codes in your FASTA string coming from file {}. \
Be aware of \
mistakes resulting from wrong FASTA file. You may wish to abort \
and correct the file. \
If you choose continue, Farseer-NMR will parse out the wrong codes.'.\
                format(self.fasta_path)
            
            wet22 = fsw(msg_title='WARNING', msg=msg, wet_num=22)
            self.logger.info(wet22.wet)
            wet22.continue_abort()
            fasta_string_no_wrong_codes = \
                ''.join(c for c in fasta_string if c in aal1tol3.keys())
            
            self.logger.debug('Wrong aa codes parsed out')
            return fasta_string_no_wrong_codes
        
        else:
            self.logger.debug('no digits found')
            return fasta_string
        
    
    def _check_presence_of_digits(self, fasta_string, fasta_path=''):
        """
        Checks the presence of digits in the FASTA string.
        
        If found user is prompt if to abort or parse them out.
        
        Parameters:
            - fasta_string (str): the fasta string
            - fasta_path (opt, str): path to fasta file, serves log purposes
        
        Returns:
            FASTA without digits (user choice)
        """
        self.logger.debug('Entered check digits')
        
        if ''.join(c for c in fasta_string if c.isdigit()):
            msg = \
'We found digits in your FASTA string coming from file {}. Be aware of \
mistakes resulting from wrong FASTA file. You may wish to abort \
and correct the file. \
If you choose continue, Farseer-NMR will parse out the digits.'.\
                format(self.fasta_path)
            
            wet22 = fsw(msg_title='WARNING', msg=msg, wet_num=22)
            self.logger.info(wet22.wet)
            wet22.continue_abort()
            fasta_string_no_digit = \
                ''.join(c for c in fasta_string if not c.isdigit())
            
            self.logger.debug('Digits parsed out')
            return fasta_string_no_digit
        
        else:
            self.logger.debug('no digits found')
            return fasta_string
    
    def reads_fasta_from_file(self, fasta_path=''):
        """
        Reads FASTA string from FASTA file. Assigns self.fasta_string attribute.
        
        Parameters:
            - fasta_path (opt, str): the path to the fasta file
            
        Returns:
            - None
        """
        self.logger.debug('fasta_path parameter set to {}'.format(fasta_path))
        fasta_path = fasta_path or self.fasta_path
        self.logger.debug('Reading FASTA from file {}'.format(fasta_path))
        
        # Opens the FASTA file, which is a string of capital letters
        # 1-letter residue code that can be split in several lines.
        fasta_file = open(fasta_path, 'r')
        fl = fasta_file.readlines()  # list of lines in fasta_file
        
        # Generates a single string from the FASTA file
        fasta_string = ''
        
        for i in fl:
            if i.startswith('>'):
                continue
            
            else:
                fasta_string += i.replace(' ', '').replace('\n', '').upper()
        
        # performs checks on the fasta string
        fasta_string = \
            self._check_presence_of_digits(fasta_string, fasta_path=fasta_path)
        fasta_string = \
            self._check_wrong_aminoacid_codes(fasta_string, fasta_path=fasta_path)
        
        fasta_file.close()
        
        self.fasta_string = fasta_string
        
        return None
    
    def reads_fasta_to_dataframe(
            self,
            fasta_string='',
            atom1='H',
            atom2='N',
            details='None',
            reads_from_file=False,
            fasta_path=''
            ):
        """
        Reads a FASTA string or a FASTA file to a structured pd.DataFrame.
        
        Parameters:
            - fasta_string (opt, str): the FASTA string, if not provided,
                reads from self.fasta_string
            - atom1 (opt, str): the atom type for assign F1 column (def: 'H').
            - atom2 (opt, str): the atom type for assign F2 column (def: 'N').
            - details (opt,str): fill Details column (def: 'None').
            - reads_from_file (opt, bool): if should read from file instead
                of from <fasta_string>.
            - fasta_path (opt, str): path to fasta file, must be given if
                reads_from_file True.
        
        Reads the FASTA string and generates a 5 column DataFrame
        with the information ready to be incorporated in the peaklists
        dataframes of FarseerSeries object.
        
        Assigns self.fasta_df
        """
        
        # assignes and validades arguments ###
        fasta_path = fasta_path or self.fasta_path
        
        if reads_from_file and fasta_string:
            
            msg = "A FASTA string was passed to the fasta_string parameter and \
reads_from_file is True. This is inconsistent because if a FASTA string was \
given there is no need to read from a file. <reads_from_file> will not be \
considered and the FASTA string will be used."
            wet = fsw(msg_title='NOTE', msg=msg, wet_num=37)
            self.logger.info(wet.wet)
        
        elif reads_from_file and not fasta_string:
            
            self.reads_fasta_from_file(fasta_path)
            fasta_string = self.fasta_string
        
        elif not fasta_string and not reads_from_file and self.fasta_string:
            
            fasta_string = self.fasta_string
        
        else:
            msg = "It was not possible to assign a FASTA string. Either it \
was not passed as argument (<fasta_string>) or is not defined as an attribute. \
Please ensure a <fasta_string> is passed or .reads_fasta_from_file() method \
is executed previously."
            wet = fsw(msg_title="WARNING", msg=msg, wet_num=37)
            self.logger.warning(wet.wet)
            return None
        
        self.logger.debug(fasta_string)
        
        # arguments assigned and validated ###
        
        # Generates FASTA reference dataframe
        dd = {}
        # ResNo is kept as str() to allow reindexing
        # later on the finds_missing function.
        dd["ResNo"] = \
            [str(i) for i in range(
                self.fasta_start_num,
                (self.fasta_start_num + len(fasta_string))
                )
            ]
        dd["1-letter"] = list(fasta_string)
        dd["3-letter"] = [aal1tol3[i] for i in fasta_string]
        # Assign F1 is generated here because it will serve in future functions.
        dd["Assign F1"] = \
            [str(i+j+atom1) for i, j in zip(dd["ResNo"], dd["3-letter"])]
        dd["Assign F2"] = \
            [str(i+j+atom2) for i, j in zip(dd["ResNo"], dd["3-letter"])]
        # Details set to 'None' as it is by default in CCPNMRv2 peaklists
        dd['Details'] = [details for i in fasta_string]
        self.fasta_df = pd.DataFrame(
            dd,
            columns=[
                'ResNo',
                '3-letter',
                '1-letter',
                'Assign F1',
                'Assign F2',
                'Details'
                ]
            )
        logs = '  * {}-{}-{}'.format(
            self.fasta_start_num,
            fasta_string,
            dd['ResNo'][-1])
        self.logger.info(logs)
        
        return None

if __name__ == "__main__":
    
    # the following FASTA examples are the same fasta sequence in
    # different file formats or with wrong characters in between.
    fasta_clean = 'ASDFGHKLMMMQPPCVASDFGHKLMMMQPPCVASDFGHKLMMMQPPCV'
    fasta_complex = \
"""
> multiline FASTA header
ASDFGHKLMM
MQPPCVASDFGHKLMM
MQPPCV
ASDFGHKLMM
MQPPCV
"""

    fasta_with_numbers = \
"""
> multiline FASTA with numbers header
ASDFGHKLMM
MQPP3CVASDFG4HKLMM
MQPPCV
ASD1FGHKLMM
MQPPCV5
"""
    fasta_wrong_codes = \
"""
> multiline FASTA header
JASDFGHKLMM
MQPPOCVASDFGHKLMM
MQPPCXXV
ASDFGHZKLMM
MQPPCV
"""
    
    list_of_fastas = [
        fasta_clean,
        fasta_complex,
        fasta_with_numbers,
        fasta_wrong_codes
        ]
    
    fasta_file_list = [
        'fasta_clean.fasta',
        'fasta_complex.fasta',
        'fasta_with_numbers.fasta',
        'fasta_wrong_codes.fasta'
        ]
    
    # sets data frame for comparison
    dd = {}
    dd["ResNo"] = [str(i) for i in range(1, (1 + len(fasta_clean)))]
    dd["1-letter"] = list(fasta_clean)
    dd["3-letter"] = [aal1tol3[i] for i in fasta_clean]
    dd["Assign F1"] = [str(i+j+'H') for i, j in zip(dd["ResNo"], dd["3-letter"])]
    dd["Assign F2"] = [str(i+j+'N') for i, j in zip(dd["ResNo"], dd["3-letter"])]
    dd['Details'] = ['None' for i in fasta_clean]
    fasta_df = pd.DataFrame(
        dd,
        columns=[
            'ResNo',
            '3-letter',
            '1-letter',
            'Assign F1',
            'Assign F2',
            'Details'
            ]
        )
    
    
    for f_str, f_file in zip(list_of_fastas, fasta_file_list):
        f = open(f_file, 'w')
        f.write(f_str)
        f.close()
        
        fh = FastaHandler(f_file, 1)
        
        fh.reads_fasta_from_file()
        print("{} correct FASTA: {}".format(f_file, fasta_clean == fh.fasta_string))
        
        fh.reads_fasta_to_dataframe(reads_from_file=True)
        print("{} correct: {}".format(f_file, fh.fasta_df.equals(fasta_df)))
        
        fh.reads_fasta_to_dataframe()
        print("{} correct: {}".format(f_file, fh.fasta_df.equals(fasta_df)))
        
        if os.path.exists(f_file):
            os.remove(f_file)
            print("... removed {}".format(f_file))
    
