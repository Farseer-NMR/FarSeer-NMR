from PyQt5.QtWidgets import QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox

from gui.gui_utils import colours
# https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
import string
translator = str.maketrans('', '', string.punctuation+" ")



from gui.popups.BasePopup import BasePopup

class ScatterPlotPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="Scatter Plot",
                           settings_key=["cs_scatter_settings"])

        self.cs_scatter_cols_page = LabelledSpinBox(self, "Columns Per Page", min=1, step=1)
        self.cs_scatter_rows_page = LabelledSpinBox(self, "Rows Per Page", min=1, step=1)
        self.cs_scatter_x_label = LabelledLineEdit(self, "X Label")
        self.cs_scatter_y_label = LabelledLineEdit(self, "Y Label")
        self.cs_scatter_mksize = LabelledSpinBox(self, "Mark Size", min=0, step=1)
        self.cs_scatter_scale = LabelledDoubleSpinBox(self, "Scale", min=0, step=0.01)
        self.cs_scatter_mk_type = LabelledCombobox(self, text="Mark Type", items=['color', 'shape'])
        self.cs_scatter_mk_start_color = ColourBox(self, text="Mark Start Colour")
        self.cs_scatter_mk_end_color = ColourBox(self, text="Mark End Colour")
        self.cs_scatter_markers = LabelledLineEdit(self, "Sequential Markers")
        self.cs_scatter_mk_color = LabelledLineEdit(self, text="Mark Colours")
        self.cs_scatter_mk_lost_color = ColourBox(self, "Lost Mark Colour")
        self.cs_scatter_mk_edgecolors = LabelledLineEdit(self, "Marker Edge Colours")
        self.cs_scatter_hide_lost = LabelledCheckbox(self, "Hide Lost Data Points")

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
        self.layout().addWidget(self.cs_scatter_mk_lost_color, 5, 1)
        self.layout().addWidget(self.cs_scatter_hide_lost, 6, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 7, 0, 1, 2)

        self.get_values()

    def get_defaults(self):
        self.cs_scatter_cols_page.setValue(self.default["cols_page"])
        self.cs_scatter_rows_page.setValue(self.default["rows_page"])
        self.cs_scatter_x_label.field.setText(self.default["x_label"])
        self.cs_scatter_y_label.field.setText(self.default["y_label"])
        self.cs_scatter_mksize.setValue(self.default["mksize"])
        self.cs_scatter_scale.setValue(self.default["scale"])
        self.cs_scatter_mk_type.select(self.default["mk_type"])

        self.cs_scatter_mk_start_color.select(self.default["mk_start_color"])
        self.cs_scatter_mk_end_color.select(self.default["mk_end_color"])
        self.cs_scatter_markers.field.setText(','.join(self.default["markers"]))
        self.cs_scatter_mk_color.field.setText(','.join(self.default["mk_color"]))
        self.cs_scatter_mk_edgecolors.field.setText(','.join(self.default["mk_edgecolors"]))
        self.cs_scatter_mk_lost_color.select(self.default["mk_lost_color"])
        self.cs_scatter_hide_lost.setChecked(self.default["hide_lost"])


    def set_values(self):
        self.local_variables["cols_page"] = self.cs_scatter_cols_page.field.value()
        self.local_variables["rows_page"] = self.cs_scatter_rows_page.field.value()
        self.local_variables["x_label"] = self.cs_scatter_x_label.field.text()
        self.local_variables["y_label"] = self.cs_scatter_y_label.field.text()
        self.local_variables["mksize"] = self.cs_scatter_mksize.field.value()
        self.local_variables["scale"] = self.cs_scatter_scale.field.value()
        self.local_variables["mk_type"] = self.cs_scatter_mk_type.fields.currentText()
        self.local_variables["mk_start_color"] = colours[self.cs_scatter_mk_start_color.fields.currentText()]
        self.local_variables["mk_end_color"] = colours[self.cs_scatter_mk_end_color.fields.currentText()]
        self.local_variables["markers"] = [x.strip().strip("'") for x in self.cs_scatter_markers.field.text().split(',')]
        self.local_variables["mk_color"] = \
            [x.translate(translator) \
                for x in self.cs_scatter_mk_color.field.text().split(',')]
        self.local_variables["mk_edgecolors"] = \
            [x.translate(translator) \
                for x in self.cs_scatter_mk_edgecolors.field.text().split(',')]
        self.local_variables["mk_lost_color"] = self.cs_scatter_mk_lost_color.fields.currentText()
        self.local_variables["hide_lost"] = self.cs_scatter_hide_lost.checkBox.isChecked()
        self.accept()

    def get_values(self):
        self.cs_scatter_cols_page.setValue(self.local_variables["cols_page"])
        self.cs_scatter_rows_page.setValue(self.local_variables["rows_page"])
        self.cs_scatter_x_label.field.setText(self.local_variables["x_label"])
        self.cs_scatter_y_label.field.setText(self.local_variables["y_label"])
        self.cs_scatter_mksize.setValue(self.local_variables["mksize"])
        self.cs_scatter_scale.setValue(self.local_variables["scale"])
        self.cs_scatter_mk_type.select(self.local_variables["mk_type"])

        self.cs_scatter_mk_start_color.select(self.local_variables["mk_start_color"])
        self.cs_scatter_mk_end_color.select(self.local_variables["mk_end_color"])
        self.cs_scatter_markers.field.setText(','.join(self.local_variables["markers"]))
        self.cs_scatter_mk_color.field.setText(','.join(self.local_variables["mk_color"]))
        self.cs_scatter_mk_edgecolors.field.setText(','.join(self.local_variables["mk_edgecolors"]))
        self.cs_scatter_mk_lost_color.select(self.local_variables["mk_lost_color"])
        self.cs_scatter_hide_lost.setChecked(self.local_variables["hide_lost"])
