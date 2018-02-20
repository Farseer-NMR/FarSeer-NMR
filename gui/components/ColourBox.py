"""
Copyright © 2017-2018 Farseer-NMR
Simon P. Skinner and João M.C. Teixeira

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

Farseer-NMR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Farseer-NMR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
"""
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5 import QtCore

from gui.components.LabelledCombobox import LabelledCombobox
from gui.gui_utils import colours, hex_to_colour_dict

class ColourBox(LabelledCombobox):
    """
    A convenience subclass of Labelled Combobox, which is populated with all
    the colours available in Matplotlib. Each colour is listed with a pixmap
    which shows an on-screen representation of the colour.
    """
    def __init__(self, parent, text=None):
        LabelledCombobox.__init__(self, parent, text)
        for item in colours.items():
            pix = QPixmap(QtCore.QSize(20, 20))
            pix.fill(QColor(item[1]))
            self.fields.addItem(QIcon(pix), item[0])
    
    def get_colour(self, colour):
        """
        Defines how to read a colour.
        """
        if colour.startswith('#'):
            if colour.upper() in hex_to_colour_dict:
                self.select(hex_to_colour_dict[colour.upper()])
            else:
                colours[colour.upper()] = colour.upper()
                pix = QPixmap(QtCore.QSize(20, 20))
                pix.fill(QColor(colour.upper()))
                self.fields.addItem(QIcon(pix), colour.upper())
                self.select(colour.upper())
            
        elif colour in colours:
            self.select(colour)
        
        else:
            self.select("black")
    
