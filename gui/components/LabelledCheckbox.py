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
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QGridLayout
from PyQt5 import QtCore

class LabelledCheckbox(QWidget):
    """
    A combination of a QLabel and a Checkbox in a single QWidget.
    Principal methods of QCheckbox are re-implemented to make behaviour more
    native to a standard QCheckbox.

    Parameters:
        parent (QWidget): specifies the parent widget containing the QLabel
            and the QCheckbox.
        text (str): text to be presented in the QLabel field.
        callback (func): a function to be called when the checkbox isChecked()
            signal is emitted.

    Methods:
        .setEnabled(bool)
        .setChecked(bool)
        .isChecked()
    """
    
    def __init__(self, parent, text, callback=None, **kw):
        QWidget.__init__(self, parent)
        grid = QGridLayout()
        self.setObjectName("LabelledCheckbox")
        self.setLayout(grid)
        self.checkBox = QCheckBox()
        label = QLabel(text, self)
        self.layout().addWidget(self.checkBox, 0, 0)
        self.layout().addWidget(label, 0, 1)
        
        if callback:
            self.set_callback(callback)
        
        label.setAlignment(QtCore.Qt.AlignLeft)
    
    def set_callback(self, callback):
        self.checkBox.stateChanged.connect(callback)
    
    def isChecked(self):
        return self.checkBox.isChecked()
    
    def setEnabled(self, boolean):
        self.checkBox.setEnabled(boolean)
    
    def setChecked(self, boolean):
        if boolean is True:
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)
