import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication

from core.utils import get_default_config_path
from gui.popups.GeneralResidueEvolution import GeneralResidueEvolution

app = QApplication(sys.argv)

from core.fslibs.Variables import Variables

class Test_GeneralResidueEvolutionPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["revo_settings"]
        fin.close()

        self.popup = GeneralResidueEvolution()
        self.variable_keys = tuple(self.popup.variables["revo_settings"].keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())


    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(self.popup.do_revo_fit.isChecked(), 
                         self.defaults["perform_resevo_fitting"]) 
        self.assertEqual(self.popup.revo_subtitle_fn.fields.currentText(), 
                         self.defaults["subtitle_fn"])
        self.assertEqual(self.popup.revo_subtitle_fs.field.value(), 
                         self.defaults["subtitle_fs"])
        self.assertEqual(self.popup.revo_subtitle_pad.field.value(), 
                         self.defaults["subtitle_pad"])
        self.assertEqual(self.popup.revo_subtitle_weight.fields.currentText(), 
                         self.defaults["subtitle_weight"])
        self.assertEqual(self.popup.revo_x_label_fn.fields.currentText(), 
                         self.defaults["x_label_fn"])
        self.assertEqual(self.popup.revo_x_label_fs.field.value(), 
                         self.defaults["x_label_fs"])
        self.assertEqual(self.popup.revo_x_label_pad.field.value(), 
                         self.defaults["x_label_pad"])
        self.assertEqual(self.popup.revo_x_label_weight.fields.currentText(), 
                         self.defaults["x_label_weight"])
        self.assertEqual(self.popup.revo_y_label_fn.fields.currentText(), 
                         self.defaults["y_label_fn"])
        self.assertEqual(self.popup.revo_y_label_fs.field.value(), 
                         self.defaults["y_label_fs"])
        self.assertEqual(self.popup.revo_y_label_pad.field.value(), 
                         self.defaults["y_label_pad"])
        self.assertEqual(self.popup.revo_y_label_weight.fields.currentText(), 
                         self.defaults["y_label_weight"])
        self.assertEqual(self.popup.revo_x_ticks_fn.fields.currentText(), 
                         self.defaults["x_ticks_fn"])
        self.assertEqual(self.popup.revo_x_ticks_fs.field.value(), 
                         self.defaults["x_ticks_fs"])
        self.assertEqual(self.popup.revo_x_ticks_pad.field.value(), 
                         self.defaults["x_ticks_pad"])
        self.assertEqual(self.popup.revo_x_ticks_weight.fields.currentText(), 
                         self.defaults["x_ticks_weight"])
        self.assertEqual(self.popup.revo_x_ticks_rotation.field.value(), 
                         self.defaults["x_ticks_rot"])
        self.assertEqual(self.popup.revo_y_ticks_fn.fields.currentText(), 
                         self.defaults["y_ticks_fn"])
        self.assertEqual(self.popup.revo_y_ticks_fs.field.value(), 
                         self.defaults["y_ticks_fs"])
        self.assertEqual(self.popup.revo_y_ticks_pad.field.value(), 
                         self.defaults["y_ticks_pad"])
        self.assertEqual(self.popup.revo_y_ticks_weight.fields.currentText(), 
                         self.defaults["y_ticks_weight"])
        self.assertEqual(self.popup.revo_y_ticks_rot.field.value(), 
                         self.defaults["y_ticks_rot"])
        self.assertEqual(self.popup.titration_x_values.field.text(), 
            ','.join([str(x) for x in self.defaults["titration_x_values"]]))

    def test_set_values(self):
        self.popup.do_revo_fit.setChecked(True)
        self.popup.revo_subtitle_fn.select('Courier New')
        self.popup.revo_subtitle_fs.setValue(55)
        self.popup.revo_subtitle_pad.setValue(2)
        self.popup.revo_subtitle_weight.select("light")
        self.popup.revo_x_label_fn.select("Times New Roman")
        self.popup.revo_x_label_fs.setValue(5)
        self.popup.revo_x_label_pad.setValue(4)
        self.popup.revo_x_label_weight.select("semibold")
        self.popup.revo_y_label_fn.select("Courier New")
        self.popup.revo_y_label_fs.setValue(99)
        self.popup.revo_y_label_pad.setValue(32)

        self.popup.revo_y_label_weight.select("bold")
        self.popup.revo_x_ticks_fn.select("monospace")
        self.popup.revo_x_ticks_fs.setValue(13)
        self.popup.revo_x_ticks_pad.setValue(8)
        self.popup.revo_x_ticks_weight.select("bold")
        self.popup.revo_x_ticks_rotation.setValue(89)
        self.popup.revo_y_ticks_fn.select("Verdana")
        self.popup.revo_y_ticks_fs.setValue(76)
        self.popup.revo_y_ticks_pad.setValue(84)
        self.popup.revo_y_ticks_weight.select("light")
        self.popup.revo_y_ticks_rot.setValue(15)
        self.popup.titration_x_values.field.setText(','.join(["1.0","2.0",
                                                              "3.0",
                                                              "4.0","5.0"]))

        self.popup.set_values()
        
        self.assertEqual(self.popup.do_revo_fit.isChecked(), True)
        self.assertEqual(self.popup.do_revo_fit.isChecked(),
                            self.popup.variables["revo_settings"][
                                "perform_resevo_fitting"])
        self.assertEqual(self.popup.revo_subtitle_fn.fields.currentText(),
                         "Courier New")
        self.assertEqual(self.popup.revo_subtitle_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["subtitle_fn"])
        self.assertEqual(self.popup.revo_subtitle_fs.field.value(), 55)
        self.assertEqual(self.popup.revo_subtitle_fs.field.value(),
                         self.popup.variables["revo_settings"]["subtitle_fs"])
        self.assertEqual(self.popup.revo_subtitle_pad.field.value(), 2)
        self.assertEqual(self.popup.revo_subtitle_pad.field.value(),
                         self.popup.variables["revo_settings"]["subtitle_pad"])
        self.assertEqual(self.popup.revo_subtitle_weight.fields.currentText(

        ), "light")
        self.assertEqual(self.popup.revo_subtitle_weight.fields.currentText(),
                         self.popup.variables["revo_settings"]["subtitle_weight"])
        self.assertEqual(self.popup.revo_x_label_fn.fields.currentText(),
                         "Times New Roman")
        self.assertEqual(self.popup.revo_x_label_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["x_label_fn"])
        self.assertEqual(self.popup.revo_x_label_fs.field.value(), 5)
        self.assertEqual(self.popup.revo_x_label_fs.field.value(),
                         self.popup.variables["revo_settings"]["x_label_fs"])
        self.assertEqual(self.popup.revo_x_label_pad.field.value(), 4)
        self.assertEqual(self.popup.revo_x_label_pad.field.value(),
                         self.popup.variables["revo_settings"]["x_label_pad"])
        self.assertEqual(self.popup.revo_x_label_weight.fields.currentText(

        ), "semibold")
        self.assertEqual(self.popup.revo_x_label_weight.fields.currentText(),
                         self.popup.variables["revo_settings"]["x_label_weight"])
        self.assertEqual(self.popup.revo_y_label_fn.fields.currentText(),
                         "Courier New")
        self.assertEqual(self.popup.revo_y_label_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["y_label_fn"])
        self.assertEqual(self.popup.revo_y_label_fs.field.value(), 99)
        self.assertEqual(self.popup.revo_y_label_fs.field.value(),
                         self.popup.variables["revo_settings"]["y_label_fs"])
        self.assertEqual(self.popup.revo_y_label_pad.field.value(), 32)
        self.assertEqual(self.popup.revo_y_label_pad.field.value(),
                         self.popup.variables["revo_settings"]["y_label_pad"])
        self.assertEqual(self.popup.revo_y_label_weight.fields.currentText(

        ), "bold")
        self.assertEqual(self.popup.revo_y_label_weight.fields.currentText(),
                         self.popup.variables["revo_settings"]["y_label_weight"])
        self.assertEqual(self.popup.revo_x_ticks_fn.fields.currentText(),
                         "monospace")
        self.assertEqual(self.popup.revo_x_ticks_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["x_ticks_fn"])
        self.assertEqual(self.popup.revo_x_ticks_fs.field.value(), 13)
        self.assertEqual(self.popup.revo_x_ticks_fs.field.value(),
                         self.popup.variables["revo_settings"]["x_ticks_fs"])
        self.assertEqual(self.popup.revo_x_ticks_pad.field.value(), 8)
        self.assertEqual(self.popup.revo_x_ticks_pad.field.value(),
                         self.popup.variables["revo_settings"]["x_ticks_pad"])
        self.assertEqual(self.popup.revo_x_ticks_weight.fields.currentText(

        ), "bold")
        self.assertEqual(self.popup.revo_x_ticks_weight.fields.currentText(),
                         self.popup.variables["revo_settings"]["x_ticks_weight"])
        self.assertEqual(self.popup.revo_x_ticks_rotation.field.value(), 89)
        self.assertEqual(self.popup.revo_x_ticks_rotation.field.value(),
                         self.popup.variables["revo_settings"]["x_ticks_rot"])
        self.assertEqual(self.popup.revo_y_ticks_fn.fields.currentText(),
                         "Verdana")
        self.assertEqual(self.popup.revo_y_ticks_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["y_ticks_fn"])
        self.assertEqual(self.popup.revo_y_ticks_fs.field.value(), 76)
        self.assertEqual(self.popup.revo_y_ticks_fs.field.value(),
                         self.popup.variables["revo_settings"]["y_ticks_fs"])
        self.assertEqual(self.popup.revo_y_ticks_pad.field.value(), 84)
        self.assertEqual(self.popup.revo_y_ticks_pad.field.value(),
                         self.popup.variables["revo_settings"]["y_ticks_pad"])
        self.assertEqual(self.popup.revo_y_ticks_weight.fields.currentText(

        ), "light")
        self.assertEqual(self.popup.revo_y_ticks_weight.fields.currentText(),
                         self.popup.variables["revo_settings"]["y_ticks_weight"])
        self.assertEqual(self.popup.revo_y_ticks_rot.field.value(), 15)
        self.assertEqual(self.popup.revo_y_ticks_rot.field.value(),
                         self.popup.variables["revo_settings"]["y_ticks_rot"])
        self.assertEqual(self.popup.titration_x_values.field.text(), '1.0,'
                                                                     '2.0,3.0,'
                                                                      '4.0,'
                                                                     '5.0')
        self.assertEqual(self.popup.titration_x_values.field.text(),
                         ','.join([str(x) for x in self.popup.variables["revo_settings"][
                             "titration_x_values"]]))

    def test_values_not_set(self):
        self.popup.do_revo_fit.setChecked(True)
        self.popup.revo_subtitle_fn.select('Courier New')
        self.popup.revo_subtitle_fs.setValue(55)
        self.popup.revo_subtitle_pad.setValue(2)
        self.popup.revo_subtitle_weight.select("light")
        self.popup.revo_x_label_fn.select("Times New Roman")
        self.popup.revo_x_label_fs.setValue(5)
        self.popup.revo_x_label_pad.setValue(4)
        self.popup.revo_x_label_weight.select("semibold")
        self.popup.revo_y_label_fn.select("Courier New")
        self.popup.revo_y_label_fs.setValue(99)
        self.popup.revo_y_label_pad.setValue(32)

        self.popup.revo_y_label_weight.select("bold")
        self.popup.revo_x_ticks_fn.select("monospace")
        self.popup.revo_x_ticks_fs.setValue(13)
        self.popup.revo_x_ticks_pad.setValue(8)
        self.popup.revo_x_ticks_weight.select("bold")
        self.popup.revo_x_ticks_rotation.setValue(89)
        self.popup.revo_y_ticks_fn.select("Verdana")
        self.popup.revo_y_ticks_fs.setValue(76)
        self.popup.revo_y_ticks_pad.setValue(84)
        self.popup.revo_y_ticks_weight.select("light")
        self.popup.revo_y_ticks_rot.setValue(15)
        self.popup.titration_x_values.field.setText(','.join(["1.0", "2.0",
                                                              "3.0",
                                                              "4.0", "5.0"]))


        self.assertEqual(self.popup.do_revo_fit.isChecked(), True)
        self.assertNotEqual(self.popup.do_revo_fit.isChecked(),
                         self.popup.variables["revo_settings"][
                             "perform_resevo_fitting"])
        self.assertEqual(self.popup.revo_subtitle_fn.fields.currentText(),
                         "Courier New")
        self.assertNotEqual(self.popup.revo_subtitle_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["subtitle_fn"])
        self.assertEqual(self.popup.revo_subtitle_fs.field.value(), 55)
        self.assertNotEqual(self.popup.revo_subtitle_fs.field.value(),
                         self.popup.variables["revo_settings"]["subtitle_fs"])
        self.assertEqual(self.popup.revo_subtitle_pad.field.value(), 2)
        self.assertNotEqual(self.popup.revo_subtitle_pad.field.value(),
                         self.popup.variables["revo_settings"]["subtitle_pad"])
        self.assertEqual(self.popup.revo_subtitle_weight.fields.currentText(

        ), "light")
        self.assertNotEqual(self.popup.revo_subtitle_weight.fields.currentText(),
                         self.popup.variables["revo_settings"][
                             "subtitle_weight"])
        self.assertEqual(self.popup.revo_x_label_fn.fields.currentText(),
                         "Times New Roman")
        self.assertNotEqual(self.popup.revo_x_label_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["x_label_fn"])
        self.assertEqual(self.popup.revo_x_label_fs.field.value(), 5)
        self.assertNotEqual(self.popup.revo_x_label_fs.field.value(),
                         self.popup.variables["revo_settings"]["x_label_fs"])
        self.assertEqual(self.popup.revo_x_label_pad.field.value(), 4)
        self.assertNotEqual(self.popup.revo_x_label_pad.field.value(),
                         self.popup.variables["revo_settings"]["x_label_pad"])
        self.assertEqual(self.popup.revo_x_label_weight.fields.currentText(

        ), "semibold")
        self.assertNotEqual(self.popup.revo_x_label_weight.fields.currentText(),
                         self.popup.variables["revo_settings"][
                             "x_label_weight"])
        self.assertEqual(self.popup.revo_y_label_fn.fields.currentText(),
                         "Courier New")
        self.assertNotEqual(self.popup.revo_y_label_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["y_label_fn"])
        self.assertEqual(self.popup.revo_y_label_fs.field.value(), 99)
        self.assertNotEqual(self.popup.revo_y_label_fs.field.value(),
                         self.popup.variables["revo_settings"]["y_label_fs"])
        self.assertEqual(self.popup.revo_y_label_pad.field.value(), 32)
        self.assertNotEqual(self.popup.revo_y_label_pad.field.value(),
                         self.popup.variables["revo_settings"]["y_label_pad"])
        self.assertEqual(self.popup.revo_y_label_weight.fields.currentText(

        ), "bold")
        self.assertNotEqual(self.popup.revo_y_label_weight.fields.currentText(),
                         self.popup.variables["revo_settings"][
                             "y_label_weight"])
        self.assertEqual(self.popup.revo_x_ticks_fn.fields.currentText(),
                         "monospace")
        self.assertNotEqual(self.popup.revo_x_ticks_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["x_ticks_fn"])
        self.assertEqual(self.popup.revo_x_ticks_fs.field.value(), 13)
        self.assertNotEqual(self.popup.revo_x_ticks_fs.field.value(),
                         self.popup.variables["revo_settings"]["x_ticks_fs"])
        self.assertEqual(self.popup.revo_x_ticks_pad.field.value(), 8)
        self.assertNotEqual(self.popup.revo_x_ticks_pad.field.value(),
                         self.popup.variables["revo_settings"]["x_ticks_pad"])
        self.assertEqual(self.popup.revo_x_ticks_weight.fields.currentText(

        ), "bold")
        self.assertNotEqual(self.popup.revo_x_ticks_weight.fields.currentText(),
                         self.popup.variables["revo_settings"][
                             "x_ticks_weight"])
        self.assertEqual(self.popup.revo_x_ticks_rotation.field.value(), 89)
        self.assertNotEqual(self.popup.revo_x_ticks_rotation.field.value(),
                         self.popup.variables["revo_settings"]["x_ticks_rot"])
        self.assertEqual(self.popup.revo_y_ticks_fn.fields.currentText(),
                         "Verdana")
        self.assertNotEqual(self.popup.revo_y_ticks_fn.fields.currentText(),
                         self.popup.variables["revo_settings"]["y_ticks_fn"])
        self.assertEqual(self.popup.revo_y_ticks_fs.field.value(), 76)
        self.assertNotEqual(self.popup.revo_y_ticks_fs.field.value(),
                         self.popup.variables["revo_settings"]["y_ticks_fs"])
        self.assertEqual(self.popup.revo_y_ticks_pad.field.value(), 84)
        self.assertNotEqual(self.popup.revo_y_ticks_pad.field.value(),
                         self.popup.variables["revo_settings"]["y_ticks_pad"])
        self.assertEqual(self.popup.revo_y_ticks_weight.fields.currentText(

        ), "light")
        self.assertNotEqual(self.popup.revo_y_ticks_weight.fields.currentText(),
                         self.popup.variables["revo_settings"][
                             "y_ticks_weight"])
        self.assertEqual(self.popup.revo_y_ticks_rot.field.value(), 15)
        self.assertNotEqual(self.popup.revo_y_ticks_rot.field.value(),
                         self.popup.variables["revo_settings"]["y_ticks_rot"])
        self.assertEqual(self.popup.titration_x_values.field.text(), '1.0,'
                                                                     '2.0,3.0,'
                                                                     '4.0,'
                                                                     '5.0')
        self.assertNotEqual(self.popup.titration_x_values.field.text(),
                         ','.join([str(x) for x in
                                   self.popup.variables["revo_settings"][
                                       "titration_x_values"]]))


if __name__ == "__main__":
    unittest.main()