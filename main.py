import sys
from functools import partial
import json
import os
from collections import OrderedDict

from PyQt5 import QtCore, QtGui

from current.setup_farseer_calculation import create_directory_structure

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QLabel, QGroupBox, QGridLayout, \
    QSpinBox, QPushButton, QTabWidget, QHBoxLayout, QSplitter, QCheckBox, QSizePolicy, QSplashScreen, QSpacerItem, QMessageBox

from gui.components.PeakListArea import PeakListArea
from gui.components.Sidebar import SideBar
from gui.components.ValuesField import ValueField

from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.Icon import Icon, ICON_DIR

from gui.popups.BarPlotPopup import BarPlotPopup
from gui.popups.ExtendedBarPopup import ExtendedBarPopup
from gui.popups.CompactBarPopup import CompactBarPopup
from gui.popups.CSPExceptionsPopup import CSPExceptionsPopup
from gui.popups.FastaSelectionPopup import FastaSelectionPopup
from gui.popups.GeneralResidueEvolution import GeneralResidueEvolution
from gui.popups.HeatMapPopup import HeatMapPopup
from gui.popups.OscillationMapPopup import OscillationMapPopup
from gui.popups.PreAnalysisPopup import PreAnalysisPopup
from gui.popups.ResidueEvolution import ResidueEvolutionPopup
from gui.popups.ScatterFlowerPlotPopup import ScatterFlowerPlotPopup
from gui.popups.ScatterPlotPopup import ScatterPlotPopup
from gui.popups.SeriesPlotPopup import SeriesPlotPopup
from gui.popups.VerticalBar import VerticalBarPopup

from gui.Footer import Footer

from gui import resources_rc


from current.fslibs.io import json_to_fsuv, fsuv_to_json

peakLists = OrderedDict()

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
                return variables
        return None


    def load_variables(self, variables):

        self.settings.load_variables(variables)
        self.settings.variables = variables
        self.interface.load_variables(variables)
        self.interface.sideBar.update_from_config(variables)


    def load_peak_lists(self, path=None):
        if os.path.exists(path):
            self.interface.sideBar.load_from_path(path)
            self.interface.sideBar.update_from_config(self.variables)

    def save_config(self, variables, path=None):

        if not path:
            fname = QFileDialog.getSaveFileName(self, 'Save Configuration' '', "*.json")
        else:
            fname = [path]
        if fname[0]:
            with open(fname[0], 'w') as outfile:
                if fname[0].endswith('.json'):
                    #self.variables["peaklists"] = self.interface.sideBar.peakLists
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


            # os.spawnl(os.P_DETACH, run_farseer(fsuv))

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

class Settings(QWidget):
    def __init__(self, parent=None, gui_settings=None, variables=None):
        QWidget.__init__(self, parent=parent)
        grid = QGridLayout()
        grid2 = QGridLayout()
        self.setLayout(grid2)
        self.gui_settings = gui_settings
        newWidget = QWidget(self)
        newWidget.setObjectName("SettingsWidget")
        newWidget.setLayout(grid)
        self.layout().addWidget(newWidget)

        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.variables = variables
        paths_group_box = QGroupBox()
        paths_groupbox_layout = QGridLayout()
        paths_groupbox_layout.setSpacing(2)
        paths_group_box.setLayout(paths_groupbox_layout)

        self.spectrum_path = LabelledLineEdit(self, "Spectrum Path", callback=self.set_spectrum_path_text)
        self.output_path = LabelledLineEdit(self, "Calculation Output Folder", callback=self.set_output_path)

        self.spectrum_path_browse = QPushButton("...", self)
        self.output_path_browse = QPushButton("...", self)

        self.spectrum_path_browse.clicked.connect(self.set_spectrum_path)
        self.output_path_browse.clicked.connect(self.set_output_path)

        paths_group_box.layout().addWidget(self.spectrum_path, 0, 0, 1, 12)
        paths_group_box.layout().addWidget(self.output_path, 1, 0, 1, 12)
        paths_group_box.layout().addWidget(self.spectrum_path_browse, 0, 13, 1, 1)
        paths_group_box.layout().addWidget(self.output_path_browse, 1, 13, 1, 1)

        self.ext_bar_checkbox = LabelledCheckbox(self, "Extended Bar")
        self.comp_bar_checkbox = LabelledCheckbox(self, "Compact Bar")
        self.vert_bar_checkbox = LabelledCheckbox(self, "Vertical Bar")
        self.res_evo_checkbox = LabelledCheckbox(self, "Residue Evolution")
        self.scatter_checkbox = LabelledCheckbox(self, "CS Scatter")
        self.dpre_checkbox = LabelledCheckbox(self, "Oscillation Map")
        self.heat_map_checkbox = LabelledCheckbox(self, "Heat Map")
        self.scatter_flower_checkbox = LabelledCheckbox(self, " CS Scatter Flower")

        self.tplot_button = QPushButton("General Series Plot Settings", self)
        self.tplot_button.clicked.connect(partial(self.show_popup, SeriesPlotPopup, self.variables))

        self.revo_button = QPushButton("General Evolution Settings", self)
        self.revo_button.clicked.connect(partial(self.show_popup, GeneralResidueEvolution, self.variables))

        self.bar_button = QPushButton("Bar Plot Settings", self)
        self.bar_button.clicked.connect(partial(self.show_popup, BarPlotPopup, self.variables))

        self.ext_bar_button = QPushButton("Settings", self)
        self.ext_bar_button.clicked.connect(partial(self.show_popup, ExtendedBarPopup, self.variables))

        self.comp_bar_button = QPushButton("Settings", self)
        self.comp_bar_button.clicked.connect(partial(self.show_popup, CompactBarPopup, self.variables))

        self.vert_bar_button = QPushButton("Settings", self)
        self.vert_bar_button.clicked.connect(partial(self.show_popup, VerticalBarPopup, self.variables))

        self.res_evo_button = QPushButton("Settings", self)
        self.res_evo_button.clicked.connect(partial(self.show_popup, ResidueEvolutionPopup, self.variables))

        self.scatter_button = QPushButton("Settings", self)
        self.scatter_button.clicked.connect(partial(self.show_popup, ScatterPlotPopup, self.variables))

        self.scatter_flower_button = QPushButton("Settings", self)
        self.scatter_flower_button.clicked.connect(partial(self.show_popup, ScatterFlowerPlotPopup, self.variables))

        self.heat_map_button = QPushButton("Settings", self)
        self.heat_map_button.clicked.connect(partial(self.show_popup, HeatMapPopup, self.variables))

        self.dpre_button = QPushButton("Settings", self)
        self.dpre_button.clicked.connect(partial(self.show_popup, OscillationMapPopup, self.variables))

        self.fasta_button = QPushButton("Select FASTA Files", self)
        self.fasta_button.clicked.connect(partial(self.show_popup, FastaSelectionPopup, self.variables))

        self.has_sidechains_checkbox = LabelledCheckbox(self, "Are Sidechain Peaks Present?")
        self.use_sidechains_checkbox = LabelledCheckbox(self, "Analyse Sidechains?")
        self.perform_comparisons_checkbox = LabelledCheckbox(self, "Perform Comparisons?")
        self.apply_fasta_checkbox = LabelledCheckbox(self, "Apply FASTA?")
        self.fasta_start = LabelledSpinBox(self, "Fasta start")

        self.expand_lost_yy = LabelledCheckbox(self, "Analyse Lost Y Residues?")
        self.expand_lost_zz = LabelledCheckbox(self, "Analyse Lost Z Residues?")

        self.figure_width = LabelledDoubleSpinBox(self, "Figure Width", min=0, max=100, step=1)
        self.figure_height = LabelledDoubleSpinBox(self, "Figure Height", min=0, max=100, step=1)
        self.figure_dpi = LabelledDoubleSpinBox(self, "Figure DPI", min=0, max=10000, step=10)
        self.figure_format = LabelledCombobox(self, "Figure Format", items=['pdf', 'png', 'ps', 'svg'])

        sidechains_groupbox = QGroupBox()
        sidechains_groupbox.setTitle("Sidechains")
        sidechains_groupbox_layout = QVBoxLayout()
        sidechains_groupbox.setLayout(sidechains_groupbox_layout)
        sidechains_groupbox.layout().addWidget(self.has_sidechains_checkbox)
        sidechains_groupbox.layout().addWidget(self.use_sidechains_checkbox)


        fasta_groupbox = QGroupBox()
        fasta_groupbox.setTitle("FASTA")
        fasta_groupbox_layout = QGridLayout()
        fasta_groupbox.setLayout(fasta_groupbox_layout)
        fasta_groupbox.layout().addWidget(self.apply_fasta_checkbox, 0, 0)
        fasta_groupbox.layout().addWidget(self.fasta_start, 0, 1)
        fasta_groupbox.layout().addWidget(self.fasta_button, 1, 0, 1, 2)



        self.x_checkbox = LabelledCheckbox(self, "x")
        self.y_checkbox = LabelledCheckbox(self, "y")
        self.z_checkbox = LabelledCheckbox(self, "z")


        series_groupbox = QGroupBox()
        series_groupbox.setTitle("Experimental Series Analysis")
        series_groupbox_layout = QVBoxLayout()
        series_groupbox.setLayout(series_groupbox_layout)
        series_groupbox.layout().addWidget(self.x_checkbox)
        series_groupbox.layout().addWidget(self.y_checkbox)
        series_groupbox.layout().addWidget(self.z_checkbox)
        series_groupbox.layout().addWidget(self.perform_comparisons_checkbox)


        figure_groupbox = QGroupBox()
        figure_groupbox.setTitle("Figure")
        figure_groupbox_layout = QVBoxLayout()
        figure_groupbox.setLayout(figure_groupbox_layout)
        figure_groupbox.layout().addWidget(self.figure_width)
        figure_groupbox.layout().addWidget(self.figure_height)
        figure_groupbox.layout().addWidget(self.figure_dpi)
        figure_groupbox.layout().addWidget(self.figure_format)

        self.cs_correction = LabelledCheckbox(self, "CS Correction?")
        self.cs_correction_res_ref = LabelledSpinBox(self, text="Correction Residue")

        cs_norm_groupbox = QGroupBox()
        cs_norm_groupbox.setTitle("Chemical Shift Normalisation")
        cs_groupbox_layout = QVBoxLayout()
        cs_norm_groupbox.setLayout(cs_groupbox_layout)
        cs_norm_groupbox.layout().addWidget(self.cs_correction)
        cs_norm_groupbox.layout().addWidget(self.cs_correction_res_ref)

        lost_analysis_groupbox = QGroupBox()
        lost_analysis_groupbox_layout = QVBoxLayout()
        lost_analysis_groupbox.setLayout(lost_analysis_groupbox_layout)
        lost_analysis_groupbox.layout().addWidget(self.expand_lost_yy)
        lost_analysis_groupbox.layout().addWidget(self.expand_lost_zz)


        cs_groupbox = QGroupBox()
        cs_groupbox.setTitle("CSP Specific")
        cs_groupbox_layout = QVBoxLayout()
        cs_groupbox.setLayout(cs_groupbox_layout)

        self.csp_alpha = LabelledDoubleSpinBox(self, text="CSP Alpha", min=0, max=1, step=0.01)
        self.csp_lost = LabelledCombobox(self, text="Show Lost Residues", items=['prev', 'full', 'zero'])
        self.csp_exceptions = QPushButton("Alpha by residue", self)
        self.csp_exceptions.clicked.connect(partial(self.show_popup, CSPExceptionsPopup, self.variables))
        cs_groupbox.layout().addWidget(self.csp_alpha)
        cs_groupbox.layout().addWidget(self.csp_lost)
        cs_groupbox.layout().addWidget(self.csp_exceptions)



        restraint_groupbox = QGroupBox()
        restraint_groupbox.setTitle("Restraint Calculation")
        restraint_groupbox_layout = QGridLayout()
        restraint_groupbox.setLayout(restraint_groupbox_layout)

        self.plot_F1_data = LabelledCheckbox(self, text="F1 data")
        self.plot_F2_data = LabelledCheckbox(self, text="F2 data")
        self.plot_CSP = LabelledCheckbox(self, text="CSPs")
        self.plot_height_ratio = LabelledCheckbox(self, text="Height Ratio", callback=self.activate_pre_analysis)
        self.plot_volume_ratio = LabelledCheckbox(self, text="Volume Ratio", callback=self.activate_pre_analysis)

        self.plot_F1_y_label = LabelledLineEdit(self, text='')
        self.plot_F2_y_label = LabelledLineEdit(self, text='')
        self.plot_CSP_y_label = LabelledLineEdit(self, text='')
        self.plot_height_y_label = LabelledLineEdit(self, text='')
        self.plot_volume_y_label = LabelledLineEdit(self, text='')

        self.plot_F1_calccol = LabelledLineEdit(self, text="")
        self.plot_F2_calccol = LabelledLineEdit(self, text="")
        self.plot_CSP_calccol = LabelledLineEdit(self, text="")
        self.plot_height_calccol = LabelledLineEdit(self, text="")
        self.plot_volume_calccol = LabelledLineEdit(self, text="")

        self.plot_F1_y_scale = LabelledDoubleSpinBox(self, text="", min=0, step=.1)
        self.plot_F2_y_scale = LabelledDoubleSpinBox(self, text="", min=0, step=.1)
        self.plot_CSP_y_scale = LabelledDoubleSpinBox(self, text="", min=0, step=.1)
        self.plot_height_y_scale = LabelledDoubleSpinBox(self, text="", min=0, step=.1)
        self.plot_volume_y_scale = LabelledDoubleSpinBox(self, text="", min=0, step=.1)

        restraint_label = QLabel("Restraint Name")
        axis_label = QLabel("Y Axis Label")
        scale_label = QLabel("Y Axis Scale")

        restraint_label.setAlignment(QtCore.Qt.AlignHCenter)
        axis_label.setAlignment(QtCore.Qt.AlignHCenter)
        scale_label.setAlignment(QtCore.Qt.AlignHCenter)


        restraint_groupbox.layout().addWidget(restraint_label, 0, 1)
        restraint_groupbox.layout().addWidget(axis_label, 0, 2)
        restraint_groupbox.layout().addWidget(scale_label, 0, 3)

        restraint_groupbox.layout().addWidget(self.plot_F1_data, 1, 0)
        restraint_groupbox.layout().addWidget(self.plot_F2_data, 2, 0)
        restraint_groupbox.layout().addWidget(self.plot_CSP, 3, 0)
        restraint_groupbox.layout().addWidget(self.plot_height_ratio, 4, 0)
        restraint_groupbox.layout().addWidget(self.plot_volume_ratio, 5, 0)


        restraint_groupbox.layout().addWidget(self.plot_F1_y_label, 1, 1)
        restraint_groupbox.layout().addWidget(self.plot_F2_y_label, 2, 1)
        restraint_groupbox.layout().addWidget(self.plot_CSP_y_label, 3, 1)
        restraint_groupbox.layout().addWidget(self.plot_height_y_label, 4, 1)
        restraint_groupbox.layout().addWidget(self.plot_volume_y_label, 5, 1)


        restraint_groupbox.layout().addWidget(self.plot_F1_calccol, 1, 2)
        restraint_groupbox.layout().addWidget(self.plot_F2_calccol, 2, 2)
        restraint_groupbox.layout().addWidget(self.plot_CSP_calccol, 3, 2)
        restraint_groupbox.layout().addWidget(self.plot_height_calccol, 4, 2)
        restraint_groupbox.layout().addWidget(self.plot_volume_calccol, 5, 2)


        restraint_groupbox.layout().addWidget(self.plot_F1_y_scale, 1, 3)
        restraint_groupbox.layout().addWidget(self.plot_F2_y_scale, 2, 3)
        restraint_groupbox.layout().addWidget(self.plot_CSP_y_scale, 3, 3)
        restraint_groupbox.layout().addWidget(self.plot_height_y_scale, 4, 3)
        restraint_groupbox.layout().addWidget(self.plot_volume_y_scale, 5, 3)


        pre_groupbox = QGroupBox()
        pre_groupbox.setTitle("PRE")
        pre_groupbox_layout = QGridLayout()
        pre_groupbox.setLayout(pre_groupbox_layout)

        self.do_pre_checkbox = LabelledCheckbox(self, "Do PRE Analysis")
        self.do_pre_checkbox.setEnabled(False)
        self.heat_map_checkbox.setEnabled(False)
        self.dpre_checkbox.setEnabled(False)
        self.pre_settings = QPushButton("PRE Settings", self)
        self.pre_settings.clicked.connect(partial(self.show_popup, PreAnalysisPopup, self.variables))

        pre_groupbox.layout().addWidget(self.do_pre_checkbox, 0, 0)
        pre_groupbox.layout().addWidget(self.pre_settings, 0, 1)
        pre_groupbox.layout().addWidget(self.dpre_checkbox, 1, 0)
        pre_groupbox.layout().addWidget(self.dpre_button, 1, 1)
        pre_groupbox.layout().addWidget(self.heat_map_checkbox, 2, 0)
        pre_groupbox.layout().addWidget(self.heat_map_button, 2, 1)


        series_plotting_groupbox = QGroupBox()
        series_plotting_groupbox.setTitle("Series Plotting")
        series_plotting_groupbox_layout = QGridLayout()
        series_plotting_groupbox.setLayout(series_plotting_groupbox_layout)

        series_plotting_groupbox.layout().addWidget(self.tplot_button, 0, 0, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.bar_button, 0, 1, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.ext_bar_checkbox, 1, 0, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.ext_bar_button, 1, 1, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.comp_bar_checkbox, 2, 0, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.comp_bar_button, 2, 1, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.vert_bar_checkbox, 3, 0, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.vert_bar_button, 3, 1, 1, 1)

        res_evo_groupbox = QGroupBox()
        res_evo_groupbox.setTitle("Residue Evolution Plot")
        res_evo_groupbox_layout = QGridLayout()
        res_evo_groupbox.setLayout(res_evo_groupbox_layout)

        res_evo_groupbox.layout().addWidget(self.revo_button, 0, 0, 1, 2)
        res_evo_groupbox.layout().addWidget(self.res_evo_checkbox, 1, 0, 1, 1)
        res_evo_groupbox.layout().addWidget(self.res_evo_button, 1, 1, 1, 1)
        res_evo_groupbox.layout().addWidget(self.scatter_checkbox, 2, 0, 1, 1)
        res_evo_groupbox.layout().addWidget(self.scatter_button, 2, 1, 1, 1)
        res_evo_groupbox.layout().addWidget(self.scatter_flower_checkbox, 3, 0, 1, 1)
        res_evo_groupbox.layout().addWidget(self.scatter_flower_button, 3, 1, 1, 1)



        buttons_groupbox = QGroupBox()
        buttons_groupbox_layout = QHBoxLayout()
        buttons_groupbox.setLayout(buttons_groupbox_layout)

        self.load_config_button = QPushButton("Load Configuration", self)
        self.save_config_button = QPushButton("Save Configuration", self)
        self.run_farseer_button = QPushButton("Run FarSeer-NMR", self)
        buttons_groupbox.layout().addWidget(self.load_config_button)
        self.load_config_button.clicked.connect(self.load_config)
        self.save_config_button.clicked.connect(self.save_config)
        self.run_farseer_button.clicked.connect(self.run_farseer_calculation)
        buttons_groupbox.layout().addWidget(self.save_config_button)
        buttons_groupbox.layout().addWidget(self.run_farseer_button)



        grid.layout().addWidget(paths_group_box, 0, 0, 3, 16)
        grid.layout().addWidget(fasta_groupbox, 7, 4, 4, 4)
        grid.layout().addWidget(sidechains_groupbox, 3, 4, 4, 4)
        grid.layout().addWidget(cs_norm_groupbox, 7, 0, 4, 4)
        grid.layout().addWidget(lost_analysis_groupbox, 3, 0, 4, 4)
        grid.layout().addWidget(series_groupbox, 3, 8, 6, 4)
        grid.layout().addWidget(figure_groupbox, 3, 12, 6, 4)
        grid.layout().addWidget(figure_groupbox, 3, 12, 6, 4)

        grid.layout().addWidget(restraint_groupbox, 11, 0, 10, 8)
        grid.layout().addWidget(cs_groupbox, 9, 8, 5, 4)
        grid.layout().addWidget(pre_groupbox, 9, 12, 5, 4)
        grid.layout().addWidget(series_plotting_groupbox, 14, 8, 7, 4)
        grid.layout().addWidget(res_evo_groupbox, 14, 12, 7, 4)
        grid.layout().addWidget(buttons_groupbox, 21, 0, 2, 16)

        self.load_variables()


    def activate_pre_analysis(self):
        if self.plot_height_ratio.isChecked() or self.plot_volume_ratio.isChecked():
            self.do_pre_checkbox.setEnabled(True)
            self.dpre_checkbox.setEnabled(True)
            self.heat_map_checkbox.setEnabled(True)
        else:
            self.do_pre_checkbox.setEnabled(False)
            self.dpre_checkbox.setEnabled(False)
            self.heat_map_checkbox.setEnabled(False)

    def set_spectrum_path_text(self, path=None):
        self.spectrum_path.setText(path)
        self.variables["general_settings"]["spectra_path"] = path
        self.parent().parent().parent().load_peak_lists(path)



    def set_output_path_text(self, path=None):
        self.output_path.setText(path)

    def set_spectrum_path(self, path=None):
        if not path:
            path = str(QFileDialog.getExistingDirectory(None, 'Select Directory', os.getcwd()))
        self.set_spectrum_path_text(path)



    def set_output_path(self, path=None):
        if not path:
            path = str(QFileDialog.getExistingDirectory(None, 'Select Directory', os.getcwd()))
        self.output_path.setText(path)

    def load_config(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Load Configuration")
        msg.setInformativeText("This will overwrite all existing settings and data points!")
        msg.setWindowTitle("Reset Experimental Series")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()
        if retval == QMessageBox.Ok:
            self.variables = self.parent().parent().parent().load_config()
            if self.variables:
                self.load_variables()
        else:
            return

    def save_config(self, path=None):

        general = self.variables["general_settings"]
        fitting = self.variables["fitting_settings"]
        cs = self.variables["cs_settings"]
        csp = self.variables["csp_settings"]
        fasta = self.variables["fasta_settings"]
        plots_f1 = self.variables["PosF1_settings"]
        plots_f2 = self.variables["PosF2_settings"]
        plots_height = self.variables["Height_ratio_settings"]
        plots_volume = self.variables["Volume_ratio_settings"]

        # General Settings

        general["spectra_path"] = self.spectrum_path.field.text()
        general["output_path"] = self.output_path.field.text()
        general["has_sidechains"] = self.has_sidechains_checkbox.isChecked()
        general["use_sidechains"] = self.use_sidechains_checkbox.isChecked()
        general["fig_height"] = self.figure_height.field.value()
        general["fig_width"] = self.figure_width.field.value()
        general["fig_dpi"] = self.figure_dpi.field.value()
        general["fig_file_type"] = self.figure_format.fields.currentText()


        # Fitting Settings
        fitting["expand_lost_yy"] = self.expand_lost_yy.isChecked()
        fitting["expand_lost_zz"] = self.expand_lost_zz.isChecked()
        fitting["perform_comparisons"] = self.perform_comparisons_checkbox.isChecked()
        fitting["do_cond1"] = self.x_checkbox.isChecked()
        fitting["do_cond2"] = self.y_checkbox.isChecked()
        fitting["do_cond3"] = self.z_checkbox.isChecked()

        # CS Settings
        cs["perform_cs_correction"] = self.cs_correction.isChecked()
        cs["cs_correction_res_ref"] = self.cs_correction_res_ref.field.value()

        # CSP Settings
        csp["csp_res4alpha"] = self.csp_alpha.field.value()
        csp["cs_lost"] = self.csp_lost.fields.currentText()

        # FASTA Settings
        fasta["applyFASTA"] = self.apply_fasta_checkbox.isChecked()
        fasta["FASTAstart"] = self.fasta_start.field.value()

        self.variables["pre_settings"]["apply_PRE_analysis"] = self.do_pre_checkbox.isChecked()

        # Plot F1 Settings
        plots_f1["calcs_PosF1_delta"] = self.plot_F1_data.isChecked()
        plots_f1["yy_label_PosF1_delta"] = self.plot_F1_y_label.field.text()
        plots_f1["yy_scale_PosF1_delta"] = self.plot_F1_y_scale.field.value()
        plots_f1["calccol_name_PosF1_delta"] = self.plot_F1_calccol.field.text()

        # Plot F2 Settings
        plots_f2["calcs_PosF2_delta"] = self.plot_F2_data.isChecked()
        plots_f2["yy_label_PosF2_delta"] = self.plot_F2_y_label.field.text()
        plots_f2["yy_scale_PosF2_delta"] = self.plot_F2_y_scale.field.value()
        plots_f2["calccol_name_PosF2_delta"] = self.plot_F2_calccol.field.text()


        # Plot CSP Settings
        csp["calcs_CSP"] = self.plot_CSP.isChecked()
        csp["yy_label_CSP"] =self.plot_CSP_y_label.field.text()
        csp["yy_scale_CSP"] = self.plot_CSP_y_scale.field.value()
        csp["calccol_name_CSP"] = self.plot_CSP_calccol.field.text()

        # Plot Height Settings
        plots_height["calcs_Height_ratio"] = self.plot_height_ratio.isChecked()
        plots_height["yy_label_Height_ratio"] = self.plot_height_y_label.field.text()
        plots_height["yy_scale_Height_ratio"] =self.plot_height_y_scale.field.value()
        plots_height["calccol_name_Height_ratio"] = self.plot_height_calccol.field.text()

        # Plot Volume Settings
        plots_volume["calcs_Volume_ratio"] = self.plot_volume_ratio.isChecked()
        plots_volume["yy_label_Volume_ratio"] = self.plot_volume_y_label.field.text()
        plots_volume["yy_scale_Volume_ratio"] = self.plot_volume_y_scale.field.value()
        plots_volume["calccol_name_Volume_ratio"] = self.plot_volume_calccol.field.text()

        # Plot Booleans
        self.variables["plotting_flags"]["do_ext_bar"] = self.ext_bar_checkbox.isChecked()
        self.variables["plotting_flags"]["do_comp_bar"] = self.comp_bar_checkbox.isChecked()
        self.variables["plotting_flags"]["do_vert_bar"] = self.vert_bar_checkbox.isChecked()
        self.variables["plotting_flags"]["do_res_evo"] = self.res_evo_checkbox.isChecked()
        self.variables["plotting_flags"]["do_cs_scatter"] = self.scatter_checkbox.isChecked()
        self.variables["plotting_flags"]["do_cs_scatter_flower"] = self.scatter_flower_checkbox.isChecked()
        self.variables["plotting_flags"]["do_heat_map"] =  self.heat_map_checkbox.isChecked()
        self.variables["plotting_flags"]["do_dpre_osci"] = self.dpre_checkbox.isChecked()

        self.parent().parent().parent().save_config(self.variables, path)

    def run_farseer_calculation(self):
        self.parent().parent().parent().run_farseer_calculation()

    def load_variables(self, variables=None):

        # if variables:
        #     self.variables = variables

        general = self.variables["general_settings"]
        fitting = self.variables["fitting_settings"]
        cs = self.variables["cs_settings"]
        csp = self.variables["csp_settings"]
        fasta = self.variables["fasta_settings"]
        plots_f1 = self.variables["PosF1_settings"]
        plots_f2 = self.variables["PosF2_settings"]
        plots_height = self.variables["Height_ratio_settings"]
        plots_volume = self.variables["Volume_ratio_settings"]


        # General Settings
        if os.path.exists(general["spectra_path"]):
            self.spectrum_path.field.setText(general["spectra_path"])
        else:
            self.spectrum_path.field.setText(os.getcwd())



        if os.path.exists(general["output_path"]):
            self.output_path.field.setText(general["output_path"])
        else:
            self.output_path.field.setText(os.getcwd())
        self.has_sidechains_checkbox.setChecked(general["has_sidechains"])
        self.use_sidechains_checkbox.setChecked(general["use_sidechains"])
        self.figure_height.setValue(general["fig_height"])
        self.figure_width.setValue(general["fig_width"])
        self.figure_dpi.setValue(general["fig_dpi"])
        self.figure_format.select(general["fig_file_type"])

        # Fitting Settings
        self.expand_lost_yy.setChecked(fitting["expand_lost_yy"])
        self.expand_lost_zz.setChecked(fitting["expand_lost_zz"])
        self.perform_comparisons_checkbox.setChecked(fitting["perform_comparisons"])
        self.x_checkbox.setChecked(fitting["do_cond1"])
        self.y_checkbox.setChecked(fitting["do_cond2"])
        self.z_checkbox.setChecked(fitting["do_cond3"])


        # CS Settings
        self.cs_correction.setChecked(cs["perform_cs_correction"])
        self.cs_correction_res_ref.setValue(cs["cs_correction_res_ref"])

        # CSP Settings
        self.csp_alpha.setValue(csp["csp_res4alpha"])
        self.csp_lost.select(csp["cs_lost"])

        # FASTA Settings
        self.apply_fasta_checkbox.setChecked(fasta["applyFASTA"])
        self.fasta_start.setValue(fasta["FASTAstart"])

        #PRE settings
        self.do_pre_checkbox.setChecked(self.variables["pre_settings"]["apply_PRE_analysis"])

        # Plot F1 Settings
        self.plot_F1_data.setChecked(plots_f1["calcs_PosF1_delta"])
        self.plot_F1_y_label.field.setText(plots_f1["yy_label_PosF1_delta"])
        self.plot_F1_y_scale.setValue(plots_f1["yy_scale_PosF1_delta"])
        self.plot_F1_calccol.field.setText(plots_f1["calccol_name_PosF1_delta"])

        # Plot F2 Settings
        self.plot_F2_data.setChecked(plots_f2["calcs_PosF2_delta"])
        self.plot_F2_y_label.field.setText(plots_f2["yy_label_PosF2_delta"])
        self.plot_F2_y_scale.setValue(plots_f2["yy_scale_PosF2_delta"])
        self.plot_F2_calccol.field.setText(plots_f2["calccol_name_PosF2_delta"])

        # Plot CSP Settings
        self.plot_CSP.setChecked(csp["calcs_CSP"])
        self.plot_CSP_y_label.field.setText(csp["yy_label_CSP"])
        self.plot_CSP_y_scale.setValue(csp["yy_scale_CSP"])
        self.plot_CSP_calccol.field.setText(csp["calccol_name_CSP"])

        # Plot Height Settings
        self.plot_height_ratio.setChecked(plots_height["calcs_Height_ratio"])
        self.plot_height_y_label.field.setText(plots_height["yy_label_Height_ratio"])
        self.plot_height_y_scale.setValue(plots_height["yy_scale_Height_ratio"])
        self.plot_height_calccol.field.setText(plots_height["calccol_name_Height_ratio"])

        # Plot Volume Settings
        self.plot_volume_ratio.setChecked(plots_volume["calcs_Volume_ratio"])
        self.plot_volume_y_label.field.setText(plots_volume["yy_label_Volume_ratio"])
        self.plot_volume_y_scale.setValue(plots_volume["yy_scale_Volume_ratio"])
        self.plot_volume_calccol.field.setText(plots_volume["calccol_name_Volume_ratio"])

        # Plot Booleans
        self.ext_bar_checkbox.setChecked(self.variables["plotting_flags"]["do_ext_bar"])
        self.comp_bar_checkbox.setChecked(self.variables["plotting_flags"]["do_comp_bar"])
        self.vert_bar_checkbox.setChecked(self.variables["plotting_flags"]["do_vert_bar"])
        self.res_evo_checkbox.setChecked(self.variables["plotting_flags"]["do_res_evo"])
        self.scatter_checkbox.setChecked(self.variables["plotting_flags"]["do_cs_scatter"])
        self.scatter_flower_checkbox.setChecked(self.variables["plotting_flags"]["do_cs_scatter_flower"])
        self.heat_map_checkbox.setChecked(self.variables["plotting_flags"]["do_heat_map"])
        self.dpre_checkbox.setChecked(self.variables["plotting_flags"]["do_pre_osci"])


    def show_popup(self, popup, variables):
        p = popup(self, variables=self.variables)
        p.exec_()
        p.raise_()


class Interface(QWidget):
 
    def __init__(self, parent=None, gui_settings=None, variables=None):
        QWidget.__init__(self, parent=parent)
        if variables:
            self.variables = variables

        self.initUI()
        self.widget2.setObjectName("InterfaceTop")
        self.gui_settings = gui_settings


    def load_variables(self, variables):

        self.variables = variables

        self.update_condition_boxes(3, 'x', len(self.variables["conditions"]["x"]))
        self.update_condition_boxes(2, 'y', len(self.variables["conditions"]["y"]))
        self.update_condition_boxes(1, 'z', len(self.variables["conditions"]["z"]))
        self.x_combobox.setValue(len(self.variables["conditions"]["x"]))
        self.y_combobox.setValue(len(self.variables["conditions"]["y"]))
        self.z_combobox.setValue(len(self.variables["conditions"]["z"]))
        self.peakListArea.update_variables(self.variables)



    def initUI(self):
        self.peakListArea = PeakListArea(self, variables=self.variables, gui_settings=gui_settings)
        grid = QGridLayout()
        grid2 = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        grid.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(grid)
        self.setObjectName("Interface")
        self.widget2 = QWidget(self)
        self.widget2.setLayout(grid2)
        self.widget3 = QWidget(self)
        widget3_layout = QGridLayout()

        self.widget3.setLayout(widget3_layout)
        self.sideBar = SideBar(self, peakLists, gui_settings=gui_settings, variables=self.variables)
        self.h_splitter = QSplitter(QtCore.Qt.Horizontal)
        widget4 = QWidget()
        widget4_layout = QGridLayout()
        widget4.setLayout(widget4_layout)
        widget4.layout().addWidget(self.sideBar)
        self.h_splitter.addWidget(widget4)
        widget4.setObjectName("Widget4")
        widget4.layout().setAlignment(QtCore.Qt.AlignTop)

        self.layout().addWidget(self.h_splitter)

        num_points_label = QLabel("Number of Points", self)
        num_points_label.setObjectName("PointsLabel")
        num_points_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid2.layout().addWidget(num_points_label, 0, 0, 1, 20)


        self.z_combobox = QSpinBox(self)
        self.y_combobox = QSpinBox(self)
        self.x_combobox = QSpinBox(self)
        self.z_label = QLabel("z", self)
        self.y_label = QLabel("y", self)
        self.x_label = QLabel("x", self)

        self.x_combobox.valueChanged.connect(partial(self.update_condition_boxes, 3, 'x'))
        self.y_combobox.valueChanged.connect(partial(self.update_condition_boxes, 2, 'y'))
        self.z_combobox.valueChanged.connect(partial(self.update_condition_boxes, 1, 'z'))

        grid2.layout().addWidget(self.x_combobox, 3, 2, 1, 1)
        grid2.layout().addWidget(self.y_combobox, 2, 2, 1, 1)
        grid2.layout().addWidget(self.z_combobox, 1, 2, 1, 1)

        grid2.layout().addWidget(self.x_label, 3, 1, 1, 1)
        grid2.layout().addWidget(self.y_label, 2, 1, 1, 1)
        grid2.layout().addWidget(self.z_label, 1, 1, 1, 1)

        self.z_combobox.setValue(1)
        self.y_combobox.setValue(1)
        self.x_combobox.setValue(1)
        self.z_combobox.setMinimum(1)
        self.y_combobox.setMinimum(1)
        self.x_combobox.setMinimum(1)
        self.z_combobox.setMaximum(10)
        self.y_combobox.setMaximum(10)
        self.x_combobox.setMaximum(15)


        self.sideBar.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)

        self.widget3.layout().addWidget(self.widget2, 0, 0, 1, 2)

        self.showTreeButton = QPushButton('Setup Experimental Series', self)

        self.showTreeButton.setObjectName("TreeButton")

        self.widget2.layout().addWidget(self.showTreeButton, 4, 2, 1, 16)
        self.peakListArea.setObjectName("PeakListArea")

        self.showTreeButton.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.widget3.layout().addWidget(self.peakListArea, 3, 0, 1, 2)
        self.showTreeButton.clicked.connect(self.peakListArea.updateTree)
        self.peakListArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.h_splitter.addWidget(self.widget3)
        # self.widget2.setFixedWidth(1264)
        self.widget2.setFixedWidth(gui_settings['interface_top_width'])
        self.widget2.setFixedHeight(gui_settings['interface_top_height'])



    def update_condition_boxes(self, row, dim, value):

        self.x, self.y, self.z = self.x_combobox.value(), self.y_combobox.value(), self.z_combobox.value()
        layout = self.widget2.layout()
        colCount = layout.columnCount()
        valuesDict = self.variables["conditions"]

        for m in range(3, colCount):
            item = layout.itemAtPosition(row, m)
            if item:
                if item.widget():
                    item.widget().hide()
            layout.removeItem(item)
        if len(valuesDict[dim]) < value:
            [valuesDict[dim].append('') for x in range(value-len(valuesDict[dim]))]
        if len(valuesDict[dim]) > value:
            valuesDict[dim] = valuesDict[dim][:value]

        for x in range(value):
            text_box = ValueField(self, x, dim, valuesDict)
            text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            if valuesDict[dim][x]:
                text_box.setText(str(valuesDict[dim][x]))

            layout.addWidget(text_box, row, x+3, 1, 1)



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
    import time
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
