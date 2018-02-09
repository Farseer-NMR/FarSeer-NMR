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
from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout
from PyQt5 import QtCore


class LabelledCombobox(QWidget):
    """
    A combination of a QLabel and a QCombobox in a single QWidget.
    Principal methods of QCombobox are re-implemented to make behaviour more
    native to a standard QCombobox.

    Parameters:
        parent (QWidget): specifies the parent widget containing the QLabel
            and the QCombobox.
        text (str): text to be presented in the QLabel field.
        callback (func): a function to be called when the QCombobox
            currentTextChanged signal is emitted.

    Methods:
        .select(str)
        .set_callback(function)
        .addItem(str)
        """
    def __init__(self, parent, text=None, items=None, callback=None):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.fields = QComboBox()
        self.texts = []
        if items:
            [self.addItem(item) for item in items]

        self.layout().addWidget(label)
        self.layout().addWidget(self.fields)

        if callback:
            self.set_callback(callback)

    def select(self, text):
        index = self.fields.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.fields.setCurrentIndex(index)

    def set_callback(self, callback):
        self.fields.currentTextChanged.connect(callback)

    def addItem(self, text):

        self.fields.addItem(text)
        self.texts.append(text)
