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

import logging
import logging.config
import core.fslibs.log_config as fslogconf
from core.fslibs.WetHandler import WetHandler as fsw
from core.utils import aal1tol3, aal3tol1

class FastaHandler:
    """
    Handles FASTA files.
    """
    def __init__(self, fasta_file_path, fasta_start_num):
        
        # activates logging
        self.logger = fslogconf.getLogger(__name__)
        logging.config.dictConfig(fslogconf.farseer_log_config)
        self.logger.debug('FastaHandler initiated')
        
        # FASTA file path
        self.fasta_path = fasta_file_path
        self.fasta_start_num = fasta_start_num
        self.logger.debug('FASTA file path read: OK')
        
    
    def _check_presence_of_digits(self, fasta_string, fasta_path=''):
        """
        Checks the presence of digits in the FASTA string.
        
        If digits are found user is prompt if to abort or parse them out.
        
        Returns:
            FASTA without digits (user choice)
        """
        
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
            
            return fasta_string_no_digit
        
        else:
            return fasta_string
    
    def read_fasta_file(
            self,
            fasta_path='',
            atom1='H',
            atom2='N',
            details='None'
            ):
        """
        Reads a FASTA file to a pd.DataFrame.
        
        Parameters:
            - fasta_path (opt, str): the FASTA file path.
            - atom1 (opt, str): the atom type for assign F1 column (def: 'H')
            - atom2 (opt, str): the atom type for assign F2 column (def: 'N')
            - details (opt,str): fill Details column (def: 'None')
        
        Reads the FASTA file and generates a 5 column DataFrame
        with the information ready to be incorporated in the peaklists
        dataframes.
        
        Returns:
            Returns and assigns self.fasta_df
        """
        fasta_path = fasta_path or self.fasta_path
        
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
        
        fasta_file.close()
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
        
        return self.fasta_df

if __name__ == "__main__":
    import os
    
    
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
    f1 = open('fasta_clean.fasta', 'w')
    f2 = open('fasta_complex.fasta', 'w')
    f3 = open('fasta_with_numbers.fasta', 'w')
    
    f1.write(fasta_clean)
    f2.write(fasta_complex)
    f3.write(fasta_with_numbers)
    
    f1.close()
    f2.close()
    f3.close()
    
    fh1 = FastaHandler('fasta_clean.fasta', 1)
    fh2 = FastaHandler('fasta_complex.fasta', 1)
    fh3 = FastaHandler('fasta_with_numbers.fasta', 1)
    
    fh1.read_fasta_file()
    fh2.read_fasta_file()
    fh3.read_fasta_file()
    
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
    
    print('f1 correct: {}'.format(fh1.fasta_df.equals(fasta_df)))
    print('f2 correct: {}'.format(fh2.fasta_df.equals(fasta_df)))
    print('f3 correct: {}'.format(fh3.fasta_df.equals(fasta_df)))
    
    # removing files
    
    fasta_file_list = [
        'fasta_clean.fasta',
        'fasta_complex.fasta',
        'fasta_with_numbers.fasta'
        ]
    
    for ffile in fasta_file_list:
        if os.path.exists(ffile):
            os.remove(ffile)
            print("... removed {}".format(ffile))
    
