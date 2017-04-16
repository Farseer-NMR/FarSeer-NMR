from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox, QLineEdit, QCheckBox, QDoubleSpinBox, QDialogButtonBox
from gui.components.LabelledLineEdit import LabelledLineEdit

import json
from current.default_config import defaults

class UserMarksPopup(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(UserMarksPopup, self).__init__(parent)
        self.setWindowTitle("Vertical Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        if vars:
            self.vars = vars["user_mark_settings"]
        self.default = defaults["user_mark_settings"]
        self.h0 = LabelledLineEdit(self, text='H0')
        self.v0 = LabelledLineEdit(self, text='V0')
        self.p1 = LabelledLineEdit(self, text='p1')
        self.p2 = LabelledLineEdit(self, text='p2')
        self.p3 = LabelledLineEdit(self, text='p3')
        self.p4 = LabelledLineEdit(self, text='p4')
        self.p5 = LabelledLineEdit(self, text='p5')

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.setValues)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.set_defaults)

        self.layout().addWidget(self.h0, 0, 0, 1, 1)
        self.layout().addWidget(self.v0, 1, 0, 1, 1)
        self.layout().addWidget(self.p1, 2, 0, 1, 1)
        self.layout().addWidget(self.p2, 3, 0, 1, 1)
        self.layout().addWidget(self.p3, 4, 0, 1, 1)
        self.layout().addWidget(self.p4, 5, 0, 1, 1)
        self.layout().addWidget(self.p5, 6, 0, 1, 1)

        self.layout().addWidget(self.buttonBox, 7, 0, 1, 2)
        print(vars)
        if vars:
            self.setValuesFromConfig()


    def setValuesFromConfig(self):
        values = self.vars
        self.h0.field.setText(values['h0'])
        self.v0.field.setText(values['v0'])
        self.p1.field.setText(values['p1'])
        self.p2.field.setText(values['p2'])
        self.p3.field.setText(values['p3'])
        self.p4.field.setText(values['p4'])
        self.p5.field.setText(values['p5'])

    def set_defaults(self):
        self.h0.field.setText('H')
        self.v0.field.setText('V')
        self.p1.field.setText('1')
        self.p2.field.setText('2')
        self.p3.field.setText('3')
        self.p4.field.setText('4')
        self.p5.field.setText('5')


    def setValues(self):
        self.accept()
