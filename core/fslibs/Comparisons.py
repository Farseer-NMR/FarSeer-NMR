"""
Copyright © 2017-2018 Farseer-NMR
João M.C. Teixeira and Simon P. Skinner

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
#import logging
#import logging.config
import numpy as np
import pandas as pd
import core.fslibs.Logger as Logger
from core.fslibs.WetHandler import WetHandler as fsw

class Comparisons:
    """
    Prepares parsed data along next and previous axis of the calculation.
    
    Given a dictionary containing all the series (FarseerSeries) along
    a given axis of the Farseer-NMR Cube, the Comparisons class stores
    that dictionary and parses it along the two other axis (next and prev)
    so that, for example, data generated along X can be compared along
    Y and Z, where Y is the next axis of X and Z and previous axis of X.
    
    Different dictionaries are stored for next and previous parsed axes.
    
    Parameters:
        dimension (str): identifies the main dimension axis of the class
            where X = along_x, Y = along_y, Z = along_z
        
        hyper_panel (5-dimension pandas.Panel): converted from dictionary     
            stores all the main axis series.
        
        other_dim_keys (lst): ordered list containing the previous and next
            dimension names, same nomenclature as 'dimension'.
        
        all_next_dim (dict): stores all the series of parsed data along
            the next dimension. Series are parsed from hyper_panel.
        
        all_prev_dim (dict): same as all_next_dim but for the previous axis.
        
        has_points_next_dim (bool): True if points are found along the
            next dimension. False by default.
        
        has_points_prev_dim (bool): True if points are found along the
            previous dimension. False by default.
        
        log (str): stores the whole log.
        
        log_export_onthefly (bool): Flag that activates on-the-fly log
            on an external file.
        
        log_export_name (str): the name of the external log file that is
            written on-the-fly.
    
    Methods:
        .log_r()
        .exports_log()
        .abort()
        .gen_next_dim()
        .gen_prev_dim()
        .transfer_log()
    """
    def __init__(
            self,
            dimension_dict,
            selfdim='cond',
            other_dim_keys=['condy','condz']):
        """
        Parameters:
            dimension_dict (dict): is a dictionary containing all the
            series for the main dimension.
        """
        self.logger = logging.getLogger(__name__)
        logging.config.dictConfig(fslogconf.farseer_log_config)
        self.logger.debug('logger initiated')
        
        self.p5d = pd.core.panelnd.create_nd_panel_factory(
            klass_name='Panel5D',
            orders=['cool', 'labels', 'items', 'major_axis', 'minor_axis'],
            slices={
                'labels': 'labels',
                'items': 'items',
                'major_axis': 'major_axis',
                'minor_axis': 'minor_axis'
                    },
            slicer=pd.Panel4D,
            aliases={'major': 'index', 'minor': 'minor_axis'},
            stat_axis=2
            )
        # condition/dimension over which the calculations where
        # performed
        self.dimension = selfdim
        self.hyper_panel = self.p5d(dimension_dict)
        # stores the dimension keys over which the comparisons
        # will be performed
        self.other_dim_keys = other_dim_keys
        # the dictionaries containing the fss.FarseerSeries of the dimensions
        # along which to be compared.
        self.all_next_dim = {}
        self.all_prev_dim = {}
        # initially considers that there are no points to compare with
        # in the labels and cool dimensions
        # becomes true after gen_comparison_*()
        self.has_points_next_dim = False
        self.has_points_prev_dim = False
        self.log = ''  # all log goes here
        self.log_export_onthefly = False
        self.log_export_name = 'Comparison_log.md'
    
    def log_r(self, logstr, istitle=False):
        """
        Registers the log and prints to the user.
        
        Parameters:
            logstr: the string to be registered in the log
            
            istitle: is True, formats logstr as a title
        """
        
        if istitle:
            logstr = \
"""
{0}  
{1}  
{0}  
""".\
                format('*'*79, logstr)
        
        else:
            logstr += '  \n'
        
        print(logstr)
        self.log += logstr
        # appends log to external file on the fly
        
        if self.log_export_onthefly:
            with open(self.log_export_name, 'a') as logfile:
                logfile.write(logstr)
        
        return
    
    def exports_log(self, mod='w', logfile_name='Comparison_log.md'):
        """ Exports log to external file. """
        
        with open(logfile_name, mod) as logfile:
            logfile.write(self.log)
        
        return
    
    def abort(self, wet):
        """
        Aborts run with message. Writes message to log.
        
        Parameters:
            - wet (WetHandler)
        """
        self.log_r(wet.wet)
        self.log_r(wet.abort_msg())
        wet.abort()
        
        return
        
    def gen_next_dim(self, series_class, comp_kwargs):
        """
        Generates dictionary with the Series parsed along the next
        dimension of the <self.dimension>.
        
        Parameters:
            series_class (class): fss.FarseerSeries.
            comp_kwargs (dict): kwargs to initiate FarseerSeries.
        
        Returns:
            None.
            
        Modifies Arg:
            all_next_dim (dict)
        """
        
        self.log_r(
            'GENERATING COMPARISONS FOR **{}** ALONG {}: {}'.format(
                    self.dimension,
                    self.other_dim_keys[0],
                    list(self.hyper_panel.labels)
                    ),
            istitle=True
            )
        
        if len(self.hyper_panel.labels) > 1:
            for dp2 in self.hyper_panel.items:
                self.all_next_dim.setdefault(dp2, {})
                
                for dp1 in self.hyper_panel.cool:
                    comparison = series_class(
                        np.array(self.hyper_panel.loc[dp1,:,dp2,:,:]),
                        items=self.hyper_panel.labels,
                        minor_axis=self.hyper_panel.minor_axis,
                        major_axis=self.hyper_panel.major_axis
                        )
                    comparison.create_attributes(
                        series_axis='C{}'.format(self.dimension[-1]), 
                        series_dps=self.hyper_panel.labels, 
                        next_dim=dp1,
                        prev_dim=dp2,
                        dim_comparison=self.other_dim_keys[0],
                        **comp_kwargs
                        )
                    self.all_next_dim[dp2].setdefault(dp1, comparison)
            
            self.log_r('** Generated comparison dictionary')
            self.has_points_next_dim = True
        
        elif len(self.hyper_panel.labels) <= 1:
            self.log_r('*** There are no points to compare along {}'.\
                format(self.other_dim_keys[0]))
        
        return
    
    def gen_prev_dim(self, series_class, comp_kwargs):
        """
        Generates dictionary with the Series parsed along the previous
        dimension of the <self.dimension>.
        
        Parameters:
            series_class (class): fss.FarseerSeries.
            comp_kwargs (dict): kwargs to initiate FarseerSeries.
        
        Returns:
            None.
            
        Modifies Arg:
            all_prev_dim (dict)
        """
        
        self.log_r(
            'GENERATING COMPARISONS FOR **{}** ALONG {}: {}'.format(
                    self.dimension,
                    self.other_dim_keys[1],
                    list(self.hyper_panel.cool)
                    ),
            istitle=True
            )
        
        if len(self.hyper_panel.cool) > 1:
            for dp2 in self.hyper_panel.labels:
                self.all_prev_dim.setdefault(dp2, {})
                
                for dp1 in self.hyper_panel.items:
                    comparison = series_class(
                        np.array(self.hyper_panel.loc[:,dp2,dp1,:,:]),
                        items=self.hyper_panel.cool,
                        minor_axis=self.hyper_panel.minor_axis,
                        major_axis=self.hyper_panel.major_axis
                        )
                    comparison.create_attributes(
                        series_axis='C{}'.format(self.dimension[-1]), 
                        series_dps=self.hyper_panel.cool, 
                        next_dim=dp1,
                        prev_dim=dp2,
                        dim_comparison=self.other_dim_keys[1],
                        **comp_kwargs
                        )
                    self.all_prev_dim[dp2].setdefault(dp1, comparison)
            
            self.log_r('** Generated comparison dictionary')
            self.has_points_prev_dim = True
            
        elif len(self.hyper_panel.labels) <= 1:
            self.log_r('*** There are no points to compare along {}'.\
                format(self.other_dim_keys[1]))
        
        return
    
    def transfer_log(self):
        """
        Transfers logs from the Series objects in self.all_prev_dim
        and self.all_next_dim to the main class object.
        """
        
        if self.has_points_next_dim:
            for dim2_pt in sorted(self.all_next_dim.keys()):
                for dim1_pt in sorted(self.all_next_dim[dim2_pt].keys()):
                    self.log += self.all_next_dim[dim2_pt][dim1_pt].log
        
        if self.has_points_prev_dim:
            for dim2_pt in sorted(self.all_prev_dim.keys()):
                for dim1_pt in sorted(self.all_prev_dim[dim2_pt].keys()):
                    self.log += self.all_prev_dim[dim2_pt][dim1_pt].log
        
        return


