from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QPushButton
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox

from gui.popups.UserMarksPopup import UserMarksPopup

from current06.default_config import defaults
from functools import partial

class BarPlotPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(BarPlotPopup, self).__init__(parent)
        self.setWindowTitle("Vertical Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.variables = None
        if variables:
            self.variables = variables["bar_plot_settings"]
            # self.user_variables = variables["user_mark_settings"]
        self.defaults = defaults["bar_plot_settings"]


        self.apply_status = LabelledCheckbox(self, text="Apply Status")
        self.meas_bar_colour = ColourBox(self, text="Measured Bar Colour")
        self.lost_bar_colour = ColourBox(self, text="Missing Bar Colour")
        self.unassigned_bar_colour = ColourBox(self, text="Unassigned Bar Colour")
        self.bar_width = LabelledDoubleSpinBox(self, text="Bar Width")
        self.bar_alpha = LabelledDoubleSpinBox(self, text="Bar Alpha")
        self.bar_linewidth = LabelledDoubleSpinBox(self, text="Bar Line Width")
        self.bar_threshold = LabelledCheckbox(self, "Apply Stdev Threshold")
        self.bar_threshold_colour = ColourBox(self, "Stdev Threshold Colour")
        self.bar_threshold_alpha = LabelledDoubleSpinBox(self, "Stdev Threshold Alpha")
        self.bar_threshold_linewidth = LabelledDoubleSpinBox(self, text="Stdev Threshold Line Width")
        self.markProlines = LabelledCheckbox(self, text="Mark Prolines")
        self.proline_marker = LabelledLineEdit(self, text="Proline Marker")
        self.user_details = LabelledCheckbox(self, "Mark User Details")
        self.user_mark_font_size = LabelledSpinBox(self, "User Mark Font Size")
        self.colour_user_details = LabelledCheckbox(self, "Colour User Details")
        self.user_markers_button = QPushButton("User Defined Markers", self)
        self.user_markers_button.clicked.connect(partial(self.launch_user_marker_popup, variables))


        self.layout().addWidget(self.apply_status, 0, 0)
        self.layout().addWidget(self.meas_bar_colour, 1, 0)
        self.layout().addWidget(self.lost_bar_colour, 2, 0)
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
        self.layout().addWidget(self.user_mark_font_size, 6, 1)
        self.layout().addWidget(self.colour_user_details, 7, 1)
        self.layout().addWidget(self.user_markers_button, 8, 0)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 1, 1, 1)

        if variables:
            self.get_values()

        # self.set_defaults()

    def launch_user_marker_popup(self, variables):
        popup = UserMarksPopup(variables=variables)
        popup.exec_()
        popup.raise_()
        print(variables["user_mark_settings"])

    def get_defaults(self):
        self.apply_status.setChecked(self.defaults["bar_status_color_flag"])
        self.meas_bar_colour.select(self.defaults["bar_measured_color"])
        self.lost_bar_colour.select(self.defaults["bar_lost_color"])
        self.unassigned_bar_colour.select(self.defaults["bar_unassigned_color"])
        self.bar_width.setValue(self.defaults["bar_width"])
        self.bar_alpha.setValue(self.defaults["bar_alpha"])
        self.bar_linewidth.setValue(self.defaults["bar_linewidth"])
        self.bar_threshold.setChecked(self.defaults["bar_threshold_flag"])
        self.bar_threshold_colour.select(self.defaults["bar_threshold_color"])
        self.bar_threshold_linewidth.setValue(self.defaults["bar_threshold_linewidth"])
        self.bar_threshold_alpha.setValue(self.defaults["bar_threshold_alpha"])
        self.user_mark_font_size.setValue(self.defaults["bar_mark_fontsize"])
        self.markProlines.setChecked(self.defaults["bar_mark_prolines_flag"])
        self.proline_marker.field.setText(self.defaults["bar_mark_prolines_symbol"])
        self.user_details.setChecked(self.defaults["bar_mark_user_details_flag"])
        self.colour_user_details.setChecked(self.defaults["bar_mark_user_details_flag"])


    def get_values(self):

        self.apply_status.setChecked(self.variables["bar_status_color_flag"])
        self.meas_bar_colour.select(self.variables["bar_measured_color"])
        self.lost_bar_colour.select(self.variables["bar_lost_color"])
        self.unassigned_bar_colour.select(self.variables["bar_unassigned_color"])
        self.bar_width.setValue(self.variables["bar_width"])
        self.bar_alpha.setValue(self.variables["bar_alpha"])
        self.bar_linewidth.setValue(self.variables["bar_linewidth"])
        self.bar_threshold.setChecked(self.variables["bar_threshold_flag"])
        self.bar_threshold_colour.select(self.variables["bar_threshold_color"])
        self.bar_threshold_alpha.setValue(self.variables["bar_threshold_alpha"])
        self.bar_threshold_linewidth.setValue(self.variables["bar_threshold_linewidth"])
        self.user_mark_font_size.setValue(self.variables["bar_mark_fontsize"])
        self.markProlines.setChecked(self.variables["bar_mark_prolines_flag"])
        self.proline_marker.field.setText(self.variables["bar_mark_prolines_symbol"])
        self.user_details.setChecked(self.variables["bar_mark_user_details_flag"])
        self.colour_user_details.setChecked(self.variables["bar_mark_user_details_flag"])

    def set_values(self, variables):

        self.variables["bar_status_color_flag"] = self.apply_status.checkBox.isChecked()
        self.variables["bar_measured_color"] = str(self.meas_bar_colour.fields.currentText())
        self.variables["bar_lost_color"] = str(self.lost_bar_colour.fields.currentText())
        self.variables["bar_unassigned_color"] = self.unassigned_bar_colour.fields.currentText()
        self.variables["bar_width"] = self.bar_width.field.value()
        self.variables["bar_alpha"] = self.bar_alpha.field.value()
        self.variables["bar_linewidth"] = self.bar_linewidth.field.value()
        self.variables["bar_threshold_flag"] = self.bar_threshold.checkBox.isChecked()
        self.variables["bar_threshold_color"] = str(self.bar_threshold_colour.fields.currentText())
        self.variables["bar_threshold_linewidth"] = self.bar_threshold_linewidth.field.value()
        self.variables["bar_threshold_alpha"] = self.bar_threshold_alpha.field.value()
        self.variables["bar_mark_fontsize"] = self.user_mark_font_size.field.value()
        self.variables["bar_mark_prolines_flag"] = self.markProlines.checkBox.isChecked()
        self.variables["bar_mark_prolines_symbol"] = str(self.proline_marker.field.text())
        self.variables["bar_mark_user_details_flag"] = self.user_details.checkBox.isChecked()
        self.variables["bar_mark_user_details_flag"] = self.colour_user_details.checkBox.isChecked()
        variables["bar_plot_settings"] = self.variables
        self.accept()
