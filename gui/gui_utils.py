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
from collections import OrderedDict
import os
import json
from matplotlib import colors as mcolors

GUI_DIR = os.path.dirname(__file__)

defaults = json.load(open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'core', 'default_config.json'),
    'r'
    ))

line_styles = ['-', '--', '-.', ':', 'o']

# https://matplotlib.org/examples/color/named_colors.html
matplt_colours_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

colours = OrderedDict(sorted(
    matplt_colours_dict.items(),
    key=lambda x: tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(x[1])[:3]))
    ))

keylist = list(colours.keys())

for key in keylist:
    if len(key) == 1:
        colours.pop(key, None)

hex_to_colour_dict = {value: key for key, value in colours.items()}

single_char_color = {
    "k":"#000000",
    "w":"#FFFFFF",
    "r":"#FF0000",
    "y":"#FFFF00",
    "g":"#008000",
    "c":"#00FFFF",
    "b":"#0000FF",
    "m":"#FF00FF"
    }

colours.update(single_char_color)

settings_1280x800 = {
    'peaklistarea_height': 350,
    'peaklistarea_width': 920,
    'scene_width': 910,
    'scene_height': 346,
    'app_height': 700,
    'app_width': 1200,
    'sideBar_height': 510,
    'interface_top_width': 920,
    'interface_top_height': 150,
    'footer_height': 10
}
settings_720p = {
    'peaklistarea_height': 350,
    'peaklistarea_width': 920,
    'scene_width': 910,
    'scene_height': 346,
    'app_height': 600,
    'app_width': 1200,
    'sideBar_height': 510,
    'interface_top_width': 920,
    'interface_top_height': 150,
    'footer_height': 60
}
settings_1k = {
    'peaklistarea_height': 510,
    'peaklistarea_width': 920,
    'scene_width': 910,
    'scene_height': 545,
    'app_height': 880,
    'app_width': 1500,
    'sideBar_height': 780,
    'interface_top_width': 1158,
    'interface_top_height': 200,
    'footer_height': 60
    }
settings_2k = {
    'peaklistarea_height': 640,
    'peaklistarea_width': 800,
    'scene_width': 910,
    'scene_height': 346,
    'app_height': 950,
    'app_width': 1700,
    'sideBar_height': 855,
    'interface_top_height': 200,
    'interface_top_width': 1345,
    'footer_height': 60
}
font_weights = [
    "light",
    "normal",
    "medium",
    "semibold",
    "bold",
    "heavy",
    "black"
]


def deliver_settings(resolution):

    if (resolution.height(), resolution.width()) == (1440, 2560):
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_2k.qss')).read()
        return settings_2k, stylesheet
    elif (resolution.height(), resolution.width()) == (1080, 1920) or \
            1040 < resolution.height() < 1440:
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_1k.qss')).read()
        return settings_1k, stylesheet
    elif (resolution.height(), resolution.width()) == (800, 1280):
        msg = " @@@@@@@@@@@@@@@@@@@@@@ \nATTENTION YOU WILL BE USING A PROTOTYPE GUI DEVELOPED ONLY TO BE FUNCTIONAL IN 1280X800 SCREENS. IT IS NOT SUPPOSED TO HAVE A GOOD LOOK.\n@@@@@@@@@@@@@@@@@@@@@@"
        print(msg)
        stylesheet = open(os.path.join(GUI_DIR,
                                       'stylesheet_1280x800.qss')).read()
        return settings_1280x800, stylesheet
    else:
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_720p.qss')).read()
        return settings_720p, stylesheet

# get_colour is used in Test scripts
# variables are loaded into config using ColourBox.get_colour()
def get_colour(colour):
    """
    Defines how to read a colour.
    """
    if colour.startswith('#'):
        if colour.upper() in hex_to_colour_dict:
            return hex_to_colour_dict[colour.upper()]
        else:
            colours[colour.upper()] = colour.upper()
            return colour.upper()
        
    elif colour in colours:
        return colour
    
    else:
        return "black"
