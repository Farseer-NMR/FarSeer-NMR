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
from PyQt5.QtWidgets import QWidget, QDoubleSpinBox, QLabel, QHBoxLayout

class LabelledDoubleSpinBox(QWidget):

    def __init__(self, parent, text, callback=None, min=None, max=None, step=None, unit=None):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = QDoubleSpinBox()

        self.layout().addWidget(label)
        self.layout().addWidget(self.field)

        if callback:
            self.set_callback(callback)

        if min:
            self.field.setMinimum(min)
        if max:
            self.field.setMaximum(max)
        if step:
            self.field.setSingleStep(step)

        if unit:
            self.unit_label = QLabel(unit)
            self.layout().addWidget(self.unit_label)

    def setValue(self, value):
        if value:
            self.field.setValue(value)
        else:
            self.field.setValue(0)

    def set_callback(self, callback):
        self.field.valueChanged.connect(callback)
