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
import unittest
import os

from core.parsing import read_peaklist
from core.setup_farseer_calculation import add_residue_information, write_peaklist_file

class Test_Case(unittest.TestCase):
    def setUp(self):
        self.nmrdraw_peaklist = read_peaklist(os.path.join('test_data', 'nmrdraw_peaklist.peaks'))
        self.nmrview_peaklist = read_peaklist(os.path.join('test_data', 'nmrview_peaklist.xpk'))
        self.result_peaklist = read_peaklist(os.path.join('test_data', 'nmr_view_draw_result.csv'))
        self.fasta_file = os.path.join('test_data', 'nmr_view_draw.fasta')
        self.maxDiff = None
        
        self.user_pkl_1 = read_peaklist(os.path.join('test_data', 'user_pkl_1.prot'))
        self.fasta_user_1 = os.path.join('test_data', 'user_pkl_1.fasta')
        self.user_pkl_1_result = read_peaklist(os.path.join('test_data', 'user_pkl_1_result.csv'))

    def test_format_detected(self):
        self.assertEqual(self.nmrdraw_peaklist[0].format_, 'nmrdraw')
        self.assertEqual(self.nmrview_peaklist[0].format_, 'nmrview')
        self.assertEqual(self.user_pkl_1[0].format_, 'user_pkl_1')

    def test_correct_fasta_addition_nmrdraw(self):
    #peaklist_path, peak_list, fasta_path, fasta_start
        nmrdraw_out = add_residue_information(
            'no_path',
            self.nmrdraw_peaklist,
            self.fasta_file,
            458
            )

        self.assertEqual(len(self.result_peaklist), len(nmrdraw_out))
        for rpeak, npeak in zip(self.result_peaklist, nmrdraw_out):
            self.assertEqual(rpeak.residue_type, npeak.residue_type)
            self.assertEqual(rpeak.residue_number, npeak.residue_number)

    def test_correct_fasta_addition_nmrview(self):
        nmrview_out = add_residue_information(
            'no_path',
            self.nmrdraw_peaklist,
            self.fasta_file,
            458
            )
        write_peaklist_file(open('nv_test.csv', 'w'), nmrview_out)
        self.assertEqual(len(self.result_peaklist), len(nmrview_out))
        for rpeak, npeak in zip(self.result_peaklist, nmrview_out):
            self.assertEqual(rpeak.residue_type, npeak.residue_type)
            self.assertEqual(rpeak.residue_number, npeak.residue_number)

    def test_correct_fasta_addition_user_pkl_1(self):
        user_pkl_1_out = add_residue_information(
            'no_path',
            self.user_pkl_1,
            self.fasta_user_1,
            1
            )
        write_peaklist_file(open('nv_test.csv', 'w'), user_pkl_1_out)
        self.assertEqual(len(self.user_pkl_1_result), len(user_pkl_1_out))
        for rpeak, npeak in zip(self.user_pkl_1_result, user_pkl_1_out):
            self.assertEqual(rpeak.residue_type, npeak.residue_type)
            self.assertEqual(rpeak.residue_number, npeak.residue_number)

if __name__ == "__main__":
    unittest.main()
