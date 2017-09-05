from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.FontComboBox import FontComboBox
from gui.components.ColourBox import ColourBox
from functools import partial

from gui.gui_utils import defaults, font_weights, line_styles


class HeatMapPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(HeatMapPopup, self).__init__(parent)
        self.setWindowTitle("PRE Heat Map")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["heat_map_settings"]
        self.default = defaults["heat_map_settings"]

        self.heat_map_rows = LabelledSpinBox(self, "Rows Per Page")
        self.heat_map_vmin = LabelledDoubleSpinBox(self, "V Min")
        self.heat_map_vmax = LabelledDoubleSpinBox(self, "V Max")
        self.heat_map_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.heat_map_x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size")
        self.heat_map_x_tick_pad = LabelledSpinBox(self, "X Tick Padding")
        self.heat_map_x_tick_weight = LabelledCombobox(self, text="X Tick Font Weight", items=font_weights)
        self.heat_map_x_ticks_rot = LabelledSpinBox(self, "X Tick Rotation")
        self.heat_map_y_label_fn = FontComboBox(self, "Y Label Font")
        self.heat_map_y_label_fs = LabelledSpinBox(self, "Y Label Font Size")
        self.heat_map_y_label_pad = LabelledSpinBox(self, "Y Label Padding")
        self.heat_map_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=font_weights)
        self.heat_map_right_margin = LabelledDoubleSpinBox(self, "Right Margin")
        self.heat_map_bottom_margin = LabelledDoubleSpinBox(self, "Bottom Margin")
        self.heat_map_cbar_font_size = LabelledSpinBox(self, "Colour Bar Font Size")
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

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 9, 1, 1, 1)

        if self.variables:
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

    def set_values(self, variables):
        self.variables["rows"] = self.heat_map_rows.field.value()
        self.variables["vmin"] = self.heat_map_vmin.field.value()
        self.variables["vmax"] = self.heat_map_vmax.field.value()
        self.variables["x_ticks_fs"] = self.heat_map_x_ticks_fs.field.value()
        self.variables["x_ticks_rot"] = self.heat_map_x_ticks_rot.field.value()
        self.variables["x_ticks_fn"] = self.heat_map_x_ticks_fn.fields.currentText()
        self.variables["x_ticks_pad"] = self.heat_map_x_tick_pad.field.value()
        self.variables["x_ticks_weight"] = self.heat_map_x_tick_weight.fields.currentText()
        self.variables["y_label_fs"] = self.heat_map_y_label_fs.field.value()
        self.variables["y_label_pad"] = self.heat_map_y_label_pad.field.value()
        self.variables["y_label_fn"] = self.heat_map_y_label_fn.fields.currentText()
        self.variables["y_label_weight"] = self.heat_map_y_label_weight.fields.currentText()
        self.variables["right_margin"] = self.heat_map_right_margin.field.value()
        self.variables["bottom_margin"] = self.heat_map_bottom_margin.field.value()
        self.variables["cbar_font_size"] = self.heat_map_cbar_font_size.field.value()
        self.variables["tag_line_color"] = self.heat_map_tag_line_color.fields.currentText()
        self.variables["tag_line_ls"] = self.heat_map_tag_ls.fields.currentText()
        self.variables["tag_line_lw"] = self.heat_map_tag_lw.field.value()
        variables["heat_map_settings"] = self.variables
        self.accept()

    def get_values(self):
        self.heat_map_rows.setValue(self.variables["rows"])
        self.heat_map_vmin.setValue(self.variables["vmin"])
        self.heat_map_vmax.setValue(self.variables["vmax"])
        self.heat_map_x_ticks_fs.setValue(self.variables["x_ticks_fs"])
        self.heat_map_x_ticks_rot.setValue(self.variables["x_ticks_rot"])
        self.heat_map_x_ticks_fn.select(self.variables["x_ticks_fn"])
        self.heat_map_x_tick_pad.setValue(self.variables["x_ticks_pad"])
        self.heat_map_x_tick_weight.select(self.variables["x_ticks_weight"])
        self.heat_map_y_label_fs.setValue(self.variables["y_label_fs"])
        self.heat_map_y_label_pad.setValue(self.variables["y_label_pad"])
        self.heat_map_y_label_fn.select(self.variables["y_label_fn"])
        self.heat_map_y_label_weight.select(self.variables["y_label_weight"])
        self.heat_map_right_margin.setValue(self.variables["right_margin"])
        self.heat_map_bottom_margin.setValue(self.variables["bottom_margin"])
        self.heat_map_cbar_font_size.setValue(self.variables["cbar_font_size"])
        self.heat_map_tag_line_color.select(self.variables["tag_line_color"])
        self.heat_map_tag_ls.select(self.variables["tag_line_ls"])
        self.heat_map_tag_lw.setValue(self.variables["tag_line_lw"])

