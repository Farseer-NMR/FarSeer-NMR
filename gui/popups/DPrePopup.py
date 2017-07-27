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
from current.default_config import defaults
from gui.gui_utils import font_weights

class DPrePopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(DPrePopup, self).__init__(parent)
        self.setWindowTitle("DPre Oscillation Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["dpre_osci_settings"]
        self.default = defaults["dpre_osci_settings"]

        self.dpre_osci_rows = LabelledSpinBox(self, "Number of Rows")
        self.dpre_osci_width = LabelledSpinBox(self, "Scale Factor for Width")
        self.dpre_osci_title_y = LabelledSpinBox(self, "Subplot Title Padding")
        self.dpre_osci_title_fs = LabelledSpinBox(self, "Title Font Size")
        self.dpre_osci_title_fn = FontComboBox(self, "Title Font")
        self.dpre_osci_dpre_ms = LabelledSpinBox(self, "Marker Size")
        self.dpre_osci_dpre_alpha = LabelledDoubleSpinBox(self, "Marker alpha")
        self.dpre_osci_smooth_lw = LabelledSpinBox(self, "Smoothed DPRE Line Width")
        self.dpre_osci_ref_color = ColourBox(self, "Reference Data Colour")
        self.dpre_osci_color_init = ColourBox(self, "Gradient Start Colour")
        self.dpre_osci_color_end = ColourBox(self, "Gradient End Colour")
        self.dpre_osci_x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size")
        self.dpre_osci_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.dpre_osci_y_label_fs = LabelledSpinBox(self, "Y Label Font Size")
        self.dpre_osci_y_label_pad = LabelledSpinBox(self, "Y Label Padding")
        self.dpre_osci_y_label_fn = FontComboBox(self, "Y Label Font")
        self.dpre_osci_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=font_weights)
        self.dpre_osci_y_ticks_len = LabelledSpinBox(self, "Y Tick Length")
        self.dpre_osci_y_ticks_fs = LabelledSpinBox(self, "Y Tick Font Size")
        self.dpre_osci_y_ticks_pad = LabelledSpinBox(self, "Y Tick Padding")
        self.dpre_osci_grid_color = ColourBox(self, "Grid Colour")
        self.dpre_osci_res_shade = LabelledCheckbox(self, "Highlight Residues?")
        self.dpre_osci_res_highlight = LabelledLineEdit(self, "Residues to Highlight")
        self.dpre_osci_rh_fs = LabelledSpinBox(self, "Highlight Font Size ")
        self.dpre_osci_rh_y = LabelledDoubleSpinBox(self, "Residue Label Scale")


        self.layout().addWidget(self.dpre_osci_width, 0, 0)
        self.layout().addWidget(self.dpre_osci_title_y, 1, 0)
        self.layout().addWidget(self.dpre_osci_title_fs, 2, 0)
        self.layout().addWidget(self.dpre_osci_title_fn, 3, 0)
        self.layout().addWidget(self.dpre_osci_dpre_ms, 4, 0)
        self.layout().addWidget(self.dpre_osci_dpre_alpha, 5, 0)
        self.layout().addWidget(self.dpre_osci_smooth_lw, 6, 0)
        self.layout().addWidget(self.dpre_osci_ref_color, 7, 0)
        self.layout().addWidget(self.dpre_osci_color_init, 8, 0)
        self.layout().addWidget(self.dpre_osci_color_end, 9, 0)
        self.layout().addWidget(self.dpre_osci_x_ticks_fs, 10, 0)
        self.layout().addWidget(self.dpre_osci_x_ticks_fn, 11, 0)
        self.layout().addWidget(self.dpre_osci_rows, 11, 0)

        self.layout().addWidget(self.dpre_osci_y_label_fs, 0, 1)
        self.layout().addWidget(self.dpre_osci_y_label_pad, 1, 1)
        self.layout().addWidget(self.dpre_osci_y_label_fn, 2, 1)
        self.layout().addWidget(self.dpre_osci_y_label_weight, 3, 1)
        self.layout().addWidget(self.dpre_osci_y_ticks_len, 4, 1)
        self.layout().addWidget(self.dpre_osci_y_ticks_fs, 5, 1)
        self.layout().addWidget(self.dpre_osci_y_ticks_pad, 6, 1)
        self.layout().addWidget(self.dpre_osci_grid_color, 7, 1)
        self.layout().addWidget(self.dpre_osci_res_shade, 8, 1)
        self.layout().addWidget(self.dpre_osci_res_highlight, 9, 1)
        self.layout().addWidget(self.dpre_osci_rh_fs, 10, 1)
        self.layout().addWidget(self.dpre_osci_rh_y, 11, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 12, 1, 1, 2)

        if variables:
            self.get_values()

    def get_defaults(self):
        self.dpre_osci_rows.setValue(self.default["dpre_osci_rows"])
        self.dpre_osci_width.setValue(self.default["dpre_osci_width"])
        self.dpre_osci_title_y.setValue(self.default["dpre_osci_title_y"])
        self.dpre_osci_title_fs.setValue(self.default["dpre_osci_title_fs"])
        self.dpre_osci_title_fn.select(self.default["dpre_osci_title_fn"])
        self.dpre_osci_dpre_ms.setValue(self.default["dpre_osci_dpre_ms"])
        self.dpre_osci_dpre_alpha.setValue(self.default["dpre_osci_dpre_alpha"])
        self.dpre_osci_smooth_lw.setValue(self.default["dpre_osci_smooth_lw"])
        self.dpre_osci_ref_color.select(self.default["dpre_osci_ref_color"])
        self.dpre_osci_color_init.select(self.default["dpre_osci_color_init"])
        self.dpre_osci_color_end.select(self.default["dpre_osci_color_end"])
        self.dpre_osci_x_ticks_fs.setValue(self.default["dpre_osci_x_ticks_fs"])
        self.dpre_osci_x_ticks_fn.select(self.default["dpre_osci_x_ticks_fn"])
        self.dpre_osci_y_label_fs.setValue(self.default["dpre_osci_y_label_fs"])
        self.dpre_osci_y_label_pad.setValue(self.default["dpre_osci_y_label_pad"])
        self.dpre_osci_y_label_fn.select(self.default["dpre_osci_y_label_fn"])
        self.dpre_osci_y_label_weight.select(self.default["dpre_osci_y_label_weight"])
        self.dpre_osci_y_ticks_len.setValue(self.default["dpre_osci_y_ticks_len"])
        self.dpre_osci_y_ticks_fs.setValue(self.default["dpre_osci_y_ticks_fs"])
        self.dpre_osci_y_ticks_pad.setValue(self.default["dpre_osci_y_ticks_pad"])
        self.dpre_osci_grid_color.select(self.default["dpre_osci_grid_color"])
        self.dpre_osci_res_shade.setChecked(self.default["dpre_osci_res_shade"])
        self.dpre_osci_res_highlight.field.setText(str(self.default["dpre_osci_res_highlight"]))
        self.dpre_osci_rh_fs.setValue(self.default["dpre_osci_rh_fs"])
        self.dpre_osci_rh_y.setValue(self.default["dpre_osci_rh_y"])


    def set_values(self, variables):
        self.variables["dpre_osci_rows"] = self.dpre_osci_rows.field.value()
        self.variables["dpre_osci_width"] = self.dpre_osci_width.field.value()
        self.variables["dpre_osci_title_y"] = self.dpre_osci_title_y.field.value()
        self.variables["dpre_osci_title_fs"] = self.dpre_osci_title_fs.field.value()
        self.variables["dpre_osci_title_fn"] = str(self.dpre_osci_title_fn.fields.currentText())
        self.variables["dpre_osci_dpre_ms"] = self.dpre_osci_dpre_ms.field.value()
        self.variables["dpre_osci_dpre_alpha"] = self.dpre_osci_dpre_alpha.field.value()
        self.variables["dpre_osci_smooth_lw"] = self.dpre_osci_smooth_lw.field.value()
        self.variables["dpre_osci_ref_color"] = str(self.dpre_osci_ref_color.fields.currentText())
        self.variables["dpre_osci_color_init"] = str(self.dpre_osci_color_init.fields.currentText())
        self.variables["dpre_osci_color_end"] = str(self.dpre_osci_color_end.fields.currentText())
        self.variables["dpre_osci_x_ticks_fs"] = self.dpre_osci_x_ticks_fs.field.value()
        self.variables["dpre_osci_x_ticks_fn"] = str(self.dpre_osci_x_ticks_fn.fields.currentText())
        self.variables["dpre_osci_y_label_fs"] = self.dpre_osci_y_label_fs.field.value()
        self.variables["dpre_osci_y_label_pad"] = self.dpre_osci_y_label_pad.field.value()
        self.variables["dpre_osci_y_label_fn"] = str(self.dpre_osci_y_label_fn.fields.currentText())
        self.variables["dpre_osci_y_label_weight"] = str(self.dpre_osci_y_label_weight.fields.currentText())
        self.variables["dpre_osci_y_ticks_len"] = self.dpre_osci_y_ticks_len.field.value()
        self.variables["dpre_osci_y_ticks_fs"] = self.dpre_osci_y_ticks_fs.field.value()
        self.variables["dpre_osci_y_ticks_pad"] = self.dpre_osci_y_ticks_pad.field.value()
        self.variables["dpre_osci_grid_color"] = str(self.dpre_osci_grid_color.fields.currentText())
        self.variables["dpre_osci_res_shade"] = self.dpre_osci_res_shade.checkBox.isChecked()
        self.variables["dpre_osci_res_highlight"] = str(self.dpre_osci_res_highlight.field.text())
        self.variables["dpre_osci_rh_fs"] = self.dpre_osci_rh_fs.field.value()
        self.variables["dpre_osci_rh_y"] = self.dpre_osci_rh_y.field.value()
        variables["dpre_osci_settings"] = self.variables
        self.accept()


    def get_values(self):
        self.dpre_osci_rows.setValue(self.variables["dpre_osci_rows"])
        self.dpre_osci_width.setValue(self.variables["dpre_osci_width"])
        self.dpre_osci_title_y.setValue(self.variables["dpre_osci_title_y"])
        self.dpre_osci_title_fs.setValue(self.variables["dpre_osci_title_fs"])
        self.dpre_osci_title_fn.select(self.variables["dpre_osci_title_fn"])
        self.dpre_osci_dpre_ms.setValue(self.variables["dpre_osci_dpre_ms"])
        self.dpre_osci_dpre_alpha.setValue(self.variables["dpre_osci_dpre_alpha"])
        self.dpre_osci_smooth_lw.setValue(self.variables["dpre_osci_smooth_lw"])
        self.dpre_osci_ref_color.select(self.variables["dpre_osci_ref_color"])
        self.dpre_osci_color_init.select(self.variables["dpre_osci_color_init"])
        self.dpre_osci_color_end.select(self.variables["dpre_osci_color_end"])
        self.dpre_osci_x_ticks_fs.setValue(self.variables["dpre_osci_x_ticks_fs"])
        self.dpre_osci_x_ticks_fn.select(self.variables["dpre_osci_x_ticks_fn"])
        self.dpre_osci_y_label_fs.setValue(self.variables["dpre_osci_y_label_fs"])
        self.dpre_osci_y_label_pad.setValue(self.variables["dpre_osci_y_label_pad"])
        self.dpre_osci_y_label_fn.select(self.variables["dpre_osci_y_label_fn"])
        self.dpre_osci_y_label_weight.select(self.variables["dpre_osci_y_label_weight"])
        self.dpre_osci_y_ticks_len.setValue(self.variables["dpre_osci_y_ticks_len"])
        self.dpre_osci_y_ticks_fs.setValue(self.variables["dpre_osci_y_ticks_fs"])
        self.dpre_osci_y_ticks_pad.setValue(self.variables["dpre_osci_y_ticks_pad"])
        self.dpre_osci_grid_color.select(self.variables["dpre_osci_grid_color"])
        self.dpre_osci_res_shade.setChecked(self.variables["dpre_osci_res_shade"])
        self.dpre_osci_res_highlight.field.setText(str(self.variables["dpre_osci_res_highlight"]))
        self.dpre_osci_rh_fs.setValue(self.variables["dpre_osci_rh_fs"])
        self.dpre_osci_rh_y.setValue(self.variables["dpre_osci_rh_y"])

