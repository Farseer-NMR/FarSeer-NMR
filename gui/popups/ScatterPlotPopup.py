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
from functools import partial

class ScatterPlotPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(ScatterPlotPopup, self).__init__(parent)
        self.setWindowTitle("Scatter Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["cs_scatter_settings"]
        self.default = defaults["cs_scatter_settings"]

        self.cs_scatter_cols_page = LabelledSpinBox(self, "Columns Per Page")
        self.cs_scatter_rows_page = LabelledSpinBox(self, "Rows Per Page")
        self.cs_scatter_x_label = LabelledLineEdit(self, "X Label")
        self.cs_scatter_y_label = LabelledLineEdit(self, "Y Label")
        self.cs_scatter_mksize = LabelledSpinBox(self, "Mark Size")
        self.cs_scatter_scale = LabelledDoubleSpinBox(self, "Scale")
        self.cs_scatter_mk_type = LabelledCombobox(self, text="Y Label Font Weight", items=['color', 'shape'])
        self.cs_scatter_mk_start_color = ColourBox(self, "Mark Start Colour")
        self.cs_scatter_mk_end_color = ColourBox(self, "Mark End Colour")
        self.cs_scatter_markers = LabelledLineEdit(self, "Sequential Markers")
        self.cs_scatter_mk_color = ColourBox(self, "Mark Colour")
        self.cs_scatter_mk_lost_color = ColourBox(self, "Lost Mark Colour")
        self.cs_scatter_mk_edgecolors = ColourBox(self, "Marker Edge Colours")
        self.cs_scatter_hide_lost = LabelledCheckbox(self, "Hide Lost Data Points")

        self.layout().addWidget(self.cs_scatter_cols_page, 0, 0)
        self.layout().addWidget(self.cs_scatter_rows_page, 1, 0)
        self.layout().addWidget(self.cs_scatter_x_label, 2, 0)
        self.layout().addWidget(self.cs_scatter_y_label, 3, 0)
        self.layout().addWidget(self.cs_scatter_mksize, 4, 0)
        self.layout().addWidget(self.cs_scatter_scale, 5, 0)
        self.layout().addWidget(self.cs_scatter_mk_type, 6, 0)


        self.layout().addWidget(self.cs_scatter_mk_start_color, 0, 1)
        self.layout().addWidget(self.cs_scatter_mk_end_color, 1, 1)
        self.layout().addWidget(self.cs_scatter_markers, 2, 1)
        self.layout().addWidget(self.cs_scatter_mk_color, 3, 1)
        self.layout().addWidget(self.cs_scatter_mk_edgecolors, 4, 1)
        self.layout().addWidget(self.cs_scatter_mk_lost_color, 5, 1)
        self.layout().addWidget(self.cs_scatter_hide_lost, 6, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 7, 0, 1, 2)

        if variables:
            self.get_values()

    def get_defaults(self):
        self.cs_scatter_cols_page.setValue(self.default["cs_scatter_cols_page"])
        self.cs_scatter_rows_page.setValue(self.default["cs_scatter_rows_page"])
        self.cs_scatter_x_label.field.setText(self.default["cs_scatter_x_label"])
        self.cs_scatter_y_label.field.setText(self.default["cs_scatter_y_label"])
        self.cs_scatter_mksize.setValue(self.default["cs_scatter_mksize"])
        self.cs_scatter_scale.setValue(self.default["cs_scatter_scale"])
        self.cs_scatter_mk_type.select(self.default["cs_scatter_mk_type"])

        self.cs_scatter_mk_start_color.select(self.default["cs_scatter_mk_start_color"])
        self.cs_scatter_mk_end_color.select(self.default["cs_scatter_mk_end_color"])
        self.cs_scatter_markers.field.setText(', '.join(self.default["cs_scatter_markers"]))
        self.cs_scatter_mk_color.select(self.default["cs_scatter_mk_color"])
        self.cs_scatter_mk_edgecolors.select(self.default["cs_scatter_mk_edgecolors"])
        self.cs_scatter_mk_lost_color.select(self.default["cs_scatter_mk_lost_color"])
        self.cs_scatter_hide_lost.setChecked(self.default["cs_scatter_hide_lost"])


    def set_values(self, variables):
        self.variables["cs_scatter_cols_page"] = self.cs_scatter_cols_page.field.value()
        self.variables["cs_scatter_rows_page"] = self.cs_scatter_rows_page.field.value()
        self.variables["cs_scatter_x_label"] = self.cs_scatter_x_label.field.text()
        self.variables["cs_scatter_y_label"] = self.cs_scatter_y_label.field.text()
        self.variables["cs_scatter_mksize"] = self.cs_scatter_mksize.field.value()
        self.variables["cs_scatter_scale"] = self.cs_scatter_scale.field.value()
        self.variables["cs_scatter_mk_type"] = self.cs_scatter_mk_type.fields.currentText()
        self.variables["cs_scatter_mk_start_color"] = self.cs_scatter_mk_start_color.fields.currentText()
        self.variables["cs_scatter_mk_end_color"] = self.cs_scatter_mk_end_color.fields.currentText()
        self.variables["cs_scatter_markers"] = list(self.cs_scatter_markers.field.text())
        self.variables["cs_scatter_mk_color"] = self.cs_scatter_mk_color.fields.currentText()
        self.variables["cs_scatter_mk_edgecolors"] = self.cs_scatter_mk_edgecolors.fields.currentText()
        self.variables["cs_scatter_mk_lost_color"] = self.cs_scatter_mk_lost_color.fields.currentText()
        self.variables["cs_scatter_hide_lost"] = self.cs_scatter_hide_lost.checkBox.isChecked()
        variables["cs_scatter_settings"] = self.variables
        self.accept()

    def get_values(self):
        self.cs_scatter_cols_page.setValue(self.variables["cs_scatter_cols_page"])
        self.cs_scatter_rows_page.setValue(self.variables["cs_scatter_rows_page"])
        self.cs_scatter_x_label.field.setText(self.variables["cs_scatter_x_label"])
        self.cs_scatter_y_label.field.setText(self.variables["cs_scatter_y_label"])
        self.cs_scatter_mksize.setValue(self.variables["cs_scatter_mksize"])
        self.cs_scatter_scale.setValue(self.variables["cs_scatter_scale"])
        self.cs_scatter_mk_type.select(self.variables["cs_scatter_mk_type"])

        self.cs_scatter_mk_start_color.select(self.variables["cs_scatter_mk_start_color"])
        self.cs_scatter_mk_end_color.select(self.variables["cs_scatter_mk_end_color"])
        self.cs_scatter_markers.field.setText(', '.join(self.variables["cs_scatter_markers"]))
        self.cs_scatter_mk_color.select(self.variables["cs_scatter_mk_color"])
        self.cs_scatter_mk_edgecolors.select(self.variables["cs_scatter_mk_edgecolors"])
        self.cs_scatter_mk_lost_color.select(self.variables["cs_scatter_mk_lost_color"])
        self.cs_scatter_hide_lost.setChecked(self.variables["cs_scatter_hide_lost"])
