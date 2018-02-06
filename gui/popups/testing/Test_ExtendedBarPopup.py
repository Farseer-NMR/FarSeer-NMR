import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication

from gui.popups.ExtendedBarPopup import ExtendedBarPopup
from core.utils import get_default_config_path


app = QApplication(sys.argv)

from core.fslibs.Variables import Variables

class Test_ExtendedBarPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["extended_bar_settings"]
        fin.close()


        self.popup = ExtendedBarPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())


    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.bar_cols.field.value(), self.defaults[
            "cols_page"])
        self.assertEqual(self.popup.bar_rows.field.value(), self.defaults[
            "rows_page"])
        self.assertEqual(self.popup.x_tick_font.fields.currentText(), 
                         self.defaults["x_ticks_fn"])
        self.assertEqual(self.popup.x_tick_font_size.field.value(), 
                         self.defaults["x_ticks_fs"])
        self.assertEqual(self.popup.x_tick_rotation.field.value(), 
                         self.defaults["x_ticks_rot"])
        self.assertEqual(self.popup.x_tick_font_weight.fields.currentText(),
                         self.defaults["x_ticks_weight"])
        self.assertEqual(self.popup.x_tick_colour.isChecked(), 
                         self.defaults["x_ticks_color_flag"])
        

    def test_set_values(self):
        self.popup.bar_cols.setValue(4)
        self.popup.bar_rows.setValue(15)
        self.popup.x_tick_font.select('Arial')
        self.popup.x_tick_font_size.setValue(15)
        self.popup.x_tick_rotation.setValue(75)
        self.popup.x_tick_font_weight.select('bold')
        self.popup.x_tick_colour.setChecked(False)
        
        self.popup.set_values()

        self.assertEqual(self.popup.bar_cols.field.value(), 4)
        self.assertEqual(self.popup.variables["extended_bar_settings"]
                         ["cols_page"], 4)
        self.assertEqual(self.popup.bar_rows.field.value(), 15)
        self.assertEqual(self.popup.variables["extended_bar_settings"][
                             "rows_page"], 15)
        self.assertEqual(self.popup.x_tick_font.fields.currentText(),
                         'Arial')
        self.assertEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_fn"], 'Arial')
        self.assertEqual(self.popup.x_tick_font_size.field.value(), 15)
        self.assertEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_fs"], 15)
        self.assertEqual(self.popup.x_tick_rotation.field.value(), 75)
        self.assertEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_rot"], 75)
        self.assertEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_weight"], 'bold')
        self.assertEqual(self.popup.x_tick_font_weight.fields.currentText(),
                         'bold')
        self.assertEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_weight"], 'bold')
        self.assertEqual(self.popup.x_tick_colour.isChecked(), False)
        self.assertEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_color_flag"], False)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

    def test_values_not_set(self):
        self.popup.bar_cols.setValue(4)
        self.popup.bar_rows.setValue(15)
        self.popup.x_tick_font.select('Arial')
        self.popup.x_tick_font_size.setValue(15)
        self.popup.x_tick_rotation.setValue(75)
        self.popup.x_tick_font_weight.select('bold')
        self.popup.x_tick_colour.setChecked(False)

        self.assertEqual(self.popup.bar_cols.field.value(), 4)
        self.assertNotEqual(self.popup.variables["extended_bar_settings"]
                         ["cols_page"], 4)
        self.assertEqual(self.popup.bar_rows.field.value(), 15)
        self.assertNotEqual(self.popup.variables["extended_bar_settings"][
                             "rows_page"], 15)
        self.assertEqual(self.popup.x_tick_font.fields.currentText(),
                         'Arial')
        self.assertNotEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_fn"], 'Arial')
        self.assertEqual(self.popup.x_tick_font_size.field.value(), 15)
        self.assertNotEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_fs"], 15)
        self.assertEqual(self.popup.x_tick_rotation.field.value(), 75)
        self.assertNotEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_rot"], 75)
        self.assertEqual(self.popup.x_tick_font_weight.fields.currentText(),
                         'bold')
        self.assertNotEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_weight"], 'bold')
        self.assertEqual(self.popup.x_tick_colour.isChecked(), False)
        self.assertNotEqual(self.popup.variables["extended_bar_settings"][
                             "x_ticks_color_flag"], False)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)


if __name__ == "__main__":
    unittest.main()