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
from functools import partial
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QDialogButtonBox

from gui.gui_utils import font_weights
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.FontComboBox import FontComboBox
from gui.popups.BasePopup import BasePopup


class ExtendedBarPopup(BasePopup):
    """
    A popup for setting Extended Bar Plot specific settings in the Farseer-NMR
    configuration.

    Parameters:
        parent(QWidget): parent widget for popup.

    Methods:
        .get_defaults()
        .get_values()
        .set_values()
    """
    def __init__(self, parent=None, **kw):
        BasePopup.__init__(
            self,
            parent,
            title="Extended Bar Plot",
            settings_key=["extended_bar_settings"]
            )
        self.bar_cols = LabelledSpinBox(self, text="Columns Per Page", minimum=1, step=1)
        self.bar_rows = LabelledSpinBox(self, text="Rows Per Page", minimum=1, step=1)
        self.x_tick_font = FontComboBox(self, "X Tick Font")
        self.x_tick_font_size = LabelledSpinBox(self, "X Tick Font Size", minimum=0, step=1)
        self.x_tick_rotation = LabelledSpinBox(
            self,
            "X Tick Rotation",
            minimum=0,
            maximum=90,
            step=1
            )
        self.x_tick_font_weight = LabelledCombobox(
            self,
            "X Tick Font Weight",
            items=font_weights
            )
        self.x_tick_colour = LabelledCheckbox(self, "Colour X Ticks?")
        # adds widgets
        self.layout().addWidget(self.bar_cols, 0, 0)
        self.layout().addWidget(self.bar_rows, 1, 0)
        self.layout().addWidget(self.x_tick_font_size, 2, 0)
        self.layout().addWidget(self.x_tick_font, 3, 0)
        self.layout().addWidget(self.x_tick_rotation, 4, 0)
        self.layout().addWidget(self.x_tick_font_weight, 5, 0)
        self.layout().addWidget(self.x_tick_colour, 6, 0)
        # buttons
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel |
            QDialogButtonBox.RestoreDefaults
            )
        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)
        # sets widget in tab
        self.layout().addWidget(self.buttonBox, 8, 0)
        self.get_values()

    def get_defaults(self):
        # check
        self.x_tick_colour.setChecked(self.defaults["x_ticks_color_flag"])
        # values
        self.bar_cols.setValue(self.defaults["cols_page"])
        self.bar_rows.setValue(self.defaults["rows_page"])
        self.x_tick_font_size.setValue(self.defaults["x_ticks_fs"])
        self.x_tick_rotation.setValue(self.defaults["x_ticks_rot"])
        # select
        self.x_tick_font.select(self.defaults["x_ticks_fn"])
        self.x_tick_font_weight.select(self.defaults["x_ticks_weight"])

    def get_values(self):
        # checked
        self.x_tick_colour.setChecked(self.local_variables["x_ticks_color_flag"])
        # value
        self.bar_cols.setValue(self.local_variables["cols_page"])
        self.bar_rows.setValue(self.local_variables["rows_page"])
        self.x_tick_font_size.setValue(self.local_variables["x_ticks_fs"])
        self.x_tick_rotation.setValue(self.local_variables["x_ticks_rot"])
        # select
        self.x_tick_font.select(self.local_variables["x_ticks_fn"])
        self.x_tick_font_weight.select(self.local_variables["x_ticks_weight"])

    def set_values(self):
        # checked
        self.local_variables["x_ticks_color_flag"] = self.x_tick_colour.isChecked()
        # value
        self.local_variables["cols_page"] = self.bar_cols.field.value()
        self.local_variables["rows_page"] = self.bar_rows.field.value()
        self.local_variables["x_ticks_fs"] = self.x_tick_font_size.field.value()
        self.local_variables["x_ticks_rot"] = self.x_tick_rotation.field.value()
        # text
        self.local_variables["x_ticks_fn"] = str(self.x_tick_font.fields.currentText())
        self.local_variables["x_ticks_weight"] = str(self.x_tick_font_weight.fields.currentText())
        self.accept()
