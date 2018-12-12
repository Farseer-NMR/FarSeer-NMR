import sys
import os
import unittest
import json
from PyQt5.QtWidgets import QApplication

from gui.popups.FastaSelectionPopup import FastaSelectionPopup
from core.utils import get_default_config_path
from core.fslibs.Variables import Variables

app = QApplication(sys.argv)


class Test_FastaSelectionPopup(unittest.TestCase):

    def setUp(self):
        """ Create the popup"""

        default_config_path = get_default_config_path()
        Variables().read(default_config_path)
        fin = open(default_config_path, 'r')
        self.defaults = json.load(fin)["fasta_files"]
        fin.close()

        self.popup = FastaSelectionPopup()
        self.variable_keys = tuple(self.popup.variables.keys())
        self.local_variable_keys = tuple(self.popup.local_variables.keys())

    def test_defaults(self):
        """Test popup reads and sets default variables"""

        self.assertEqual(list(self.popup.cond_widget_dict.keys()), [''])

    def test_set_values(self):
        self.popup.add_field('mut1', os.path.join('test' ,'path', '1'))
        self.popup.add_field('mut2', os.path.join('test' ,'path', '2'))
        self.popup.add_field('mut3', os.path.join('test' ,'path', '3'))

        self.popup.set_values()

        self.assertIn("mut1", self.popup.cond_widget_dict.keys())
        self.assertIn("mut2", self.popup.cond_widget_dict.keys())
        self.assertIn("mut3", self.popup.cond_widget_dict.keys())

        self.assertEqual(self.popup.cond_widget_dict["mut1"][0].field.text(),
                         os.path.join('test' ,'path', '1'))
        self.assertEqual(self.popup.cond_widget_dict["mut2"][0].field.text(),
                         os.path.join('test' ,'path', '2'))
        self.assertEqual(self.popup.cond_widget_dict["mut3"][0].field.text(),
                         os.path.join('test' ,'path', '3'))

        self.assertEqual(self.popup.variables["fasta_files"]["mut1"],
                         os.path.join('test' ,'path', '1'))
        self.assertEqual(self.popup.variables["fasta_files"]["mut2"],
                         os.path.join('test' ,'path', '2'))
        self.assertEqual(self.popup.variables["fasta_files"]["mut3"],
                         os.path.join('test' ,'path', '3'))

    def test_values_not_set(self):
        self.popup.add_field('mut1', os.path.join('test' ,'path', '1'))
        self.popup.add_field('mut2', os.path.join('test' ,'path', '2'))
        self.popup.add_field('mut3', os.path.join('test' ,'path', '3'))

        self.assertIn("mut1", self.popup.cond_widget_dict.keys())
        self.assertIn("mut2", self.popup.cond_widget_dict.keys())
        self.assertIn("mut3", self.popup.cond_widget_dict.keys())

        self.assertEqual(self.popup.cond_widget_dict["mut1"][0].field.text(),
                         os.path.join('test' ,'path', '1'))
        self.assertEqual(self.popup.cond_widget_dict["mut2"][0].field.text(),
                         os.path.join('test' ,'path', '2'))
        self.assertEqual(self.popup.cond_widget_dict["mut3"][0].field.text(),
                         os.path.join('test' ,'path', '3'))

        self.assertNotIn("mut1", self.popup.variables["fasta_files"].keys())
        self.assertNotIn("mut2", self.popup.variables["fasta_files"].keys())
        self.assertNotIn("mut3", self.popup.variables["fasta_files"].keys())


if __name__ == "__main__":
    unittest.main()
