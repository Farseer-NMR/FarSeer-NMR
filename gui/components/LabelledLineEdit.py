from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout

from gui.components.ModifiedLineEdit import ModifiedLineEdit

class LabelledLineEdit(QWidget):

    def __init__(self, parent, text, callback=None):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = ModifiedLineEdit(self)

        self.layout().addWidget(label)
        self.layout().addWidget(self.field)

        if callback:
            self.set_callback(callback)

    def set_callback(self, callback):
        self.field.textModified.connect(callback)

    def setText(self, text):
        self.field.setText(text)

