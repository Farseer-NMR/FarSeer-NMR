import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication
from core.utils import get_default_config_path

from gui.popups.ResidueEvolution import ResidueEvolutionPopup

app = QApplication(sys.argv)

from core.fslibs.Variables import Variables

class Test_ResidueEvolutionPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''
        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["res_evo_settings"]
        fin.close()

        self.popup = ResidueEvolutionPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())


    def test_defaults(self):
        """Test popup reads and sets default variables"""
        self.assertEqual(self.popup.res_evo_cols.field.value(),
                         self.defaults["cols_page"])
        self.assertEqual(self.popup.res_evo_rows.field.value(),
                         self.defaults["rows_page"])
        self.assertEqual(self.popup.res_evo_set_x_values.isChecked(),
                         self.defaults["set_x_values"])
        self.assertEqual(self.popup.res_evo_x_ticks_nbins.field.value(),
                         self.defaults["x_ticks_nbins"])
        self.assertEqual(self.popup.res_evo_x_label.field.text(),
                         self.defaults["x_label"])
        self.assertEqual(
            self.popup.res_evo_plot_line_style.fields.currentText(),
            self.defaults["line_style"])
        self.assertEqual(self.popup.res_evo_plot_line_width.field.value(),
                         self.defaults["line_width"])
        self.assertEqual(self.popup.res_evo_line_color.fields.currentText(),
                         self.defaults["line_color"])
        self.assertEqual(self.popup.res_evo_marker_color.fields.currentText(),
                         self.defaults["marker_color"])
        self.assertEqual(
            self.popup.res_evo_plot_marker_style.fields.currentText(),
            self.defaults["marker_style"])
        self.assertEqual(self.popup.res_evo_plot_marker_size.field.value(),
                         self.defaults["marker_size"])
        self.assertEqual(self.popup.res_evo_plot_fill_between.isChecked(),
                         self.defaults["fill_between"])
        self.assertEqual(
            self.popup.res_evo_plot_fill_colour.fields.currentText(),
            self.defaults["fill_color"])
        self.assertEqual(self.popup.res_evo_fill_alpha.field.value(),
                         self.defaults["fill_alpha"])
        self.assertEqual(
            self.popup.res_evo_fit_line_colour.fields.currentText(),
            self.defaults["fit_line_color"])
        self.assertEqual(self.popup.res_evo_fit_line_width.field.value(),
                         self.defaults["fit_line_width"])
        self.assertEqual(
            self.popup.res_evo_fit_line_style.fields.currentText(),
            self.defaults["fit_line_style"])


    def test_set_values(self):
        self.popup.res_evo_cols.setValue(8)
        self.popup.res_evo_rows.setValue(5)
        self.popup.res_evo_set_x_values.setChecked(True)
        self.popup.res_evo_x_ticks_nbins.setValue(8)
        self.popup.res_evo_x_label.setText("stuff in tube")
        self.popup.res_evo_plot_line_style.select(":")
        self.popup.res_evo_plot_line_width.setValue(5)
        self.popup.res_evo_line_color.select("magenta")
        self.popup.res_evo_marker_color.select("orange")
        self.popup.res_evo_plot_marker_style.select("-")
        self.popup.res_evo_plot_marker_size.setValue(5)
        self.popup.res_evo_plot_fill_between.setChecked(False)
        self.popup.res_evo_plot_fill_colour.select("red")
        self.popup.res_evo_fill_alpha.setValue(0.4)
        self.popup.res_evo_fit_line_colour.select("brown")
        self.popup.res_evo_fit_line_width.setValue(8)
        self.popup.res_evo_fit_line_style.select(":")

        self.popup.set_values()

        self.assertEqual(self.popup.res_evo_cols.field.value(), 8)
        self.assertEqual(self.popup.res_evo_rows.field.value(), 5)
        self.assertEqual(self.popup.res_evo_set_x_values.isChecked(), True)
        self.assertEqual(self.popup.res_evo_x_ticks_nbins.field.value(), 8)
        self.assertEqual(self.popup.res_evo_x_label.field.text(),
                         "stuff in tube")
        self.assertEqual(
            self.popup.res_evo_plot_line_style.fields.currentText(), ":")
        self.assertEqual(self.popup.res_evo_plot_line_width.field.value(), 5)
        self.assertEqual(self.popup.res_evo_line_color.fields.currentText(),
                         "magenta")
        self.assertEqual(self.popup.res_evo_marker_color.fields.currentText(),
                         "orange")
        self.assertEqual(
            self.popup.res_evo_plot_marker_style.fields.currentText(), "-")
        self.assertEqual(self.popup.res_evo_plot_marker_size.field.value(), 5)
        self.assertEqual(self.popup.res_evo_plot_fill_between.isChecked(),
                         False)
        self.assertEqual(
            self.popup.res_evo_plot_fill_colour.fields.currentText(), "red")
        self.assertEqual(self.popup.res_evo_fill_alpha.field.value(), 0.4)
        self.assertEqual(
            self.popup.res_evo_fit_line_colour.fields.currentText(), "brown")
        self.assertEqual(self.popup.res_evo_fit_line_width.field.value(), 8)
        self.assertEqual(
            self.popup.res_evo_fit_line_style.fields.currentText(), ":")

        self.assertEqual(self.popup.res_evo_cols.field.value(),
                         self.popup.variables["res_evo_settings"]["cols_page"])
        self.assertEqual(self.popup.res_evo_rows.field.value(),
                         self.popup.variables["res_evo_settings"]["rows_page"])
        self.assertEqual(self.popup.res_evo_set_x_values.isChecked(),
                         self.popup.variables["res_evo_settings"][
                             "set_x_values"])
        self.assertEqual(self.popup.res_evo_x_ticks_nbins.field.value(),
                         self.popup.variables["res_evo_settings"][
                             "x_ticks_nbins"])
        self.assertEqual(self.popup.res_evo_x_label.field.text(),
                         self.popup.variables["res_evo_settings"]["x_label"])
        self.assertEqual(
            self.popup.res_evo_plot_line_style.fields.currentText(),
            self.popup.variables["res_evo_settings"]["line_style"])
        self.assertEqual(self.popup.res_evo_plot_line_width.field.value(),
                         self.popup.variables["res_evo_settings"][
                             "line_width"])
        self.assertEqual(self.popup.res_evo_line_color.fields.currentText(),
                         self.popup.variables["res_evo_settings"][
                             "line_color"])
        self.assertEqual(self.popup.res_evo_marker_color.fields.currentText(),
                         self.popup.variables["res_evo_settings"][
                             "marker_color"])
        self.assertEqual(
            self.popup.res_evo_plot_marker_style.fields.currentText(),
            self.popup.variables["res_evo_settings"]["marker_style"])
        self.assertEqual(self.popup.res_evo_plot_marker_size.field.value(),
                         self.popup.variables["res_evo_settings"][
                             "marker_size"])
        self.assertEqual(self.popup.res_evo_plot_fill_between.isChecked(),
                         self.popup.variables["res_evo_settings"][
                             "fill_between"])
        self.assertEqual(
            self.popup.res_evo_plot_fill_colour.fields.currentText(),
            self.popup.variables["res_evo_settings"]["fill_color"])
        self.assertEqual(self.popup.res_evo_fill_alpha.field.value(),
                         self.popup.variables["res_evo_settings"][
                             "fill_alpha"])
        self.assertEqual(
            self.popup.res_evo_fit_line_colour.fields.currentText(),
            self.popup.variables["res_evo_settings"]["fit_line_color"])
        self.assertEqual(self.popup.res_evo_fit_line_width.field.value(),
                         self.popup.variables["res_evo_settings"][
                             "fit_line_width"])
        self.assertEqual(
            self.popup.res_evo_fit_line_style.fields.currentText(),
            self.popup.variables["res_evo_settings"]["fit_line_style"])

        self.assertEqual(tuple(self.popup.local_variables.keys()), self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()), self.variable_keys)


    def test_values_not_set(self):

        self.popup.res_evo_cols.setValue(8)
        self.popup.res_evo_rows.setValue(5)
        self.popup.res_evo_set_x_values.setChecked(True)
        self.popup.res_evo_x_ticks_nbins.setValue(8)
        self.popup.res_evo_x_label.setText("stuff in tube")
        self.popup.res_evo_plot_line_style.select(":")
        self.popup.res_evo_plot_line_width.setValue(5)
        self.popup.res_evo_line_color.select("magenta")
        self.popup.res_evo_marker_color.select("orange")
        self.popup.res_evo_plot_marker_style.select("-")
        self.popup.res_evo_plot_marker_size.setValue(5)
        self.popup.res_evo_plot_fill_between.setChecked(False)
        self.popup.res_evo_plot_fill_colour.select("red")
        self.popup.res_evo_fill_alpha.setValue(0.4)
        self.popup.res_evo_fit_line_colour.select("brown")
        self.popup.res_evo_fit_line_width.setValue(8)
        self.popup.res_evo_fit_line_style.select(":")

        self.assertEqual(self.popup.res_evo_cols.field.value(), 8)
        self.assertEqual(self.popup.res_evo_rows.field.value(), 5)
        self.assertEqual(self.popup.res_evo_set_x_values.isChecked(), True)
        self.assertEqual(self.popup.res_evo_x_ticks_nbins.field.value(), 8)
        self.assertEqual(self.popup.res_evo_x_label.field.text(),
                         "stuff in tube")
        self.assertEqual(
            self.popup.res_evo_plot_line_style.fields.currentText(), ":")
        self.assertEqual(self.popup.res_evo_plot_line_width.field.value(), 5)
        self.assertEqual(self.popup.res_evo_line_color.fields.currentText(),
                         "magenta")
        self.assertEqual(self.popup.res_evo_marker_color.fields.currentText(),
                         "orange")
        self.assertEqual(
            self.popup.res_evo_plot_marker_style.fields.currentText(), "-")
        self.assertEqual(self.popup.res_evo_plot_marker_size.field.value(), 5)
        self.assertEqual(self.popup.res_evo_plot_fill_between.isChecked(),
                         False)
        self.assertEqual(
            self.popup.res_evo_plot_fill_colour.fields.currentText(), "red")
        self.assertEqual(self.popup.res_evo_fill_alpha.field.value(), 0.4)
        self.assertEqual(
            self.popup.res_evo_fit_line_colour.fields.currentText(), "brown")
        self.assertEqual(self.popup.res_evo_fit_line_width.field.value(), 8)
        self.assertEqual(
            self.popup.res_evo_fit_line_style.fields.currentText(), ":")

        self.assertNotEqual(self.popup.res_evo_cols.field.value(),
                            self.popup.variables["res_evo_settings"][
                                "cols_page"])
        self.assertNotEqual(self.popup.res_evo_rows.field.value(),
                            self.popup.variables["res_evo_settings"][
                                "rows_page"])
        self.assertNotEqual(self.popup.res_evo_set_x_values.isChecked(),
                            self.popup.variables["res_evo_settings"][
                                "set_x_values"])
        self.assertNotEqual(self.popup.res_evo_x_ticks_nbins.field.value(),
                            self.popup.variables["res_evo_settings"][
                                "x_ticks_nbins"])
        self.assertNotEqual(self.popup.res_evo_x_label.field.text(),
                            self.popup.variables["res_evo_settings"][
                                "x_label"])
        self.assertNotEqual(
            self.popup.res_evo_plot_line_style.fields.currentText(),
            self.popup.variables["res_evo_settings"]["line_style"])
        self.assertNotEqual(self.popup.res_evo_plot_line_width.field.value(),
                            self.popup.variables["res_evo_settings"][
                                "line_width"])
        self.assertNotEqual(self.popup.res_evo_line_color.fields.currentText(),
                            self.popup.variables["res_evo_settings"][
                                "line_color"])
        self.assertNotEqual(
            self.popup.res_evo_marker_color.fields.currentText(),
            self.popup.variables["res_evo_settings"]["marker_color"])
        self.assertNotEqual(
            self.popup.res_evo_plot_marker_style.fields.currentText(),
            self.popup.variables["res_evo_settings"]["marker_style"])
        self.assertNotEqual(self.popup.res_evo_plot_marker_size.field.value(),
                            self.popup.variables["res_evo_settings"][
                                "marker_size"])
        self.assertNotEqual(self.popup.res_evo_plot_fill_between.isChecked(),
                            self.popup.variables["res_evo_settings"][
                                "fill_between"])
        self.assertNotEqual(
            self.popup.res_evo_plot_fill_colour.fields.currentText(),
            self.popup.variables["res_evo_settings"]["fill_color"])
        self.assertNotEqual(self.popup.res_evo_fill_alpha.field.value(),
                            self.popup.variables["res_evo_settings"][
                                "fill_alpha"])
        self.assertNotEqual(
            self.popup.res_evo_fit_line_colour.fields.currentText(),
            self.popup.variables["res_evo_settings"]["fit_line_color"])
        self.assertNotEqual(self.popup.res_evo_fit_line_width.field.value(),
                            self.popup.variables["res_evo_settings"][
                                "fit_line_width"])
        self.assertNotEqual(
            self.popup.res_evo_fit_line_style.fields.currentText(),
            self.popup.variables["res_evo_settings"]["fit_line_style"])

if __name__ == "__main__":
    unittest.main()