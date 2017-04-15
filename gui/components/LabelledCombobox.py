from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout

class LabelledCombobox(QWidget):

    def __init__(self, parent, text, items=None):

        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        label = QLabel(text)
        self.fields = QComboBox()
        if items:
            self.fields.addItems(items)

        self.layout().addWidget(label)
        self.layout().addWidget(self.fields)