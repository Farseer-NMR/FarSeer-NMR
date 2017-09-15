from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox
from gui.components.FontComboBox import FontComboBox

from functools import partial
from gui.gui_utils import defaults, font_weights

class OscillationMapPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(OscillationMapPopup, self).__init__(parent)
        self.setWindowTitle("Oscillation Map")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["dpre_osci_settings"]
        self.default = defaults["dpre_osci_settings"]

        self.dpre_osci_rows = LabelledSpinBox(self, "Number of Rows", min=1, step=1)
        self.dpre_osci_width = LabelledSpinBox(self, "Scale Factor for Width")
        self.dpre_osci_y_label = LabelledLineEdit(self, "Y Label")
        self.dpre_osci_y_label_fs = LabelledSpinBox(self, "Y Label Font Size", min=0, step=1)
        self.dpre_osci_ymax = LabelledDoubleSpinBox(self, "Y Maximum", min=0, step=0.1)
        self.dpre_osci_dpre_ms = LabelledSpinBox(self, "Marker Size", min=0, step=1)
        self.dpre_osci_dpre_alpha = LabelledDoubleSpinBox(self, "Marker Transparency", min=0, max=1, step=0.1)
        self.dpre_osci_smooth_lw = LabelledSpinBox(self, "Smoothed DPRE Line Width", min=0, step=1)
        self.dpre_osci_ref_color = ColourBox(self, "Reference Data Colour")
        self.dpre_osci_color_init = LabelledLineEdit(self, "Grad Start Colour (hex)")
        self.dpre_osci_color_end = LabelledLineEdit(self, "Grad End Colour (hex)")
        self.dpre_osci_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.dpre_osci_x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size", min=0, step=1)
        self.dpre_osci_x_ticks_pad = LabelledDoubleSpinBox(self, "X Tick Padding", min=-100, max=100, step=0.1)
        self.dpre_osci_x_ticks_weight = LabelledCombobox(self, text="X Font Weight", items=font_weights)
        self.dpre_osci_grid_color = ColourBox(self, "Grid Colour")
        self.dpre_osci_res_highlight = LabelledCheckbox(self, "Highlight Residues?")
        self.dpre_osci_res_highlight_list = LabelledLineEdit(self, "Residues to Highlight")
        self.dpre_osci_shade = LabelledCheckbox(self, "Shade Residues?")
        self.dpre_osci_regions = LabelledLineEdit(self, "Regions to Shade")
        self.dpre_osci_rh_fs = LabelledSpinBox(self, "Highlight Font Size ", min=0, step=1)
        self.dpre_osci_rh_y = LabelledDoubleSpinBox(self, "Residue Label Scale", min=0, max=1, step=0.01)


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

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 11, 0, 2, 2)

        if variables:
            self.get_values()

    def set_ranges(self, field_value):
        ll = field_value.split(',')
        return [[int(x.split('-')[0]), int(x.split('-')[1])] for x in ll]

    def get_ranges(self, ranges):
        return ','.join(["%s-%s" % (x[0], x[1]) for x in ranges])

    def get_defaults(self):
        self.dpre_osci_rows.setValue(self.default["rows"])
        self.dpre_osci_width.setValue(self.default["width"])
        self.dpre_osci_y_label.setText(self.default["y_label"])
        self.dpre_osci_y_label_fs.setValue(self.default["y_label_fs"])
        self.dpre_osci_dpre_ms.setValue(self.default["dpre_ms"])
        self.dpre_osci_dpre_alpha.setValue(self.default["dpre_alpha"])
        self.dpre_osci_smooth_lw.setValue(self.default["smooth_lw"])
        self.dpre_osci_ref_color.select(self.default["ref_color"])
        self.dpre_osci_color_init.field.setText(self.default["color_init"])
        self.dpre_osci_color_end.field.setText(self.default["color_end"])
        self.dpre_osci_x_ticks_fs.setValue(self.default["x_ticks_fs"])
        self.dpre_osci_x_ticks_fn.select(self.default["x_ticks_fn"])
        self.dpre_osci_x_ticks_pad.setValue(self.default["x_ticks_pad"])
        self.dpre_osci_x_ticks_weight.select(self.default["x_ticks_weight"])
        self.dpre_osci_grid_color.select(self.default["grid_color"])
        self.dpre_osci_shade.setChecked(self.default["shade"])
        self.dpre_osci_regions.setText(self.get_ranges(self.default["shade_regions"]))
        self.dpre_osci_res_highlight.setChecked(self.default["res_highlight"])
        self.dpre_osci_res_highlight_list.field.setText(','.join(list(map(str, self.default["res_hl_list"]))))
        self.dpre_osci_rh_fs.setValue(self.default["res_highlight_fs"])
        self.dpre_osci_rh_y.setValue(self.default["res_highlight_y"])
        self.dpre_osci_ymax.setValue(self.default["ymax"])


    def set_values(self, variables):
        self.variables["rows"] = self.dpre_osci_rows.field.value()
        self.variables["width"] = self.dpre_osci_width.field.value()
        self.variables["y_label"] = self.dpre_osci_y_label.field.text()
        self.variables["y_label_fs"] = self.dpre_osci_y_label_fs.field.value()
        self.variables["dpre_ms"] = self.dpre_osci_dpre_ms.field.value()
        self.variables["dpre_alpha"] = self.dpre_osci_dpre_alpha.field.value()
        self.variables["smooth_lw"] = self.dpre_osci_smooth_lw.field.value()
        self.variables["ref_color"] = self.dpre_osci_ref_color.fields.currentText()
        self.variables["color_init"] = self.dpre_osci_color_init.field.text()
        self.variables["color_end"] = self.dpre_osci_color_end.field.text()
        self.variables["x_ticks_fs"] = self.dpre_osci_x_ticks_fs.field.value()
        self.variables["x_ticks_fn"] = self.dpre_osci_x_ticks_fn.fields.currentText()
        self.variables["x_ticks_pad"] = self.dpre_osci_x_ticks_pad.field.value()
        self.variables["x_ticks_weight"] = self.dpre_osci_x_ticks_weight.fields.currentText()
        self.variables["grid_color"] = self.dpre_osci_grid_color.fields.currentText()
        self.variables["shade"] = self.dpre_osci_shade.isChecked()
        self.variables["shade_regions"] = self.set_ranges(self.dpre_osci_regions.field.text())
        self.variables["res_highlight"] = self.dpre_osci_res_highlight.isChecked()
        self.variables["res_hl_list"] = list(map(int, self.dpre_osci_res_highlight_list.field.text().split(',')))
        self.variables["res_highlight_fs"] = self.dpre_osci_rh_fs.field.value()
        self.variables["res_highlight_y"] = self.dpre_osci_rh_y.field.value()
        self.variables["ymax"] = self.dpre_osci_ymax.field.value()
        variables["dpre_osci_settings"] = self.variables
        self.accept()


    def get_values(self):
        self.dpre_osci_rows.setValue(self.variables["rows"])
        self.dpre_osci_width.setValue(self.variables["width"])
        self.dpre_osci_y_label.setText(self.variables["y_label"])
        self.dpre_osci_y_label_fs.setValue(self.variables["y_label_fs"])
        self.dpre_osci_dpre_ms.setValue(self.variables["dpre_ms"])
        self.dpre_osci_dpre_alpha.setValue(self.variables["dpre_alpha"])
        self.dpre_osci_smooth_lw.setValue(self.variables["smooth_lw"])
        self.dpre_osci_ref_color.select(self.variables["ref_color"])
        self.dpre_osci_color_init.field.setText(self.variables["color_init"])
        self.dpre_osci_color_end.field.setText(self.variables["color_end"])
        self.dpre_osci_x_ticks_fs.setValue(self.variables["x_ticks_fs"])
        self.dpre_osci_x_ticks_fn.select(self.variables["x_ticks_fn"])
        self.dpre_osci_x_ticks_pad.setValue(self.variables["x_ticks_pad"])
        self.dpre_osci_x_ticks_weight.select(self.variables["x_ticks_weight"])
        self.dpre_osci_grid_color.select(self.variables["grid_color"])
        self.dpre_osci_shade.setChecked(self.variables["shade"])
        self.dpre_osci_res_highlight.setChecked(self.variables["res_highlight"])
        self.dpre_osci_res_highlight_list.field.setText(','.join(list(map(str, self.variables["res_hl_list"]))))
        self.dpre_osci_regions.setText(self.get_ranges(self.variables["shade_regions"]))
        self.dpre_osci_rh_fs.setValue(self.variables["res_highlight_fs"])
        self.dpre_osci_rh_y.setValue(self.variables["res_highlight_y"])
        self.dpre_osci_ymax.setValue(self.variables["ymax"])

