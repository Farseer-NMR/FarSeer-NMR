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

class ExperimentPlot(PlottingBase):
    """
    Defines a class for plots where each subplot represents the data
    for the whole experiment where X axes are the Residue numbers (labels)
    and Y axes the NMR parameter to be represented.
    
    Not functional on its own.
    """
    def __init__(self,
            data,
            data_info,
            config=None,
            partype="",
            exp_names="",
            **kwargs
            ):
        super().__init__(data, data_info, config=config, **kwargs)
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("ExperimentPlot initiated")
        
        self.logger.debug("Partype Selected: {}".format(partype))
        
        self.ppm_data = False
        self.ratio_data = False
        
        # for ('H1_delta', 'N15_delta', 'CSP')
        if partype == 'ppm' :
            self.ppm_data = True
        
        # for ('Height_ratio','Vol_ratio')
        elif partype == 'ratio':
            self.ratio_data = True
        
        self.logger.debug(
            "PPM and RATIO data types? {} and {}".format(
                self.ppm_data,
                self.ratio_data
                )
            )
        
        if exp_names:
            self.experiment_names = exp_names
        else:
            self.experiment_names = [str(i) for i in range(data.shape[0])]
            
        self.logger.debug("Experiment names: {}".format(self.experiment_names))
        
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
        self.num_subplots = self.data.shape[0]
        self.logger.debug("Number of subplots: {}".format(self.num_subplots))
        
        return
