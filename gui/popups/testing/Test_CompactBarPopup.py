import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication

from gui.popups.CompactBarPopup import CompactBarPopup
from core.utils import get_default_config_path
from core.fslibs.Variables import Variables

app = QApplication(sys.argv)


class Test_CompactBarPopup(unittest.TestCase):

    def setUp(self):
        """ Create the popup"""

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["compact_bar_settings"]
        fin.close()

        self.popup = CompactBarPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())

    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.bar_cols.field.value(),
                         self.defaults["cols_page"])
        self.assertEqual(self.popup.bar_rows.field.value(),
                         self.defaults["rows_page"])
        self.assertEqual(self.popup.x_tick_font.fields.currentText(),
                         self.defaults["x_ticks_fn"])
        self.assertEqual(self.popup.x_tick_font_size.field.value(),
                         self.defaults["x_ticks_fs"])
        self.assertEqual(self.popup.x_tick_rotation.field.value(),
                         self.defaults["x_ticks_rot"])
        self.assertEqual(self.popup.x_tick_weight.fields.currentText(),
                         self.defaults["x_ticks_weight"])
        self.assertEqual(self.popup.shade_unassigned_checkbox.isChecked(),
                         self.defaults["unassigned_shade"])
        self.assertEqual(self.popup.unassigned_shade_alpha.field.value(),
                         self.defaults["unassigned_shade_alpha"])

    def test_set_values(self):
        self.popup.bar_cols.setValue(4)
        self.popup.bar_rows.setValue(10)
        self.popup.x_tick_font.select("Times New Roman")
        self.popup.x_tick_font_size.setValue(48)
        self.popup.x_tick_rotation.setValue(145)
        self.popup.x_tick_weight.select('bold')
        self.popup.shade_unassigned_checkbox.setChecked(False)
        self.popup.unassigned_shade_alpha.setValue(0.6)
        self.popup.set_values()

        self.assertEqual(
            self.popup.variables["compact_bar_settings"]['cols_page'], 4)
        self.assertEqual(
            self.popup.variables["compact_bar_settings"]['rows_page'], 10)
        self.assertEqual(
            self.popup.variables["compact_bar_settings"]
            ['x_ticks_fn'], "Times New Roman")
        self.assertEqual(
            self.popup.variables["compact_bar_settings"]['x_ticks_fs'], 48)
        self.assertEqual(
            self.popup.variables["compact_bar_settings"]['x_ticks_rot'], 145)
        self.assertEqual(self.popup.variables["compact_bar_settings"]
                         ['x_ticks_weight'], 'bold')
        self.assertEqual(self.popup.variables["compact_bar_settings"]
                         ['unassigned_shade'], False)
        self.assertEqual(self.popup.variables["compact_bar_settings"]
                         ['unassigned_shade_alpha'], 0.6)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

    def test_values_not_set(self):
        self.popup.bar_cols.setValue(4)
        self.popup.bar_rows.setValue(10)
        self.popup.x_tick_font.select("Times New Roman")
        self.popup.x_tick_font_size.setValue(48)
        self.popup.x_tick_rotation.setValue(145)
        self.popup.x_tick_weight.select('bold')
        self.popup.shade_unassigned_checkbox.setChecked(False)
        self.popup.unassigned_shade_alpha.setValue(160)

        self.assertNotEqual(
            self.popup.variables["compact_bar_settings"]['cols_page'], 4)
        self.assertNotEqual(
            self.popup.variables["compact_bar_settings"]['rows_page'], 10)
        self.assertNotEqual(
            self.popup.variables["compact_bar_settings"]['x_ticks_fn'],
            "Times New Roman")
        self.assertNotEqual(
            self.popup.variables["compact_bar_settings"]['x_ticks_fs'], 48)
        self.assertNotEqual(
            self.popup.variables["compact_bar_settings"]['x_ticks_rot'],
            145)
        self.assertNotEqual(
            self.popup.variables["compact_bar_settings"]['x_ticks_weight'],
            'bold')
        self.assertNotEqual(
            self.popup.variables["compact_bar_settings"]['unassigned_shade'],
            False)
        self.assertNotEqual(self.popup.variables["compact_bar_settings"][
                             'unassigned_shade_alpha'], 160)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

    def test_spinboxes(self):

        self.popup.bar_cols.setValue(0)
        self.popup.bar_rows.setValue(0)
        self.popup.x_tick_font_size.setValue(1)
        self.popup.x_tick_rotation.setValue(361)
        self.assertEqual(self.popup.bar_cols.field.value(), 1)
        self.assertEqual(self.popup.bar_rows.field.value(), 1)
        self.assertEqual(self.popup.x_tick_font_size.field.value(), 1)
        self.assertEqual(self.popup.x_tick_rotation.field.value(), 360)


if __name__ == "__main__":
    unittest.main()
