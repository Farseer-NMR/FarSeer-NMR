import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication

from gui.popups.HeatMapPopup import HeatMapPopup
from core.utils import get_default_config_path

app = QApplication(sys.argv)

from core.fslibs.Variables import Variables

class Test_HeatMapPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["heat_map_settings"]
        fin.close()

        self.popup = HeatMapPopup()
        self.variable_keys = tuple(self.popup.variables["heat_map_settings"].keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())

    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.heat_map_rows.field.value(),
                         self.defaults["rows"])
        self.assertEqual(self.popup.heat_map_vmin.field.value(),
                         self.defaults["vmin"])
        self.assertEqual(self.popup.heat_map_vmax.field.value(),
                         self.defaults["vmax"])
        self.assertEqual(self.popup.heat_map_x_ticks_fn.fields.currentText(),
                         self.defaults["x_ticks_fn"])
        self.assertEqual(self.popup.heat_map_x_ticks_fs.field.value(),
                         self.defaults["x_ticks_fs"])
        self.assertEqual(self.popup.heat_map_x_tick_pad.field.value(),
                         self.defaults["x_ticks_pad"])
        self.assertEqual(self.popup.heat_map_x_tick_weight.fields.currentText(),
                         self.defaults["x_ticks_weight"])
        self.assertEqual(self.popup.heat_map_x_ticks_rot.field.value(),
                         self.defaults["x_ticks_rot"])
        self.assertEqual(self.popup.heat_map_y_label_fn.fields.currentText(),
                         self.defaults["y_label_fn"])
        self.assertEqual(self.popup.heat_map_y_label_fs.field.value(),
                         self.defaults["y_label_fs"])
        self.assertEqual(self.popup.heat_map_y_label_pad.field.value(),
                         self.defaults["y_label_pad"])
        self.assertEqual(self.popup.heat_map_y_label_weight.fields.currentText(),
                         self.defaults["y_label_weight"])
        self.assertEqual(self.popup.heat_map_right_margin.field.value(),
                         self.defaults["right_margin"])
        self.assertEqual(self.popup.heat_map_bottom_margin.field.value(),
                         self.defaults["bottom_margin"])
        self.assertEqual(self.popup.heat_map_cbar_font_size.field.value(),
                         self.defaults["cbar_font_size"])
        self.assertEqual(self.popup.heat_map_tag_line_color.fields.currentText(),
                         self.defaults["tag_line_color"])
        self.assertEqual(self.popup.heat_map_tag_ls.fields.currentText(),
                         self.defaults["tag_line_ls"])
        self.assertEqual(self.popup.heat_map_tag_lw.field.value(),
                         self.defaults["tag_line_lw"])

    def test_change_variables(self):
        pass

    def test_set_values(self):
        self.popup.heat_map_rows.setValue(10)
        self.popup.heat_map_vmin.setValue(0.2)
        self.popup.heat_map_vmax.setValue(0.9)
        self.popup.heat_map_x_ticks_fs.setValue(12)
        self.popup.heat_map_x_ticks_rot.setValue(45)
        self.popup.heat_map_x_ticks_fn.select("Courier New")
        self.popup.heat_map_x_tick_pad.setValue(2)
        self.popup.heat_map_x_tick_weight.select("semibold")
        self.popup.heat_map_y_label_fs.setValue(16)
        self.popup.heat_map_y_label_pad.setValue(5)
        self.popup.heat_map_y_label_fn.select("Times New Roman")
        self.popup.heat_map_y_label_weight.select("normal")
        self.popup.heat_map_right_margin.setValue(0.45)
        self.popup.heat_map_bottom_margin.setValue(0.8)
        self.popup.heat_map_cbar_font_size.setValue(8)
        self.popup.heat_map_tag_line_color.select("white")
        self.popup.heat_map_tag_ls.select(":")
        self.popup.heat_map_tag_lw.setValue(0.6)
        self.popup.set_values()

        self.assertEqual(self.popup.heat_map_rows.field.value(), 10)
        self.assertEqual(self.popup.heat_map_rows.field.value(),
                         self.popup.variables["heat_map_settings"]["rows"])
        self.assertEqual(self.popup.heat_map_vmin.field.value(), 0.2)
        self.assertEqual(self.popup.heat_map_vmin.field.value(),
                         self.popup.variables["heat_map_settings"]["vmin"])
        self.assertEqual(self.popup.heat_map_vmax.field.value(), 0.9)
        self.assertEqual(self.popup.heat_map_vmax.field.value(),
                         self.popup.variables["heat_map_settings"]["vmax"])
        self.assertEqual(self.popup.heat_map_x_ticks_fn.fields.currentText(),
                         "Courier New")
        self.assertEqual(self.popup.heat_map_x_ticks_fn.fields.currentText(),
                         self.popup.variables["heat_map_settings"]["x_ticks_fn"])
        self.assertEqual(self.popup.heat_map_x_ticks_fs.field.value(), 12)
        self.assertEqual(self.popup.heat_map_x_ticks_fs.field.value(),
                         self.popup.variables["heat_map_settings"]["x_ticks_fs"])
        self.assertEqual(self.popup.heat_map_x_tick_pad.field.value(), 2)
        self.assertEqual(self.popup.heat_map_x_tick_pad.field.value(),
                         self.popup.variables["heat_map_settings"]["x_ticks_pad"])
        self.assertEqual(
            self.popup.heat_map_x_tick_weight.fields.currentText(), "semibold")
        self.assertEqual(
            self.popup.heat_map_x_tick_weight.fields.currentText(),
            self.popup.variables["heat_map_settings"]["x_ticks_weight"])
        self.assertEqual(self.popup.heat_map_x_ticks_rot.field.value(), 45)
        self.assertEqual(self.popup.heat_map_x_ticks_rot.field.value(),
                         self.popup.variables["heat_map_settings"]["x_ticks_rot"])
        self.assertEqual(self.popup.heat_map_y_label_fn.fields.currentText(

        ), "Times New Roman")
        self.assertEqual(self.popup.heat_map_y_label_fn.fields.currentText(),
                         self.popup.variables["heat_map_settings"]["y_label_fn"])
        self.assertEqual(self.popup.heat_map_y_label_fs.field.value(), 16)
        self.assertEqual(self.popup.heat_map_y_label_fs.field.value(),
                         self.popup.variables["heat_map_settings"]["y_label_fs"])
        self.assertEqual(self.popup.heat_map_y_label_pad.field.value(), 5)
        self.assertEqual(self.popup.heat_map_y_label_pad.field.value(),
                         self.popup.variables["heat_map_settings"]["y_label_pad"])
        self.assertEqual(
            self.popup.heat_map_y_label_weight.fields.currentText(), "normal")
        self.assertEqual(
            self.popup.heat_map_y_label_weight.fields.currentText(),
            self.popup.variables["heat_map_settings"]["y_label_weight"])
        self.assertEqual(self.popup.heat_map_right_margin.field.value(), 0.45)
        self.assertEqual(self.popup.heat_map_right_margin.field.value(),
                         self.popup.variables["heat_map_settings"]["right_margin"])
        self.assertEqual(self.popup.heat_map_bottom_margin.field.value(), 0.8)
        self.assertEqual(self.popup.heat_map_bottom_margin.field.value(),
                         self.popup.variables["heat_map_settings"]["bottom_margin"])
        self.assertEqual(self.popup.heat_map_cbar_font_size.field.value(), 8)
        self.assertEqual(self.popup.heat_map_cbar_font_size.field.value(),
                         self.popup.variables["heat_map_settings"]["cbar_font_size"])
        self.assertEqual(
            self.popup.heat_map_tag_line_color.fields.currentText(), "white")
        self.assertEqual(
            self.popup.heat_map_tag_line_color.fields.currentText(),
            self.popup.variables["heat_map_settings"]["tag_line_color"])
        self.assertEqual(self.popup.heat_map_tag_ls.fields.currentText(), ":")
        self.assertEqual(self.popup.heat_map_tag_ls.fields.currentText(),
                         self.popup.variables["heat_map_settings"]["tag_line_ls"])
        self.assertEqual(self.popup.heat_map_tag_lw.field.value(), 0.6)
        self.assertEqual(self.popup.heat_map_tag_lw.field.value(),
                         self.popup.variables["heat_map_settings"]["tag_line_lw"])

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables["heat_map_settings"].keys()),
                         self.variable_keys)

    def test_values_not_set(self):
        self.popup.heat_map_rows.setValue(10)
        self.popup.heat_map_vmin.setValue(0.2)
        self.popup.heat_map_vmax.setValue(0.9)
        self.popup.heat_map_x_ticks_fs.setValue(12)
        self.popup.heat_map_x_ticks_rot.setValue(45)
        self.popup.heat_map_x_ticks_fn.select("Courier New")
        self.popup.heat_map_x_tick_pad.setValue(2)
        self.popup.heat_map_x_tick_weight.select("semibold")
        self.popup.heat_map_y_label_fs.setValue(16)
        self.popup.heat_map_y_label_pad.setValue(5)
        self.popup.heat_map_y_label_fn.select("Times New Roman")
        self.popup.heat_map_y_label_weight.select("normal")
        self.popup.heat_map_right_margin.setValue(0.45)
        self.popup.heat_map_bottom_margin.setValue(0.8)
        self.popup.heat_map_cbar_font_size.setValue(8)
        self.popup.heat_map_tag_line_color.select("white")
        self.popup.heat_map_tag_ls.select(":")
        self.popup.heat_map_tag_lw.setValue(0.6)


        self.assertEqual(self.popup.heat_map_rows.field.value(), 10)
        self.assertNotEqual(self.popup.heat_map_rows.field.value(),
                         self.popup.variables["heat_map_settings"]["rows"])
        self.assertEqual(self.popup.heat_map_vmin.field.value(), 0.2)
        self.assertNotEqual(self.popup.heat_map_vmin.field.value(),
                         self.popup.variables["heat_map_settings"]["vmin"])
        self.assertEqual(self.popup.heat_map_vmax.field.value(), 0.9)
        self.assertNotEqual(self.popup.heat_map_vmax.field.value(),
                         self.popup.variables["heat_map_settings"]["vmax"])
        self.assertEqual(self.popup.heat_map_x_ticks_fn.fields.currentText(),
                         "Courier New")
        self.assertNotEqual(self.popup.heat_map_x_ticks_fn.fields.currentText(),
                         self.popup.variables["heat_map_settings"]["x_ticks_fn"])
        self.assertEqual(self.popup.heat_map_x_ticks_fs.field.value(), 12)
        self.assertNotEqual(self.popup.heat_map_x_ticks_fs.field.value(),
                         self.popup.variables["heat_map_settings"]["x_ticks_fs"])
        self.assertEqual(self.popup.heat_map_x_tick_pad.field.value(), 2)
        self.assertNotEqual(self.popup.heat_map_x_tick_pad.field.value(),
                         self.popup.variables["heat_map_settings"]["x_ticks_pad"])
        self.assertEqual(
            self.popup.heat_map_x_tick_weight.fields.currentText(), "semibold")
        self.assertNotEqual(
            self.popup.heat_map_x_tick_weight.fields.currentText(),
            self.popup.variables["heat_map_settings"]["x_ticks_weight"])
        self.assertEqual(self.popup.heat_map_x_ticks_rot.field.value(), 45)
        self.assertNotEqual(self.popup.heat_map_x_ticks_rot.field.value(),
                         self.popup.variables["heat_map_settings"]["x_ticks_rot"])
        self.assertEqual(self.popup.heat_map_y_label_fn.fields.currentText(

        ), "Times New Roman")
        self.assertNotEqual(self.popup.heat_map_y_label_fn.fields.currentText(),
                         self.popup.variables["heat_map_settings"]["y_label_fn"])
        self.assertEqual(self.popup.heat_map_y_label_fs.field.value(), 16)
        self.assertNotEqual(self.popup.heat_map_y_label_fs.field.value(),
                         self.popup.variables["heat_map_settings"]["y_label_fs"])
        self.assertEqual(self.popup.heat_map_y_label_pad.field.value(), 5)
        self.assertNotEqual(self.popup.heat_map_y_label_pad.field.value(),
                         self.popup.variables["heat_map_settings"]["y_label_pad"])
        self.assertEqual(
            self.popup.heat_map_y_label_weight.fields.currentText(), "normal")
        self.assertNotEqual(
            self.popup.heat_map_y_label_weight.fields.currentText(),
            self.popup.variables["heat_map_settings"]["y_label_weight"])
        self.assertEqual(self.popup.heat_map_right_margin.field.value(), 0.45)
        self.assertNotEqual(self.popup.heat_map_right_margin.field.value(),
                         self.popup.variables["heat_map_settings"]["right_margin"])
        self.assertEqual(self.popup.heat_map_bottom_margin.field.value(), 0.8)
        self.assertNotEqual(self.popup.heat_map_bottom_margin.field.value(),
                         self.popup.variables["heat_map_settings"]["bottom_margin"])
        self.assertEqual(self.popup.heat_map_cbar_font_size.field.value(), 8)
        self.assertNotEqual(self.popup.heat_map_cbar_font_size.field.value(),
                         self.popup.variables["heat_map_settings"]["cbar_font_size"])
        self.assertEqual(
            self.popup.heat_map_tag_line_color.fields.currentText(), "white")
        self.assertNotEqual(
            self.popup.heat_map_tag_line_color.fields.currentText(),
            self.popup.variables["heat_map_settings"]["tag_line_color"])
        self.assertEqual(self.popup.heat_map_tag_ls.fields.currentText(),
        ":")
        self.assertNotEqual(self.popup.heat_map_tag_ls.fields.currentText(),
                         self.popup.variables["heat_map_settings"]["tag_line_ls"])
        self.assertEqual(self.popup.heat_map_tag_lw.field.value(), 0.6)
        self.assertNotEqual(self.popup.heat_map_tag_lw.field.value(),
                         self.popup.variables["heat_map_settings"]["tag_line_lw"])

        self.assertEqual(tuple(self.popup.local_variables.keys()),
                         self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables["heat_map_settings"].keys()),
                         self.variable_keys)

if __name__ == "__main__":
    unittest.main()