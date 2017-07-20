from PyQt5.QtWidgets import QLineEdit, QSizePolicy


class ValueField(QLineEdit):

    def __init__(self, parent, index, dim, valuesDict):
        QLineEdit.__init__(self, parent)
        self.index = index
        self.dim = dim
        self.textChanged.connect(self.updateValuesDict)
        self.valuesDict = valuesDict
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

    def updateValuesDict(self, value):
        self.valuesDict[self.dim][self.index] = value