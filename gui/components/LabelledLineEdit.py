from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout
from PyQt5 import QtCore

class LabelledLineEdit(QWidget):

    def __init__(self, parent, text, callback=None):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = ModifiedLineEdit(self)

        self.layout().addWidget(label)
        self.layout().addWidget(self.field)

        if callback:
            self.set_callback(callback)

    def set_callback(self, callback):
        self.field.textModified.connect(callback)

    def setText(self, text):
        self.field.setText(text)

class ModifiedLineEdit(QLineEdit):
    textModified = QtCore.pyqtSignal(str, str)

    def __init__(self, parent, contents=None):
        super(ModifiedLineEdit, self).__init__(contents, parent)
        self.returnPressed.connect(self.checkText)
        self._before = contents

    def focusInEvent(self, event):
        if event.reason() != QtCore.Qt.PopupFocusReason:
            self._before = self.text()
        super(ModifiedLineEdit, self).focusInEvent(event)

    def focusOutEvent(self, event):
        if event.reason() != QtCore.Qt.PopupFocusReason:
            self.checkText()
        super(ModifiedLineEdit, self).focusOutEvent(event)

    def checkText(self):
        if self._before != self.text():
            self._before = self.text()
            self.textModified.emit(self._before, self.text())