"""
Copyright © 2017-2018 Farseer-NMR

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
#from abc import ABCMeta, abstractmethod

from math import ceil
from matplotlib import pyplot as plt

import core.fslibs.Logger as Logger


class PlottingBase:
    """
    Plotting base class with methods common to all plots.
    
    Not functional on its own.
    
    Parameters:
        - data (np.array(dtype=int) of shape [z,y,x]): multidimensional array
            containain the dataset to be plot. Where:
                X) is the column containing the calculated or observed NMR
                    parameter to be used as Y axis in plots,
                Y) are rows containing the X information for each residue
                Z) is [Y,X] for each experiment.
            Data can be further treated with data_select() method.
        
        - data_info (np.array(dtype=str) of shape [z,y,x]): same as <data>
            but for columns ResNo, 1-letter, 3-letter, Peak Status, Merit,
            Fit Method, Vol. Method, Details; in this order.
        
        - config (opt, dict): a dictionary containing all the configuration
            parameters required for this plotting routine. If None provided
            uses the default configuration. Access the default configuration
            via the plotbase_config class attribute.
        
        - additional kwargs can be passed as **kwargs.
    """
    
    info_cols={
        "ResNo":0,
        "1-letter":1,
        "3-letter":2,
        "Peak Status":3,
        "Merit":4,
        "Fit Method":5,
        "Vol. Method":6,
        "Details":7,
        "ATOM":8
        }
    
    plotbase_config = {
        "figure_header":"No header provided",
        "header_fontsize":5,
        "figure_path":"my_plot.pdf",
        "figure_dpi":300,
        "fig_height": 11.69,
        "fig_width": 8.69
        }
    
    def __init__(self, data, data_info, config=None, **kwargs):
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("ExperimentPlot initiated")
        
        self.data = data
        self.data_info = data_info
        self.kwargs = kwargs
        
        self.logger.debug("Shape of data matrix: {}".format(self.data.shape))
        self.logger.debug("Shape of data info: {}".format(self.data_info.shape))
        #self.logger.debug("Kwargs: {}".format(self.kwargs))
        
        if config:
            self.config = {
                **self.plotbase_config,
                **self.default_config,
                **config
                }.copy()
        else:
            self.config = {
                **self.plotbase_config,
                **self.default_config
                }.copy()
        
        self.logger.debug("Configuration dictionary \n{}".format(self.config))
        
        self.figure = None
        self.axs = None
        self.len_axs = None
        
        #super().__init__()
    
    def _hex_to_RGB(self, hexx):
        """
        This function was taken from:
        Copyright 2017 Ben Southgate
        https://github.com/bsouthga/blog
        
        The MIT License (MIT)
        
        Permission is hereby granted, free of charge,
        to any person obtaining a copy of this software and associated
        documentation files (the "Software"), to deal in the Software
        without restriction, including without limitation the rights to
        use, copy, modify, merge, publish, distribute, sublicense,
        and/or sell copies of the Software, and to permit persons to
        whom the Software is furnished to do so, subject to the
        following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
        OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
        NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
        HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
        WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
        FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
        OTHER DEALINGS IN THE SOFTWARE.

        "#FFFFFF" -> [255,255,255]
        """
        # if clause not part of the original function, added for the Farseer-NMR Project.
        if not(hexx.startswith("#") and len(hexx) == 7):
            msg = "The input colour is not in HEX format."
            self._abort(fsw(msg_title="ERROR", msg=msg, wet_num=27))
        # Pass 16 to the integer function for change of base
        return [int(hexx[i:i+2], 16) for i in range(1,6,2)]

    def _RGB_to_hex(self, RGB):
        """
        This function was taken verbatim from:
        Copyright 2017 Ben Southgate
        https://github.com/bsouthga/blog
        
        The MIT License (MIT)
        
        Permission is hereby granted, free of charge,
        to any person obtaining a copy of this software and associated
        documentation files (the "Software"), to deal in the Software
        without restriction, including without limitation the rights to
        use, copy, modify, merge, publish, distribute, sublicense,
        and/or sell copies of the Software, and to permit persons to
        whom the Software is furnished to do so, subject to the
        following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
        OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
        NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
        HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
        WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
        FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
        OTHER DEALINGS IN THE SOFTWARE.
        
        [255,255,255] -> "#FFFFFF"
        """
        # Components need to be integers for hex to make sense
        RGB = [int(x) for x in RGB]
        hexx = "#"+"".join(
            ["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB]
            )
        return hexx
    
    def _color_dict(self, gradient):
        """
        This function was taken verbatim from:
        Copyright 2017 Ben Southgate
        https://github.com/bsouthga/blog
        
        The MIT License (MIT)
        
        Permission is hereby granted, free of charge,
        to any person obtaining a copy of this software and associated
        documentation files (the "Software"), to deal in the Software
        without restriction, including without limitation the rights to
        use, copy, modify, merge, publish, distribute, sublicense,
        and/or sell copies of the Software, and to permit persons to
        whom the Software is furnished to do so, subject to the
        following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
        OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
        NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
        HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
        WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
        FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
        OTHER DEALINGS IN THE SOFTWARE.
        
        Takes in a list of RGB sub-lists and returns dictionary of
        colors in RGB and hex form for use in a graphing function
        defined later on.
        """
        d = {
            "hex":[self._RGB_to_hex(RGB) for RGB in gradient],
            "r":[RGB[0] for RGB in gradient],
            "g":[RGB[1] for RGB in gradient],
            "b":[RGB[2] for RGB in gradient]
            }
        
        return d
    
    
    def _linear_gradient(self, start_hex, finish_hex="#FFFFFF", n=10):
        """
        This function was taken verbatim from:
        Copyright 2017 Ben Southgate
        https://github.com/bsouthga/blog
        
        The MIT License (MIT)
        
        Permission is hereby granted, free of charge,
        to any person obtaining a copy of this software and associated
        documentation files (the "Software"), to deal in the Software
        without restriction, including without limitation the rights to
        use, copy, modify, merge, publish, distribute, sublicense,
        and/or sell copies of the Software, and to permit persons to
        whom the Software is furnished to do so, subject to the
        following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
        OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
        NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
        HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
        WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
        FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
        OTHER DEALINGS IN THE SOFTWARE.
        
        returns a gradient list of (n) colors between
        two hex colors. start_hex and finish_hex
        should be the full six-digit color string,
        inlcuding the number sign ("#FFFFFF")
        """
        # Starting and ending colors in RGB form
        s = self._hex_to_RGB(start_hex)
        f = self._hex_to_RGB(finish_hex)
        # Initilize a list of the output colors with the starting color
        RGB_list = [s]
        # Calcuate a color at each evenly spaced value of t from 1 to n
        for t in range(1, n):
            # Interpolate RGB vector for color at the current value of t
            curr_vector = [
                int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
                for j in range(3)
            ]
            # Add it to our list of output colors
            RGB_list.append(curr_vector)
        
        return self._color_dict(RGB_list)
    
    def _config_fig(self):
        """
        Calculates number of subplot rows per page based on
        user data and settings.
        
        Returns:
            - numrows (int): number of total rows
            - real_fig_height (float, inches): final figure height
        """
        
        numrows = ceil(self.num_subplots/self.config["cols_page"]) + 1 
        
        real_fig_height = \
            (self.config["fig_height"] / self.config["rows_page"]) \
                * numrows
        
        return numrows, real_fig_height
    
    def draw_figure(self):
        """
        Draws the figure architecture.
        
        Defines the size of the figure and subplots based
        on the data to plot.
        
        Returns:
            - None.
        
        Stores :
            - self.figure: Figure object.
            - self.axs: axes of the figure (in case matplotlib is used).
            - self.len_axs (int): the number of subplots created in the
                figure object.
        """
        self._calcs_numsubplots()
        
        numrows, real_fig_height = self._config_fig()
        
        # http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
        self.figure, self.axs = plt.subplots(
            nrows=numrows,
            ncols=self.config["cols_page"],
            figsize=(self.config["fig_width"], real_fig_height)
            )        
        self.axs = self.axs.ravel()
        self.len_axs = len(self.axs)
        plt.tight_layout(
            rect=[0.01,0.01,0.995,0.995]
            )
        
        self.logger.debug("Figure drawn correctly")
        
        return
    
    def clean_subplots(self):
        """ Removes unsed subplots."""
        self.logger.debug("Length Axes: {}".format(self.len_axs))
        for i in range(self.num_subplots, self.len_axs):
            self.axs[i].remove()
    
    def adjust_subplots(self):
        self.figure.subplots_adjust(
            hspace=self.config["hspace"],
            wspace=self.config["wspace"]
            )
    
    def save_figure(self, path=''):
        """Saves figure to path"""
        
        path = path or self.config["figure_path"]
        
        self.figure.text(
            0.01,
            0.01,
            self.config["figure_header"],
            fontsize=self.config["header_fontsize"]
            )
        
        self.figure.savefig(
            path,
            dpi=self.config["figure_dpi"]
            )
        
        
        self.logger.info("**Saved plot figure** {}".format(path))
        
        return
    
    
if __name__ == "__main__":
    
    print(__name__)
