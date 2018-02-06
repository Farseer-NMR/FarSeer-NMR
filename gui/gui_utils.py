from collections import OrderedDict
import os
import json
from matplotlib import colors as mcolors
GUI_DIR = os.path.dirname(__file__)



line_styles = ['-', '--', '-.', ':', 'o']

## https://matplotlib.org/examples/color/named_colors.html
matplt_colours_dict = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

colours = OrderedDict(sorted(matplt_colours_dict.items(),
                             key=lambda x: tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(x[1])[:3]))))

keylist = list(colours.keys())

hex_to_colour_dict = {value: key for key, value in colours.items()}

for key in keylist:
    if len(key) == 1:
        colours.pop(key, None)



settings_1280x800 = {'peaklistarea_height': 350,
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
settings_720p = {'peaklistarea_height': 350,
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
settings_1k = {'peaklistarea_height': 510,
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
settings_2k = {'peaklistarea_height': 640,
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
font_weights = ["light", "normal", "medium", "semibold", "bold", "heavy", "black"]

def deliver_settings(resolution):

    if (resolution.height(), resolution.width()) == (1440, 2560):
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_2k.qss')).read()
        print('2k')
        return settings_2k, stylesheet
    elif (resolution.height(), resolution.width()) == (1080, 1920) or 1040 < resolution.height() < 1440:
        print('1k')
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_1k.qss')).read()
        return settings_1k, stylesheet
    elif (resolution.height(), resolution.width()) == (800, 1280):
        print('1280x800')
        msg = " @@@@@@@@@@@@@@@@@@@@@@ \nATTENTION YOU WILL BE USING A PROTOTYPE GUI DEVELOPED ONLY TO BE FUNCTIONAL IN 1280X800 SCREENS. IT IS NOT SUPPOSED TO HAVE A GOOD LOOK.\n@@@@@@@@@@@@@@@@@@@@@@"
        print(msg)
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_1280x800.qss')).read()
        return settings_1280x800, stylesheet
    else:
        print('720p')
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_720p.qss')).read()
        return settings_720p, stylesheet

def get_colour(colour):
    if colour.startswith('#'):
        return hex_to_colour_dict[colour.upper()]
    else:
        return colour
