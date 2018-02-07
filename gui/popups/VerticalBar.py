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

class VerticalBarPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(
                           self,
                           parent,
                           title="Vertical Bar Plot",
                           settings_key="vert_bar_settings"
                           )

        self.bar_cols = LabelledSpinBox(
                                        self,
                                        text="Columns Per Page",
                                        minimum=1,
                                        step=1
                                        )
        self.bar_rows = LabelledSpinBox(
                                        self,
                                        text="Rows Per Page",
                                        minimum=1,
                                        step=1
                                        )


        self.layout().addWidget(self.bar_cols, 0, 0)
        self.layout().addWidget(self.bar_rows, 1, 0)


        self.buttonBox = QDialogButtonBox(
                                          QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel |
                                          QDialogButtonBox.RestoreDefaults
                                          )

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).\
            clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 2, 0, 1, 1)

        self.get_values()

    def get_defaults(self):
        self.bar_cols.setValue(self.defaults["cols_page"])
        self.bar_rows.setValue(self.defaults["rows_page"])


    def get_values(self):
        self.bar_cols.setValue(self.local_variables["cols_page"])
        self.bar_rows.setValue(self.local_variables["rows_page"])

    def set_values(self):
        self.local_variables["cols_page"] = self.bar_cols.field.value()
        self.local_variables["rows_page"] = self.bar_rows.field.value()
        self.accept()
