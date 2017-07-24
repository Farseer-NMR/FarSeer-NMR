from PyQt5.QtWidgets import QWidget, QDoubleSpinBox, QLabel, QHBoxLayout

class LabelledDoubleSpinBox(QWidget):

    def __init__(self, parent, text, callback=None):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.field = QDoubleSpinBox()

        self.layout().addWidget(label)
        self.layout().addWidget(self.field)

        if callback:
            self.set_callback(callback)

    def setValue(self, value):
        if value:
            self.field.setValue(value)
        else:
            self.field.setValue(0)

    def set_callback(self, callback):
        self.field.valueChanged.connect(callback)