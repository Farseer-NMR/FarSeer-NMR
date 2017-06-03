from PyQt5.QtWidgets import QWidget, QDoubleSpinBox, QLabel, QHBoxLayout

class LabelledDoubleSpinBox(QWidget):

    def __init__(self, parent, text):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = QDoubleSpinBox()

        self.layout().addWidget(label)
        self.layout().addWidget(self.field)

    def setValue(self, value):
        if value:
            self.field.setValue(value)
        else:
            self.field.setValue(0)
