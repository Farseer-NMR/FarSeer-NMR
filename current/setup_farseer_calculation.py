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
import csv
import os
from shutil import copy2

from current.parsing import read_peaklist


def create_directory_structure(output_path, variables):
    spectrum_dir = output_path+'/spectra/'
    if os.path.exists(os.path.join(spectrum_dir)):
        return "Path Exists"

    else:
        os.makedirs(spectrum_dir)
    exp_dataset = variables["experimental_dataset"]
    if not exp_dataset:
        return "No dataset"
    for ii, z_key in enumerate(variables["conditions"]["z"]):
        for jj, y_key in enumerate(variables["conditions"]["y"]):
            z_name = '_'.join(["{:0>2}".format(ii), z_key])
            y_name = '_'.join(["{:0>2}".format(jj), y_key])
            if not os.path.exists(os.path.join(spectrum_dir, z_name, y_name)):
                os.makedirs(os.path.join(spectrum_dir, z_name, y_name))
            if variables["fasta_settings"]["applyFASTA"]:
                if variables["fasta_files"][y_key]:
                    fasta_file = variables["fasta_files"][y_key]
                    copy2(fasta_file, os.path.join(spectrum_dir, z_name, y_name))
            for kk, x_key in enumerate(variables["conditions"]["x"]):
                x_name = '_'.join(["{:0>2}".format(kk), x_key])
                fout = open(os.path.join(spectrum_dir, z_name, y_name, "%s.csv" % x_name), 'w')
                peaklist_path = variables["peaklists"][exp_dataset[z_key][y_key][x_key]]
                peaklist = read_peaklist(peaklist_path)
                write_peaklist_file(fout, peaklist)
                fout.close()
    return "Run"


def write_peaklist_file(fin, peak_list):
    writer = csv.writer(fin)
    header = ['Number', '#', 'Position F1', 'Position F2', 'Assign F1',
              'Assign F2', 'Height', 'Volume', 'Line Width F1 (Hz)',
              'Line Width F2 (Hz)', 'Merit', 'Details', 'Fit Method',
              'Vol. Method']
    writer.writerow(header)
    for ii, peak in enumerate(peak_list):
        writer.writerow([
            ii,
            peak.peak_number,
            peak.positions[0],
            peak.positions[1],
            peak.assignments[0],
            peak.assignments[1],
            peak.height,
            peak.volume,
            peak.linewidths[0],
            peak.linewidths[1],
            peak.merit,
            peak.details,
            peak.fit_method,
            peak.volume_method
        ])

def list_all_files_in_path(path):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path)
              for f in filenames]
    return result
