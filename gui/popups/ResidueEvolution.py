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

class ResidueEvolutionPopup(QDialog):

    def __init__(self, parent=None, vars=None, **kw):
        super(ResidueEvolutionPopup, self).__init__(parent)
        self.setWindowTitle("Residue Evolution Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)
        self.vars = None
        if vars:
            self.vars = vars["res_evo_settings"]
        self.default = defaults["res_evo_settings"]

        self.res_evo_cols = LabelledSpinBox(self, text="Columns Per Page")
        self.res_evo_rows = LabelledSpinBox(self, text="Rows Per Page")
        self.res_evo_set_x_values = LabelledCheckbox(self, "Use User Defined X Values?")
        self.res_evo_x_ticks_nbins = LabelledSpinBox(self, text="Number of Ticks")
        self.res_evo_x_label = LabelledLineEdit(self, text="X Label")
        self.res_evo_plot_line_style = LabelledCombobox(self, text="Plot Line Style", items=['-', '--', '-.', ':'])
        self.res_evo_plot_line_width = LabelledSpinBox(self, 'Line Width')
        self.res_evo_line_color = ColourBox(self, text='Marker Colour')
        self.res_evo_plot_marker_style = LabelledCombobox(self, text="Plot Line Style", items=['-', '--', '-.', ':', 'o'])
        self.res_evo_plot_marker_size = LabelledSpinBox(self, 'Marker Size')
        self.res_evo_plot_fill_between = LabelledCheckbox(self, text="Draw Data Shade")
        self.res_evo_plot_fill_colour = ColourBox(self, text="Shade Colour")
        self.res_evo_fill_alpha = LabelledSpinBox(self, text="Shade Transparency")
        self.res_evo_fit_line_colour = ColourBox(self, text="Fit Line Colour")
        self.res_evo_fit_line_width = LabelledSpinBox(self, text="Fit Line Width")
        self.res_evo_fit_line_style = LabelledSpinBox(self, text="Fit Line Style")

        self.layout().addWidget(self.res_evo_cols, 0, 0)
        self.layout().addWidget(self.res_evo_rows, 1, 0)
        self.layout().addWidget(self.res_evo_set_x_values, 2, 0)
        self.layout().addWidget(self.res_evo_x_ticks_nbins, 3, 0)
        self.layout().addWidget(self.res_evo_x_label, 4, 0)
        self.layout().addWidget(self.res_evo_plot_line_style, 5, 0)
        self.layout().addWidget(self.res_evo_plot_line_width, 6, 0)
        self.layout().addWidget(self.res_evo_line_color, 7, 0)
        self.layout().addWidget(self.res_evo_plot_marker_style, 0, 1)
        self.layout().addWidget(self.res_evo_plot_marker_size, 1, 1)
        self.layout().addWidget(self.res_evo_plot_fill_between, 2, 1)
        self.layout().addWidget(self.res_evo_plot_fill_colour, 3, 1)
        self.layout().addWidget(self.res_evo_fill_alpha, 4, 1)
        self.layout().addWidget(self.res_evo_fit_line_colour, 5, 1)
        self.layout().addWidget(self.res_evo_fit_line_width, 6, 1)
        self.layout().addWidget(self.res_evo_fit_line_style, 7, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 0, 1, 2)

        if vars:
            self.get_values()

    def get_defaults(self):
        self.res_evo_cols.field.setValue(self.default["res_evo_cols_page"])
        self.res_evo_rows.field.setValue(self.default["res_evo_rows_page"])
        self.set_x_values.checkBox.setChecked(self.default["res_evo_set_x_values"])
        self.res_evo_x_ticks_nbins.field.setValue(self.default["res_evo_x_ticks_nbins"])
        self.res_evo_x_label.field.setText(self.default["res_evo_x_label"])
        self.res_evo_plot_line_style.select(self.default["res_evo_plot_line_style"])
        self.res_evo_plot_line_width.field.setValue(self.default["res_evo_plot_line_width"])
        self.res_evo_line_color.field.select(self.default["res_evo_line_color"])
        self.res_evo_plot_marker_style.select(self.default["res_evo_plot_marker_style"])
        self.res_evo_plot_marker_size.field.setValue(self.default["res_evo_plot_marker_size"])
        self.res_evo_plot_fill_between.checkBox.setChecked(self.default["res_evo_fill_between"])
        self.res_evo_plot_fill_colour.select(self.default["res_evo_fill_color"])
        self.res_evo_fill_alpha.field.setValue(self.default["res_evo_fill_alpha"])
        self.res_evo_fit_line_colour.select(self.default["res_evo_fit_line_color"])
        self.res_evo_fit_line_width.field.setValue(self.default["res_evo_fit_line_width"])
        self.res_evo_fit_line_style.field.select(self.default["res_evo_fit_line_style"])

    def set_values(self):
        self.vars["res_evo_cols_page"] = self.res_evo_cols.field.value()
        self.vars["res_evo_rows_page"] = self.res_evo_rows.field.value()
        self.vars["res_evo_set_x_values"] = self.set_x_values.checkBox.isChecked()
        self.vars["res_evo_x_ticks_nbins"] = self.res_evo_x_ticks_nbins.field.value()
        self.vars["res_evo_x_label"] = self.res_evo_x_label.field.text()
        self.vars["res_evo_plot_line_style"] = self.res_evo_plot_line_style.currentText()
        self.vars["res_evo_plot_line_width"] = self.res_evo_plot_line_width.field.value()
        self.vars["res_evo_line_color"] = self.res_evo_line_color.field.currentText()
        self.vars["res_evo_plot_marker_style"] = self.res_evo_plot_marker_style.currentText()
        self.vars["res_evo_plot_marker_size"] = self.res_evo_plot_marker_size.field.value()
        self.vars["res_evo_fill_between"] = self.res_evo_plot_fill_between.checkBox.isChecked()
        self.vars["res_evo_fill_color"] = self.res_evo_plot_fill_colour.currentText()
        self.vars["res_evo_fill_alpha"] = self.res_evo_fill_alpha.field.value()
        self.vars["res_evo_fit_line_color"] = self.res_evo_fit_line_colour.currentText()
        self.vars["res_evo_fit_line_width"] = self.res_evo_fit_line_width.field.value()
        self.vars["res_evo_fit_line_style"] = self.res_evo_fit_line_style.field.currentText()
        vars["res_evo_settings"] = self.vars
        self.accept()

    def get_values(self):
        self.res_evo_cols.field.setValue(self.default["res_evo_cols_page"])
        self.res_evo_rows.field.setValue(self.default["res_evo_rows_page"])
        self.set_x_values.checkBox.setChecked(self.default["res_evo_set_x_values"])
        self.res_evo_x_ticks_nbins.field.setValue(self.default["res_evo_x_ticks_nbins"])
        self.res_evo_x_label.field.setText(self.default["res_evo_x_label"])
        self.res_evo_plot_line_style.select(self.default["res_evo_plot_line_style"])
        self.res_evo_plot_line_width.field.setValue(self.default["res_evo_plot_line_width"])
        self.res_evo_line_color.field.select(self.default["res_evo_line_color"])
        self.res_evo_plot_marker_style.select(self.default["res_evo_plot_marker_style"])
        self.res_evo_plot_marker_size.field.setValue(self.default["res_evo_plot_marker_size"])
        self.res_evo_plot_fill_between.checkBox.setChecked(self.default["res_evo_fill_between"])
        self.res_evo_plot_fill_colour.select(self.default["res_evo_fill_color"])
        self.res_evo_fill_alpha.field.setValue(self.default["res_evo_fill_alpha"])
        self.res_evo_fit_line_colour.select(self.default["res_evo_fit_line_color"])
        self.res_evo_fit_line_width.field.setValue(self.default["res_evo_fit_line_width"])
        self.res_evo_fit_line_style.field.select(self.default["res_evo_fit_line_style"])
