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
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton, QWidget, QGridLayout
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox
from functools import partial

from gui.popups.BasePopup import BasePopup


class UserMarksPopup(BasePopup):
    """
    A popup for setting User defined plot marks in the  Farseer-NMR
    configuration.

    Parameters:
        parent(QWidget): parent widget for popup.

    Methods:
        .get_defaults()
        .get_values()
        .set_values()
        """
    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="User Marks Popup")

        self.marker_rows = 0
        layout2 = QGridLayout()
        layout1 = QGridLayout()
        self.mainWidget = QWidget(self)
        self.buttonWidget = QWidget(self)
        self.mainWidget.setLayout(layout1)
        self.buttonWidget.setLayout(layout2)
        self.buttonBox = QDialogButtonBox(
                                          QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel |
                                          QDialogButtonBox.RestoreDefaults)
        self.buttonBox.accepted.connect(self.setValues)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).\
            clicked.connect(self.set_defaults)
        self.buttonWidget.layout().addWidget(self.buttonBox)
        self.layout().addWidget(self.mainWidget, 0, 0)
        self.layout().addWidget(self.buttonWidget, 1, 0)
        self.pairs = []
        if self.variables:
            self.set_values_from_config()
        else:
            key = LabelledLineEdit(self, text='key')
            value = LabelledLineEdit(self, text='value')
            colour = ColourBox(self, text='colour')
            addButton = QPushButton("Add", self)
            removeButton = QPushButton("Remove", self)
            addButton.clicked.connect(self.add_row_to_popup)
            removeButton.clicked.\
                connect(partial(self.remove_row_to_popup, self.marker_rows))
            self.pairs.append([key, value, colour, addButton, removeButton])

            self.mainWidget.layout().addWidget(key, self.marker_rows, 0)
            self.mainWidget.layout().addWidget(value, self.marker_rows, 1)
            self.mainWidget.layout().addWidget(colour, self.marker_rows, 2)
            self.mainWidget.layout().addWidget(addButton, self.marker_rows, 3)
            self.mainWidget.layout().\
                addWidget(removeButton, self.marker_rows, 4)
            self.marker_rows += 1

    def add_row_to_popup(self):
        key = LabelledLineEdit(self, text='key')
        value = LabelledLineEdit(self, text='value')
        colour = ColourBox(self, text='colour')
        addButton = QPushButton("Add", self)
        addButton.clicked.connect(self.add_row_to_popup)
        removeButton = QPushButton("Remove", self)
        removeButton.clicked.\
            connect(partial(self.remove_row_to_popup, self.marker_rows))
        self.pairs.append([key, value, colour, addButton, removeButton])
        self.mainWidget.layout().addWidget(key, self.marker_rows, 0)
        self.mainWidget.layout().addWidget(value, self.marker_rows, 1)
        self.mainWidget.layout().addWidget(colour, self.marker_rows, 2)
        self.mainWidget.layout().addWidget(addButton, self.marker_rows, 3)
        self.mainWidget.layout().addWidget(removeButton, self.marker_rows, 4)
        self.marker_rows += 1

    def remove_row_to_popup(self, index, pop=True):

        if self.marker_rows == 1:
            print('cant remove only row from popup')
            for widget in self.pairs[0]:
                if hasattr(widget, 'field'):
                    widget.setText('')
                elif hasattr(widget, 'fields'):
                    widget.fields.setCurrentIndex(0)
                else:
                    break
            return

        self.marker_rows -= 1
        colCount = self.mainWidget.layout().columnCount()
        for m in range(0, colCount):
            item = self.mainWidget.layout().itemAtPosition(index, m)
            if item:
                if item.widget():
                    item.widget().hide()
            self.mainWidget.layout().removeItem(item)

        if pop:
            self.pairs.pop(index)

    def set_values_from_config(self):
        for i in range(self.marker_rows):
            self.remove_row_to_popup(i, pop=False)
        self.pairs = []
        self.marker_rows = 0

        for key1, value1 in \
                self.variables["bar_plot_settings"]["user_marks_dict"].items():

            key = LabelledLineEdit(self, text='key')
            key.field.setText(key1)
            value = LabelledLineEdit(self, text='value')
            value.field.setText(value1)
            colour = ColourBox(self, text='colour')
            colour.select(self.variables
                          ["bar_plot_settings"]["user_bar_colors_dict"][key1])
            addButton = QPushButton("Add", self)
            addButton.clicked.connect(self.add_row_to_popup)
            removeButton = QPushButton("Remove", self)
            removeButton.clicked.\
                connect(partial(self.remove_row_to_popup, self.marker_rows))
            self.pairs.append([key, value, colour, addButton, removeButton])
            self.mainWidget.layout().addWidget(key, self.marker_rows, 0)
            self.mainWidget.layout().addWidget(value, self.marker_rows, 1)
            self.mainWidget.layout().addWidget(colour, self.marker_rows, 2)
            self.mainWidget.layout().addWidget(addButton, self.marker_rows, 3)
            self.mainWidget.layout().\
                addWidget(removeButton, self.marker_rows, 4)
            self.marker_rows += 1

    def set_defaults(self):
        for i in range(self.marker_rows):
            self.remove_row_to_popup(i, pop=False)

        self.marker_rows = 0
        self.pairs = []

        for key1, value1 in \
                self.defaults["bar_plot_settings"]["user_marks_dict"].items():

            key = LabelledLineEdit(self, text='key')
            key.field.setText(key1)
            value = LabelledLineEdit(self, text='value')
            colour = ColourBox(self, text='colour')
            colour.select(self.defaults
                          ["bar_plot_settings"]["user_bar_colors_dict"][key1])
            value.field.setText(value1)
            addButton = QPushButton("Add", self)
            addButton.clicked.connect(self.add_row_to_popup)
            removeButton = QPushButton("Remove", self)
            removeButton.clicked.\
                connect(partial(self.remove_row_to_popup, self.marker_rows))
            self.pairs.append([key, value, colour, addButton, removeButton])
            self.mainWidget.layout().addWidget(key, self.marker_rows, 0)
            self.mainWidget.layout().addWidget(value, self.marker_rows, 1)
            self.mainWidget.layout().addWidget(colour, self.marker_rows, 2)
            self.mainWidget.layout().addWidget(addButton, self.marker_rows, 3)
            self.mainWidget.layout().\
                addWidget(removeButton, self.marker_rows, 4)
            self.marker_rows += 1

    def set_values(self):
        self.variables["bar_plot_settings"]["user_marks_dict"] = \
            {pair[0].field.text(): pair[1].field.text() for pair in self.pairs}
        self.variables["bar_plot_settings"]["user_bar_colors_dict"] = \
            {pair[0].field.text(): pair[2].fields.currentText()
             for pair in self.pairs}
        self.accept()
