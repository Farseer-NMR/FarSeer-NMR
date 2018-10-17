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

def parse_user_peaklist_2(peaklist_file):
    """
    Parses a CARA peaklist.
    
    File extention: *.str
    Peaklist format:
    
           loop_
      _Atom_shift_assign_ID
      _Residue_seq_code
      _Residue_label
      _Atom_name
      _Atom_type
      _Chem_shift_value
      _Chem_shift_value_error
      _Chem_shift_ambiguity_code
         1  181   CYS  C     C 174.365 0.3     1  
         2  181   CYS  CA    C  57.746 0.3     1  
         3  181   CYS  CB    C  43.369 0.3     1  
         4  181   CYS  H     H   9.977 0.020   1 
    
    In the current version, only H and N atoms are considered.
    
    Returns:
        a list fo Peak objects.
    """
    fin = open(peaklist_file, 'r')
    peakList = []
    
    current_residue = None
    residue_counter = 0
    
    for line in fin:
        if not line.strip() \
                or line.strip().startswith('_') \
                or line.strip().endswith('_'):
            continue
        
        ls = line.strip().split()
        
        if ls[3] not in ('N', 'H'):
            continue
        
        if ls[1] != current_residue:
            current_residue = ls[1]
            positions = [ls[5]]
            atom = [ls[3]]
            residue_counter += 1
        
        elif ls[1] == current_residue:
            positions.append(ls[5])
            atom.append(ls[3])
            
            peak = Peak(
                peak_number=residue_counter,
                positions=positions,
                residue_type=ls[2].title(),
                residue_number=ls[1],
                atoms=atom,
                linewidths=[0, 0],
                volume=0,
                height=0,
                details="None",
                format_='user_pkl_2'
                )
            
            peakList.append(peak)
    
    fin.close()
    return peakList
