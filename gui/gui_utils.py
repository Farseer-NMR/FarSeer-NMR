from collections import OrderedDict

colours = OrderedDict([('#ff0000','red'),
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
                       ('#666666', 'light grey'),
                       ('#999999', 'grey'),
                       ('#000000', 'black')])


settings_720p = {'peaklistarea_height': 420,
                 'peaklistarea_width': 420,
                 'app_height': 768,
                 'app_width': 1366
                 }
settings_1k = {'peaklistarea_height': 420,
               'peaklistarea_width': 420,
               'app_height': 850,
               'app_width': 1300
               }
settings_2k = {}

def deliver_settings(resolution):
    if resolution == (768, 1366):
        return settings_720p
    elif resolution == (1920, 1080):
        return settings_1k