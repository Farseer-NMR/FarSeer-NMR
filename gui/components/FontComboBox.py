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
from PyQt5 import QtCore
import matplotlib.font_manager

from gui.components.LabelledCombobox import LabelledCombobox

fonts = [
         'Agency FB',
         'Algerian',
         'Arial',
         'Arial Rounded MT Bold',
         'Arial Unicode MS',
         'Baskerville Old Face',
         'Bauhaus 93',
         'Bell MT',
         'Berlin Sans FB',
         'Berlin Sans FB Demi',
         'Bernard MT Condensed',
         'Blackadder ITC',
         'Bodoni MT',
         'Book Antiqua',
         'Bookman Old Style',
         'Bookshelf Symbol 7',
         'Bradley Hand ITC',
         'Britannic Bold',
         'Broadway',
         'Brush Script MT',
         'Calibri',
         'Californian FB',
         'Calisto MT',
         'Cambria',
         'Candara',
         'Castellar',
         'Centaur',
         'Century',
         'Century Gothic',
         'Century Schoolbook',
         'Chiller',
         'Colonna MT',
         'Comic Sans MS',
         'Consolas',
         'Constantia',
         'Cooper Black',
         'Copperplate Gothic Bold',
         'Copperplate Gothic Light',
         'Corbel',
         'Courier New',
         'Curlz MT',
         'Ebrima',
         'Edwardian Script ITC',
         'Elephant',
         'Engravers MT',
         'Eras Bold ITC',
         'Eras Demi ITC',
         'Eras Light ITC',
         'Eras Medium ITC',
         'Felix Titling',
         'Footlight MT Light',
         'Forte',
         'Franklin Gothic Book',
         'Franklin Gothic Demi',
         'Franklin Gothic Demi Cond',
         'Franklin Gothic Heavy',
         'Franklin Gothic Medium',
         'Franklin Gothic Medium Cond',
         'Freestyle Script',
         'French Script MT',
         'Gabriola',
         'Gadugi',
         'Garamond',
         'Georgia',
         'Gigi',
         'Gill Sans MT',
         'Gill Sans MT Condensed',
         'Gill Sans MT Ext Condensed Bold',
         'Gill Sans Ultra Bold',
         'Gill Sans Ultra Bold Condensed',
         'Gloucester MT Extra Condensed',
         'Goudy Old Style',
         'Goudy Stout',
         'Haettenschweiler',
         'Harlow Solid Italic',
         'Harrington',
         'High Tower Text',
         'Impact',
         'Imprint MT Shadow',
         'Informal Roman',
         'Javanese Text',
         'Jokerman',
         'Juice ITC',
         'Kristen ITC',
         'Kunstler Script',
         'Leelawadee',
         'Leelawadee UI',
         'Lucida Bright',
         'Lucida Calligraphy',
         'Lucida Console',
         'Lucida Fax',
         'Lucida Handwriting',
         'Lucida Sans',
         'Lucida Sans Typewriter',
         'Lucida Sans Unicode',
         'MS Outlook',
         'MS Reference Sans Serif',
         'MS Reference Specialty',
         'MT Extra',
         'MV Boli',
         'Magneto',
         'Maiandra GD',
         'Malgun Gothic',
         'Marlett',
         'Matura MT Script Capitals',
         'Microsoft Himalaya',
         'Microsoft New Tai Lue',
         'Microsoft PhagsPa',
         'Microsoft Sans Serif',
         'Microsoft Tai Le',
         'Microsoft Uighur',
         'Microsoft Yi Baiti',
         'Mistral',
         'Modern No. 20',
         'Mongolian Baiti',
         'monospace',
         'Monotype Corsiva',
         'Myanmar Text',
         'Niagara Engraved',
         'Niagara Solid',
         'Nirmala UI',
         'OCR A Extended',
         'Old English Text MT',
         'Onyx',
         'Palace Script MT',
         'Palatino Linotype',
         'Papyrus',
         'Parchment',
         'Perpetua',
         'Perpetua Titling MT',
         'Playbill',
         'Poor Richard',
         'Pristina',
         'Rage Italic',
         'Ravie',
         'Rockwell',
         'Rockwell Condensed',
         'Rockwell Extra Bold',
         'Script MT Bold',
         'Segoe MDL2 Assets',
         'Segoe Print',
         'Segoe Script',
         'Segoe UI',
         'Segoe UI Emoji',
         'Segoe UI Historic',
         'Segoe UI Symbol',
         'Showcard Gothic',
         'SimSun-ExtB',
         'Snap ITC',
         'Stencil',
         'Sylfaen',
         'Symbol',
         'Tahoma',
         'Tempus Sans ITC',
         'Times New Roman',
         'Trebuchet MS',
         'Tw Cen MT',
         'Tw Cen MT Condensed',
         'Tw Cen MT Condensed Extra Bold',
         'Verdana',
         'Viner Hand ITC',
         'Vivaldi',
         'Vladimir Script',
         'Webdings',
         'Wide Latin',
         'Wingdings',
         'Wingdings'
         ]

def get_font_from_file(fname):
    return matplotlib.font_manager.FontProperties(fname=fname).get_name()

class FontComboBox(LabelledCombobox):
    """
    A convenience subclass of Labelled Combobox, which is populated with
    the fonts available in matplotlib. To prevent incompatibility between OS
    font availabilities, the common fonts are listed above and used to populate
    the combobox.
    """
    
    def __init__(self, parent, text=None):
        LabelledCombobox.__init__(self, parent, text, fonts)
    
    def select(self, item):
        """Re-implementation of the LabelledCombobox select fonts from list
        faithfully."""
        index = list(self.texts).index(item)
        if index:
            self.fields.setCurrentIndex(index)
