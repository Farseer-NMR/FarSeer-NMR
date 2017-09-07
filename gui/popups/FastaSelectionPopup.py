from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QDialogButtonBox, QFileDialog, QGridLayout, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from gui.components.LabelledCheckbox import LabelledCheckbox
from gui.components.LabelledDoubleSpinBox import LabelledDoubleSpinBox
from gui.components.LabelledSpinBox import LabelledSpinBox
from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.components.ColourBox import ColourBox

from gui.popups.UserMarksPopup import UserMarksPopup

from gui.gui_utils import defaults
from functools import partial

from collections import OrderedDict

class FastaSelectionPopup(QDialog):

    def __init__(self, parent=None, variables=None, **kw):
        super(FastaSelectionPopup, self).__init__(parent)
        self.setWindowTitle("FASTA Selection Popup")

        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("Y conditions", self)
        self.layout().addWidget(label)
        self.cond_widget_dict = {}

        if variables:
            self.fasta_files = OrderedDict(sorted(variables["fasta_files"].items()))
            self.get_values(variables)

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(partial(self.set_values, variables))
        self.buttonBox.rejected.connect(self.reject)

        self.layout().addWidget(self.buttonBox)


    def get_values(self, variables):
        if self.fasta_files:
            for cond_name, fasta_path in self.fasta_files.items():
                self.add_field(cond_name, fasta_path)
        elif variables["conditions"]["y"]:
            for cond in variables["conditions"]["y"]:
                self.add_field(cond, '')



    def set_values(self, variables):
        for name, widget in self.cond_widget_dict.items():
            self.fasta_files[name] = widget[0].field.text()
        variables["fasta_files"] = self.fasta_files
        self.accept()



    def add_field(self, cond_name, fasta_path):

        widget = QWidget()
        widget_layout = QHBoxLayout()
        widget.setLayout(widget_layout)
        line_edit = LabelledLineEdit(self, cond_name)
        if fasta_path:
            line_edit.setText(fasta_path)
        button = QPushButton("...", self)
        line_edit.field.setMinimumWidth(250)
        button.setMaximumWidth(25)
        button.clicked.connect(partial(self.raise_file_dialog, line_edit))
        widget.layout().addWidget(line_edit)
        widget.layout().addWidget(button)
        widget_items = (line_edit, button)
        self.cond_widget_dict[cond_name] = widget_items
        self.layout().addWidget(widget)

        return

    def raise_file_dialog(self, file_field):
        fasta_file = QFileDialog.getOpenFileName(self, "Select FASTA File", "", "*.fasta")
        if fasta_file:
            file_field.field.setText(fasta_file[0])