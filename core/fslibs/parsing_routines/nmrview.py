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

def parse_nmrview_peaklist(peaklist_file):
    """Parse a 2D peaklist in NmrDraw format
label dataset sw sf
1H 15N
None
{9578.54 } {1944.77 }
{599.7728 } { 60.7814 }
 1H.L  1H.P  1H.W  1H.B  1H.E  1H.J  1H.U  15N.L  15N.P  15N.W  15N.B  15N.E  15N.J  15N.U  vol  int  stat  comment  flag0
7  {480.HN}   8.772   0.050   0.050   ?   0.000   {?}   {480.N}   130.768   0.050   0.050   ?   0.000   {?}  827229.31250 100862.75000 1 {?} 0
8  {}   0.000   0.000   0.000   ?   0.000   {?}   {}   0.000   0.000   0.000   ?   0.000   {?}  0.00000 0.00000 -1 {?} 0
9  {640.HN}   8.657   0.050   0.050   ?   0.000   {?}   {640.N}   130.164   0.050   0.050   ?   0.000   {?}  493697.26562 57617.50000 1 {?} 0
10  {}   0.000   0.000   0.000   ?   0.000   {?}   {}   0.000   0.000   0.000   ?   0.000   {?}  0.00000 0.00000 -1 {?} 0
11  {739.HN}   8.846   0.050   0.050   ?   0.000   {?}   {739.N}   129.894   0.050   0.050   ?   0.000   {?}  677300.62500 81214.85938 1 {?} 0
12  {}   0.000   0.000   0.000   ?   0.000   {?}   {}   0.000   0.000   0.000   ?   0.000   {?}  0.00000 0.00000 -1 {?} 0

    Parameters:
        - peaklist_file (str): path to peaklist file.

    Returns:
        - peakList (list): list of Peak objects.
    """
    peakList = []
    fin = open(peaklist_file, 'r')
    lines = fin.readlines()
    dimension_names = lines[1].strip().split()
    dimension_count = len(dimension_names)
    headings = lines[5].strip().split()
    dimension_headings = [x.split('.') for x in headings if '.' in x]
    dimension_headings = \
        [x for x in dimension_headings if x[0] in dimension_names]
    field_count = int(len(dimension_headings) / dimension_count)

    for line in lines[6:]:
        fields = line.strip().split()
        volume, height, status, comment = fields[-5:-1]

        if line[1] == '{}' or status == '-1':
            continue

        peak_data = fields[:-5]
        peak_number = int(peak_data[0])
        volume = float(volume)
        height = float(height)
        details = comment[1:-1].strip()
        positions = [None] * dimension_count
        labels = [None] * dimension_count
        linewidths = [None] * dimension_count
        atoms = [None] * dimension_count

        if details == '?':
            details = None

        for i in range(dimension_count):
            field_start = 1 + i*field_count
            field_end = field_start+1*field_count
            dimension_data = peak_data[field_start:field_end]

            label, position, linewidth = dimension_data[:3]

            label = label[1:-1]

            if label == '?':
                label = None
            if label:
                atoms[i] = label.split('.')[1][0]

            positions[i] = float(position)
            linewidths[i] = float(linewidth)
            labels[i] = label

        if None not in labels:
            peak = Peak(
                peak_number=peak_number,
                positions=positions,
                volume=volume,
                height=height,
                residue_number=re.match(r'^\d+', labels[0]).group(0),
                residue_type=None,
                linewidths=linewidths,
                atoms=atoms,
                details=details,
                format_="nmrview"
                )
            peakList.append(peak)
    
    fin.close()
    return peakList
