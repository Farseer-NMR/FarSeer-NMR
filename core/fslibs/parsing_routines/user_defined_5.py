"""
Copyright © 2017-2018 Farseer-NMR
Teixeira, J.M.C., Skinner, S.P., Arbesú, M. et al. J Biomol NMR (2018).
https://doi.org/10.1007/s10858-018-0182-5

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

def parse_user_peaklist_5(peaklist_file):
    """
    Parses CCPNMRv2 peaklists into the peakList class format.
    Requires only Position F1, Position F2, Assign F1 and Assign F2 columns.
    
    Parameters:
        - peaklist_file: path to peaklist file.
    
    Returns peakList object
    """
    fin = pd.read_csv(peaklist_file)
    peakList = []
    
    for row in fin.index:
        atoms = []
        if fin.loc[row,'Assign F1'][-4:-1] in aal1tol3.values():
            atoms.append(fin.loc[row,'Assign F1'][-1])
        
        if fin.loc[row,'Assign F2'][-4:-1] in aal1tol3.values():
            atoms.append(fin.loc[row,'Assign F2'][-1])
        
        try:
            lw1 = fin.loc[row,'Line Width F1 (Hz)']
        except KeyError:
            lw1 = None
        
        try:
            lw2 = fin.loc[row,'Line Width F2 (Hz)']
        except KeyError:
            lw2 = None
            
        try:
            vol = fin.loc[row,'Volume']
        except KeyError:
            vol = None
        
        try:
            hgt = fin.loc[row,'Height']
        except KeyError:
            hgt = None
        
        try:
            fit = fin.loc[row,'Fit. Method']
        except KeyError:
            fit = None
        
        try:
            merit = fin.loc[row,'Merit']
        except KeyError:
            merit = None
        
        try:
            volmet = fin.loc[row,'Vol. Method']
        except KeyError:
            volmet = None
        
        try:
            details = fin.loc[row,'Details']
        except KeyError:
            details = "None"
        
        peak = Peak(
            peak_number=fin.loc[row,'Number'],
            positions=[
                fin.loc[row,'Position F1'],
                fin.loc[row,'Position F2']
                ],
            atoms=atoms,
            residue_number=str(fin.loc[row,'Assign F1'])[:-4],
            residue_type=str(fin.loc[row,'Assign F1'])[-4:-1],
            linewidths=[lw1,lw2],
            volume=vol,
            height=hgt,
            fit_method=fit,
            merit=merit,
            volume_method=volmet,
            details=details,
            format_='user_pkl_5'
            )
        peakList.append(peak)
    
    return peakList
