from gui.components.LabelledCombobox import LabelledCombobox
from PyQt5 import QtCore

import matplotlib.font_manager
# flist = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
# print(flist)
# # items = sorted(list(set([matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in flist])))


def getFonts():
    """Get the current list of system fonts"""

    import matplotlib.font_manager
    l = matplotlib.font_manager.get_fontconfig_fonts()
    fonts = [matplotlib.font_manager.FontProperties(fname=fname).get_name() for fname in l]
    fonts = list(set(fonts))
    fonts.sort()
    return fonts

def get_font_from_file(fname):
    return matplotlib.font_manager.FontProperties(fname=fname).get_name()

class FontComboBox(LabelledCombobox):

    def __init__(self, parent, text=None):
        LabelledCombobox.__init__(self, parent, text, getFonts())

    def select(self, text):
        font = get_font_from_file(matplotlib.font_manager.findfont(text))
        index = self.fields.findText(font, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.fields.setCurrentIndex(index)
