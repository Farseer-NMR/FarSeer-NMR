import sys
import json
import os

from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QApplication, QSplashScreen, QVBoxLayout, QWidget

from gui.components.TabWidget import TabWidget
from gui.Footer import Footer

from gui import resources_rc


class Main(QWidget):

    def __init__(self, parent=None, gui_settings=None, config=None, **kw):

        QWidget.__init__(self, parent=parent)

        variables = json.load(
            open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'current', 'default_config.json'), 'r'))

        tabWidget = TabWidget(gui_settings, variables)

        footer = Footer(self, gui_settings=gui_settings)


        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        self.layout().addWidget(tabWidget)
        self.layout().addWidget(footer)

        self.setObjectName("MainWidget")
        if config:
            tabWidget.load_config(config)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    import argparse

    parser = argparse.ArgumentParser(description='Run Farseer')
    parser.add_argument('--config', metavar='path', required=False,
                        help='Farseer Configuration File')
    splash_pix = QtGui.QPixmap('gui/images/splash-screen.png')

    args = parser.parse_args()

    splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(False)

    splash.show()

    screen_resolution = app.desktop().screenGeometry()

    from gui import gui_utils
    gui_settings, stylesheet = gui_utils.deliver_settings(screen_resolution)

    ex = Main(gui_settings=gui_settings, config=args.config)
    splash.finish(ex)
    fin = 'gui/SinkinSans/SinkinSans-400Regular.otf'
    font_id = QtGui.QFontDatabase.addApplicationFont(fin)

    app.setStyleSheet(stylesheet)

    ex.show()
    ex.raise_()
    sys.exit(app.exec_())
