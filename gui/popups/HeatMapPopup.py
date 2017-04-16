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

class HeatMapPopup(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(HeatMapPopup, self).__init__(parent)
        self.setWindowTitle("Residue Evolution Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.vars = None
        if vars:
            self.vars = vars["heat_map_settings"]
        self.default = defaults["heat_map_settings"]

        self.heat_map_rows = LabelledSpinBox(self, "Rows Per Page")
        self.heat_map_vmin = LabelledDoubleSpinBox(self, "V Min")
        self.heat_map_vmax = LabelledDoubleSpinBox(self, "V Max")
        self.heat_map_x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size")
        self.heat_map_x_ticks_rot = LabelledSpinBox(self, "X Tick Rotation")
        self.heat_map_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.heat_map_x_tick_pad = LabelledSpinBox(self, "X Tick Padding")
        self.heat_map_y_label_fs = LabelledSpinBox(self, "Y Label Font Size")
        self.heat_map_y_label_pad = LabelledSpinBox(self, "Y Label Padding")
        self.heat_map_y_label_fn = FontComboBox(self, "Y Label Font")
        self.heat_map_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=['bold', 'normal'])
        self.heat_map_right_margin = LabelledDoubleSpinBox(self, "Right Margin")
        self.heat_map_bottom_margin = LabelledDoubleSpinBox(self, "Bottom Margin")
        self.heat_map_top_margin = LabelledDoubleSpinBox(self, "Top Margin")
        self.heat_map_cbar_font_size = LabelledSpinBox(self, "Colour Bar Font Size")


        self.layout().addWidget(self.heat_map_rows, 0, 0)
        self.layout().addWidget(self.heat_map_vmin, 1, 0)
        self.layout().addWidget(self.heat_map_vmax, 2, 0)
        self.layout().addWidget(self.heat_map_x_ticks_fs, 3, 0)
        self.layout().addWidget(self.heat_map_x_ticks_rot, 4, 0)
        self.layout().addWidget(self.heat_map_x_ticks_fn, 5, 0)
        self.layout().addWidget(self.heat_map_x_tick_pad, 6, 0)
        self.layout().addWidget(self.heat_map_y_label_fs, 7, 0)
        self.layout().addWidget(self.heat_map_y_label_pad, 0, 1)
        self.layout().addWidget(self.heat_map_y_label_fn, 1, 1)
        self.layout().addWidget(self.heat_map_y_label_weight, 2, 1)
        self.layout().addWidget(self.heat_map_right_margin, 3, 1)
        self.layout().addWidget(self.heat_map_bottom_margin, 4, 1)
        self.layout().addWidget(self.heat_map_top_margin, 5, 1)
        self.layout().addWidget(self.heat_map_cbar_font_size, 6, 1)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 10, 0, 1, 2)

        if self.vars:
            self.get_values()

    def get_defaults(self):
        self.heat_map_rows.field.setValue(self.default["heat_map_rows"])
        self.heat_map_vmin.field.setValue(self.default["heat_map_vmin"])
        self.heat_map_vmax.field.setValue(self.default["heat_map_vmax"])
        self.heat_map_x_ticks_fs.field.setValue(self.default["heat_map_x_ticks_fs"])
        self.heat_map_x_ticks_rot.field.setValue(self.default["heat_map_x_ticks_rot"])
        self.heat_map_x_ticks_fn.select(self.default["heat_map_x_ticks_fn"])
        self.heat_map_x_tick_pad.field.setValue(self.default["heat_map_x_tick_pad"])
        self.heat_map_y_label_fs.field.setValue(self.default["heat_map_y_label_fs"])
        self.heat_map_y_label_pad.field.setValue(self.default["heat_map_y_label_pad"])
        self.heat_map_y_label_fn.select(self.default["heat_map_y_label_fn"])
        self.heat_map_y_label_weight.select(self.default["heat_map_y_label_weight"])
        self.heat_map_right_margin.field.setValue(self.default["heat_map_right_margin"])
        self.heat_map_bottom_margin.field.setValue(self.default["heat_map_bottom_margin"])
        self.heat_map_top_margin.field.setValue(self.default["heat_map_top_margin"])
        self.heat_map_cbar_font_size.field.setValue(self.default["heat_map_cbar_font_size"])

    def set_values(self):
        self.vars["heat_map_rows"] = self.heat_map_rows.field.value()
        self.vars["heat_map_vmin"] = self.heat_map_vmin.field.value()
        self.vars["heat_map_vmax"] = self.heat_map_vmax.field.value()
        self.vars["heat_map_x_ticks_fs"] = self.heat_map_x_ticks_fs.field.value()
        self.vars["heat_map_x_ticks_rot"] = self.heat_map_x_ticks_rot.field.value()
        self.vars["heat_map_x_ticks_fn"] = self.heat_map_x_ticks_fn.fields.currentText()
        self.vars["heat_map_x_tick_pad"] = self.heat_map_x_tick_pad.field.value()
        self.vars["heat_map_y_label_fs"] = self.heat_map_y_label_fs.field.value()
        self.vars["heat_map_y_label_pad"] = self.heat_map_y_label_pad.field.value()
        self.vars["heat_map_y_label_fn"] = self.heat_map_y_label_fn.fields.currentText()
        self.vars["heat_map_y_label_weight"] = self.heat_map_y_label_weight.fields.currentText()
        self.vars["heat_map_right_margin"] = self.heat_map_right_margin.field.value()
        self.vars["heat_map_bottom_margin"] = self.heat_map_bottom_margin.field.value()
        self.vars["heat_map_top_margin"] = self.heat_map_top_margin.field.value()
        self.vars["heat_map_cbar_font_size"] = self.heat_map_cbar_font_size.field.value()
        vars["heat_map_settings"] = self.vars
        self.accept()

    def get_values(self):
        self.heat_map_rows.field.setValue(self.vars["heat_map_rows"])
        self.heat_map_vmin.field.setValue(self.vars["heat_map_vmin"])
        self.heat_map_vmax.field.setValue(self.vars["heat_map_vmax"])
        self.heat_map_x_ticks_fs.field.setValue(self.vars["heat_map_x_ticks_fs"])
        self.heat_map_x_ticks_rot.field.setValue(self.vars["heat_map_x_ticks_rot"])
        self.heat_map_x_ticks_fn.select(self.vars["heat_map_x_ticks_fn"])
        self.heat_map_x_tick_pad.field.setValue(self.vars["heat_map_x_tick_pad"])
        self.heat_map_y_label_fs.field.setValue(self.vars["heat_map_y_label_fs"])
        self.heat_map_y_label_pad.field.setValue(self.vars["heat_map_y_label_pad"])
        self.heat_map_y_label_fn.select(self.vars["heat_map_y_label_fn"])
        self.heat_map_y_label_weight.select(self.vars["heat_map_y_label_weight"])
        self.heat_map_right_margin.field.setValue(self.vars["heat_map_right_margin"])
        self.heat_map_bottom_margin.field.setValue(self.vars["heat_map_bottom_margin"])
        self.heat_map_top_margin.field.setValue(self.vars["heat_map_top_margin"])
        self.heat_map_cbar_font_size.field.setValue(self.vars["heat_map_cbar_font_size"])

