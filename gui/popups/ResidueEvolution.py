from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox, QLineEdit, QCheckBox, QDoubleSpinBox, QDialogButtonBox


class ResidueEvolutionPopup(QDialog):

    def __init__(self, parent=None, **kw):
        super(ResidueEvolutionPopup, self).__init__(parent)
        self.setWindowTitle("Extended Bar Plot")
        grid = QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)

        res_evo_cols_label = QLabel("Columns Per Page", self)
        res_evo_rows_label = QLabel("Rows Per Page", self)
        res_evo_title_label = QLabel("Title Size", self)
        res_evo_font_size_label = QLabel("Title Font Size", self)
        res_evo_font_label = QLabel("Title Font", self)
        set_x_values_label = QLabel("Set X Values", self)
        x_tick_font_label = QLabel("X Tick Font", self)
        x_tick_font_size_label = QLabel("X Tick Font Size", self)
        x_tick_padding_label = QLabel("X Tick Padding", self)
        x_tick_flag_label = QLabel("Label X Axis?", self)
        y_tick_padding_label = QLabel("Y Tick Padding", self)
        y_tick_font_size_label = QLabel("Y Tick Font Size", self)
        res_evo_plot_colour_label = QLabel("Plot Colour", self)
        res_evo_plot_line_style_label = QLabel("Line Style", self)
        res_evo_plot_marker_style_label = QLabel("Marker Style", self)
        res_evo_plot_marker_colour_label = QLabel("Marker Colour", self)
        res_evo_plot_marker_size_label = QLabel("Marker Size", self)
        res_evo_plot_line_width_label = QLabel("Line Width", self)
        res_evo_plot_fill_between_label = QLabel("Fill Between?", self)
        res_evo_plot_fill_colour_label = QLabel("Fill Colour", self)
        res_evo_plot_fill_alpha_label = QLabel("Fill Alphar", self)



        self.layout().addWidget(res_evo_cols_label, 0, 0)
        self.layout().addWidget(res_evo_rows_label, 1, 0)
        self.layout().addWidget(res_evo_title_label, 2, 0)
        self.layout().addWidget(res_evo_font_size_label, 3, 0)
        self.layout().addWidget(res_evo_font_label, 4, 0)
        self.layout().addWidget(set_x_values_label, 5, 0)
        self.layout().addWidget(x_tick_font_label, 6, 0)
        self.layout().addWidget(x_tick_font_size_label, 7, 0)
        self.layout().addWidget(x_tick_padding_label, 8, 0)
        self.layout().addWidget(x_tick_flag_label, 9, 0)
        self.layout().addWidget(y_tick_padding_label, 10, 0)
        self.layout().addWidget(y_tick_font_size_label, 11, 0)
        self.layout().addWidget(res_evo_plot_colour_label, 12, 0)
        self.layout().addWidget(res_evo_plot_line_style_label, 13, 0)
        self.layout().addWidget(res_evo_plot_marker_style_label, 14, 0)
        self.layout().addWidget(res_evo_plot_marker_colour_label, 15, 0)
        self.layout().addWidget(res_evo_plot_marker_size_label, 16, 0)
        self.layout().addWidget(res_evo_plot_line_width_label, 17, 0)
        self.layout().addWidget(res_evo_plot_fill_between_label, 18, 0)
        self.layout().addWidget(res_evo_plot_fill_colour_label, 19, 0)
        self.layout().addWidget(res_evo_plot_fill_alpha_label, 20, 0)



        self.res_evo_cols = QSpinBox()
        self.res_evo_cols = QSpinBox()
        self.res_evo_title = QLineEdit()
        self.res_evo_font_size = QSpinBox()
        self.res_evo_font = QLineEdit()
        self.set_x_values = QCheckBox()
        self.x_tick_font = QLineEdit()
        self.x_tick_font_size = QSpinBox()
        self.x_tick_padding = QDoubleSpinBox()
        self.x_label_flag = QCheckBox()
        self.y_tick_padding = QDoubleSpinBox()
        self.y_tick_font_size = QSpinBox()
        self.res_evo_plot_colour = QLineEdit()
        self.res_evo_plot_line_style = QLineEdit()
        self.res_evo_plot_marker_style = QLineEdit()
        self.res_evo_plot_marker_colour = QLineEdit()
        self.res_evo_plot_marker_size = QSpinBox()


        self.layout().addWidget(self.res_evo_cols, 0, 1)
        self.layout().addWidget(self.res_evo_cols, 1, 1)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Reset)

        self.buttonBox.accepted.connect(self.setValues)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(self.set_defaults)

        self.layout().addWidget(self.buttonBox, 20, 0, 1, 2)

        # self.set_defaults()

    def set_defaults(self):
        self.res_evocols.setValue(1)
        self.res_evorows.setValue(6)
        self.apply_status.setChecked(True)
        self.meas_res_evocolour.setText('k')
        self.lost_res_evocolour.setText('red')
        self.unassigned_res_evocolour.setText('grey')
        self.res_evowidth.setValue(0.7)
        self.res_evoalpha.setValue(1)
        self.res_evolinewidth.setValue(10)
        self.res_evotitle.setText('1.05')
        self.res_evotitle_font.setText('Arial')
        self.res_evotitle_font_size.setValue(10)
        self.res_evothreshold.setChecked(True)
        self.res_evothreshold_colour.setText('red')
        self.res_evothreshold_linewidth.setValue(1)
        self.x_tick_rotation.setValue(90)
        self.x_tick_font_size.setValue(6)
        self.x_tick_font.setText('monospace')
        self.x_tick_padding.setValue(0.1)
        self.y_tick_font_size.setValue(9)
        self.y_grid_colour.setText('grey')
        self.markProlines.setChecked(True)
        self.proline_marker.setText('P')
        self.user_details.setChecked(True)

    def setValues(self):
        self.accept()
