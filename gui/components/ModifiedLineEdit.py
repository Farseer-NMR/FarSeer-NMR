"""
Code taken from Stack Overflow
https://stackoverflow.com/questions/12182133/pyqt4-combine-textchanged-and-editingfinished-for-qlineedit/12182671

Authors
Katya: https://stackoverflow.com/users/1035567/katya
ekhumoro: https://stackoverflow.com/users/984421/ekhumoro
Avaris: https://stackoverflow.com/users/843822/avaris

"""

from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore

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