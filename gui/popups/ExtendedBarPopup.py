from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.FontComboBox import FontComboBox

from current.default_config import defaults
from gui.gui_utils import font_weights
from functools import partial

class ExtendedBarPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(ExtendedBarPopup, self).__init__(parent)
        self.setWindowTitle("Extended Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)

        self.variables = None
        if variables:
            self.variables = variables["extended_bar_settings"]
        self.defaults = defaults["extended_bar_settings"]

        self.bar_cols = LabelledSpinBox(self, text="Columns Per Page")
        self.bar_rows = LabelledSpinBox(self, text="Rows Per Page")
        self.x_tick_font = FontComboBox(self, "X Tick Font")
        self.x_tick_font_size = LabelledSpinBox(self, "X Tick Font Size")
        self.x_tick_rotation = LabelledSpinBox(self, "X Tick Rotation")
        self.x_tick_font_weight = LabelledCombobox(self, "X Tick Font Weight", items=font_weights)
        self.x_tick_colour = LabelledCheckbox(self, "Colour X Ticks?")

        self.layout().addWidget(self.bar_cols, 0, 0)
        self.layout().addWidget(self.bar_rows, 1, 0)
        self.layout().addWidget(self.x_tick_font_size, 2, 0)
        self.layout().addWidget(self.x_tick_font, 3, 0)
        self.layout().addWidget(self.x_tick_rotation, 4, 0)
        self.layout().addWidget(self.x_tick_font_weight, 5, 0)
        self.layout().addWidget(self.x_tick_colour, 6, 0)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 0)
        if self.variables:
            self.get_values()

    def get_defaults(self):
        self.bar_cols.setValue(self.defaults["ext_bar_cols_page"])
        self.bar_rows.setValue(self.defaults["ext_bar_rows_page"])
        self.x_tick_font.select(self.defaults["ext_bar_x_ticks_fn"])
        self.x_tick_font_size.setValue(self.defaults["ext_bar_x_ticks_fs"])
        self.x_tick_rotation.setValue(self.defaults["ext_bar_x_ticks_rot"])
        self.x_tick_font_weight.select(self.defaults["ext_bar_x_ticks_weight"])
        self.x_tick_colour.setChecked(self.defaults["ext_bar_x_ticks_color_flag"])


    def get_values(self):
        self.bar_cols.setValue(self.variables["ext_bar_cols_page"])
        self.bar_rows.setValue(self.variables["ext_bar_rows_page"])
        self.x_tick_font.select(self.variables["ext_bar_x_ticks_fn"])
        self.x_tick_font_size.setValue(self.variables["ext_bar_x_ticks_fs"])
        self.x_tick_rotation.setValue(self.variables["ext_bar_x_ticks_rot"])
        self.x_tick_font_weight.select(self.variables["ext_bar_x_ticks_weight"])
        self.x_tick_colour.setChecked(self.variables["ext_bar_x_ticks_color_flag"])

    def set_values(self, variables):
        self.variables["ext_bar_cols_page"] = self.bar_cols.field.value()
        self.variables["ext_bar_rows_page"] = self.bar_rows.field.value()
        self.variables["ext_bar_x_ticks_fn"] = str(self.x_tick_font.fields.currentText())
        self.variables["ext_bar_x_ticks_fs"] = self.x_tick_font_size.field.value()
        self.variables["ext_bar_x_ticks_rot"] = self.x_tick_rotation.field.value()
        self.variables["ext_bar_x_ticks_weight"] = str(self.x_tick_font_weight.fields.currentText())
        self.variables["ext_bar_x_ticks_color_flag"] = self.x_tick_colour.checkBox.isChecked()
        variables["extended_bar_settings"] = self.variables
        self.accept()
