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
from core.fslibs.Peak import Peak

def parse_user1_peaklist(peaklist_file):
    """
    Parses a user defined CARA-derived peaklist.
    
    File extention: *.prot
    Peaklist format:
    
        1  10.494 0.000 H     238
        2 130.175 0.000 N     238
        4   9.965 0.000 H     216
        5 125.165 0.000 N     216
    
    In the current version, only H and N atoms are considered.
    
    Returns:
        a list fo Peak objects.
    """
    
    fin = open(peaklist_file, 'r')
    peakList = []
    
    current_residue = None
    count_residue = 0
    
    for line in fin:
        
        if not line.strip():
            continue
        
        ls = line.strip().split()
        
        if ls[3] not in ('N', 'H'):
            continue
        
        if ls[-1] != current_residue:
            current_residue = ls[-1]
            position = [ls[1]]
            atom = [ls[3]]
            count_residue += 1
        
        elif ls[-1] == current_residue:
            position.append(ls[1])
            atom.append(ls[3])
            
            peak = Peak(
                peak_number=count_residue,
                positions=position,
                residue_number=current_residue,
                residue_type=None,
                atoms=atom,
                linewidths=[0, 0],
                volume=0,
                height=0,
                format_='user_def_1'
                )
            
            peakList.append(peak)
    
    fin.close()
    
    return peakList 
