from PyQt5.QtWidgets import QDialogButtonBox, QPushButton

from gui.components.ColourBox import ColourBox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.popups.BasePopup import BasePopup
from gui.popups.UserMarksPopup import UserMarksPopup


class BarPlotPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, "bar_plot_settings", "Bar Plot")

        self.meas_bar_colour = ColourBox(self, text="Measured Bar Colour")
        self.apply_status = LabelledCheckbox(self, text="Apply Peak Status")
        self.lost_bar_colour = ColourBox(self, text="Lost Bar Colour")
        self.unassigned_bar_colour = ColourBox(self, text="Unassigned Bar Colour")
        self.bar_width = LabelledDoubleSpinBox(self, text="Bar Width", min=0, max=1, step=0.1)
        self.bar_alpha = LabelledDoubleSpinBox(self, text="Bar Transparency", min=0, max=1, step=0.1)
        self.bar_linewidth = LabelledDoubleSpinBox(self, text="Bar Line Width", min=0, step=0.1)
        self.bar_threshold = LabelledCheckbox(self, "Apply Stdev Threshold")
        self.bar_threshold_colour = ColourBox(self, "Stdev Threshold Colour")
        self.bar_threshold_alpha = LabelledDoubleSpinBox(self, "Stdev Threshold Alpha", min=0, max=1, step=0.1)
        self.bar_threshold_linewidth = LabelledDoubleSpinBox(self, text="Stdev Threshold Line Width", min=0, step=0.1)
        self.user_mark_font_size = LabelledSpinBox(self, "Mark Font Size", min=0, step=1)
        self.markProlines = LabelledCheckbox(self, text="Mark Prolines")
        self.proline_marker = LabelledLineEdit(self, text="Proline Marker")
        self.user_details = LabelledCheckbox(self, "Mark User Details")
        self.colour_user_details = LabelledCheckbox(self, "Colour User Details")
        self.user_markers_button = QPushButton("User Defined Markers", self)
        self.user_markers_button.clicked.connect(self.launch_user_marker_popup)


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
        self.layout().addWidget(self.colour_user_details, 6, 1)
        self.layout().addWidget(self.user_markers_button, 7, 1)
        self.layout().addWidget(self.user_mark_font_size, 8, 1)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)
        self.layout().addWidget(self.buttonBox, 9, 1, 1, 1)
        self.get_values()

    def launch_user_marker_popup(self):
        UserMarksPopup(variables=self.local_variables["user_marks_dict"]).launch()

    def get_defaults(self):
        self.apply_status.setChecked(self.defaults["status_color_flag"])
        self.meas_bar_colour.select(self.defaults["measured_color"])
        self.lost_bar_colour.select(self.defaults["lost_color"])
        self.unassigned_bar_colour.select(self.defaults["unassigned_color"])
        self.bar_width.setValue(self.defaults["bar_width"])
        self.bar_alpha.setValue(self.defaults["bar_alpha"])
        self.bar_linewidth.setValue(self.defaults["bar_linewidth"])
        self.bar_threshold.setChecked(self.defaults["threshold_flag"])
        self.bar_threshold_colour.select(self.defaults["threshold_color"])
        self.bar_threshold_linewidth.setValue(self.defaults["threshold_linewidth"])
        self.bar_threshold_alpha.setValue(self.defaults["threshold_alpha"])
        self.user_mark_font_size.setValue(self.defaults["mark_fontsize"])
        self.markProlines.setChecked(self.defaults["mark_prolines_flag"])
        self.proline_marker.field.setText(self.defaults["mark_prolines_symbol"])
        self.user_details.setChecked(self.defaults["mark_user_details_flag"])
        self.colour_user_details.setChecked(self.defaults["color_user_details_flag"])


    def get_values(self):

        self.apply_status.setChecked(self.local_variables["status_color_flag"])
        self.meas_bar_colour.select(self.local_variables["measured_color"])
        self.lost_bar_colour.select(self.local_variables["lost_color"])
        self.unassigned_bar_colour.select(self.local_variables["unassigned_color"])
        self.bar_width.setValue(self.local_variables["bar_width"])
        self.bar_alpha.setValue(self.local_variables["bar_alpha"])
        self.bar_linewidth.setValue(self.local_variables["bar_linewidth"])
        self.bar_threshold.setChecked(self.local_variables["threshold_flag"])
        self.bar_threshold_colour.select(self.local_variables["threshold_color"])
        self.bar_threshold_alpha.setValue(self.local_variables["threshold_alpha"])
        self.bar_threshold_linewidth.setValue(self.local_variables["threshold_linewidth"])
        self.user_mark_font_size.setValue(self.local_variables["mark_fontsize"])
        self.markProlines.setChecked(self.local_variables["mark_prolines_flag"])
        self.proline_marker.field.setText(self.local_variables["mark_prolines_symbol"])
        self.user_details.setChecked(self.local_variables["mark_user_details_flag"])
        self.colour_user_details.setChecked(self.local_variables["color_user_details_flag"])

    def set_values(self):

        self.local_variables["status_color_flag"] = self.apply_status.checkBox.isChecked()
        self.local_variables["measured_color"] = str(self.meas_bar_colour.fields.currentText())
        self.local_variables["lost_color"] = str(self.lost_bar_colour.fields.currentText())
        self.local_variables["unassigned_color"] = self.unassigned_bar_colour.fields.currentText()
        self.local_variables["bar_width"] = self.bar_width.field.value()
        self.local_variables["bar_alpha"] = self.bar_alpha.field.value()
        self.local_variables["bar_linewidth"] = self.bar_linewidth.field.value()
        self.local_variables["threshold_flag"] = self.bar_threshold.checkBox.isChecked()
        self.local_variables["threshold_color"] = str(self.bar_threshold_colour.fields.currentText())
        self.local_variables["threshold_linewidth"] = self.bar_threshold_linewidth.field.value()
        self.local_variables["threshold_alpha"] = self.bar_threshold_alpha.field.value()
        self.local_variables["mark_fontsize"] = self.user_mark_font_size.field.value()
        self.local_variables["mark_prolines_flag"] = self.markProlines.checkBox.isChecked()
        self.local_variables["mark_prolines_symbol"] = str(self.proline_marker.field.text())
        self.local_variables["mark_user_details_flag"] = self.user_details.checkBox.isChecked()
        self.local_variables["color_user_details_flag"] = self.colour_user_details.checkBox.isChecked()
        self.accept()
