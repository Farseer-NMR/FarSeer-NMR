

from PyQt5.QtWidgets import QWidget

from gui.components.TabFooter import TabFooter
from core.fslibs.Variables import Variables



class BaseWidget(QWidget):

    variables = Variables()._vars

    def __init__(self, parent=None, gui_settings=None, footer=True):
        QWidget.__init__(self, parent=parent)

        self.gui_settings = gui_settings

        if footer:
            self.tab_footer = TabFooter(self)
            self.tab_footer.load_config_button.clicked.connect(parent.load_config)
            self.tab_footer.save_config_button.clicked.connect(parent.save_config)
            self.tab_footer.run_farseer_button.clicked.connect(parent.run_farseer_calculation)



