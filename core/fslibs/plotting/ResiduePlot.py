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
import numpy as np

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.WetHandler import WetHandler as fsw

class ResiduePlot(PlottingBase):
    """
    Defines a class for plots where each subplot represents the evolution
    of an given paramenter for a single residue along the whole series.
    
    Not functional on its own.
    """
    def __init__(self,
            data,
            data_info,
            config=None,
            exp_names=None,
            **kwargs
            ):
        super().__init__(data, data_info, config=config, **kwargs)
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("ResiduePlot initiated")
        
        if exp_names:
            self.exp_names = exp_names
        else:
            self.exp_names = [str(i) for i in range(data.shape[0])]
        
        self.logger.debug("Exp names set to: {}".format(self.exp_names))
        
        self.num_subplots = None
        
        return
    
    def _calcs_numsubplots(self):
        """
        Calculates the total number of subplots to be plotted
        based on the user data.
        
        Returns:
            - None
            
        Stores:
            - self.num_subplots (int)
        """
        self.num_subplots = self.data.shape[1]
        self.logger.debug("Number of subplots: {}".format(self.num_subplots))
        
        return
        
    
    def plot(self):
        """Runs all operations to plot."""
        self.draw_figure() # from PlottingBase
        self.plot_subplots()
        self.adjust_subplots()
        self.clean_subplots()
        return
    
    def plot_subplots(self):
        
        for i in range(self.data.shape[1]):
            
            self.subplot(
                self.axs[i],
                self.data[:,i],
                self.data_info[:,i,:]
                )
        
        return

if __name__ == "__main__":
    
    print(__name__)
