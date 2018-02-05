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
from PyQt5.QtWidgets import QDialogButtonBox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox
from gui.components.FontComboBox import FontComboBox

from gui.gui_utils import font_weights, colours

# https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
import string
translator = str.maketrans('', '', string.punctuation+" ")


from gui.popups.BasePopup import BasePopup

class ScatterFlowerPlotPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="Scatter Flower Plot",
                           settings_key=["cs_scatter_flower_settings"])

        self.cs_scatter_flower_x_label = LabelledLineEdit(self, "X Label")
        self.cs_scatter_flower_y_label = LabelledLineEdit(self, "Y Label")
        self.cs_scatter_flower_mksize = LabelledSpinBox(self, "Mark Size", min=0, step=1)
        self.cs_scatter_flower_color_grad = LabelledCheckbox(self, "Colour Gradient")
        self.cs_scatter_flower_color_start = ColourBox(self, text="Mark Start Colour")
        self.cs_scatter_flower_color_end = ColourBox(self, text="Mark End Colour")
        self.cs_scatter_flower_color_list = LabelledLineEdit(self, "Colour List")

        self.cs_scatter_flower_x_label_fn = FontComboBox(self, "X Label Font")
        self.cs_scatter_flower_x_label_fs = LabelledSpinBox(self, "X Label Font Size", min=0, step=1)
        self.cs_scatter_flower_x_label_pad = LabelledDoubleSpinBox(self, "X Label Padding", min=-100, max=100, step=0.1)
        self.cs_scatter_flower_x_label_weight = LabelledCombobox(self, text="X Label Font Weight", items=font_weights)

        self.cs_scatter_flower_y_label_fn = FontComboBox(self, "Y Label Font")
        self.cs_scatter_flower_y_label_fs = LabelledSpinBox(self, "Y Label Font Size", min=0, step=1)
        self.cs_scatter_flower_y_label_pad = LabelledDoubleSpinBox(self, "Y Label Padding", min=-100, max=100, step=0.1)
        self.cs_scatter_flower_y_label_weight = LabelledCombobox(self, text="Y Label Font Weight", items=font_weights)

        self.cs_scatter_flower_x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.cs_scatter_flower_x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size", min=0, step=1)
        self.cs_scatter_flower_x_ticks_pad = LabelledDoubleSpinBox(self, "X Tick Padding", min=-100, max=100, step=0.1)
        self.cs_scatter_flower_x_ticks_weight = LabelledCombobox(self, text="X Tick Weight", items=font_weights)
        self.cs_scatter_flower_x_ticks_rot = LabelledSpinBox(self, "X Tick Rotation", min=0, max=360, step=1)

        self.cs_scatter_flower_y_ticks_fn = FontComboBox(self, "Y Tick Font")
        self.cs_scatter_flower_y_ticks_fs = LabelledSpinBox(self, "Y Tick Font Size", min=0, step=1)
        self.cs_scatter_flower_y_ticks_pad = LabelledDoubleSpinBox(self, "Y Tick Padding", min=-100, max=100, step=0.1)
        self.cs_scatter_flower_y_ticks_weight = LabelledCombobox(self, text="Y Tick Weight", items=font_weights)
        self.cs_scatter_flower_y_ticks_rot = LabelledSpinBox(self, "Y Tick Rotation", min=0, max=360, step=1)

        self.layout().addWidget(self.cs_scatter_flower_x_label, 0, 0)
        self.layout().addWidget(self.cs_scatter_flower_y_label, 1, 0)
        self.layout().addWidget(self.cs_scatter_flower_mksize, 2, 0)
        self.layout().addWidget(self.cs_scatter_flower_color_grad, 3, 0)
        self.layout().addWidget(self.cs_scatter_flower_color_start, 4, 0)
        self.layout().addWidget(self.cs_scatter_flower_color_end, 5, 0)
        self.layout().addWidget(self.cs_scatter_flower_x_label_fn, 6, 0)
        self.layout().addWidget(self.cs_scatter_flower_x_label_fs, 7, 0)
        self.layout().addWidget(self.cs_scatter_flower_color_list, 8, 0)


        self.layout().addWidget(self.cs_scatter_flower_x_label_pad, 0, 1)
        self.layout().addWidget(self.cs_scatter_flower_x_label_weight, 1, 1)
        self.layout().addWidget(self.cs_scatter_flower_y_label_fn, 2, 1)
        self.layout().addWidget(self.cs_scatter_flower_y_label_fs, 3, 1)
        self.layout().addWidget(self.cs_scatter_flower_y_label_pad, 4, 1)
        self.layout().addWidget(self.cs_scatter_flower_y_label_weight, 5, 1)
        self.layout().addWidget(self.cs_scatter_flower_x_ticks_fn, 6, 1)
        self.layout().addWidget(self.cs_scatter_flower_x_ticks_fs, 7, 1)


        self.layout().addWidget(self.cs_scatter_flower_x_ticks_pad, 0, 2)
        self.layout().addWidget(self.cs_scatter_flower_x_ticks_weight, 1, 2)
        self.layout().addWidget(self.cs_scatter_flower_x_ticks_rot, 2, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_fn, 3, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_fs, 4, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_pad, 5, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_weight, 6, 2)
        self.layout().addWidget(self.cs_scatter_flower_y_ticks_rot, 7, 2)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 8, 1, 1, 2)

        self.get_values()

    def get_defaults(self):
        self.cs_scatter_flower_x_label.field.setText(self.default["x_label"])
        self.cs_scatter_flower_y_label.field.setText(self.default["y_label"])
        self.cs_scatter_flower_mksize.setValue(self.default["mksize"])
        self.cs_scatter_flower_color_grad.setChecked(self.default["color_grad"])
        self.cs_scatter_flower_color_start.select(self.default["mk_start_color"])
        self.cs_scatter_flower_color_end.select(self.default["mk_end_color"])
        self.cs_scatter_flower_color_list.field.setText(','.join(self.default["color_list"]))

        self.cs_scatter_flower_x_label_fn.select(self.default["x_label_fn"])
        self.cs_scatter_flower_x_label_fs.setValue(self.default["x_label_fs"])
        self.cs_scatter_flower_x_label_pad.setValue(self.default["x_label_pad"])
        self.cs_scatter_flower_x_label_weight.select(self.default["x_label_weight"])

        self.cs_scatter_flower_y_label_fn.select(self.default["y_label_fn"])
        self.cs_scatter_flower_y_label_fs.setValue(self.default["y_label_fs"])
        self.cs_scatter_flower_y_label_pad.setValue(self.default["y_label_pad"])
        self.cs_scatter_flower_y_label_weight.select(self.default["y_label_weight"])

        self.cs_scatter_flower_x_ticks_fn.select(self.default["x_ticks_fn"])
        self.cs_scatter_flower_x_ticks_fs.setValue(self.default["x_ticks_fs"])
        self.cs_scatter_flower_x_ticks_pad.setValue(self.default["x_ticks_pad"])
        self.cs_scatter_flower_x_ticks_weight.select(self.default["x_ticks_weight"])
        self.cs_scatter_flower_x_ticks_rot.setValue(self.default["x_ticks_rot"])

        self.cs_scatter_flower_y_ticks_fn.select(self.default["y_ticks_fn"])
        self.cs_scatter_flower_y_ticks_fs.setValue(self.default["y_ticks_fs"])
        self.cs_scatter_flower_y_ticks_pad.setValue(self.default["y_ticks_pad"])
        self.cs_scatter_flower_y_ticks_weight.select(self.default["y_ticks_weight"])
        self.cs_scatter_flower_y_ticks_rot.setValue(self.default["y_ticks_rot"])


    def set_values(self):
        self.local_variables["x_label"] = self.cs_scatter_flower_x_label.field.text()
        self.local_variables["y_label"] = self.cs_scatter_flower_y_label.field.text()
        self.local_variables["mksize"] = self.cs_scatter_flower_mksize.field.value()
        self.local_variables["color_grad"] = self.cs_scatter_flower_color_grad.checkBox.isChecked()
        self.local_variables["mk_start_color"] = colours[self.cs_scatter_flower_color_start.fields.currentText()]
        self.local_variables["mk_end_color"] = colours[self.cs_scatter_flower_color_end.fields.currentText()]

        self.local_variables["x_label_fn"] = self.cs_scatter_flower_x_label_fn.fields.currentText()
        self.local_variables["x_label_fs"] = self.cs_scatter_flower_x_label_fs.field.value()
        self.local_variables["x_label_pad"] = self.cs_scatter_flower_x_label_pad.field.value()
        self.local_variables["x_label_weight"] = self.cs_scatter_flower_x_label_weight.fields.currentText()

        self.local_variables["y_label_fn"] = self.cs_scatter_flower_y_label_fn.fields.currentText()
        self.local_variables["y_label_fs"] = self.cs_scatter_flower_y_label_fs.field.value()
        self.local_variables["y_label_pad"] = self.cs_scatter_flower_y_label_pad.field.value()
        self.local_variables["y_label_weight"] = self.cs_scatter_flower_y_label_weight.fields.currentText()

        self.local_variables["x_label_fn"] = self.cs_scatter_flower_x_label_fn.fields.currentText()
        self.local_variables["x_label_fs"] = self.cs_scatter_flower_x_label_fs.field.value()
        self.local_variables["x_label_pad"] = self.cs_scatter_flower_x_label_pad.field.value()
        self.local_variables["x_label_weight"] = self.cs_scatter_flower_x_label_weight.fields.currentText()

        self.local_variables["x_ticks_fn"] = self.cs_scatter_flower_x_ticks_fn.fields.currentText()
        self.local_variables["x_ticks_fs"] = self.cs_scatter_flower_x_ticks_fs.field.value()
        self.local_variables["x_ticks_pad"] = self.cs_scatter_flower_x_ticks_pad.field.value()
        self.local_variables["x_ticks_weight"] = self.cs_scatter_flower_x_ticks_weight.fields.currentText()
        self.local_variables["x_ticks_rot"] = self.cs_scatter_flower_x_ticks_rot.field.value()

        self.local_variables["y_ticks_fn"] = self.cs_scatter_flower_y_ticks_fn.fields.currentText()
        self.local_variables["y_ticks_fs"] = self.cs_scatter_flower_y_ticks_fs.field.value()
        self.local_variables["y_ticks_pad"] = self.cs_scatter_flower_y_ticks_pad.field.value()
        self.local_variables["y_ticks_weight"] = self.cs_scatter_flower_y_ticks_weight.fields.currentText()
        self.local_variables["y_ticks_rot"] = self.cs_scatter_flower_y_ticks_rot.field.value()
        self.local_variables["color_list"] = \
            [x.translate(translator) \
                for x in self.cs_scatter_flower_color_list.field.text().\
                    split(',')]
        
        self.accept()

    def get_values(self):

        self.cs_scatter_flower_x_label.field.setText(self.local_variables["x_label"])
        self.cs_scatter_flower_y_label.field.setText(self.local_variables["y_label"])
        self.cs_scatter_flower_mksize.setValue(self.local_variables["mksize"])
        self.cs_scatter_flower_color_grad.setChecked(self.local_variables["color_grad"])
        self.cs_scatter_flower_color_start.select(self.local_variables["mk_start_color"])
        self.cs_scatter_flower_color_end.select(self.local_variables["mk_end_color"])
        self.cs_scatter_flower_color_list.field.setText(','.join(self.local_variables["color_list"]))

        self.cs_scatter_flower_x_label_fn.select(self.local_variables["x_label_fn"])
        self.cs_scatter_flower_x_label_fs.setValue(self.local_variables["x_label_fs"])
        self.cs_scatter_flower_x_label_pad.setValue(self.local_variables["x_label_pad"])
        self.cs_scatter_flower_x_label_weight.select(self.local_variables["x_label_weight"])

        self.cs_scatter_flower_y_label_fn.select(self.local_variables["y_label_fn"])
        self.cs_scatter_flower_y_label_fs.setValue(self.local_variables["y_label_fs"])
        self.cs_scatter_flower_y_label_pad.setValue(self.local_variables["y_label_pad"])
        self.cs_scatter_flower_y_label_weight.select(self.local_variables["y_label_weight"])

        self.cs_scatter_flower_x_ticks_fn.select(self.local_variables["x_ticks_fn"])
        self.cs_scatter_flower_x_ticks_fs.setValue(self.local_variables["x_ticks_fs"])
        self.cs_scatter_flower_x_ticks_pad.setValue(self.local_variables["x_ticks_pad"])
        self.cs_scatter_flower_x_ticks_weight.select(self.local_variables["x_ticks_weight"])
        self.cs_scatter_flower_x_ticks_rot.setValue(self.local_variables["x_ticks_rot"])

        self.cs_scatter_flower_y_ticks_fn.select(self.local_variables["y_ticks_fn"])
        self.cs_scatter_flower_y_ticks_fs.setValue(self.local_variables["y_ticks_fs"])
        self.cs_scatter_flower_y_ticks_pad.setValue(self.local_variables["y_ticks_pad"])
        self.cs_scatter_flower_y_ticks_weight.select(self.local_variables["y_ticks_weight"])
        self.cs_scatter_flower_y_ticks_rot.setValue(self.local_variables["y_ticks_rot"])
