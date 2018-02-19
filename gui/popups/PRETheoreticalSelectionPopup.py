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
from collections import OrderedDict
from functools import partial

from PyQt5.QtWidgets import (QDialogButtonBox, QFileDialog, QHBoxLayout,
                             QLabel, QPushButton, QWidget)

from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.popups.BasePopup import BasePopup


class PRETheoreticalSelectionPopup(BasePopup):
    """
    A popup for setting Theoretical PRE file path settings in the Farseer-NMR
    configuration.

    Parameters:
        parent(QWidget): parent widget for popup.

    Methods:
        .get_defaults()
        .get_values()
        .set_values()
        .add_field(str, str)
        .raise_file_dialog(QLineEdit)
    """
    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="Theoretical PRE Selection Popup",
                           settings_key=["pre_files"], layout='vbox')

        label = QLabel("Y conditions", self)
        self.layout().addWidget(label)
        self.cond_widget_dict = {}

        self.pre_files = OrderedDict(self.local_variables.items())

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)

        self.layout().addWidget(self.buttonBox)

        self.get_values()

    def get_values(self):
        if self.pre_files:
            for cond_name, pre_path in self.pre_files.items():
                self.add_field(cond_name, pre_path)
        elif self.variables["conditions"]["y"]:
            for cond in self.variables["conditions"]["y"]:
                self.add_field(cond, '')

    def set_values(self):
        for name, widget in self.cond_widget_dict.items():
            self.pre_files[name] = widget[0].field.text()
        self.local_variables.update(self.pre_files)
        self.accept()

    def add_field(self, cond_name, pre_path):

        widget = QWidget()
        widget_layout = QHBoxLayout()
        widget.setLayout(widget_layout)
        line_edit = LabelledLineEdit(self, cond_name)
        if pre_path:
            line_edit.setText(pre_path)
        button = QPushButton("...", self)
        line_edit.field.setMinimumWidth(250)
        button.setMaximumWidth(25)
        button.clicked.connect(partial(self.raise_file_dialog, line_edit))
        widget.layout().addWidget(line_edit)
        widget.layout().addWidget(button)
        widget_items = (line_edit, button)
        self.cond_widget_dict[cond_name] = widget_items
        self.layout().addWidget(widget)

        return

    def raise_file_dialog(self, file_field):
        pre_file = QFileDialog.getOpenFileName(
                                                 self,
                                                 "Select Theo. PRE File",
                                                 "",
                                                 "*.pre"
                                                )
        if pre_file:
            file_field.field.setText(pre_file[0])
