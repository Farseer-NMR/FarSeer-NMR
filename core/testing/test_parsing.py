import unittest

from core import parsing 

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

        self.assertEqual(parsing.get_peaklist_format(ansig_peaklist), 'ANSIG')
        self.assertNotEqual(parsing.get_peaklist_format(sparky_peaklist), 'ANSIG')
        self.assertNotEqual(parsing.get_peaklist_format(nmrdraw_peaklist), 'ANSIG')
        self.assertNotEqual(parsing.get_peaklist_format(nmrview_peaklist), 'ANSIG')
        self.assertNotEqual(parsing.get_peaklist_format(ccpn_peaklist), 'ANSIG')

        self.assertNotEqual(parsing.get_peaklist_format(ansig_peaklist), 'SPARKY')
        self.assertEqual(parsing.get_peaklist_format(sparky_peaklist), 'SPARKY')
        self.assertNotEqual(parsing.get_peaklist_format(nmrdraw_peaklist), 'SPARKY')
        self.assertNotEqual(parsing.get_peaklist_format(nmrview_peaklist), 'SPARKY')
        self.assertNotEqual(parsing.get_peaklist_format(ccpn_peaklist), 'SPARKY')

        self.assertNotEqual(parsing.get_peaklist_format(ansig_peaklist), 'NMRDRAW')
        self.assertNotEqual(parsing.get_peaklist_format(sparky_peaklist), 'NMRDRAW')
        self.assertEqual(parsing.get_peaklist_format(nmrdraw_peaklist), 'NMRDRAW')
        self.assertNotEqual(parsing.get_peaklist_format(nmrview_peaklist), 'NMRDRAW')
        self.assertNotEqual(parsing.get_peaklist_format(ccpn_peaklist), 'NMRDRAW')

        self.assertNotEqual(parsing.get_peaklist_format(ansig_peaklist), 'NMRVIEW')
        self.assertNotEqual(parsing.get_peaklist_format(sparky_peaklist), 'NMRVIEW')
        self.assertNotEqual(parsing.get_peaklist_format(nmrdraw_peaklist), 'NMRVIEW')
        self.assertEqual(parsing.get_peaklist_format(nmrview_peaklist), 'NMRVIEW')
        self.assertNotEqual(parsing.get_peaklist_format(ccpn_peaklist), 'NMRVIEW')

        self.assertNotEqual(parsing.get_peaklist_format(ansig_peaklist), 'CCPN')
        self.assertNotEqual(parsing.get_peaklist_format(sparky_peaklist), 'CCPN')
        self.assertNotEqual(parsing.get_peaklist_format(nmrdraw_peaklist), 'CCPN')
        self.assertNotEqual(parsing.get_peaklist_format(nmrview_peaklist), 'CCPN')
        self.assertEqual(parsing.get_peaklist_format(ccpn_peaklist), 'CCPN')
    

    def test_parse_ansig(self):
        """
        Test ansig peaklist parsing
        """
        peaklist = parsing.parse_ansig_peaklist(ansig_peaklist)
        assignments = [peak.assignments for peak in peaklist if '???' not in peak.assignments]
        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        peak_assigments = peaklist[0].assignments
        linewidths = peaklist[0].linewidths
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details


        self.assertEqual(len(peaklist), 190)
        self.assertEqual(len(assignments), 182)
        self.assertIsNotNone(peak_number)
        self.assertIsNotNone(peak_assigments)
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
        peaklist = parsing.parse_sparky_peaklist(sparky_peaklist)
        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        peak_assigments = peaklist[0].assignments
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertIsNotNone(peak_number)
        self.assertIsNotNone(peak_assigments)
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
        peaklist = parsing.parse_nmrview_peaklist(nmrview_peaklist)
        assignments = [peak.assignments for peak in peaklist if None not in peak.assignments]

        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        peak_assigments = peaklist[0].assignments
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertIsNotNone(peak_number)
        self.assertIsNotNone(peak_assigments)
        self.assertIsNotNone(positions)
        self.assertIsNotNone(atoms)
        self.assertNotIn(None, linewidths)
        self.assertIsNotNone(volume)
        self.assertIsNotNone(height)
        self.assertIsNone(fit_method)
        self.assertIsNone(volume_method)
        self.assertIsNone(merit)
        self.assertIsNone(details)

        self.assertEqual(len(peaklist), 190)
        self.assertEqual(len(assignments), 182)


    def test_parse_nmrdraw(self):
        """
        Test nmrdraw peaklist parsing
        """
        peaklist = parsing.parse_nmrdraw_peaklist(nmrdraw_peaklist)
        assignments = [peak.assignments for peak in peaklist if '' not in peak.assignments]

        self.assertEqual(len(peaklist), 190)
        self.assertEqual(len(assignments), 182)

        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        peak_assigments = peaklist[0].assignments
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertIsNotNone(peak_number)
        self.assertIsNotNone(peak_assigments)
        self.assertIsNotNone(positions)
        self.assertIsNotNone(atoms)
        self.assertNotIn(None, linewidths)
        self.assertIsNotNone(volume)
        self.assertIsNotNone(height)
        self.assertIsNone(fit_method)
        self.assertIsNone(volume_method)
        self.assertIsNone(merit)
        self.assertIsNone(details)

    def test_parse_ccpn(self):
        """
        Test CCPN peaklist parsing
        """
        peaklist = parsing.parse_ccpn_peaklist(ccpn_peaklist)
        assignments = [peak.assignments for peak in peaklist if '' not in peak.assignments]

        peak_number = peaklist[0].peak_number
        positions = peaklist[0].positions
        atoms = peaklist[0].atoms
        linewidths = peaklist[0].linewidths
        peak_assigments = peaklist[0].assignments
        volume = peaklist[0].volume
        height = peaklist[0].height
        fit_method = peaklist[0].fit_method
        merit = peaklist[0].merit
        volume_method = peaklist[0].volume_method
        details = peaklist[0].details

        self.assertIsNotNone(peak_number)
        self.assertIsNotNone(peak_assigments)
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
        self.assertEqual(len(assignments), 58)





if __name__ == "__main__":
    unittest.main()
