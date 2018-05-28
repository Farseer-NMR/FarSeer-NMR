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
