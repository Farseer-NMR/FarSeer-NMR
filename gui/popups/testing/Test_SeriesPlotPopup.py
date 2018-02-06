import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication
from core.utils import get_default_config_path

from gui.popups.SeriesPlotPopup import SeriesPlotPopup


app = QApplication(sys.argv)

from core.fslibs.Variables import Variables

class Test_SeriesPlotPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["series_plot_settings"]
        fin.close()

        self.popup = SeriesPlotPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())


    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.series_subtitle_fn.fields.currentText(),
                         self.defaults["subtitle_fn"])
        self.assertEqual(self.popup.series_subtitle_fs.field.value(),
                         self.defaults["subtitle_fs"])
        self.assertEqual(self.popup.series_subtitle_weight.fields.currentText(),
                         self.defaults["subtitle_weight"])
        self.assertEqual(self.popup.series_subtitle_pad.field.value(),
                         self.defaults["subtitle_pad"])
        self.assertEqual(self.popup.series_x_label_fn.fields.currentText(),
                         self.defaults["x_label_fn"])
        self.assertEqual(self.popup.series_x_label_fs.field.value(),
                         self.defaults["x_label_fs"])
        self.assertEqual(self.popup.series_x_label_pad.field.value(),
                         self.defaults["x_label_pad"])
        self.assertEqual(self.popup.series_x_label_weight.fields.currentText(),
                         self.defaults["x_label_weight"])
        self.assertEqual(self.popup.series_y_label_fn.fields.currentText(),
                         self.defaults["y_label_fn"])
        self.assertEqual(self.popup.series_y_label_fs.field.value(),
                         self.defaults["y_label_fs"])
        self.assertEqual(self.popup.series_y_label_pad.field.value(),
                         self.defaults["y_label_pad"])
        self.assertEqual(self.popup.series_y_label_weight.fields.currentText(),
                         self.defaults["y_label_weight"])
        self.assertEqual(self.popup.series_x_ticks_pad.field.value(),
                         self.defaults["x_ticks_pad"])
        self.assertEqual(self.popup.series_x_ticks_len.field.value(),
                         self.defaults["x_ticks_len"])

        self.assertEqual(self.popup.series_y_ticks_fn.fields.currentText(),
                         self.defaults["y_ticks_fn"])
        self.assertEqual(self.popup.series_y_ticks_fs.field.value(),
                         self.defaults["y_ticks_fs"])
        self.assertEqual(self.popup.series_y_ticks_rot.field.value(),
                         self.defaults["y_ticks_rot"])
        self.assertEqual(self.popup.series_y_ticks_pad.field.value(),
                         self.defaults["y_ticks_pad"])
        self.assertEqual(self.popup.series_y_ticks_weight.fields.currentText(),
                         self.defaults["y_ticks_weight"])
        self.assertEqual(self.popup.series_y_ticks_len.field.value(),
                         self.defaults["y_ticks_len"])
        self.assertEqual(self.popup.series_y_grid_flag.isChecked(),
                         self.defaults["y_grid_flag"])
        self.assertEqual(self.popup.series_y_grid_color.fields.currentText(),
                         self.defaults["y_grid_color"])
        self.assertEqual(self.popup.series_y_grid_linestyle.fields.currentText(),
                         self.defaults["y_grid_linestyle"])
        self.assertEqual(self.popup.series_y_grid_linewidth.field.value(),
                         self.defaults["y_grid_linewidth"])
        self.assertEqual(self.popup.series_y_grid_alpha.field.value(),
                         self.defaults["y_grid_alpha"])

        self.assertEqual(self.popup.theo_pre_color.fields.currentText(),
                         self.defaults["theo_pre_color"])
        self.assertEqual(self.popup.theo_pre_lw.field.value(),
                         self.defaults["theo_pre_lw"])
        self.assertEqual(self.popup.tag_cartoon_color.fields.currentText(),
                         self.defaults["tag_cartoon_color"])
        self.assertEqual(self.popup.tag_cartoon_lw.field.value(),
                         self.defaults["tag_cartoon_lw"])
        self.assertEqual(self.popup.tag_cartoon_ls.fields.currentText(),
                         self.defaults["tag_cartoon_ls"])

    def test_set_values(self):
        self.popup.series_subtitle_fn.select("Verdana")
        self.popup.series_subtitle_fs.setValue(10)
        self.popup.series_subtitle_weight.select("bold")
        self.popup.series_subtitle_pad.setValue(0.78)
        self.popup.series_x_label_fn.select("Verdana")
        self.popup.series_x_label_fs.setValue(10)
        self.popup.series_x_label_pad.setValue(3)
        self.popup.series_x_label_weight.select("semibold")
        self.popup.series_y_label_fn.select("Verdana")
        self.popup.series_y_label_fs.setValue(15)
        self.popup.series_y_label_pad.setValue(8)
        self.popup.series_y_label_weight.select("semibold")
        self.popup.series_x_ticks_pad.setValue(52.8)
        self.popup.series_x_ticks_len.setValue(1)

        self.popup.series_y_ticks_fn.select("Verdana")
        self.popup.series_y_ticks_fs.setValue(81)
        self.popup.series_y_ticks_rot.setValue(45)
        self.popup.series_y_ticks_pad.setValue(8)
        self.popup.series_y_ticks_weight.select("bold")
        self.popup.series_y_ticks_len.setValue(1)
        self.popup.series_y_grid_flag.setChecked(False)
        self.popup.series_y_grid_color.select("red")
        self.popup.series_y_grid_linestyle.select(":")
        self.popup.series_y_grid_linewidth.setValue(0.5)
        self.popup.series_y_grid_alpha.setValue(0.7)

        self.popup.theo_pre_color.select("white")
        self.popup.theo_pre_lw.setValue(0.8)
        self.popup.tag_cartoon_color.select("bisque")
        self.popup.tag_cartoon_lw.setValue(0.8)
        self.popup.tag_cartoon_ls.select("-")

        self.popup.set_values()

        self.assertEqual(self.popup.series_subtitle_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.series_subtitle_fs.field.value(), 10)
        self.assertEqual(
            self.popup.series_subtitle_weight.fields.currentText(), "bold")
        self.assertEqual(self.popup.series_subtitle_pad.field.value(), 0.78)
        self.assertEqual(self.popup.series_x_label_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.series_x_label_fs.field.value(), 10)
        self.assertEqual(self.popup.series_x_label_pad.field.value(), 3)
        self.assertEqual(self.popup.series_x_label_weight.fields.currentText(),
                         "semibold")
        self.assertEqual(self.popup.series_y_label_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.series_y_label_fs.field.value(), 15)
        self.assertEqual(self.popup.series_y_label_pad.field.value(), 8)
        self.assertEqual(self.popup.series_y_label_weight.fields.currentText(),
                         "semibold")
        self.assertEqual(self.popup.series_x_ticks_pad.field.value(), 52.8)
        self.assertEqual(self.popup.series_x_ticks_len.field.value(), 1)

        self.assertEqual(self.popup.series_y_ticks_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.series_y_ticks_fs.field.value(), 81)
        self.assertEqual(self.popup.series_y_ticks_rot.field.value(), 45)
        self.assertEqual(self.popup.series_y_ticks_pad.field.value(), 8)
        self.assertEqual(self.popup.series_y_ticks_weight.fields.currentText(),
                         "bold")
        self.assertEqual(self.popup.series_y_ticks_len.field.value(), 1)
        self.assertEqual(self.popup.series_y_grid_flag.isChecked(), False)
        self.assertEqual(self.popup.series_y_grid_color.fields.currentText(),
                         "red")
        self.assertEqual(
            self.popup.series_y_grid_linestyle.fields.currentText(), ":")
        self.assertEqual(self.popup.series_y_grid_linewidth.field.value(), 0.5)
        self.assertEqual(self.popup.series_y_grid_alpha.field.value(), 0.7)

        self.assertEqual(self.popup.theo_pre_color.fields.currentText(),
                         "white")
        self.assertEqual(self.popup.theo_pre_lw.field.value(), 0.8)
        self.assertEqual(self.popup.tag_cartoon_color.fields.currentText(),
                         "bisque")
        self.assertEqual(self.popup.tag_cartoon_lw.field.value(), 0.8)
        self.assertEqual(self.popup.tag_cartoon_ls.fields.currentText(), "-")

        self.assertEqual(self.popup.series_subtitle_fn.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "subtitle_fn"])
        self.assertEqual(self.popup.series_subtitle_fs.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "subtitle_fs"])
        self.assertEqual(
            self.popup.series_subtitle_weight.fields.currentText(),
            self.popup.variables["series_plot_settings"]["subtitle_weight"])
        self.assertEqual(self.popup.series_subtitle_pad.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "subtitle_pad"])
        self.assertEqual(self.popup.series_x_label_fn.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "x_label_fn"])
        self.assertEqual(self.popup.series_x_label_fs.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "x_label_fs"])
        self.assertEqual(self.popup.series_x_label_pad.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "x_label_pad"])
        self.assertEqual(self.popup.series_x_label_weight.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "x_label_weight"])
        self.assertEqual(self.popup.series_y_label_fn.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "y_label_fn"])
        self.assertEqual(self.popup.series_y_label_fs.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "y_label_fs"])
        self.assertEqual(self.popup.series_y_label_pad.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "y_label_pad"])
        self.assertEqual(self.popup.series_y_label_weight.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "y_label_weight"])
        self.assertEqual(self.popup.series_x_ticks_pad.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "x_ticks_pad"])
        self.assertEqual(self.popup.series_x_ticks_len.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "x_ticks_len"])

        self.assertEqual(self.popup.series_y_ticks_fn.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "y_ticks_fn"])
        self.assertEqual(self.popup.series_y_ticks_fs.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "y_ticks_fs"])
        self.assertEqual(self.popup.series_y_ticks_rot.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "y_ticks_rot"])
        self.assertEqual(self.popup.series_y_ticks_pad.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "y_ticks_pad"])
        self.assertEqual(self.popup.series_y_ticks_weight.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "y_ticks_weight"])
        self.assertEqual(self.popup.series_y_ticks_len.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "y_ticks_len"])
        self.assertEqual(self.popup.series_y_grid_flag.isChecked(),
                         self.popup.variables["series_plot_settings"][
                             "y_grid_flag"])
        self.assertEqual(self.popup.series_y_grid_color.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "y_grid_color"])
        self.assertEqual(
            self.popup.series_y_grid_linestyle.fields.currentText(),
            self.popup.variables["series_plot_settings"]["y_grid_linestyle"])
        self.assertEqual(self.popup.series_y_grid_linewidth.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "y_grid_linewidth"])
        self.assertEqual(self.popup.series_y_grid_alpha.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "y_grid_alpha"])

        self.assertEqual(self.popup.theo_pre_color.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "theo_pre_color"])
        self.assertEqual(self.popup.theo_pre_lw.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "theo_pre_lw"])
        self.assertEqual(self.popup.tag_cartoon_color.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "tag_cartoon_color"])
        self.assertEqual(self.popup.tag_cartoon_lw.field.value(),
                         self.popup.variables["series_plot_settings"][
                             "tag_cartoon_lw"])
        self.assertEqual(self.popup.tag_cartoon_ls.fields.currentText(),
                         self.popup.variables["series_plot_settings"][
                             "tag_cartoon_ls"])

        self.assertEqual(tuple(self.popup.local_variables.keys()), self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()), self.variable_keys)


    def test_values_not_set(self):
        self.popup.series_subtitle_fn.select("Verdana")
        self.popup.series_subtitle_fs.setValue(10)
        self.popup.series_subtitle_weight.select("bold")
        self.popup.series_subtitle_pad.setValue(0.78)
        self.popup.series_x_label_fn.select("Verdana")
        self.popup.series_x_label_fs.setValue(10)
        self.popup.series_x_label_pad.setValue(3)
        self.popup.series_x_label_weight.select("semibold")
        self.popup.series_y_label_fn.select("Verdana")
        self.popup.series_y_label_fs.setValue(15)
        self.popup.series_y_label_pad.setValue(8)
        self.popup.series_y_label_weight.select("semibold")
        self.popup.series_x_ticks_pad.setValue(52.8)
        self.popup.series_x_ticks_len.setValue(1)

        self.popup.series_y_ticks_fn.select("Verdana")
        self.popup.series_y_ticks_fs.setValue(81)
        self.popup.series_y_ticks_rot.setValue(45)
        self.popup.series_y_ticks_pad.setValue(8)
        self.popup.series_y_ticks_weight.select("bold")
        self.popup.series_y_ticks_len.setValue(1)
        self.popup.series_y_grid_flag.setChecked(False)
        self.popup.series_y_grid_color.select("red")
        self.popup.series_y_grid_linestyle.select(":")
        self.popup.series_y_grid_linewidth.setValue(0.5)
        self.popup.series_y_grid_alpha.setValue(0.7)

        self.popup.theo_pre_color.select("white")
        self.popup.theo_pre_lw.setValue(0.8)
        self.popup.tag_cartoon_color.select("bisque")
        self.popup.tag_cartoon_lw.setValue(0.8)
        self.popup.tag_cartoon_ls.select("-")

        self.assertEqual(self.popup.series_subtitle_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.series_subtitle_fs.field.value(), 10)
        self.assertEqual(
            self.popup.series_subtitle_weight.fields.currentText(), "bold")
        self.assertEqual(self.popup.series_subtitle_pad.field.value(), 0.78)
        self.assertEqual(self.popup.series_x_label_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.series_x_label_fs.field.value(), 10)
        self.assertEqual(self.popup.series_x_label_pad.field.value(), 3)
        self.assertEqual(self.popup.series_x_label_weight.fields.currentText(),
                         "semibold")
        self.assertEqual(self.popup.series_y_label_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.series_y_label_fs.field.value(), 15)
        self.assertEqual(self.popup.series_y_label_pad.field.value(), 8)
        self.assertEqual(self.popup.series_y_label_weight.fields.currentText(),
                         "semibold")
        self.assertEqual(self.popup.series_x_ticks_pad.field.value(), 52.8)
        self.assertEqual(self.popup.series_x_ticks_len.field.value(), 1)

        self.assertEqual(self.popup.series_y_ticks_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.series_y_ticks_fs.field.value(), 81)
        self.assertEqual(self.popup.series_y_ticks_rot.field.value(), 45)
        self.assertEqual(self.popup.series_y_ticks_pad.field.value(), 8)
        self.assertEqual(self.popup.series_y_ticks_weight.fields.currentText(),
                         "bold")
        self.assertEqual(self.popup.series_y_ticks_len.field.value(), 1)
        self.assertEqual(self.popup.series_y_grid_flag.isChecked(), False)
        self.assertEqual(self.popup.series_y_grid_color.fields.currentText(),
                         "red")
        self.assertEqual(
            self.popup.series_y_grid_linestyle.fields.currentText(), ":")
        self.assertEqual(self.popup.series_y_grid_linewidth.field.value(), 0.5)
        self.assertEqual(self.popup.series_y_grid_alpha.field.value(), 0.7)

        self.assertEqual(self.popup.theo_pre_color.fields.currentText(),
                         "white")
        self.assertEqual(self.popup.theo_pre_lw.field.value(), 0.8)
        self.assertEqual(self.popup.tag_cartoon_color.fields.currentText(),
                         "bisque")
        self.assertEqual(self.popup.tag_cartoon_lw.field.value(), 0.8)
        self.assertEqual(self.popup.tag_cartoon_ls.fields.currentText(), "-")


        self.assertNotEqual(self.popup.series_subtitle_fn.fields.currentText(),
                            self.popup.variables["series_plot_settings"][
                                "subtitle_fn"])
        self.assertNotEqual(self.popup.series_subtitle_fs.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "subtitle_fs"])
        self.assertNotEqual(
            self.popup.series_subtitle_weight.fields.currentText(),
            self.popup.variables["series_plot_settings"]["subtitle_weight"])
        self.assertNotEqual(self.popup.series_subtitle_pad.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "subtitle_pad"])
        self.assertNotEqual(self.popup.series_x_label_fn.fields.currentText(),
                            self.popup.variables["series_plot_settings"][
                                "x_label_fn"])
        self.assertNotEqual(self.popup.series_x_label_fs.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "x_label_fs"])
        self.assertNotEqual(self.popup.series_x_label_pad.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "x_label_pad"])
        self.assertNotEqual(
            self.popup.series_x_label_weight.fields.currentText(),
            self.popup.variables["series_plot_settings"]["x_label_weight"])
        self.assertNotEqual(self.popup.series_y_label_fn.fields.currentText(),
                            self.popup.variables["series_plot_settings"][
                                "y_label_fn"])
        self.assertNotEqual(self.popup.series_y_label_fs.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "y_label_fs"])
        self.assertNotEqual(self.popup.series_y_label_pad.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "y_label_pad"])
        self.assertNotEqual(
            self.popup.series_y_label_weight.fields.currentText(),
            self.popup.variables["series_plot_settings"]["y_label_weight"])
        self.assertNotEqual(self.popup.series_x_ticks_pad.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "x_ticks_pad"])
        self.assertNotEqual(self.popup.series_x_ticks_len.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "x_ticks_len"])

        self.assertNotEqual(self.popup.series_y_ticks_fn.fields.currentText(),
                            self.popup.variables["series_plot_settings"][
                                "y_ticks_fn"])
        self.assertNotEqual(self.popup.series_y_ticks_fs.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "y_ticks_fs"])
        self.assertNotEqual(self.popup.series_y_ticks_rot.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "y_ticks_rot"])
        self.assertNotEqual(self.popup.series_y_ticks_pad.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "y_ticks_pad"])
        self.assertNotEqual(
            self.popup.series_y_ticks_weight.fields.currentText(),
            self.popup.variables["series_plot_settings"]["y_ticks_weight"])
        self.assertNotEqual(self.popup.series_y_ticks_len.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "y_ticks_len"])
        self.assertNotEqual(self.popup.series_y_grid_flag.isChecked(),
                            self.popup.variables["series_plot_settings"][
                                "y_grid_flag"])
        self.assertNotEqual(
            self.popup.series_y_grid_color.fields.currentText(),
            self.popup.variables["series_plot_settings"]["y_grid_color"])
        self.assertNotEqual(
            self.popup.series_y_grid_linestyle.fields.currentText(),
            self.popup.variables["series_plot_settings"]["y_grid_linestyle"])
        self.assertNotEqual(self.popup.series_y_grid_linewidth.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "y_grid_linewidth"])
        self.assertNotEqual(self.popup.series_y_grid_alpha.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "y_grid_alpha"])

        self.assertNotEqual(self.popup.theo_pre_color.fields.currentText(),
                            self.popup.variables["series_plot_settings"][
                                "theo_pre_color"])
        self.assertNotEqual(self.popup.theo_pre_lw.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "theo_pre_lw"])
        self.assertNotEqual(self.popup.tag_cartoon_color.fields.currentText(),
                            self.popup.variables["series_plot_settings"][
                                "tag_cartoon_color"])
        self.assertNotEqual(self.popup.tag_cartoon_lw.field.value(),
                            self.popup.variables["series_plot_settings"][
                                "tag_cartoon_lw"])
        self.assertNotEqual(self.popup.tag_cartoon_ls.fields.currentText(),
                            self.popup.variables["series_plot_settings"][
                                "tag_cartoon_ls"])

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)


if __name__ == "__main__":
    unittest.main()