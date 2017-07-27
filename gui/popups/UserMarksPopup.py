from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QDialogButtonBox, QPushButton, QWidget
from gui.components.LabelledLineEdit import LabelledLineEdit
from functools import partial
from current.default_config import defaults

class UserMarksPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(UserMarksPopup, self).__init__(parent)
        self.setWindowTitle("User Defined Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.marker_rows = 0
        layout2 = QGridLayout()
        layout1 = QGridLayout()
        self.mainWidget = QWidget(self)
        self.buttonWidget = QWidget(self)
        self.mainWidget.setLayout(layout1)
        self.buttonWidget.setLayout(layout2)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.setValues, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.set_defaults)
        self.buttonWidget.layout().addWidget(self.buttonBox)

        self.setLayout(grid)
        self.layout().addWidget(self.mainWidget, 0, 0)
        self.layout().addWidget(self.buttonWidget, 1, 0)
        self.pairs = []
        if variables:
            self.variables = variables
            self.setValuesFromConfig()
        else:
            key = LabelledLineEdit(self, text='key')
            value = LabelledLineEdit(self, text='value')
            addButton = QPushButton("Add", self)
            removeButton = QPushButton("Remove", self)
            addButton.clicked.connect(self.add_row_to_popup)
            removeButton.clicked.connect(partial(self.remove_row_to_popup, self.marker_rows))
            addButton.setFixedWidth(50)
            removeButton.setFixedWidth(50)
            self.pairs.append([key, value, addButton, removeButton])

            self.mainWidget.layout().addWidget(key, self.marker_rows, 0)
            self.mainWidget.layout().addWidget(value, self.marker_rows, 1)
            self.mainWidget.layout().addWidget(addButton, self.marker_rows, 2)
            self.mainWidget.layout().addWidget(removeButton, self.marker_rows, 3)
            self.marker_rows += 1
            # self.pairs.append([self.buttonBox])
            self.marker_rows += 1


    def add_row_to_popup(self):
        key = LabelledLineEdit(self, text='key')
        value = LabelledLineEdit(self, text='value')
        addButton = QPushButton("Add", self)
        addButton.clicked.connect(self.add_row_to_popup)
        removeButton = QPushButton("Remove", self)
        removeButton.clicked.connect(partial(self.remove_row_to_popup, self.marker_rows))
        # addButton.setFixedWidth(50)
        # removeButton.setFixedWidth(50)
        self.pairs.append([key, value, addButton, removeButton])
        self.mainWidget.layout().addWidget(key, self.marker_rows, 0)
        self.mainWidget.layout().addWidget(value, self.marker_rows, 1)
        self.mainWidget.layout().addWidget(addButton, self.marker_rows, 2)
        self.mainWidget.layout().addWidget(removeButton, self.marker_rows, 3)
        self.marker_rows += 1
        # print(self.pairs)
        print(self.marker_rows)

    def remove_row_to_popup(self, index):

        print(index, 'remove index number')
        self.marker_rows -= 1
        colCount = self.mainWidget.layout().columnCount()
        for m in range(0, colCount):
            item = self.mainWidget.layout().itemAtPosition(index, m)
            if item:
                if item.widget():
                    item.widget().hide()
            self.mainWidget.layout().removeItem(item)
        # if index in self.pairs:
        self.pairs.pop(index)

    def setValuesFromConfig(self):
        for i in range(self.marker_rows):
            self.remove_row_to_popup(i)

        self.marker_rows = 0

        for key1, value1 in self.variables["user_mark_settings"].items():

            key = LabelledLineEdit(self, text='key')
            key.field.setText(key1)
            value = LabelledLineEdit(self, text='value')
            value.field.setText(value1)
            addButton = QPushButton("Add", self)
            addButton.clicked.connect(self.add_row_to_popup)
            removeButton = QPushButton("Remove", self)
            removeButton.clicked.connect(partial(self.remove_row_to_popup, self.marker_rows))
            # addButton.setFixedWidth(50)
            # removeButton.setFixedWidth(50)
            self.pairs.append([key, value, addButton, removeButton])
            self.mainWidget.layout().addWidget(key, self.marker_rows, 0)
            self.mainWidget.layout().addWidget(value, self.marker_rows, 1)
            self.mainWidget.layout().addWidget(addButton, self.marker_rows, 2)
            self.mainWidget.layout().addWidget(removeButton, self.marker_rows, 3)
            self.marker_rows += 1
            print(self.marker_rows, 'setvalsfromconfig')


    def set_defaults(self):

        for i in range(self.marker_rows):
            self.remove_row_to_popup(i)

        self.marker_rows = 0

        for key1, value1 in defaults["user_mark_settings"].items():

            key = LabelledLineEdit(self, text='key')
            key.field.setText(key1)
            value = LabelledLineEdit(self, text='value')
            value.field.setText(value1)
            addButton = QPushButton("Add", self)
            addButton.clicked.connect(self.add_row_to_popup)
            removeButton = QPushButton("Remove", self)
            removeButton.clicked.connect(partial(self.remove_row_to_popup, self.marker_rows))
            # addButton.setFixedWidth(100)
            # removeButton.setFixedWidth(100)
            self.pairs.append([key, value, addButton, removeButton])
            self.mainWidget.layout().addWidget(key, self.marker_rows, 0)
            self.mainWidget.layout().addWidget(value, self.marker_rows, 1)
            self.mainWidget.layout().addWidget(addButton, self.marker_rows, 2)
            self.mainWidget.layout().addWidget(removeButton, self.marker_rows, 3)
            self.marker_rows += 1


    def setValues(self, variables):
        user_dict = {pair[0].field.text():pair[1].field.text() for pair in self.pairs}
        variables["user_mark_settings"] = user_dict
        print(variables["user_mark_settings"])
        self.accept()
