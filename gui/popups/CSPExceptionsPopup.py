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

from core.utils import aal3tol1

from gui.popups.BasePopup import BasePopup
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox


class CSPExceptionsPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="Alpha By Residue",
                           settings_key=["csp_settings",
                                         "csp_res_exceptions"])

        self.alpha_value = self.variables["csp_settings"]["csp_res4alpha"]
        self.value_dict = {}

        for ii, res in enumerate(sorted(aal3tol1.keys())):
            self.value_dict[res] = LabelledDoubleSpinBox(
                                                         self,
                                                         text=res,
                                                         minimum=0.01,
                                                         maximum=1,
                                                         step=0.01
                                                         )
            if ii < 5:
                self.layout().addWidget(self.value_dict[res], ii, 0)
            elif 5 <= ii < 10:
                self.layout().addWidget(self.value_dict[res], ii-5, 1)
            elif 10 <= ii < 15:
                self.layout().addWidget(self.value_dict[res], ii-10, 2)
            else:
                self.layout().addWidget(self.value_dict[res], ii-15, 3)

        self.buttonBox = QDialogButtonBox(
                                          QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel |
                                          QDialogButtonBox.RestoreDefaults
                                          )

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).\
            clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 6, 2, 1, 2)
        self.get_values()

    def set_values(self):
        tmp_dict = {}
        for key, value in self.value_dict.items():
            tmp_dict[aal3tol1[key]] = round(value.field.value(), 2)
        self.local_variables.update(tmp_dict)
        self.accept()

    def get_values(self):
        for key, value in self.value_dict.items():
            if aal3tol1[key] in self.local_variables.keys():
                value.field.setValue(self.local_variables[aal3tol1[key]])
            else:
                value.field.setValue(self.alpha_value)

    def get_defaults(self):
        defaults = self.defaults["csp_settings"]["csp_res_exceptions"]
        for key, value in self.value_dict.items():
            if aal3tol1[key] in defaults.keys():
                value.field.setValue(defaults[aal3tol1[key]])
            else:
                value.field.setValue(self.alpha_value)
