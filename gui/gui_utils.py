from collections import OrderedDict
import os
import json
GUI_DIR = os.path.dirname(__file__)

defaults = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../' 'current', 'default_config.json'), 'r'))

line_styles = ['-', '--', '-.', ':', 'o']

colours = OrderedDict([('#ff0000','red'),
                       ('#8b0000','dark red'),
                       ('#00ffff', 'cyan'),
                       ('#ff8000', 'orange'),
                       ('#0080ff', 'manganese blue'),
                       ('#ffff00', 'yellow'),
                       ('#0000ff', 'blue'),
                       ('#80ff00', 'chartreuse'),
                       ('#8000ff', 'purple'),
                       ('#00ff00', 'green'),
                       ('#ff00ff', 'magenta'),
                       ('#00ff80', 'spring green'),
                       ('#ff0080', 'deep pink'),
                       ('#e7e7e7', 'light grey'),
                       ('#999999', 'grey'),
                       ('#000000', 'black')])


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
font_weights = ["ultralight", "light", "normal", "regular", "book", "medium", "roman", "semibold", "demibold", "demi", "bold", "heavy", "extra bold", "black"]

def deliver_settings(resolution):
    print(resolution)

    if (resolution.height(), resolution.width()) == (1440, 2560):
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_2k.qss')).read()
        print('2k')
        return settings_2k, stylesheet
    elif (resolution.height(), resolution.width()) == (1080, 1920) or 1040 < resolution.height() < 1440:
        print('1k')
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_1k.qss')).read()
        return settings_1k, stylesheet
    else:
        print('720p')
        stylesheet = open(os.path.join(GUI_DIR, 'stylesheet_720p.qss')).read()
        return settings_720p, stylesheet
