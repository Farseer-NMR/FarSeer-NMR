import unittest

from core import parsing
import core.fslibs.parsing_routines as fspr

ansig_peaklist = 'test_data/ansig_peaklist.xpk'
sparky_peaklist = 'test_data/sparky_peaklist.peaks'
nmrdraw_peaklist = 'test_data/nmrdraw_peaklist.peaks'
nmrview_peaklist = 'test_data/nmrview_peaklist.xpk'
ccpn_peaklist = 'test_data/ccpn_peaklist.csv'


class Test_Parsing(unittest.TestCase):

    def test_get_peaklist_format(self):
        """
        Test that peaklist format detection returns correct values.
        """
        self.assertEqual(parsing.get_peaklist_format(ansig_peaklist),
                         'ANSIG')
        self.assertNotEqual(parsing.get_peaklist_format(sparky_peaklist),
                            'ANSIG')
        self.assertNotEqual(parsing.get_peaklist_format(nmrdraw_peaklist),
                            'ANSIG')
        self.assertNotEqual(parsing.get_peaklist_format(nmrview_peaklist),
                            'ANSIG')
        self.assertNotEqual(parsing.get_peaklist_format(ccpn_peaklist),
                            'ANSIG')

        self.assertNotEqual(parsing.get_peaklist_format(ansig_peaklist),
                            'SPARKY')
        self.assertEqual(parsing.get_peaklist_format(sparky_peaklist),
                         'SPARKY')
        self.assertNotEqual(parsing.get_peaklist_format(nmrdraw_peaklist),
                            'SPARKY')
        self.assertNotEqual(parsing.get_peaklist_format(nmrview_peaklist),
                            'SPARKY')
        self.assertNotEqual(parsing.get_peaklist_format(ccpn_peaklist),
                            'SPARKY')

        self.assertNotEqual(parsing.get_peaklist_format(ansig_peaklist),
                            'NMRDRAW')
        self.assertNotEqual(parsing.get_peaklist_format(sparky_peaklist),
                            'NMRDRAW')
        self.assertEqual(parsing.get_peaklist_format(nmrdraw_peaklist),
                         'NMRDRAW')
        self.assertNotEqual(parsing.get_peaklist_format(nmrview_peaklist),
                            'NMRDRAW')
        self.assertNotEqual(parsing.get_peaklist_format(ccpn_peaklist),
                            'NMRDRAW')

        self.assertNotEqual(parsing.get_peaklist_format(ansig_peaklist),
                            'NMRVIEW')
        self.assertNotEqual(parsing.get_peaklist_format(sparky_peaklist),
                            'NMRVIEW')
        self.assertNotEqual(parsing.get_peaklist_format(nmrdraw_peaklist),
                            'NMRVIEW')
        self.assertEqual(parsing.get_peaklist_format(nmrview_peaklist),
                         'NMRVIEW')
        self.assertNotEqual(parsing.get_peaklist_format(ccpn_peaklist),
                            'NMRVIEW')

        self.assertNotEqual(parsing.get_peaklist_format(ansig_peaklist),
                            'CCPNMRV2')
        self.assertNotEqual(parsing.get_peaklist_format(sparky_peaklist),
                            'CCPNMRV2')
        self.assertNotEqual(parsing.get_peaklist_format(nmrdraw_peaklist),
                            'CCPNMRV2')
        self.assertNotEqual(parsing.get_peaklist_format(nmrview_peaklist),
                            'CCPNMRV2')
        self.assertEqual(parsing.get_peaklist_format(ccpn_peaklist), 'CCPNMRV2')

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

        self.assertIsNotNone(peak_number)
        self.assertIsNotNone(positions)
        self.assertIsNotNone(atoms)
        self.assertNotIn(None, linewidths)
        self.assertIsNotNone(volume)
        self.assertIsNotNone(height)
        self.assertIsNotNone(fit_method)
        self.assertIsNotNone(volume_method)
        self.assertIsNotNone(merit)
        self.assertIsNotNone(details)

        self.assertEqual(len(peaklist), 58)
        #self.assertEqual(len(residue_number), 58)


if __name__ == "__main__":
    unittest.main()
