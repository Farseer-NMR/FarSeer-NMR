from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox
from gui.components.FontComboBox import FontComboBox

from functools import partial
from current.default_config import defaults
from gui.gui_utils import font_weights


class ScatterFlowerPlotPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(ScatterFlowerPlotPopup, self).__init__(parent)
        self.setWindowTitle("Scatter Flower Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["cs_scatter_flower_settings"]
        self.default = defaults["cs_scatter_flower_settings"]

        self.cs_scatter_flower_x_label = LabelledLineEdit(self, "X Label")
        self.cs_scatter_flower_y_label = LabelledLineEdit(self, "Y Label")
        self.cs_scatter_flower_mksize = LabelledSpinBox(self, "Mark Size")
        self.cs_scatter_flower_color_grad = LabelledCheckbox(self, "Colour Gradient")
        self.cs_scatter_flower_color_start = ColourBox(self, "Mark Start Colour")
        self.cs_scatter_flower_color_end = ColourBox(self, "Mark End Colour")

        self.cs_scatter_flower_x_label_fn = FontComboBox(self, "X Label Font")
        self.cs_scatter_flower_x_label_fs = LabelledSpinBox(self, "X Label Font Size")
        self.cs_scatter_flower_x_label_pad = LabelledSpinBox(self, "X Label Padding")
        self.cs_scatter_flower_x_label_weight = LabelledCombobox(self, text="X Label Font Weight", items=font_weights)

        self.cs_scatter_flower_y_label_fn = FontComboBox(self, "Y Label Font")
        self.cs_scatter_flower_y_label_fs = LabelledSpinBox(self, "Y Label Font Size")
        self.cs_scatter_flower_y_label_pad = LabelledSpinBox(self, "Y Label Padding")
        self.cs_scatter_flower_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=font_weights)

        self.cs_scatter_flower_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.cs_scatter_flower_x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size")
        self.cs_scatter_flower_x_ticks_pad = LabelledSpinBox(self, "X Tick Padding")
        self.cs_scatter_flower_x_ticks_weight = LabelledCombobox(self, text="X Tick Weight", items=font_weights)
        self.cs_scatter_flower_x_ticks_rot = LabelledSpinBox(self, "X Tick Rotation")

        self.cs_scatter_flower_y_ticks_fn = FontComboBox(self, "Y Tick Font")
        self.cs_scatter_flower_y_ticks_fs = LabelledSpinBox(self, "Y Tick Font Size")
        self.cs_scatter_flower_y_ticks_pad = LabelledSpinBox(self, "Y Tick Padding")
        self.cs_scatter_flower_y_ticks_weight = LabelledCombobox(self, text="Y Tick Weight", items=font_weights)
        self.cs_scatter_flower_y_ticks_rot = LabelledSpinBox(self, "Y Tick Rotation")

        self.layout().addWidget(self.cs_scatter_flower_x_label, 0, 0)
        self.layout().addWidget(self.cs_scatter_flower_y_label, 1, 0)
        self.layout().addWidget(self.cs_scatter_flower_mksize, 2, 0)
        self.layout().addWidget(self.cs_scatter_flower_color_grad, 3, 0)
        self.layout().addWidget(self.cs_scatter_flower_color_start, 4, 0)
        self.layout().addWidget(self.cs_scatter_flower_color_end, 5, 0)
        self.layout().addWidget(self.cs_scatter_flower_x_label_fn, 6, 0)
        self.layout().addWidget(self.cs_scatter_flower_x_label_fs, 7, 0)


        self.layout().addWidget(self.cs_scatter_flower_x_label_pad, 0, 1)
        self.layout().addWidget(self.cs_scatter_flower_x_label_weight, 1, 1)
        self.layout().addWidget(self.cs_scatter_flower_y_label_fn, 2, 1)
        self.layout().addWidget(self.cs_scatter_flower_y_label_fs, 3, 1)
        self.layout().addWidget(self.cs_scatter_flower_y_label_pad, 4, 1)
        self.layout().addWidget(self.cs_scatter_flower_y_label_weight, 5, 1)
        self.layout().addWidget(self.cs_scatter_flower_x_ticks_fn, 6, 1)
        self.layout().addWidget(self.cs_scatter_flower_x_ticks_fs, 7, 1)


        self.layout().addWidget(self.cs_scatter_flower_x_ticks_pad, 0, 2)
        self.layout().addWidget(self.cs_scatter_flower_x_ticks_weight, 1, 2)
        self.layout().addWidget(self.cs_scatter_flower_x_ticks_rot, 2, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_fn, 3, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_fs, 4, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_pad, 5, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_weight, 6, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_rot, 7, 2)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 1, 1, 2)

        if variables:
            self.get_values()

    def get_defaults(self):
        self.cs_scatter_flower_x_label.field.setText(self.default["cs_scatter_flower_x_label"])
        self.cs_scatter_flower_y_label.field.setText(self.default["cs_scatter_flower_y_label"])
        self.cs_scatter_flower_mksize.setValue(self.default["cs_scatter_flower_mksize"])
        self.cs_scatter_flower_color_grad.setChecked(self.default["cs_scatter_flower_color_grad"])
        self.cs_scatter_flower_color_start.select(self.default["cs_scatter_flower_color_start"])
        self.cs_scatter_flower_color_end.select(self.default["cs_scatter_flower_color_end"])

        self.cs_scatter_flower_x_label_fn.select(self.default["cs_scatter_flower_x_label_fn"])
        self.cs_scatter_flower_x_label_fs.setValue(self.default["cs_scatter_flower_x_label_fs"])
        self.cs_scatter_flower_x_label_pad.setValue(self.default["cs_scatter_flower_x_label_pad"])
        self.cs_scatter_flower_x_label_weight.select(self.default["cs_scatter_flower_x_label_weight"])

        self.cs_scatter_flower_y_label_fn.select(self.default["cs_scatter_flower_y_label_fn"])
        self.cs_scatter_flower_y_label_fs.setValue(self.default["cs_scatter_flower_y_label_fs"])
        self.cs_scatter_flower_y_label_pad.setValue(self.default["cs_scatter_flower_y_label_pad"])
        self.cs_scatter_flower_y_label_weight.select(self.default["cs_scatter_flower_y_label_weight"])

        self.cs_scatter_flower_x_ticks_fn.select(self.default["cs_scatter_flower_x_ticks_fn"])
        self.cs_scatter_flower_x_ticks_fs.setValue(self.default["cs_scatter_flower_x_ticks_fs"])
        self.cs_scatter_flower_x_ticks_pad.setValue(self.default["cs_scatter_flower_x_ticks_pad"])
        self.cs_scatter_flower_x_ticks_weight.select(self.default["cs_scatter_flower_x_ticks_weight"])
        self.cs_scatter_flower_x_ticks_rot.setValue(self.default["cs_scatter_flower_x_ticks_rot"])

        self.cs_scatter_flower_y_ticks_fn.select(self.default["cs_scatter_flower_y_ticks_fn"])
        self.cs_scatter_flower_y_ticks_fs.setValue(self.default["cs_scatter_flower_y_ticks_fs"])
        self.cs_scatter_flower_y_ticks_pad.setValue(self.default["cs_scatter_flower_y_ticks_pad"])
        self.cs_scatter_flower_y_ticks_weight.select(self.default["cs_scatter_flower_y_ticks_weight"])
        self.cs_scatter_flower_y_ticks_rot.setValue(self.default["cs_scatter_flower_y_ticks_rot"])


    def set_values(self, variables):
        self.variables["cs_scatter_flower_x_label"] = self.cs_scatter_flower_x_label.field.text()
        self.variables["cs_scatter_flower_y_label"] = self.cs_scatter_flower_y_label.field.text()
        self.variables["cs_scatter_flower_mksize"] = self.cs_scatter_flower_mksize.field.value()
        self.variables["cs_scatter_flower_color_grad"] = self.cs_scatter_flower_color_grad.checkBox.isChecked()
        self.variables["cs_scatter_flower_color_start"] = self.cs_scatter_flower_color_start.fields.currentText()
        self.variables["cs_scatter_flower_color_end"] = self.cs_scatter_flower_color_end.fields.currentText()

        self.variables["cs_scatter_flower_x_label_fn"] = self.cs_scatter_flower_x_label_fn.fields.currentText()
        self.variables["cs_scatter_flower_x_label_fs"] = self.cs_scatter_flower_x_label_fs.field.value()
        self.variables["cs_scatter_flower_x_label_pad"] = self.cs_scatter_flower_x_label_pad.field.value()
        self.variables["cs_scatter_flower_x_label_weight"] = self.cs_scatter_flower_x_label_weight.fields.currentText()

        self.variables["cs_scatter_flower_y_label_fn"] = self.cs_scatter_flower_y_label_fn.fields.currentText()
        self.variables["cs_scatter_flower_y_label_fs"] = self.cs_scatter_flower_y_label_fs.field.value()
        self.variables["cs_scatter_flower_y_label_pad"] = self.cs_scatter_flower_y_label_pad.field.value()
        self.variables["cs_scatter_flower_y_label_weight"] = self.cs_scatter_flower_y_label_weight.fields.currentText()

        self.variables["cs_scatter_flower_x_label_fn"] = self.cs_scatter_flower_x_label_fn.fields.currentText()
        self.variables["cs_scatter_flower_x_label_fs"] = self.cs_scatter_flower_x_label_fs.field.value()
        self.variables["cs_scatter_flower_x_label_pad"] = self.cs_scatter_flower_x_label_pad.field.value()
        self.variables["cs_scatter_flower_x_label_weight"] = self.cs_scatter_flower_x_label_weight.fields.currentText()

        self.variables["cs_scatter_flower_x_ticks_fn"] = self.cs_scatter_flower_x_ticks_fn.fields.currentText()
        self.variables["cs_scatter_flower_x_ticks_fs"] = self.cs_scatter_flower_x_ticks_fs.field.value()
        self.variables["cs_scatter_flower_x_ticks_pad"] = self.cs_scatter_flower_x_ticks_pad.field.value()
        self.variables["cs_scatter_flower_x_ticks_weight"] = self.cs_scatter_flower_x_ticks_weight.fields.currentText()
        self.variables["cs_scatter_flower_x_ticks_rot"] = self.cs_scatter_flower_x_ticks_rot.field.value()

        self.variables["cs_scatter_flower_y_ticks_fn"] = self.cs_scatter_flower_y_ticks_fn.fields.currentText()
        self.variables["cs_scatter_flower_y_ticks_fs"] = self.cs_scatter_flower_y_ticks_fs.field.value()
        self.variables["cs_scatter_flower_y_ticks_pad"] = self.cs_scatter_flower_y_ticks_pad.field.value()
        self.variables["cs_scatter_flower_y_ticks_weight"] = self.cs_scatter_flower_y_ticks_weight.fields.currentText()
        self.variables["cs_scatter_flower_y_ticks_rot"] = self.cs_scatter_flower_y_ticks_rot.field.value()

        variables["cs_scatter_flower_settings"] = self.variables
        self.accept()

    def get_values(self):

        self.cs_scatter_flower_x_label.field.setText(self.variables["cs_scatter_flower_x_label"])
        self.cs_scatter_flower_y_label.field.setText(self.variables["cs_scatter_flower_y_label"])
        self.cs_scatter_flower_mksize.setValue(self.variables["cs_scatter_flower_mksize"])
        self.cs_scatter_flower_color_grad.setChecked(self.variables["cs_scatter_flower_color_grad"])
        self.cs_scatter_flower_color_start.select(self.variables["cs_scatter_flower_color_start"])
        self.cs_scatter_flower_color_end.select(self.variables["cs_scatter_flower_color_end"])

        self.cs_scatter_flower_x_label_fn.select(self.variables["cs_scatter_flower_x_label_fn"])
        self.cs_scatter_flower_x_label_fs.setValue(self.variables["cs_scatter_flower_x_label_fs"])
        self.cs_scatter_flower_x_label_pad.setValue(self.variables["cs_scatter_flower_x_label_pad"])
        self.cs_scatter_flower_x_label_weight.select(self.variables["cs_scatter_flower_x_label_weight"])

        self.cs_scatter_flower_y_label_fn.select(self.variables["cs_scatter_flower_y_label_fn"])
        self.cs_scatter_flower_y_label_fs.setValue(self.variables["cs_scatter_flower_y_label_fs"])
        self.cs_scatter_flower_y_label_pad.setValue(self.variables["cs_scatter_flower_y_label_pad"])
        self.cs_scatter_flower_y_label_weight.select(self.variables["cs_scatter_flower_y_label_weight"])

        self.cs_scatter_flower_x_ticks_fn.select(self.variables["cs_scatter_flower_x_ticks_fn"])
        self.cs_scatter_flower_x_ticks_fs.setValue(self.variables["cs_scatter_flower_x_ticks_fs"])
        self.cs_scatter_flower_x_ticks_pad.setValue(self.variables["cs_scatter_flower_x_ticks_pad"])
        self.cs_scatter_flower_x_ticks_weight.select(self.variables["cs_scatter_flower_x_ticks_weight"])
        self.cs_scatter_flower_x_ticks_rot.setValue(self.variables["cs_scatter_flower_x_ticks_rot"])

        self.cs_scatter_flower_y_ticks_fn.select(self.variables["cs_scatter_flower_y_ticks_fn"])
        self.cs_scatter_flower_y_ticks_fs.setValue(self.variables["cs_scatter_flower_y_ticks_fs"])
        self.cs_scatter_flower_y_ticks_pad.setValue(self.variables["cs_scatter_flower_y_ticks_pad"])
        self.cs_scatter_flower_y_ticks_weight.select(self.variables["cs_scatter_flower_y_ticks_weight"])
        self.cs_scatter_flower_y_ticks_rot.setValue(self.variables["cs_scatter_flower_y_ticks_rot"])
