from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from functools import partial

from gui.gui_utils import defaults

class VerticalBarPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(VerticalBarPopup, self).__init__(parent)
        self.setWindowTitle("Vertical Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["vert_bar_settings"]
        self.defaults = defaults["vert_bar_settings"]

        self.bar_cols = LabelledSpinBox(self, text="Columns Per Page", min=1, step=1)
        self.bar_rows = LabelledSpinBox(self, text="Rows Per Page", min=1, step=1)


        self.layout().addWidget(self.bar_cols, 0, 0)
        self.layout().addWidget(self.bar_rows, 1, 0)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 2, 0, 1, 1)

        if variables:
            self.get_values()

        # self.set_defaults()

    def get_defaults(self):
        self.bar_cols.setValue(self.defaults["cols_page"])
        self.bar_rows.setValue(self.defaults["rows_page"])


    def get_values(self):
        self.bar_cols.setValue(self.variables["cols_page"])
        self.bar_rows.setValue(self.variables["rows_page"])

    def set_values(self, variables):
        self.variables["cols_page"] = self.bar_cols.field.value()
        self.variables["rows_page"] = self.bar_rows.field.value()
        variables["vert_bar_settings"] = self.variables
        self.accept()
