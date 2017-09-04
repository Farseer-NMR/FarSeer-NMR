from gui.components.LabelledCombobox import LabelledCombobox
from gui.gui_utils import colours
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5 import QtCore


class ColourBox(LabelledCombobox):

    def __init__(self, parent, text=None):

        LabelledCombobox.__init__(self, parent, text)
        for item in colours.items():
            pix = QPixmap(QtCore.QSize(20, 20))
            pix.fill(QColor(item[0]))
            self.fields.addItem(QIcon(pix), item[1])



