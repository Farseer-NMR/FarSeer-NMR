from collections import OrderedDict
from functools import partial

from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QFileDialog, QPushButton, QWidget, QHBoxLayout

from gui.components.LabelledLineEdit import LabelledLineEdit
from gui.popups.BasePopup import BasePopup


class FastaSelectionPopup(BasePopup):

    def __init__(self, parent=None, **kw):
        BasePopup.__init__(self, parent, title="FASTA Selection Popup",
                           settings_key=["fasta_files"], layout='vbox')

        label = QLabel("Y conditions", self)
        self.layout().addWidget(label)
        self.cond_widget_dict = {}

        self.fasta_files = OrderedDict(self.local_variables.items())

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.set_values)
        self.buttonBox.rejected.connect(self.reject)

        self.layout().addWidget(self.buttonBox)

        self.get_values()


    def get_values(self):
        if self.fasta_files:
            for cond_name, fasta_path in self.fasta_files.items():
                self.add_field(cond_name, fasta_path)
        elif self.variables["conditions"]["y"]:
            for cond in self.variables["conditions"]["y"]:
                self.add_field(cond, '')



    def set_values(self):
        for name, widget in self.cond_widget_dict.items():
            self.fasta_files[name] = widget[0].field.text()
        self.local_variables = self.fasta_files
        self.variables.update(self.local_variables)
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