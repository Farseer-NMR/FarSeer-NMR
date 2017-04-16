from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox, QLineEdit, QCheckBox, QDoubleSpinBox, QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox
from gui.components.FontComboBox import FontComboBox

import json
from current.default_config import defaults

class ScatterPlotPopup(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(ScatterPlotPopup, self).__init__(parent)
        self.setWindowTitle("Residue Evolution Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.vars = None
        if vars:
            self.vars = vars["cs_scatter_settings"]
        self.default = defaults["cs_scatter_settings"]

        self.cs_scatter_cols_page = LabelledSpinBox(self, "Columns Per Page")
        self.cs_scatter_rows_page = LabelledSpinBox(self, "Rows Per Page")
        self.cs_scatter_title_y = LabelledSpinBox(self, "Y Title Size")
        self.cs_scatter_title_fn = FontComboBox(self, "Title Font")
        self.cs_scatter_title_fs = LabelledSpinBox(self, "Title Font Size")
        self.cs_scatter_x_label_fn = FontComboBox(self, "X Font Label")
        self.cs_scatter_x_label_fs = LabelledSpinBox(self, "X Label Font Size")
        self.cs_scatter_x_label_pad = LabelledSpinBox(self, "X Label Padding")
        self.cs_scatter_x_label_weight = LabelledCombobox(self, text="X Label Font Weight", items=['bold', 'normal'])
        self.cs_scatter_x_ticks_pad = LabelledSpinBox(self, "X Tick Padding")
        self.cs_scatter_x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size")
        self.cs_scatter_y_label_fn = FontComboBox(self, "Y Label Font")
        self.cs_scatter_y_label_fs = LabelledSpinBox(self, "Y Label Font Size")
        self.cs_scatter_y_label_pad = LabelledSpinBox(self, "Y Label Padding")
        self.cs_scatter_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=['bold', 'normal'])
        self.cs_scatter_y_ticks_pad = LabelledSpinBox(self, "Y Tick Padding")
        self.cs_scatter_y_ticks_fs = LabelledSpinBox(self, "Y Label Tick Size")
        self.cs_scatter_mksize = LabelledSpinBox(self, "Mark Size")
        self.cs_scatter_scale = LabelledDoubleSpinBox(self, "Scale")
        self.cs_scatter_mk_type = LabelledCombobox(self, text="Y Label Font Weight", items=['color', 'shape'])
        self.cs_scatter_mk_start_color = ColourBox(self, "Mark Start Colour")
        self.cs_scatter_mk_end_color = ColourBox(self, "Mark End Colour")
        self.cs_scatter_mk_lost_color = ColourBox(self, "Mark Lost Colour")
        self.cs_scatter_markers = LabelledLineEdit(self, "Sequential Markers")
        self.cs_scatter_mk_color = ColourBox(self, "Mark Colour")
        self.cs_scatter_mk_edgecolors = ColourBox(self, "Marker Edge Colours")
        self.cs_scatter_mk_edge_lost = ColourBox(self, "Lost Marker Edge Colours")

        self.layout().addWidget(self.cs_scatter_cols_page, 0, 0)
        self.layout().addWidget(self.cs_scatter_rows_page, 1, 0)
        self.layout().addWidget(self.cs_scatter_title_y, 2, 0)
        self.layout().addWidget(self.cs_scatter_title_fn, 3, 0)
        self.layout().addWidget(self.cs_scatter_title_fs, 4, 0)
        self.layout().addWidget(self.cs_scatter_x_label_fn, 5, 0)
        self.layout().addWidget(self.cs_scatter_x_label_fs, 6, 0)
        self.layout().addWidget(self.cs_scatter_x_label_pad, 7, 0)
        self.layout().addWidget(self.cs_scatter_x_label_weight, 8, 0)

        self.layout().addWidget(self.cs_scatter_x_ticks_pad, 0, 1)
        self.layout().addWidget(self.cs_scatter_x_ticks_fs, 1, 1)
        self.layout().addWidget(self.cs_scatter_y_label_fn, 2, 1)
        self.layout().addWidget(self.cs_scatter_y_label_fs, 3, 1)
        self.layout().addWidget(self.cs_scatter_y_label_pad, 4, 1)
        self.layout().addWidget(self.cs_scatter_y_label_weight, 5, 1)
        self.layout().addWidget(self.cs_scatter_y_ticks_pad, 6, 1)
        self.layout().addWidget(self.cs_scatter_y_ticks_fs, 7, 1)
        self.layout().addWidget(self.cs_scatter_mksize, 8, 1)

        self.layout().addWidget(self.cs_scatter_scale, 0, 2)
        self.layout().addWidget(self.cs_scatter_mk_type, 1, 2)
        self.layout().addWidget(self.cs_scatter_mk_start_color, 2, 2)
        self.layout().addWidget(self.cs_scatter_mk_end_color, 3, 2)
        self.layout().addWidget(self.cs_scatter_mk_lost_color, 4, 2)
        self.layout().addWidget(self.cs_scatter_markers, 5, 2)
        self.layout().addWidget(self.cs_scatter_mk_color, 6, 2)
        self.layout().addWidget(self.cs_scatter_mk_edgecolors, 7, 2)
        self.layout().addWidget(self.cs_scatter_mk_edge_lost, 8, 2)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 10, 0, 1, 2)

        if vars:
            self.get_values()

    def get_defaults(self):
        self.cs_scatter_cols_page.field.setValue(self.default["cs_scatter_cols_page"])
        self.cs_scatter_rows_page.field.setValue(self.default["cs_scatter_rows_page"])
        self.cs_scatter_title_y.field.setValue(self.default["cs_scatter_title_y"])
        self.cs_scatter_title_fn.select(self.default["cs_scatter_title_fn"])
        self.cs_scatter_title_fs.field.setValue(self.default["cs_scatter_title_fs"])
        self.cs_scatter_x_label_fn.select(self.default["cs_scatter_x_label_fn"])
        self.cs_scatter_x_label_fs.field.setValue(self.default["cs_scatter_x_label_fs"])
        self.cs_scatter_x_label_pad.field.setValue(self.default["cs_scatter_x_label_pad"])
        self.cs_scatter_x_label_weight.select(self.default["cs_scatter_x_label_weight"])
        self.cs_scatter_x_ticks_pad.field.setValue(self.default["cs_scatter_x_ticks_pad"])
        self.cs_scatter_x_ticks_fs.field.setValue(self.default["cs_scatter_x_ticks_fs"])
        self.cs_scatter_y_label_fn.select(self.default["cs_scatter_y_label_fn"])
        self.cs_scatter_y_label_fs.field.setValue(self.default["cs_scatter_y_label_fs"])
        self.cs_scatter_y_label_pad.field.setValue(self.default["cs_scatter_y_label_pad"])
        self.cs_scatter_y_label_weight.select(self.default["cs_scatter_y_label_weight"])
        self.cs_scatter_y_ticks_pad.field.setValue(self.default["cs_scatter_y_ticks_pad"])
        self.cs_scatter_y_ticks_fs.field.setValue(self.default["cs_scatter_y_ticks_fs"])
        self.cs_scatter_mksize.field.setValue(self.default["cs_scatter_mksize"])
        self.cs_scatter_scale.field.setValue(self.default["cs_scatter_scale"])
        self.cs_scatter_mk_type.select(self.default["cs_scatter_mk_type"])
        self.cs_scatter_mk_start_color.select(self.default["cs_scatter_mk_start_color"])
        self.cs_scatter_mk_end_color.select(self.default["cs_scatter_mk_end_color"])
        self.cs_scatter_mk_lost_color.select(self.default["cs_scatter_mk_lost_color"])
        self.cs_scatter_markers.field.setText(', '.join(self.default["cs_scatter_markers"]))
        self.cs_scatter_mk_color.select(self.default["cs_scatter_mk_color"])
        self.cs_scatter_mk_edgecolors.select(self.default["cs_scatter_mk_edgecolors"])
        self.cs_scatter_mk_edge_lost.select(self.default["cs_scatter_mk_edge_lost"])


    def set_values(self):
        self.vars["cs_scatter_cols_page"] = self.cs_scatter_cols_page.field.value()
        self.vars["cs_scatter_rows_page"] = self.cs_scatter_rows_page.field.value()
        self.vars["cs_scatter_title_y"] = self.cs_scatter_title_y.field.value()
        self.vars["cs_scatter_title_fn"] = self.cs_scatter_title_fn.fields.currentText()
        self.vars["cs_scatter_title_fs"] = self.cs_scatter_title_fs.field.value()
        self.vars["cs_scatter_x_label_fn"] = self.cs_scatter_x_label_fn.fields.currentText()
        self.vars["cs_scatter_x_label_fs"] = self.cs_scatter_x_label_fs.field.value()
        self.vars["cs_scatter_x_label_pad"] = self.cs_scatter_x_label_pad.field.value()
        self.vars["cs_scatter_x_label_weight"] = self.cs_scatter_x_label_weight.fields.currentText()
        self.vars["cs_scatter_x_ticks_pad"] = self.cs_scatter_x_ticks_pad.field.value()
        self.vars["cs_scatter_x_ticks_fs"] = self.cs_scatter_x_ticks_fs.field.value()
        self.vars["cs_scatter_y_label_fn"] = self.cs_scatter_y_label_fn.fields.currentText()
        self.vars["cs_scatter_y_label_fs"] = self.cs_scatter_y_label_fs.field.value()
        self.vars["cs_scatter_y_label_pad"] = self.cs_scatter_y_label_pad.field.value()
        self.vars["cs_scatter_y_label_weight"] = self.cs_scatter_y_label_weight.fields.currentText()
        self.vars["cs_scatter_y_ticks_pad"] = self.cs_scatter_y_ticks_pad.field.value()
        self.vars["cs_scatter_y_ticks_fs"] = self.cs_scatter_y_ticks_fs.field.value()
        self.vars["cs_scatter_mksize"] = self.cs_scatter_mksize.field.value()
        self.vars["cs_scatter_scale"] = self.cs_scatter_scale.field.value()
        self.vars["cs_scatter_mk_type"] = self.cs_scatter_mk_type.fields.currentText()
        self.vars["cs_scatter_mk_start_color"] = self.cs_scatter_mk_start_color.fields.currentText()
        self.vars["cs_scatter_mk_end_color"] = self.cs_scatter_mk_end_color.fields.currentText()
        self.vars["cs_scatter_mk_lost_color"] = self.cs_scatter_mk_lost_color.fields.currentText()
        self.vars["cs_scatter_markers"] = list(self.cs_scatter_markers.field.text())
        self.vars["cs_scatter_mk_color"] = self.cs_scatter_mk_color.fields.currentText()
        self.vars["cs_scatter_mk_edgecolors"] = self.cs_scatter_mk_edgecolors.fields.currentText()
        self.vars["cs_scatter_mk_edge_lost"] = self.cs_scatter_mk_edge_lost.fields.currentText()
        vars["cs_scatter_settings"] = self.vars
        self.accept()

    def get_values(self):
        self.cs_scatter_cols_page.field.setValue(self.vars["cs_scatter_cols_page"])
        self.cs_scatter_rows_page.field.setValue(self.vars["cs_scatter_rows_page"])
        self.cs_scatter_title_y.field.setValue(self.vars["cs_scatter_title_y"])
        self.cs_scatter_title_fn.select(self.vars["cs_scatter_title_fn"])
        self.cs_scatter_title_fs.field.setValue(self.vars["cs_scatter_title_fs"])
        self.cs_scatter_x_label_fn.select(self.vars["cs_scatter_x_label_fn"])
        self.cs_scatter_x_label_fs.field.setValue(self.vars["cs_scatter_x_label_fs"])
        self.cs_scatter_x_label_pad.field.setValue(self.vars["cs_scatter_x_label_pad"])
        self.cs_scatter_x_label_weight.select(self.vars["cs_scatter_x_label_weight"])
        self.cs_scatter_x_ticks_pad.field.setValue(self.vars["cs_scatter_x_ticks_pad"])
        self.cs_scatter_x_ticks_fs.field.setValue(self.vars["cs_scatter_x_ticks_fs"])
        self.cs_scatter_y_label_fn.select(self.vars["cs_scatter_y_label_fn"])
        self.cs_scatter_y_label_fs.field.setValue(self.vars["cs_scatter_y_label_fs"])
        self.cs_scatter_y_label_pad.field.setValue(self.vars["cs_scatter_y_label_pad"])
        self.cs_scatter_y_label_weight.select(self.vars["cs_scatter_y_label_weight"])
        self.cs_scatter_y_ticks_pad.field.setValue(self.vars["cs_scatter_y_ticks_pad"])
        self.cs_scatter_y_ticks_fs.field.setValue(self.vars["cs_scatter_y_ticks_fs"])
        self.cs_scatter_mksize.field.setValue(self.vars["cs_scatter_mksize"])
        self.cs_scatter_scale.field.setValue(self.vars["cs_scatter_scale"])
        self.cs_scatter_mk_type.select(self.vars["cs_scatter_mk_type"])
        self.cs_scatter_mk_start_color.select(self.vars["cs_scatter_mk_start_color"])
        self.cs_scatter_mk_end_color.select(self.vars["cs_scatter_mk_end_color"])
        self.cs_scatter_mk_lost_color.select(self.vars["cs_scatter_mk_lost_color"])
        self.cs_scatter_markers.field.setText(', '.join(self.vars["cs_scatter_markers"]))
        self.cs_scatter_mk_color.select(self.vars["cs_scatter_mk_color"])
        self.cs_scatter_mk_edgecolors.select(self.vars["cs_scatter_mk_edgecolors"])
        self.cs_scatter_mk_edge_lost.select(self.vars["cs_scatter_mk_edge_lost"])
