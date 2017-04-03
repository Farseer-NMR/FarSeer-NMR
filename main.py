import sys
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QSpinBox, QPushButton, QTabWidget, QHBoxLayout, QComboBox
from gui.components.PeakListArea import PeakListArea
from gui.components.Sidebar import SideBar
from gui.components.ValuesField import ValueField

from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.popups.ExtendedBarPopup import ExtendedBarPopup
from gui.popups.CompactBarPopup import CompactBarPopup
from gui.popups.VerticalBar import VerticalBarPopup
from gui.popups.ResidueEvolution import ResidueEvolutionPopup
from gui.popups.UserMarksPopup import UserMarksPopup

valuesDict = {
            'x': [],
            'y': [],
            'z': []
        }


class Main(QTabWidget):

    def __init__(self):
        QTabWidget.__init__(self, parent=None)
        tab1 = Settings()
        tab2 = Interface()
        tab3 = QWidget()
        self.addTab(tab1, "Settings")
        self.addTab(tab2, "PeakList Selection")
        self.addTab(tab3, "Results")


class Settings(QWidget):
    def __init__(self):
        QWidget.__init__(self, parent=None)
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)

        # label1 = QLabel("General Settings", self)
        label2 = QLabel("Spectrum Path", self)
        label3 = QLabel("Log file Path", self)


        self.ext_bar_checkbox = LabelledCheckbox(self, "Extended Bar")
        self.comp_bar_checkbox = LabelledCheckbox(self, "Compact Bar")
        self.vert_bar_checkbox = LabelledCheckbox(self, "Vertical Bar")
        self.res_evo_checkbox = LabelledCheckbox(self, "Residue Evolution")
        self.user_details_checkbox = LabelledCheckbox(self, "User Details")

        self.ext_bar_button = QPushButton("Settings", self)
        self.ext_bar_button.clicked.connect(partial(self.show_popup, ExtendedBarPopup))

        self.comp_bar_button = QPushButton("Settings", self)
        self.comp_bar_button.clicked.connect(partial(self.show_popup, CompactBarPopup))
        self.vert_bar_button = QPushButton("Settings", self)
        self.vert_bar_button.clicked.connect(partial(self.show_popup, VerticalBarPopup))

        self.res_evo_button = QPushButton("Settings", self)
        self.res_evo_button.clicked.connect(partial(self.show_popup, ResidueEvolutionPopup))

        self.user_details_button = QPushButton("Settings", self)
        self.user_details_button.clicked.connect(partial(self.show_popup, UserMarksPopup))


        self.spectra_path = QLineEdit()
        self.logfile_path = QLineEdit()
        self.has_sidechains_checkbox = LabelledCheckbox(self, "Sidechain Peaks?")
        self.use_sidechains_checkbox = LabelledCheckbox(self, "Analyse Sidechains?")
        self.perform_controls_checkbox = LabelledCheckbox(self, "Perform Controls?")
        self.apply_fasta_checkbox = LabelledCheckbox(self, "Apply FASTA?")
        self.fasta_start = LabelledSpinBox(self, "Fasta start")

        self.res_evo_fitting = LabelledCheckbox(self, "Fit Parameter Evolution?")
        self.res_evo_fit_line_colour = LabelledLineEdit(self, text="Fit Line Colour")
        self.res_evo_fit_line_width = LabelledSpinBox(self, "Fit Line Width")

        self.expand_lost_yy = LabelledCheckbox(self, "Analyse Lost Y Residues?")
        self.expand_lost_zz = LabelledCheckbox(self, "Analyse Lost Z Residues?")

        grid.layout().addWidget(label2, 1, 0)
        grid.layout().addWidget(label3, 2, 0)
        grid.layout().addWidget(self.spectra_path, 1, 1, 1, 4)
        grid.layout().addWidget(self.logfile_path, 2, 1, 1, 4)

        grid.layout().addWidget(self.has_sidechains_checkbox, 3, 0, 1, 1)
        grid.layout().addWidget(self.use_sidechains_checkbox, 3, 1, 1, 1)
        grid.layout().addWidget(self.perform_controls_checkbox, 3, 2, 1, 1)
        grid.layout().addWidget(self.apply_fasta_checkbox, 3, 3, 1, 1)
        grid.layout().addWidget(self.fasta_start, 3, 4, 1, 1)

        grid.layout().addWidget(self.res_evo_fitting, 4, 0, 1, 1)
        grid.layout().addWidget(self.res_evo_fit_line_colour, 4, 1, 1, 1)
        grid.layout().addWidget(self.res_evo_fit_line_width, 4, 2, 1, 1)
        grid.layout().addWidget(self.expand_lost_yy, 4, 3, 1, 1)
        grid.layout().addWidget(self.expand_lost_zz, 4, 4, 1, 1)


        self.cs_correction = LabelledCheckbox(self, "Perform CS Correction?")
        self.cs_correction_res_ref = LabelledLineEdit(self, text="Correction Residue")
        self.csp_alpha = LabelledLineEdit(self, text="CSP Alpha")
        self.csp_lost = LabelledCombobox(self, text="CSP Lost Mode", items=['prev', 'full'])
        self.csp_exceptions = QPushButton("CSP Exceptions", self)

        grid.layout().addWidget(self.cs_correction, 5, 0, 1, 1)
        grid.layout().addWidget(self.cs_correction_res_ref, 5, 1, 1, 1)
        grid.layout().addWidget(self.csp_alpha, 5, 2, 1, 1)
        grid.layout().addWidget(self.csp_lost, 5, 3, 1, 1)
        grid.layout().addWidget(self.csp_exceptions, 5, 4, 1, 1)

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

        grid.layout().addWidget(self.plot_F1_data, 6, 0, 1, 1)
        grid.layout().addWidget(self.plot_F2_data, 6, 1, 1, 1)
        grid.layout().addWidget(self.plot_CSP, 6, 2, 1, 1)
        grid.layout().addWidget(self.plot_height_ratio, 6, 3, 1, 1)
        grid.layout().addWidget(self.plot_volume_ratio, 6, 4, 1, 1)

        grid.layout().addWidget(self.plot_F1_y_label, 7, 0, 1, 1)
        grid.layout().addWidget(self.plot_F2_y_label, 7, 1, 1, 1)
        grid.layout().addWidget(self.plot_CSP_y_label, 7, 2, 1, 1)
        grid.layout().addWidget(self.plot_height_y_label, 7, 3, 1, 1)
        grid.layout().addWidget(self.plot_volume_y_label, 7, 4, 1, 1)

        grid.layout().addWidget(self.plot_F1_calccol, 8, 0, 1, 1)
        grid.layout().addWidget(self.plot_F2_calccol, 8, 1, 1, 1)
        grid.layout().addWidget(self.plot_CSP_calccol, 8, 2, 1, 1)
        grid.layout().addWidget(self.plot_height_calccol, 8, 3, 1, 1)
        grid.layout().addWidget(self.plot_volume_calccol, 8, 4, 1, 1)

        grid.layout().addWidget(self.plot_F1_y_scale, 9, 0, 1, 1)
        grid.layout().addWidget(self.plot_F2_y_scale, 9, 1, 1, 1)
        grid.layout().addWidget(self.plot_CSP_y_scale, 9, 2, 1, 1)
        grid.layout().addWidget(self.plot_height_y_scale, 9, 3, 1, 1)
        grid.layout().addWidget(self.plot_volume_y_scale, 9, 4, 1, 1)

        grid.layout().addWidget(self.ext_bar_checkbox, 10, 0, 1, 1)
        grid.layout().addWidget(self.comp_bar_checkbox, 10, 1, 1, 1)
        grid.layout().addWidget(self.vert_bar_checkbox, 10, 2, 1, 1)
        grid.layout().addWidget(self.res_evo_checkbox, 10, 3, 1, 1)
        grid.layout().addWidget(self.user_details_checkbox, 10, 4, 1, 1)

        grid.layout().addWidget(self.ext_bar_button, 11, 0, 1, 1)
        grid.layout().addWidget(self.comp_bar_button, 11, 1, 1, 1)
        grid.layout().addWidget(self.vert_bar_button, 11, 2, 1, 1)
        grid.layout().addWidget(self.res_evo_button, 11, 3, 1, 1)
        grid.layout().addWidget(self.user_details_button, 11, 4, 1, 1)

    def show_popup(self, popup):
        p = popup()
        p.exec()
        p.raise_()


    def show_compact_bar_popup(self):
        popup = CompactBarPopup()
        popup.exec()
        popup.raise_()


class Interface(QWidget):
 
    def __init__(self):
        QWidget.__init__(self, parent=None)

        self.initUI()

    def initUI(self):
        self.peakListArea = PeakListArea(self, valuesDict=valuesDict)
        grid = QGridLayout()
        grid1 = QGridLayout()
        grid2 = QGridLayout()
        grid.setVerticalSpacing(0)
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)


        widget1 = QWidget(self)
        widget1.setLayout(grid1)
        self.widget2 = QWidget(self)
        self.widget2.setLayout(grid2)
        axes_label = QLabel("Use axes", self)
        self.x_checkbox = LabelledCheckbox(self, "x", fixed=True)
        self.y_checkbox = LabelledCheckbox(self, "y", fixed=True)
        self.z_checkbox = LabelledCheckbox(self, "z", fixed=True)
        self.widget2.layout().addWidget(axes_label, 0, 0, 1, 1)
        self.widget2.layout().addWidget(self.x_checkbox, 3, 0)
        self.widget2.layout().addWidget(self.y_checkbox, 2, 0)
        self.widget2.layout().addWidget(self.z_checkbox, 1, 0)

        self.sideBar = SideBar(self)

        self.layout().addWidget(self.sideBar, 0, 0, 4, 1)

        num_points_label = QLabel("Number of Points", self)

        grid2.layout().addWidget(num_points_label, 0, 1)

        self.z_combobox = QSpinBox(self)
        self.y_combobox = QSpinBox(self)
        self.x_combobox = QSpinBox(self)

        self.x_combobox.valueChanged.connect(partial(self.update_condition_boxes, 3, 'x'))
        self.y_combobox.valueChanged.connect(partial(self.update_condition_boxes, 2, 'y'))
        self.z_combobox.valueChanged.connect(partial(self.update_condition_boxes, 1, 'z'))

        self.z_combobox.setFixedWidth(100)
        self.y_combobox.setFixedWidth(100)
        self.x_combobox.setFixedWidth(100)

        grid2.layout().addWidget(self.x_combobox, 3, 1, 1, 1)
        grid2.layout().addWidget(self.y_combobox, 2, 1, 1, 1)
        grid2.layout().addWidget(self.z_combobox, 1, 1, 1, 1)

        self.z_combobox.setValue(1)
        self.y_combobox.setValue(1)
        self.x_combobox.setValue(1)

        self.layout().addWidget(self.widget2, 1, 1)

        self.showTreeButton = QPushButton('Show Parameter Tree', self)

        self.layout().addWidget(self.showTreeButton, 2, 1, 1, 3)
        self.layout().addWidget(self.peakListArea, 3, 1, 1, 3)
        self.showTreeButton.clicked.connect(self.peakListArea.updateTree)
        # self.peakListArea.hide()
        


    def update_condition_boxes(self, row, dim, value):

        self.x, self.y, self.z = self.x_combobox.value(), self.y_combobox.value(), self.z_combobox.value()
        layout = self.widget2.layout()
        colCount = layout.columnCount()
        for m in range(2, colCount):
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
            text_box.setFixedWidth(50)
            text_box.setText(str(valuesDict[dim][x]))
            layout.addWidget(text_box, row, x+2, 1, 1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    ex.raise_()
    sys.exit(app.exec_())
