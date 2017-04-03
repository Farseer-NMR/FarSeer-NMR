from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QGridLayout
from PyQt5 import QtCore

class LabelledCheckbox(QWidget):

    def __init__(self, parent, text, callback=None, fixed=False, **kw):
        QWidget.__init__(self, parent)
        grid = QGridLayout()
        self.setLayout(grid)
        checkBox = QCheckBox()
        checkBox.setFixedWidth(20)

        label = QLabel(text, self)

        self.layout().addWidget(checkBox, 0, 0)
        self.layout().addWidget(label, 0, 1)
        if fixed:
            self.setFixedWidth(50)

        if callback:
            self.setCallback(callback)

        label.setAlignment(QtCore.Qt.AlignLeft)

    def setCallback(self, callback):
        self.connect(self, QtCore.SIGNAL('clicked()'), callback)