from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.FontComboBox import FontComboBox

from gui.gui_utils import font_weights, defaults
from functools import partial

class CompactBarPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(CompactBarPopup, self).__init__(parent)
        self.setWindowTitle("Compact Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["compact_bar_settings"]
        self.defaults = defaults["compact_bar_settings"]

        self.bar_cols = LabelledSpinBox(self, text="Columns Per Page", min=1, step=1)
        self.bar_rows = LabelledSpinBox(self, text="Rows Per Page", min=1, step=1)
        self.x_tick_font = FontComboBox(self, "X Tick Font")
        self.x_tick_font_size = LabelledSpinBox(self, "X Tick Font Size", min=0, step=1)
        self.x_tick_rotation = LabelledSpinBox(self, "X Tick Rotation", min=0, max=360, step=1)
        self.x_tick_weight = LabelledCombobox(self, "X Tick Font Weight", items=font_weights)
        self.shade_unassigned_checkbox = LabelledCheckbox(self, "Shade Unassigned?")
        self.unassigned_shade_alpha = LabelledDoubleSpinBox(self, "Unassigned Shade Transparency", min=0, max=1, step=0.1)


        self.layout().addWidget(self.bar_cols, 0, 0)
        self.layout().addWidget(self.bar_rows, 1, 0)
        self.layout().addWidget(self.x_tick_font_size, 2, 0)
        self.layout().addWidget(self.x_tick_font, 3, 0)
        self.layout().addWidget(self.x_tick_rotation, 4, 0)
        self.layout().addWidget(self.x_tick_weight, 5, 0)
        self.layout().addWidget(self.shade_unassigned_checkbox, 6, 0)
        self.layout().addWidget(self.unassigned_shade_alpha, 7, 0)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 0)

        if self.variables:
            self.get_values()

    def get_defaults(self):
        self.bar_cols.setValue(self.defaults["cols_page"])
        self.bar_rows.setValue(self.defaults["rows_page"])
        self.x_tick_font_size.setValue(self.defaults["x_ticks_fs"])
        self.x_tick_font.select(self.defaults["x_ticks_fn"])
        self.x_tick_rotation.setValue(self.defaults["x_ticks_rot"])
        self.x_tick_weight.select(self.defaults["x_ticks_weight"])
        self.shade_unassigned_checkbox.setChecked(self.defaults["unassigned_shade"])
        self.unassigned_shade_alpha.setValue(self.defaults["unassigned_shade_alpha"])

    def get_values(self):
        self.bar_cols.setValue(self.variables["cols_page"])
        self.bar_rows.setValue(self.variables["rows_page"])
        self.x_tick_font_size.setValue(self.variables["x_ticks_fs"])
        self.x_tick_font.select(self.variables["x_ticks_fn"])
        self.x_tick_rotation.setValue(self.variables["x_ticks_rot"])
        self.x_tick_weight.select(self.variables["x_ticks_weight"])
        self.shade_unassigned_checkbox.setChecked(self.variables["unassigned_shade"])
        self.unassigned_shade_alpha.setValue(self.variables["unassigned_shade_alpha"])

    def set_values(self, variables):
        self.variables["cols_page"] = self.bar_cols.field.value()
        self.variables["rows_page"] = self.bar_rows.field.value()
        self.variables["x_ticks_fn"] = str(self.x_tick_font.fields.currentText())
        self.variables["x_ticks_fs"] = self.x_tick_font_size.field.value()
        self.variables["x_ticks_rot"] = self.x_tick_rotation.field.value()
        self.variables["x_ticks_weight"] = str(self.x_tick_weight.fields.currentText())
        self.variables["unassigned_shade"] = self.shade_unassigned_checkbox.isChecked()
        self.variables["unassigned_shade_alpha"] = self.unassigned_shade_alpha.field.value()
        variables["compact_bar_settings"] = self.variables
        self.accept()
