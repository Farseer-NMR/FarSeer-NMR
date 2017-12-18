

from PyQt5.QtWidgets import QWidget

from gui.components.TabFooter import TabFooter



class BaseWidget(QWidget):

    def __init__(self, parent=None, gui_settings=None, variables=None, footer=True):
        QWidget.__init__(self, parent=parent)

        if variables:
            self.variables = variables
        self.gui_settings = gui_settings

        if footer:
            self.tab_footer = TabFooter(self)

