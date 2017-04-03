from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox, QLineEdit, QCheckBox, QDoubleSpinBox, QDialogButtonBox


class VerticalBarPopup(QDialog):

    def __init__(self, parent=None, **kw):
        super(VerticalBarPopup, self).__init__(parent)
        self.setWindowTitle("Vertical Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)

        bar_cols_label = QLabel("Columns Per Page", self)
        bar_rows_label = QLabel("Rows Per Page", self)


        self.layout().addWidget(bar_cols_label, 0, 0)
        self.layout().addWidget(bar_rows_label, 1, 0)


        self.bar_cols = QSpinBox()
        self.bar_rows = QSpinBox()


        self.layout().addWidget(self.bar_cols, 0, 1)
        self.layout().addWidget(self.bar_rows, 1, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.setValues)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.set_defaults)

        self.layout().addWidget(self.buttonBox, 2, 0, 1, 2)


    def set_defaults(self):
        self.bar_cols.setValue(6)
        self.bar_rows.setValue(1)


    def setValues(self):
        self.accept()
