import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication

from core.utils import get_default_config_path

from gui.popups.PreAnalysisPopup import PreAnalysisPopup

app = QApplication(sys.argv)



from core.fslibs.Variables import Variables

class Test_PreAnalysisPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["pre_settings"]
        fin.close()


        self.popup = PreAnalysisPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())


    def test_defaults(self):
        """Test popup reads and sets default variables"""
        self.assertEqual(self.popup.gauss_x_size.field.value(),
                         self.defaults["gauss_x_size"])
        self.assertEqual(self.popup.gaussian_stdev.field.value(),
                         self.defaults["gaussian_stdev"])


    def test_set_values(self):

        self.popup.gauss_x_size.setValue(5)
        self.popup.gaussian_stdev.setValue(8)

        self.popup.set_values()

        self.assertEqual(self.popup.gauss_x_size.field.value(), 5)
        self.assertEqual(self.popup.gaussian_stdev.field.value(), 8)
        self.assertEqual(self.popup.variables["pre_settings"]["gauss_x_size"], 5)
        self.assertEqual(self.popup.variables["pre_settings"]["gaussian_stdev"], 8)

    def test_values_not_set(self):

        self.popup.gauss_x_size.setValue(5)
        self.popup.gaussian_stdev.setValue(8)

        self.assertEqual(self.popup.gauss_x_size.field.value(), 5)
        self.assertEqual(self.popup.gaussian_stdev.field.value(), 8)
        self.assertNotEqual(self.popup.variables["pre_settings"]["gauss_x_size"], 5)
        self.assertNotEqual(self.popup.variables["pre_settings"]["gaussian_stdev"], 8)
        self.assertEqual(tuple(self.popup.local_variables.keys()), self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()), self.variable_keys)


if __name__ == "__main__":
    unittest.main()