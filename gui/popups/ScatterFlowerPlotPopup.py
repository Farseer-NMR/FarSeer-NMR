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
from gui.components.FontComboBox import FontComboBox
from gui.popups.BasePopup import BasePopup
from gui.gui_utils import font_weights, colours

# https://stackoverflow.com/questions/34293875/how-to-remove-punctuation-marks-from-a-string-in-python-3-x-using-translate
translator = str.maketrans('', '', string.punctuation+" ")


class ScatterFlowerPlotPopup(BasePopup):
    """
    A popup for setting Scatter Flower Plot specific settings in the
    Farseer-NMR configuration.

    Parameters:
        parent(QWidget): parent widget for popup.

    Methods:
        .get_defaults()
        .get_values()
        .set_values()
    """
    def __init__(self, parent=None, **kw):
        BasePopup.__init__(
            self,
            parent,
            title="Scatter Flower Plot",
            settings_key=["cs_scatter_flower_settings"]
            )
        self.x_label = LabelledLineEdit(self, "X Label")
        self.y_label = LabelledLineEdit(self, "Y Label")
        self.mksize = LabelledSpinBox(self, "Mark Size", minimum=0, step=1)
        self.color_grad = LabelledCheckbox(self, "Colour Gradient")
        self.color_start = ColourBox(self, text="Mark Start Colour")
        self.color_end = ColourBox(self, text="Mark End Colour")
        self.color_list = LabelledLineEdit(self, "Colour List")
        self.x_label_fn = FontComboBox(self, "X Label Font")
        self.x_label_fs = LabelledSpinBox(self, "X Label Font Size", minimum=0, step=1)
        self.x_label_pad = LabelledDoubleSpinBox(
            self,
            "X Label Padding",
            minimum=-100,
            maximum=100,
            step=0.1
            )
        self.x_label_weight = LabelledCombobox(self, text="X Label Font Weight", items=font_weights)
        self.y_label_fn = FontComboBox(self, "Y Label Font")
        self.y_label_fs = LabelledSpinBox(self, "Y Label Font Size", minimum=0, step=1)
        self.y_label_pad = LabelledDoubleSpinBox(
            self,
            "Y Label Padding",
            minimum=-100,
            maximum=100,
            step=0.1
            )
        self.y_label_weight = LabelledCombobox(
            self,
            text="Y Label Font Weight",
            items=font_weights
            )
        self.x_ticks_fn = FontComboBox(self, "X Tick Font")
        self.x_ticks_fs = LabelledSpinBox(self, "X Tick Font Size", minimum=0, step=1)
        self.x_ticks_pad = LabelledDoubleSpinBox(
            self,
            "X Tick Padding",
            minimum=-100,
            maximum=100,
            step=0.1
            )
        self.x_ticks_weight = LabelledCombobox(self, text="X Tick Weight", items=font_weights)
        self.x_ticks_rot = LabelledSpinBox(
            self,
            "X Tick Rotation",
            minimum=0,
            maximum=360,
            step=1
            )
        self.y_ticks_fn = FontComboBox(self, "Y Tick Font")
        self.y_ticks_fs = LabelledSpinBox(self, "Y Tick Font Size", minimum=0, step=1)
        self.y_ticks_pad = LabelledDoubleSpinBox(
            self,
            "Y Tick Padding",
            minimum=-100,
            maximum=100,
            step=0.1
            )
        self.y_ticks_weight = LabelledCombobox(self, text="Y Tick Weight", items=font_weights)
        self.y_ticks_rot = LabelledSpinBox(
            self,
            "Y Tick Rotation",
            minimum=0,
            maximum=360,
            step=1
            )
        self.res_label_color = ColourBox(self, text="Residue Label Colour")
        # layout
        self.layout().addWidget(self.x_label, 0, 0)
        self.layout().addWidget(self.y_label, 1, 0)
        self.layout().addWidget(self.mksize, 2, 0)
        self.layout().addWidget(self.color_grad, 3, 0)
        self.layout().addWidget(self.color_start, 4, 0)
        self.layout().addWidget(self.color_end, 5, 0)
        self.layout().addWidget(self.x_label_fn, 6, 0)
        self.layout().addWidget(self.x_label_fs, 7, 0)
        self.layout().addWidget(self.color_list, 8, 0)
        self.layout().addWidget(self.res_label_color, 8, 1)
        self.layout().addWidget(self.x_label_pad, 0, 1)
        self.layout().addWidget(self.x_label_weight, 1, 1)
        self.layout().addWidget(self.y_label_fn, 2, 1)
        self.layout().addWidget(self.y_label_fs, 3, 1)
        self.layout().addWidget(self.y_label_pad, 4, 1)
        self.layout().addWidget(self.y_label_weight, 5, 1)
        self.layout().addWidget(self.x_ticks_fn, 6, 1)
        self.layout().addWidget(self.x_ticks_fs, 7, 1)
        self.layout().addWidget(self.x_ticks_pad, 0, 2)
        self.layout().addWidget(self.x_ticks_weight, 1, 2)
        self.layout().addWidget(self.x_ticks_rot, 2, 2)
        self.layout().addWidget(self.y_ticks_fn, 3, 2)
        self.layout().addWidget(self.y_ticks_fs, 4, 2)
        self.layout().addWidget(self.y_ticks_pad, 5, 2)
        self.layout().addWidget(self.y_ticks_weight, 6, 2)
        self.layout().addWidget(self.y_ticks_rot, 7, 2)
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel |
            QDialogButtonBox.RestoreDefaults
            )
        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)
        self.layout().addWidget(self.buttonBox, 9, 0, 1, 2)
        self.get_values()

    def get_defaults(self):
        # text
        self.x_label.field.setText(self.defaults["x_label"])
        self.y_label.field.setText(self.defaults["y_label"])
        self.color_list.field.setText(','.join(self.defaults["color_list"]))
        # value
        self.mksize.setValue(self.defaults["mksize"])
        self.x_label_fs.setValue(self.defaults["x_label_fs"])
        self.x_label_pad.setValue(self.defaults["x_label_pad"])
        self.y_label_fs.setValue(self.defaults["y_label_fs"])
        self.y_label_pad.setValue(self.defaults["y_label_pad"])
        self.x_ticks_fs.setValue(self.defaults["x_ticks_fs"])
        self.x_ticks_pad.setValue(self.defaults["x_ticks_pad"])
        self.x_ticks_rot.setValue(self.defaults["x_ticks_rot"])
        self.y_ticks_fs.setValue(self.defaults["y_ticks_fs"])
        self.y_ticks_pad.setValue(self.defaults["y_ticks_pad"])
        self.y_ticks_rot.setValue(self.defaults["y_ticks_rot"])
        # colour
        self.color_start.get_colour(self.defaults["mk_start_color"])
        self.color_end.get_colour(self.defaults["mk_end_color"])
        self.res_label_color.get_colour(self.defaults["res_label_color"])
        # chceked
        self.color_grad.setChecked(self.defaults["color_grad"])
        # dropdown
        self.x_label_fn.select(self.defaults["x_label_fn"])
        self.x_label_weight.select(self.defaults["x_label_weight"])
        self.y_label_fn.select(self.defaults["y_label_fn"])
        self.y_label_weight.select(self.defaults["y_label_weight"])
        self.x_ticks_fn.select(self.defaults["x_ticks_fn"])
        self.x_ticks_weight.select(self.defaults["x_ticks_weight"])
        self.y_ticks_fn.select(self.defaults["y_ticks_fn"])
        self.y_ticks_weight.select(self.defaults["y_ticks_weight"])

    def set_values(self):
        # text
        self.local_variables["x_label"] = self.x_label.field.text()
        self.local_variables["y_label"] = self.y_label.field.text()
        self.local_variables["x_label_fn"] = self.x_label_fn.fields.currentText()
        self.local_variables["x_label_weight"] = self.x_label_weight.fields.currentText()
        self.local_variables["y_label_fn"] = self.y_label_fn.fields.currentText()
        self.local_variables["y_label_weight"] = self.y_label_weight.fields.currentText()
        self.local_variables["x_label_fn"] = self.x_label_fn.fields.currentText()
        self.local_variables["x_label_weight"] = self.x_label_weight.fields.currentText()
        self.local_variables["x_ticks_fn"] = self.x_ticks_fn.fields.currentText()
        self.local_variables["x_ticks_weight"] = self.x_ticks_weight.fields.currentText()
        self.local_variables["y_ticks_fn"] = self.y_ticks_fn.fields.currentText()
        self.local_variables["y_ticks_weight"] = self.y_ticks_weight.fields.currentText()
        # value
        self.local_variables["mksize"] = self.mksize.field.value()
        self.local_variables["x_label_fs"] = self.x_label_fs.field.value()
        self.local_variables["x_label_pad"] = self.x_label_pad.field.value()
        self.local_variables["y_label_fs"] = self.y_label_fs.field.value()
        self.local_variables["y_label_pad"] = self.y_label_pad.field.value()
        self.local_variables["x_label_fs"] = self.x_label_fs.field.value()
        self.local_variables["x_label_pad"] = self.x_label_pad.field.value()
        self.local_variables["x_ticks_fs"] = self.x_ticks_fs.field.value()
        self.local_variables["x_ticks_pad"] = self.x_ticks_pad.field.value()
        self.local_variables["x_ticks_rot"] = self.x_ticks_rot.field.value()
        self.local_variables["y_ticks_fs"] = self.y_ticks_fs.field.value()
        self.local_variables["y_ticks_pad"] = self.y_ticks_pad.field.value()
        self.local_variables["y_ticks_rot"] = self.y_ticks_rot.field.value()
        # check
        self.local_variables["color_grad"] = self.color_grad.isChecked()
        # colours
        self.local_variables["mk_start_color"] = colours[self.color_start.fields.currentText()]
        self.local_variables["mk_end_color"] = colours[self.color_end.fields.currentText()]
        self.local_variables["res_label_color"] = self.res_label_color.fields.currentText()
        self.local_variables["color_list"] = \
            [x.translate(translator) for x in self.color_list.field.text().split(',')]
        self.accept()

    def get_values(self):
        # text
        self.x_label.field.setText(self.local_variables["x_label"])
        self.y_label.field.setText(self.local_variables["y_label"])
        self.color_list.field.setText(','.join(self.local_variables["color_list"]))
        # value
        self.mksize.setValue(self.local_variables["mksize"])
        self.x_label_fs.setValue(self.local_variables["x_label_fs"])
        self.x_label_pad.setValue(self.local_variables["x_label_pad"])
        self.y_label_fs.setValue(self.local_variables["y_label_fs"])
        self.y_label_pad.setValue(self.local_variables["y_label_pad"])
        self.x_ticks_fs.setValue(self.local_variables["x_ticks_fs"])
        self.x_ticks_pad.setValue(self.local_variables["x_ticks_pad"])
        self.x_ticks_rot.setValue(self.local_variables["x_ticks_rot"])
        self.y_ticks_fs.setValue(self.local_variables["y_ticks_fs"])
        self.y_ticks_pad.setValue(self.local_variables["y_ticks_pad"])
        self.y_ticks_rot.setValue(self.local_variables["y_ticks_rot"])
        # checked
        self.color_grad.setChecked(self.local_variables["color_grad"])
        # colours
        self.color_start.get_colour(self.local_variables["mk_start_color"])
        self.color_end.get_colour(self.local_variables["mk_end_color"])
        self.res_label_color.get_colour(self.local_variables["res_label_color"])
        # dropdown
        self.x_label_fn.select(self.local_variables["x_label_fn"])
        self.x_label_weight.select(self.local_variables["x_label_weight"])
        self.y_label_fn.select(self.local_variables["y_label_fn"])
        self.y_label_weight.select(self.local_variables["y_label_weight"])
        self.x_ticks_fn.select(self.local_variables["x_ticks_fn"])
        self.x_ticks_weight.select(self.local_variables["x_ticks_weight"])
        self.y_ticks_fn.select(self.local_variables["y_ticks_fn"])
        self.y_ticks_weight.select(self.local_variables["y_ticks_weight"])
