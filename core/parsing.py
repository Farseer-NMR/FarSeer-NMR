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

from core.utils import aal1tol3
from core.fslibs.Peak import Peak

file_extensions = ['peaks', 'xpk', 'out', 'csv']

def get_peaklist_format(file_path):
    fin = open(file_path, 'r')
    
    if len(file_path.split('.')) < 2:
        print('Invalid File Extension')
        return
    
    if file_path.split('.')[-1] not in file_extensions:
        print('Invalid File Extension. Suffix not in accepted format.')
        return
    
    for line in fin:
        if not line.strip():
            continue
        
        if (line.lstrip().startswith("Assignment") and "w1" in line) or \
                line.startswith("<sparky save file>"):
            fin.close()
            return "SPARKY"
        
        if line.lstrip().startswith("ANSIG") and "crosspeak" in line:
            fin.close()
            return "ANSIG"
        
        if line.startswith("DATA") and "X_AXIS" in line:
            fin.close()
            return "NMRDRAW"
        
        if line.split()[0].isdigit() and line.split()[1].startswith('{'):
            fin.close()
            return "NMRVIEW"
        
        if line.startswith("Number"):
            fin.close()
            return "CCPN"


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
    # always follows chemical shifts
    intensity_column_number = 13*dimension_count
    # assignment field occurs after 13 character intensity
    # field, plus 12 character spectrum name field and seven 6
    # character symmetry and connection fields
    assignment_field_start_index = intensity_column_number+13+12+7*6
    fin = open(peaklist_file, 'r')
    lines = fin.readlines()
    first_two_lines = lines[:2]
    
    if first_two_lines[1][11] != '2':
        print("Peak list is not from a 2D spectrum")
        return
    
    for ii, line in enumerate(lines[2:]):
        
        if line.strip().startswith('!'):
            continue
        
        if line.strip().startswith('ANSIG'):
            continue
        
        height = float(
            line[intensity_column_number:intensity_column_number+13].strip() \
                or '0')
        volume = height
        peak_positions = [0] * dimension_count
        peak_labels = [None] * dimension_count
        line_widths = [None] * dimension_count
        atoms = [None] * dimension_count
        
        for dimension in range(dimension_count):
            
            shifts_field = dimension*13
            sequence_code_field = assignment_field_start_index + (dimension*4)
            residue_name_field = \
                assignment_field_start_index \
                + (dimension_count*4) \
                + (dimension*4)
            atom_name_field = \
                assignment_field_start_index \
                + (dimension_count*8) \
                + (dimension*4)
            peak_positions[dimension] = \
                float(line[shifts_field:shifts_field+13])
            residue_number = line[sequence_code_field:sequence_code_field+4].\
                strip() or '?'
            residue_name = line[residue_name_field:residue_name_field+4].\
                strip() or '?'
            atom = line[atom_name_field:atom_name_field+4].strip() or '?'
            atoms[dimension] = atom[0]
            peak_labels[dimension] = '%s%s%s' % (
                residue_number,
                residue_name, atom[0]
                )
        peak_labels.reverse()
        peak_positions.reverse()
        atoms.reverse()
        line_widths.reverse()
        
        if '???' not in peak_labels:
            peak = Peak(
                peak_number=ii+1,
                positions=peak_positions,
                volume=volume,
                height=height,
                assignments=peak_labels,
                linewidths=line_widths,
                atoms=atoms,
                format="ansig"
                )
            peakList.append(peak)
    fin.close()
    
    return peakList

def parse_nmrdraw_peaklist(peaklist_file):
    """Parse a 2D peaklist in NmrDraw format
REMARK

DATA  X_AXIS 1H           1  2048   12.685ppm   -3.277ppm
DATA  Y_AXIS 15N          1  1024  135.000ppm  103.035ppm

variables   INDEX X_AXIS Y_AXIS DX DY X_PPM Y_PPM X_HZ Y_HZ XW YW XW_HZ YW_HZ X1 X3 Y1 Y3 HEIGHT DHEIGHT VOL PCHI2 TYPE ASS CLUSTID MEMCNT TROUBLE
FORMAT %5d %9.3f %9.3f %6.3f %6.3f %8.3f %8.3f %9.3f %9.3f %7.3f %7.3f %8.3f %8.3f %4d %4d %4d %4d %13e %13e %13e %.5f %d %s %4d %4d %4d

    7   502.767   136.454  2.000  2.000    8.772  130.768  2351.453   259.152   7.349   9.187   34.372   17.448  501  503  135  137  1.008628e+05  0.000000e+00  8.272293e+05 0.00000 1 480.H;480.N    0    0    0
    9   517.575   155.785  2.000  2.000    8.657  130.164  2420.710   295.866   9.572  10.187   44.768   19.346  516  518  154  156  5.761750e+04  0.000000e+00  4.936973e+05 0.00000 1 640.H;640.N    0    0    0
   11   493.340   164.410  2.000  2.000    8.846  129.894  2307.361   312.246   6.402  10.046   29.940   19.080  492  494  163  165  8.121486e+04  0.000000e+00  6.773006e+05 0.00000 1 739.H;739.N    0    0    0
   19   518.456   203.628  2.000  2.000    8.650  128.669  2424.833   386.727   6.995   9.486   32.714   18.015  517  519  202  204  1.150421e+05  0.000000e+00  9.242484e+05 0.00000 1 508.H;508.N    0    0    0
   20   682.727   211.562  2.000  2.000    7.369  128.421  3193.130   401.797   7.168   9.734   33.525   18.487  681  683  210  212  1.136131e+05  0.000000e+00  9.425642e+05 0.00000 1 542.H;542.N    0    0    0
   21   567.806   215.211  2.000  2.000    8.265  128.307  2655.641   408.726   6.202   8.294   29.007   15.752  566  568  214  216  5.714155e+04  0.000000e+00  4.769788e+05 0.00000 1 494.H;494.N    0    0    0
   23   617.869   218.059  2.000  2.000    7.875  128.218  2889.787   414.136   3.580   7.180   16.742   13.637  616  618  217  219  2.160228e+06  0.000000e+00  1.713618e+07 0.00000 1 765.H;765.N    0    0    0
   26   509.184   222.297  2.000  2.000    8.722  128.085  2381.465   422.184   6.314   9.337   29.531   17.733  508  510  221  223  1.404175e+05  0.000000e+00  1.127275e+06 0.00000 1 510.H;510.N    0    0    0
   31   655.592   258.869  2.000  2.000    7.581  126.943  3066.220   491.641   5.359   8.513   25.065   16.167  654  656  257  259  7.345364e+04  0.000000e+00  5.971680e+05 0.00000 1 682.H;682.N    0    0    0

    Line starting VARS or variables contains contents of each column.
    """

    peakList = []
    isotopes = []
    fin = open(peaklist_file, 'r')
    dimension_count = 0

    # create a dictionary to store key:value pairs of
    # column_label: column_index
    field_dictionary = {}

    for line in fin:
        line = line.strip()
        # ignore blank lines and lines starting with REMARK
        
        if not line:
            continue
        
        if line.startswith('REMARK'):
            continue
        
        data = line.split()
        
        if line.startswith('DATA'):
            dimension_count += 1
            continue
        
        if line.startswith('VARS') or line.startswith('variables'):
            # populate field_dictionary with key:value pairs
            # of column_label: column_index
            for i, key in enumerate(data[1:]):
                field_dictionary[key] = i
            continue
        
        # if field dictionary is empty
        elif not field_dictionary:
            continue
        
        # if field doesn't begin with an integer
        elif not line[0].isdigit():
            continue
        
        positions = [0] * dimension_count
        linewidths = [None] * dimension_count
        dimension_labels = (('X_PPM', 'XW'), ('Y_PPM', 'YW'), ('Z_PPM', 'ZW'))
        
        height = float(data[field_dictionary['HEIGHT']])
        volume = float(data[field_dictionary['VOL']])
        annotations = data[field_dictionary['ASS']].split(';')
        atoms = [annotation.split('.')[1] for annotation in annotations
                 if annotation]
        
        for dimension in range(dimension_count):
            ppm_heading, linewidth_heading = dimension_labels[dimension]
            positions[dimension] = float(data[field_dictionary[ppm_heading]])
            linewidths[dimension] = \
                float(data[field_dictionary[linewidth_heading]])
        
        if '' not in annotations:
            peak = Peak(
                peak_number=data[0],
                assignments=annotations,
                atoms=atoms,
                height=height,
                volume=volume,
                positions=positions,
                linewidths=linewidths,
                format="nmrdraw"
                )
            peakList.append(peak)
    
    fin.close()
    
    return peakList


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


def parse_ccpn_peaklist(peaklist_file):
    fin = open(peaklist_file, 'r')
    next(fin)
    peakList = []
    reader = csv.reader(fin)
    
    for row in reader:
        if not(row): continue
        atoms = []
    
        for v in aal1tol3.values():
            if v in row[4]:
                a1 = row[4].strip().split(v)[-1]
                atoms.append(a1)
    
            if v in row[5]:
                a2 = row[5].strip().split(v)[-1]
                atoms.append(a2)
    
        peak = Peak(
            peak_number=row[1],
            positions=[row[2], row[3]],
            assignments=[row[4], row[5]],
            atoms=atoms,
            linewidths=[row[8], row[9]],
            volume=row[7],
            height=row[6],
            fit_method=row[12], merit=row[10],
            volume_method=row[13],
            details=row[11],
            format='ccpn'
            )
        
        peakList.append(peak)
    
    fin.close()
    return peakList


def parse_sparky_peaklist(peaklist_file):
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
        annotations = [resnumber+aal1tol3[resname]+x[0] for x in atoms]
        linewidths = [None] * 2
        ppms = [line_list[1], line_list[2]]
        height = line_list[3]
        volume = line_list[4]
        peak = Peak(
            peak_number=ii+1,
            positions=ppms,
            assignments=annotations,
            atoms=atoms,
            linewidths=linewidths,
            volume=volume,
            height=height,
            format="sparky"
            )
        peakList.append(peak)
    
    return peakList

def read_peaklist(fin):
    
    peaklist_file = fin
    file_format = get_peaklist_format(peaklist_file)
    
    if file_format == 'ANSIG':
        return parse_ansig_peaklist(peaklist_file)
    
    elif file_format == 'NMRDRAW':
        return parse_nmrdraw_peaklist(peaklist_file)
    
    elif file_format == 'NMRVIEW':
        return parse_nmrview_peaklist(peaklist_file)
    
    elif file_format == 'SPARKY':
        return parse_sparky_peaklist(peaklist_file)
    
    elif file_format == 'CCPN':
        return parse_ccpn_peaklist(peaklist_file)
