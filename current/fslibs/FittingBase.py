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
from abc import ABCMeta, abstractmethod

class FittingBase(metaclass=ABCMeta):
    """
    Fitting base class.
    
    To implement a new fitting formula create a class that inherits
    FittingBase and define its specific funtions (@abstractmethod),
    see HillEquation as example.
    """
    @abstractmethod
    def equation(self, *args):
        """The equation formula to which continuous data is fit."""
        pass
    
    @abstractmethod
    def log_okay(self, *args):
        """
        What to write in the fit_report.log file when fit
        performs correctly.
        """
        pass
    
    @abstractmethod
    def results(self, *args):
        """Row structure of fit_table.csv."""
        pass
    
    @abstractmethod
    def txt_plot(self, *args):
        """Text writen in the FarseerSeries.plot_res_evo() subplots."""
        pass
    
    @abstractmethod
    def results_header(self):
        """Header structure of fit_table.csv."""
        pass
    
    @abstractmethod
    def fit_log_header(self, col):
        """Header for fit_report.log file."""
        pass
    
    # FITTING LOG FILE FAILED:
    def fit_failed(self, res, x, y):
        """What to write in the fit_report.log file when fit fails."""
        s2w = \
"""
ResNo:  {}
xdata: {}
ydata: {}
!¡FIT FAILED TO FIND MINIMIZATION!¡
**************************
""". \
                format(res, list(x), list(y))
        
        return s2w
    
    # NOT ENOUGH DATA
    def not_enough_data(self, res, x, y):
        """
        What to write in the fit_report.log file when
        there isn't enough data to evaluate.
        """
        s2w = \
"""
ResNo:  {}
xdata: {}
ydata: {}
!¡NOT ENOUGH DATA POINTS - FIT NOT PERFORMED!¡
**************************
""". \
                format(res, list(x), list(y))
        
        return s2w
    
    @abstractmethod
    def fit_data(self, *args):
        """Workflow for fitting data with the specific equation."""
        pass

