from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox, QLineEdit, QCheckBox, QDoubleSpinBox, QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox
from gui.components.FontComboBox import FontComboBox

import json
from current.default_config import defaults

class BarPlot(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(VerticalBarPopup, self).__init__(parent)
        self.setWindowTitle("Vertical Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.vars = None
        if vars:
            self.vars = vars["vert_bar_settings"]
        self.defaults = defaults["vert_bar_settings"]


        self.apply_status = LabelledCheckbox(self, text="Apply Status")
        self.meas_bar_colour = ColourBox(self, text="Measured Bar Colour")
        self.lost_bar_colour = ColourBox(self, text="Missing Bar Colour")
        self.unassigned_bar_colour = ColourBox(self, text="Unassigned Bar Colour")
        self.bar_width = LabelledDoubleSpinBox(self, text="Bar Width")
        self.bar_alpha = LabelledSpinBox(self, text="Bar Alpha")
        self.bar_linewidth = LabelledDoubleSpinBox(self, text="Bar Line Width")
        self.bar_threshold = LabelledCheckbox(self, "Apply Stdev Threshold")
        self.bar_threshold_colour = ColourBox(self, "Stdev Threshold Colour")
        self.bar_threshold_linewidth = LabelledSpinBox(self, text="Stdev Threshold Line Width")
        self.markProlines = LabelledCheckbox(self, text="Mark Prolines")
        self.proline_marker = LabelledLineEdit(self, text="Proline Marker")
        self.user_details = LabelledCheckbox(self, "Mark User Details")
        self.user_mark_font_size = LabelledSpinBox(self, "User Mark Font Size")
        self.colour_user_details = LabelledCheckbox(self, "Colour User Details")

        self.layout().addWidget(self.apply_status, 0, 0)
        self.layout().addWidget(self.meas_bar_colour, 1, 0)
        self.layout().addWidget(self.lost_bar_colour, 2, 0)
        self.layout().addWidget(self.unassigned_bar_colour, 3, 0)
        self.layout().addWidget(self.bar_width, 4, 0)
        self.layout().addWidget(self.bar_alpha, 5, 0)
        self.layout().addWidget(self.bar_linewidth, 6, 0)
        self.layout().addWidget(self.bar_threshold, 0, 1)
        self.layout().addWidget(self.bar_threshold_linewidth, 1, 1)
        self.layout().addWidget(self.bar_threshold_colour, 2, 1)
        self.layout().addWidget(self.markProlines, 3, 1)
        self.layout().addWidget(self.proline_marker, 4, 1)
        self.layout().addWidget(self.user_details, 5, 1)
        self.layout().addWidget(self.user_mark_font_size, 6, 1)
        self.layout().addWidget(self.colour_user_details, 7, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 2, 1, 2)

        if vars:
            self.get_values()

        # self.set_defaults()

    def get_defaults(self):
        self.bar_cols.field.setValue(self.defaults["vert_bar_cols_page"])
        self.bar_rows.field.setValue(self.defaults["vert_bar_rows_page"])
        self.apply_status.checkBox.setChecked(self.defaults["vert_bar_apply_status_2_bar_color"])
        self.meas_bar_colour.select(self.defaults["vert_bar_color_measured"])
        self.lost_bar_colour.select(self.defaults["vert_bar_color_lost"])
        self.unassigned_bar_colour.select(self.defaults["vert_bar_color_unassigned"])
        self.bar_width.field.setValue(self.defaults["vert_bar_bar_width"])
        self.bar_alpha.field.setValue(self.defaults["vert_bar_bar_alpha"])
        self.bar_linewidth.field.setValue(self.defaults["vert_bar_bar_linewidth"])
        self.bar_title_y.field.setValue(self.defaults["vert_bar_title_y"])
        self.bar_title_font.select(self.defaults["vert_bar_title_fn"])
        self.bar_title_font_size.field.setValue(self.defaults["vert_bar_title_fs"])
        self.bar_threshold.checkBox.setChecked(self.defaults["vert_bar_plot_threshold"])
        self.bar_threshold_colour.select(self.defaults["vert_bar_plot_threshold_color"])
        self.bar_threshold_linewidth.field.setValue(self.defaults["vert_bar_plot_threshold_lw"])
        self.x_label_font.select(self.defaults["vert_bar_x_label_fn"])
        self.x_label_font_size.field.setValue(self.defaults["vert_bar_x_label_fs"])
        self.x_label_font_weight.field.setText(self.defaults["vert_bar_x_label_weight"])
        self.x_label_padding.field.setValue(self.defaults["vert_bar_x_label_pad"])

        self.y_label_font.select(self.defaults["vert_bar_y_label_fn"])
        self.y_label_font_size.field.setValue(self.defaults["vert_bar_y_label_fs"])
        self.y_label_font_weight.field.setText(self.defaults["vert_bar_y_label_weight"])
        self.y_label_padding.field.setValue(self.defaults["vert_bar_y_label_pad"])
        self.y_tick_rotation.field.setValue(self.defaults["vert_bar_y_label_rot"])

        self.x_tick_font_size.field.setValue(self.defaults["vert_bar_x_ticks_fs"])
        self.x_tick_font.select(self.defaults["vert_bar_x_ticks_fn"])
        self.x_tick_padding.field.setValue(self.defaults["vert_bar_x_ticks_pad"])
        self.x_tick_length.field.setValue(self.defaults["vert_bar_x_ticks_len"])


        self.y_tick_font_size.field.setValue(self.defaults["vert_bar_y_ticks_fs"])
        self.y_tick_padding.field.setValue(self.defaults["vert_bar_y_ticks_pad"])
        self.y_tick_rotation.field.setValue(self.defaults["vert_bar_y_ticks_rot"])
        self.y_tick_font.select(self.defaults["vert_bar_y_ticks_fn"])
        self.x_grid_colour.select(self.defaults["vert_bar_x_grid_color"])


        self.markProlines.checkBox.setChecked(self.defaults["vert_bar_mark_prolines"])
        self.proline_marker.field.setText(self.defaults["vert_bar_proline_mark"])
        self.user_details.checkBox.setChecked(self.defaults["vert_bar_mark_user_details"])
        self.user_mark_font_size.field.setValue(self.defaults["vert_bar_mark_fs"])


    def get_values(self):
        self.bar_cols.field.setValue(self.vars["vert_bar_cols_page"])
        self.bar_rows.field.setValue(self.vars["vert_bar_rows_page"])
        self.apply_status.checkBox.setChecked(self.vars["vert_bar_apply_status_2_bar_color"])
        self.meas_bar_colour.select(self.vars["vert_bar_color_measured"])
        self.lost_bar_colour.select(self.vars["vert_bar_color_lost"])
        self.unassigned_bar_colour.select(self.vars["vert_bar_color_unassigned"])
        self.bar_width.field.setValue(self.vars["vert_bar_bar_width"])
        self.bar_alpha.field.setValue(self.vars["vert_bar_bar_alpha"])
        self.bar_linewidth.field.setValue(self.vars["vert_bar_bar_linewidth"])
        self.bar_title_y.field.setValue(self.vars["vert_bar_title_y"])
        self.bar_title_font.select(self.vars["vert_bar_title_fn"])
        self.bar_title_font_size.field.setValue(self.vars["vert_bar_title_fs"])
        self.bar_threshold.checkBox.setChecked(self.vars["vert_bar_plot_threshold"])
        self.bar_threshold_colour.select(self.vars["vert_bar_plot_threshold_color"])
        self.bar_threshold_linewidth.field.setValue(self.vars["vert_bar_plot_threshold_lw"])
        self.x_label_font.select(self.vars["vert_bar_x_label_fn"])
        self.x_label_font_size.field.setValue(self.vars["vert_bar_x_label_fs"])
        self.x_label_font_weight.field.setText(self.vars["vert_bar_x_label_weight"])
        self.x_label_padding.field.setValue(self.vars["vert_bar_x_label_pad"])

        self.y_label_font.select(self.vars["vert_bar_y_label_fn"])
        self.y_label_font_size.field.setValue(self.vars["vert_bar_y_label_fs"])
        self.y_label_font_weight.field.setText(self.vars["vert_bar_y_label_weight"])
        self.y_label_padding.field.setValue(self.vars["vert_bar_y_label_pad"])
        self.y_tick_rotation.field.setValue(self.vars["vert_bar_y_label_rot"])

        self.x_tick_font_size.field.setValue(self.vars["vert_bar_x_ticks_fs"])
        self.x_tick_font.select(self.vars["vert_bar_x_ticks_fn"])
        self.x_tick_padding.field.setValue(self.vars["vert_bar_x_ticks_pad"])
        self.x_tick_length.field.setValue(self.vars["vert_bar_x_ticks_len"])


        self.y_tick_font_size.field.setValue(self.vars["vert_bar_y_ticks_fs"])
        self.y_tick_padding.field.setValue(self.vars["vert_bar_y_ticks_pad"])
        self.y_tick_rotation.field.setValue(self.vars["vert_bar_y_ticks_rot"])
        self.y_tick_font.select(self.vars["vert_bar_y_ticks_fn"])
        self.x_grid_colour.select(self.vars["vert_bar_x_grid_color"])


        self.markProlines.checkBox.setChecked(self.vars["vert_bar_mark_prolines"])
        self.proline_marker.field.setText(self.vars["vert_bar_proline_mark"])
        self.user_details.checkBox.setChecked(self.vars["vert_bar_mark_user_details"])
        self.user_mark_font_size.field.setValue(self.vars["vert_bar_mark_fs"])

    def set_values(self):
        self.vars["vert_bar_cols_page"] = self.bar_cols.field.value()
        self.vars["vert_bar_rows_page"] = self.bar_rows.field.value()
        self.vars["vert_bar_color_measured"] = self.meas_bar_colour.fields.currentText()
        self.vars["vert_bar_apply_status_2_bar_color"] = self.apply_status.checkBox.isChecked()
        self.vars["vert_bar_color_lost"] = self.lost_bar_colour.fields.currentText()
        self.vars["vert_bar_color_unassigned"] = self.unassigned_bar_colour.fields.currentText()
        self.vars["vert_bar_bar_width"] = self.bar_width.field.value()
        self.vars["vert_bar_bar_alpha"] = self.bar_alpha.field.value()
        self.vars["vert_bar_bar_linewidth"] = self.bar_linewidth.field.value()
        self.vars["vert_bar_title_y"] = self.bar_title_y.field.value()
        self.vars["vert_bar_title_fn"] = self.bar_title_font.fields.currentText()
        self.vars["vert_bar_title_fs"] = self.bar_title_font_size.field.value()
        self.vars["vert_bar_plot_threshold"] = self.bar_threshold.checkBox.isChecked()
        self.vars["vert_bar_plot_threshold_color"] = self.bar_threshold_colour.fields.currentText()
        self.vars["vert_bar_plot_threshold_lw"] = self.bar_threshold_linewidth.field.value()
        self.vars["vert_bar_x_label_fn"] = self.x_label_font.fields.currentText()
        self.vars["vert_bar_x_label_fs"] = self.x_label_font_size.field.value()
        self.vars["vert_bar_x_label_pad"] = self.x_label_padding.field.value()
        self.vars["vert_bar_x_label_weight"] = self.x_label_font_weight.field.text()
        self.vars["vert_bar_x_ticks_fn"] = self.x_tick_font.fields.currentText()
        self.vars["vert_bar_x_ticks_fs"] = self.x_tick_font_size.field.value()
        self.vars["vert_bar_y_ticks_rot"] = self.y_tick_rotation.field.value()
        self.vars["vert_bar_x_ticks_pad"] = self.x_tick_padding.field.value()
        self.vars["vert_bar_y_label_fn"] = self.y_label_font.fields.currentText()
        self.vars["vert_bar_y_label_weight"] = self.y_label_font_weight.field.text()
        self.vars["vert_bar_y_label_fs"] = self.y_label_font_size.field.value()
        self.vars["vert_bar_y_label_pad"] = self.y_label_padding.field.value()
        self.vars["vert_bar_y_ticks_fs"] = self.y_tick_font_size.field.value()
        self.vars["vert_bar_y_ticks_pad"] = self.y_tick_padding.field.value()
        self.vars["vert_bar_x_ticks_len"] = self.x_tick_length.field.value()
        self.vars["vert_bar_x_grid_color"] = self.x_grid_colour.fields.currentText()
        self.vars["vert_bar_mark_prolines"] = self.markProlines.checkBox.isChecked()
        self.vars["vert_bar_proline_mark"] = self.proline_marker.field.text()
        self.vars["vert_bar_mark_user_details"] = self.user_details.checkBox.isChecked()
        self.vars["vert_bar_mark_fs"] = self.user_mark_font_size.field.value()
        vars["vert_bar_settings"] = self.vars
        self.accept()
