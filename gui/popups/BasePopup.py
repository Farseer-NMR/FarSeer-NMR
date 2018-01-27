from PyQt5.QtWidgets import QDialog, QGridLayout, QVBoxLayout
from PyQt5 import QtCore
from current.fslibs.Variables import Variables
from gui.gui_utils import defaults
from current.utils import get_nested_value

class BasePopup(QDialog):

    variables = Variables()._vars

    def __init__(self, parent, settings_key=None, title=None, layout='grid', **kw):
        QDialog.__init__(self, parent)

        self.setWindowTitle(title)
        if layout == 'grid':
            grid = QGridLayout()
            grid.setAlignment(QtCore.Qt.AlignTop)
            self.setLayout(grid)

        if layout == 'vbox':
            v_layout = QVBoxLayout()
            v_layout.setAlignment(QtCore.Qt.AlignTop)
            self.setLayout(v_layout)
        self.defaults = defaults
        if settings_key:
            if isinstance(settings_key, str):
                self.local_variables = self.variables[settings_key]
            elif isinstance(settings_key, list):
                self.local_variables = get_nested_value(self.variables,
                                                        settings_key)


    def launch(self):
        self.exec_()
        self.raise_()