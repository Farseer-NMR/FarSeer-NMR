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
from core.utils import aal1tol3, read_fasta_file, peaklist_format_requires_fasta
from core.fslibs import wet as fsw

def check_input_construction(output_path, variables):

    if not output_path.endswith('/'):
        output_path += '/'


    if os.path.exists(os.path.join(output_path, 'spectra')):
        return "Spectra"

    if os.path.exists(os.path.join(output_path, 'Backbone')):
        return "Backbone"

    if os.path.exists(os.path.join(output_path, 'Sidechains')):
        return "Sidechains"

    exp_dataset = variables["experimental_dataset"]

    if not exp_dataset:
        return "No dataset"

    populated_tree = True
    for k, v in exp_dataset.items():
        if isinstance(v, dict):
            for k1, v1 in v.items():
                if isinstance(v1, dict):
                    for k2, v2 in v1.items():
                        if v2:
                            populated_tree = populated_tree & True
                        else:
                            populated_tree = populated_tree & False

    if not(populated_tree):
        return "No populated Tree"
    if variables["fasta_settings"]["applyFASTA"]:
        for y_key in variables["conditions"]["y"]:
            fasta_file = variables["fasta_files"].get(y_key, False)
            if not fasta_file:
                return "FASTA file not provided"

    for kz, vz in exp_dataset.items():
        for ky, vy in vz.items():
            for kx, vx in vy.items():
                peaklist_path = variables["peaklists"][vx]
                peaklist = read_peaklist(peaklist_path)
                if peaklist[0].format_ in peaklist_format_requires_fasta:
                    fasta_file = variables["fasta_files"].get(ky, False)
                    if not fasta_file:
                        print('FASTA file not specified for {}'.format(ky))
                        return "No FASTA for peaklist"

    if variables["pre_settings"]["apply_PRE_analysis"]:
        if not(all([k in ['dia', 'para'] for k in exp_dataset.keys()])):
            return "Para name not set"
        for y_key in variables["conditions"]["y"]:
            pre_file = variables["pre_files"].get(y_key, False)
            if not pre_file:
                return "PRE file not provided"

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
                copy2(fasta_file, os.path.join(spectrum_dir, z_name, y_name))

            if variables["pre_settings"]["apply_PRE_analysis"] \
                    and z_name == "01_para":
                pre_file = variables["pre_files"][y_key]
                copy2(pre_file, os.path.join(spectrum_dir, z_name, y_name))

            for kk, x_key in enumerate(variables["conditions"]["x"]):
                x_name = '_'.join(["{:0>2}".format(kk), x_key])
                fout = open(
                    os.path.join(
                        spectrum_dir,
                        z_name,
                        y_name,
                        "%s.csv" % x_name
                        ),
                    'w'
                    )
                peaklist_path = \
                    variables["peaklists"][exp_dataset[z_key][y_key][x_key]]
                peaklist = read_peaklist(peaklist_path)

                if peaklist[0].format_ in peaklist_format_requires_fasta:
                    fasta_file = variables["fasta_files"].get(y_key)
                    fasta_start = variables['fasta_settings']['FASTAstart']
                    write_peaklist_file(
                        fout,
                        add_residue_information(
                            peaklist_path,
                            peaklist,
                            fasta_file,
                            fasta_start
                            )
                        )
                else:
                    write_peaklist_file(fout, peaklist)

                fout.close()

def write_peaklist_file(fin, peak_list):
    writer = csv.writer(fin)
    header = [
        'Number',
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
        'Vol. Method'
        ]
    writer.writerow(header)

    for ii, peak in enumerate(peak_list):
        print(peak)
        writer.writerow(
            [
                ii,
                peak.peak_number,
                peak.positions[0],
                peak.positions[1],
                "".join([peak.residue_number, peak.residue_type, peak.atoms[0]]),
                "".join([peak.residue_number, peak.residue_type, peak.atoms[1]]),
                peak.height,
                peak.volume,
                peak.linewidths[0],
                peak.linewidths[1],
                peak.merit,
                peak.details,
                peak.fit_method,
                peak.volume_method
                ]
            )


def list_all_files_in_path(path):
    result = \
        [os.path.join(dp, f) for dp, dn, filenames in os.walk(path)
            for f in filenames]
    return result

def add_residue_information(peaklist_path, peak_list, fasta_path, fasta_start):
    """
    Parameters:
        - peaklist_path (str): the path for the peaklist original file.
        - peak_list (list): a list of Peak objects.
        - fasta_path (str): a string with the path for the FASTA file.
        - fasta_start (int): the FASTA's first residue number.

    Returns:
        - cleaned_peaklist (list): a list of Peak objects with residue type
            added in attribute residue_type.
    """
    cleaned_peaklist = []
    # Generates a single string from the FASTA file
    fasta = read_fasta_file(fasta_path)

    fasta_dict = \
        {ii + fasta_start: aal1tol3.get(residue)
            for ii, residue in enumerate(fasta)}

    for peak in peak_list:

        try:
            res_type = fasta_dict[int(peak.residue_number)]
        except KeyError:
            msg = \
"""There is a residue number in your peaklist file:
{}
that is not present in your FASTA file
{}

Please review the agreement between your peaklists and FASTA file.
""".\
                format(peaklist_path, fasta_path)
            print(fsw.gen_wet("ERROR", msg, 31))
            fsw.abort(m="Bad peaklist format")
        peak.residue_type = res_type
        cleaned_peaklist.append(peak)

    return cleaned_peaklist
