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

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.WetHandler import WetHandler as fsw

class SinglePlot(PlottingBase):
    """
    Plots a single plot with single subplot.
    """
    
    def __init__(
            self,
            data,
            data_info,
            config=None,
            data_extra=None,
            **kwargs
            ):
        
        super().__init__(data, data_info, config=config, **kwargs)
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("ExperimentPlot initiated")
        
        self.data_extra = data_extra
        
        self.nun_subplots = None
    
    def _calcs_numsubplots(self):
        """
        Exists to maintain integrity with PlottingBase.
        """
        self.num_subplots = 1
        
        return
    
    def plot(self):
        """Runs all operations to plot."""
        self.draw_figure() # from PlottingBase
        self.plot_subplots()
        self.adjust_subplots()
        self.clean_subplots()
        return
    
    def plot_subplots(self):
        
        self.subplot(self.axs[0], self.data, self.data_info)
