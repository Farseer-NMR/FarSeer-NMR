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

class VerticalBarPopup(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(VerticalBarPopup, self).__init__(parent)
        self.setWindowTitle("Vertical Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.vars = None
        if vars:
            self.vars = vars["vert_bar_settings"]
        self.defaults = defaults["vert_bar_settings"]

        self.bar_cols = LabelledSpinBox(self, text="Columns Per Page")
        self.bar_rows = LabelledSpinBox(self, text="Rows Per Page")


        self.layout().addWidget(self.bar_cols, 0, 0)
        self.layout().addWidget(self.bar_rows, 1, 0)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 2, 0, 1, 1)

        if vars:
            self.get_values()

        # self.set_defaults()

    def get_defaults(self):
        self.bar_cols.field.setValue(self.defaults["vert_bar_cols_page"])
        self.bar_rows.field.setValue(self.defaults["vert_bar_rows_page"])


    def get_values(self):
        self.bar_cols.field.setValue(self.vars["vert_bar_cols_page"])
        self.bar_rows.field.setValue(self.vars["vert_bar_rows_page"])

    def set_values(self):
        self.vars["vert_bar_cols_page"] = self.bar_cols.field.value()
        self.vars["vert_bar_rows_page"] = self.bar_rows.field.value()
        vars["vert_bar_settings"] = self.vars
        self.accept()
