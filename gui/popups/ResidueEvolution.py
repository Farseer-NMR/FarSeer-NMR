from PyQt5.QtWidgets import QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.ColourBox import ColourBox

from gui.popups.BasePopup import BasePopup

class ResidueEvolutionPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="Residue Evolution Plot",
                           settings_key=["res_evo_settings"])

        self.res_evo_cols = LabelledSpinBox(self, text="Columns Per Page", min=1, step=1)
        self.res_evo_rows = LabelledSpinBox(self, text="Rows Per Page", min=1, step=1)
        self.res_evo_set_x_values = LabelledCheckbox(self, "Use User Defined X Values?")
        self.res_evo_x_ticks_nbins = LabelledSpinBox(self, text="Number of Ticks", min=1, step=1)
        self.res_evo_x_label = LabelledLineEdit(self, text="X Label")
        self.res_evo_plot_line_style = LabelledCombobox(self, text="Plot Line Style", items=['-', '--', '-.', ':'])
        self.res_evo_plot_line_width = LabelledSpinBox(self, 'Line Width', min=0, step=1)
        self.res_evo_line_color = ColourBox(self, text='Line Colour')
        self.res_evo_plot_marker_style = LabelledCombobox(self, text="Marker Style", items=['-', '--', '-.', ':', 'o'])
        self.res_evo_plot_marker_size = LabelledSpinBox(self, 'Marker Size', min=0, step=1)
        self.res_evo_marker_color = ColourBox(self, text='Marker Colour')
        self.res_evo_plot_fill_between = LabelledCheckbox(self, text="Draw Data Shade")
        self.res_evo_plot_fill_colour = ColourBox(self, text="Shade Colour")
        self.res_evo_fill_alpha = LabelledDoubleSpinBox(self, text="Shade Transparency", min=0, max=1, step=0.1)
        self.res_evo_fit_line_colour = ColourBox(self, text="Fit Line Colour")
        self.res_evo_fit_line_width = LabelledSpinBox(self, text="Fit Line Width", min=0, step=1)
        self.res_evo_fit_line_style = LabelledCombobox(self, text="Fit Line Style", items=['-', '--', '-.', ':', 'o'])

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
        self.layout().addWidget(self.res_evo_marker_color, 2, 1)
        self.layout().addWidget(self.res_evo_plot_fill_between, 3, 1)
        self.layout().addWidget(self.res_evo_plot_fill_colour, 4, 1)
        self.layout().addWidget(self.res_evo_fill_alpha, 5, 1)
        self.layout().addWidget(self.res_evo_fit_line_colour, 6, 1)
        self.layout().addWidget(self.res_evo_fit_line_width, 7, 1)
        self.layout().addWidget(self.res_evo_fit_line_style, 8, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 9, 0, 1, 2)

        self.get_values()

    def get_defaults(self):
        self.res_evo_cols.setValue(self.default["cols_page"])
        self.res_evo_rows.setValue(self.default["rows_page"])
        self.res_evo_set_x_values.setChecked(self.default["set_x_values"])
        self.res_evo_x_ticks_nbins.setValue(self.default["x_ticks_nbins"])
        self.res_evo_x_label.field.setText(self.default["x_label"])
        self.res_evo_plot_line_style.select(self.default["line_style"])
        self.res_evo_plot_line_width.setValue(self.default["line_width"])
        self.res_evo_line_color.select(self.default["line_color"])
        self.res_evo_marker_color.select(self.default["marker_color"])
        self.res_evo_plot_marker_style.select(self.default["marker_style"])
        self.res_evo_plot_marker_size.setValue(self.default["marker_size"])
        self.res_evo_plot_fill_between.setChecked(self.default["fill_between"])
        self.res_evo_plot_fill_colour.select(self.default["fill_color"])
        self.res_evo_fill_alpha.setValue(self.default["fill_alpha"])
        self.res_evo_fit_line_colour.select(self.default["fit_line_color"])
        self.res_evo_fit_line_width.setValue(self.default["fit_line_width"])
        self.res_evo_fit_line_style.select(self.default["fit_line_style"])

    def set_values(self):
        self.local_variables["cols_page"] = self.res_evo_cols.field.value()
        self.local_variables["rows_page"] = self.res_evo_rows.field.value()
        self.local_variables["set_x_values"] = self.res_evo_set_x_values.checkBox.isChecked()
        self.local_variables["x_ticks_nbins"] = self.res_evo_x_ticks_nbins.field.value()
        self.local_variables["x_label"] = self.res_evo_x_label.field.text()
        self.local_variables["line_style"] = self.res_evo_plot_line_style.fields.currentText()
        self.local_variables["line_width"] = self.res_evo_plot_line_width.field.value()
        self.local_variables["line_color"] = self.res_evo_line_color.fields.currentText()
        self.local_variables["marker_color"] = self.res_evo_marker_color.fields.currentText()
        self.local_variables["marker_style"] = self.res_evo_plot_marker_style.fields.currentText()
        self.local_variables["marker_size"] = self.res_evo_plot_marker_size.field.value()
        self.local_variables["fill_between"] = self.res_evo_plot_fill_between.checkBox.isChecked()
        self.local_variables["fill_color"] = self.res_evo_plot_fill_colour.fields.currentText()
        self.local_variables["fill_alpha"] = self.res_evo_fill_alpha.field.value()
        self.local_variables["fit_line_color"] = self.res_evo_fit_line_colour.fields.currentText()
        self.local_variables["fit_line_width"] = self.res_evo_fit_line_width.field.value()
        self.local_variables["fit_line_style"] = self.res_evo_fit_line_style.fields.currentText()
        self.accept()

    def get_values(self):
        self.res_evo_cols.setValue(self.local_variables["cols_page"])
        self.res_evo_rows.setValue(self.local_variables["rows_page"])
        self.res_evo_set_x_values.setChecked(self.local_variables["set_x_values"])
        self.res_evo_x_ticks_nbins.setValue(self.local_variables["x_ticks_nbins"])
        self.res_evo_x_label.field.setText(self.local_variables["x_label"])
        self.res_evo_plot_line_style.select(self.local_variables["line_style"])
        self.res_evo_plot_line_width.setValue(self.local_variables["line_width"])
        self.res_evo_line_color.select(self.local_variables["line_color"])
        self.res_evo_plot_marker_style.select(self.local_variables["marker_style"])
        self.res_evo_plot_marker_size.setValue(self.local_variables["marker_size"])
        self.res_evo_plot_fill_between.setChecked(self.local_variables["fill_between"])
        self.res_evo_plot_fill_colour.select(self.local_variables["fill_color"])
        self.res_evo_fill_alpha.setValue(self.local_variables["fill_alpha"])
        self.res_evo_fit_line_colour.select(self.local_variables["fit_line_color"])
        self.res_evo_fit_line_width.setValue(self.local_variables["fit_line_width"])
        self.res_evo_fit_line_style.select(self.local_variables["fit_line_style"])
        self.res_evo_marker_color.select(self.local_variables["marker_color"])
