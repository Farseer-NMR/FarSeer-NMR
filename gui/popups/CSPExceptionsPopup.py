from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QPushButton
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox

from current.utils import aal3tol1

from gui.gui_utils import defaults
from functools import partial

class CSPExceptionsPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(CSPExceptionsPopup, self).__init__(parent)
        self.setWindowTitle("Alpha By Residue")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        self.alpha_value = self.parent().csp_alpha.field.value()
        if variables:
            self.variables = variables["csp_settings"]["csp_res_exceptions"]

        self.defaults = defaults["csp_settings"]["csp_res_exceptions"]
        self.value_dict = {}
        for ii, res in enumerate(sorted(aal3tol1.keys())):
            self.value_dict[res] = LabelledDoubleSpinBox(self, text=res, min=0, max=1, step=0.01)
            if ii < 5:
                self.layout().addWidget(self.value_dict[res], ii, 0)
            elif 5 <= ii < 10:
                self.layout().addWidget(self.value_dict[res], ii-5, 1)
            elif 10 <= ii < 15:
                self.layout().addWidget(self.value_dict[res], ii-10, 2)
            else:
                self.layout().addWidget(self.value_dict[res], ii-15, 3)


        if variables:
            self.get_values()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 6, 2, 1, 2)

    def set_values(self, variables):
        tmp_dict = {}
        for key, value in self.value_dict.items():
            if value.field.value() > 0:
                tmp_dict[aal3tol1[key]] = value.field.value()
        variables["csp_settings"]["csp_res_exceptions"] = tmp_dict
        self.accept()

    def get_values(self):
        for key, value in self.value_dict.items():
            if aal3tol1[key] in self.variables.keys():
                value.field.setValue(self.variables[aal3tol1[key]])
            else:
                value.field.setValue(self.alpha_value)


    def get_defaults(self):
        for key, value in self.value_dict.items():
            if aal3tol1[key] in self.defaults.keys():
                value.field.setValue(self.variables[aal3tol1[key]])
            else:
                value.field.setValue(self.alpha_value)