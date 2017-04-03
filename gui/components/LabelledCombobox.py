from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout

class LabelledCombobox(QWidget):

    def __init__(self, parent, text, items):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.fields = QComboBox()
        self.fields.addItems(items)

        self.layout().addWidget(label)
        self.layout().addWidget(self.fields)