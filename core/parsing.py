"""
Copyright © 2017-2018 Farseer-NMR
Simon P. Skinner and João M.C. Teixeira

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
import re
import csv
import pandas as pd

from core.utils import aal1tol3, eval_str_to_float
from core.fslibs import wet as fsw
import core.fslibs.parsing_routines as fspr

file_extensions = [
    'peaks',
    'xpk',
    'out',
    'csv',
    'prot',
    'str'
    ]
    
eval_elements_usr_pkl_1 = [
    str.isdigit,
    eval_str_to_float,
    eval_str_to_float,
    str.isalpha,
    str.isdigit
    ]

ccpnmr_headers = set([
    '#',
    'Position F1',
    'Position F2',
    'Assign F1',
    'Assign F2',
    'Height',
    'Volume',
    'Line Width F1 (Hz)',
    'Line Width F2 (Hz)',
    'Merit',
    'Details',
    'Fit Method',
    'Vol. Method',
    'Number'
        ])

user3_headers = set([
    'Peak',
    'Region',
    'Type',
    'Index (F2)',
    'Index (F1)',
    '?(F2) [ppm]',
    '?(F1) [ppm]',
    '?(F2) [Hz]',
    '?(F1) [Hz]',
    'Intensity [abs]',
    'Annotation'
    ])

def get_peaklist_format(file_path):
    fin = open(file_path, 'r')

    if len(file_path.split('.')) < 2:
        print('Invalid File Extension')
        return

    file_ext = file_path.split('.')[-1]
    if file_ext not in file_extensions:
        msg = \
"""*** The following file was not recognised as a valid peaklist
*** {}
*** suffix not in accepted formats. Accepted formats are:
*** *.peaks *.xpk *.out and *.csv (CCPNMR2)
*** visit folder Documentation/Accepted_Peaklists_Formats for more information.
*** If this file is not a peaklists, simply IGNORE this message.
""".\
            format(file_path)
        print(msg)
        #print('Invalid File Extension. Suffix not in accepted format.')
        return "Not accepted suffix"
    
    for line in fin:
        
        ls = line.strip().split()
        
        if not line.strip():
            continue
        
        elif (line.lstrip().startswith("Assignment") and "w1" in line) or \
                line.startswith("<sparky save file>"):
            fin.close()
            return "SPARKY"
        
        elif line.lstrip().startswith("ANSIG") and "crosspeak" in line:
            fin.close()
            return "ANSIG"
        
        elif line.startswith("DATA") and "X_AXIS" in line:
            fin.close()
            return "NMRDRAW"
        
        elif line.split()[0].isdigit() and line.split()[1].startswith('{'):
            fin.close()
            return "NMRVIEW"
        
        # because columns in ccpnmr peaklists may be swapped
        elif set(line.strip().split(',')) == ccpnmr_headers:
            fin.close()
            return "CCPNMRV2"
        
        elif line.strip().split()[0].isdigit() \
                and line.strip().split()[-1].isdigit() \
                and file_path.endswith('.prot') \
                and len(ls) == 5 \
                and all([f(e) for e, f in zip(ls, eval_elements_usr_pkl_1)]):
                
            fin.close()
            return "USER_PKL_1"
        
        elif (line.strip() == 'loop_' \
                    or line.strip() == '_Atom_shift_assign_ID') \
                and file_path.endswith('.str'):
            
            fin.close()
            return "USER_PKL_2"
        
        
        elif set(line.strip().rstrip(',').split(',')) == user3_headers \
                and file_ext == 'csv':
            
            fin.close()
            return "USER_PKL_3"
        
        
        # INSERT YOUR VALIDATION CODE HERE
        # SO THAT YOU PEAKLIST FORMAT IS RECOGNIZED
        #elif ****:
            #fin.close()
            #return "YOUR_FORMAT"
        
        else:
            print('here')
            continue

    else:
        msg = \
"""We could not read peaklist file: {}.
Mostly likely due to a bad peaklist formatting syntax.
""".\
            format(file_path)
        print(fsw.gen_wet("ERROR", msg, 30))
        return "Bad peaklist format"

def read_peaklist(peaklist_file):
    """
    Reads peaklist file to Farseer-NMR format.
    
    Parameters:
        -peaklist_file (str): path to original file
    
    Returns:
        - list (core.Peak): list of Peak objects or None if peaklist_file
            cannot be parsed.
    """
    
    def give_none(x): return None
    
    file_format = get_peaklist_format(peaklist_file)
    
    dict_of_parsing_functs = {
        'ANSIG':fspr.ansig,
        'NMRDRAW':fspr.nmrdraw,
        'NMRVIEW':fspr.nmrview,
        'SPARKY':fspr.sparky,
        'CCPNMRV2':fspr.ccpnmrv2,
        'USER_PKL_1':fspr.user_pkl_1,
        'USER_PKL_2':fspr.user_pkl_2,
        'USER_PKL_3':fspr.user_pkl_3,
        'Bad peaklist format': give_none,
        'Not accepted suffix': give_none
        }
    
    return dict_of_parsing_functs[file_format](peaklist_file)
    
    # if file_format == 'ANSIG':
        # return fspr.ansig(peaklist_file)

    # elif file_format == 'NMRDRAW':
        # return fspr.nmrdraw(peaklist_file)

    # elif file_format == 'NMRVIEW':
        # return fspr.nmrview(peaklist_file)

    # elif file_format == 'SPARKY':
        # return fspr.sparky(peaklist_file)

    # elif file_format == 'CCPNMRV2':
        # return fspr.ccpnmrv2(peaklist_file)
    
    # elif file_format == 'USER_PKL_1':
        # return fspr.user_pkl_1(peaklist_file)
    
    # elif file_format == 'USER_PKL_2':
        # return fspr.user_pkl_2(peaklist_file)
    
    # elif file_format == 'USER_PKL_3':
        # return fspr.user_pkl_3(peaklist_file)
    
    # #elif file_format == "YOUR_FORMAT":
        # #return fspr.your_function(peaklist_file)
    
    # elif file_format == "Bad peaklist format":
        # return None
