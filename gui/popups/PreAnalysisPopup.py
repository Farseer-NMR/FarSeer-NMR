from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox

from gui.gui_utils import defaults
from functools import partial

class PreAnalysisPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(PreAnalysisPopup, self).__init__(parent)
        self.setWindowTitle("PRE Settings")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["pre_settings"]
        self.default = defaults["pre_settings"]

        self.gaussian_stdev = LabelledDoubleSpinBox(self, "Gaussian Stdev")
        self.gauss_x_size = LabelledDoubleSpinBox(self, "Gaussian X Size")

        self.layout().addWidget(self.gauss_x_size, 0, 0)
        self.layout().addWidget(self.gaussian_stdev, 1, 0)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 2, 0)

        if variables:
            self.get_values()

    def get_defaults(self):
        self.gauss_x_size.field.setValue(self.default["gauss_x_size"])
        self.gaussian_stdev.field.setValue(self.default["gaussian_stdev"])

    def set_values(self, variables):
        self.variables["gaussian_stdev"] = self.gaussian_stdev.field.value()
        self.variables["gauss_x_size"] = self.gauss_x_size.field.value()
        variables["pre_settings"] = self.variables
        self.accept()


    def get_values(self):
        self.gaussian_stdev.setValue(self.variables["gaussian_stdev"])
        self.gauss_x_size.setValue(self.variables["gauss_x_size"])
