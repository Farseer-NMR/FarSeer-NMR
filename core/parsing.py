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

from core.utils import aal1tol3
from core.fslibs import wet as fsw
import core.fslibs.parsing_routines as fspr

file_extensions = [
    'peaks',
    'xpk',
    'out',
    'csv',
    'str'
    ]

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
        return

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

    for line in fin:
        if not line.strip():
            continue

        elif (line.lstrip().startswith("Assignment") and "w1" in line) or \
                line.startswith("<sparky save file>"):
            fin.close()
            return "SPARKY"

        elif line.lstrip().startswith("ANSIG") and "crosspeak" in line:
            fin.close()
            return "ANSIG"

        elif line.startswith("DATA") and "X_AXIS" in line \
                or line.startswith('REMARK'):
            fin.close()
            return "NMRDRAW"

        elif line.split()[0].isdigit() and line.split()[1].startswith('{'):
            fin.close()
            return "NMRVIEW"

        # because columns in ccpnmr peaklists may be swapped
        elif set(line.strip().split(',')) == ccpnmr_headers:
            fin.close()
            return "CCPNMRV2"

        else:
            msg = \
"""We could not read peaklist file: {}.
Mostly likely due to a bad peaklist formatting syntax.
""".\
                format(file_path)
            print(fsw.gen_wet("ERROR", msg, 30))
            return "Bad peaklist format"


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
                atoms[i] = label.split('.')[1]

            positions[i] = float(position)
            linewidths[i] = float(linewidth)
            labels[i] = label
        if None not in labels:
            peak = Peak(
                peak_number=peak_number,
                positions=positions,
                volume=volume,
                height=height,
                assignments=labels,
                linewidths=linewidths,
                atoms=atoms,
                details=details,
                format="nmrview"
                )
            peakList.append(peak)

    fin.close()

    return peakList



def read_peaklist(fin):

    peaklist_file = fin
    file_format = get_peaklist_format(peaklist_file)

    if file_format == 'ANSIG':
        return fspr.ansig(peaklist_file)

    elif file_format == 'NMRDRAW':
        return fspr.nmrdraw(peaklist_file)

    elif file_format == 'NMRVIEW':
        return parse_nmrview_peaklist(peaklist_file)

    elif file_format == 'SPARKY':
        return fspr.sparky(peaklist_file)

    elif file_format == 'CCPNMRV2':
        return fspr.ccpnmrv2(peaklist_file)

    elif file_format == "Bad peaklist format":
        return None
