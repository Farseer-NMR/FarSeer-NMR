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

class ExtendedBarPopup(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(ExtendedBarPopup, self).__init__(parent)
        self.setWindowTitle("Extended Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)

        self.vars = None
        if vars:
            self.vars = vars["extended_bar_settings"]
        self.defaults = defaults["extended_bar_settings"]

        self.bar_cols = LabelledSpinBox(self, text="Columns Per Page")
        self.bar_rows = LabelledSpinBox(self, text="Rows Per Page")
        self.x_tick_font = FontComboBox(self, "X Tick Font")
        self.x_tick_font_size = LabelledSpinBox(self, "X Tick Font Size")
        self.x_tick_rotation = LabelledSpinBox(self, "X Tick Rotation")
        self.x_tick_padding = LabelledDoubleSpinBox(self, "X Tick Padding")
        self.x_tick_font_weight = LabelledCombobox(self, "X Tick Font Weight", items=['normal', 'bold'])
        self.x_tick_colour = LabelledCheckbox(self, "Colour X Ticks?")

        self.layout().addWidget(self.bar_cols, 0, 0)
        self.layout().addWidget(self.bar_rows, 1, 0)
        self.layout().addWidget(self.x_tick_font_size, 2, 0)
        self.layout().addWidget(self.x_tick_font, 3, 0)
        self.layout().addWidget(self.x_tick_padding, 4, 0)
        self.layout().addWidget(self.x_tick_rotation, 5, 0)
        self.layout().addWidget(self.x_tick_font_weight, 6, 0)
        self.layout().addWidget(self.x_tick_colour, 7, 0)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 0)
        if self.vars:
            self.get_values()

    def get_defaults(self):
        self.bar_cols.field.setValue(self.defaults["ext_bar_cols_page"])
        self.bar_rows.field.setValue(self.defaults["ext_bar_rows_page"])
        self.x_tick_font_size.field.setValue(self.defaults["ext_bar_x_ticks_fs"])
        self.x_tick_font.select(self.defaults["ext_bar_x_ticks_fn"])
        self.x_tick_padding.field.setValue(self.defaults["ext_bar_x_ticks_pad"])
        self.x_tick_font_weight.field.setValue(self.defaults["ext_bar_x_ticks_weight"])
        self.x_tick_colour.checkBox.setChecked()(self.defaults["ext_bar_x_ticks_colour"])


    def get_values(self):
        self.bar_cols.field.setValue(self.vars["ext_bar_cols_page"])
        self.bar_rows.field.setValue(self.vars["ext_bar_rows_page"])
        self.x_tick_rotation.field.setValue(self.vars["ext_bar_x_ticks_rot"])
        self.x_tick_font_size.field.setValue(self.vars["ext_bar_y_label_fs"])
        self.x_tick_font.select(self.vars["ext_bar_x_ticks_fn"])
        self.x_tick_padding.field.setValue(self.vars["ext_bar_x_ticks_pad"])

    def set_values(self):
        self.vars["ext_bar_cols_page"] = self.bar_cols.field.value()
        self.vars["ext_bar_rows_page"] = self.bar_rows.field.value()
        self.vars["ext_bar_x_ticks_fn"] = self.x_tick_font.fields.currentText()
        self.vars["ext_bar_x_ticks_fs"] = self.x_tick_font_size.field.value()
        self.vars["ext_bar_x_ticks_rot"] = self.x_tick_rotation.field.value()
        self.vars["ext_bar_x_ticks_pad"] = self.x_tick_padding.field.value()
        self.vars["ext_bar_x_ticks_pad"] = self.x_tick_padding.field.value()
        self.vars["ext_bar_x_ticks_pad"] = self.x_tick_padding.field.value()
        vars["extended_bar_settings"] = self.vars
        self.accept()
