from PyQt5.QtWidgets import QDialogButtonBox

from gui.popups.BasePopup import BasePopup
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.FontComboBox import FontComboBox

from gui.gui_utils import font_weights

class CompactBarPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, "compact_bar_settings", "Compact Bar "
                                                                 "Plot")

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

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 0)

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
        self.bar_cols.setValue(self.local_variables["cols_page"])
        self.bar_rows.setValue(self.local_variables["rows_page"])
        self.x_tick_font_size.setValue(self.local_variables["x_ticks_fs"])
        self.x_tick_font.select(self.local_variables["x_ticks_fn"])
        self.x_tick_rotation.setValue(self.local_variables["x_ticks_rot"])
        self.x_tick_weight.select(self.local_variables["x_ticks_weight"])
        self.shade_unassigned_checkbox.setChecked(self.local_variables["unassigned_shade"])
        self.unassigned_shade_alpha.setValue(self.local_variables["unassigned_shade_alpha"])

    def set_values(self):
        self.local_variables["cols_page"] = self.bar_cols.field.value()
        self.local_variables["rows_page"] = self.bar_rows.field.value()
        self.local_variables["x_ticks_fn"] = str(self.x_tick_font.fields.currentText())
        self.local_variables["x_ticks_fs"] = self.x_tick_font_size.field.value()
        self.local_variables["x_ticks_rot"] = self.x_tick_rotation.field.value()
        self.local_variables["x_ticks_weight"] = str(self.x_tick_weight.fields.currentText())
        self.local_variables["unassigned_shade"] = self.shade_unassigned_checkbox.isChecked()
        self.local_variables["unassigned_shade_alpha"] = self.unassigned_shade_alpha.field.value()
        self.variables.update(self.local_variables)

        self.accept()
