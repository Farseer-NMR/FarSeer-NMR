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
import os
import datetime

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QLabel,
    QMessageBox,
    QTabWidget,
    QWidget
    )

from core.setup_farseer_calculation import create_directory_structure, check_input_construction
from core.fslibs.Variables import Variables
from gui.components.Icon import ICON_DIR
from gui.tabs.peaklist_selection import PeaklistSelection
from gui.tabs.settings import Settings


class TabWidget(QTabWidget):
    """
    The container for all tab widgets in the Farseer-NMR GUI.

    To add a new tab to the tab widget, the QWidget class of the needs to be
    imported into this file. The instantiation of the class and the addition
    of the QWidget to the TabWidget need to be coded in the add_tabs_to_widget
    method.

    Parameters:
        gui_settings (dict): a dictionary carrying the settings required to
            correctly render the graphics based on screen resolution.

    Methods:
        .add_tabs_to_widget()
        .set_data_sets()
        .add_tab(QWidget, str, str)
        .load_config(str)
        .load_variables()
        .load_peak_lists(str)
        .save_config(str)
        .run_farseer_calculation
    """
    variables = Variables()._vars
    
    def __init__(self, gui_settings):
        QTabWidget.__init__(self, parent=None)
        
        self.widgets = []
        self.gui_settings = gui_settings
        self._add_tab_logo()
        self.add_tabs_to_widget()

    def add_tabs_to_widget(self):
        """
        Create instances of all widget classes and add them to the TabWidget
        """
        self.peaklist_selection = \
            PeaklistSelection(self, gui_settings=self.gui_settings, footer=False)
        self.interface = Settings(self, gui_settings=self.gui_settings, footer=True)
        self.add_tab(self.peaklist_selection, "PeakList Selection")
        self.add_tab(self.interface, "Settings", "Settings")
        self.widgets.extend([self.peaklist_selection, self.interface])

    def set_data_sets(self):
        """Set data in the tabs if they have data_sets as an attribute"""
        for widget in self.widgets:
            if hasattr(widget, 'set_data_sets'):
                widget.set_data_sets()

    def add_tab(self, widget, name, object_name=None):
        """Re-implemented of the addTab method to ensure proper compatibility
        with the stylesheet and architecture.
        """
        tab = QWidget()
        tab.setLayout(QGridLayout())
        tab.layout().addWidget(widget)
        self.addTab(tab, name)
        
        if object_name:
            tab.setObjectName(object_name)

    def load_config(self, path=None):
        """
        Connection from Tab footer to TabWidget for loading Farseer-NMR
        configuration files.
        """
        if not path:
            fname = QFileDialog.getOpenFileName(None, 'Load Configuration', os.getcwd())
        
        else:
            fname = [path]
        
        if fname[0]:
            if fname[0].split('.')[1] == 'json':
                Variables().read(fname[0])
                self.load_variables()
                self.config_file = fname[0]
        
        return

    def load_variables(self):
        """Load variables into self.variables instance."""
        self.interface.load_variables()
        self.peaklist_selection.load_variables()
        self.peaklist_selection.side_bar.update_from_config()

    def load_peak_lists(self, path=None):
        """Load peaklists into sidebar. Called from self.load_variables."""
        if os.path.exists(path):
            self.peaklist_selection.side_bar.load_from_path(path)

    def save_config(self, path=None):
        """
        Connection from Tab footer to TabWidget for saving Farseer-NMR
        configuration files.
        """
        self.interface.save_config()
        
        if not path:
            filters = "JSON files (*.json)"
            selected_filter = "JSON files (*.json)"
            fname = QFileDialog.getSaveFileName(
                self,
                "Save Configuration",
                "",
                filters,
                selected_filter
                )
        else:
            fname = [path]
        
        if not fname[0].endswith('.json'):
            fname = [fname[0] + ".json"]
        
        if fname[0]:
            with open(fname[0], 'w') as outfile:
                Variables().write(outfile)
                self.config_file = os.path.abspath(fname[0])
        
        print('Configuration saved to {}'.format(fname[0]))

    def run_farseer_calculation(self):
        """
        Executes Farseer-NMR calculation in its own thread.
        Saves configuration if not already saved.
        Performs necessary checks for execution.
        """
        
        msg = QMessageBox()
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setIcon(QMessageBox.Warning)
        
        if not all(x for x in self.variables["conditions"].values()):
            msg.setText('Experimental Series not set up correctly.')
            msg.setInformativeText(
"""Please ensure that all conditions in the
Peaklist Tree have labels and that all
X axis conditions have a peaklist associated."""
                )
            msg.exec_()
            return
        
        from core.Threading import Threading
        output_path = self.variables["general_settings"]["output_path"]
        run_msg = check_input_construction(output_path, self.variables)
        print(run_msg)
        
        if run_msg in ["Spectra", "Backbone", "Sidechains"]:
            msg.setText("{} Path Exists.".format(run_msg))
            msg.setInformativeText(
"""{} folder already exists in Calculation Output Path.
Calculation cannot be launched.""".format(run_msg)
                )
            msg.exec_()
        
        elif run_msg == "No dataset":
            msg.setText("No dataset configured.")
            msg.setInformativeText(
                "No Experimental dataset has been created. "
                "Please define an Experimental Dataset Tree and populate it \
with the corresponding peaklist files.")
            msg.exec_()
        
        elif run_msg == "FASTA file not provided":
            msg.setText("FASTA file not provided.")
            msg.setInformativeText(
"""The Apply FASTA box is activated.
This calculation requires FASTA files to be
specified for each Y axis condition."""
                )
            msg.exec_()
        
        elif run_msg == "No FASTA for peaklist":
            msg.setText("No FASTA for NmrDraw/NmrView peaklists")
            msg.setInformativeText(
"""You have input NmrView/NmrDraw peaklists.
These require a FASTA file to be specified.
Plase do so in FASTA menu.
Refer to WET#26 for more details.
"""
                )
            msg.exec_()
        
        elif run_msg == "No populated Tree":
            msg.setText("Tree not completely populated.")
            msg.setInformativeText(
                "There are branches in the Experimental Tree which are \
not populated. Please ensure that all branches have a peaklist assigned."
                )
            msg.exec_()
        
        elif run_msg == "Para name not set":
            msg.setText("You have activated Do PRE Analysis")
            msg.setInformativeText(
"""When analysing paramagnetic data, the datapoint names
of the Z axis must be exactly "dia" and "para"
for diamagnetic and paramagnetic datasets, respectively.

We appologise but other words are not accepted.
Please correct the Z names accordingly.
"""
                )
            msg.exec_()
        
        elif run_msg == "PRE file not provided":
            msg.setText("PRE file not provided.")
            msg.setInformativeText(
"""The PRE Analysis box is activated.
This calculation requires Theoretical PRE files
to be specified for each Y axis condition.""")
            msg.exec_()
        
        elif run_msg == "Run":
            create_directory_structure(output_path, self.variables)
            from core.farseermain import read_user_variables, run_farseer
            run_config_name = "user_config_{}.json".format(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                )
            config_path = os.path.join(output_path, run_config_name)
            self.save_config(path=config_path)
            fsuv = read_user_variables(output_path, config_path)
            Threading(function=run_farseer, args=fsuv)
        
        else:
            print('Run could not be initiated')

    def _add_tab_logo(self):
        """Add logo to tab header."""
        self.tablogo = QLabel(self)
        self.tablogo.setAutoFillBackground(True)
        self.tablogo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        pixmap = QtGui.QPixmap(os.path.join(ICON_DIR, 'icons/header-logo.png'))
        self.tablogo.setPixmap(pixmap)
        self.tablogo.setContentsMargins(9, 0, 0, 6)
        self.setCornerWidget(self.tablogo, corner=QtCore.Qt.TopLeftCorner)
        self.setFixedSize(QtCore.QSize(
            self.gui_settings['app_width'],
            self.gui_settings['app_height']
                ))
