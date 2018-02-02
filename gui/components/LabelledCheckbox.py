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

    def __init__(self, parent, text, callback=None, fixed=False, **kw):
        QWidget.__init__(self, parent)
        grid = QGridLayout()
        self.setObjectName("LabelledCheckbox")
        self.setLayout(grid)
        self.checkBox = QCheckBox()

        label = QLabel(text, self)

        self.layout().addWidget(self.checkBox, 0, 0)
        self.layout().addWidget(label, 0, 1)
        # if fixed:
        #     self.setFixedWidth(50)

        if callback:
            self.setCallback(callback)

        label.setAlignment(QtCore.Qt.AlignLeft)

    def setCallback(self, callback):
        self.checkBox.stateChanged.connect(callback)

    def isChecked(self):
        return self.checkBox.isChecked()

    def setEnabled(self, bool):
        self.checkBox.setEnabled(bool)

    def setChecked(self, value):
        if value is not None:
            self.checkBox.setChecked(value)
        else:
            self.checkBox.setChecked(False)
