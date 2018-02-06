import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication
from current.utils import aal3tol1, aal1tol3
from current.utils import get_default_config_path


from gui.popups.CSPExceptionsPopup import CSPExceptionsPopup

app = QApplication(sys.argv)

from current.fslibs.Variables import Variables

test_values = [0.06, 0.36, 0.48, 0.4, 0.32, 0.96, 0.51, 0.84, 0.72, 0.63,
               0.64, 0.02, 0.98, 0.97, 0.45, 0.92, 0.44, 0.31, 0.27, 0.42]


class Test_CSPExceptionsPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["csp_settings"]["csp_res_exceptions"]
        fin.close()

        self.popup = CSPExceptionsPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())


    def test_defaults(self):
        """Test popup reads and sets default variables"""
        for res, val in self.popup.value_dict.items():
            if res != "Gly":
                self.assertEqual(val.field.value(),
                                 self.popup.alpha_value)
            else:
                self.assertEqual(val.field.value(), 0.2)

        self.assertIn("Gly", self.popup.value_dict.keys())

    def test_change_variables(self):
        pass


    def test_set_values(self):
        keys = list(self.popup.value_dict.keys())
        for val, key in zip(test_values, keys):
            self.popup.value_dict[key].setValue(val)

        for ii, key in enumerate(keys):
            self.assertEqual(self.popup.value_dict[key].field.value(),
                             test_values[ii])

        self.popup.set_values()

        for ii, k in enumerate(keys):
            key = aal3tol1[k]
            self.assertEqual(self.popup.variables["csp_settings"][
                                 "csp_res_exceptions"][key], test_values[ii])

    def test_values_not_set(self):
        keys = list(self.popup.value_dict.keys())
        for val, key in zip(test_values, keys):
            self.popup.value_dict[key].setValue(val)

        for ii, key in enumerate(keys):
            self.assertEqual(self.popup.value_dict[key].field.value(),
                             test_values[
                ii])

        for ii, k in enumerate(keys):
            key = aal3tol1[k]
            if key in self.popup.variables["csp_settings"][
                                 "csp_res_exceptions"].keys():
                self.assertNotEqual(self.popup.variables["csp_settings"][
                                 "csp_res_exceptions"][key], test_values[ii])




if __name__ == "__main__":
    unittest.main()