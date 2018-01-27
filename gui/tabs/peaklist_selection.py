
from collections import OrderedDict
from functools import partial

from PyQt5 import QtCore

from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QSizePolicy, QSpinBox, QSplitter, QWidget

from gui.components.BaseWidget import BaseWidget
from gui.components.PeakListArea import PeakListArea
from gui.components.Sidebar import SideBar
from gui.components.ValuesField import ValueField


class PeaklistSelection(BaseWidget):
    def __init__(self, parent, gui_settings=None, variables=None, footer=None):
        BaseWidget.__init__(self, parent=parent, gui_settings=gui_settings, footer=footer)

        self.gui_parent = parent
        self.initUI()
        self.widget2.setObjectName("InterfaceTop")


    def load_variables(self):

        self.update_condition_boxes(3, 'x', len(self.variables["conditions"]["x"]))
        self.update_condition_boxes(2, 'y', len(self.variables["conditions"]["y"]))
        self.update_condition_boxes(1, 'z', len(self.variables["conditions"]["z"]))
        self.x_combobox.setValue(len(self.variables["conditions"]["x"]))
        self.y_combobox.setValue(len(self.variables["conditions"]["y"]))
        self.z_combobox.setValue(len(self.variables["conditions"]["z"]))
        self.peak_list_area.update_variables()

    def initUI(self):
        self.peak_list_area = PeakListArea(self, gui_settings=self.gui_settings)
        grid = QGridLayout()
        grid2 = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        grid.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(grid)
        self.setObjectName("PeakListSelection")
        self.widget2 = QWidget(self)
        self.widget2.setLayout(grid2)
        self.widget3 = QWidget(self)
        widget3_layout = QGridLayout()

        self.widget3.setLayout(widget3_layout)
        self.sideBar = SideBar(self, gui_settings=self.gui_settings)
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
        self.peak_list_area.setObjectName("PeakListArea")

        self.showTreeButton.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.widget3.layout().addWidget(self.peak_list_area, 3, 0, 1, 2)
        self.showTreeButton.clicked.connect(self.peak_list_area.updateTree)
        self.showTreeButton.clicked.connect(self.gui_parent.set_data_sets)
        self.peak_list_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.h_splitter.addWidget(self.widget3)
        # self.widget2.setFixedWidth(1264)
        self.widget2.setFixedWidth(self.gui_settings['interface_top_width'])
        self.widget2.setFixedHeight(self.gui_settings['interface_top_height'])

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
            [valuesDict[dim].append('') for x in range(value - len(valuesDict[dim]))]
        if len(valuesDict[dim]) > value:
            valuesDict[dim] = valuesDict[dim][:value]

        for x in range(value):
            text_box = ValueField(self, x, dim, valuesDict)
            text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            if valuesDict[dim][x]:
                text_box.setText(str(valuesDict[dim][x]))

            layout.addWidget(text_box, row, x + 3, 1, 1)



