from PyQt5.QtWidgets import QDialogButtonBox

from gui.components.LabelledSpinBox import LabelledSpinBox

from gui.popups.BasePopup import BasePopup

class PreAnalysisPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="PRE Settings",
                           settings_key=["pre_settings"])

        self.gaussian_stdev = LabelledSpinBox(self, "Gaussian Stdev", min=1, step=1)
        self.gauss_x_size = LabelledSpinBox(self, "Gaussian X Size", min=1, step=1)

        self.layout().addWidget(self.gauss_x_size, 0, 0)
        self.layout().addWidget(self.gaussian_stdev, 1, 0)


        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.get_defaults)

        self.layout().addWidget(self.buttonBox, 2, 0)

        self.get_values()

    def get_defaults(self):
        self.gauss_x_size.field.setValue(self.default["gauss_x_size"])
        self.gaussian_stdev.field.setValue(self.default["gaussian_stdev"])

    def set_values(self):
        self.local_variables["gaussian_stdev"] = self.gaussian_stdev.field.value()
        self.local_variables["gauss_x_size"] = self.gauss_x_size.field.value()
        self.accept()


    def get_values(self):
        self.gaussian_stdev.setValue(self.local_variables["gaussian_stdev"])
        self.gauss_x_size.setValue(self.local_variables["gauss_x_size"])
