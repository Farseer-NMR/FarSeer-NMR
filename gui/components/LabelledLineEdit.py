from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout

class LabelledLineEdit(QWidget):

    def __init__(self, parent, text):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = QLineEdit()

        self.layout().addWidget(label)
        self.layout().addWidget(self.field)