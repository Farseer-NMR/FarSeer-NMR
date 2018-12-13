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
import sys
import os
import argparse
from gui import gui_utils

from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QApplication, QSplashScreen, QVBoxLayout, QWidget

from gui.components.TabWidget import TabWidget
from gui.Footer import Footer
from gui import resources_rc

from core.fslibs.Variables import Variables


class Main(QWidget):

    def __init__(self, parent=None, gui_settings=None, config=None, **kw):
        QWidget.__init__(self, parent=parent)
        default_config = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'core',
            'default_config.json'
            )
        #
        if config:
            Variables().read(config)
        else:
            Variables().read(default_config)
        #
        tabWidget = TabWidget(gui_settings)
        footer = Footer(self, gui_settings=gui_settings)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        self.layout().addWidget(tabWidget)
        self.layout().addWidget(footer)
        self.setObjectName("MainWidget")
    
def run(argv):
    app = QApplication(argv)
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Farseer')
    parser.add_argument(
        '--config',
        metavar='path',
        required=False,
        help='Farseer Configuration File'
        )
    splash_file = os.path.join(os.pardir, 'gui', 'images', 'splash-screen.png')
    splash_pix = QtGui.QPixmap(splash_file)
    args = parser.parse_args()
    splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(False)
    splash.show()
    screen_resolution = app.desktop().screenGeometry()
    
    gui_settings, stylesheet = gui_utils.deliver_settings(screen_resolution)
    
    ex = Main(gui_settings=gui_settings, config=args.config)
    splash.finish(ex)
    font_file = os.path.join(os.pardir, 'gui', 'SinkinSans', 'SinkinSans-400Regular.otf')
    font_id = QtGui.QFontDatabase.addApplicationFont(font_file)
    app.setStyleSheet(stylesheet)
    ex.show()
    ex.raise_()
    execution = app.exec_()

    del ex
    del app

    sys.exit(execution)
    return

if __name__ == '__main__':
    
    run(sys.argv)
