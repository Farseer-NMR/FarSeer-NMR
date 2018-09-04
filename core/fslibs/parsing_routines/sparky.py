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
import re
from core.fslibs.Peak import Peak

def parse_sparky_peaklist(peaklist_file):
    """
    Parses Sparky peaklists according to format:
    
      Assignment         w1         w2       Height       Volume
     L480HN-L480N      8.772    130.768   1.01E+05   8.27E+05 bx
     A640HN-A640N      8.657    130.164   5.76E+04   4.94E+05 bx
     A739HN-A739N      8.846    129.894   8.12E+04   6.77E+05 bx
     V508HN-V508N      8.650    128.669   1.15E+05   9.24E+05 bx
     K542HN-K542N      7.369    128.421   1.14E+05   9.43E+05 bx
    
    Parameters:
        - peaklist_file (str): path to peaklist
    
    Returns: list of core.fslibs.Peak.Peak objects.
    """
    peakList = []
    with open(peaklist_file) as f:
        lines = f.readlines()[1:]
        f.close()
    
    for ii, line in enumerate(lines):
        line_list = line.strip().split()
    
        if len(line_list) < 4:
            continue
    
        if '?' in line_list[0]:
            continue
    
        assignment = re.sub(
            r"([A-Z])([0-9]+)([A-Z])",
            "\\1 \\2 \\3",
            line_list[0]
            ).split()
        resname = assignment[0]
        resnumber = assignment[1]
        atoms = [assignment[2].split('-')[0], assignment[-1]]
        linewidths = [None] * 2
        ppms = [line_list[1], line_list[2]]
        height = line_list[3]
        volume = line_list[4]
        peak = Peak(
            peak_number=ii+1,
            positions=ppms,
            residue_number=resnumber,
            residue_type=resname,
            atoms=atoms,
            linewidths=linewidths,
            volume=volume,
            height=height,
            format_="sparky"
            )
        peakList.append(peak)
    
    return peakList
