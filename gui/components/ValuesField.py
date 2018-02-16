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

DISALLOWED_CHARS = [
    '.',
    ':',
    '"',
    '/',
    '\\',
    '°',
    "'",
    '*',
    '?',
    '!',
    ';'
]

from PyQt5.QtWidgets import QLineEdit, QMessageBox, QSizePolicy


class ValueField(QLineEdit):
    """
    QLineEdit that enables settings different conditions in the upper
    section of the PeaklistSelectionArea.

    Parameters:
        parent(QWidget): parent widget
        index(int): index of the condition in the conditions list
        dim(str): x, y, or z. determines dimension in Farseer-NMR Cube.
        valuesDict(dict): dictionary containing values for conditions.

    Methods:
        .updateValuesDict()
    """
    def __init__(self, parent, index, dim, valuesDict):
        QLineEdit.__init__(self, parent)
        self.index = index
        self.dim = dim
        self.textChanged.connect(self.updateValuesDict)
        self.valuesDict = valuesDict
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Invalid Characters in Condition Name")
        self.msg.setInformativeText(
"""These characters:
 . : " / \ ° ' * ? ! ; 
cannot be used in condition names."""
        )
        self.msg.setWindowTitle("Invalid Characters")
        self.msg.setStandardButtons(QMessageBox.Ok)


    def updateValuesDict(self, value):

        if any(substr in DISALLOWED_CHARS for substr in value):
            self.msg.exec_()
            self.setText(value[:-1])
            return

        self.valuesDict[self.dim][self.index] = value


    def dropEvent(self, event):
        event.ignore()
        return
