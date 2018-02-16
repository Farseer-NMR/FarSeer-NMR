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

from core.parsing import read_peaklist
from core.utils import aal1tol3


def check_input_construction(output_path, variables):

    if not output_path.endswith('/'):
        output_path += '/'

    spectrum_dir = output_path + 'spectra/'
    if os.path.exists(os.path.join(spectrum_dir)):
        return "Path Exists"

    exp_dataset = variables["experimental_dataset"]
    if not exp_dataset:
        return "No dataset"
    for ii, z_key in enumerate(variables["conditions"]["z"]):
        for jj, y_key in enumerate(variables["conditions"]["y"]):
            if variables["fasta_settings"]["applyFASTA"]:
                fasta_file = variables["fasta_files"].get(y_key)
                if not fasta_file:
                    return "Invalid Fasta"

            for kk, x_key in enumerate(variables["conditions"]["x"]):
                peaklist_path = variables["peaklists"][exp_dataset[z_key]
                [y_key][x_key]]
                peaklist = read_peaklist(peaklist_path)
                if peaklist[0].format in ['nmrdraw', 'nmrview']:
                    fasta_file = variables["fasta_files"].get(y_key)
                    if not fasta_file:
                        print('fasta file not specified for %s' % y_key)
                        return "Invalid Fasta"
    else:
        return "Run"





def create_directory_structure(output_path, variables):

    spectrum_dir = os.path.join(output_path, 'spectra')
    exp_dataset = variables["experimental_dataset"]

    for ii, z_key in enumerate(variables["conditions"]["z"]):
        for jj, y_key in enumerate(variables["conditions"]["y"]):
            z_name = '_'.join(["{:0>2}".format(ii), z_key])
            y_name = '_'.join(["{:0>2}".format(jj), y_key])

            if not os.path.exists(os.path.join(spectrum_dir, z_name, y_name)):
                os.makedirs(os.path.join(spectrum_dir, z_name, y_name))
            if variables["fasta_settings"]["applyFASTA"]:

                fasta_file = variables["fasta_files"][y_key]
                copy2(fasta_file, os.path.join(spectrum_dir,
                                                   z_name, y_name))
            for kk, x_key in enumerate(variables["conditions"]["x"]):
                x_name = '_'.join(["{:0>2}".format(kk), x_key])
                fout = open(os.path.join(spectrum_dir, z_name, y_name,
                                         "%s.csv" % x_name), 'w')
                peaklist_path = variables["peaklists"][exp_dataset[z_key]
                                                       [y_key][x_key]]
                peaklist = read_peaklist(peaklist_path)
                if peaklist[0].format in ['nmrdraw', 'nmrview']:
                    fasta_file = variables["fasta_files"].get(y_key)
                    fasta_start = variables['fasta_settings']['FASTAstart']
                    write_peaklist_file(fout,
                                    add_residue_information(peaklist,
                                                            fasta_file,
                                                            fasta_start))
                else:
                    write_peaklist_file(fout, peaklist)
                fout.close()


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

def add_residue_information(peak_list, fasta_file, fasta_start):


    cleaned_peaklist = []

    fasta = ''.join([line.replace('\n', '') for line in
                     open(fasta_file, 'r').readlines()[1:]])
    fasta_dict = {ii + fasta_start: aal1tol3.get(residue) for ii, residue in
                  enumerate(fasta)}
    import pprint
    for peak in peak_list:
        if all(ass is None for ass in peak.assignments) and \
                not '' in peak.assignments:
            continue
        resno = peak.assignments[0].split('.')[0]

        res_type = fasta_dict.get(int(resno))
        if not res_type:
            print('Residue number %s is invalid' % str(resno))
            continue
        assignment = [''.join([resno, res_type, 'H']),
                      ''.join([resno, res_type, 'N'])]
        peak.assignments = assignment
        cleaned_peaklist.append(peak)
    return cleaned_peaklist
