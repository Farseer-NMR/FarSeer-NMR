import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication

from gui.popups.OscillationMapPopup import OscillationMapPopup

from gui.gui_utils import get_colour
from current.utils import get_default_config_path

app = QApplication(sys.argv)

from current.fslibs.Variables import Variables

class Test_OscillationMapPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["dpre_osci_settings"]
        fin.close()


        self.popup = OscillationMapPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())

    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.dpre_osci_rows.field.value(),
                         self.defaults["rows"])
        self.assertEqual(self.popup.dpre_osci_width.field.value(),
                         self.defaults["width"])
        self.assertEqual(self.popup.dpre_osci_y_label.field.text(),
                         self.defaults["y_label"])
        self.assertEqual(self.popup.dpre_osci_y_label_fs.field.value(),
                         self.defaults["y_label_fs"])
        self.assertEqual(self.popup.dpre_osci_dpre_ms.field.value(),
                         self.defaults["dpre_ms"])
        self.assertEqual(self.popup.dpre_osci_dpre_alpha.field.value(),
                         self.defaults["dpre_alpha"])
        self.assertEqual(self.popup.dpre_osci_smooth_lw.field.value(),
                         self.defaults["smooth_lw"])
        self.assertEqual(self.popup.dpre_osci_ref_color.fields.currentText(),
                         get_colour(self.defaults["ref_color"]))
        self.assertEqual(self.popup.dpre_osci_color_init.fields
                         .currentText(),
                         get_colour(self.defaults["color_init"]))
        self.assertEqual(self.popup.dpre_osci_color_end.fields.currentText(),
                         get_colour(self.defaults["color_end"]))
        self.assertEqual(self.popup.dpre_osci_x_ticks_fs.field.value(),
                         self.defaults["x_ticks_fs"])
        self.assertEqual(self.popup.dpre_osci_x_ticks_fn.fields.currentText(),
                         self.defaults["x_ticks_fn"])
        self.assertEqual(self.popup.dpre_osci_x_ticks_pad.field.value(),
                         self.defaults["x_ticks_pad"])
        self.assertEqual(
            self.popup.dpre_osci_x_ticks_weight.fields.currentText(),
            self.defaults["x_ticks_weight"])
        self.assertEqual(self.popup.dpre_osci_grid_color.fields.currentText(),
                         self.defaults["grid_color"])
        self.assertEqual(self.popup.dpre_osci_shade.isChecked(),
                         self.defaults["shade"])
        self.assertEqual(self.popup.dpre_osci_regions.field.text(),
                         self.popup.get_ranges(self.defaults["shade_regions"]))
        self.assertEqual(self.popup.dpre_osci_res_highlight.isChecked(),
                         self.defaults["res_highlight"])
        self.assertEqual(self.popup.dpre_osci_res_highlight_list.field.text(),
                         ','.join(
                             list(map(str, self.defaults["res_hl_list"]))))
        self.assertEqual(self.popup.dpre_osci_rh_fs.field.value(),
                         self.defaults["res_highlight_fs"])
        self.assertEqual(self.popup.dpre_osci_rh_y.field.value(),
                         self.defaults["res_highlight_y"])
        self.assertEqual(self.popup.dpre_osci_ymax.field.value(),
                         self.defaults["ymax"])
        #
    def test_set_values(self):
        self.popup.dpre_osci_rows.setValue(5)
        self.popup.dpre_osci_width.setValue(4)
        self.popup.dpre_osci_y_label.setText("PRE")
        self.popup.dpre_osci_y_label_fs.setValue(8)
        self.popup.dpre_osci_dpre_ms.setValue(5)
        self.popup.dpre_osci_dpre_alpha.setValue(0.3)
        self.popup.dpre_osci_smooth_lw.setValue(2)
        self.popup.dpre_osci_ref_color.select("white")
        self.popup.dpre_osci_color_init.select("blue")
        self.popup.dpre_osci_color_end.select("red")
        self.popup.dpre_osci_x_ticks_fs.setValue(18)
        self.popup.dpre_osci_x_ticks_fn.select("Courier New")
        self.popup.dpre_osci_x_ticks_pad.setValue(0.8)
        self.popup.dpre_osci_x_ticks_weight.select("bold")
        self.popup.dpre_osci_grid_color.select("red")
        self.popup.dpre_osci_shade.setChecked(True)
        self.popup.dpre_osci_regions.setText("0-10, 18-45")
        self.popup.dpre_osci_res_highlight.setChecked(True)
        self.popup.dpre_osci_res_highlight_list.field.setText("3,4,5")
        self.popup.dpre_osci_rh_fs.setValue(8)
        self.popup.dpre_osci_rh_y.setValue(0.7)
        self.popup.dpre_osci_ymax.setValue(0.9)
        self.popup.set_values()

        self.assertEqual(self.popup.dpre_osci_rows.field.value(), 5)
        self.assertEqual(self.popup.dpre_osci_rows.field.value(),
                         self.popup.variables["dpre_osci_settings"]["rows"])
        self.assertEqual(self.popup.dpre_osci_width.field.value(), 4)
        self.assertEqual(self.popup.dpre_osci_width.field.value(),
                         self.popup.variables["dpre_osci_settings"]["width"])
        self.assertEqual(self.popup.dpre_osci_y_label.field.text(), "PRE")
        self.assertEqual(self.popup.dpre_osci_y_label.field.text(),
                         self.popup.variables["dpre_osci_settings"]["y_label"])
        self.assertEqual(self.popup.dpre_osci_y_label_fs.field.value(), 8)
        self.assertEqual(self.popup.dpre_osci_y_label_fs.field.value(),
                         self.popup.variables["dpre_osci_settings"]["y_label_fs"])
        self.assertEqual(self.popup.dpre_osci_dpre_ms.field.value(), 5)
        self.assertEqual(self.popup.dpre_osci_dpre_ms.field.value(),
                         self.popup.variables["dpre_osci_settings"]["dpre_ms"])
        self.assertEqual(self.popup.dpre_osci_dpre_alpha.field.value(), 0.3)
        self.assertEqual(self.popup.dpre_osci_dpre_alpha.field.value(),
                         self.popup.variables["dpre_osci_settings"]["dpre_alpha"])
        self.assertEqual(self.popup.dpre_osci_smooth_lw.field.value(),
                         self.popup.variables["dpre_osci_settings"]["smooth_lw"])
        self.assertEqual(self.popup.dpre_osci_smooth_lw.field.value(), 2)
        self.assertEqual(self.popup.dpre_osci_ref_color.fields.currentText(),
                         self.popup.variables["dpre_osci_settings"]["ref_color"])
        self.assertEqual(self.popup.dpre_osci_ref_color.fields.currentText(

        ), "white")
        self.assertEqual(self.popup.dpre_osci_color_init.fields.currentText(),
                         self.popup.variables["dpre_osci_settings"]["color_init"])
        self.assertEqual(
            self.popup.dpre_osci_color_init.fields.currentText(), "blue")
        self.assertEqual(self.popup.dpre_osci_color_end.fields.currentText(),
                         self.popup.variables["dpre_osci_settings"]["color_end"])
        self.assertEqual(self.popup.dpre_osci_color_end.fields.currentText(

        ), "red")
        self.assertEqual(self.popup.dpre_osci_x_ticks_fs.field.value(), 18)
        self.assertEqual(self.popup.dpre_osci_x_ticks_fs.field.value(),
                         self.popup.variables["dpre_osci_settings"]["x_ticks_fs"])
        self.assertEqual(
            self.popup.dpre_osci_x_ticks_fn.fields.currentText(), "Courier "
                                                                  "New")
        self.assertEqual(self.popup.dpre_osci_x_ticks_fn.fields.currentText(),
                         self.popup.variables["dpre_osci_settings"]["x_ticks_fn"])
        self.assertEqual(self.popup.dpre_osci_x_ticks_pad.field.value(), 0.8)
        self.assertEqual(self.popup.dpre_osci_x_ticks_pad.field.value(),
                         self.popup.variables["dpre_osci_settings"]["x_ticks_pad"])
        self.assertEqual(
            self.popup.dpre_osci_x_ticks_weight.fields.currentText(), "bold")
        self.assertEqual(
            self.popup.dpre_osci_x_ticks_weight.fields.currentText(),
            self.popup.variables["dpre_osci_settings"]["x_ticks_weight"])
        self.assertEqual(
            self.popup.dpre_osci_grid_color.fields.currentText(), "red")
        self.assertEqual(self.popup.dpre_osci_grid_color.fields.currentText(),
                         self.popup.variables["dpre_osci_settings"]["grid_color"])
        self.assertEqual(self.popup.dpre_osci_shade.isChecked(), True)
        self.assertEqual(self.popup.dpre_osci_shade.isChecked(),
                         self.popup.variables["dpre_osci_settings"]["shade"])
        self.assertEqual(self.popup.dpre_osci_regions.field.text(),
                         "0-10, 18-45")
        self.assertEqual(self.popup.set_ranges(self.popup.dpre_osci_regions.field.text()),
                         self.popup.variables["dpre_osci_settings"]["shade_regions"])
        self.assertEqual(self.popup.dpre_osci_res_highlight.isChecked(), True)
        self.assertEqual(self.popup.dpre_osci_res_highlight.isChecked(),
                         self.popup.variables["dpre_osci_settings"]["res_highlight"])
        self.assertEqual(
            self.popup.dpre_osci_res_highlight_list.field.text(), "3,4,5")
        self.assertEqual(self.popup.dpre_osci_res_highlight_list.field.text(),
                         ','.join(list(
                             map(str, self.popup.variables["dpre_osci_settings"]["res_hl_list"]))))
        self.assertEqual(self.popup.dpre_osci_rh_fs.field.value(), 8)
        self.assertEqual(self.popup.dpre_osci_rh_fs.field.value(),
                         self.popup.variables["dpre_osci_settings"]["res_highlight_fs"])
        self.assertEqual(self.popup.dpre_osci_rh_y.field.value(), 0.7)
        self.assertEqual(self.popup.dpre_osci_rh_y.field.value(),
                         self.popup.variables["dpre_osci_settings"]["res_highlight_y"])
        self.assertEqual(self.popup.dpre_osci_ymax.field.value(), 0.9)
        self.assertEqual(self.popup.dpre_osci_ymax.field.value(),
                         self.popup.variables["dpre_osci_settings"]["ymax"])

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

    def test_values_not_set(self):
        self.popup.dpre_osci_rows.setValue(5)
        self.popup.dpre_osci_width.setValue(4)
        self.popup.dpre_osci_y_label.setText("PRE")
        self.popup.dpre_osci_y_label_fs.setValue(8)
        self.popup.dpre_osci_dpre_ms.setValue(5)
        self.popup.dpre_osci_dpre_alpha.setValue(0.3)
        self.popup.dpre_osci_smooth_lw.setValue(2)
        self.popup.dpre_osci_ref_color.select("white")
        self.popup.dpre_osci_color_init.select("blue")
        self.popup.dpre_osci_color_end.select("red")
        self.popup.dpre_osci_x_ticks_fs.setValue(18)
        self.popup.dpre_osci_x_ticks_fn.select("Courier New")
        self.popup.dpre_osci_x_ticks_pad.setValue(0.8)
        self.popup.dpre_osci_x_ticks_weight.select("bold")
        self.popup.dpre_osci_grid_color.select("red")
        self.popup.dpre_osci_shade.setChecked(True)
        self.popup.dpre_osci_regions.setText("0-10, 18-45")
        self.popup.dpre_osci_res_highlight.setChecked(True)
        self.popup.dpre_osci_res_highlight_list.field.setText("3,4,5")
        self.popup.dpre_osci_rh_fs.setValue(8)
        self.popup.dpre_osci_rh_y.setValue(0.7)
        self.popup.dpre_osci_ymax.setValue(0.9)


        self.assertEqual(self.popup.dpre_osci_rows.field.value(), 5)
        self.assertNotEqual(self.popup.dpre_osci_rows.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "rows"])
        self.assertEqual(self.popup.dpre_osci_width.field.value(), 4)
        self.assertNotEqual(self.popup.dpre_osci_width.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "width"])
        self.assertEqual(self.popup.dpre_osci_y_label.field.text(), "PRE")
        self.assertNotEqual(self.popup.dpre_osci_y_label.field.text(),
                         self.popup.variables["dpre_osci_settings"][
                             "y_label"])
        self.assertEqual(self.popup.dpre_osci_y_label_fs.field.value(), 8)
        self.assertNotEqual(self.popup.dpre_osci_y_label_fs.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "y_label_fs"])
        self.assertEqual(self.popup.dpre_osci_dpre_ms.field.value(), 5)
        self.assertNotEqual(self.popup.dpre_osci_dpre_ms.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "dpre_ms"])
        self.assertEqual(self.popup.dpre_osci_dpre_alpha.field.value(),
                         0.3)
        self.assertNotEqual(self.popup.dpre_osci_dpre_alpha.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "dpre_alpha"])
        self.assertEqual(self.popup.dpre_osci_smooth_lw.field.value(), 2)
        self.assertNotEqual(self.popup.dpre_osci_smooth_lw.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "smooth_lw"])
        self.assertNotEqual(
            self.popup.dpre_osci_ref_color.fields.currentText(),
            self.popup.variables["dpre_osci_settings"]["ref_color"])
        self.assertEqual(self.popup.dpre_osci_ref_color.fields.currentText(

        ), "white")
        self.assertNotEqual(
            self.popup.dpre_osci_color_init.fields.currentText(),
            self.popup.variables["dpre_osci_settings"]["color_init"])
        self.assertEqual(
            self.popup.dpre_osci_color_init.fields.currentText(), "blue")
        self.assertNotEqual(
            self.popup.dpre_osci_color_end.fields.currentText(),
            self.popup.variables["dpre_osci_settings"]["color_end"])
        self.assertEqual(self.popup.dpre_osci_color_end.fields.currentText(

        ), "red")
        self.assertEqual(self.popup.dpre_osci_x_ticks_fs.field.value(), 18)
        self.assertNotEqual(self.popup.dpre_osci_x_ticks_fs.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "x_ticks_fs"])
        self.assertEqual(
            self.popup.dpre_osci_x_ticks_fn.fields.currentText(),
            "Courier "
            "New")
        self.assertNotEqual(
            self.popup.dpre_osci_x_ticks_fn.fields.currentText(),
            self.popup.variables["dpre_osci_settings"]["x_ticks_fn"])
        self.assertEqual(self.popup.dpre_osci_x_ticks_pad.field.value(),
                         0.8)
        self.assertNotEqual(self.popup.dpre_osci_x_ticks_pad.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "x_ticks_pad"])
        self.assertEqual(
            self.popup.dpre_osci_x_ticks_weight.fields.currentText(),
            "bold")
        self.assertNotEqual(
            self.popup.dpre_osci_x_ticks_weight.fields.currentText(),
            self.popup.variables["dpre_osci_settings"]["x_ticks_weight"])
        self.assertEqual(
            self.popup.dpre_osci_grid_color.fields.currentText(), "red")
        self.assertNotEqual(
            self.popup.dpre_osci_grid_color.fields.currentText(),
            self.popup.variables["dpre_osci_settings"]["grid_color"])
        self.assertEqual(self.popup.dpre_osci_shade.isChecked(), True)
        self.assertNotEqual(self.popup.dpre_osci_shade.isChecked(),
                         self.popup.variables["dpre_osci_settings"][
                             "shade"])
        self.assertEqual(self.popup.dpre_osci_regions.field.text(),
                         "0-10, 18-45")
        self.assertNotEqual(self.popup.set_ranges(
            self.popup.dpre_osci_regions.field.text()),
                         self.popup.variables["dpre_osci_settings"][
                             "shade_regions"])
        self.assertEqual(self.popup.dpre_osci_res_highlight.isChecked(),
                         True)
        self.assertNotEqual(self.popup.dpre_osci_res_highlight.isChecked(),
                         self.popup.variables["dpre_osci_settings"][
                             "res_highlight"])
        self.assertEqual(
            self.popup.dpre_osci_res_highlight_list.field.text(), "3,4,5")
        self.assertNotEqual(
            self.popup.dpre_osci_res_highlight_list.field.text(),
            ','.join(list(
                map(str, self.popup.variables["dpre_osci_settings"][
                    "res_hl_list"]))))
        self.assertEqual(self.popup.dpre_osci_rh_fs.field.value(), 8)
        self.assertNotEqual(self.popup.dpre_osci_rh_fs.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "res_highlight_fs"])
        self.assertEqual(self.popup.dpre_osci_rh_y.field.value(), 0.7)
        self.assertNotEqual(self.popup.dpre_osci_rh_y.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "res_highlight_y"])
        self.assertEqual(self.popup.dpre_osci_ymax.field.value(), 0.9)
        self.assertNotEqual(self.popup.dpre_osci_ymax.field.value(),
                         self.popup.variables["dpre_osci_settings"][
                             "ymax"])

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()),
                         self.variable_keys)

if __name__ == "__main__":
    unittest.main()