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
"""
from PyQt5.QtWidgets import QWidget

from gui.components.TabFooter import TabFooter
from current.fslibs.Variables import Variables



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



