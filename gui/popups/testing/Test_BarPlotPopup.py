import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication

from gui.popups.BarPlotPopup import BarPlotPopup
from core.utils import get_default_config_path
from core.fslibs.Variables import Variables

app = QApplication(sys.argv)


class Test_BarPlotPopup(unittest.TestCase):

    def setUp(self):
        """ Create the popup"""
        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["bar_plot_settings"]
        fin.close()

        self.popup = BarPlotPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())

    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.apply_status.isChecked(),
                         self.defaults["status_color_flag"])
        self.assertEqual(self.popup.meas_bar_colour.fields.currentText(),
                         self.defaults["measured_color"])
        self.assertEqual(self.popup.missing_bar_colour.fields.currentText(),
                         self.defaults["missing_color"])
        self.assertEqual(self.popup.unassigned_bar_colour.fields.currentText(),
                         self.defaults["unassigned_color"])
        self.assertEqual(self.popup.bar_width.field.value(),
                         self.defaults["bar_width"])
        self.assertEqual(self.popup.bar_alpha.field.value(),
                         self.defaults["bar_alpha"])
        self.assertEqual(self.popup.bar_linewidth.field.value(),
                         self.defaults["bar_linewidth"])
        self.assertEqual(self.popup.bar_threshold.isChecked(),
                         self.defaults["threshold_flag"])
        self.assertEqual(self.popup.bar_threshold_colour.fields.currentText(),
                         self.defaults["threshold_color"])
        self.assertEqual(self.popup.bar_threshold_linewidth.field.value(),
                         self.defaults["threshold_linewidth"])
        self.assertEqual(self.popup.bar_threshold_alpha.field.value(),
                         self.defaults["threshold_alpha"])
        self.assertEqual(self.popup.user_mark_font_size.field.value(),
                         self.defaults["mark_fontsize"])
        self.assertEqual(self.popup.markProlines.isChecked(),
                         self.defaults["mark_prolines_flag"])
        self.assertEqual(self.popup.proline_marker.field.text(),
                         self.defaults["mark_prolines_symbol"])
        self.assertEqual(self.popup.user_details.isChecked(),
                         self.defaults["mark_user_details_flag"])
        self.assertEqual(self.popup.colour_user_details.isChecked(),
                         self.defaults["color_user_details_flag"])

    def test_set_values(self):
        self.popup.apply_status.setChecked(False)
        self.popup.meas_bar_colour.select('peru')
        self.popup.missing_bar_colour.select('bisque')
        self.popup.unassigned_bar_colour.select('white')
        self.popup.bar_width.setValue(0.6)
        self.popup.bar_alpha.setValue(0.5)
        self.popup.bar_linewidth.setValue(15)
        self.popup.bar_threshold.setChecked(False)
        self.popup.bar_threshold_colour.select('yellow')
        self.popup.bar_threshold_linewidth.setValue(82)
        self.popup.bar_threshold_alpha.setValue(0.2)
        self.popup.user_mark_font_size.setValue(16)
        self.popup.markProlines.setChecked(False)
        self.popup.proline_marker.field.setText('Proline')
        self.popup.user_details.setChecked(True)
        self.popup.colour_user_details.setChecked(True)
        self.popup.set_values()

        self.assertEqual(self.popup.apply_status.isChecked(), False)
        self.assertEqual(self.popup.variables["bar_plot_settings"]
                         ["status_color_flag"], False)
        self.assertEqual(self.popup.meas_bar_colour.fields.currentText(),
                         'peru')
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "measured_color"], 'peru')
        self.assertEqual(self.popup.missing_bar_colour.fields.currentText(),
                         'bisque')
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "missing_color"], 'bisque')
        self.assertEqual(self.popup.unassigned_bar_colour.fields
                         .currentText(), 'white')
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "unassigned_color"], 'white')
        self.assertEqual(self.popup.bar_width.field.value(), 0.6)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "bar_width"], 0.6)
        self.assertEqual(self.popup.bar_alpha.field.value(), 0.5)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "bar_alpha"], 0.5)
        self.assertEqual(self.popup.bar_linewidth.field.value(), 15)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "bar_linewidth"], 15)
        self.assertEqual(self.popup.bar_threshold.isChecked(), False)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "threshold_flag"], False)
        self.assertEqual(self.popup.bar_threshold_colour.fields.currentText(),
                         'yellow')
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "threshold_color"], 'yellow')
        self.assertEqual(self.popup.bar_threshold_linewidth.field.value(), 82)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "threshold_linewidth"], 82)
        self.assertEqual(self.popup.bar_threshold_alpha.field.value(), 0.2)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "threshold_alpha"], 0.2)
        self.assertEqual(self.popup.user_mark_font_size.field.value(), 16)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "mark_fontsize"], 16)
        self.assertEqual(self.popup.markProlines.isChecked(), False)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "mark_prolines_flag"], False)
        self.assertEqual(self.popup.proline_marker.field.text(), 'Proline')
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "mark_prolines_symbol"], 'Proline')
        self.assertEqual(self.popup.user_details.isChecked(), True)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "mark_user_details_flag"], True)
        self.assertEqual(self.popup.colour_user_details.isChecked(), True)
        self.assertEqual(self.popup.variables["bar_plot_settings"][
                             "color_user_details_flag"], True)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

    def test_values_not_set(self):
        self.popup.apply_status.setChecked(True)
        self.popup.meas_bar_colour.select('peru')
        self.popup.missing_bar_colour.select('bisque')
        self.popup.unassigned_bar_colour.select('white')
        self.popup.bar_width.setValue(0.6)
        self.popup.bar_alpha.setValue(0.5)
        self.popup.bar_linewidth.setValue(15)
        self.popup.bar_threshold.setChecked(False)
        self.popup.bar_threshold_colour.select('yellow')
        self.popup.bar_threshold_linewidth.setValue(82)
        self.popup.bar_threshold_alpha.setValue(0.2)
        self.popup.user_mark_font_size.setValue(16)
        self.popup.markProlines.setChecked(False)
        self.popup.proline_marker.field.setText('Proline')
        self.popup.user_details.setChecked(True)
        self.popup.colour_user_details.setChecked(True)

        self.assertNotEqual(self.popup.variables["bar_plot_settings"]
                            ["status_color_flag"], False)
        self.assertEqual(self.popup.meas_bar_colour.fields.currentText(),
                         'peru')
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "measured_color"], 'peru')
        self.assertEqual(self.popup.missing_bar_colour.fields.currentText(),
                         'bisque')
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "missing_color"], 'bisque')
        self.assertEqual(self.popup.unassigned_bar_colour.fields
                         .currentText(), 'white')
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "unassigned_color"], 'white')
        self.assertEqual(self.popup.bar_width.field.value(), 0.6)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "bar_width"], 0.6)
        self.assertEqual(self.popup.bar_alpha.field.value(), 0.5)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "bar_alpha"], 0.5)
        self.assertEqual(self.popup.bar_linewidth.field.value(), 15)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "bar_linewidth"], 15)
        self.assertEqual(self.popup.bar_threshold.isChecked(), False)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "threshold_flag"], False)
        self.assertEqual(self.popup.bar_threshold_colour.fields.currentText(),
                         'yellow')
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "threshold_color"], 'yellow')
        self.assertEqual(self.popup.bar_threshold_linewidth.field.value(), 82)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                             "threshold_linewidth"], 82)
        self.assertEqual(self.popup.bar_threshold_alpha.field.value(), 0.2)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                             "threshold_alpha"], 0.2)
        self.assertEqual(self.popup.user_mark_font_size.field.value(), 16)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "mark_fontsize"], 16)
        self.assertEqual(self.popup.markProlines.isChecked(), False)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "mark_prolines_flag"], False)
        self.assertEqual(self.popup.proline_marker.field.text(), 'Proline')
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "mark_prolines_symbol"], 'Proline')
        self.assertEqual(self.popup.user_details.isChecked(), True)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "mark_user_details_flag"], True)
        self.assertEqual(self.popup.colour_user_details.isChecked(), True)
        self.assertNotEqual(self.popup.variables["bar_plot_settings"][
                                "color_user_details_flag"], True)

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)


if __name__ == "__main__":
    unittest.main()
