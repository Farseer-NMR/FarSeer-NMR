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

class TitrationPlotPopup(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(TitrationPlotPopup, self).__init__(parent)
        self.setWindowTitle("Residue Evolution Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.vars = None
        if vars:
            self.vars = vars["tplot_settings"]
        # self.default = defaults["tplot_settings"]

        self.tplot_subtitle_fn = FontComboBox(self, "Subtitle Font")
        self.tplot_title_fs = LabelledSpinBox(self, "Subtitle Font Size")
        self.tplot_subtitle_pad = LabelledDoubleSpinBox(self, "Subtitle Padding")
        self.tplot_subtitle_weight = LabelledCombobox(self, text="Subtitle Font Weight", items=['bold', 'italic', 'normal'])

        self.tplot_x_label_fn = FontComboBox(self, "X Font Label")
        self.tplot_x_label_fs = LabelledSpinBox(self, "X Label Font Size")
        self.tplot_x_label_pad = LabelledSpinBox(self, "X Label Padding")
        self.tplot_x_label_weight = LabelledCombobox(self, text="X Label Font Weight", items=['bold', 'normal'])

        self.tplot_y_label_fn = FontComboBox(self, "Y Label Font")
        self.tplot_y_label_fs = LabelledSpinBox(self, "Y Label Font Size")
        self.tplot_y_label_pad = LabelledSpinBox(self, "Y Label Padding")
        self.tplot_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=['bold', 'normal'])

        self.tplot_x_ticks_pad = LabelledSpinBox(self, "X Tick Padding")
        self.tplot_x_ticks_len = LabelledSpinBox(self, "X Tick Length")

        self.tplot_y_ticks_fn = FontComboBox(self, "Y Tick Font")
        self.tplot_y_ticks_fs = LabelledSpinBox(self, "Y Tick Font Size")
        self.tplot_y_ticks_rot = LabelledSpinBox(self, "Y Tick Rotation")
        self.tplot_y_ticks_pad = LabelledDoubleSpinBox(self, "Y Tick Padding")
        self.tplot_y_ticks_weight = LabelledCombobox(self, text="Y Tick Font Weight", items=['bold', 'normal'])
        self.tplot_y_ticks_len = LabelledDoubleSpinBox(self, "Y Tick Length")
        self.tplot_y_grid_flag = LabelledCheckbox(self, "Show Y Grid")
        self.tplot_y_grid_color = ColourBox(self, "Y Grid Colour")
        self.tplot_y_grid_linestyle = LabelledCombobox(self, text="Y Grid Line Style", items=['-', '--', '-.', ':'])
        self.tplot_y_grid_linewidth = LabelledDoubleSpinBox(self, "Y Grid Line Width")
        self.tplot_y_grid_alpha = LabelledDoubleSpinBox(self, "Y Grid Alpha")
        self.tplot_vspace = LabelledDoubleSpinBox(self, "Plot Vertical Spacing")



        self.layout().addWidget(self.tplot_subtitle_fn, 0, 0)
        self.layout().addWidget(self.tplot_title_fs, 1, 0)
        self.layout().addWidget(self.tplot_subtitle_pad, 2, 0)
        self.layout().addWidget(self.tplot_subtitle_weight, 3, 0)
        self.layout().addWidget(self.tplot_title_fs, 4, 0)
        self.layout().addWidget(self.tplot_x_label_fn, 5, 0)
        self.layout().addWidget(self.tplot_x_label_fs, 6, 0)
        self.layout().addWidget(self.tplot_x_label_pad, 7, 0)
        self.layout().addWidget(self.tplot_x_label_weight, 8, 0)
        self.layout().addWidget(self.tplot_x_ticks_pad, 9, 0)

        self.layout().addWidget(self.tplot_x_ticks_len, 0, 1)
        self.layout().addWidget(self.tplot_y_label_fn, 1, 1)
        self.layout().addWidget(self.tplot_y_label_fs, 2, 1)
        self.layout().addWidget(self.tplot_y_label_pad, 3, 1)
        self.layout().addWidget(self.tplot_y_label_fs, 4, 1)
        self.layout().addWidget(self.tplot_y_label_pad, 5, 1)
        self.layout().addWidget(self.tplot_y_label_weight, 6, 1)
        self.layout().addWidget(self.tplot_y_ticks_fn, 7, 1)
        self.layout().addWidget(self.tplot_y_ticks_fs, 8, 1)
        self.layout().addWidget(self.tplot_y_ticks_rot, 9, 1)

        self.layout().addWidget(self.tplot_y_ticks_pad, 0, 2)
        self.layout().addWidget(self.tplot_y_ticks_weight, 1, 2)
        self.layout().addWidget(self.tplot_y_ticks_len, 2, 2)
        self.layout().addWidget(self.tplot_y_grid_flag, 3, 2)
        self.layout().addWidget(self.tplot_y_grid_color, 4, 2)
        self.layout().addWidget(self.tplot_y_grid_linestyle, 5, 2)
        self.layout().addWidget(self.tplot_y_grid_linewidth, 6, 2)
        self.layout().addWidget(self.tplot_y_grid_alpha, 7, 2)
        self.layout().addWidget(self.tplot_vspace, 8, 2)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 10, 0, 1, 2)

        if vars:
            self.get_values()

    def get_defaults(self):
        self.tplot_subtitle_fn.field.select(self.default["tplot_subtitle_fn"])
        self.tplot_title_fs.field.setValue(self.default["tplot_title_fs"])
        self.tplot_subtitle_pad.field.setValue(self.default["tplot_title_y"])
        self.tplot_subtitle_weight.select(self.default["tplot_title_fn"])
        self.tplot_x_label_fn.select(self.default["tplot_x_label_fn"])
        self.tplot_x_label_fs.field.setValue(self.default["tplot_x_label_fs"])
        self.tplot_x_label_pad.field.setValue(self.default["tplot_x_label_pad"])
        self.tplot_x_label_weight.select(self.default["tplot_x_label_weight"])
        self.tplot_y_label_fn.select(self.default["tplot_y_label_fn"])
        self.tplot_y_label_fs.field.setValue(self.default["tplot_y_label_fs"])
        self.tplot_y_label_pad.field.setValue(self.default["tplot_y_label_pad"])
        self.tplot_y_label_weight.select(self.default["tplot_y_label_weight"])
        self.tplot_x_ticks_pad.field.setValue(self.default["tplot_x_ticks_pad"])
        self.tplot_x_ticks_len.field.setValue(self.default["tplot_x_ticks_fs"])

        self.tplot_y_ticks_fn.field.select(self.default["tplot_y_ticks_fn"])
        self.tplot_y_ticks_fs.field.setValue(self.default["tplot_y_ticks_fs"])
        self.tplot_y_ticks_rot.field.setValue(self.default["tplot_y_ticks_rot"])
        self.tplot_y_ticks_pad.field.setValue(self.default["tplot_y_ticks_pad"])
        self.tplot_y_ticks_weight.select(self.default["tplot_y_ticks_weight"])
        self.tplot_y_ticks_len.field.setValue(self.default["tplot_y_ticks_len"])
        self.tplot_y_grid_flag.checkBox.setChecked(self.default["tplot_y_grid_flag"])
        self.tplot_y_grid_color.select(self.default["tplot_y_grid_color"])
        self.tplot_y_grid_linestyle.field.select(self.default["tplot_y_grid_linestyle"])
        self.tplot_y_grid_linewidth.field.setValue(self.default["tplot_y_grid_linewidth"])
        self.tplot_y_grid_alpha.field.setValue(self.default["tplot_y_grid_alpha"])


    def set_values(self):
        self.vars["tplot_subtitle_fn"] = self.tplot_subtitle_fn.field.currentText()
        self.vars["tplot_title_fs"] = self.tplot_title_y.field.value()
        self.vars["tplot_subtitle_pad"] = self.tplot_subtitle_pad.field.value()
        self.vars["tplot_subtitle_weight"] = self.tplot_subtitle_weight.fields.currentText()
        self.vars["tplot_x_label_fn"] = self.tplot_x_label_fn.fields.currentText()
        self.vars["tplot_x_label_fs"] = self.tplot_x_label_fs.field.value()
        self.vars["tplot_x_label_pad"] = self.tplot_x_label_pad.field.value()
        self.vars["tplot_x_label_weight"] = self.tplot_x_label_weight.fields.currentText()
        self.vars["tplot_y_label_fn"] = self.tplot_y_label_fn.fields.currentText()
        self.vars["tplot_y_label_fs"] = self.tplot_y_label_fs.field.value()
        self.vars["tplot_y_label_pad"] = self.tplot_y_label_pad.field.value()
        self.vars["tplot_y_label_weight"] = self.tplot_y_label_weight.fields.currentText()

        self.vars["tplot_x_ticks_pad"] = self.tplot_x_ticks_pad.field.value()
        self.vars["tplot_x_ticks_len"] = self.tplot_x_ticks_len.field.value()

        self.vars["tplot_y_ticks_fn"] = self.tplot_y_ticks_pad.fields.currentText()
        self.vars["tplot_y_ticks_fs"] = self.tplot_y_ticks_fs.field.value()
        self.vars["tplot_y_ticks_rot"] = self.tplot_y_ticks_rot.field.value()
        self.vars["tplot_y_ticks_pad"] = self.tplot_y_ticks_pad.field.value()

        self.vars["tplot_y_ticks_weight"] = self.tplot_y_ticks_weight.fields.currentText()
        self.vars["tplot_y_ticks_len"] = self.tplot_y_ticks_len.field.value()
        self.vars["tplot_y_grid_flag"] = self.tplot_y_grid_flag.checkBox.isChecked()
        self.vars["tplot_y_grid_color"] = self.tplot_y_grid_color.fields.currentText()
        self.vars["tplot_y_grid_linestyle"] = self.tplot_y_grid_linestyle.fields.currentText()
        self.vars["tplot_y_grid_linewidth"] = self.tplot_y_grid_linewidth.field.value()
        self.vars["tplot_y_grid_alpha"] = self.tplot_y_grid_alpha.field.value()

        vars["tplot_settings"] = self.vars
        self.accept()

    def get_values(self):
        self.tplot_subtitle_fn.field.select(self.vars["tplot_subtitle_fn"])
        self.tplot_title_fs.field.setValue(self.vars["tplot_title_fs"])
        self.tplot_subtitle_pad.field.setValue(self.vars["tplot_title_y"])
        self.tplot_subtitle_weight.select(self.vars["tplot_title_fn"])
        self.tplot_x_label_fn.select(self.vars["tplot_x_label_fn"])
        self.tplot_x_label_fs.field.setValue(self.vars["tplot_x_label_fs"])
        self.tplot_x_label_pad.field.setValue(self.vars["tplot_x_label_pad"])
        self.tplot_x_label_weight.select(self.vars["tplot_x_label_weight"])
        self.tplot_y_label_fn.select(self.vars["tplot_y_label_fn"])
        self.tplot_y_label_fs.field.setValue(self.vars["tplot_y_label_fs"])
        self.tplot_y_label_pad.field.setValue(self.vars["tplot_y_label_pad"])
        self.tplot_y_label_weight.select(self.vars["tplot_y_label_weight"])
        self.tplot_x_ticks_pad.field.setValue(self.vars["tplot_x_ticks_pad"])
        self.tplot_x_ticks_len.field.setValue(self.vars["tplot_x_ticks_fs"])

        self.tplot_y_ticks_fn.field.select(self.vars["tplot_y_ticks_fn"])
        self.tplot_y_ticks_fs.field.setValue(self.vars["tplot_y_ticks_fs"])
        self.tplot_y_ticks_rot.field.setValue(self.vars["tplot_y_ticks_rot"])
        self.tplot_y_ticks_pad.field.setValue(self.vars["tplot_y_ticks_pad"])
        self.tplot_y_ticks_weight.select(self.vars["tplot_y_ticks_weight"])
        self.tplot_y_ticks_len.field.setValue(self.vars["tplot_y_ticks_len"])
        self.tplot_y_grid_flag.checkBox.setChecked(self.vars["tplot_y_grid_flag"])
        self.tplot_y_grid_color.select(self.vars["tplot_y_grid_color"])
        self.tplot_y_grid_linestyle.field.select(self.vars["tplot_y_grid_linestyle"])
        self.tplot_y_grid_linewidth.field.setValue(self.vars["tplot_y_grid_linewidth"])
        self.tplot_y_grid_alpha.field.setValue(self.vars["tplot_y_grid_alpha"])
