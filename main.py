import sys
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QGridLayout, QSpinBox, QPushButton, QTabWidget
from gui.components.PeakListArea import PeakListArea
from gui.components.Sidebar import SideBar
from gui.components.ValuesField import ValueField

from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.popups.ExtendedBarPopup import ExtendedBarPopup
from gui.popups.CompactBarPopup import CompactBarPopup

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

        label1 = QLabel("General Settings", self)
        label2 = QLabel("Spectrum Path", self)
        label3 = QLabel("Log file Path", self)


        self.ext_bar_checkbox = LabelledCheckbox(self, "Extended Bar")
        self.comp_bar_checkbox = LabelledCheckbox(self, "Compact Bar")
        self.vert_bar_checkbox = LabelledCheckbox(self, "Vertical Bar")
        self.res_evo_checkbox = LabelledCheckbox(self, "Residue Evolution")

        self.ext_bar_button = QPushButton("Settings", self)
        self.ext_bar_button.clicked.connect(self.show_extended_bar_popup)

        self.comp_bar_button = QPushButton("Settings", self)
        self.comp_bar_button.clicked.connect(self.show_compact_bar_popup)
        self.vert_bar_button = QPushButton("Settings", self)
        self.res_evo_button = QPushButton("Settings", self)


        self.spectra_path = QLineEdit()
        self.logfile_path = QLineEdit()
        self.has_sidechains_checkbox = LabelledCheckbox(self, "Sidechain Peaks?")
        self.use_sidechains_checkbox = LabelledCheckbox(self, "Analyse Sidechains?")
        self.perform_controls_checkbox = LabelledCheckbox(self, "Perform Controls?")

        grid.layout().addWidget(label1, 0, 0)
        grid.layout().addWidget(label2, 1, 0)
        grid.layout().addWidget(label3, 2, 0)
        grid.layout().addWidget(self.spectra_path, 1, 1, 1, 4)
        grid.layout().addWidget(self.logfile_path, 2, 1, 1, 4)
        grid.layout().addWidget(self.has_sidechains_checkbox, 3, 0, 1, 1)
        grid.layout().addWidget(self.use_sidechains_checkbox, 3, 1, 1, 1)
        grid.layout().addWidget(self.perform_controls_checkbox, 3, 2, 1, 1)

        grid.layout().addWidget(self.ext_bar_checkbox, 6, 0, 1, 1)
        grid.layout().addWidget(self.comp_bar_checkbox, 6, 1, 1, 1)
        grid.layout().addWidget(self.vert_bar_checkbox, 6, 2, 1, 1)
        grid.layout().addWidget(self.res_evo_checkbox, 6, 3, 1, 1)

        grid.layout().addWidget(self.ext_bar_button, 7, 0, 1, 1)
        grid.layout().addWidget(self.comp_bar_button, 7, 1, 1, 1)
        grid.layout().addWidget(self.vert_bar_button, 7, 2, 1, 1)
        grid.layout().addWidget(self.res_evo_button, 7, 3, 1, 1)

    def show_extended_bar_popup(self):
        popup = ExtendedBarPopup()
        popup.exec()
        popup.raise_()


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
        self.peakListArea.hide()
        


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
