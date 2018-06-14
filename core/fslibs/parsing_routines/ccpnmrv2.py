"""
Copyright © 2017-2018 Farseer-NMR
Teixeira, J.M.C., Skinner, S.P., Arbesú, M. et al. J Biomol NMR (2018).
https://doi.org/10.1007/s10858-018-0182-5

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
from core.utils import aal1tol3
from core.fslibs.Peak import Peak
from core.fslibs import wet as fsw

def parse_ccpnmrv2_peaklist(peaklist_file):
    """
    Parses CCPNMRv2 peaklists into the peakList class format.
    
    Parameters:
        - peaklist_file: path to peaklist file.
    
    Returns peakList object
    """
    fin = pd.read_csv(peaklist_file)
    peakList = []
    checks_misleading_chars(fin, peaklist_file)
    
    for row in fin.index:
        atoms = []
        if fin.loc[row,'Assign F1'][-4:-1] in aal1tol3.values():
            atoms.append(fin.loc[row,'Assign F1'][-1])
        
        if fin.loc[row,'Assign F2'][-4:-1] in aal1tol3.values():
            atoms.append(fin.loc[row,'Assign F2'][-1])
        
        peak = Peak(
            peak_number=fin.loc[row,'Number'],
            positions=[
                fin.loc[row,'Position F1'],
                fin.loc[row,'Position F2']
                ],
            atoms=atoms,
            residue_number=str(fin.loc[row,'Assign F1'])[:-4],
            residue_type=str(fin.loc[row,'Assign F1'])[-4:-1],
            linewidths=[
                fin.loc[row,'Line Width F1 (Hz)'],
                fin.loc[row,'Line Width F2 (Hz)']
                ],
            volume=fin.loc[row,'Volume'],
            height=fin.loc[row,'Height'],
            fit_method=fin.loc[row,'Fit Method'],
            merit=fin.loc[row,'Merit'],
            volume_method=fin.loc[row,'Vol. Method'],
            details=fin.loc[row,'Details'],
            format_='ccpnmrv2'
            )
        peakList.append(peak)
    
    return peakList
    
    
def checks_misleading_chars(pkl_df, pkl_file_path):
    """
    Checks for the presence misleading characters in the DataFrame.
    This may come from entries of unassigned residues
    that were not removed.
    
    Parameters:
        - pkl_df (pd.DataFrame): contains converted input peaklist
        -pkl_file_path (str): path to original peaklist file
    
    Returns:
        - None
    
    """
    # for assignment cols
    ## empty
    empty_cells_f1 = pkl_df.loc[:,'Assign F1'].isnull()
    empty_cells_f2 = pkl_df.loc[:,'Assign F2'].isnull()
    
    if empty_cells_f1.values.any() or empty_cells_f2.values.any():
        rows_bool = empty_cells_f1 | empty_cells_f2
        msg = "The peaklist {} contains no assignment \
information in lines {}. Please review that peaklist.".format(
            pkl_file_path,
            [2+int(i) for i in rows_bool.index[rows_bool].tolist()]
            )
        print(fsw.gen_wet('ERROR', msg, 29))
        fsw.abort()
    
    ## misleading chars
    non_digit_f1 = \
        pkl_df.loc[:,'Assign F1'].str.strip().str.contains('\W', regex=True)
    
    non_digit_f2 = \
        pkl_df.loc[:,'Assign F2'].str.strip().str.contains('\W', regex=True)
    
    if  non_digit_f1.any() or non_digit_f2.any():
        rows_bool = non_digit_f1 | non_digit_f2
        msg = "The peaklist {} contains misleading \
charaters in Assignment columns in line {}.".format(
            pkl_file_path,
            [2+int(i) for i in rows_bool.index[rows_bool].tolist()]
            )
        print(fsw.gen_wet('ERROR', msg, 29))
        fsw.abort()
    
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
        #if not any(pkl_df.loc[:,col].isnull()):
            #continue
        non_digit = pkl_df.loc[:,col].\
            astype(str).str.strip().str.contains(
                '[\!\"\#\$\%\&\\\'\(\)\*\,\-\/\:\;\<\=\>\?\@\[\]\^\_\`\{\|\}\~]',
                regex=True
                )
        print(non_digit)
        if non_digit.any():
            msg = "The peaklist {} contains misleading \
charaters in line {} of column [{}].".format(
                pkl_file_path,
                [2+int(i) for i in non_digit.index[non_digit].tolist()],
                col
                )
            print(fsw.gen_wet('ERROR', msg, 29))
            fsw.abort()
    
    return
