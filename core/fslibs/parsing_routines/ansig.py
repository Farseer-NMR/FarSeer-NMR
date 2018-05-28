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
import string
from core.fslibs.Peak import Peak

def parse_ansig_peaklist(peaklist_file):
    """Parse a 2D peaklist in ANSIG format
       From ANSIG Manual:
       For 2D crosspeaks files the record has the format:
        FORMAT (3E13.6, A12, 7I6, 6A4)

        The values for each crosspeak are given in the following order:
        E13.6	Coordinates (F1, F2, ...)
        E13.6	Intensity
        A12	Spectrum name
        I6	Symmetry connection
        2I6	F1 connections (prev, next)
        2I6	F2 connections (prev, next)
            ... (further Fdim connections)
        2I6	Corresponding connections
        A4	Sequence assignments; F1, F2, ...
        A4	Residue assignemnts; F1, F2, ...
        A4	Nucleus assignments; F1, F2, ...

ANSIG v3.3 export crosspeaks file
   190     2
 1.307676E+02 8.772405E+00 8.272293E+05Trosy_highCo     0     0     0     0     0     0     023  23  Leu Leu N   HN
 1.301636E+02 8.656933E+00 4.936973E+05Trosy_highCo     0     0     0     0     0     0     0183 183 Ala Ala N   HN
 1.298941E+02 8.845919E+00 6.773006E+05Trosy_highCo     0     0     0     0     0     0     0282 282 Ala Ala N   HN
    """
    peakList = []
    # FarSeer-NMR only supports peaklists so dimension_count must equal 2
    dimension_count = 2
    # Each chemical shift is 13 characters wide and intensity
    
    fin = open(peaklist_file, 'r')
    lines = fin.readlines()
    fin.close()
    
    if lines[1].split()[-1] != '2':
        print("Peak list is not from a 2D spectrum")
        return
    
    counter = 1
    for ii, line in enumerate(lines[2:]):
        ls = line.strip().split()
        
        if len(ls) < 15 \
                or line.strip().startswith('!') \
                or line.strip().startswith('ANSIG'):
            continue
        
        peak_number = counter
        positions = [ls[1], ls[0]]
        
        if ls[-2] == 'N' and ls[-1] == 'HN':
            atoms = ['H', 'N']
        else:
            continue
        
        residue_number = ls[10]
        residue_type = ls[11]
        height = ls[2].rstrip(string.ascii_letters+string.punctuation)
        volume = height
        linewidths = [0, 0]
        peak = Peak(
                peak_number=counter,
                positions=positions,
                volume=volume,
                height=height,
                residue_number=residue_number,
                residue_type=residue_type,
                linewidths=linewidths,
                atoms=atoms,
                format_="ansig"
                )
        peakList.append(peak)
        counter += 1
    
    return peakList
