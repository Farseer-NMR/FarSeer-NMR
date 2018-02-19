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
from functools import partial
import os

from PyQt5 import QtCore

from PyQt5.QtWidgets import QFileDialog, QGridLayout, QGroupBox, \
    QLabel, QMessageBox, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from gui.components.BaseWidget import BaseWidget
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox

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
from gui.popups.PRETheoreticalSelectionPopup import PRETheoreticalSelectionPopup


class Settings(BaseWidget):

    def __init__(self, parent=None, gui_settings=None, footer=None):

        BaseWidget.__init__(self, parent=parent,
                            gui_settings=gui_settings, footer=footer)

        grid = QGridLayout()
        grid2 = QGridLayout()
        self.setLayout(grid2)
        new_widget = QWidget(self)
        new_widget.setObjectName("SettingsWidget")
        new_widget.setLayout(grid)
        self.layout().addWidget(new_widget)

        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        paths_group_box = QGroupBox()
        paths_groupbox_layout = QGridLayout()
        paths_groupbox_layout.setSpacing(2)
        paths_group_box.setLayout(paths_groupbox_layout)

        self.spectrum_path = \
            LabelledLineEdit(self, "Spectrum Path",
                             callback=self.set_spectrum_path_text)
        self.output_path = LabelledLineEdit(self, "Calculation Output Folder",
                                            callback=self.set_output_path)

        self.spectrum_path_browse = QPushButton("...", self)
        self.output_path_browse = QPushButton("...", self)

        self.spectrum_path_browse.clicked.connect(self.set_spectrum_path)
        self.output_path_browse.clicked.connect(self.set_output_path)

        paths_group_box.layout().addWidget(self.spectrum_path, 0, 0, 1, 12)
        paths_group_box.layout().addWidget(self.output_path, 1, 0, 1, 12)
        paths_group_box.layout().addWidget(self.spectrum_path_browse,
                                           0, 13, 1, 1)
        paths_group_box.layout().addWidget(self.output_path_browse,
                                           1, 13, 1, 1)

        self.ext_bar_checkbox = LabelledCheckbox(self, "Extended Bar")
        self.comp_bar_checkbox = LabelledCheckbox(self, "Compact Bar")
        self.vert_bar_checkbox = LabelledCheckbox(self, "Vertical Bar")
        self.res_evo_checkbox = LabelledCheckbox(self, "Residue Evolution")
        self.scatter_checkbox = LabelledCheckbox(self, "CS Scatter")
        self.dpre_checkbox = LabelledCheckbox(self, "Oscillation Map")
        self.heat_map_checkbox = LabelledCheckbox(self, "Heat Map")
        self.scatter_flower_checkbox = LabelledCheckbox(self,
                                                        " CS Scatter Flower")

        self.tplot_button = QPushButton("General Series Plot Settings", self)
        self.tplot_button.clicked.connect(partial(self.show_popup,
                                                  SeriesPlotPopup))

        self.revo_button = QPushButton("General Evolution Settings", self)
        self.revo_button.clicked.connect(partial(self.show_popup,
                                                 GeneralResidueEvolution))

        self.bar_button = QPushButton("Bar Plot Settings", self)
        self.bar_button.clicked.connect(partial(self.show_popup, BarPlotPopup))

        self.ext_bar_button = QPushButton("Settings", self)
        self.ext_bar_button.clicked.connect(partial(self.show_popup,
                                                    ExtendedBarPopup))

        self.comp_bar_button = QPushButton("Settings", self)
        self.comp_bar_button.clicked.connect(partial(self.show_popup,
                                                     CompactBarPopup))

        self.vert_bar_button = QPushButton("Settings", self)
        self.vert_bar_button.clicked.connect(partial(self.show_popup,
                                                     VerticalBarPopup))

        self.res_evo_button = QPushButton("Settings", self)
        self.res_evo_button.clicked.connect(partial(self.show_popup,
                                                    ResidueEvolutionPopup))

        self.scatter_button = QPushButton("Settings", self)
        self.scatter_button.clicked.connect(partial(self.show_popup,
                                                    ScatterPlotPopup))

        self.scatter_flower_button = QPushButton("Settings", self)
        self.scatter_flower_button.clicked.connect(partial(
            self.show_popup, ScatterFlowerPlotPopup))

        self.heat_map_button = QPushButton("Settings", self)
        self.heat_map_button.clicked.connect(partial(
            self.show_popup, HeatMapPopup))

        self.dpre_button = QPushButton("Settings", self)
        self.dpre_button.clicked.connect(partial(self.show_popup,
                                                 OscillationMapPopup))

        self.fasta_button = QPushButton("Select FASTA Files", self)
        self.fasta_button.clicked.connect(partial(self.show_popup,
                                                  FastaSelectionPopup))

        self.has_sidechains_checkbox = LabelledCheckbox(
            self, "Are Sidechain Peaks Present?")
        self.use_sidechains_checkbox = LabelledCheckbox(self,
                                                        "Analyse Sidechains?")
        self.perform_comparisons_checkbox = LabelledCheckbox(
            self, "Perform Comparisons?")
        self.apply_fasta_checkbox = LabelledCheckbox(self, "Apply FASTA?")
        self.fasta_start = LabelledSpinBox(
                                           self,
                                           "Fasta start",
                                           maximum=10000,
                                           step=1
                                           )

        self.expand_lost_yy = LabelledCheckbox(self,
                                               "Search lost residues along Y axis?")
        self.expand_lost_zz = LabelledCheckbox(self,
                                               "Search lost residues along Z axis?")

        self.figure_width = LabelledDoubleSpinBox(
                                                  self,
                                                  "Figure Width",
                                                  minimum=0.1,
                                                  maximum=100,
                                                  step=0.1
                                                  )
        self.figure_height = LabelledDoubleSpinBox(
                                                   self,
                                                   "Figure Height",
                                                   minimum=0.1,
                                                   maximum=100,
                                                   step=0.1
                                                  )
        self.figure_dpi = LabelledSpinBox(self,
                                          "Figure DPI",
                                          minimum=0,
                                          maximum=10000,
                                          step=10)
        self.figure_format = LabelledCombobox(self,
                                              "Figure Format",
                                              items=['pdf',
                                                     'png',
                                                     'ps',
                                                     'svg'])

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

        self.x_checkbox = LabelledCheckbox(self, "Along X Axis")
        self.y_checkbox = LabelledCheckbox(self, "Along Y Axis")
        self.z_checkbox = LabelledCheckbox(self, "Along Z Axis")

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
        self.cs_correction_res_ref = LabelledSpinBox(self,
                                                     text="Correction Residue")

        cs_norm_groupbox = QGroupBox()
        cs_norm_groupbox.setTitle("Chemical Shift Normalisation")
        cs_groupbox_layout = QVBoxLayout()
        cs_norm_groupbox.setLayout(cs_groupbox_layout)
        cs_norm_groupbox.layout().addWidget(self.cs_correction)
        cs_norm_groupbox.layout().addWidget(self.cs_correction_res_ref)

        lost_analysis_groupbox = QGroupBox()
        lost_analysis_groupbox.setTitle("Search lost residues across axes")
        lost_analysis_groupbox_layout = QVBoxLayout()
        lost_analysis_groupbox.setLayout(lost_analysis_groupbox_layout)
        lost_analysis_groupbox.layout().addWidget(self.expand_lost_yy)
        lost_analysis_groupbox.layout().addWidget(self.expand_lost_zz)

        cs_groupbox = QGroupBox()
        cs_groupbox.setTitle("CSP Specific")
        cs_groupbox_layout = QVBoxLayout()
        cs_groupbox.setLayout(cs_groupbox_layout)

        self.csp_alpha = LabelledDoubleSpinBox(self,
                                               text="CSP Alpha",
                                               minimum=0.01,
                                               maximum=1,
                                               step=0.01)
        self.csp_lost = LabelledCombobox(self,
                                         text="Show Lost Residues",
                                         items=['prev', 'full', 'zero'])
        self.csp_exceptions = QPushButton("Alpha by residue", self)
        self.csp_exceptions.clicked.connect(partial(self.show_popup,
                                                    CSPExceptionsPopup
                                                    ))
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
        self.plot_height_ratio = LabelledCheckbox(self,
                                                  text="Height Ratio",
                                                  callback=self.activate_pre)
        self.plot_volume_ratio = LabelledCheckbox(self,
                                                  text="Volume Ratio",
                                                  callback=self.activate_pre)

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

        self.plot_F1_y_scale = LabelledDoubleSpinBox(
                                                     self,
                                                     text="",
                                                     minimum=0,
                                                     step=0.1
                                                    )
        self.plot_F2_y_scale = LabelledDoubleSpinBox(
                                                     self,
                                                     text="",
                                                     minimum=0,
                                                     step=0.1
                                                    )
        self.plot_CSP_y_scale = LabelledDoubleSpinBox(
                                                      self,
                                                      text="",
                                                      minimum=0,
                                                      step=0.1
                                                     )
        self.plot_height_y_scale = LabelledDoubleSpinBox(
                                                         self,
                                                         text="",
                                                         minimum=0,
                                                         step=0.1
                                                        )
        self.plot_volume_y_scale = LabelledDoubleSpinBox(
                                                         self,
                                                         text="",
                                                         minimum=0,
                                                         step=0.1
                                                        )

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
        self.pre_settings.clicked.connect(partial(self.show_popup,
                                                  PreAnalysisPopup))
        
        self.pretheo_button = QPushButton("Select Theo. PRE Files", self)
        self.pretheo_button.clicked.connect(partial(self.show_popup,
                                                  PRETheoreticalSelectionPopup))
        
        
        pre_groupbox.layout().addWidget(self.do_pre_checkbox, 0, 0)
        pre_groupbox.layout().addWidget(self.pre_settings, 0, 1)
        pre_groupbox.layout().addWidget(self.dpre_checkbox, 1, 0)
        pre_groupbox.layout().addWidget(self.dpre_button, 1, 1)
        pre_groupbox.layout().addWidget(self.heat_map_checkbox, 2, 0)
        pre_groupbox.layout().addWidget(self.heat_map_button, 2, 1)
        pre_groupbox.layout().addWidget(self.pretheo_button, 3, 1)

        series_plotting_groupbox = QGroupBox()
        series_plotting_groupbox.setTitle("Series Plotting")
        series_plotting_groupbox_layout = QGridLayout()
        series_plotting_groupbox.setLayout(series_plotting_groupbox_layout)

        series_plotting_groupbox.layout().addWidget(self.tplot_button,
                                                    0, 0, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.bar_button,
                                                    0, 1, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.ext_bar_checkbox,
                                                    1, 0, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.ext_bar_button,
                                                    1, 1, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.comp_bar_checkbox,
                                                    2, 0, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.comp_bar_button,
                                                    2, 1, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.vert_bar_checkbox,
                                                    3, 0, 1, 1)
        series_plotting_groupbox.layout().addWidget(self.vert_bar_button,
                                                    3, 1, 1, 1)

        res_evo_groupbox = QGroupBox()
        res_evo_groupbox.setTitle("Residue Evolution Plot")
        res_evo_groupbox_layout = QGridLayout()
        res_evo_groupbox.setLayout(res_evo_groupbox_layout)

        res_evo_groupbox.layout().addWidget(self.revo_button,
                                            0, 0, 1, 2)
        res_evo_groupbox.layout().addWidget(self.res_evo_checkbox,
                                            1, 0, 1, 1)
        res_evo_groupbox.layout().addWidget(self.res_evo_button,
                                            1, 1, 1, 1)
        res_evo_groupbox.layout().addWidget(self.scatter_checkbox,
                                            2, 0, 1, 1)
        res_evo_groupbox.layout().addWidget(self.scatter_button,
                                            2, 1, 1, 1)
        res_evo_groupbox.layout().addWidget(self.scatter_flower_checkbox,
                                            3, 0, 1, 1)
        res_evo_groupbox.layout().addWidget(self.scatter_flower_button,
                                            3, 1, 1, 1)
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
        grid.layout().addWidget(self.tab_footer, 21, 0, 2, 16)

        self.load_variables()

    def activate_pre(self):
        if self.plot_height_ratio.isChecked() or \
                self.plot_volume_ratio.isChecked():
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
        self.variables["general_settings"]["output_path"] = path

    def set_spectrum_path(self, path=None):
        if not path:
            path = str(QFileDialog.getExistingDirectory(None,
                                                        'Select Directory',
                                                        os.getcwd()))
        self.set_spectrum_path_text(path)

    def set_output_path(self, path=None):
        if not path:
            path = str(QFileDialog.getExistingDirectory(None,
                                                        'Select Directory',
                                                        os.getcwd()))
        self.output_path.setText(path)
        self.variables["general_settings"]["output_path"] = path

    def load_config(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Load Configuration")
        msg.setInformativeText("This will overwrite all existing "
                               "settings and data points!")
        msg.setWindowTitle("Reset Experimental Series")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        retval = msg.exec_()
        if retval == QMessageBox.Ok:
            self.variables = self.parent().parent().parent().load_config()

            self.load_variables()
        else:
            return

    def save_config(self):
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
        fitting["perform_comparisons"] = \
            self.perform_comparisons_checkbox.isChecked()
        fitting["do_along_x"] = self.x_checkbox.isChecked()
        fitting["do_along_y"] = self.y_checkbox.isChecked()
        fitting["do_along_z"] = self.z_checkbox.isChecked()

        # CS Settings
        cs["perform_cs_correction"] = self.cs_correction.isChecked()
        cs["cs_correction_res_ref"] = self.cs_correction_res_ref.field.value()

        # CSP Settings
        csp["csp_res4alpha"] = round(self.csp_alpha.field.value(), 2)
        csp["cs_lost"] = self.csp_lost.fields.currentText()

        # FASTA Settings
        fasta["applyFASTA"] = self.apply_fasta_checkbox.isChecked()
        fasta["FASTAstart"] = self.fasta_start.field.value()

        self.variables["pre_settings"]["apply_PRE_analysis"] = \
            self.do_pre_checkbox.isChecked()

        # Plot F1 Settings
        plots_f1["calcs_PosF1_delta"] = self.plot_F1_data.isChecked()
        plots_f1["yy_label_PosF1_delta"] = self.plot_F1_y_label.field.text()
        plots_f1["yy_scale_PosF1_delta"] = self.plot_F1_y_scale.field.value()
        plots_f1["calccol_name_PosF1_delta"] = \
            self.plot_F1_calccol.field.text()

        # Plot F2 Settings
        plots_f2["calcs_PosF2_delta"] = self.plot_F2_data.isChecked()
        plots_f2["yy_label_PosF2_delta"] = self.plot_F2_y_label.field.text()
        plots_f2["yy_scale_PosF2_delta"] = self.plot_F2_y_scale.field.value()
        plots_f2["calccol_name_PosF2_delta"] = \
            self.plot_F2_calccol.field.text()

        # Plot CSP Settings
        csp["calcs_CSP"] = self.plot_CSP.isChecked()
        csp["yy_label_CSP"] = self.plot_CSP_y_label.field.text()
        csp["yy_scale_CSP"] = self.plot_CSP_y_scale.field.value()
        csp["calccol_name_CSP"] = self.plot_CSP_calccol.field.text()

        # Plot Height Settings
        plots_height["calcs_Height_ratio"] = self.plot_height_ratio.isChecked()
        plots_height["yy_label_Height_ratio"] = \
            self.plot_height_y_label.field.text()
        plots_height["yy_scale_Height_ratio"] = \
            self.plot_height_y_scale.field.value()
        plots_height["calccol_name_Height_ratio"] = \
            self.plot_height_calccol.field.text()

        # Plot Volume Settings
        plots_volume["calcs_Volume_ratio"] = self.plot_volume_ratio.isChecked()
        plots_volume["yy_label_Volume_ratio"] = \
            self.plot_volume_y_label.field.text()
        plots_volume["yy_scale_Volume_ratio"] = \
            self.plot_volume_y_scale.field.value()
        plots_volume["calccol_name_Volume_ratio"] = \
            self.plot_volume_calccol.field.text()

        # Plot Booleans
        self.variables["plotting_flags"]["do_ext_bar"] = \
            self.ext_bar_checkbox.isChecked()
        self.variables["plotting_flags"]["do_comp_bar"] = \
            self.comp_bar_checkbox.isChecked()
        self.variables["plotting_flags"]["do_vert_bar"] = \
            self.vert_bar_checkbox.isChecked()
        self.variables["plotting_flags"]["do_res_evo"] = \
            self.res_evo_checkbox.isChecked()
        self.variables["plotting_flags"]["do_cs_scatter"] = \
            self.scatter_checkbox.isChecked()
        self.variables["plotting_flags"]["do_cs_scatter_flower"] = \
            self.scatter_flower_checkbox.isChecked()
        self.variables["plotting_flags"]["do_heat_map"] = \
            self.heat_map_checkbox.isChecked()
        self.variables["plotting_flags"]["do_dpre_osci"] = \
            self.dpre_checkbox.isChecked()


    def run_farseer_calculation(self):
        self.parent().parent().parent().run_farseer_calculation()

    def load_variables(self):
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
        self.perform_comparisons_checkbox.setChecked(
            fitting["perform_comparisons"])
        self.x_checkbox.setChecked(fitting["do_along_x"])
        self.y_checkbox.setChecked(fitting["do_along_y"])
        self.z_checkbox.setChecked(fitting["do_along_z"])

        # CS Settings
        self.cs_correction.setChecked(cs["perform_cs_correction"])
        self.cs_correction_res_ref.setValue(cs["cs_correction_res_ref"])

        # CSP Settings
        self.csp_alpha.setValue(csp["csp_res4alpha"])
        self.csp_lost.select(csp["cs_lost"])

        # FASTA Settings
        self.apply_fasta_checkbox.setChecked(fasta["applyFASTA"])
        self.fasta_start.setValue(fasta["FASTAstart"])

        # PRE settings
        self.do_pre_checkbox.setChecked(self.variables["pre_settings"]
                                        ["apply_PRE_analysis"])

        # Plot F1 Settings
        self.plot_F1_data.setChecked(
            plots_f1["calcs_PosF1_delta"])
        self.plot_F1_y_label.field.setText(
            plots_f1["yy_label_PosF1_delta"])
        self.plot_F1_y_scale.setValue(
            plots_f1["yy_scale_PosF1_delta"]
                                      )
        self.plot_F1_calccol.field.setText(
            plots_f1["calccol_name_PosF1_delta"])

        # Plot F2 Settings
        self.plot_F2_data.setChecked(plots_f2["calcs_PosF2_delta"])
        self.plot_F2_y_label.field.setText(plots_f2["yy_label_PosF2_delta"])
        self.plot_F2_y_scale.setValue(plots_f2["yy_scale_PosF2_delta"])
        self.plot_F2_calccol.field.setText(
            plots_f2["calccol_name_PosF2_delta"])

        # Plot CSP Settings
        self.plot_CSP.setChecked(csp["calcs_CSP"])
        self.plot_CSP_y_label.field.setText(csp["yy_label_CSP"])
        self.plot_CSP_y_scale.setValue(csp["yy_scale_CSP"])
        self.plot_CSP_calccol.field.setText(csp["calccol_name_CSP"])

        # Plot Height Settings
        self.plot_height_ratio.setChecked(plots_height["calcs_Height_ratio"])
        self.plot_height_y_label.field.setText(
            plots_height["yy_label_Height_ratio"])
        self.plot_height_y_scale.setValue(
            plots_height["yy_scale_Height_ratio"])
        self.plot_height_calccol.field.setText(
            plots_height["calccol_name_Height_ratio"])

        # Plot Volume Settings
        self.plot_volume_ratio.setChecked(plots_volume["calcs_Volume_ratio"])
        self.plot_volume_y_label.field.setText(
            plots_volume["yy_label_Volume_ratio"])
        self.plot_volume_y_scale.setValue(
            plots_volume["yy_scale_Volume_ratio"])
        self.plot_volume_calccol.field.setText(
            plots_volume["calccol_name_Volume_ratio"])

        # Plot Booleans
        self.ext_bar_checkbox.setChecked(
            self.variables["plotting_flags"]["do_ext_bar"])
        self.comp_bar_checkbox.setChecked(
            self.variables["plotting_flags"]["do_comp_bar"])
        self.vert_bar_checkbox.setChecked(
            self.variables["plotting_flags"]["do_vert_bar"])
        self.res_evo_checkbox.setChecked(
            self.variables["plotting_flags"]["do_res_evo"])
        self.scatter_checkbox.setChecked(
            self.variables["plotting_flags"]["do_cs_scatter"])
        self.scatter_flower_checkbox.setChecked(
            self.variables["plotting_flags"]["do_cs_scatter_flower"])
        self.heat_map_checkbox.setChecked(
            self.variables["plotting_flags"]["do_heat_map"])
        self.dpre_checkbox.setChecked(
            self.variables["plotting_flags"]["do_dpre_osci"])

    def show_popup(self, popup):
        popup(self).launch()
