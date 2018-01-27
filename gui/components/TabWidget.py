import sys
import json
import os

from PyQt5 import QtCore, QtGui

from current.setup_farseer_calculation import create_directory_structure

from PyQt5.QtWidgets import QFileDialog, QGridLayout, QLabel, \
     QMessageBox, QTabWidget, QWidget

from gui.components.Icon import ICON_DIR


from gui.tabs.peaklist_selection import PeaklistSelection
from gui.tabs.paraset import Paraset
from gui.tabs.settings import Settings

from current.fslibs.Variables import Variables



class TabWidget(QTabWidget):

    variables = Variables()._vars

    def __init__(self, gui_settings):
        QTabWidget.__init__(self, parent=None)

        self.widgets = []
        self.gui_settings = gui_settings
        self.add_tab_logo()
        self.add_tabs_to_widget()


    def add_tabs_to_widget(self):
        self.peaklist_selection = PeaklistSelection(self, gui_settings=self.gui_settings, footer=False)
        self.settings = Settings(self, gui_settings=self.gui_settings, footer=True)

        self.add_tab(self.peaklist_selection, "PeakList Selection")
        self.add_tab(self.settings, "Settings", "Settings")

        self.widgets.extend([self.peaklist_selection, self.settings])


    def set_data_sets(self):
        for widget in self.widgets:
            if hasattr(widget, 'set_data_sets'):
                widget.set_data_sets()

    def add_tab(self, widget, name, object_name=None):
        tab = QWidget()
        tab.setLayout(QGridLayout())
        tab.layout().addWidget(widget)
        self.addTab(tab, name)
        if object_name:
            tab.setObjectName(object_name)


    def load_config(self, path=None):
        if not path:
            fname = QFileDialog.getOpenFileName(None, 'Load Configuration', os.getcwd())
        else:
            fname = [path]
        if fname[0]:
            if fname[0].split('.')[1] == 'json':
                # variables = json.load(open(fname[0], 'r'))
                # self.settings.spectrum_path.field.setText('')
                # self.variables = variables
                Variables().read(fname[0])
        return

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

    def save_config(self, path=None):
        if not path:
            filters = "JSON files (*.json)"
            selected_filter = "JSON files (*.json)"
            fname = QFileDialog.getSaveFileName(self, " Save Configuration ", "", filters,
                                                  selected_filter)

        else:
            fname = [path]
        if not fname[0].endswith('.json'):
            fname = [fname[0] +".json"]
        if fname[0]:
            with open(fname[0], 'w') as outfile:
                Variables().write(outfile)

        print('Configuration saved to %s' % fname[0])

    def run_farseer_calculation(self):
        from current.Threading import Threading
        output_path = self.settings.output_path.field.text()
        run_msg = create_directory_structure(output_path, self.variables)

        if run_msg == 'Run':
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
                msg.setInformativeText(
                    "Spectrum folder already exists in Calculation Output Path. Calculation cannot be launched.")
            elif run_msg == "No dataset":
                msg.setText("No dataset")
                msg.setInformativeText(
                    "No Experimental dataset has been created. Please populate Experimental Dataset Tree.")
            msg.exec_()

    def add_tab_logo(self):

        self.tablogo = QLabel(self)
        self.tablogo.setAutoFillBackground(True)
        self.tablogo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        pixmap = QtGui.QPixmap(os.path.join(ICON_DIR, 'icons/header-logo.png'))
        self.tablogo.setPixmap(pixmap)
        self.tablogo.setContentsMargins(9, 0, 0, 6)
        self.setCornerWidget(self.tablogo, corner=QtCore.Qt.TopLeftCorner)
        self.setFixedSize(QtCore.QSize(self.gui_settings['app_width'], self.gui_settings['app_height']))


