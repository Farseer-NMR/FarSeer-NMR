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

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="PRE Heat Map",
                           settings_key=["heat_map_settings"])

        self.heat_map_rows = LabelledSpinBox(self, "Rows Per Page", min=1, step=1)
        self.heat_map_vmin = LabelledDoubleSpinBox(self, "V Min", min=0, step=0.01)
        self.heat_map_vmax = LabelledDoubleSpinBox(self, "V Max", max=1, min=0, step=0.01)
        self.heat_map_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.heat_map_x_ticks_fs = LabelledDoubleSpinBox(self, "X Tick Font Size", min=0, step=1)
        self.heat_map_x_tick_pad = LabelledDoubleSpinBox(self, "X Tick Padding", min=-100, step=0.1)
        self.heat_map_x_tick_weight = LabelledCombobox(self, text="X Tick Font Weight", items=font_weights)
        self.heat_map_x_ticks_rot = LabelledSpinBox(self, "X Tick Rotation", max=360, min=0, step=1)
        self.heat_map_y_label_fn = FontComboBox(self, "Y Label Font")
        self.heat_map_y_label_fs = LabelledSpinBox(self, "Y Label Font Size", min=0, step=1)
        self.heat_map_y_label_pad = LabelledDoubleSpinBox(self, "Y Label Padding", min=-100, step=0.1)
        self.heat_map_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=font_weights)
        self.heat_map_right_margin = LabelledDoubleSpinBox(self, "Right Margin", min=0, max=1, step=0.01)
        self.heat_map_bottom_margin = LabelledDoubleSpinBox(self, "Bottom Margin", min=0, max=1, step=0.01)
        self.heat_map_cbar_font_size = LabelledSpinBox(self, "Colour Bar Font Size", min=0, step=1)
        self.heat_map_tag_line_color = ColourBox(self, "Tag Line Colour")
        self.heat_map_tag_ls = LabelledCombobox(self, "Tag Line Style", items=line_styles)
        self.heat_map_tag_lw = LabelledDoubleSpinBox(self, "Tag Line Width", min=0, step=0.1)


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



        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 9, 1, 1, 1)

        self.get_values()

    def get_defaults(self):
        self.heat_map_rows.setValue(self.default["rows"])
        self.heat_map_vmin.setValue(self.default["vmin"])
        self.heat_map_vmax.setValue(self.default["vmax"])
        self.heat_map_x_ticks_fs.setValue(self.default["x_ticks_fs"])
        self.heat_map_x_ticks_rot.setValue(self.default["x_ticks_rot"])
        self.heat_map_x_ticks_fn.select(self.default["x_ticks_fn"])
        self.heat_map_x_tick_pad.setValue(self.default["x_ticks_pad"])
        self.heat_map_x_tick_weight.select(self.default["x_ticks_weight"])
        self.heat_map_y_label_fs.setValue(self.default["y_label_fs"])
        self.heat_map_y_label_pad.setValue(self.default["y_label_pad"])
        self.heat_map_y_label_fn.select(self.default["y_label_fn"])
        self.heat_map_y_label_weight.select(self.default["y_label_weight"])
        self.heat_map_right_margin.setValue(self.default["right_margin"])
        self.heat_map_bottom_margin.setValue(self.default["bottom_margin"])
        self.heat_map_cbar_font_size.setValue(self.default["cbar_font_size"])
        self.heat_map_tag_line_color.select(self.default["tag_line_color"])
        self.heat_map_tag_ls.select(self.default["tag_line_ls"])
        self.heat_map_tag_lw.setValue(self.default["tag_line_lw"])

    def set_values(self):
        self.local_variables["rows"] = self.heat_map_rows.field.value()
        self.local_variables["vmin"] = self.heat_map_vmin.field.value()
        self.local_variables["vmax"] = self.heat_map_vmax.field.value()
        self.local_variables["x_ticks_fs"] = self.heat_map_x_ticks_fs.field.value()
        self.local_variables["x_ticks_rot"] = self.heat_map_x_ticks_rot.field.value()
        self.local_variables["x_ticks_fn"] = self.heat_map_x_ticks_fn.fields.currentText()
        self.local_variables["x_ticks_pad"] = self.heat_map_x_tick_pad.field.value()
        self.local_variables["x_ticks_weight"] = self.heat_map_x_tick_weight.fields.currentText()
        self.local_variables["y_label_fs"] = self.heat_map_y_label_fs.field.value()
        self.local_variables["y_label_pad"] = self.heat_map_y_label_pad.field.value()
        self.local_variables["y_label_fn"] = self.heat_map_y_label_fn.fields.currentText()
        self.local_variables["y_label_weight"] = self.heat_map_y_label_weight.fields.currentText()
        self.local_variables["right_margin"] = self.heat_map_right_margin.field.value()
        self.local_variables["bottom_margin"] = self.heat_map_bottom_margin.field.value()
        self.local_variables["cbar_font_size"] = self.heat_map_cbar_font_size.field.value()
        self.local_variables["tag_line_color"] = self.heat_map_tag_line_color.fields.currentText()
        self.local_variables["tag_line_ls"] = self.heat_map_tag_ls.fields.currentText()
        self.local_variables["tag_line_lw"] = self.heat_map_tag_lw.field.value()
        self.variables.update(self.local_variables)
        self.accept()

    def get_values(self):
        self.heat_map_rows.setValue(self.local_variables["rows"])
        self.heat_map_vmin.setValue(self.local_variables["vmin"])
        self.heat_map_vmax.setValue(self.local_variables["vmax"])
        self.heat_map_x_ticks_fs.setValue(self.local_variables["x_ticks_fs"])
        self.heat_map_x_ticks_rot.setValue(self.local_variables["x_ticks_rot"])
        self.heat_map_x_ticks_fn.select(self.local_variables["x_ticks_fn"])
        self.heat_map_x_tick_pad.setValue(self.local_variables["x_ticks_pad"])
        self.heat_map_x_tick_weight.select(self.local_variables["x_ticks_weight"])
        self.heat_map_y_label_fs.setValue(self.local_variables["y_label_fs"])
        self.heat_map_y_label_pad.setValue(self.local_variables["y_label_pad"])
        self.heat_map_y_label_fn.select(self.local_variables["y_label_fn"])
        self.heat_map_y_label_weight.select(self.local_variables["y_label_weight"])
        self.heat_map_right_margin.setValue(self.local_variables["right_margin"])
        self.heat_map_bottom_margin.setValue(self.local_variables["bottom_margin"])
        self.heat_map_cbar_font_size.setValue(self.local_variables["cbar_font_size"])
        self.heat_map_tag_line_color.select(self.local_variables["tag_line_color"])
        self.heat_map_tag_ls.select(self.local_variables["tag_line_ls"])
        self.heat_map_tag_lw.setValue(self.local_variables["tag_line_lw"])

