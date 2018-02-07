import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication

from gui.popups.VerticalBar import VerticalBarPopup
from core.utils import get_default_config_path
from core.fslibs.Variables import Variables

app = QApplication(sys.argv)


class Test_VerticalBarPopup(unittest.TestCase):

    def setUp(self):
        """ Create the popup"""
        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["vert_bar_settings"]
        fin.close()

        self.popup = VerticalBarPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())

    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.bar_cols.field.value(), self.defaults[
            "cols_page"])
        self.assertEqual(self.popup.bar_rows.field.value(), self.defaults[
            "rows_page"])

    def test_set_values(self):

        self.popup.bar_cols.setValue(15)
        self.popup.bar_rows.setValue(20)

        self.popup.set_values()

        self.assertEqual(self.popup.bar_cols.field.value(), 15)
        self.assertEqual(self.popup.variables["vert_bar_settings"]
                         ["cols_page"], 15)

        self.assertEqual(self.popup.bar_rows.field.value(), 20)
        self.assertEqual(self.popup.variables["vert_bar_settings"]
                         ["rows_page"], 20)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

    def test_values_not_set(self):

        self.popup.bar_cols.setValue(15)
        self.popup.bar_rows.setValue(20)

        self.assertEqual(self.popup.bar_cols.field.value(), 15)
        self.assertNotEqual(self.popup.variables["vert_bar_settings"]
                            ["cols_page"], 15)

        self.assertEqual(self.popup.bar_rows.field.value(), 20)
        self.assertNotEqual(self.popup.variables["vert_bar_settings"]
                            ["rows_page"], 20)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)


if __name__ == "__main__":
    unittest.main()
