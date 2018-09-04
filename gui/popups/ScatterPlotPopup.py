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
import string
from PyQt5.QtWidgets import QDialogButtonBox

from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox
from gui.gui_utils import colours
from gui.popups.BasePopup import BasePopup

# https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
translator = str.maketrans('', '', string.punctuation+" ")


class ScatterPlotPopup(BasePopup):
    """
    A popup for setting Scatter Plot specific settings in the Farseer-NMR
    configuration.

    Parameters:
        parent(QWidget): parent widget for popup.

    Methods:
        .get_defaults()
        .get_values()
        .set_values()
    """
    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="Scatter Plot", settings_key=["cs_scatter_settings"])
        self.cs_scatter_cols_page = LabelledSpinBox(self, "Columns Per Page", minimum=1, step=1)
        self.cs_scatter_rows_page = LabelledSpinBox(self, "Rows Per Page", minimum=1, step=1)
        self.cs_scatter_x_label = LabelledLineEdit(self, "X Label")
        self.cs_scatter_y_label = LabelledLineEdit(self, "Y Label")
        self.cs_scatter_mksize = LabelledSpinBox(self, "Mark Size", minimum=0, step=1)
        self.cs_scatter_scale = LabelledDoubleSpinBox(self, "Scale", minimum=0, step=0.01)
        self.cs_scatter_mk_type = LabelledCombobox(
            self,
            text="Mark Type",
            items=['color', 'shape']
            )
        self.cs_scatter_mk_start_color = ColourBox(self, text="Mark Start Colour")
        self.cs_scatter_mk_end_color = ColourBox(self, text="Mark End Colour")
        self.cs_scatter_markers = LabelledLineEdit(self, "Sequential Markers")
        self.cs_scatter_mk_color = LabelledLineEdit(self, text="Mark Colours")
        self.cs_scatter_mk_missing_color = ColourBox(self, "Missing Mark Colour")
        self.cs_scatter_mk_edgecolors = LabelledLineEdit(self, "Marker Edge Colours")
        self.cs_scatter_hide_missing = LabelledCheckbox(self, "Hide Missing Data Points")
        # layout
        self.layout().addWidget(self.cs_scatter_cols_page, 0, 0)
        self.layout().addWidget(self.cs_scatter_rows_page, 1, 0)
        self.layout().addWidget(self.cs_scatter_x_label, 2, 0)
        self.layout().addWidget(self.cs_scatter_y_label, 3, 0)
        self.layout().addWidget(self.cs_scatter_mksize, 4, 0)
        self.layout().addWidget(self.cs_scatter_scale, 5, 0)
        self.layout().addWidget(self.cs_scatter_mk_type, 6, 0)
        self.layout().addWidget(self.cs_scatter_mk_start_color, 0, 1)
        self.layout().addWidget(self.cs_scatter_mk_end_color, 1, 1)
        self.layout().addWidget(self.cs_scatter_markers, 2, 1)
        self.layout().addWidget(self.cs_scatter_mk_color, 3, 1)
        self.layout().addWidget(self.cs_scatter_mk_edgecolors, 4, 1)
        self.layout().addWidget(self.cs_scatter_mk_missing_color, 5, 1)
        self.layout().addWidget(self.cs_scatter_hide_missing, 6, 1)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel |
            QDialogButtonBox.RestoreDefaults
            )
        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)
        self.layout().addWidget(self.buttonBox, 7, 0, 1, 2)
        self.get_values()

    def get_defaults(self):
        # value
        self.cs_scatter_cols_page.setValue(self.defaults["cols_page"])
        self.cs_scatter_rows_page.setValue(self.defaults["rows_page"])
        self.cs_scatter_mksize.setValue(self.defaults["mksize"])
        self.cs_scatter_scale.setValue(self.defaults["scale"])
        # text
        self.cs_scatter_x_label.field.setText(self.defaults["x_label"])
        self.cs_scatter_y_label.field.setText(self.defaults["y_label"])
        self.cs_scatter_markers.field.setText(','.join(self.defaults["markers"]))
        self.cs_scatter_mk_color.field.setText(','.join(self.defaults["mk_color"]))
        self.cs_scatter_mk_edgecolors.field.setText(','.join(self.defaults["mk_edgecolors"]))
        # dropdown
        self.cs_scatter_mk_type.select(self.defaults["mk_type"])
        # colour
        self.cs_scatter_mk_start_color.get_colour(self.defaults["mk_start_color"])
        self.cs_scatter_mk_end_color.get_colour(self.defaults["mk_end_color"])
        self.cs_scatter_mk_missing_color.get_colour(self.defaults["mk_missing_color"])
        # check
        self.cs_scatter_hide_missing.setChecked(self.defaults["hide_missing"])

    def set_values(self):
        # value
        self.local_variables["cols_page"] = self.cs_scatter_cols_page.field.value()
        self.local_variables["rows_page"] = self.cs_scatter_rows_page.field.value()
        self.local_variables["mksize"] = self.cs_scatter_mksize.field.value()
        self.local_variables["scale"] = self.cs_scatter_scale.field.value()
        # text
        self.local_variables["x_label"] = self.cs_scatter_x_label.field.text()
        self.local_variables["y_label"] = self.cs_scatter_y_label.field.text()
        self.local_variables["markers"] = \
            [x.strip().strip("'") for x in self.cs_scatter_markers.field.text().split(',')]
        # dropdown
        self.local_variables["mk_type"] = self.cs_scatter_mk_type.fields.currentText()
        # colour
        self.local_variables["mk_start_color"] = \
            colours[self.cs_scatter_mk_start_color.fields.currentText()]
        self.local_variables["mk_end_color"] = \
            colours[self.cs_scatter_mk_end_color.fields.currentText()]
        self.local_variables["mk_color"] = \
            [x.translate(translator) for x in self.cs_scatter_mk_color.field.text().split(',')]
        self.local_variables["mk_edgecolors"] = \
            [x.translate(translator) for x in self.cs_scatter_mk_edgecolors.field.text().split(',')]
        self.local_variables["mk_missing_color"] = self.cs_scatter_mk_missing_color.fields.currentText()
        # checked
        self.local_variables["hide_missing"] = self.cs_scatter_hide_missing.isChecked()
        self.accept()

    def get_values(self):
        # values
        self.cs_scatter_cols_page.setValue(self.local_variables["cols_page"])
        self.cs_scatter_rows_page.setValue(self.local_variables["rows_page"])
        self.cs_scatter_mksize.setValue(self.local_variables["mksize"])
        self.cs_scatter_scale.setValue(self.local_variables["scale"])
        # text
        self.cs_scatter_x_label.field.setText(self.local_variables["x_label"])
        self.cs_scatter_y_label.field.setText(self.local_variables["y_label"])
        self.cs_scatter_markers.field.setText(','.join(self.local_variables["markers"]))
        self.cs_scatter_mk_color.field.setText(','.join(self.local_variables["mk_color"]))
        self.cs_scatter_mk_edgecolors.field.setText(','.join(self.local_variables["mk_edgecolors"]))
        # dropdown
        self.cs_scatter_mk_type.select(self.local_variables["mk_type"])
        # colours
        self.cs_scatter_mk_start_color.get_colour(self.local_variables["mk_start_color"])
        self.cs_scatter_mk_end_color.get_colour(self.local_variables["mk_end_color"])
        self.cs_scatter_mk_missing_color.get_colour(self.local_variables["mk_missing_color"])
        # check
        self.cs_scatter_hide_missing.setChecked(self.local_variables["hide_missing"])
