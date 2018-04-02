import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication
from core.utils import get_default_config_path
from gui.gui_utils import colours
from gui.popups.ScatterPlotPopup import ScatterPlotPopup
from core.fslibs.Variables import Variables

app = QApplication(sys.argv)


class Test_ScatterPlotPopup(unittest.TestCase):

    def setUp(self):
        """ Create the popup"""

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["cs_scatter_settings"]
        fin.close()

        self.popup = ScatterPlotPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())

    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.cs_scatter_cols_page.field.value(),
                         self.defaults["cols_page"])
        self.assertEqual(self.popup.cs_scatter_rows_page.field.value(),
                         self.defaults["rows_page"])
        self.assertEqual(self.popup.cs_scatter_x_label.field.text(),
                         self.defaults["x_label"])
        self.assertEqual(self.popup.cs_scatter_y_label.field.text(),
                         self.defaults["y_label"])
        self.assertEqual(self.popup.cs_scatter_mksize.field.value(),
                         self.defaults["mksize"])
        self.assertEqual(self.popup.cs_scatter_scale.field.value(),
                         self.defaults["scale"])
        self.assertEqual(self.popup.cs_scatter_mk_type.fields.currentText(),
                         self.defaults["mk_type"])
        self.assertEqual(
            colours.get(self.popup.cs_scatter_mk_start_color.fields.currentText()),
            self.defaults["mk_start_color"])
        self.assertEqual(
            colours.get(self.popup.cs_scatter_mk_end_color.fields.currentText()),
            self.defaults["mk_end_color"])
        self.assertEqual(self.popup.cs_scatter_markers.field.text(),
                         ','.join(self.defaults["markers"]))
        self.assertEqual(self.popup.cs_scatter_mk_color.field.text(),
                         ','.join(self.defaults["mk_color"]))
        self.assertEqual(self.popup.cs_scatter_mk_edgecolors.field.text(),
                         ','.join(self.defaults["mk_edgecolors"]))
        self.assertEqual(
            self.popup.cs_scatter_mk_missing_color.fields.currentText(),
            self.defaults["mk_missing_color"])
        self.assertEqual(self.popup.cs_scatter_hide_missing.isChecked(),
                         self.defaults["hide_missing"])

    def test_set_values(self):
        self.popup.cs_scatter_cols_page.setValue(6)
        self.popup.cs_scatter_rows_page.setValue(8)
        self.popup.cs_scatter_x_label.setText('x label')
        self.popup.cs_scatter_y_label.setText('y label')
        self.popup.cs_scatter_mksize.setValue(25)
        self.popup.cs_scatter_scale.setValue(0.05)
        self.popup.cs_scatter_mk_type.select("shape")

        self.popup.cs_scatter_mk_start_color.select("gold")
        self.popup.cs_scatter_mk_end_color.select("white")
        self.popup.cs_scatter_markers.setText("^,>,v,<,s,p,h,8")
        self.popup.cs_scatter_mk_color.setText("blue")
        self.popup.cs_scatter_mk_edgecolors.field.setText("red,blue")
        self.popup.cs_scatter_mk_missing_color.select("orange")
        self.popup.cs_scatter_hide_missing.setChecked(True)

        self.popup.set_values()

        self.assertEqual(self.popup.cs_scatter_cols_page.field.value(), 6)
        self.assertEqual(self.popup.cs_scatter_rows_page.field.value(), 8)
        self.assertEqual(self.popup.cs_scatter_x_label.field.text(), "x label")
        self.assertEqual(self.popup.cs_scatter_y_label.field.text(), "y label")
        self.assertEqual(self.popup.cs_scatter_mksize.field.value(), 25)
        self.assertEqual(self.popup.cs_scatter_scale.field.value(), 0.05)
        self.assertEqual(self.popup.cs_scatter_mk_type.fields.currentText(),
                         "shape")
        self.assertEqual(
            self.popup.cs_scatter_mk_start_color.fields.currentText(), "gold")
        self.assertEqual(
            self.popup.cs_scatter_mk_end_color.fields.currentText(), "white")
        self.assertEqual(self.popup.cs_scatter_markers.field.text(),
                         "^,>,v,<,s,p,h,8")
        self.assertEqual(self.popup.cs_scatter_mk_color.field.text(), "blue")
        self.assertEqual(self.popup.cs_scatter_mk_edgecolors.field.text(),
                         "red,blue")
        self.assertEqual(
            self.popup.cs_scatter_mk_missing_color.fields.currentText(), "orange")
        self.assertEqual(self.popup.cs_scatter_hide_missing.isChecked(), True)

        self.assertEqual(self.popup.cs_scatter_cols_page.field.value(),
                         self.popup.variables["cs_scatter_settings"][
                             "cols_page"])
        self.assertEqual(self.popup.cs_scatter_rows_page.field.value(),
                         self.popup.variables["cs_scatter_settings"][
                             "rows_page"])
        self.assertEqual(self.popup.cs_scatter_x_label.field.text(),
                         self.popup.variables["cs_scatter_settings"][
                             "x_label"])
        self.assertEqual(self.popup.cs_scatter_y_label.field.text(),
                         self.popup.variables["cs_scatter_settings"][
                             "y_label"])
        self.assertEqual(self.popup.cs_scatter_mksize.field.value(),
                         self.popup.variables["cs_scatter_settings"]["mksize"])
        self.assertEqual(self.popup.cs_scatter_scale.field.value(),
                         self.popup.variables["cs_scatter_settings"]["scale"])
        self.assertEqual(self.popup.cs_scatter_mk_type.fields.currentText(),
                         self.popup.variables["cs_scatter_settings"][
                             "mk_type"])

        self.assertEqual(
            colours.get(self.popup.cs_scatter_mk_start_color.fields.currentText()),
            self.popup.variables["cs_scatter_settings"]["mk_start_color"])
        self.assertEqual(
            colours.get(self.popup.cs_scatter_mk_end_color.fields.currentText()),
            self.popup.variables["cs_scatter_settings"]["mk_end_color"])
        self.assertEqual(self.popup.cs_scatter_markers.field.text(), ','.join(
            self.popup.variables["cs_scatter_settings"]["markers"]))
        self.assertEqual(self.popup.cs_scatter_mk_color.field.text(), ','.join(
            self.popup.variables["cs_scatter_settings"]["mk_color"]))
        self.assertEqual(self.popup.cs_scatter_mk_edgecolors.field.text(),
                         ','.join(self.popup.variables["cs_scatter_settings"][
                                      "mk_edgecolors"]))
        self.assertEqual(
            self.popup.cs_scatter_mk_missing_color.fields.currentText(),
            self.popup.variables["cs_scatter_settings"]["mk_missing_color"])
        self.assertEqual(self.popup.cs_scatter_hide_missing.isChecked(),
                         self.popup.variables["cs_scatter_settings"][
                             "hide_missing"])

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

    def test_values_not_set(self):
        self.popup.cs_scatter_cols_page.setValue(6)
        self.popup.cs_scatter_rows_page.setValue(8)
        self.popup.cs_scatter_x_label.setText('x label')
        self.popup.cs_scatter_y_label.setText('y label')
        self.popup.cs_scatter_mksize.setValue(25)
        self.popup.cs_scatter_scale.setValue(0.05)
        self.popup.cs_scatter_mk_type.select("shape")

        self.popup.cs_scatter_mk_start_color.select("gold")
        self.popup.cs_scatter_mk_end_color.select("white")
        self.popup.cs_scatter_markers.setText("^,>,v,<,s,p,h,8")
        self.popup.cs_scatter_mk_color.setText("blue")
        self.popup.cs_scatter_mk_edgecolors.field.setText("red, blue")
        self.popup.cs_scatter_mk_missing_color.select("orange")
        self.popup.cs_scatter_hide_missing.setChecked(True)

        self.assertEqual(self.popup.cs_scatter_cols_page.field.value(), 6)
        self.assertEqual(self.popup.cs_scatter_rows_page.field.value(), 8)
        self.assertEqual(self.popup.cs_scatter_x_label.field.text(), "x label")
        self.assertEqual(self.popup.cs_scatter_y_label.field.text(), "y label")
        self.assertEqual(self.popup.cs_scatter_mksize.field.value(), 25)
        self.assertEqual(self.popup.cs_scatter_scale.field.value(), 0.05)
        self.assertEqual(self.popup.cs_scatter_mk_type.fields.currentText(),
                         "shape")

        self.assertEqual(
            self.popup.cs_scatter_mk_start_color.fields.currentText(), "gold")
        self.assertEqual(
            self.popup.cs_scatter_mk_end_color.fields.currentText(), "white")
        self.assertEqual(self.popup.cs_scatter_markers.field.text(),
                         "^,>,v,<,s,p,h,8")
        self.assertEqual(self.popup.cs_scatter_mk_color.field.text(), "blue")
        self.assertEqual(self.popup.cs_scatter_mk_edgecolors.field.text(),
                         "red, blue")
        self.assertEqual(
            self.popup.cs_scatter_mk_missing_color.fields.currentText(), "orange")
        self.assertEqual(self.popup.cs_scatter_hide_missing.isChecked(), True)

        self.assertNotEqual(self.popup.cs_scatter_cols_page.field.value(),
                            self.popup.variables["cs_scatter_settings"][
                                "cols_page"])
        self.assertNotEqual(self.popup.cs_scatter_rows_page.field.value(),
                            self.popup.variables["cs_scatter_settings"][
                                "rows_page"])
        self.assertNotEqual(self.popup.cs_scatter_x_label.field.text(),
                            self.popup.variables["cs_scatter_settings"][
                                "x_label"])
        self.assertNotEqual(self.popup.cs_scatter_y_label.field.text(),
                            self.popup.variables["cs_scatter_settings"][
                                "y_label"])
        self.assertNotEqual(self.popup.cs_scatter_mksize.field.value(),
                            self.popup.variables["cs_scatter_settings"][
                                "mksize"])
        self.assertNotEqual(self.popup.cs_scatter_scale.field.value(),
                            self.popup.variables["cs_scatter_settings"][
                                "scale"])
        self.assertNotEqual(self.popup.cs_scatter_mk_type.fields.currentText(),
                            self.popup.variables["cs_scatter_settings"][
                                "mk_type"])

        self.assertNotEqual(
            self.popup.cs_scatter_mk_start_color.fields.currentText(),
            self.popup.variables["cs_scatter_settings"]["mk_start_color"])
        self.assertNotEqual(
            self.popup.cs_scatter_mk_end_color.fields.currentText(),
            self.popup.variables["cs_scatter_settings"]["mk_end_color"])
        self.assertNotEqual(self.popup.cs_scatter_markers.field.text(),
                            ','.join(
                                self.popup.variables["cs_scatter_settings"][
                                    "markers"]))
        self.assertNotEqual(self.popup.cs_scatter_mk_color.field.text(),
                            ','.join(
                                self.popup.variables["cs_scatter_settings"][
                                    "mk_color"]))
        self.assertNotEqual(self.popup.cs_scatter_mk_edgecolors.field.text(),
                            ','.join(
                                self.popup.variables["cs_scatter_settings"][
                                    "mk_edgecolors"]))
        self.assertNotEqual(
            self.popup.cs_scatter_mk_missing_color.fields.currentText(),
            self.popup.variables["cs_scatter_settings"]["mk_missing_color"])
        self.assertNotEqual(self.popup.cs_scatter_hide_missing.isChecked(),
                            self.popup.variables["cs_scatter_settings"][
                                "hide_missing"])


if __name__ == "__main__":
    unittest.main()
