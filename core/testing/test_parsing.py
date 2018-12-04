import os
import unittest
import itertools as it
from core import parsing
import core.fslibs.parsing_routines as fspr

ansig_peaklist = os.path.join('test_data', 'ansig_peaklist.xpk')
sparky_peaklist = os.path.join('test_data', 'sparky_peaklist.peaks')
nmrdraw_peaklist = os.path.join('test_data', 'nmrdraw_peaklist.peaks')
nmrview_peaklist = os.path.join('test_data', 'nmrview_peaklist.xpk')
ccpn_peaklist = os.path.join('test_data', 'ccpn_peaklist.csv')
user_pkl_1 = os.path.join('test_data', 'user_pkl_1.prot')
user_pkl_2 = os.path.join('test_data', 'user_pkl_2.str')

pkls_types = {
    'ANSIG':os.path.join('test_data', 'ansig_peaklist.xpk'),
    'SPARKY':os.path.join('test_data', 'sparky_peaklist.peaks'),
    'NMRDRAW':os.path.join('test_data', 'nmrdraw_peaklist.peaks'),
    'NMRVIEW':os.path.join('test_data', 'nmrview_peaklist.xpk'),
    'CCPNMRV2':os.path.join('test_data', 'ccpn_peaklist.csv'),
    'USER_PKL_1':os.path.join('test_data', 'user_pkl_1.prot'),
    'USER_PKL_2':os.path.join('test_data', 'user_pkl_2.str'),
    'USER_PKL_3':os.path.join('test_data', 'user_pkl_3.csv')
    }

class Test_Parsing(unittest.TestCase):

    def test_get_peaklist_format(self):
        """
        Test that peaklist format detection returns correct values.
        """
        
        for pkl_current, pkl_test in \
            it.product(pkls_types.keys(), pkls_types.keys()):
                
            if pkl_current == pkl_test:
                self.assertEqual(
                    parsing.get_peaklist_format(pkls_types[pkl_test]),
                    pkl_current
                    )
            
            elif pkl_current != pkl_test:
                self.assertNotEqual(
                    parsing.get_peaklist_format(pkls_types[pkl_test]),
                    pkl_current
                    )
            

    def test_parse_ansig(self):
        """
        Test ansig peaklist parsing
        """
        peaklist = fspr.ansig(ansig_peaklist)
        residue_type = peaklist[0].residue_type
        residue_number = peaklist[0].residue_number
        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertEqual(len(peaklist), 182)
        #self.assertEqual(len(residue_number), 182)
        self.assertIsNotNone(peak_number)
        self.assertIsNotNone(residue_type)
        self.assertIsNotNone(residue_number)
        self.assertIsNotNone(positions)
        self.assertIsNotNone(atoms)
        self.assertIsNotNone(linewidths)
        self.assertIsNotNone(volume)
        self.assertIsNotNone(height)
        self.assertIsNone(fit_method)
        self.assertIsNone(volume_method)
        self.assertIsNone(merit)
        self.assertIsNone(details)

    def test_parse_sparky(self):
        """
        Test sparky peaklist parsing
        """
        peaklist = fspr.sparky(sparky_peaklist)
        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        residue_type = peaklist[0].residue_type
        residue_number = peaklist[0].residue_number
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertIsNotNone(peak_number)
        self.assertIsNotNone(residue_type)
        self.assertIsNotNone(residue_number)
        self.assertIsNotNone(positions)
        self.assertIsNotNone(atoms)
        self.assertIn(None, linewidths)
        self.assertIsNotNone(volume)
        self.assertIsNotNone(height)
        self.assertIsNone(fit_method)
        self.assertIsNone(volume_method)
        self.assertIsNone(merit)
        self.assertIsNone(details)

        self.assertEqual(len(peaklist), 181)

    def test_parse_nmrview(self):
        """
        Test nmrview peaklist parsing
        """
        peaklist = fspr.nmrview(nmrview_peaklist)
        residue_types = any([peak.residue_type for peak in peaklist])
        residue_number = peaklist[0].residue_number
        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertIsNotNone(peak_number)
        self.assertFalse(residue_types)
        self.assertIsNotNone(residue_number)
        self.assertIsNotNone(positions)
        self.assertIsNotNone(atoms)
        self.assertNotIn(None, linewidths)
        self.assertIsNotNone(volume)
        self.assertIsNotNone(height)
        self.assertIsNone(fit_method)
        self.assertIsNone(volume_method)
        self.assertIsNone(merit)
        self.assertIsNone(details)

        self.assertEqual(len(peaklist), 182)
        #self.assertEqual(len(residue_number), 182)

    def test_parse_nmrdraw(self):
        """
        Test nmrview peaklist parsing
        """
        peaklist = fspr.nmrview(nmrview_peaklist)
        residue_types = any([peak.residue_type for peak in peaklist])
        residue_number = peaklist[0].residue_number
        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertIsNotNone(peak_number)
        self.assertFalse(residue_types)
        self.assertIsNotNone(residue_number)
        self.assertIsNotNone(positions)
        self.assertIsNotNone(atoms)
        self.assertNotIn(None, linewidths)
        self.assertIsNotNone(volume)
        self.assertIsNotNone(height)
        self.assertIsNone(fit_method)
        self.assertIsNone(volume_method)
        self.assertIsNone(merit)
        self.assertIsNone(details)

        self.assertEqual(len(peaklist), 182)
        #self.assertEqual(len(residue_number), 182)

    def test_parse_ccpn(self):
        """
        Test CCPN peaklist parsing
        
        Bypasses CCPNMRv2 peaklists.
    
        This peaklist is not parsed to Peak, a list with one
        dummy Peak element is created with .format_ = ccpnmrv2
        so that it is bypassed directly to spectra in
        core.setup_farseer_calculation.py
        """
        peaklist = fspr.ccpnmrv2(ccpn_peaklist)
        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        residue_type = peaklist[0].residue_type
        residue_number = peaklist[0].residue_number
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertIsNone(peak_number)
        self.assertIsNone(positions)
        self.assertIsNone(atoms)
        self.assertEqual([None, None], linewidths)
        self.assertIsNone(volume)
        self.assertIsNone(height)
        self.assertIsNone(fit_method)
        self.assertIsNone(volume_method)
        self.assertIsNone(merit)
        self.assertIsNone(details)

        self.assertEqual(len(peaklist), 1)
        #self.assertEqual(len(residue_number), 58)


if __name__ == "__main__":
    unittest.main()
