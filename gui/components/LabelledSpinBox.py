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
from PyQt5.QtWidgets import QWidget, QSpinBox, QLabel, QHBoxLayout

class LabelledSpinBox(QWidget):
    """
    A combination of a QLabel and a QDoubleSpinBox in a single QWidget.
    Principal methods of QDoubleSpinBox are re-implemented to make behaviour
    more native to a standard QDoubleSpinBox.

    Parameters:
        parent (QWidget): specifies the parent widget containing the QLabel
            and the QSpinBox.
        text (str): text to be presented in the QLabel field.
        callback (func): a function to be called when the QSpinBox
            valueChanged() signal is emitted.
        maximum (float): maximum value the QSpinBox can take.
        minimum (float): minimum value the QSpinBox can take.
        step (float): determines how the value is incremented by scrolling
            or by clicking the up/down buttons.


    Methods:
        .setValue(float)
        .set_callback(function)
        """
    def __init__(self, parent, text, callback=None, minimum=-100000, maximum=100000, step=1):
        QWidget.__init__(self, parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = QSpinBox()
        self.layout().addWidget(label)
        self.layout().addWidget(self.field)
        
        if minimum:
            self.field.setMinimum(minimum)
        
        if maximum:
            self.field.setMaximum(maximum)
        
        if step:
            self.field.setSingleStep(step)
        
        if callback:
            self.set_callback(callback)

    def setValue(self, value):
        if value:
            self.field.setValue(value)
        else:
            self.field.setValue(0)

    def set_callback(self, callback):
        self.field.valueChanged.connect(callback)
