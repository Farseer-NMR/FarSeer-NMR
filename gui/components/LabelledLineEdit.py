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
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout

from gui.components.ModifiedLineEdit import ModifiedLineEdit


class LabelledLineEdit(QWidget):
    """
    A combination of a QLabel and a ModifiedLineWidget in a single QWidget.
    Principal methods of QDoubleSpinBox are re-implemented to make behaviour
    more native to a standard QDoubleSpinBox.

    Parameters:
        parent (QWidget): specifies the parent widget containing the QLabel
            and the ModifiedLineWidget.
        text (str): text to be presented in the QLabel field.

    Methods:
        .setText (str)
        .set_callback (function)
        """
    def __init__(self, parent, text, callback=None):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = ModifiedLineEdit(self)

        self.layout().addWidget(label)
        self.layout().addWidget(self.field)

        if callback:
            self.set_callback(callback)

    def set_callback(self, callback):
        self.field.textModified.connect(callback)

    def setText(self, text):
        self.field.setText(text)
