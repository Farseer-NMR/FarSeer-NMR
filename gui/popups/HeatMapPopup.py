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

from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.FontComboBox import FontComboBox
from gui.components.ColourBox import ColourBox
from gui.gui_utils import font_weights, line_styles
from gui.popups.BasePopup import BasePopup


class HeatMapPopup(BasePopup):
    """
    A popup for setting Heat Plot specific settings in the Farseer-NMR
    configuration.

    Parameters:
        parent(QWidget): parent widget for popup.

    Methods:
        .get_defaults()
        .get_values()
        .set_values()
    """
    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="PRE Heat Map", settings_key=["heat_map_settings"])
        self.heat_map_rows = LabelledSpinBox(self, "Rows Per Page", minimum=1, step=1)
        self.heat_map_vmin = LabelledDoubleSpinBox(self, "V Min", minimum=0, step=0.01)
        self.heat_map_vmax = LabelledDoubleSpinBox(
            self,
            "V Max",
            maximum=1,
            minimum=0,
            step=0.01
            )
        self.heat_map_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.heat_map_x_ticks_fs = LabelledDoubleSpinBox(
            self,
            "X Tick Font Size",
            minimum=0,
            step=1
            )
        self.heat_map_x_tick_pad = LabelledDoubleSpinBox(
            self,
            "X Tick Padding",
            minimum=-100,
            step=0.1
            )
        self.heat_map_x_tick_weight = LabelledCombobox(
            self,
            text="X Tick Font Weight",
            items=font_weights
            )
        self.heat_map_x_ticks_rot = LabelledSpinBox(
            self,
            "X Tick Rotation",
            maximum=360,
            minimum=0,
            step=1
            )
        self.heat_map_y_label_fn = FontComboBox(self, "Y Label Font")
        self.heat_map_y_label_fs = LabelledSpinBox(
            self,
            "Y Label Font Size",
            minimum=0,
            step=1
            )
        self.heat_map_y_label_pad = LabelledDoubleSpinBox(
            self,
            "Y Label Padding",
            minimum=-100,
            step=0.1
            )
        self.heat_map_y_label_weight = LabelledCombobox(
            self,
            text="Y Label Font Weight",
            items=font_weights
            )
        self.heat_map_right_margin = LabelledDoubleSpinBox(
            self,
            "Right Margin",
            minimum=0,
            maximum=1,
            step=0.01
            )
        self.heat_map_bottom_margin = LabelledDoubleSpinBox(
            self,
            "Bottom Margin",
            minimum=0,
            maximum=1,
            step=0.01
            )
        self.heat_map_cbar_font_size = LabelledSpinBox(
            self,
            "Colour Bar Font Size",
            minimum=0,
            step=1
            )
        self.heat_map_tag_line_color = ColourBox(self, "Tag Line Colour")
        self.heat_map_tag_ls = LabelledCombobox(self, "Tag Line Style", items=line_styles)
        self.heat_map_tag_lw = LabelledDoubleSpinBox(
            self,
            "Tag Line Width",
            minimum=0,
            step=0.1
            )
        # add buttons
        self.layout().addWidget(self.heat_map_rows, 0, 0)
        self.layout().addWidget(self.heat_map_vmin, 1, 0)
        self.layout().addWidget(self.heat_map_vmax, 2, 0)
        self.layout().addWidget(self.heat_map_right_margin, 3, 0)
        self.layout().addWidget(self.heat_map_bottom_margin, 4, 0)
        self.layout().addWidget(self.heat_map_cbar_font_size, 5, 0)
        self.layout().addWidget(self.heat_map_tag_line_color, 6, 0)
        self.layout().addWidget(self.heat_map_tag_ls, 7, 0)
        self.layout().addWidget(self.heat_map_tag_lw, 8, 0)
        self.layout().addWidget(self.heat_map_x_ticks_fn, 0, 1)
        self.layout().addWidget(self.heat_map_x_ticks_fs, 1, 1)
        self.layout().addWidget(self.heat_map_x_ticks_rot, 2, 1)
        self.layout().addWidget(self.heat_map_x_tick_pad, 3, 1)
        self.layout().addWidget(self.heat_map_x_tick_weight, 4, 1)
        self.layout().addWidget(self.heat_map_y_label_fn, 5, 1)
        self.layout().addWidget(self.heat_map_y_label_fs, 6, 1)
        self.layout().addWidget(self.heat_map_y_label_pad, 7, 1)
        self.layout().addWidget(self.heat_map_y_label_weight, 8, 1)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel |
            QDialogButtonBox.RestoreDefaults
            )
        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)
        self.layout().addWidget(self.buttonBox, 9, 1, 1, 1)
        self.get_values()

    def get_defaults(self):
        # value
        self.heat_map_rows.setValue(self.defaults["rows"])
        self.heat_map_vmin.setValue(self.defaults["vmin"])
        self.heat_map_vmax.setValue(self.defaults["vmax"])
        self.heat_map_x_ticks_fs.setValue(self.defaults["x_ticks_fs"])
        self.heat_map_x_ticks_rot.setValue(self.defaults["x_ticks_rot"])
        self.heat_map_x_tick_pad.setValue(self.defaults["x_ticks_pad"])
        self.heat_map_y_label_fs.setValue(self.defaults["y_label_fs"])
        self.heat_map_y_label_pad.setValue(self.defaults["y_label_pad"])
        self.heat_map_right_margin.setValue(self.defaults["right_margin"])
        self.heat_map_bottom_margin.setValue(self.defaults["bottom_margin"])
        self.heat_map_cbar_font_size.setValue(self.defaults["cbar_font_size"])
        self.heat_map_tag_lw.setValue(self.defaults["tag_line_lw"])
        # select
        self.heat_map_x_ticks_fn.select(self.defaults["x_ticks_fn"])
        self.heat_map_x_tick_weight.select(self.defaults["x_ticks_weight"])
        self.heat_map_y_label_fn.select(self.defaults["y_label_fn"])
        self.heat_map_y_label_weight.select(self.defaults["y_label_weight"])
        self.heat_map_tag_ls.select(self.defaults["tag_line_ls"])
        # colour
        self.heat_map_tag_line_color.get_colour(self.defaults["tag_line_color"])
    
    def set_values(self):
        # value
        self.local_variables["rows"] = self.heat_map_rows.field.value()
        self.local_variables["vmin"] = self.heat_map_vmin.field.value()
        self.local_variables["vmax"] = self.heat_map_vmax.field.value()
        self.local_variables["x_ticks_fs"] = self.heat_map_x_ticks_fs.field.value()
        self.local_variables["x_ticks_rot"] = self.heat_map_x_ticks_rot.field.value()
        self.local_variables["x_ticks_pad"] = self.heat_map_x_tick_pad.field.value()
        self.local_variables["y_label_fs"] = self.heat_map_y_label_fs.field.value()
        self.local_variables["y_label_pad"] = self.heat_map_y_label_pad.field.value()
        self.local_variables["right_margin"] = self.heat_map_right_margin.field.value()
        self.local_variables["bottom_margin"] = self.heat_map_bottom_margin.field.value()
        self.local_variables["cbar_font_size"] = self.heat_map_cbar_font_size.field.value()
        self.local_variables["tag_line_lw"] = self.heat_map_tag_lw.field.value()
        # select
        self.local_variables["x_ticks_fn"] = self.heat_map_x_ticks_fn.fields.currentText()
        self.local_variables["x_ticks_weight"] = self.heat_map_x_tick_weight.fields.currentText()
        self.local_variables["y_label_fn"] = self.heat_map_y_label_fn.fields.currentText()
        self.local_variables["y_label_weight"] = self.heat_map_y_label_weight.fields.currentText()
        self.local_variables["tag_line_ls"] = self.heat_map_tag_ls.fields.currentText()
        # colour
        self.local_variables["tag_line_color"] = self.heat_map_tag_line_color.fields.currentText()
        #
        self.accept()

    def get_values(self):
        # value
        self.heat_map_rows.setValue(self.local_variables["rows"])
        self.heat_map_vmin.setValue(self.local_variables["vmin"])
        self.heat_map_vmax.setValue(self.local_variables["vmax"])
        self.heat_map_x_ticks_fs.setValue(self.local_variables["x_ticks_fs"])
        self.heat_map_x_ticks_rot.setValue(self.local_variables["x_ticks_rot"])
        self.heat_map_x_tick_pad.setValue(self.local_variables["x_ticks_pad"])
        self.heat_map_y_label_fs.setValue(self.local_variables["y_label_fs"])
        self.heat_map_y_label_pad.setValue(self.local_variables["y_label_pad"])
        self.heat_map_right_margin.setValue(self.local_variables["right_margin"])
        self.heat_map_bottom_margin.setValue(self.local_variables["bottom_margin"])
        self.heat_map_cbar_font_size.setValue(self.local_variables["cbar_font_size"])
        self.heat_map_tag_lw.setValue(self.local_variables["tag_line_lw"])
        # select
        self.heat_map_x_ticks_fn.select(self.local_variables["x_ticks_fn"])
        self.heat_map_x_tick_weight.select(self.local_variables["x_ticks_weight"])
        self.heat_map_y_label_fn.select(self.local_variables["y_label_fn"])
        self.heat_map_y_label_weight.select(self.local_variables["y_label_weight"])
        self.heat_map_tag_ls.select(self.local_variables["tag_line_ls"])
        # colour
        self.heat_map_tag_line_color.get_colour(self.local_variables["tag_line_color"])
