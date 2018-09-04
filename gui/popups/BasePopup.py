"""
Copyright © 2017-2018 Farseer-NMR
Simon P. Skinner and João M.C. Teixeira

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

Farseer-NMR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Farseer-NMR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
"""
import json
from PyQt5.QtWidgets import QDialog, QGridLayout, QVBoxLayout
from PyQt5 import QtCore

from core.fslibs.Variables import Variables
from core.utils import get_nested_value, get_default_config_path

defaults = json.load(open(get_default_config_path(), 'r'))

class BasePopup(QDialog):
    """
    Base QDialog for all Farseer-NMR popups.
    
    Parameters:
        parent(QWidget): parent QWidget
        settings_keys(str or list): specifies the keys to access popup specific
            settings in variables.
        title(str): name of the popup.
    
    Methods:
        .launch()
    
    """
    
    variables = Variables()._vars
    
    def __init__(self, parent, settings_key=None, title=None, layout='grid', **kw):
        QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        
        if layout == 'grid':
            grid = QGridLayout()
            grid.setAlignment(QtCore.Qt.AlignTop)
            self.setLayout(grid)
        
        if layout == 'vbox':
            v_layout = QVBoxLayout()
            v_layout.setAlignment(QtCore.Qt.AlignTop)
            self.setLayout(v_layout)
        
        if settings_key:
            if isinstance(settings_key, str):
                self.local_variables = self.variables[settings_key]
                self.defaults = defaults[settings_key]

            elif isinstance(settings_key, list):
                self.local_variables = get_nested_value(self.variables, settings_key)
                self.defaults = get_nested_value(defaults, settings_key)
    
    def launch(self):
        self.exec_()
        self.raise_()
