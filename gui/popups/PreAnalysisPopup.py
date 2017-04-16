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

class DPrePopup(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(DPrePopup, self).__init__(parent)
        self.setWindowTitle("Residue Evolution Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.vars = None
        if vars:
            self.vars = vars["pre_settings"]
        self.default = defaults["pre_settings"]

        self.applySmooth = LabelledCheckbox(self, "Apply Smoothing")
        self.gaussian_stdev = LabelledSpinBox(self, "Gaussian Stdev")
        self.gauss_x_size = LabelledSpinBox(self, "Gaussian X Size")
        self.d_pre_y_max = LabelledDoubleSpinBox(self, "PRE Y Max")
        self.d_pre_y_label = LabelledLineEdit(self, "PRE Y Label")
        self.d_pre_rows = LabelledSpinBox(self, "PRE Rows Per Page")
        self.pre_colour = ColourBox(self, "PRE colour")
        self.pre_lw = LabelledSpinBox(self, "PRE Line Width")
        self.tag_color = ColourBox(self, "Tag Colour")
        self.tag_lw = LabelledSpinBox(self, "Tag Line Width")
        self.pre_ls = LabelledCombobox(self, text="PRE Line Style", items=['-', '--', '-.', ':'])

        self.layout().addWidget(self.applySmooth, 0, 0)
        self.layout().addWidget(self.gaussian_stdev, 1, 0)
        self.layout().addWidget(self.gauss_x_size, 2, 0)
        self.layout().addWidget(self.d_pre_y_max, 3, 0)
        self.layout().addWidget(self.d_pre_y_label, 4, 0)
        self.layout().addWidget(self.d_pre_rows, 5, 0)
        self.layout().addWidget(self.pre_colour, 6, 0)
        self.layout().addWidget(self.pre_lw, 7, 0)
        self.layout().addWidget(self.tag_color, 8, 0)
        self.layout().addWidget(self.tag_lw, 9, 0)
        self.layout().addWidget(self.pre_ls, 10, 0)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 12, 0, 1, 2)

        if vars:
            self.get_values()

    def get_defaults(self):
        self.applySmooth.checkBox.setChecked(self.default["apply_smooth"])
        self.gaussian_stdev.field.setValue(self.default["gaussian_stdev"])
        self.gauss_x_size.field.setValue(self.default["gauss_x_size"])
        self.d_pre_y_max.field.setValue(self.default["d_pre_y_max"])
        self.d_pre_y_label.setText(self.default["d_pre_y_label"])
        self.d_pre_rows.field.setValue(self.default["d_pre_rows"])
        self.pre_colour.select(self.default["pre_color"])
        self.pre_lw.field.setValue(self.default["pre_lw"])
        self.tag_color.select(self.default["tag_color"])
        self.tag_lw.field.setValue(self.default["tag_lw"])
        self.pre_ls.select(self.default["tag_ls"])

    def set_values(self):
        self.vars["apply_smooth"] = self.applySmooth.checkBox.isChecked()
        self.vars["gaussian_stdev"] = self.gaussian_stdev.field.value()
        self.vars["gauss_x_size"] = self.gauss_x_size.field.value()
        self.vars["d_pre_y_max"] = self.d_pre_y_max.field.value()
        self.vars["d_pre_y_label"] = self.d_pre_y_label.text()
        self.vars["d_pre_rows"] = self.d_pre_rows.field.value()
        self.vars["pre_color"] = self.pre_colour.items.currentText()
        self.vars["pre_lw"] = self.pre_lw.field.value()
        self.vars["tag_color"] = self.tag_color.items.currentText()
        self.vars["tag_lw"] = self.tag_lw.field.value()
        self.vars["tag_ls"] = self.pre_ls.items.currentText()
        vars["pre_settings"] = self.vars
        self.accept()


    def get_values(self):
        self.applySmooth.checkBox.setChecked(self.vars["apply_smooth"])
        self.gaussian_stdev.field.setValue(self.vars["gaussian_stdev"])
        self.gauss_x_size.field.setValue(self.vars["gauss_x_size"])
        self.d_pre_y_max.field.setValue(self.vars["d_pre_y_max"])
        self.d_pre_y_label.setText(self.vars["d_pre_y_label"])
        self.d_pre_rows.field.setValue(self.vars["d_pre_rows"])
        self.pre_colour.select(self.vars["pre_color"])
        self.pre_lw.field.setValue(self.vars["pre_lw"])
        self.tag_color.select(self.vars["tag_color"])
        self.tag_lw.field.setValue(self.vars["tag_lw"])
        self.pre_ls.select(self.vars["tag_ls"])
