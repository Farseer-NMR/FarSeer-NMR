import sys
import unittest
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import os
from core.utils import get_default_config_path

from gui.popups.SeriesPlotPopup import SeriesPlotPopup

app = QApplication(sys.argv)

from core.fslibs.Variables import Variables

class Test_BarPlotPopup(unittest.TestCase):

    def setUp(self):
        ''' Create the popup'''
        default_config = '/Users/fbssps/PycharmProjects/FarSeer-NMR/current/default_config.json'

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

        pass

    def test_change_variables(self):
        pass


    def test_set_values(self):
        pass


if __name__ == "__main__":
    unittest.main()