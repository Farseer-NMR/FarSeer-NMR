import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import os

from gui.popups.BarPlotPopup import BarPlotPopup

app = QApplication(sys.argv)

from core.fslibs.Variables import Variables

class Test_BarPlotPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''
        default_config = '/Users/fbssps/PycharmProjects/FarSeer-NMR/core/default_config.json'

        Variables().read(default_config)
        fin = open(default_config, 'r')
        self.popup = BarPlotPopup()
        self.defaults = json.load(fin)["bar_plot_settings"]
        fin.close()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())
        print(self.local_variable_keys)


    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.apply_status.isChecked(), self.defaults["status_color_flag"])
        self.assertEqual(self.popup.meas_bar_colour.fields.currentText(), self.defaults["measured_color"])
        self.assertEqual(self.popup.lost_bar_colour.fields.currentText(), self.defaults["lost_color"])
        self.assertEqual(self.popup.unassigned_bar_colour.fields.currentText(), self.defaults["unassigned_color"])
        self.assertEqual(self.popup.bar_width.field.value(), self.defaults["bar_width"])
        self.assertEqual(self.popup.bar_alpha.field.value(), self.defaults["bar_alpha"])
        self.assertEqual(self.popup.bar_linewidth.field.value(), self.defaults["bar_linewidth"])
        self.assertEqual(self.popup.bar_threshold.isChecked(), self.defaults["threshold_flag"])
        self.assertEqual(self.popup.bar_threshold_colour.fields.currentText(), self.defaults["threshold_color"])
        self.assertEqual(self.popup.bar_threshold_linewidth.field.value(), self.defaults["threshold_linewidth"])
        self.assertEqual(self.popup.bar_threshold_alpha.field.value(), self.defaults["threshold_alpha"])
        self.assertEqual(self.popup.user_mark_font_size.field.value(), self.defaults["mark_fontsize"])
        self.assertEqual(self.popup.markProlines.isChecked(), self.defaults["mark_prolines_flag"])
        self.assertEqual(self.popup.proline_marker.field.text(), self.defaults["mark_prolines_symbol"])
        self.assertEqual(self.popup.user_details.isChecked(), self.defaults["mark_user_details_flag"])
        self.assertEqual(self.popup.colour_user_details.isChecked(), self.defaults["color_user_details_flag"])

    def test_change_variables(self):
        pass


    def test_set_values(self):
        self.popup.apply_status.setChecked(False)
        self.popup.set_values()
        self.assertEqual(self.popup.local_variables["status_color_flag"], False)
        self.assertEqual(self.popup.local_variables["status_color_flag"], self.popup.variables["bar_plot_settings"]["status_color_flag"])
        self.assertEqual(tuple(self.popup.local_variables.keys()), self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()), self.variable_keys)


if __name__ == "__main__":
    unittest.main()
