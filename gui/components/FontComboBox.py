from gui.components.LabelledCombobox import LabelledCombobox
from gui.gui_utils import colours
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5 import QtCore

import matplotlib.font_manager
flist = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
items = sorted(list(set([matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist])))

def get_font_from_file(fname):
    return matplotlib.font_manager.FontProperties(fname=fname).get_name()

class FontComboBox(LabelledCombobox):

    def __init__(self, parent, text=None):
        LabelledCombobox.__init__(self, parent, text, items)

    def select(self, text):
        font = get_font_from_file(matplotlib.font_manager.findfont(text))
        index = self.fields.findText(font, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.fields.setCurrentIndex(index)
