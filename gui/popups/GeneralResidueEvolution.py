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

from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledCombobox import LabelledCombobox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.FontComboBox import FontComboBox

from gui.gui_utils import font_weights

from gui.popups.BasePopup import BasePopup


class GeneralResidueEvolution(BasePopup):
    """
    A popup for setting General Residue Evolution Plot specific settings in the
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
                           title="Residue Evolution Plot",
                           settings_key=["revo_settings"]
                          )

        self.do_revo_fit = LabelledCheckbox(
                                            self,
                                            text="Fit Parameter Evolution"
                                           )
        self.revo_subtitle_fn = FontComboBox(self, text="Subtitle Font")
        self.revo_subtitle_fs = LabelledSpinBox(
                                                self,
                                                text="Subtitle Font Size",
                                                minimum=0,
                                                step=1
                                                )
        self.revo_subtitle_pad = LabelledDoubleSpinBox(
                                                       self,
                                                       text="Subtitle Padding",
                                                       minimum=-100,
                                                       maximum=100,
                                                       step=0.1
                                                       )
        self.revo_subtitle_weight = LabelledCombobox(
                                                   self,
                                                   text="Subtitle Font Weight",
                                                   items=font_weights
                                                    )

        self.revo_x_label_fn = FontComboBox(self, text="X Label Font")
        self.revo_x_label_fs = LabelledSpinBox(
                                               self,
                                               text="X Label Font Size",
                                               minimum=0,
                                               step=1
                                               )
        self.revo_x_label_pad = LabelledDoubleSpinBox(
                                                      self,
                                                      text="X Label Padding",
                                                      minimum=-100,
                                                      maximum=100,
                                                      step=0.1
                                                      )
        self.revo_x_label_weight = LabelledCombobox(
                                                    self,
                                                    text="X Label Font Weight",
                                                    items=font_weights
                                                    )

        self.revo_y_label_fn = FontComboBox(self, text="Y Label Font Size")
        self.revo_y_label_fs = LabelledSpinBox(
                                               self,
                                               text="Y Label Font Size",
                                               minimum=0,
                                               step=1
                                               )
        self.revo_y_label_pad = LabelledSpinBox(
                                                self,
                                                text="Y Label Padding",
                                                minimum=-100,
                                                maximum=100,
                                                step=0.1
                                                )
        self.revo_y_label_weight = LabelledCombobox(
                                                    self,
                                                    text="Y Label Font Weight",
                                                    items=font_weights
                                                    )

        self.revo_x_ticks_fn = FontComboBox(self, text="X Tick Font")
        self.revo_x_ticks_fs = LabelledSpinBox(
                                               self,
                                               text="X Tick Font Size",
                                               minimum=0,
                                               step=1
                                               )
        self.revo_x_ticks_pad = LabelledDoubleSpinBox(
                                                      self,
                                                      text="X Tick Padding",
                                                      minimum=-100,
                                                      maximum=100,
                                                      step=0.1
                                                      )
        self.revo_x_ticks_weight = LabelledCombobox(
                                                    self,
                                                    text="X Tick Font Weight",
                                                    items=font_weights
                                                    )
        self.revo_x_ticks_rotation = LabelledDoubleSpinBox(
                                                        self,
                                                        text="X Tick Rotation",
                                                        minimum=0,
                                                        maximum=360,
                                                        step=1
                                                           )

        self.revo_y_ticks_fn = FontComboBox(self, text="Y Tick Font")
        self.revo_y_ticks_fs = LabelledSpinBox(
                                               self,
                                               text="Y Tick Font Size",
                                               minimum=0,
                                               step=1)

        self.revo_y_ticks_pad = LabelledDoubleSpinBox(
                                                      self,
                                                      text="Y Tick Padding",
                                                      minimum=-100,
                                                      maximum=100,
                                                      step=0.1
                                                      )
        self.revo_y_ticks_weight = LabelledCombobox(
                                                    self,
                                                    text="Y Tick Font Weight",
                                                    items=font_weights
                                                    )
        self.revo_y_ticks_rot = LabelledSpinBox(
                                                self,
                                                text="Y Tick Rotation",
                                                minimum=0,
                                                maximum=360,
                                                step=1
                                                )
        self.titration_x_values = LabelledLineEdit(
                                                   self,
                                                   text="Titration X Values"
                                                   )

        self.layout().addWidget(self.revo_subtitle_fn, 0, 0)
        self.layout().addWidget(self.revo_subtitle_fs, 1, 0)
        self.layout().addWidget(self.revo_subtitle_pad, 2, 0)
        self.layout().addWidget(self.revo_subtitle_weight, 3, 0)
        self.layout().addWidget(self.revo_x_label_fn, 4, 0)
        self.layout().addWidget(self.revo_x_label_fs, 5, 0)
        self.layout().addWidget(self.revo_x_label_pad, 6, 0)
        self.layout().addWidget(self.revo_x_label_weight, 7, 0)
        self.layout().addWidget(self.revo_y_label_fn, 8, 0)
        self.layout().addWidget(self.revo_y_label_fs, 9, 0)
        self.layout().addWidget(self.revo_y_label_pad, 10, 0)
        self.layout().addWidget(self.titration_x_values, 11, 0)

        self.layout().addWidget(self.revo_y_label_weight, 0, 1)
        self.layout().addWidget(self.revo_x_ticks_fn, 1, 1)
        self.layout().addWidget(self.revo_x_ticks_fs, 2, 1)
        self.layout().addWidget(self.revo_x_ticks_pad, 3, 1)
        self.layout().addWidget(self.revo_x_ticks_weight, 4, 1)
        self.layout().addWidget(self.revo_x_ticks_rotation, 5, 1)
        self.layout().addWidget(self.revo_y_ticks_fn, 6, 1)
        self.layout().addWidget(self.revo_y_ticks_fs, 7, 1)
        self.layout().addWidget(self.revo_y_ticks_pad, 8, 1)
        self.layout().addWidget(self.revo_y_ticks_weight, 9, 1)
        self.layout().addWidget(self.revo_y_ticks_rot, 10, 1)
        self.layout().addWidget(self.do_revo_fit, 11, 1)

        self.buttonBox = QDialogButtonBox(
                                          QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel |
                                          QDialogButtonBox.RestoreDefaults
                                          )

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).\
            clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 12, 0, 1, 2)

        self.get_values()

    def get_defaults(self):
        self.do_revo_fit.checkBox.setChecked(
            self.defaults["perform_resevo_fitting"])
        self.revo_subtitle_fn.select(self.defaults["revo_subtitle_fn"])
        self.revo_subtitle_fs.setValue(self.defaults["revo_subtitle_fs"])
        self.revo_subtitle_pad.setValue(self.defaults["revo_subtitle_pad"])
        self.revo_subtitle_weight.select(self.defaults["revo_subtitle_weight"])
        self.revo_x_label_fn.select(self.defaults["revo_x_label_fn"])
        self.revo_x_label_fs.setValue(self.defaults["revo_x_label_fs"])
        self.revo_x_label_pad.setValue(self.defaults["revo_x_label_pad"])
        self.revo_x_label_weight.select(self.defaults["revo_x_label_weight"])
        self.revo_y_label_fn.select(self.defaults["revo_y_label_fn"])
        self.revo_y_label_fs.setValue(self.defaults["revo_y_label_fs"])
        self.revo_y_label_pad.setValue(self.defaults["revo_y_label_pad"])

        self.revo_y_label_weight.select(self.defaults["revo_y_label_weight"])
        self.revo_x_ticks_fn.select(self.defaults["revo_x_ticks_fn"])
        self.revo_x_ticks_fs.setValue(self.defaults["revo_x_ticks_fs"])
        self.revo_x_ticks_pad.setValue(self.defaults["revo_x_ticks_pad"])
        self.revo_x_ticks_weight.select(self.defaults["revo_x_ticks_weight"])
        self.revo_x_ticks_rotation.setValue(self.defaults["revo_x_ticks_rot"])
        self.revo_y_ticks_fn.select(self.defaults["revo_y_ticks_fn"])
        self.revo_y_ticks_fs.setValue(self.defaults["revo_y_ticks_fs"])
        self.revo_y_ticks_pad.setValue(self.defaults["revo_y_ticks_pad"])
        self.revo_y_ticks_weight.select(self.defaults["revo_y_ticks_weight"])
        self.revo_y_ticks_rot.setValue(self.defaults["revo_y_ticks_rot"])
        self.titration_x_values.field.setText(','.join(
            [str(x) for x in self.defaults["titration_x_values"]]))

    def set_values(self):
        self.local_variables["perform_resevo_fitting"] = \
            self.do_revo_fit.isChecked()
        self.local_variables["subtitle_fn"] = \
            str(self.revo_subtitle_fn.fields.currentText())
        self.local_variables["subtitle_fs"] = \
            self.revo_subtitle_fs.field.value()
        self.local_variables["subtitle_pad"] = \
            self.revo_subtitle_pad.field.value()
        self.local_variables["subtitle_weight"] = \
            str(self.revo_subtitle_weight.fields.currentText())
        self.local_variables["x_label_fn"] = \
            str(self.revo_x_label_fn.fields.currentText())
        self.local_variables["x_label_fs"] = \
            self.revo_x_label_fs.field.value()
        self.local_variables["x_label_pad"] = \
            self.revo_x_label_pad.field.value()
        self.local_variables["x_label_weight"] = \
            str(self.revo_x_label_weight.fields.currentText())
        self.local_variables["y_label_fn"] = \
            str(self.revo_y_label_fn.fields.currentText())
        self.local_variables["y_label_fs"] = \
            self.revo_y_label_fs.field.value()
        self.local_variables["y_label_pad"] = \
            self.revo_y_label_pad.field.value()

        self.local_variables["y_label_weight"] = \
            str(self.revo_y_label_weight.fields.currentText())
        self.local_variables["x_ticks_fn"] = \
            str(self.revo_x_ticks_fn.fields.currentText())
        self.local_variables["x_ticks_fs"] = \
            self.revo_x_ticks_fs.field.value()
        self.local_variables["x_ticks_pad"] = \
            self.revo_x_ticks_pad.field.value()
        self.local_variables["x_ticks_weight"] = \
            str(self.revo_x_ticks_weight.fields.currentText())
        self.local_variables["x_ticks_rot"] = \
            self.revo_x_ticks_rotation.field.value()
        self.local_variables["y_ticks_fn"] = \
            str(self.revo_y_ticks_fn.fields.currentText())
        self.local_variables["y_ticks_fs"] = \
            self.revo_y_ticks_fs.field.value()
        self.local_variables["y_ticks_pad"] = \
            self.revo_y_ticks_pad.field.value()
        self.local_variables["y_ticks_weight"] = \
            str(self.revo_y_ticks_weight.fields.currentText())
        self.local_variables["y_ticks_rot"] = \
            self.revo_y_ticks_rot.field.value()
        self.local_variables["titration_x_values"] = \
            [float(x) for x in self.titration_x_values.field.text().split(',')]
        self.accept()

    def get_values(self):
        self.do_revo_fit.setChecked(
            self.local_variables["perform_resevo_fitting"])
        self.revo_subtitle_fn.select(self.local_variables["subtitle_fn"])
        self.revo_subtitle_fs.setValue(self.local_variables["subtitle_fs"])
        self.revo_subtitle_pad.setValue(self.local_variables["subtitle_pad"])
        self.revo_subtitle_weight.select(
            self.local_variables["subtitle_weight"])
        self.revo_x_label_fn.select(self.local_variables["x_label_fn"])
        self.revo_x_label_fs.setValue(self.local_variables["x_label_fs"])
        self.revo_x_label_pad.setValue(self.local_variables["x_label_pad"])
        self.revo_x_label_weight.select(self.local_variables["x_label_weight"])
        self.revo_y_label_fn.select(self.local_variables["y_label_fn"])
        self.revo_y_label_fs.setValue(self.local_variables["y_label_fs"])
        self.revo_y_label_pad.setValue(self.local_variables["y_label_pad"])

        self.revo_y_label_weight.select(self.local_variables["y_label_weight"])
        self.revo_x_ticks_fn.select(self.local_variables["x_ticks_fn"])
        self.revo_x_ticks_fs.setValue(self.local_variables["x_ticks_fs"])
        self.revo_x_ticks_pad.setValue(self.local_variables["x_ticks_pad"])
        self.revo_x_ticks_weight.select(self.local_variables["x_ticks_weight"])
        self.revo_x_ticks_rotation.setValue(
            self.local_variables["x_ticks_rot"])
        self.revo_y_ticks_fn.select(self.local_variables["y_ticks_fn"])
        self.revo_y_ticks_fs.setValue(self.local_variables["y_ticks_fs"])
        self.revo_y_ticks_pad.setValue(self.local_variables["y_ticks_pad"])
        self.revo_y_ticks_weight.select(self.local_variables["y_ticks_weight"])
        self.revo_y_ticks_rot.setValue(self.local_variables["y_ticks_rot"])
        self.revo_y_ticks_rot.setValue(self.local_variables["y_ticks_rot"])
        self.titration_x_values.field.setText(','.join(
            [str(x) for x in self.local_variables["titration_x_values"]]))
