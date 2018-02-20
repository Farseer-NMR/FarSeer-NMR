"""
Copyright © 2017-2018 Farseer-NMR
Simon P. Skinner and João M.C. Teixeira

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

Farseer-NMR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Farseer-NMR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.

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
    """
    A subclass of QLineEdit which combines the textChanged and editingFinished
    signals into a textModified signal.

    Parameters:
        parent (QWidget): specifies the parent widget containing the QLabel
            and the QSpinBox.
        contents (str): text to be present in the LineEdit on instantiation.

    Methods:
        .focusInEvent(QEvent)
        .focusInEvent(QEvent)
        .checkText()
        """
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
