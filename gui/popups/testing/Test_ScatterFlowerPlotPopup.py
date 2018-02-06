import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication
from core.utils import get_default_config_path

from gui.popups.ScatterFlowerPlotPopup import ScatterFlowerPlotPopup

app = QApplication(sys.argv)

from core.fslibs.Variables import Variables

class Test_ScatterFlowerPlotPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["cs_scatter_flower_settings"]
        fin.close()

        self.popup = ScatterFlowerPlotPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())


    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.cs_scatter_flower_x_label.field.text(),
                         self.defaults["x_label"])
        self.assertEqual(self.popup.cs_scatter_flower_y_label.field.text(),
                         self.defaults["y_label"])
        self.assertEqual(self.popup.cs_scatter_flower_mksize.field.value(),
                         self.defaults["mksize"])
        self.assertEqual(self.popup.cs_scatter_flower_color_grad.isChecked(),
                         self.defaults["color_grad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_color_start.fields.currentText(),
            self.defaults["mk_start_color"])
        self.assertEqual(
            self.popup.cs_scatter_flower_color_end.fields.currentText(),
            self.defaults["mk_end_color"])
        self.assertEqual(self.popup.cs_scatter_flower_color_list.field.text(),
                         ','.join(self.defaults["color_list"]))

        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_fn.fields.currentText(),
            self.defaults["x_label_fn"])
        self.assertEqual(self.popup.cs_scatter_flower_x_label_fs.field.value(),
                         self.defaults["x_label_fs"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_pad.field.value(),
            self.defaults["x_label_pad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_weight.fields.currentText(),
            self.defaults["x_label_weight"])

        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_fn.fields.currentText(),
            self.defaults["y_label_fn"])
        self.assertEqual(self.popup.cs_scatter_flower_y_label_fs.field.value(),
                         self.defaults["y_label_fs"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_pad.field.value(),
            self.defaults["y_label_pad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_weight.fields.currentText(),
            self.defaults["y_label_weight"])

        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_fn.fields.currentText(),
            self.defaults["x_ticks_fn"])
        self.assertEqual(self.popup.cs_scatter_flower_x_ticks_fs.field.value(),
                         self.defaults["x_ticks_fs"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_pad.field.value(),
            self.defaults["x_ticks_pad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_weight.fields.currentText(),
            self.defaults["x_ticks_weight"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_rot.field.value(),
            self.defaults["x_ticks_rot"])

        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_fn.fields.currentText(),
            self.defaults["y_ticks_fn"])
        self.assertEqual(self.popup.cs_scatter_flower_y_ticks_fs.field.value(),
                         self.defaults["y_ticks_fs"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_pad.field.value(),
            self.defaults["y_ticks_pad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_weight.fields.currentText(),
            self.defaults["y_ticks_weight"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_rot.field.value(),
            self.defaults["y_ticks_rot"])

    def test_set_values(self):
        self.popup.cs_scatter_flower_x_label.setText("X Label")
        self.popup.cs_scatter_flower_y_label.setText("Y Label")
        self.popup.cs_scatter_flower_mksize.setValue(10)
        self.popup.cs_scatter_flower_color_grad.setChecked(False)
        self.popup.cs_scatter_flower_color_start.select("silver")
        self.popup.cs_scatter_flower_color_end.select("brown")
        self.popup.cs_scatter_flower_color_list.setText(
            "red,blue,orange")

        self.popup.cs_scatter_flower_x_label_fn.select("monospace")
        self.popup.cs_scatter_flower_x_label_fs.setValue(15)
        self.popup.cs_scatter_flower_x_label_pad.setValue(3)
        self.popup.cs_scatter_flower_x_label_weight.select("bold")

        self.popup.cs_scatter_flower_y_label_fn.select("Impact")
        self.popup.cs_scatter_flower_y_label_fs.setValue(18)
        self.popup.cs_scatter_flower_y_label_pad.setValue(5)
        self.popup.cs_scatter_flower_y_label_weight.select("semibold")

        self.popup.cs_scatter_flower_x_ticks_fn.select("Verdana")
        self.popup.cs_scatter_flower_x_ticks_fs.setValue(3)
        self.popup.cs_scatter_flower_x_ticks_pad.setValue(15)
        self.popup.cs_scatter_flower_x_ticks_weight.select("bold")
        self.popup.cs_scatter_flower_x_ticks_rot.setValue(75)

        self.popup.cs_scatter_flower_y_ticks_fn.select("Verdana")
        self.popup.cs_scatter_flower_y_ticks_fs.setValue(3)
        self.popup.cs_scatter_flower_y_ticks_pad.setValue(15)
        self.popup.cs_scatter_flower_y_ticks_weight.select("bold")
        self.popup.cs_scatter_flower_y_ticks_rot.setValue(60)


        self.popup.set_values()

        self.assertEqual(self.popup.cs_scatter_flower_x_label.field.text(),
                         "X Label")
        self.assertEqual(self.popup.cs_scatter_flower_y_label.field.text(),
                         "Y Label")
        self.assertEqual(self.popup.cs_scatter_flower_mksize.field.value(), 10)
        self.assertEqual(self.popup.cs_scatter_flower_color_grad.isChecked(),
                         False)
        self.assertEqual(
            self.popup.cs_scatter_flower_color_start.fields.currentText(),
            "silver")
        self.assertEqual(
            self.popup.cs_scatter_flower_color_end.fields.currentText(),
            "brown")
        self.assertEqual(self.popup.cs_scatter_flower_color_list.field.text(),
                         "red,blue,orange")

        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_fn.fields.currentText(),
            "monospace")
        self.assertEqual(self.popup.cs_scatter_flower_x_label_fs.field.value(),
                         15)
        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_pad.field.value(), 3)
        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_weight.fields.currentText(),
            "bold")

        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_fn.fields.currentText(),
            "Impact")
        self.assertEqual(self.popup.cs_scatter_flower_y_label_fs.field.value(),
                         18)
        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_pad.field.value(), 5)
        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_weight.fields.currentText(),
            "semibold")

        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_fn.fields.currentText(),
            "Verdana")
        self.assertEqual(self.popup.cs_scatter_flower_x_ticks_fs.field.value(),
                         3)
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_pad.field.value(), 15)
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_weight.fields.currentText(),
            "bold")
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_rot.field.value(), 75)

        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_fn.fields.currentText(),
            "Verdana")
        self.assertEqual(self.popup.cs_scatter_flower_y_ticks_fs.field.value(),
                         3)
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_pad.field.value(), 15)
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_weight.fields.currentText(),
            "bold")
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_rot.field.value(), 60)

        self.assertEqual(self.popup.cs_scatter_flower_x_label.field.text(),
                         self.popup.variables["cs_scatter_flower_settings"][
                             "x_label"])
        self.assertEqual(self.popup.cs_scatter_flower_y_label.field.text(),
                         self.popup.variables["cs_scatter_flower_settings"][
                             "y_label"])
        self.assertEqual(self.popup.cs_scatter_flower_mksize.field.value(),
                         self.popup.variables["cs_scatter_flower_settings"][
                             "mksize"])
        self.assertEqual(self.popup.cs_scatter_flower_color_grad.isChecked(),
                         self.popup.variables["cs_scatter_flower_settings"][
                             "color_grad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_color_start.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "mk_start_color"])
        self.assertEqual(
            self.popup.cs_scatter_flower_color_end.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["mk_end_color"])
        self.assertEqual(self.popup.cs_scatter_flower_color_list.field.text(),
                         ','.join(self.popup.variables[
                                      "cs_scatter_flower_settings"][
                                      "color_list"]))

        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_fn.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["x_label_fn"])
        self.assertEqual(self.popup.cs_scatter_flower_x_label_fs.field.value(),
                         self.popup.variables["cs_scatter_flower_settings"][
                             "x_label_fs"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_pad.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["x_label_pad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_weight.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "x_label_weight"])

        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_fn.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["y_label_fn"])
        self.assertEqual(self.popup.cs_scatter_flower_y_label_fs.field.value(),
                         self.popup.variables["cs_scatter_flower_settings"][
                             "y_label_fs"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_pad.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["y_label_pad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_weight.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "y_label_weight"])

        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_fn.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["x_ticks_fn"])
        self.assertEqual(self.popup.cs_scatter_flower_x_ticks_fs.field.value(),
                         self.popup.variables["cs_scatter_flower_settings"][
                             "x_ticks_fs"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_pad.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["x_ticks_pad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_weight.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "x_ticks_weight"])
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_rot.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["x_ticks_rot"])

        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_fn.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["y_ticks_fn"])
        self.assertEqual(self.popup.cs_scatter_flower_y_ticks_fs.field.value(),
                         self.popup.variables["cs_scatter_flower_settings"][
                             "y_ticks_fs"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_pad.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["y_ticks_pad"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_weight.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "y_ticks_weight"])
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_rot.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["y_ticks_rot"])
        self.assertEqual(tuple(self.popup.local_variables.keys()), self.local_variable_keys)
        self.assertEqual(tuple(self.popup.variables.keys()), self.variable_keys)

    def test_values_not_set(self):
        self.popup.cs_scatter_flower_x_label.setText("X Label")
        self.popup.cs_scatter_flower_y_label.setText("Y Label")
        self.popup.cs_scatter_flower_mksize.setValue(10)
        self.popup.cs_scatter_flower_color_grad.setChecked(False)
        self.popup.cs_scatter_flower_color_start.select("silver")
        self.popup.cs_scatter_flower_color_end.select("brown")
        self.popup.cs_scatter_flower_color_list.setText(
            "red,blue,orange")

        self.popup.cs_scatter_flower_x_label_fn.select("monospace")
        self.popup.cs_scatter_flower_x_label_fs.setValue(15)
        self.popup.cs_scatter_flower_x_label_pad.setValue(3)
        self.popup.cs_scatter_flower_x_label_weight.select("bold")

        self.popup.cs_scatter_flower_y_label_fn.select("Impact")
        self.popup.cs_scatter_flower_y_label_fs.setValue(18)
        self.popup.cs_scatter_flower_y_label_pad.setValue(5)
        self.popup.cs_scatter_flower_y_label_weight.select("semibold")

        self.popup.cs_scatter_flower_x_ticks_fn.select("Verdana")
        self.popup.cs_scatter_flower_x_ticks_fs.setValue(3)
        self.popup.cs_scatter_flower_x_ticks_pad.setValue(15)
        self.popup.cs_scatter_flower_x_ticks_weight.select("bold")
        self.popup.cs_scatter_flower_x_ticks_rot.setValue(75)

        self.popup.cs_scatter_flower_y_ticks_fn.select("Verdana")
        self.popup.cs_scatter_flower_y_ticks_fs.setValue(3)
        self.popup.cs_scatter_flower_y_ticks_pad.setValue(15)
        self.popup.cs_scatter_flower_y_ticks_weight.select("bold")
        self.popup.cs_scatter_flower_y_ticks_rot.setValue(60)

        self.assertEqual(self.popup.cs_scatter_flower_x_label.field.text(),
                         "X Label")
        self.assertEqual(self.popup.cs_scatter_flower_y_label.field.text(),
                         "Y Label")
        self.assertEqual(self.popup.cs_scatter_flower_mksize.field.value(), 10)
        self.assertEqual(self.popup.cs_scatter_flower_color_grad.isChecked(),
                         False)
        self.assertEqual(
            self.popup.cs_scatter_flower_color_start.fields.currentText(),
            "silver")
        self.assertEqual(
            self.popup.cs_scatter_flower_color_end.fields.currentText(),
            "brown")
        self.assertEqual(self.popup.cs_scatter_flower_color_list.field.text(),
                         "red,blue,orange")

        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_fn.fields.currentText(),
            "monospace")
        self.assertEqual(self.popup.cs_scatter_flower_x_label_fs.field.value(),
                         15)
        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_pad.field.value(), 3)
        self.assertEqual(
            self.popup.cs_scatter_flower_x_label_weight.fields.currentText(),
            "bold")

        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_fn.fields.currentText(),
            "Impact")
        self.assertEqual(self.popup.cs_scatter_flower_y_label_fs.field.value(),
                         18)
        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_pad.field.value(), 5)
        self.assertEqual(
            self.popup.cs_scatter_flower_y_label_weight.fields.currentText(),
            "semibold")

        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_fn.fields.currentText(),
            "Verdana")
        self.assertEqual(self.popup.cs_scatter_flower_x_ticks_fs.field.value(),
                         3)
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_pad.field.value(), 15)
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_weight.fields.currentText(),
            "bold")
        self.assertEqual(
            self.popup.cs_scatter_flower_x_ticks_rot.field.value(), 75)

        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_fn.fields.currentText(),
            "Verdana")
        self.assertEqual(self.popup.cs_scatter_flower_y_ticks_fs.field.value(),
                         3)
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_pad.field.value(), 15)
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_weight.fields.currentText(),
            "bold")
        self.assertEqual(
            self.popup.cs_scatter_flower_y_ticks_rot.field.value(), 60)

        self.assertNotEqual(self.popup.cs_scatter_flower_x_label.field.text(),
                            self.popup.variables["cs_scatter_flower_settings"][
                                "x_label"])
        self.assertNotEqual(self.popup.cs_scatter_flower_y_label.field.text(),
                            self.popup.variables["cs_scatter_flower_settings"][
                                "y_label"])
        self.assertNotEqual(self.popup.cs_scatter_flower_mksize.field.value(),
                            self.popup.variables["cs_scatter_flower_settings"][
                                "mksize"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_color_grad.isChecked(),
            self.popup.variables["cs_scatter_flower_settings"]["color_grad"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_color_start.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "mk_start_color"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_color_end.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["mk_end_color"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_color_list.field.text(), ','.join(
                self.popup.variables["cs_scatter_flower_settings"][
                    "color_list"]))

        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_label_fn.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["x_label_fn"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_label_fs.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["x_label_fs"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_label_pad.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["x_label_pad"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_label_weight.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "x_label_weight"])

        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_label_fn.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["y_label_fn"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_label_fs.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["y_label_fs"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_label_pad.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["y_label_pad"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_label_weight.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "y_label_weight"])

        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_ticks_fn.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["x_ticks_fn"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_ticks_fs.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["x_ticks_fs"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_ticks_pad.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["x_ticks_pad"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_ticks_weight.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "x_ticks_weight"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_x_ticks_rot.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["x_ticks_rot"])

        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_ticks_fn.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"]["y_ticks_fn"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_ticks_fs.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["y_ticks_fs"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_ticks_pad.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["y_ticks_pad"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_ticks_weight.fields.currentText(),
            self.popup.variables["cs_scatter_flower_settings"][
                "y_ticks_weight"])
        self.assertNotEqual(
            self.popup.cs_scatter_flower_y_ticks_rot.field.value(),
            self.popup.variables["cs_scatter_flower_settings"]["y_ticks_rot"])


if __name__ == "__main__":
    unittest.main()