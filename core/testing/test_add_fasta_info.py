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

from core.parsing import read_peaklist
from core.setup_farseer_calculation import add_residue_information, write_peaklist_file

class Test_Case(unittest.TestCase):
    def setUp(self):
        self.nmrdraw_peaklist = read_peaklist('test_data/nmrdraw_peaklist.peaks')
        self.nmrview_peaklist = read_peaklist('test_data/nmrview_peaklist.xpk')
        self.result_peaklist = read_peaklist('test_data/nmr_view_draw_result.csv')
        self.fasta_file = 'test_data/nmr_view_draw.fasta'
        self.maxDiff = None

    def test_format_detected(self):
        self.assertEqual(self.nmrdraw_peaklist[0].format, 'nmrdraw')
        self.assertEqual(self.nmrview_peaklist[0].format, 'nmrview')

    def test_correct_fasta_addition_nmrdraw(self):
        nmrdraw_out = add_residue_information(self.nmrdraw_peaklist,
                                              self.fasta_file,
                                              458)

        self.assertEqual(len(self.result_peaklist), len(nmrdraw_out))
        for rpeak, npeak in zip(self.result_peaklist, nmrdraw_out):
            self.assertEqual(rpeak.assignments, npeak.assignments)



    def test_correct_fasta_addition_nmrview(self):
        nmrview_out = add_residue_information(self.nmrview_peaklist,
                                              self.fasta_file,
                                              458)
        write_peaklist_file(open('nv_test.csv', 'w'), nmrview_out)
        self.assertEqual(len(self.result_peaklist), len(nmrview_out))
        for rpeak, npeak in zip(self.result_peaklist, nmrview_out):
            self.assertEqual(rpeak.assignments, npeak.assignments)



if __name__ == "__main__":
    unittest.main()
