import sys
import json
import os

from PyQt5 import QtCore, QtGui

from current.setup_farseer_calculation import create_directory_structure

from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QLabel, \
     QMessageBox, QSplashScreen, QTabWidget, QVBoxLayout, QWidget

from gui.components.Icon import ICON_DIR


from gui.Footer import Footer

from gui import resources_rc

from gui.tabs.peaklist_selection import Interface
from gui.tabs.settings import Settings


class TabWidget(QTabWidget):

    def __init__(self, gui_settings):
        QTabWidget.__init__(self, parent=None)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab1.setLayout(QGridLayout())
        self.tab2.setLayout(QGridLayout())
        variables = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'current', 'default_config.json'), 'r'))
        self.variables = variables
        self.interface = Interface(gui_settings=gui_settings, variables=variables)
        self.settings = Settings(gui_settings=gui_settings, variables=variables)
        self.tab1.layout().addWidget(self.settings)
        self.tab2.layout().addWidget(self.interface)
        self.addTab(self.tab2, "PeakList Selection")
        self.addTab(self.tab1, "Settings")
        self.tab1.setObjectName("Settings")
        self.tablogo = QLabel(self)
        self.tablogo.setAutoFillBackground(True)
        self.tablogo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        pixmap = QtGui.QPixmap(os.path.join(ICON_DIR, 'icons/header-logo.png'))
        self.tablogo.setPixmap(pixmap)
        self.tablogo.setContentsMargins(9, 0, 0, 6)
        self.setCornerWidget(self.tablogo, corner=QtCore.Qt.TopLeftCorner)
        self.setFixedSize(QtCore.QSize(gui_settings['app_width'], gui_settings['app_height']))
        self.config_file = None

    def load_config(self, path=None):
        if not path:
            fname = QFileDialog.getOpenFileName(None, 'Load Configuration', os.getcwd())
        else:
            fname = [path]
        if fname[0]:
            if fname[0].split('.')[1] == 'json':
                variables = json.load(open(fname[0], 'r'))
                self.settings.spectrum_path.field.setText('')
                self.variables = variables
                self.load_variables(variables)
                print(self.variables["peaklists"], "peaklists")
                return variables
        return None


    def load_variables(self, variables):

        self.settings.load_variables(variables)
        self.settings.variables = variables
        self.interface.load_variables(variables)
        self.interface.sideBar.update_from_config(variables)


    def load_peak_lists(self, path=None):
        print('load')
        if os.path.exists(path):
            self.interface.sideBar.load_from_path(path)
            self.interface.sideBar.update_from_config(self.variables)

    def save_config(self, variables, path=None):
        print(variables["peaklists"], 'saving')
        if not path:
            fname = QFileDialog.getSaveFileName(self, 'Save Configuration' '', "*.json")
        else:
            fname = [path]
        if fname[0]:
            with open(fname[0], 'w') as outfile:
                if fname[0].endswith('.json'):
                    print(self.interface.sideBar.peakLists)
                    if not variables["peaklists"]:
                        variables["peaklists"] = self.interface.sideBar.peakLists
                    
                    json.dump(variables, outfile, indent=4)
                    self.config_file = fname[0]
                print('Configuration saved to %s' % fname[0])


    def run_farseer_calculation(self):
        from current.Threading import Threading
        output_path = self.settings.output_path.field.text()
        run_msg = create_directory_structure(output_path, self.variables)


        if run_msg =='Run':
            from current.farseermain import read_user_variables, run_farseer
            if self.config_file:
                path, config_name = os.path.split(self.config_file)
                fsuv = read_user_variables(path, config_name)
            else:
                self.settings.save_config(path=os.path.join(output_path, 'user_config.json'))
                fsuv = read_user_variables(output_path, 'user_config.json')

            process = Threading(function=run_farseer, args=fsuv)

        else:
            msg = QMessageBox()
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Warning)
            if run_msg == "Path Exists":
                msg.setText("Output Path Exists")
                msg.setInformativeText("Spectrum folder already exists in Calculation Output Path. Calculation cannot be launched.")
            elif run_msg == "No dataset":
                msg.setText("No dataset")
                msg.setInformativeText("No Experimental dataset has been created. Please populate Experimental Dataset Tree.")
            msg.exec_()





class Main(QWidget):

    def __init__(self, parent=None, gui_settings=None, config=None, **kw):
        QWidget.__init__(self, parent=parent)
        tabWidget = TabWidget(gui_settings)

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
