from PyQt5.QtWidgets import QLineEdit


class ValueField(QLineEdit):

    def __init__(self, parent, index, dim, valuesDict):
        QLineEdit.__init__(self, parent)
        self.index = index
        self.dim = dim
        self.textChanged.connect(self.updateValuesDict)
        self.valuesDict = valuesDict

    def updateValuesDict(self, value):
        self.valuesDict[self.dim][self.index] = value