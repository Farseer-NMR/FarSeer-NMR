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
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton

from gui.components.ColourBox import ColourBox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.popups.BasePopup import BasePopup
from gui.popups.UserMarksPopup import UserMarksPopup


class BarPlotPopup(BasePopup):
    """
    A popup for setting Bar Plot specific settings in the Farseer-NMR
    configuration.

    Parameters:
        parent(QWidget): parent widget for popup.

    Methods:
        .launch_user_marker_popup
        .get_defaults()
        .get_values()
        .set_values()
    """
    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, "bar_plot_settings", "Bar Plot")
        self.meas_bar_colour = ColourBox(self, text="Measured Bar Colour")
        self.apply_status = LabelledCheckbox(self, text="Apply Peak Status")
        self.missing_bar_colour = ColourBox(self, text="Missing Bar Colour")
        self.unassigned_bar_colour = ColourBox(self, text="Unassigned Bar Colour")
        self.bar_width = LabelledDoubleSpinBox(
            self,
            text="Bar Width",
            minimum=0,
            maximum=1,
            step=0.1
            )
        self.bar_alpha = LabelledDoubleSpinBox(
            self,
            text="Bar Transparency",
            minimum=0,
            maximum=1,
            step=0.1
            )
        self.bar_linewidth = LabelledDoubleSpinBox(
            self,
            text="Bar Line Width",
            minimum=0,
            step=0.1
            )
        self.bar_threshold = LabelledCheckbox(self, "Apply Stdev Threshold")
        self.bar_threshold_colour = ColourBox(self, "Stdev Threshold Colour")
        self.bar_threshold_alpha = LabelledDoubleSpinBox(
            self,
            "Stdev Threshold Alpha",
            minimum=0,
            maximum=1,
            step=0.1
            )
        self.bar_threshold_linewidth = LabelledDoubleSpinBox(
            self,
            text="Stdev Threshold Line Width",
            minimum=0,
            step=0.1
            )
        self.user_mark_font_size = LabelledSpinBox(self, "Mark Font Size", minimum=0, step=1)
        self.markProlines = LabelledCheckbox(self, text="Mark Prolines")
        self.proline_marker = LabelledLineEdit(self, text="Proline Marker")
        self.user_details = LabelledCheckbox(self, "Mark User Details")
        self.colour_user_details = LabelledCheckbox(self, "Colour User Details")
        self.user_markers_button = QPushButton("User Defined Markers", self)
        self.user_markers_button.clicked.connect(self.launch_user_marker_popup)
        self.layout().addWidget(self.apply_status, 0, 0)
        self.layout().addWidget(self.meas_bar_colour, 1, 0)
        self.layout().addWidget(self.missing_bar_colour, 2, 0)
        self.layout().addWidget(self.unassigned_bar_colour, 3, 0)
        self.layout().addWidget(self.bar_width, 4, 0)
        self.layout().addWidget(self.bar_alpha, 5, 0)
        self.layout().addWidget(self.bar_linewidth, 6, 0)
        self.layout().addWidget(self.bar_threshold, 7, 0)
        self.layout().addWidget(self.bar_threshold_linewidth, 0, 1)
        self.layout().addWidget(self.bar_threshold_colour, 1, 1)
        self.layout().addWidget(self.bar_threshold_alpha, 2, 1)
        self.layout().addWidget(self.markProlines, 3, 1)
        self.layout().addWidget(self.proline_marker, 4, 1)
        self.layout().addWidget(self.user_details, 5, 1)
        self.layout().addWidget(self.colour_user_details, 6, 1)
        self.layout().addWidget(self.user_markers_button, 7, 1)
        self.layout().addWidget(self.user_mark_font_size, 8, 1)
        # add OK CANCEL RESTORE buttons
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel |
            QDialogButtonBox.RestoreDefaults)
        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)
        self.layout().addWidget(self.buttonBox, 9, 1, 1, 1)
        self.get_values()

    def launch_user_marker_popup(self):
        UserMarksPopup(variables=self.local_variables["user_marks_dict"]).launch()

    def get_defaults(self):
        # check boxes
        self.apply_status.setChecked(self.defaults["status_color_flag"])
        self.bar_threshold.setChecked(self.defaults["threshold_flag"])
        self.markProlines.setChecked(self.defaults["mark_prolines_flag"])
        self.user_details.setChecked(self.defaults["mark_user_details_flag"])
        self.colour_user_details.setChecked(self.defaults["color_user_details_flag"])
        # colours
        self.meas_bar_colour.get_colour(self.defaults["measured_color"])
        self.missing_bar_colour.get_colour(self.defaults["missing_color"])
        self.unassigned_bar_colour.get_colour(self.defaults["unassigned_color"])
        self.bar_threshold_colour.get_colour(self.defaults["threshold_color"])
        # values
        self.bar_width.setValue(self.defaults["bar_width"])
        self.bar_alpha.setValue(self.defaults["bar_alpha"])
        self.bar_linewidth.setValue(self.defaults["bar_linewidth"])
        self.bar_threshold_linewidth.setValue(self.defaults["threshold_linewidth"])
        self.bar_threshold_alpha.setValue(self.defaults["threshold_alpha"])
        self.user_mark_font_size.setValue(self.defaults["mark_fontsize"])
        # text
        self.proline_marker.field.setText(self.defaults["mark_prolines_symbol"])
    
    def get_values(self):
        # check boxes
        self.apply_status.setChecked(self.local_variables["status_color_flag"])
        self.bar_threshold.setChecked(self.local_variables["threshold_flag"])
        self.markProlines.setChecked(self.local_variables["mark_prolines_flag"])
        self.user_details.setChecked(self.local_variables["mark_user_details_flag"])
        self.colour_user_details.setChecked(self.local_variables["color_user_details_flag"])
        # colours
        self.meas_bar_colour.get_colour(self.local_variables["measured_color"])
        self.missing_bar_colour.get_colour(self.local_variables["missing_color"])
        self.unassigned_bar_colour.get_colour(self.local_variables["unassigned_color"])
        self.bar_threshold_colour.get_colour(self.local_variables["threshold_color"])
        # values
        self.bar_width.setValue(self.local_variables["bar_width"])
        self.bar_alpha.setValue(self.local_variables["bar_alpha"])
        self.bar_linewidth.setValue(self.local_variables["bar_linewidth"])
        self.bar_threshold_alpha.setValue(self.local_variables["threshold_alpha"])
        self.bar_threshold_linewidth.setValue(self.local_variables["threshold_linewidth"])
        self.user_mark_font_size.setValue(self.local_variables["mark_fontsize"])
        # text
        self.proline_marker.field.setText(self.local_variables["mark_prolines_symbol"])
        
    
    def set_values(self):
        # check boxes
        self.local_variables["status_color_flag"] = self.apply_status.isChecked()
        self.local_variables["threshold_flag"] = self.bar_threshold.isChecked()
        self.local_variables["mark_prolines_flag"] = self.markProlines.isChecked()
        self.local_variables["mark_user_details_flag"] = self.user_details.isChecked()
        self.local_variables["color_user_details_flag"] = self.colour_user_details.isChecked()
        # colours
        self.local_variables["measured_color"] = self.meas_bar_colour.fields.currentText()
        self.local_variables["missing_color"] = self.missing_bar_colour.fields.currentText()
        self.local_variables["unassigned_color"] = self.unassigned_bar_colour.fields.currentText()
        self.local_variables["threshold_color"] = self.bar_threshold_colour.fields.currentText()
        # values
        self.local_variables["bar_width"] = self.bar_width.field.value()
        self.local_variables["bar_alpha"] = self.bar_alpha.field.value()
        self.local_variables["bar_linewidth"] = self.bar_linewidth.field.value()
        self.local_variables["threshold_alpha"] = self.bar_threshold_alpha.field.value()
        self.local_variables["threshold_linewidth"] = self.bar_threshold_linewidth.field.value()
        self.local_variables["mark_fontsize"] = self.user_mark_font_size.field.value()
        # text
        self.local_variables["mark_prolines_symbol"] = str(self.proline_marker.field.text())
        #
        self.accept()
