from PyQt5.QtWidgets import QWidget, QSpinBox, QLabel, QHBoxLayout

class LabelledSpinBox(QWidget):

    def __init__(self, parent, text):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = QSpinBox()
        self.field.setMaximum(10000)
        self.field.setMinimum(-10000)

        self.layout().addWidget(label)
        self.layout().addWidget(self.field)