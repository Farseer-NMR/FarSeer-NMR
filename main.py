import sys
from functools import partial
import json
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog, QLabel, QGroupBox, QGridLayout, \
    QSpinBox, QPushButton, QTabWidget, QHBoxLayout, QSplitter, QCheckBox, QSizePolicy, QSplashScreen, QSpacerItem

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
from gui.popups.GeneralResidueEvolution import GeneralResidueEvolution
from gui.popups.VerticalBar import VerticalBarPopup
from gui.popups.PreAnalysisPopup import PreAnalysisPopup
from gui.popups.ResidueEvolution import ResidueEvolutionPopup
from gui.popups.ScatterPlotPopup import ScatterPlotPopup
from gui.popups.ScatterFlowerPlotPopup import ScatterFlowerPlotPopup
from gui.popups.HeatMapPopup import HeatMapPopup
from gui.popups.DPrePopup import DPrePopup
from gui.popups.TitrationPlotPopup import TitrationPlotPopup

from gui.Footer import Footer

from gui import resources_rc


from current06.fslibs.io import json_to_fsuv

valuesDict = {
            'x': [],
            'y': [],
            'z': []
        }

peakLists = {}

class TabWidget(QTabWidget):

    def __init__(self, app_dims, gui_settings):
        QTabWidget.__init__(self, parent=None)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab1.setLayout(QGridLayout())
        self.tab2.setLayout(QGridLayout())
        self.tab3 = QWidget()

        self.tab1.layout().addWidget(Settings(gui_settings=gui_settings))
        self.tab2.layout().addWidget(Interface(gui_settings=gui_settings))


        self.addTab(self.tab2, "PeakList Selection")
        self.addTab(self.tab1, "Settings")
        self.addTab(self.tab3, "Results")


        self.tab1.setObjectName("Settings")

        """
        self.tabButton = QToolButton(self)
        self.tabButton.setIcon(Icon('icons/header-cogs.png'))
        self.tabButton.setText('')
        self.tabButton.setIconSize(self.tabButton.size())
        self.setAutoFillBackground(True)
        self.tabButton.setStyleSheet('QIcon {background-color: #001450;}')
        self.setCornerWidget(self.tabButton)

        """

        self.tablogo = QLabel(self)
        self.tablogo.setAutoFillBackground(True)
        self.tablogo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)




        pixmap = QtGui.QPixmap(os.path.join(ICON_DIR, 'icons/header-logo.png'))
        self.tablogo.setPixmap(pixmap)
        self.tablogo.setContentsMargins(9, 0, 0, 6)
        self.setCornerWidget(self.tablogo, corner=QtCore.Qt.TopLeftCorner)
        self.setFixedSize(QtCore.QSize(gui_settings['app_width'], gui_settings['app_height']))


    def load_config(self):
        import os
        fname = QFileDialog.getOpenFileName(self, 'Load Configuration', os.getcwd())
        if fname[0]:
            variables = json.load(open(fname[0], 'r'))
            return variables
        return None

    def save_config(self, variables):

        fname = QFileDialog.getSaveFileName(self, 'Save Configuration')
        with open(fname[0], 'w') as outfile:
            json.dump(variables, outfile, indent=4, sort_keys=True)

    def run_farseer_calculation(self):
        from current.setup_farseer_calculation import create_directory_structure
        spectrum_path = self.tab1.spectrum_path.field.text()
        peak_list_objects = self.tab2.peakListArea.peak_list_objects
        # spectrum_dir = os.getcwd()
        create_directory_structure(spectrum_path, valuesDict, peak_list_objects, peakLists)
        self.write_fsuv(spectrum_path)
        from current.farseermain import read_user_variables, run_farseer
        fsuv, cwd = read_user_variables(spectrum_path)
        run_farseer('{}/spectra'.format(cwd), fsuv)

    def write_fsuv(self, file_path):
        variables = self.tab1.variables
        json_to_fsuv(file_path, variables=variables)





class Settings(QWidget):
    def __init__(self, parent=None, gui_settings=None):
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
        grid.setSpacing(3)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        from current.default_config import defaults
        # self.variables = None
        self.variables = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'current', 'blank_config.json'), 'r'))
        paths_group_box = QGroupBox()
        paths_groupbox_layout = QVBoxLayout()
        paths_groupbox_layout.setSpacing(5)
        paths_group_box.setLayout(paths_groupbox_layout)

        self.spectrum_path = LabelledLineEdit(self, "Spectrum Path")
        self.logfile_path = LabelledLineEdit(self, "Log file Path")

        paths_group_box.layout().addWidget(self.spectrum_path)
        paths_group_box.layout().addWidget(self.logfile_path)

        self.ext_bar_checkbox = LabelledCheckbox(self, "Extended Bar")
        self.comp_bar_checkbox = LabelledCheckbox(self, "Compact Bar")
        self.vert_bar_checkbox = LabelledCheckbox(self, "Vertical Bar")
        self.res_evo_checkbox = LabelledCheckbox(self, "Residue Evolution")
        self.scatter_checkbox = LabelledCheckbox(self, "CS Scatter")
        self.dpre_checkbox = LabelledCheckbox(self, "DPre")
        self.heat_map_checkbox = LabelledCheckbox(self, "PRE Heat Map")
        self.scatter_flower_checkbox = LabelledCheckbox(self, " CS Scatter Flower")

        self.tplot_button = QPushButton("Titration Plot Settings", self)
        self.tplot_button.clicked.connect(partial(self.show_popup, TitrationPlotPopup, self.variables))

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
        #
        # self.user_details_button = QPushButton("Settings", self)
        # self.user_details_button.clicked.connect(partial(self.show_popup, UserMarksPopup, self.variables))

        self.scatter_button = QPushButton("Settings", self)
        self.scatter_button.clicked.connect(partial(self.show_popup, ScatterPlotPopup, self.variables))

        self.scatter_flower_button = QPushButton("Settings", self)
        self.scatter_flower_button.clicked.connect(partial(self.show_popup, ScatterFlowerPlotPopup, self.variables))

        self.heat_map_button = QPushButton("Settings", self)
        self.heat_map_button.clicked.connect(partial(self.show_popup, HeatMapPopup, self.variables))

        self.dpre_button = QPushButton("Settings", self)
        self.dpre_button.clicked.connect(partial(self.show_popup, DPrePopup, self.variables))

        self.has_sidechains_checkbox = LabelledCheckbox(self, "Sidechain Peaks?")
        self.use_sidechains_checkbox = LabelledCheckbox(self, "Analyse Sidechains?")
        self.perform_comparisons_checkbox = LabelledCheckbox(self, "Perform Comparisons?")
        self.apply_fasta_checkbox = LabelledCheckbox(self, "Apply FASTA?")
        self.fasta_start = LabelledSpinBox(self, "Fasta start")

        self.expand_lost_yy = LabelledCheckbox(self, "Analyse Lost Y Residues?")
        self.expand_lost_zz = LabelledCheckbox(self, "Analyse Lost Z Residues?")

        self.figure_width = LabelledDoubleSpinBox(self, "Figure Width")
        self.figure_height = LabelledDoubleSpinBox(self, "Figure Height")
        self.figure_dpi = LabelledDoubleSpinBox(self, "Figure DPI")
        self.figure_format = LabelledCombobox(self, "Figure Format", items=['pdf', 'png', 'ps', 'svg'])

        grid.layout().addWidget(paths_group_box, 0, 0, 4, 20)


        general_groupbox = QGroupBox()
        general_groupbox_layout = QHBoxLayout()
        general_groupbox_layout.setSpacing(5)
        general_groupbox.setLayout(general_groupbox_layout)

        general_groupbox.layout().addWidget(self.has_sidechains_checkbox)
        general_groupbox.layout().addWidget(self.use_sidechains_checkbox)
        general_groupbox.layout().addWidget(self.perform_comparisons_checkbox)
        general_groupbox.layout().addWidget(self.expand_lost_yy)
        general_groupbox.layout().addWidget(self.expand_lost_zz)

        figure_groupbox = QGroupBox()
        figure_groupbox_layout = QHBoxLayout()
        figure_groupbox_layout.setSpacing(10)
        figure_groupbox.setLayout(figure_groupbox_layout)

        figure_groupbox.layout().addWidget(self.figure_width)
        figure_groupbox.layout().addWidget(self.figure_height)
        figure_groupbox.layout().addWidget(self.figure_dpi)
        figure_groupbox.layout().addWidget(self.figure_format)


        grid.layout().addWidget(general_groupbox, 5, 0, 2, 20)
        grid.layout().addWidget(figure_groupbox, 7, 0, 2, 20)

        # res_evo_groupbox = QGroupBox()
        # res_evo_groupbox_layout = QHBoxLayout()
        # res_evo_groupbox.setLayout(res_evo_groupbox_layout)
        #
        # res_evo_groupbox.layout().addWidget(self.res_evo_fitting)
        # res_evo_groupbox.layout().addWidget(self.res_evo_fit_line_colour)
        # res_evo_groupbox.layout().addWidget(self.res_evo_fit_line_width)

        # grid.layout().addWidget(res_evo_groupbox, 4, 0, 1, 3)

        fasta_groupbox = QGroupBox()
        fasta_groupbox_layout = QHBoxLayout()
        fasta_groupbox.setLayout(fasta_groupbox_layout)

        fasta_groupbox.layout().addWidget(self.apply_fasta_checkbox)
        fasta_groupbox.layout().addWidget(self.fasta_start)
        grid.layout().addWidget(fasta_groupbox, 9, 14, 2, 6)



        self.cs_correction = LabelledCheckbox(self, "CS Correction?")
        self.cs_correction_res_ref = LabelledSpinBox(self, text="Correction Residue")
        self.csp_alpha = LabelledDoubleSpinBox(self, text="CSP Alpha")
        self.csp_lost = LabelledCombobox(self, text="CSP Lost Mode", items=['prev', 'full'])
        self.csp_exceptions = QPushButton("CSP Exceptions", self)
        self.do_pre = LabelledCheckbox(self, "PRE Analysis")
        self.pre_settings = QPushButton("PRE Settings", self)
        self.pre_settings.clicked.connect(partial(self.show_popup, PreAnalysisPopup, self.variables))

        cs_groupbox = QGroupBox()
        cs_groupbox_layout = QHBoxLayout()
        cs_groupbox.setLayout(cs_groupbox_layout)


        cs_groupbox.layout().addWidget(self.do_pre)
        cs_groupbox.layout().addWidget(self.pre_settings)
        cs_groupbox.layout().addWidget(self.cs_correction)
        cs_groupbox.layout().addWidget(self.cs_correction_res_ref)
        cs_groupbox.layout().addWidget(self.csp_alpha)
        cs_groupbox.layout().addWidget(self.csp_lost)
        cs_groupbox.layout().addWidget(self.csp_exceptions)


        grid.layout().addWidget(cs_groupbox, 9, 0, 2, 14)

        self.plot_F1_data = LabelledCheckbox(self, text="Plot F1 data")
        self.plot_F2_data = LabelledCheckbox(self, text="Plot F2 data")
        self.plot_CSP = LabelledCheckbox(self, text="Plot CSPs")
        self.plot_height_ratio = LabelledCheckbox(self, text="Plot Height Ratio")
        self.plot_volume_ratio = LabelledCheckbox(self, text="Plot Volume Ratio")

        self.plot_F1_y_label = LabelledLineEdit(self, text="Y Axis Label")
        self.plot_F2_y_label = LabelledLineEdit(self, text="Y Axis Label")
        self.plot_CSP_y_label = LabelledLineEdit(self, text="Y Axis Label")
        self.plot_height_y_label = LabelledLineEdit(self, text="Y Axis Label")
        self.plot_volume_y_label = LabelledLineEdit(self, text="Y Axis Label")

        self.plot_F1_calccol = LabelledLineEdit(self, text="Data Column")
        self.plot_F2_calccol = LabelledLineEdit(self, text="Data Column")
        self.plot_CSP_calccol = LabelledLineEdit(self, text="Data Column")
        self.plot_height_calccol = LabelledLineEdit(self, text="Data Column")
        self.plot_volume_calccol = LabelledLineEdit(self, text="Data Column")

        self.plot_F1_y_scale = LabelledDoubleSpinBox(self, text="Y Axis Scale")
        self.plot_F2_y_scale = LabelledDoubleSpinBox(self, text="Y Axis Scale")
        self.plot_CSP_y_scale = LabelledDoubleSpinBox(self, text="Y Axis Scale")
        self.plot_height_y_scale = LabelledDoubleSpinBox(self, text="Y Axis Scale")
        self.plot_volume_y_scale = LabelledDoubleSpinBox(self, text="Y Axis Scale")

        plot_F1_group_box = QGroupBox(self)
        plot_F2_group_box = QGroupBox(self)
        plot_csp_group_box = QGroupBox(self)
        plot_height_group_box = QGroupBox(self)
        plot_volume_group_box = QGroupBox(self)

        plot_F1_layout = QVBoxLayout()
        plot_F2_layout = QVBoxLayout()
        plot_csp_layout = QVBoxLayout()
        plot_height_layout = QVBoxLayout()
        plot_volume_layout = QVBoxLayout()

        plot_F1_group_box.setLayout(plot_F1_layout)
        plot_F2_group_box.setLayout(plot_F2_layout)
        plot_csp_group_box.setLayout(plot_csp_layout)
        plot_height_group_box.setLayout(plot_height_layout)
        plot_volume_group_box.setLayout(plot_volume_layout)

        plot_F1_layout.setSpacing(5)
        plot_F2_layout.setSpacing(5)
        plot_csp_layout.setSpacing(5)
        plot_height_layout.setSpacing(5)
        plot_volume_layout.setSpacing(5)


        plot_F1_group_box.layout().addWidget(self.plot_F1_data)
        plot_F1_group_box.layout().addWidget(self.plot_F1_y_label)
        plot_F1_group_box.layout().addWidget(self.plot_F1_calccol)
        plot_F1_group_box.layout().addWidget(self.plot_F1_y_scale)

        plot_F2_group_box.layout().addWidget(self.plot_F2_data)
        plot_F2_group_box.layout().addWidget(self.plot_F2_y_label)
        plot_F2_group_box.layout().addWidget(self.plot_F2_calccol)
        plot_F2_group_box.layout().addWidget(self.plot_F2_y_scale)

        plot_csp_group_box.layout().addWidget(self.plot_CSP)
        plot_csp_group_box.layout().addWidget(self.plot_CSP_y_label)
        plot_csp_group_box.layout().addWidget(self.plot_CSP_calccol)
        plot_csp_group_box.layout().addWidget(self.plot_CSP_y_scale)

        plot_height_group_box.layout().addWidget(self.plot_height_ratio)
        plot_height_group_box.layout().addWidget(self.plot_height_y_label)
        plot_height_group_box.layout().addWidget(self.plot_height_calccol)
        plot_height_group_box.layout().addWidget(self.plot_height_y_scale)

        plot_volume_group_box.layout().addWidget(self.plot_volume_ratio)
        plot_volume_group_box.layout().addWidget(self.plot_volume_y_label)
        plot_volume_group_box.layout().addWidget(self.plot_volume_calccol)
        plot_volume_group_box.layout().addWidget(self.plot_volume_y_scale)

        # plots_widget = QWidget()
        # plot_layout = QGridLayout()
        # plots_widget.setLayout(plot_layout)

        grid.layout().addWidget(plot_F1_group_box, 11, 0, 5, 4)
        grid.layout().addWidget(plot_F2_group_box, 11, 4, 5, 4)
        grid.layout().addWidget(plot_csp_group_box, 11, 8, 5, 4)
        grid.layout().addWidget(plot_height_group_box, 11, 12, 5, 4)
        grid.layout().addWidget(plot_volume_group_box, 11, 16, 5, 4)

        # grid.layout().addWidget(plots_widget, 6, 0, 3, 5)

        tplot_group_box = QGroupBox(self)

        ext_bar_group_box = QGroupBox(self)
        comp_bar_group_box = QGroupBox(self)
        vert_bar_group_box = QGroupBox(self)
        res_evo_plot_group_box = QGroupBox(self)
        heat_map_group_box = QGroupBox(self)
        scatter_group_box = QGroupBox(self)
        scatter_flower_group_box = QGroupBox(self)
        dpre_group_box = QGroupBox(self)
        revo_plot_group_box = QGroupBox(self)

        tplot_group_box_layout = QVBoxLayout()
        ext_bar_group_box_layout = QHBoxLayout()
        comp_bar_group_box_layout = QHBoxLayout()
        vert_bar_group_box_layout = QHBoxLayout()
        res_evo_plot_group_box_layout = QHBoxLayout()
        heat_map_group_box_layout = QHBoxLayout()
        scatter_group_box_layout = QHBoxLayout()
        scatter_flower_group_box_layout = QHBoxLayout()
        dpre_group_box_layout = QHBoxLayout()
        revo_plot_group_box_layout = QHBoxLayout()

        tplot_group_box.setLayout(tplot_group_box_layout)
        ext_bar_group_box.setLayout(ext_bar_group_box_layout)
        comp_bar_group_box.setLayout(comp_bar_group_box_layout)
        vert_bar_group_box.setLayout(vert_bar_group_box_layout)
        res_evo_plot_group_box.setLayout(res_evo_plot_group_box_layout)
        heat_map_group_box.setLayout(heat_map_group_box_layout)
        scatter_group_box.setLayout(scatter_group_box_layout)
        scatter_flower_group_box.setLayout(scatter_flower_group_box_layout)
        dpre_group_box.setLayout(dpre_group_box_layout)
        revo_plot_group_box.setLayout(revo_plot_group_box_layout)

        tplot_group_box.layout().addWidget(self.tplot_button)
        tplot_group_box.layout().addWidget(self.bar_button)
        ext_bar_group_box.layout().addWidget(self.ext_bar_checkbox)
        ext_bar_group_box.layout().addWidget(self.ext_bar_checkbox)
        comp_bar_group_box.layout().addWidget(self.comp_bar_checkbox)
        vert_bar_group_box.layout().addWidget(self.vert_bar_checkbox)
        res_evo_plot_group_box.layout().addWidget(self.res_evo_checkbox)
        heat_map_group_box.layout().addWidget(self.heat_map_checkbox)
        scatter_group_box.layout().addWidget(self.scatter_checkbox)
        scatter_flower_group_box.layout().addWidget(self.scatter_flower_checkbox)
        dpre_group_box.layout().addWidget(self.dpre_checkbox)

        ext_bar_group_box.layout().addWidget(self.ext_bar_button)
        comp_bar_group_box.layout().addWidget(self.comp_bar_button)
        vert_bar_group_box.layout().addWidget(self.vert_bar_button)
        res_evo_plot_group_box.layout().addWidget(self.res_evo_button)
        heat_map_group_box.layout().addWidget(self.heat_map_button)
        scatter_flower_group_box.layout().addWidget(self.scatter_flower_button)
        scatter_group_box.layout().addWidget(self.scatter_button)
        dpre_group_box.layout().addWidget(self.dpre_button)
        revo_plot_group_box.layout().addWidget(self.revo_button)

        grid.layout().addWidget(tplot_group_box, 16, 0, 2, 4)
        grid.layout().addWidget(ext_bar_group_box, 16, 4, 2, 4)
        grid.layout().addWidget(comp_bar_group_box, 16, 8, 2, 4)
        grid.layout().addWidget(vert_bar_group_box, 16, 12, 2, 4)
        grid.layout().addWidget(dpre_group_box, 16, 16, 2, 4)
        grid.layout().addWidget(revo_plot_group_box, 18, 0, 2, 4)
        grid.layout().addWidget(res_evo_plot_group_box, 18, 4, 2, 4)
        grid.layout().addWidget(scatter_group_box, 18, 8, 2, 4)
        grid.layout().addWidget(scatter_flower_group_box, 18, 12, 2, 4)
        grid.layout().addWidget(heat_map_group_box, 18, 16, 2, 4)

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

        grid.layout().addWidget(buttons_groupbox, 20, 0, 1, 20)



    def load_config(self):
        self.variables = self.parent().parent().load_config()
        if self.variables:
            self.load_variables()

    def save_config(self):
        self.parent().parent().save_config(self.variables)

    def run_farseer_calculation(self):
        self.parent().parent().run_farseer_calculation()

    def load_variables(self):

        general = self.variables["general_settings"]
        fitting = self.variables["fitting_settings"]
        cs = self.variables["cs_settings"]
        csp = self.variables["csp_settings"]
        fasta = self.variables["fasta_settings"]
        plots_f1 = self.variables["plots_PosF1_settings"]
        plots_f2 = self.variables["plots_PosF2_settings"]
        plots_csp = self.variables["plots_CSP_settings"]
        plots_height = self.variables["plots_Height_ratio_settings"]
        plots_volume = self.variables["plots_Volume_ratio_settings"]

        # General Settings
        self.spectrum_path.field.setText(general["spectrum_path"])
        self.logfile_path.field.setText(general["logfile_name"])
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

        # CS Settings
        self.cs_correction.setChecked(cs["perform_cs_correction"])
        self.cs_correction_res_ref.setValue(cs["cs_correction_res_ref"])

        # CSP Settings
        self.csp_alpha.setValue(csp["csp_res4alpha"])
        self.csp_lost.select(csp["cs_lost"])

        # FASTA Settings
        self.apply_fasta_checkbox.setChecked(fasta["applyFASTA"])
        self.fasta_start.setValue(fasta["FASTAstart"])

        # Plot F1 Settings
        self.plot_F1_data.setChecked(plots_f1["plots_PosF1_delta"])
        self.plot_F1_y_label.field.setText(plots_f1["yy_label_PosF1_delta"])
        self.plot_F1_y_scale.setValue(plots_f1["yy_scale_PosF1_delta"])
        self.plot_F1_calccol.field.setText(plots_f1["calccol_name_PosF1_delta"])

        # Plot F2 Settings
        self.plot_F2_data.setChecked(plots_f2["plots_PosF2_delta"])
        self.plot_F2_y_label.field.setText(plots_f2["yy_label_PosF2_delta"])
        self.plot_F2_y_scale.setValue(plots_f2["yy_scale_PosF2_delta"])
        self.plot_F2_calccol.field.setText(plots_f2["calccol_name_PosF2_delta"])

        # Plot CSP Settings
        self.plot_CSP.setChecked(plots_csp["plots_CSP"])
        self.plot_CSP_y_label.field.setText(plots_csp["yy_label_CSP"])
        self.plot_CSP_y_scale.setValue(plots_csp["yy_scale_CSP"])
        self.plot_CSP_calccol.field.setText(plots_csp["calccol_name_CSP"])

        # Plot Height Settings
        self.plot_height_ratio.setChecked(plots_height["plots_Height_ratio"])
        self.plot_height_y_label.field.setText(plots_height["yy_label_Height_ratio"])
        self.plot_height_y_scale.setValue(plots_height["yy_scale_Height_ratio"])
        self.plot_height_calccol.field.setText(plots_height["calccol_name_Height_ratio"])

        # Plot Volume Settings
        self.plot_volume_ratio.setChecked(plots_volume["plots_Volume_ratio"])
        self.plot_volume_y_label.field.setText(plots_volume["yy_label_Volume_ratio"])
        self.plot_volume_y_scale.setValue(plots_volume["yy_scale_Volume_ratio"])
        self.plot_volume_calccol.field.setText(plots_volume["calccol_name_Volume_ratio"])

        # Plot Booleans
        self.ext_bar_checkbox.setChecked(self.variables["extended_bar_settings"]["do_ext_bar"])
        self.comp_bar_checkbox.setChecked(self.variables["compact_bar_settings"]["do_comp_bar"])
        self.vert_bar_checkbox.setChecked(self.variables["vert_bar_settings"]["do_vert_bar"])
        self.res_evo_checkbox.setChecked(self.variables["res_evo_settings"]["do_res_evo"])
        self.scatter_checkbox.setChecked(self.variables["cs_scatter_settings"]["do_cs_scatter"])
        self.heat_map_checkbox.setChecked(self.variables["heat_map_settings"]["do_heat_map"])
        self.dpre_checkbox.setChecked(self.variables["dpre_osci_settings"]["do_dpre"])
        # self.user_details_checkbox.setChecked(fitting["include_user_annotations"])

    def show_popup(self, popup, variables):
        p = popup(variables=self.variables)
        p.exec()
        p.raise_()


class Interface(QWidget):
 
    def __init__(self, parent=None, gui_settings=None):
        QWidget.__init__(self, parent=parent)
        self.initUI()
        self.widget2.setObjectName("InterfaceTop")
        self.gui_settings = gui_settings
        # self.setStyleSheet('.QWidget { border: 1px solid red; margin-top: 0;}')

    def initUI(self):
        self.peakListArea = PeakListArea(self, valuesDict=valuesDict, gui_settings=gui_settings)
        grid = QGridLayout()
        grid2 = QGridLayout()
        # grid2.setHorizontalSpacing(0)
        grid.setAlignment(QtCore.Qt.AlignTop)
        grid.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(grid)
        self.setObjectName("Interface")
        self.widget2 = QWidget(self)
        self.widget2.setLayout(grid2)
        axes_label = QLabel(" Axes    ", self)
        axes_label.setObjectName("AxesLabel")
        self.x_checkbox = QCheckBox(self)
        self.y_checkbox = QCheckBox(self)
        self.z_checkbox = QCheckBox(self)
        self.x_label = QLabel("x", self)
        self.y_label = QLabel("y", self)
        self.z_label = QLabel("z", self)
        self.widget2.layout().addWidget(axes_label, 0, 0, 1, 2)
        self.widget2.layout().addWidget(self.x_checkbox, 3, 0, 1, 1)
        self.widget2.layout().addWidget(self.y_checkbox, 2, 0, 1, 1)
        self.widget2.layout().addWidget(self.z_checkbox, 1, 0, 1, 1)
        self.widget2.layout().addWidget(self.x_label, 3, 1, 1, 1)
        self.widget2.layout().addWidget(self.y_label, 2, 1, 1, 1)
        self.widget2.layout().addWidget(self.z_label, 1, 1, 1, 1)
        self.widget3 = QWidget(self)
        widget3_layout = QGridLayout()

        self.widget3.setLayout(widget3_layout)

        self.sideBar = SideBar(self, peakLists, gui_settings=gui_settings)
        self.h_splitter = QSplitter(QtCore.Qt.Horizontal)
        widget4 = QWidget()
        widget4_layout = QGridLayout()
        widget4.setLayout(widget4_layout)
        widget4.layout().addWidget(self.sideBar)
        self.h_splitter.addWidget(widget4)

        self.layout().addWidget(self.h_splitter)

        num_points_label = QLabel("Number of Points", self)
        num_points_label.setObjectName("PointsLabel")
        num_points_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid2.layout().addWidget(num_points_label, 0, 2, 1, 12)


        self.z_combobox = QSpinBox(self)
        self.y_combobox = QSpinBox(self)
        self.x_combobox = QSpinBox(self)

        self.x_combobox.valueChanged.connect(partial(self.update_condition_boxes, 3, 'x'))
        self.y_combobox.valueChanged.connect(partial(self.update_condition_boxes, 2, 'y'))
        self.z_combobox.valueChanged.connect(partial(self.update_condition_boxes, 1, 'z'))

        grid2.layout().addWidget(self.x_combobox, 3, 2, 1, 1)
        grid2.layout().addWidget(self.y_combobox, 2, 2, 1, 1)
        grid2.layout().addWidget(self.z_combobox, 1, 2, 1, 1)

        self.z_combobox.setValue(1)
        self.y_combobox.setValue(1)
        self.x_combobox.setValue(1)
        self.z_combobox.setMinimum(1)
        self.y_combobox.setMinimum(1)
        self.x_combobox.setMinimum(1)
        self.z_combobox.setMaximum(10)
        self.y_combobox.setMaximum(10)
        self.x_combobox.setMaximum(10)
        self.sideBar.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)

        self.widget3.layout().addWidget(self.widget2, 0, 0, 1, 2)

        self.showTreeButton = QPushButton('Show Parameter Tree', self)

        self.showTreeButton.setObjectName("TreeButton")

        self.widget2.layout().addWidget(self.showTreeButton, 4, 2, 1, 12)
        self.peakListArea.setObjectName("PeakListArea")

        self.showTreeButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
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
        for m in range(3, colCount):
            item = layout.itemAtPosition(row, m)
            if item:
                if item.widget():
                    item.widget().hide()
            layout.removeItem(item)
        if len(valuesDict[dim]) < value:
            [valuesDict[dim].append(0) for x in range(value-len(valuesDict[dim]))]
        if len(valuesDict[dim]) > value:
            valuesDict[dim] = valuesDict[dim][:value]
        for x in range(value):
            text_box = ValueField(self, x, dim, valuesDict)
            # text_box.setFixedWidth(50)
            text_box.setText(str(valuesDict[dim][x]))
            layout.addWidget(text_box, row, x+3, 1, 1)


class Main(QWidget):

    def __init__(self, parent=None, gui_settings=None, **kw):
        QWidget.__init__(self, parent=parent)
        print(gui_settings)
        tabWidget = TabWidget(app_dims, gui_settings)
        footer = Footer(self, gui_settings=gui_settings)

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        self.layout().addWidget(tabWidget)
        self.layout().addWidget(footer)
        self.setObjectName("MainWidget")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    import time
    splash_pix = QtGui.QPixmap('gui/images/splash-screen.png')

    splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash.setEnabled(False)

    splash.show()

    screen_resolution = app.desktop().screenGeometry()

    from gui import gui_utils
    gui_settings = gui_utils.deliver_settings(screen_resolution)


    if (screen_resolution.height(), screen_resolution.width()) == (720, 1280):
        app_dims = screen_resolution.size()
        stylesheet = open('gui/stylesheet_720p.qss').read()
        print('720p')
    # elif (screen_resolution.height(), screen_resolution.width()) == (1440, 2560):
    #     app_dims = QtCore.QSize(1800, 850)
    else:
        app_dims = QtCore.QSize(1600, 1000)
        stylesheet = open('gui/stylesheet_2k.qss').read()
    ex = Main(gui_settings=gui_settings)
    splash.finish(ex)
    fin = 'gui/SinkinSans/SinkinSans-400Regular.otf'
    font_id = QtGui.QFontDatabase.addApplicationFont(fin)

    app.setStyleSheet(stylesheet)

    ex.show()
    ex.raise_()
    sys.exit(app.exec_())
