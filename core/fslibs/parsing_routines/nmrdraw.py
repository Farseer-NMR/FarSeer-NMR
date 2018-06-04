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
import re
from core.fslibs.Peak import Peak

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
    dimension_labels = {
        'X_AXIS':('X_PPM', 'XW'),
        'Y_AXIS':('Y_PPM', 'YW'),
        'Z_AXIS':('Z_PPM', 'ZW')
        }

    fin = open(peaklist_file, 'r')

    # create a dictionary to store key:value pairs of
    # column_label: column_index
    field_dictionary = {}

    # http://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.read_csv.html
    line_counter = 0

    for line in fin:

        line = line.strip()
        # ignore blank lines and lines starting with REMARK

        if not line \
                or line.startswith('REMARK') \
                or line.startswith('FORMAT'):
            line_counter += 1
            continue

        elif line.startswith('DATA'):
            dim = re.search('[a-zA-Z]+', line.split()[2]).group(0)
            print(dim)
            field_dictionary[dim] = line.split()[1]
            line_counter += 1
            continue

        elif line.startswith('VARS') or line.startswith('variables'):
            df_header = line.split()[1:]
            line_counter += 1
            break

        elif line.split()[0].isdigit():
            break

    pkl = pd.read_csv(peaklist_file,
        sep='\s+',
        skiprows=line_counter,
        header=0,
        names=df_header,
        index_col=False
        )

    for row in pkl.index:
        atoms = re.findall('[HN]', str(pkl.loc[row,'ASS']))

        if atoms:
            peak = Peak(
                peak_number=pkl.loc[row,'INDEX'],
                residue_number=re.search('^\d+', str(pkl.loc[row,'ASS'])),
                residue_type=None,
                atoms=atoms,
                height=pkl.loc[row,'HEIGHT'],
                volume=pkl.loc[row,'VOL'],
                positions=[
                    float(pkl.loc[row,dimension_labels[field_dictionary['H']][0]]),
                    float(pkl.loc[row,dimension_labels[field_dictionary['N']][0]])
                    ],
                linewidths=[
                    float(pkl.loc[row,dimension_labels[field_dictionary['H']][1]]),
                    float(pkl.loc[row,dimension_labels[field_dictionary['N']][1]])
                    ],
                format_="nmrdraw"
                )
            peakList.append(peak)

    fin.close()
    return peakList
