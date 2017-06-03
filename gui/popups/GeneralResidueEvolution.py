from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox, QLineEdit, QCheckBox, QDoubleSpinBox, QDialogButtonBox
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


class GeneralResidueEvolution(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(GeneralResidueEvolution, self).__init__(parent)
        self.setWindowTitle("Residue Evolution Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["revo_settings"]
        self.default = defaults["revo_settings"]

        self.revo_subtitle_fn = FontComboBox(self, text="Subtitle Font")
        self.revo_subtitle_fs = LabelledSpinBox(self, text="Subtitle Font Size")
        self.revo_subtitle_pad = LabelledSpinBox(self, text="Subtitle Padding")
        self.revo_subtitle_weight = LabelledCombobox(self, text="Subtitle Font Weight", items=font_weights)

        self.revo_x_label_fn = FontComboBox(self, text="X Label Font Size")
        self.revo_x_label_fs = LabelledSpinBox(self, text="X Label Font Size")
        self.revo_x_label_pad = LabelledSpinBox(self, text="X Label Padding")
        self.revo_x_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=font_weights)

        self.revo_y_label_fn = FontComboBox(self, text="Y Label Font Size")
        self.revo_y_label_fs = LabelledSpinBox(self, text="Y Label Font Size")
        self.revo_y_label_pad = LabelledSpinBox(self, text="Y Label Padding")
        self.revo_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=font_weights)

        self.revo_x_ticks_fn = FontComboBox(self, text="X Tick Font Size")
        self.revo_x_ticks_fs = LabelledSpinBox(self, text="X Tick Font Size")
        self.revo_x_ticks_pad = LabelledSpinBox(self, text="X Tick Padding")
        self.revo_x_ticks_weight = LabelledCombobox(self, text="X Tick Font Weight", items=font_weights)
        self.revo_x_ticks_rotation = LabelledDoubleSpinBox(self, text="X Tick Rotation")

        self.revo_y_ticks_fn = FontComboBox(self, text="Y Tick Font Size")
        self.revo_y_ticks_fs = LabelledSpinBox(self, text="Y Tick Font Size")
        self.revo_y_ticks_pad = LabelledSpinBox(self, text="Y Tick Padding")
        self.revo_y_ticks_weight = LabelledCombobox(self, text="Y Tick Font Weight", items=font_weights)
        self.revo_y_ticks_rot = LabelledDoubleSpinBox(self, text="Y Tick Font Weight")

        self.layout().addWidget(self.revo_subtitle_fn, 0, 0)
        self.layout().addWidget(self.revo_subtitle_fs, 1, 0)
        self.layout().addWidget(self.revo_subtitle_pad, 2, 0)
        self.layout().addWidget(self.revo_subtitle_weight, 3, 0)
        self.layout().addWidget(self.revo_x_label_fn, 4, 0)
        self.layout().addWidget(self.revo_x_label_fs, 5, 0)
        self.layout().addWidget(self.revo_x_label_pad, 6, 0)
        self.layout().addWidget(self.revo_x_label_weight, 7, 0)
        self.layout().addWidget(self.revo_y_label_fn, 8, 0)
        self.layout().addWidget(self.revo_y_label_fs, 9, 0)
        self.layout().addWidget(self.revo_y_label_pad, 10, 0)


        self.layout().addWidget(self.revo_y_label_weight, 0, 1)
        self.layout().addWidget(self.revo_x_ticks_fn, 1, 1)
        self.layout().addWidget(self.revo_x_ticks_fs, 2, 1)
        self.layout().addWidget(self.revo_x_ticks_pad, 3, 1)
        self.layout().addWidget(self.revo_x_ticks_weight, 4, 1)
        self.layout().addWidget(self.revo_x_ticks_rotation, 5, 1)
        self.layout().addWidget(self.revo_y_ticks_fn, 6, 1)
        self.layout().addWidget(self.revo_y_ticks_fs, 7, 1)
        self.layout().addWidget(self.revo_y_ticks_pad, 8, 1)
        self.layout().addWidget(self.revo_y_ticks_weight, 9, 1)
        self.layout().addWidget(self.revo_y_ticks_rot, 10, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 11, 0, 1, 2)

        if variables:
            self.get_values()

    def get_defaults(self):
        self.revo_subtitle_fn.setValue(self.default["revo_subtitle_fn"])
        self.revo_subtitle_fs.select(self.default["revo_subtitle_fs"])
        self.revo_subtitle_pad.setValue(self.default["revo_subtitle_pad"])
        self.revo_subtitle_weight.select(self.default["revo_subtitle_weight"])
        self.revo_x_label_fn.select(self.default["revo_x_label_fn"])
        self.revo_x_label_fs.setValue(self.default["revo_x_label_fs"])
        self.revo_x_label_pad.setValue(self.default["revo_x_label_pad"])
        self.revo_x_label_weight.select(self.default["revo_x_label_weight"])
        self.revo_y_label_fn.select(self.default["revo_y_label_fn"])
        self.revo_y_label_fs.setValue(self.default["revo_y_label_fs"])
        self.revo_y_label_pad.setValue(self.default["revo_y_label_pad"])

        self.y_label_font_weight.select(self.default["revo_y_label_weight"])
        self.revo_x_ticks_fn.select(self.default["revo_x_ticks_fn"])
        self.revo_x_ticks_fs.setValue(self.default["revo_x_ticks_fs"])
        self.revo_x_ticks_pad.setValue(self.default["revo_x_ticks_pad"])
        self.revo_x_ticks_weight.select(self.default["revo_x_ticks_weight"])
        self.revo_x_ticks_rotation.setValue(self.default["revo_x_ticks_rotation"])
        self.revo_y_ticks_fn.select(self.default["revo_y_ticks_fn"])
        self.revo_y_ticks_fs.setValue(self.default["revo_y_ticks_fs"])
        self.revo_y_ticks_pad.setValue(self.default["revo_y_ticks_pad"])
        self.revo_y_ticks_weight.select(self.default["revo_y_ticks_weight"])
        self.revo_y_ticks_rot.setValue(self.default["revo_y_ticks_rot"])



    def set_values(self, variables):
        self.variables["revo_subtitle_fn"] = self.revo_cols.fields.currentText()
        self.variables["revo_subtitle_fs"] = self.revo_rows.field.value()
        self.variables["revo_subtitle_pad"] = self.revo_title_y.field.value()
        self.variables["revo_subtitle_weight"] = self.revo_font.fields.currentText()
        self.variables["revo_x_label_fn"] = self.revo_font_size.fields.currentText()
        self.variables["revo_x_label_fs"] = self.revo_font_size.field.value()
        self.variables["revo_x_label_pad"] = self.x_label_padding.field.value()
        self.variables["revo_x_label_weight"] = self.x_label_font_weight.fields.currentText()
        self.variables["revo_y_label_fn"] = self.y_label_font.fields.currentText()
        self.variables["revo_y_label_fs"] = self.y_label_font_size.field.value()
        self.variables["revo_y_label_pad"] = self.y_label_padding.field.value()

        self.variables["revo_y_label_weight"] = self.y_label_font_weight.fields.currentText()
        self.variables["revo_x_ticks_fn"] = self.revo_x_ticks_fn.fields.currentText()
        self.variables["revo_x_ticks_fs"] = self.revo_x_ticks_fs.field.value()
        self.variables["revo_x_ticks_pad"] = self.revo_x_ticks_pad.field.value()
        self.variables["revo_x_ticks_weight"] = self.revo_x_ticks_weight.fields.currentText()
        self.variables["revo_x_ticks_rotation"] = self.revo_x_ticks_rotation.field.value()
        self.variables["revo_y_ticks_fn"] = self.revo_y_ticks_fn.fields.currentText()
        self.variables["revo_y_ticks_fs"] = self.revo_y_ticks_fs.field.value()
        self.variables["revo_y_ticks_pad"] = self.revo_y_ticks_pad.field.value()
        self.variables["revo_y_ticks_weight"] = self.revo_y_ticks_weight.fields.currentText()
        self.variables["revo_y_ticks_rot"] = self.revo_y_ticks_rot.field.value()
        variables["revo_settings"] = self.variables
        self.accept()

    def get_values(self):
        self.revo_subtitle_fn.setValue(self.variables["revo_subtitle_fn"])
        self.revo_subtitle_fs.select(self.variables["revo_subtitle_fs"])
        self.revo_subtitle_pad.setValue(self.variables["revo_subtitle_pad"])
        self.revo_subtitle_weight.select(self.variables["revo_subtitle_weight"])
        self.revo_x_label_fn.select(self.variables["revo_x_label_fn"])
        self.revo_x_label_fs.setValue(self.variables["revo_x_label_fs"])
        self.revo_x_label_pad.setValue(self.variables["revo_x_label_pad"])
        self.revo_x_label_weight.select(self.variables["revo_x_label_weight"])
        self.revo_y_label_fn.select(self.variables["revo_y_label_fn"])
        self.revo_y_label_fs.setValue(self.variables["revo_y_label_fs"])
        self.revo_y_label_pad.setValue(self.variables["revo_y_label_pad"])

        self.y_label_font_weight.select(self.variables["revo_y_label_weight"])
        self.revo_x_ticks_fn.select(self.variables["revo_x_ticks_fn"])
        self.revo_x_ticks_fs.setValue(self.variables["revo_x_ticks_fs"])
        self.revo_x_ticks_pad.setValue(self.variables["revo_x_ticks_pad"])
        self.revo_x_ticks_weight.select(self.variables["revo_x_ticks_weight"])
        self.revo_x_ticks_rotation.setValue(self.variables["revo_x_ticks_rotation"])
        self.revo_y_ticks_fn.select(self.variables["revo_y_ticks_fn"])
        self.revo_y_ticks_fs.setValue(self.variables["revo_y_ticks_fs"])
        self.revo_y_ticks_pad.setValue(self.variables["revo_y_ticks_pad"])
        self.revo_y_ticks_weight.select(self.variables["revo_y_ticks_weight"])
        self.revo_y_ticks_rot.setValue(self.variables["revo_y_ticks_rot"])
