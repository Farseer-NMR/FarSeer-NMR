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
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox
from gui.components.FontComboBox import FontComboBox

from gui.gui_utils import font_weights, get_colour

from gui.popups.BasePopup import BasePopup

class OscillationMapPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="Oscillation Map",
                           settings_key=["dpre_osci_settings"])

        self.dpre_osci_rows = LabelledSpinBox(self, "Number of Rows", minimum=1, step=1)
        self.dpre_osci_width = LabelledSpinBox(self, "Scale Factor for Width")
        self.dpre_osci_y_label = LabelledLineEdit(self, "Y Label")
        self.dpre_osci_y_label_fs = LabelledSpinBox(self, "Y Label Font Size", minimum=0, step=1)
        self.dpre_osci_ymax = LabelledDoubleSpinBox(self, "Y Maximum", minimum=0, step=0.1)
        self.dpre_osci_dpre_ms = LabelledSpinBox(self, "Marker Size", minimum=0, step=1)
        self.dpre_osci_dpre_alpha = LabelledDoubleSpinBox(self, "Marker Transparency", minimum=0, maximum=1, step=0.1)
        self.dpre_osci_smooth_lw = LabelledSpinBox(self, "Smoothed DPRE Line Width", minimum=0, step=1)
        self.dpre_osci_ref_color = ColourBox(self, "Reference Data Colour")
        self.dpre_osci_color_init = ColourBox(self, "Grad Start Colour")
        self.dpre_osci_color_end = ColourBox(self, "Grad End Colour")
        self.dpre_osci_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.dpre_osci_x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size", minimum=0, step=1)
        self.dpre_osci_x_ticks_pad = LabelledDoubleSpinBox(self, "X Tick Padding", minimum=-100, maximum=100, step=0.1)
        self.dpre_osci_x_ticks_weight = LabelledCombobox(self, text="X Font Weight", items=font_weights)
        self.dpre_osci_grid_color = ColourBox(self, "Grid Colour")
        self.dpre_osci_res_highlight = LabelledCheckbox(self, "Highlight Residues?")
        self.dpre_osci_res_highlight_list = LabelledLineEdit(self, "Residues to Highlight")
        self.dpre_osci_shade = LabelledCheckbox(self, "Shade Residues?")
        self.dpre_osci_regions = LabelledLineEdit(self, "Regions to Shade")
        self.dpre_osci_rh_fs = LabelledSpinBox(self, "Highlight Font Size ", minimum=0, step=1)
        self.dpre_osci_rh_y = LabelledDoubleSpinBox(self, "Residue Label Scale", minimum=0, maximum=1, step=0.01)


        self.layout().addWidget(self.dpre_osci_rows, 0, 0)
        self.layout().addWidget(self.dpre_osci_width, 1, 0)
        self.layout().addWidget(self.dpre_osci_y_label, 2, 0)
        self.layout().addWidget(self.dpre_osci_ref_color, 3, 0)
        self.layout().addWidget(self.dpre_osci_color_init, 4, 0)
        self.layout().addWidget(self.dpre_osci_color_end, 5, 0)
        self.layout().addWidget(self.dpre_osci_x_ticks_fs, 6, 0)
        self.layout().addWidget(self.dpre_osci_x_ticks_fn, 7, 0)
        self.layout().addWidget(self.dpre_osci_x_ticks_pad, 8, 0)
        self.layout().addWidget(self.dpre_osci_x_ticks_weight, 9, 0)
        self.layout().addWidget(self.dpre_osci_grid_color, 10, 0)


        self.layout().addWidget(self.dpre_osci_dpre_ms, 0, 1)
        self.layout().addWidget(self.dpre_osci_dpre_alpha, 1, 1)

        self.layout().addWidget(self.dpre_osci_y_label_fs, 2, 1)
        self.layout().addWidget(self.dpre_osci_smooth_lw, 3, 1)
        self.layout().addWidget(self.dpre_osci_res_highlight, 4, 1)
        self.layout().addWidget(self.dpre_osci_res_highlight_list, 5, 1)
        self.layout().addWidget(self.dpre_osci_shade, 6, 1)
        self.layout().addWidget(self.dpre_osci_regions, 7, 1)
        self.layout().addWidget(self.dpre_osci_rh_fs, 8, 1)
        self.layout().addWidget(self.dpre_osci_rh_y, 9, 1)
        self.layout().addWidget(self.dpre_osci_ymax, 10, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 11, 0, 2, 2)

        self.get_values()


    def set_ranges(self, field_value):
        ll = field_value.split(',')
        return [[int(x.split('-')[0]), int(x.split('-')[1])] for x in ll]

    def get_ranges(self, ranges):
        return ','.join(["%s-%s" % (x[0], x[1]) for x in ranges])

    def get_defaults(self):
        self.dpre_osci_rows.setValue(self.defaults["rows"])
        self.dpre_osci_width.setValue(self.defaults["width"])
        self.dpre_osci_y_label.setText(self.defaults["y_label"])
        self.dpre_osci_y_label_fs.setValue(self.defaults["y_label_fs"])
        self.dpre_osci_dpre_ms.setValue(self.defaults["dpre_ms"])
        self.dpre_osci_dpre_alpha.setValue(self.defaults["dpre_alpha"])
        self.dpre_osci_smooth_lw.setValue(self.defaults["smooth_lw"])
        self.dpre_osci_ref_color.select(get_colour(self.defaults["ref_color"]))
        self.dpre_osci_color_init.select(get_colour(self.defaults["color_init"]))
        self.dpre_osci_color_end.select(get_colour(self.defaults["color_end"]))
        self.dpre_osci_x_ticks_fs.setValue(self.defaults["x_ticks_fs"])
        self.dpre_osci_x_ticks_fn.select(self.defaults["x_ticks_fn"])
        self.dpre_osci_x_ticks_pad.setValue(self.defaults["x_ticks_pad"])
        self.dpre_osci_x_ticks_weight.select(self.defaults["x_ticks_weight"])
        self.dpre_osci_grid_color.select(self.defaults["grid_color"])
        self.dpre_osci_shade.setChecked(self.defaults["shade"])
        self.dpre_osci_regions.setText(self.get_ranges(self.defaults["shade_regions"]))
        self.dpre_osci_res_highlight.setChecked(self.defaults["res_highlight"])
        self.dpre_osci_res_highlight_list.field.setText(','.join(list(map(str, self.defaults["res_hl_list"]))))
        self.dpre_osci_rh_fs.setValue(self.defaults["res_highlight_fs"])
        self.dpre_osci_rh_y.setValue(self.defaults["res_highlight_y"])
        self.dpre_osci_ymax.setValue(self.defaults["ymax"])


    def set_values(self):
        self.local_variables["rows"] = self.dpre_osci_rows.field.value()
        self.local_variables["width"] = self.dpre_osci_width.field.value()
        self.local_variables["y_label"] = self.dpre_osci_y_label.field.text()
        self.local_variables["y_label_fs"] = self.dpre_osci_y_label_fs.field.value()
        self.local_variables["dpre_ms"] = self.dpre_osci_dpre_ms.field.value()
        self.local_variables["dpre_alpha"] = self.dpre_osci_dpre_alpha.field.value()
        self.local_variables["smooth_lw"] = self.dpre_osci_smooth_lw.field.value()
        self.local_variables["ref_color"] = str(self.dpre_osci_ref_color.fields.currentText())
        self.local_variables["color_init"] = str(self.dpre_osci_color_init.fields.currentText())
        self.local_variables["color_end"] = str(self.dpre_osci_color_end.fields.currentText())
        self.local_variables["x_ticks_fs"] = self.dpre_osci_x_ticks_fs.field.value()
        self.local_variables["x_ticks_fn"] = self.dpre_osci_x_ticks_fn.fields.currentText()
        self.local_variables["x_ticks_pad"] = self.dpre_osci_x_ticks_pad.field.value()
        self.local_variables["x_ticks_weight"] = self.dpre_osci_x_ticks_weight.fields.currentText()
        self.local_variables["grid_color"] = self.dpre_osci_grid_color.fields.currentText()
        self.local_variables["shade"] = self.dpre_osci_shade.isChecked()
        self.local_variables["shade_regions"] = self.set_ranges(self.dpre_osci_regions.field.text())
        self.local_variables["res_highlight"] = self.dpre_osci_res_highlight.isChecked()
        self.local_variables["res_hl_list"] = list(map(int, self.dpre_osci_res_highlight_list.field.text().split(',')))
        self.local_variables["res_highlight_fs"] = self.dpre_osci_rh_fs.field.value()
        self.local_variables["res_highlight_y"] = self.dpre_osci_rh_y.field.value()
        self.local_variables["ymax"] = self.dpre_osci_ymax.field.value()
        self.accept()


    def get_values(self):
        self.dpre_osci_rows.setValue(self.local_variables["rows"])
        self.dpre_osci_width.setValue(self.local_variables["width"])
        self.dpre_osci_y_label.setText(self.local_variables["y_label"])
        self.dpre_osci_y_label_fs.setValue(self.local_variables["y_label_fs"])
        self.dpre_osci_dpre_ms.setValue(self.local_variables["dpre_ms"])
        self.dpre_osci_dpre_alpha.setValue(self.local_variables["dpre_alpha"])
        self.dpre_osci_smooth_lw.setValue(self.local_variables["smooth_lw"])
        self.dpre_osci_ref_color.select(self.local_variables["ref_color"])
        self.dpre_osci_color_init.select(self.local_variables["color_init"])
        self.dpre_osci_color_end.select(self.local_variables["color_end"])
        self.dpre_osci_x_ticks_fs.setValue(self.local_variables["x_ticks_fs"])
        self.dpre_osci_x_ticks_fn.select(self.local_variables["x_ticks_fn"])
        self.dpre_osci_x_ticks_pad.setValue(self.local_variables["x_ticks_pad"])
        self.dpre_osci_x_ticks_weight.select(self.local_variables["x_ticks_weight"])
        self.dpre_osci_grid_color.select(self.local_variables["grid_color"])
        self.dpre_osci_shade.setChecked(self.local_variables["shade"])
        self.dpre_osci_res_highlight.setChecked(self.local_variables["res_highlight"])
        self.dpre_osci_res_highlight_list.field.setText(','.join(list(map(str, self.local_variables["res_hl_list"]))))
        self.dpre_osci_regions.setText(self.get_ranges(self.local_variables["shade_regions"]))
        self.dpre_osci_rh_fs.setValue(self.local_variables["res_highlight_fs"])
        self.dpre_osci_rh_y.setValue(self.local_variables["res_highlight_y"])
        self.dpre_osci_ymax.setValue(self.local_variables["ymax"])

