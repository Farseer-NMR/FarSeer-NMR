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
from PyQt5.QtWidgets import QDialogButtonBox

from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.popups.BasePopup import BasePopup


class PreAnalysisPopup(BasePopup):
    """
    A popup for setting PRE analysis specific settings in the Farseer-NMR
    configuration.

    Parameters:
        parent(QWidget): parent widget for popup.

    Methods:
        .get_defaults()
        .get_values()
        .set_values()
    """
    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="PRE Settings", settings_key=["pre_settings"])
        self.gaussian_stdev = LabelledSpinBox(self, "Gaussian Stdev", minimum=1, step=1)
        self.gauss_x_size = LabelledSpinBox(self, "Gaussian X Size", minimum=1, step=1)
        self.layout().addWidget(self.gauss_x_size, 0, 0)
        self.layout().addWidget(self.gaussian_stdev, 1, 0)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel |
            QDialogButtonBox.RestoreDefaults
            )
        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)
        self.layout().addWidget(self.buttonBox, 2, 0)
        self.get_values()

    def get_defaults(self):
        self.gauss_x_size.field.setValue(self.defaults["gauss_x_size"])
        self.gaussian_stdev.field.setValue(self.defaults["gaussian_stdev"])

    def set_values(self):
        self.local_variables["gaussian_stdev"] = self.gaussian_stdev.field.value()
        self.local_variables["gauss_x_size"] = self.gauss_x_size.field.value()
        self.accept()

    def get_values(self):
        self.gaussian_stdev.setValue(self.local_variables["gaussian_stdev"])
        self.gauss_x_size.setValue(self.local_variables["gauss_x_size"])
