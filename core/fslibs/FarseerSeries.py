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
import logging
import logging.config
import glob
import os
import numpy as np
import pandas as pd
import itertools as it
from pydoc import locate
from math import ceil
from matplotlib import pyplot as plt
import datetime 

import core.fslibs.log_config as fslogconf
from core.fslibs import wet as fsw

class FarseerSeries(pd.Panel):
    """
    A series of NMR experiments.
    
    Inherits a pd.Panel. Each DataFrame is an experiment (peaklist)
    and progression along panel.items is the evolution of the series
    along an experimental variable.
    
    Attributes:
        calc_folder (str): folder name to store calculations.
        
        comparison_folder (str): folder name to store comparisons.
        
        tables_and_plots_folder (str): subfolder name to store tables
            and plots resulting from the calculations.
        
        chimera_att_folder (str): subfolder name to store UCSF Chimera 
            Attribute files
        
        export_series_folder (str): subfolder name to store the series
            peaklists after all restraints are calculated.
        
        calc_path (str): the absolute path to store calculation results.
        
        series_axis (str): identifies the main axis of the series,
            where X = along_x, Y = along_y, Z = along_z
        
        series_datapoints (list): ordered list with the names of the
            series data points.
            
        next_dim (str): the name of the next dimension. For X is Y.
        
        prev_dim (str): the name of the previous dimension. For X is Z.
        
        dim_comparison (str): if the series corresponds to a parsed 
            comparison, the name of the dimension along which is
            compared.
        
        resonance_type (str): {'Backbone', 'Sidechains'}
        
        res_info (pd.Panel): a copy of the residue information and 
            measurement status.
        
        restraint_list (list): ORDERED names of the restraints that can
            be calculated.
        
        cs_missing (str): {'prev', 'full', 'zero'}, how to represent bars
            for missing residues.
            
        csp_alpha4res (dict): a dictionary containing the alpha values
            to be used for each residue in the CSP calculation formula.
        
        fitdf (dict): stored pd.DataFrames with information on fitting.
        fit_performed (bool): defaults False. True after .perform_fit().
    
    Methods:
        
        Initiates:
            .create_attributes()
            .log_r()
            .exports_log()
            .abort()
        
        Calculation:
            .calc_ratio()
            .calc_cs_diffs()
            .calc_csp()
                .csp_willi()
            .perform_fit()
            .load_theoretical_PRE()
            .calc_Delta_PRE()
        
        Creates Plot:
            .plot_base()
        
            Subplot routines:
                .plot_bar_horizontal()
                .plot_bar_vertical()
                .plot_res_evo()
                .plot_cs_scatter()
                .plot_cs_scatter_flower()
                .plot_DPRE_heatmap()
                .plot_DPRE_plot()
            
            Subplot add-ons:
                .set_item_colors()
                .text_marker()
                .plot_threshold()
                .plot_theo_pre()
                    
                    Helper functions:
                        .hex_to_RGB()
                        .RGB_to_hex()
                        .color_dict()
                        .linear_gradient()
            
            Plot finishing:
                .clean_subplots()
                .write_plot()
        
        Exporting resuts:
            .write_table()
            .write_Chimera_attributes()
            .export_series_to_tsv()
    """
    
    # folder names
    calc_folder = 'Calculations'  
    comparison_folder = 'Comparisons'  
    tables_and_plots_folder = 'TablesAndPlots'
    chimera_att_folder = 'ChimeraAttributeFiles'
    export_series_folder = 'FullPeaklists'
    axis_list = ['x','y','z']
    # allowed folder names for paramagnetic series
    paramagnetic_names = ['para', '01_para']
    
    def create_attributes(
            self,
            series_axis='along',
            series_dps=['foo'],
            next_dim='bar',
            prev_dim='zoo',
            dim_comparison='',
            resonance_type='Backbone',
            csp_alpha4res=0.14,
            csp_res_exceptions={'G':0.2},
            cs_missing='prev',
            restraint_list=[
                'H1_delta',
                'N15_delta',
                'CSP',
                'Height_ratio',
                'Vol_ratio'
                ],
            log_export_onthefly=False,
            log_export_name='FarseerSet_log.md'):
        """Creates the instance attributes."""
        
        self.logger = fslogconf.getLogger(__name__)
        logging.config.dictConfig(fslogconf.farseer_log_config)
        self.logger.debug('logger initiated')
        
        self.cs_missing = cs_missing
        # normalization value for F2 dimension.
        self.csp_alpha4res = \
            {key:csp_alpha4res for key in 'ARNDCEQGHILKMFPSTWYV'}
        
        for k, v in csp_res_exceptions.items():
            self.csp_alpha4res[k] = v
        
        # variables that store characteristics of the titration.
        self.series_axis = series_axis
        self.series_datapoints = series_dps
        self.next_dim = next_dim
        self.prev_dim = prev_dim
        self.dim_comparison = dim_comparison
        if self.series_axis.startswith('along') \
                and self.series_datapoints[-1] in self.paramagnetic_names:
            self.para_name = self.series_datapoints[-1]
        else:
            self.para_name = False
        self.resonance_type = resonance_type
        self.res_info = \
            self.loc[:,:,['ResNo','1-letter','3-letter','Peak Status']]
        self.restraint_list = restraint_list
        # dictionary to store dataframes with information on fitting results
        self.fit_plot_text = {}
        self.fit_plot_ydata = {}
        self.fit_okay = {}
        # becomes if perform_fit() runs.
        # affects plot_res_evo()
        self.fit_performed = False 
        self.PRE_loaded = False  # True after .load_theoretical_PRE
        # log related variables
        self.log = ''
        self.log_export_onthefly = log_export_onthefly
        self.log_export_name = log_export_name
        
        # defines the path to store the calculations
        # if stores the result of a calculation
        if series_axis.startswith('along'):
            self.calc_path = '{}/{}/{}/{}/{}'.format(
                self.resonance_type,
                self.calc_folder,
                self.series_axis,
                self.prev_dim,
                self.next_dim
                )
        
        # if stores comparisons among calculations
        elif series_axis.startswith('C'):
            self.calc_path = '{}/{}/{}/{}/{}/{}'.format(
                self.resonance_type,
                self.comparison_folder,
                self.series_axis,
                self.dim_comparison,
                self.prev_dim,
                self.next_dim
                )
        
        # Creates all the folders necessary to store the data.
        # folders are created here when generating the object to avoid having
        # os.makedirs spread over the code, in this way all the folders created
        # are here summarized
        if not(os.path.exists(self.calc_path)):
            os.makedirs(self.calc_path)
        
        self.chimera_att_folder = \
            "{}/{}".format(self.calc_path, self.chimera_att_folder)
        
        if not(os.path.exists(self.chimera_att_folder)):
            os.makedirs(self.chimera_att_folder)
        
        self.tables_and_plots_folder = \
            '{}/{}'.format(self.calc_path, self.tables_and_plots_folder)
        
        if not(os.path.exists(self.tables_and_plots_folder)):
            os.makedirs(self.tables_and_plots_folder)
        
        self.export_series_folder = \
            '{}/{}'.format(self.calc_path, self.export_series_folder)
        
        if not(os.path.exists(self.export_series_folder)):
            os.makedirs(self.export_series_folder)
        
    @property
    def _constructor(self):
        # because Titration inherits a pd.Panel.
        return FarseerSeries
        
    def log_r(self, logstr, istitle=False):
        """
        Registers the log string and prints it.
        
        Parameters:
            logstr (str): the string to be registered in the log.
            
            istitle (bool): flag to format logstr as a title.
        """
        
        if istitle:
            logstr = \
"""
{0}  
{1}  
{0}  
""".format('*'*79, logstr)
        
        else:
            logstr += '  \n'
        
        print(logstr)
        self.log += logstr
        
        # appends log to external file on the fly
        if self.log_export_onthefly:
            with open(self.log_export_name, 'a') as logfile:
                logfile.write(logstr)
        
        return
    
    def exports_log( self, mod='a', path='farseer.log'):
        """Exports log to external file.
        
        Parameters:
            mod (str): python.open() arg mode.
            
            logfile_name (str): the external log file name.
        """
        
        with open(path, mod) as logfile:
            logfile.write(self.log)
        
        return
    
    def abort(self):
        """Aborts run with message."""
        
        self.log_r(fsw.abort_msg)
        fsw.abort()
        
        return
    
    def create_header(self, extra_info="", file_path=""):
        """
        Creates description header for files and plots using "#" as
        comment character.
        
        Differentiates between calculations and comparisons.
        
        Parameters:
            - extra_info (str): additional info that may be relevant for
                the process that calls create_header.
            - file_path (srt): the path where the target file will be
                saved.
            
        Returns:
            - header_1 (str) containing the header.
        """
        
        # discriminates between main calculation or comparison.
        if self.dim_comparison:
            self_axis_index = self.axis_list.index(self.dim_comparison[-1])
            hh_string = '# Parameters/observables analysed along "{}" axis \
and stacked (compared) along "{}" axis'.format(
                self.series_axis[-1].upper(),
                self.dim_comparison[-1].upper()
                )
        
        else:
            self_axis_index = self.axis_list.index(self.series_axis[-1])
            hh_string = '# Parameters/observables analysed along "{}" axis'.\
                format(self.series_axis[-1].upper())
        
        
        header_1 = \
"""{}
# keeping fixed the following data points on the other Farseer-NMR Cube coordinates:
# - along {} axis: "{}" 
# - along {} axis: "{}"
# {}
# 
# Calculation Output Folder: {}
# Original file path: {}
# Creation date: {}
#
""".\
                format(
                    hh_string,
                    self.axis_list[self_axis_index-1],
                    self.prev_dim,
                    self.axis_list[self_axis_index-2],
                    self.next_dim,
                    extra_info,
                    os.getcwd(),
                    file_path,
                    datetime.datetime.now().strftime("%c")
                    )
        
        return header_1
    
    def hex_to_RGB(self, hexx):
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
            self.log_r(fsw.gen_wet("ERROR", msg, 27))
            self.abort()
        # Pass 16 to the integer function for change of base
        return [int(hexx[i:i+2], 16) for i in range(1,6,2)]

    def RGB_to_hex(self, RGB):
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
    
    def color_dict(self, gradient):
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
            "hex":[self.RGB_to_hex(RGB) for RGB in gradient],
            "r":[RGB[0] for RGB in gradient],
            "g":[RGB[1] for RGB in gradient],
            "b":[RGB[2] for RGB in gradient]
            }
        
        return d
    
    
    def linear_gradient(self, start_hex, finish_hex="#FFFFFF", n=10):
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
        s = self.hex_to_RGB(start_hex)
        f = self.hex_to_RGB(finish_hex)
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
        return self.color_dict(RGB_list)
    
    def calc_cs_diffs(self, calccol, sourcecol):
        """
        Calculates the difference between two columns along a Series 
        using as reference the column from the reference experiment, 
        which is always stored in Item=0.
        
        Calculation results are stored in new columns.
        """
        
        self.loc[:,:,calccol] = \
            self.loc[:,:,sourcecol].sub(self.ix[0,:,sourcecol], axis='index')
        
        # sets missing peaks results according to the self.cs_missing
        if self.cs_missing == 'full':
            for item in self.items:
                mask_missing = self.loc[item,:,'Peak Status'] == 'missing'
                self.loc[item,mask_missing,calccol] = 1.
        
        elif self.cs_missing == 'prev':
            for iitem in range(1, len(self.items)):
                mask_missing = self.ix[iitem,:,'Peak Status'] == 'missing'
                self.ix[iitem,mask_missing,calccol] = \
                    self.ix[iitem-1,mask_missing,calccol]
        
        elif self.cs_missing == 'zero':
            for iitem in range(1, len(self.items)):
                mask_missing = self.ix[iitem,:,'Peak Status'] == 'missing'
                self.ix[iitem,mask_missing,calccol] = 0
        
        self.log_r('**Calculated** {}'.format(calccol))
        
        return
    
    def calc_ratio(self, calccol, sourcecol):
        """
        Calculates the ratio between two columns along a series of
        experiments using as reference the column from the reference
        experiment, which is always stored in Item=0.
        
        Calculation result is stored in a new column of each DataFrame.
        """
        
        self.loc[:,:,calccol] = \
            self.loc[:,:,sourcecol].div(self.ix[0,:,sourcecol], axis='index')
        self.log_r('**Calculated** {}'.format(calccol))
        
        return
    
    def csp_willi(self, s):
        """
        Formula that calculates Chemical Shift Perturbations (CSPs).
        
        Parameters:
            s (pd.Series): s[0], 1-letter res code; s[1]; chemical shift 
            for nuclei 1, s[2], chemical shift for nuclei 2.
        
        np.sqrt(0.5*(H1**2 + (alpha*N15)**2))

        where the proportional normalization factor (alpha) for the 15N
        dimension is set by default to 0.2 for Glycine and 0.14 for all
        the other residues.

        Williamson, M. P. Using chemical shift perturbation to
        characterise ligand binding. Prog. Nuc. Magn. Res. Spect.
        73, 1–16 (2013). SEE CORRIGENDUM
        """
        return np.sqrt(0.5*(s[1]**2+(self.csp_alpha4res[s[0]]*s[2])**2))
    
    def calc_csp(self, calccol='CSP', pos1='PosF1_delta', pos2='PosF2_delta'):
        """
        Calculates the Chemical Shift Perturbation (CSP) values
        based on a formula.
        
        calccol (str): the name of the new column that stores results.
        pos1 (str): the column name of the source data for nuclei 1.
        pos2 (str): the column name for the source data for nuclei 2.
        """

        self.loc[:,:,calccol] = \
            self.loc[:,:,['1-letter',pos1,pos2]].\
                apply(lambda x: self.csp_willi(x), axis=2)
        self.log_r('**Calculated** {}'.format(calccol))
        
        return
    
    def load_theoretical_PRE(self, spectra_path, datapoint):
        """
        Loads theoretical PRE values to represent in bar plots.
        
        Theorital PRE files (*.pre) should be stored in a '01_para' 
        or 'para' folder at the along_z hierarchy level.
        
        Reads information on the tag position stored in the
        *.pre file as an header comment, for example, '#40'.
        
        Parameters:
            spectra_path (str): absolute path to the spectra/ folder.
            
            datapoint (str): the name of the data point.
        
        Modifies: 
            self: added columns 'tag', 'Theo PRE'.
        """
        if not(self.para_name):
            self.log_r(fsw.gen_wet("ERROR", "Paramagnetic Z axis name incorrect", 1))
            self.abort()
            return
        self.PRE_loaded = True
        target_folder = '{}/{}/{}/'.format(spectra_path, self.para_name, datapoint)
        pre_file = glob.glob('{}*.pre'.format(target_folder))
        
        if len(pre_file) > 1:
            raise ValueError(
                '@@@ There are more than one .pre file in the folder {}'.\
                    format(target_folder)
                )
        
        elif len(pre_file) < 1:
            raise ValueError('@@@ There is no .pre file in folder {}'.\
                format(target_folder))
        
        # loads theoretical PRE data to 'Theo PRE' new column
        # sets 1 to the diamagnetic Item.
        predf = pd.read_csv(
            pre_file[0],
            sep='\s+',
            usecols=[1],
            names=['Theo PRE'],
            comment='#'
            )
        self.log_r('**Added Theoretical PRE file** {}'.format(pre_file[0]))
        self.log_r('*Theoretical PRE for diamagnetic set to 1 by default*')
        self.loc[:,:,'Theo PRE'] = 1
        self.loc[self.para_name,:,'Theo PRE'] = predf.loc[:,'Theo PRE']
        # reads information on the tag position.
        tagf = open(pre_file[0], 'r')
        tag = tagf.readline().strip().strip('#')
        
        try:
            tag_num = int(tag)
        
        except ValueError:
            msg = \
"Theoretical PRE file incomplete. Header with tag number is missing."
            self.log_r(fsw.gen_wet('ERROR', msg, 15))
            self.abort()
        
        # check tag residue
        if not(any(self.loc[self.para_name,:,'ResNo'].isin([tag]))):
            msg = \
'The residue number where the tag is placed according to the \*.pre file ({}) \
is not part of the protein sequence ({}-{}).'.\
                format(
                    tag_num,
                    int(self.res_info.iloc[0,0,0]),
                    int(self.res_info.iloc[0,:,0].tail(n=1))
                    )
            self.log_r(fsw.gen_wet('ERROR', msg, 17))
            self.abort()
        
        self.loc[self.para_name,:,'tag'] = ''
        tagmask = self.loc[self.para_name,:,'ResNo'] == tag
        self.loc[self.para_name,tagmask,'tag'] = '*'
        tagf.close()
        self.log_r('**Tag position found** at residue {}'.format(tag_num))
        
        return
        
    def calc_Delta_PRE(
            self, sourcecol,
            targetcol,
            guass_x_size=7,
            gaussian_stddev=1):
        """
        Calculates DELTA PRE.
        
        Arbesú, M. et al. The Unique Domain Forms a Fuzzy Intramolecular 
        Complex in Src Family Kinases. Structure 25, 630–640.e4 (2017).
        
        Parameters:
            sourcecol (str): the column name of the intensity data.
            
            targetcol (str): the column name to store delta PRE data.
            
            guass_x_size (int): 1D Gaussian kernel of window size.
            
            gaussian_stddev (int): standard deviation.
        """
        # astropy is imported to avoind demanding import when not necessary
        from astropy.convolution import Gaussian1DKernel, convolve
        
        # http://docs.astropy.org/en/stable/api/astropy.convolution.Gaussian1DKernel.html
        gauss = Gaussian1DKernel(gaussian_stddev, x_size=guass_x_size)
        self.loc[:,:,targetcol] = \
            self.loc[:,:,'Theo PRE'].sub(self.loc[:,:,sourcecol])
        self.log_r('**Calculated DELTA PRE** for source {} in target {}'.\
                format(sourcecol, targetcol))
        
        for exp in self.items:
            # converts to 0 negative values
            negmask = self.loc[exp,:,targetcol] < 0
            self.loc[exp,negmask,targetcol] = 0
            # aplies convolution with a normalized 1D Gaussian kernel
            smooth_col = '{}_smooth'.format(targetcol)
            self.loc[exp,:,smooth_col] = convolve(
                np.array(self.loc[exp,:,targetcol]),
                gauss,
                boundary='extend',
                normalize_kernel=True
                )
        self.log_r(\
'**Calculated DELTA PRE Smoothed** for source {} in target {} \
with window size {} and stdev {}'.\
            format(sourcecol, smooth_col, guass_x_size, gaussian_stddev))

        return
    
    def write_table(
            self, restraint_folder,
            tablecol,
            resonance_type='Backbone'):
        """
        Exports to .csv file the columns along the series.
        
        Parameters:
            restraint_folder (str): the folder name.
            
            tablecol (str): the column name to be exported.
            
            resonance_type (str): {'Backbone', 'Sidechains'}
        """
        
        # concatenates the values of the table with the residues numbers
        try:
            data_table = self.loc[:,:,tablecol].astype(float)
            is_float = True
        
        except ValueError:
            data_table = self.loc[:,:,tablecol]
            is_float = False
            
        if resonance_type == 'Backbone':
            table = pd.concat([self.res_info.iloc[0,:,0:3], data_table], axis=1)
        
        if resonance_type == 'Sidechains':
            table = pd.concat(
                [
                    self.res_info.iloc[0,:,0],
                    self.ix[0,:,'ATOM'],
                    self.res_info.iloc[0,:,1:3],
                    data_table
                    ],
                axis=1
                )
        
        tablefolder = '{}/{}'.format(
            self.tables_and_plots_folder, 
            restraint_folder
            )
        
        if not(os.path.exists(tablefolder)):
            os.makedirs(tablefolder)
        
        file_path = '{}/{}.csv'.format(tablefolder, tablecol)
        fileout = open(file_path, 'w')
        header = \
            "# Table for '{}' resonances.\n".format(self.resonance_type)
        header += self.create_header(
            extra_info="Datapoints in series: {}".\
                format(list(self.series_datapoints)),
            file_path=file_path
            )
        header += "# {} data\n#\n".format(tablecol)
        fileout.write(header)
        
        if is_float:
            fileout.write(
                table.to_csv(
                    sep=',',
                    index=False,
                    na_rep='NaN',
                    float_format='%.4f'
                    )
                )
        
        else:
            fileout.write(
                table.to_csv(
                    sep=',',
                    index=False,
                    na_rep='NaN',
                    )
                )
        
        fileout.close()
        self.log_r('**Exported data table:** {}'.format(file_path))
        
        return
    
    def write_Chimera_attributes(
            self, calccol,
            resformat=':',
            colformat='{:.5f}'):
        """
        Exports values in column to Chimera Attribute files.
        http://www.cgl.ucsf.edu/chimera/docs/ContributedSoftware/defineattrib/defineattrib.html#attrfile
        
        One file is exported for each experiment in the Series.
        
        Parameters:
            resformat (str): formatting prefix for the 'ResNo' column. 
                Must match the residue selection command in Chimera.
                See:
                www.cgl.ucsf.edu/chimera/docs/UsersGuide/midas/frameatom_spec.html
                Defined in the Chimera_ATT_Res_format variable.
            
            colformat (str): formatting code.
        """
        
        s2w = ''
        resform = lambda x: "\t{}{}\t".format(resformat, x)
        colform = lambda x: colformat.format(x)
        formatting = {'ResNo': resform}
        
        for item in self.items:
            mask_missing = self.loc[item,:,'Peak Status'] == 'missing'
            mask_unassigned = self.loc[item,:,'Peak Status'] == 'unassigned'
            mask_measured = self.loc[item,:,'Peak Status'] == 'measured'
            file_path = '{}/{}'.format(self.chimera_att_folder, calccol)
            
            if not(os.path.exists(file_path)):
                os.makedirs(file_path)
            
            file_name = '{}/{}_{}.att'.format(file_path, item, calccol)
            fileout = open(file_name, 'w')
            header = self.create_header(file_path=file_name)
            attheader = \
"""#
#
# missing peaks {}
#
# unassigned peaks {}
#
attribute: {}
match mode: 1-to-1
recipient: residues
\t""".\
                format(
                    resformat+self.loc[item,mask_missing,'ResNo'].\
                        to_string(header=False, index=False).\
                            replace(' ', '').replace('\n', ','),
                    resformat+self.loc[item,mask_unassigned,'ResNo'].\
                        to_string(header=False, index=False).\
                            replace(' ', '').replace('\n', ','),
                    calccol.lower()
                    )
            fileout.write(header+attheader)
            formatting[calccol] = colform
            to_write = self.loc[item,mask_measured,['ResNo',calccol]].\
                to_string(
                    header=False,
                    index=False,
                    formatters=formatting,
                    col_space=0
                    ).replace(' ', '')
            fileout.write(to_write)
            fileout.close()
            self.log_r('**Exported Chimera Att** {}'.format(file_name))
        
        return
    
    def export_series_to_tsv(self):
        """
        Exports the experimental series with measured and
        calculated data to .csv files.
        """
        
        for item in self.items:
            file_path = '{}/{}.csv'.format(self.export_series_folder, item)
            fileout = open(file_path, 'w')
            ###
            header = self.create_header(
                extra_info="Peaklist from datapoint: {}".format(item),
                file_path=file_path
                )
            fileout.write(header)
            fileout.write(
                self.loc[item].to_csv(
                    sep=',',
                    index=False,
                    na_rep='NaN',
                    float_format='%.4f'
                    )
                )
            self.log_r('**Exported parsed peaklist** {}'.format(file_path))
            fileout.close()
        
        return
    
    def set_item_colors(self, items, series, d):
        """
        Translates the 'Peak Status' col to a dict of colours.
        
        Parameters:
            items (matplotlib obj): either plot bars, ticks, etc...
        
            series (pd.Series): containing the 'Peak Status' information.
        
            d (dict): keys are series values, and values are colours.
        
        Returns:
            None, series are changed in place.
        """
        
        for i, it in zip(series.index, items):
            if str(series[i]) in d.keys():
                it.set_color(d[str(series[i])])
            
            else:
                continue
        return
    
    def text_marker(
            self, ax,
            axbar, series,
            d, yy_scale,
            fs=3,
            orientation='horizontal'):
        """
        Places a text mark over the bars of a Bar Plot.
        
        Parameters:
            ax (matplotlib subplot axis): where maker is written.
            
            axbar (matplotlib object): bars of plot.
            
            series (pd.Series): series with information source.
            
            d (dict): translates information into marker.
            
            yy_scale (float): vertical scale calibrates marker position
            
            fs (int): font size
            
            orientation (str): {'horizontal', 'vertical'}
                wheter plotting in a vertical or horizontal barplot.
        """
        
        def vpos_sign(x, y):
            """Scales to the vertical position - positive and negative."""
            if y>=0:
                return x
            else:
                return (x*-1)-(yy_scale/20)
        
        def hpos_sign(x, y):
            """Scales to the horizontal position - positive and negative."""
            if y >= 0:
                return x+(yy_scale/20)
            else:
                return (x*-1)-(yy_scale/20)
        
        for i, bar in zip(series.index, axbar):
            if str(series[i]) in d.keys():
                x0, y0 = bar.xy
                if orientation == 'vertical':
                    hpos = hpos_sign(bar.get_width(), x0)
                    vpos = bar.get_y() + bar.get_height()/2
                    vaa='center'
                
                elif orientation == 'horizontal':
                    vpos = vpos_sign(bar.get_height(), y0)
                    hpos = bar.get_x() + bar.get_width() / 2.5
                    vaa='bottom'
                
                ax.text(
                    hpos,
                    vpos,
                    d[str(series[i])],
                    ha='center',
                    va=vaa,
                    fontsize=fs
                    )
            else:
                continue
        
        return
    
    def plot_threshold(
            self, ax,
            series, color,
            lw, alpha,
            orientation = 'horizontal',
            zorder=5):
        """
        Plots threshold line that identifies relevant perturnations.
        
        Parameters:
            ax (matplotlib subplot axis): subplot where line is drawn.
            
            series (pd.Series): values to evaluate.
            
            color (str): line color.
            
            lw (int): line width.
            
            alpha (float): transparency.
            
            orientation (str): {'horizontal', 'vertical'}
                wheter plotting in a vertical or horizontal barplot.
            
            zorder (int): the matplotlib zorder kwarg.
        """
        
        sorted_cs = series.abs().sort_values().dropna()
        firstdecile = sorted_cs[0:ceil(0.1*len(sorted_cs))]
        threshold = firstdecile.mean() + 5*firstdecile.std()
        
        if orientation == 'horizontal':
            ax.axhline(
                y=threshold,
                color=color, 
                linewidth=lw,
                alpha=alpha,
                zorder=zorder
                )
            # in case there are negative numbers, plots the threshold,
            # if there are not negative numbers, this line is never displayed
            ax.axhline(
                y=-threshold,
                color=color, 
                linewidth=lw,
                alpha=alpha,
                zorder=zorder
                )
        
        elif orientation == 'vertical':
            ax.axvline(
                x=threshold,
                color=color, 
                linewidth=lw,
                alpha=alpha,
                zorder=zorder
                )
            # in case there are negative numbers, plots the threshold,
            # if there are not negative numbers, this line is never displayed
            ax.axvline(
                x=-threshold,
                color=color, 
                linewidth=lw,
                alpha=alpha,
                zorder=zorder
                )
        
        return
    
    def plot_theo_pre(
            self, axs,
            exp, y,
            bartype='h',
            pre_color='lightblue',
            pre_lw=1,
            tag_color='red',
            tag_ls='-',
            tag_lw=0.1):
        """
        Plots theoretical PRE.
        
        Parameters:
            axs (matplotlib subplot axis): where values are plot.
            
            exp (str): the name of the Z axis data point.
            
            y (float): plot's y axis limit
            
            bartype (str): {'h', 'v', 'hm'}, whether plot of type 
                horizontal, vertical or Heat Map.
            
            pre_color (str): the colour of plot line
            
            pre_lw (int): line width
            
            tag_color (str): the colour of the tag cartoon
            
            tag_ls (str): matplotlib linestyle kwarg for the tag tick
            
            tag_lw (float): tag tick line width.
        """
        
        if (self.series_axis == 'along_z' and exp == self.para_name) \
                or (self.series_axis == 'Cz' \
                    and (self.next_dim in self.paramagnetic_names or self.prev_dim in self.paramagnetic_names)):
            # plot theoretical PRE
            
            x_axis_values = np.arange(
                float(self.loc[exp,:,'ResNo'].head(n=1))-1,
                float(self.loc[exp,:,'ResNo'].tail(n=1)),
                1,
                )
            
            if bartype == 'v':
                axs.plot(
                    self.loc[exp,:,'Theo PRE'],
                    x_axis_values,
                    zorder=9,
                    color=pre_color,
                    lw=pre_lw
                    )
            
            elif bartype == 'h':
                axs.plot(
                    x_axis_values,
                    self.loc[exp,:,'Theo PRE'],
                    zorder=9,
                    color=pre_color,
                    lw=pre_lw
                    )
            
            # plot tag position
            xtagm = self.loc[exp,:,'tag']=='*'
            xtag = float(self.loc[exp,xtagm,'ResNo'])-1
            
            if bartype in ['h', 'DPRE_plot']:
                axs.vlines(
                    xtag,
                    0,
                    y,
                    colors=tag_color,
                    linestyle=tag_ls,
                    linewidth=tag_lw,
                    zorder=10
                    )
                axs.plot(
                    xtag,
                    y,
                    'o',
                    zorder=10,
                    color='red',
                    markersize=2
                    )
            
            elif bartype == 'v':
                axs.hlines(
                    xtag,
                    0,
                    y,
                    colors=tag_color,
                    linestyle=tag_ls,
                    linewidth=tag_lw,
                    zorder=10
                    )
                axs.plot(
                    y,
                    xtag,
                    'o',
                    zorder=10,
                    color='red',
                    markersize=2
                    )
            
            elif bartype == 'hm':
                axs.vlines(
                    xtag,
                    0,
                    y,
                    colors=tag_color,
                    linestyle=tag_ls,
                    linewidth=tag_lw,
                    zorder=10
                    )
        
        else:
            return
    
    def plot_bar_horizontal(
        self, plot_style,
        calccol, axs,
        i, experiment,
        y_lims=(0,1),
        ylabel='ppm or ratio',
        measured_color='black',
        status_color_flag=True,
        missing_color='red',
        unassigned_color='grey',
        bar_width=0.7,
        bar_alpha=1,
        bar_linewidth=0,
        subtitle_fn='Arial',
        subtitle_fs=8,
        subtitle_pad=1.05,
        subtitle_weight='normal',
        threshold_flag=True,
        threshold_color='red',
        threshold_linewidth=1,
        threshold_alpha=1,
        threshold_zorder=5,
        x_label_fn='Arial',
        x_label_fs=8, 
        x_label_pad=2,
        x_label_weight='bold',
        x_label_rot=0,
        y_label_fn='Arial',
        y_label_fs=8,
        y_label_pad=2,
        y_label_weight='bold',
        y_label_rot=90,
        x_ticks_pad=2,
        x_ticks_len=1,
        y_ticks_fn='Arial',
        y_ticks_fs=9,
        y_ticks_pad=-3,
        y_ticks_weight='normal',
        y_ticks_nbins=8,
        y_ticks_len=2,
        y_ticks_rot=0,
        y_grid_flag=True,
        y_grid_color='lightgrey',
        y_grid_linestyle='-',
        y_grid_linewidth=0.2,
        y_grid_alpha=1,
        mark_fontsize=3,
        mark_prolines_flag=True,
        mark_prolines_symbol='P',
        mark_user_details_flag=False,
        color_user_details_flag=False,
        user_marks_dict={},
        user_bar_colors_dict={},
        theo_pre_color='red',
        theo_pre_lw=0.2,
        tag_cartoon_color='magenta',
        tag_cartoon_lw=0.2,
        tag_cartoon_ls=':',
        x_ticks_color_flag=True,
        x_ticks_fn='monospace',
        x_ticks_fs=6,
        x_ticks_weight='normal',
        x_ticks_rot=90,
        unassigned_shade=False,
        unassigned_shade_alpha=0.5,
        vspace='',
        rows_page='',
        cols_page=''):
        """
        Plots horizontal bar plots.
        
        Parameters:
            plot_style (str): {'bar_extender', 'bar_compacted'},
                template to use.
            
            calccol (str): the name of the column to plot.
            
            axs: matplotlib axis object.
            
            i (int): the index of the subplot axis.
            
            experiment (srt): the name of the data point.
        """
        
        if plot_style == 'bar_extended' and self.resonance_type == 'Backbone':
            # fillna(0) is added because nan conflicts with text_maker()
            # in bar.get_height() which return nan
            bars = axs[i].bar(
                self.major_axis,
                self.loc[experiment,:,calccol].fillna(0),
                width=bar_width,
                align='center',
                alpha=bar_alpha,
                linewidth=bar_linewidth,
                zorder=4
                )
            
            # ticks positions:
            # this is used to fit both applyFASTA=True or False
            # reduces xticks to 100 as maximum to avoid ticklabel overlap
            if self.shape[1] > 100:
                xtick_spacing = self.shape[1]//100
            
            else:
                xtick_spacing = 1
            
            ticklabels = \
                self.loc[experiment,0::xtick_spacing,['ResNo','1-letter']].\
                    apply(lambda x: ''.join(x), axis=1)
            # Configure XX ticks and Label
            axs[i].set_xticks(self.major_axis)
            ## https://github.com/matplotlib/matplotlib/issues/6266
            axs[i].set_xticklabels(
                ticklabels,
                fontname=x_ticks_fn,
                fontsize=x_ticks_fs,
                fontweight=x_ticks_weight,
                rotation=x_ticks_rot
                )
            
            # defines xticks colors
            if x_ticks_color_flag:
                self.set_item_colors(
                    axs[i].get_xticklabels(),
                    self.loc[experiment,0::xtick_spacing,'Peak Status'],
                    {
                        'measured':measured_color,
                        'missing':missing_color,
                        'unassigned':unassigned_color
                        }
                    )
            
        elif plot_style == 'bar_extended' \
                and self.resonance_type == 'Sidechains':
            bars = axs[i].bar(
                self.major_axis,
                self.loc[experiment,:,calccol].fillna(0),
                width=bar_width,
                align='center',
                alpha=bar_alpha,
                linewidth=bar_linewidth,
                zorder=4
                )
        
            # Configure XX ticks and Label
            axs[i].set_xticks(self.major_axis)
            ## https://github.com/matplotlib/matplotlib/issues/6266
            axs[i].set_xticklabels(
                self.loc[experiment,:,['ResNo', '1-letter', 'ATOM']].\
                    apply(lambda x: ''.join(x), axis=1),
                fontname=x_ticks_fn,
                fontsize=x_ticks_fs,
                fontweight=x_ticks_weight,
                rotation=x_ticks_rot
                )
            
            # defines xticks colors
            if x_ticks_color_flag:
                self.set_item_colors(
                    axs[i].get_xticklabels(),
                    self.loc[experiment, :, 'Peak Status'],
                    {
                        'measured':measured_color,
                        'missing':missing_color,
                        'unassigned':unassigned_color
                        }
                    )
        
        elif plot_style == 'bar_compacted':
            bars = axs[i].bar(
                self.loc[experiment,:,'ResNo'].astype(float),
                self.loc[experiment,:,calccol].fillna(0),
                width=bar_width,
                align='center',
                alpha=bar_alpha,
                linewidth=bar_linewidth,
                zorder=4
                )
            
            initialresidue = int(self.ix[0, 0, 'ResNo'])
            finalresidue = int(self.loc[experiment,:,'ResNo'].tail(1))
            
            if self.shape[1] > 100:
                xtick_spacing = self.shape[1]//100*10
            
            else:
                xtick_spacing = 10
            
            first_tick = ceil(initialresidue/10)*xtick_spacing
            xtickarange = np.arange(first_tick, finalresidue+1, xtick_spacing)
            axs[i].set_xticks(xtickarange)
            # https://github.com/matplotlib/matplotlib/issues/6266
            axs[i].set_xticklabels(
                xtickarange,
                fontname=x_ticks_fn,
                fontsize=x_ticks_fs,
                fontweight=x_ticks_weight,
                rotation=x_ticks_rot
                )
            
            if unassigned_shade:
                unassignedmask = \
                    self.loc[experiment, :, 'Peak Status'] == 'unassigned'
                
                for residue in self.loc[experiment, unassignedmask, 'ResNo']:
                    residue = int(residue) - 0.5
                    axs[i].axvspan(
                        residue,
                        residue+1,
                        color=unassigned_color,
                        alpha=unassigned_shade_alpha,
                        lw=0
                        )
        
        # Set subplot titles
        axs[i].set_title(
            experiment,
            y=subtitle_pad,
            fontsize=subtitle_fs,
            fontname=subtitle_fn,
            weight=subtitle_weight
            )
        # defines bars colors
        self.set_item_colors(
            bars,
            self.loc[experiment,:,'Peak Status'],
            {
                'measured':measured_color,
                'missing':missing_color,
                'unassigned':unassigned_color
                }
            )
        # configures spines
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        # cConfigures YY ticks
        axs[i].set_ylim(y_lims[0], y_lims[1])
        axs[i].locator_params(axis='y', tight=True, nbins=y_ticks_nbins)
        axs[i].set_yticklabels(
            ['{:.2f}'.format(yy) for yy in axs[i].get_yticks()],
            fontname=y_ticks_fn,
            fontsize=y_ticks_fs,
            fontweight=y_ticks_weight,
            rotation=y_ticks_rot
            )
        # configures tick params
        axs[i].margins(x=0.01)
        axs[i].tick_params(
            axis='x',
            pad=x_ticks_pad,
            length=x_ticks_len,
            direction='out'
            )
        axs[i].tick_params(
            axis='y',
            pad=y_ticks_pad,
            length=y_ticks_len,
            direction='out'
            )
        # Set axes labels
        axs[i].set_xlabel(
            'Residue',
            fontname=x_label_fn,
            fontsize=x_label_fs,
            labelpad=x_label_pad,
            weight=x_label_weight,
            rotation=x_label_rot
            )
        axs[i].set_ylabel(
            ylabel,
            fontsize=y_label_fs,
            labelpad=y_label_pad,
            fontname=y_label_fn,
            weight=y_label_weight,
            rotation=y_label_rot
            )
        
        # Adds grid
        if y_grid_flag:
            axs[i].yaxis.grid(
                color=y_grid_color,
                linestyle=y_grid_linestyle,
                linewidth=y_grid_linewidth,
                alpha=y_grid_alpha,
                zorder=0
                )
        
        # Adds red line to identify significant changes.
        if threshold_flag and (calccol in self.restraint_list[:3]):
            self.plot_threshold(
                axs[i],
                self.loc[experiment,:,calccol],
                threshold_color,
                threshold_linewidth,
                threshold_alpha,
                zorder=threshold_zorder
                )
        
        if mark_prolines_flag:
            self.text_marker(
                axs[i],
                bars,
                self.loc[experiment,:,'1-letter'],
                {'P':mark_prolines_symbol},
                y_lims[1],
                fs=mark_fontsize
                )
        
        if mark_user_details_flag:
            self.text_marker(
                axs[i],
                bars,
                self.loc[experiment,:,'Details'],
                user_marks_dict,
                y_lims[1],
                fs=mark_fontsize
                )
        
        if color_user_details_flag:
            self.set_item_colors(
                bars,
                self.loc[experiment,:,'Details'],
                user_bar_colors_dict
                )
        
        if self.PRE_loaded and (calccol in self.restraint_list[3:]):
            self.plot_theo_pre(
                axs[i],
                experiment,
                y_lims[1]*0.05,
                bartype='h',
                pre_color=theo_pre_color,
                pre_lw=theo_pre_lw,
                tag_color=tag_cartoon_color,
                tag_ls=tag_cartoon_ls,
                tag_lw=tag_cartoon_lw
                )
    
    def plot_bar_vertical(
            self, calccol,
            axs, i,
            experiment,
            y_lims=(0,1),
            ylabel='ppm or ratio',
            measured_color='black',
            status_color_flag=True,
            missing_color='red',
            unassigned_color='grey',
            bar_width=0.7,
            bar_alpha=1,
            bar_linewidth=0,
            subtitle_fn='Arial',
            subtitle_fs=8,
            subtitle_pad=1.05,
            subtitle_weight='normal',
            threshold_flag=True,
            threshold_color='red',
            threshold_linewidth=1,
            threshold_alpha=1,
            threshold_zorder=5,
            x_label_fn='Arial',
            x_label_fs=8, 
            x_label_pad=2,
            x_label_weight='bold',
            x_label_rot=-90,
            y_label_fn='Arial',
            y_label_fs=8,
            y_label_pad=2,
            y_label_weight='bold',
            y_label_rot=90,
            x_ticks_pad=2,
            x_ticks_len=1,
            y_ticks_fn='Arial',
            y_ticks_fs=9,
            y_ticks_pad=-3,
            y_ticks_weight='normal',
            y_ticks_nbins=8,
            y_ticks_len=2,
            y_ticks_rot=0,
            y_grid_flag=True,
            y_grid_color='lightgrey',
            y_grid_linestyle='-',
            y_grid_linewidth=0.2,
            y_grid_alpha=1,
            mark_fontsize=3,
            mark_prolines_flag=True,
            mark_prolines_symbol='P',
            mark_user_details_flag=False,
            color_user_details_flag=False,
            user_marks_dict={},
            user_bar_colors_dict={},
            theo_pre_color='red',
            theo_pre_lw=0.2,
            tag_cartoon_color='magenta',
            tag_cartoon_lw=0.2,
            tag_cartoon_ls=':',
            x_ticks_color_flag=True,
            x_ticks_fn='monospace',
            x_ticks_fs=6,
            x_ticks_weight='normal',
            x_ticks_rot=0,
            vspace='',
            rows_page='',
            cols_page=''):
        """
        Plots vertical bar plots.
        
        Parameters:
            calccol (str): the name of the column to plot.
            
            axs: matplotlib axis object.
            
            i (int): the index of the subplot axis.
            
            experiment (srt): the name of the data point.
        """
        
        # fillna(0) is added because nan conflicts with text_maker()
        # .iloc[::-1]
        # in bat.get_height() which return nan
        bars = axs[i].barh(
            self.major_axis,
            self.loc[experiment,:,calccol].fillna(0),
            height=bar_width,
            align='center',
            alpha=bar_alpha,
            linewidth=bar_linewidth,
            zorder=4
            )
        axs[i].invert_yaxis()
        # Set subplot titles
        axs[i].set_title(
            experiment,
            y=subtitle_pad,
            fontsize=subtitle_fs,
            fontname=subtitle_fn,
            weight=subtitle_weight
            )
        # configures spines
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        axs[i].spines['left'].set_zorder(10)
        axs[i].spines['right'].set_zorder(10)
        ## Configure XX ticks and Label
        axs[i].margins(y=0.01)
        
        if self.shape[1] > 100:
            xtick_spacing = self.shape[1]//100
        
        else:
            xtick_spacing = 1
        
        axs[i].set_yticks(self.major_axis)
        # https://github.com/matplotlib/matplotlib/issues/6266
        axs[i].set_yticklabels(
            self.loc[experiment,0::xtick_spacing,['ResNo','1-letter']].\
                apply(lambda x: ''.join(x), axis=1),
            fontname=x_ticks_fn,
            fontsize=x_ticks_fs-2,
            fontweight=x_ticks_weight,
            rotation=0
            )
        ## defines colors
        self.set_item_colors(
            bars,
            self.loc[experiment,:,'Peak Status'],
            {
                'measured':measured_color,
                'missing':missing_color,
                'unassigned':unassigned_color
                }
            )
        
        if x_ticks_color_flag:
            self.set_item_colors(
                axs[i].get_yticklabels(),
                self.loc[experiment,0::xtick_spacing,'Peak Status'],
                {
                    'measured':measured_color,
                    'missing':missing_color,
                    'unassigned':unassigned_color
                    }
                )
        
        ## Configures YY ticks
        axs[i].set_xlim(y_lims[0], y_lims[1])
        axs[i].locator_params(axis='x', tight=True, nbins=y_ticks_nbins)
        axs[i].set_xticklabels(
            ['{:.2f}'.format(xx) for xx in axs[i].get_xticks()],
            fontname=y_ticks_fn,
            fontsize=y_ticks_fs,
            fontweight=y_ticks_weight,
            rotation=-45
            )
        # configures tick params
        axs[i].tick_params(
            axis='y',
            pad=x_ticks_pad,
            length=x_ticks_len,
            direction='out'
            )
        axs[i].tick_params(
            axis='x',
            pad=y_ticks_pad,
            length=y_ticks_len,
            direction='out'
            )
        # Set axes labels
        axs[i].set_ylabel(
            'Residue',
            fontname=x_label_fn,
            fontsize=x_label_fs,
            labelpad=x_label_pad+6,
            weight=x_label_weight,
            rotation=x_label_rot
            )
        axs[i].set_xlabel(
            ylabel,
            fontsize=y_label_fs,
            labelpad=y_label_pad,
            fontname=y_label_fn,
            weight=y_label_weight,
            rotation=0
            )
        
        # Adds grid
        if y_grid_flag:
            axs[i].xaxis.grid(
                color=y_grid_color,
                linestyle=y_grid_linestyle,
                linewidth=y_grid_linewidth,
                alpha=y_grid_alpha,
                zorder=0
                )
        
        # Adds red line to identify significant changes.
        if threshold_flag and (calccol in self.restraint_list[:3]):
            self.plot_threshold(
                axs[i],
                self.loc[experiment,:,calccol],
                threshold_color,
                threshold_linewidth,
                threshold_alpha,
                orientation='vertical',
                zorder=threshold_zorder
                )
        
        if mark_prolines_flag:
            self.text_marker(
                axs[i],
                bars,
                self.loc[experiment,:,'1-letter'],
                {'P':mark_prolines_symbol},
                y_lims[1]*0.6,
                fs=mark_fontsize,
                orientation='vertical'
                )
        
        if mark_user_details_flag:
            self.text_marker(
                axs[i],
                bars,
                self.loc[experiment,:,'Details'],
                user_marks_dict,
                y_lims[1]*0.6,
                fs=mark_fontsize,
                orientation='vertical'
                )
        
        if color_user_details_flag:
            self.set_item_colors(
                bars,
                self.loc[experiment,:,'Details'],
                user_bar_colors_dict
                )
        
        if self.PRE_loaded and (calccol in self.restraint_list[3:]):
            self.plot_theo_pre(
                axs[i],
                experiment,
                y_lims[1]*0.1,
                bartype='v',
                pre_color=theo_pre_color,
                pre_lw=theo_pre_lw,
                tag_color=tag_cartoon_color,
                tag_ls=tag_cartoon_ls,
                tag_lw=tag_cartoon_lw
                )
        
        return
    
    
    def plot_res_evo(
            self, calccol,
            axs, i,
            row_number,
            y_lims=(0,1),
            y_label='ppm or ratio',
            subtitle_fn='Arial',
            subtitle_fs=8,
            subtitle_pad=0.98,
            subtitle_weight='normal',
            x_label_fn='Arial',
            x_label_fs=3,
            x_label_pad=2,
            x_label_weight='normal',
            y_label_fn='Arial',
            y_label_fs=6 ,
            y_label_pad=2,
            y_label_weight='normal',
            x_ticks_fn='Arial',
            x_ticks_fs=5,
            x_ticks_pad=1,
            x_ticks_weight=1,
            x_ticks_rot=0,
            x_ticks_len=2,
            x_ticks_nbins=5,
            y_ticks_fn='Arial',
            y_ticks_fs=5,
            y_ticks_pad=1,
            y_ticks_weight=1,
            y_ticks_len=2,
            y_ticks_rot=0,
            y_ticks_nbins=8,
            x_label='[Ligand]',
            set_x_values=True,
            line_style='-',
            line_width=1,
            line_color='r',
            marker_style='o',
            marker_color='darkred',
            marker_size=3,
            fill_between=True,
            fill_color='pink',
            fill_alpha=0.5,
            fit_line_color = 'black',
            fit_line_width = 1,
            fit_line_style = '-',
            titration_x_values=None,
            vspace='',
            rows_page='',
            cols_page='',
            perform_resevo_fitting=''):
        """
        Plots residue resolved parameter evolution along the series.
        
        Parameters:
            calccol (str): the name of the column to plot.
            
            axs: matplotlib axis object.
            
            i (int): the index of the subplot axis.
            
            row_number (int): the index of the current residue.
        """
        
        # Draws subplot title
        res = self.ix[0,i,'ResNo']
        subtitle = self.ix[0,i,'ResNo'] + self.ix[0,i,'1-letter']
        axs[i].set_title(
            subtitle,
            y=subtitle_pad,
            fontsize=subtitle_fs,
            fontname=subtitle_fn,
            fontweight=subtitle_weight
            )
        # PREPARING DATA
        y = np.array(self.loc[:,row_number,calccol].fillna(value=0))
        
        # if the user wants to represent the condition in the x axis
        # for the first dimension
        if set_x_values \
                and (self.series_axis == 'along_x' \
                    or self.dim_comparison == 'along_x'):
            if len(titration_x_values) != len(self.items):
                msg = \
"The number of coordinate values defined for fitting/data respresentation, \
<fitting_x_values> variable [{}], do not match the number of \
data points <along_x>, i.e. input peaklists. Please correct <fitting_x_values> \
variable or confirm you have not forgot any peaklist [{}].".\
                    format(titration_x_values, self.items)
                self.log_r(fsw.gen_wet('ERROR', msg, 5))
                self.abort()
            
            x = np.array(titration_x_values)
            xmin = titration_x_values[0]
            xmax = titration_x_values[-1]
            
        # for 2D and 3D analysis this option is not available
        elif (self.series_axis in ['along_y', 'along_z']) \
                or (self.dim_comparison in ['along_y', 'along_z']):
            x = np.arange(0, len(y))
            xmin = 0
            xmax = len(y)-1
            axs[i].set_xticks(x)
            xlabels = self.items
            x_ticks_rot=45
        
        # just give a range for the x axis
        # in case representing the along_x without titration_x_values
        else:
            x = np.arange(0, len(y))
            axs[i].set_xticks(x)
            xmin = 0
            xmax = len(y)-1
            xlabels = x
        
        # Configure Axis Ticks
        axs[i].set_xlim(xmin, xmax)
        axs[i].set_ylim(y_lims[0], y_lims[1])
        
        if set_x_values \
                and (self.series_axis == 'along_x' \
                    or self.dim_comparison == 'along_x'):
            axs[i].locator_params(axis='x', tight=True, nbins=x_ticks_nbins)
            
            def eval_tick(x):
                if x >= 1:
                    if int(x) % x == 0:
                        return int(x)
                    elif int(x) % x != 0:
                        return str(x)
                else:
                    return str(x)
            
            xlabels = [eval_tick(n) for n in axs[i].get_xticks()]
        
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        axs[i].spines['left'].set_zorder(10)
        axs[i].spines['right'].set_zorder(10)
        axs[i].set_xticklabels(
            xlabels,
            fontname=x_ticks_fn,
            fontsize=x_ticks_fs,
            fontweight=x_ticks_weight,
            rotation=x_ticks_rot
            )
        axs[i].locator_params(axis='y', tight=True, nbins=y_ticks_nbins)
        axs[i].set_yticklabels(
            ['{:.2f}'.format(yy) for yy in axs[i].get_yticks()],
            fontname=y_ticks_fn,
            fontsize=y_ticks_fs,
            fontweight=y_ticks_weight,
            rotation=y_ticks_rot
            )
        axs[i].xaxis.tick_bottom()
        axs[i].yaxis.tick_left()
        axs[i].tick_params(
            axis='x',
            pad=x_ticks_pad,
            length=x_ticks_len,
            direction='out'
            )
        axs[i].tick_params(
            axis='y',
            pad=y_ticks_pad,
            length=y_ticks_len,
            direction='out'
            )
        ## Configure axes labels
        axs[i].set_xlabel(
            x_label,
            fontsize=x_label_fs,
            labelpad=x_label_pad,
            fontname=x_label_fn,
            weight=x_label_weight
            )
        ## Configure YY ticks/label
        axs[i].set_ylabel(
            y_label,
            fontsize=y_label_fs,
            labelpad=y_label_pad,
            fontname=y_label_fn,
            weight=y_label_weight
            )
        
        # writes unassigned in the center of the plot for unassigned peaks
        # and plots nothing
        if self.ix[0,row_number,'Peak Status'] == 'unassigned':
            axs[i].text(
                (x[0] + x[-1]) / 2,
                (y_lims[0]+y_lims[1])/2,
                'unassigned',
                fontsize=8,
                fontname='Arial',
                va='center', ha='center')
            
            return
        
        # do not represent the missing peaks.
        mes_mask = np.array(self.loc[:,row_number,'Peak Status'] != 'missing')
        y = y[mes_mask]
        x = x[mes_mask]
        # Plots data
        axs[i].plot(
            x,
            y,
            ls=line_style,
            color=line_color,
            marker=marker_style,
            mfc=marker_color,
            markersize=marker_size,
            lw=line_width,
            zorder=5
            )
        
        if fill_between:
            axs[i].fill_between(
                x,
                0,
                y,
                facecolor=fill_color,
                alpha=fill_alpha
                )
        
        fit_res_col = "{}_{}".format(calccol, res)
        
        if self.fit_performed \
                and self.series_axis == 'along_x'\
                and self.fit_okay[fit_res_col]:
            #print(res)
            #print(self.xfit)
            #print(self.fit_plot_ydata[fit_res_col])
            # plot fit
            axs[i].plot(
                self.xfit,
                self.fit_plot_ydata[fit_res_col],
                fit_line_style,
                lw=fit_line_width,
                color=fit_line_color, zorder=6
                )
            # write text
            axs[i].text(
                xmax*0.05,
                y_lims[1]*0.97,
                self.fit_plot_text[fit_res_col],
                ha='left',
                va='top',
                fontsize=4
                )
        
        elif self.fit_performed and self.series_axis == 'along_x' \
                and not(self.fit_okay[fit_res_col]):
            axs[i].text(
                xmax*0.05,
                y_lims[1]*0.97,
                self.fit_plot_text[fit_res_col],
                ha='left',
                va='top',
                fontsize=4
                )
        
        return
    
    
    def plot_cs_scatter(
            self, axs,
            i, row_number,
            subtitle_fn='Arial',
            subtitle_fs=8,
            subtitle_pad=0.98,
            subtitle_weight='normal',
            x_label='1H (ppm)',
            x_label_fn='Arial',
            x_label_fs=3,
            x_label_pad=2,
            x_label_weight='normal',
            y_label='15N (ppm)',
            y_label_fn='Arial',
            y_label_fs=6 ,
            y_label_pad=2,
            y_label_weight='normal',
            x_ticks_fn='Arial',
            x_ticks_fs=5,
            x_ticks_pad=1,
            x_ticks_weight=1,
            x_ticks_rot=0,
            x_ticks_len=2,
            y_ticks_fn='Arial',
            y_ticks_fs=5,
            y_ticks_pad=1,
            y_ticks_weight=1,
            y_ticks_rot=0,
            y_ticks_len=2,
            mksize=20,
            scale=0.01,
            mk_type='color',
            mk_start_color='#cdcdcd',
            mk_end_color='#000000',
            markers=['^','>','v','<','s','p','h','8','*','D'],
            mk_color=['none'],
            mk_edgecolors='black',
            mk_missing_color='red',
            hide_missing=False,
            titration_x_values='',
            rows_page='',
            cols_page='',
            perform_resevo_fitting=''):
        """
        Plots residue resolved CSPs along the series and normalised to
        the reference experiment.
        
        Parameters:
            calccol (str): the name of the column to plot.
            
            axs: matplotlib axis object.
            
            i (int): the index of the subplot axis.
            
            row_number (int): the index of the current residue.
        """
        
        def set_tick_labels():
            # adjust the ticks to a maximum of 4.
            # http://stackoverflow.com/questions/6682784/how-to-reduce-number-of-ticks-with-matplotlib
            axs[i].locator_params(axis='both', tight=True, nbins=4)
            axs[i].set_xticklabels(
                axs[i].get_xticks(),
                fontname=x_ticks_fn,
                fontsize=x_ticks_fs,
                fontweight=x_ticks_weight,
                rotation=x_ticks_rot
                )
            axs[i].set_yticklabels(
                axs[i].get_yticks(),
                fontname=y_ticks_fn,
                fontsize=y_ticks_fs,
                fontweight=y_ticks_weight,
                rotation=y_ticks_rot
                )
        
        # Configure subtitle
        subtitle = self.ix[0,i,'ResNo'] + self.ix[0,i,'1-letter']
        axs[i].set_title(
            subtitle,
            y=subtitle_pad,
            fontsize=subtitle_fs,
            fontname=subtitle_fn,
            fontweight=subtitle_weight
            )
        # Configure Axis Ticks
        axs[i].xaxis.tick_bottom()
        axs[i].tick_params(
            axis='x',
            pad=x_ticks_pad,
            length=x_ticks_len,
            direction='out'
            )
        axs[i].yaxis.tick_left()
        axs[i].tick_params(
            axis='y',
            pad=y_ticks_pad,
            length=y_ticks_len,
            direction='out'
            )
        ## Configure axes labels
        axs[i].set_xlabel(
            x_label,
            fontsize=x_label_fs,
            labelpad=x_label_pad,
            fontname=x_label_fn,
            weight=x_label_weight
            )
        ## Configure YY ticks/label
        axs[i].set_ylabel(
            y_label,
              fontsize=y_label_fs,
            labelpad=y_label_pad,
            fontname=y_label_fn,
            weight=y_label_weight
            )
        
        # check assignment
        # if residue is unassigned, identifies in the subplot
        if self.ix[0,row_number,'Peak Status'] == 'unassigned':
            axs[i].text(
                0,
                0,
                'unassigned',
                fontsize=7,
                fontname='Arial',
                va='center',
                ha='center'
                )
            axs[i].set_xlim(-1,1)
            axs[i].set_ylim(-1,1)
            set_tick_labels()
            axs[i].invert_xaxis()
            axs[i].invert_yaxis()
            return
        
        elif not(self.ix[:,i,'H1_delta'].any()) \
                and not(self.ix[:,i,'N15_delta'].any()):
            axs[i].text(
                0,
                0,
                'all data lost',
                fontsize=7,
                fontname='Arial',
                va='center',
                ha='center'
                )
            axs[i].set_xlim(-1,1)
            axs[i].set_ylim(-1,1)
            set_tick_labels()
            axs[i].invert_xaxis()
            axs[i].invert_yaxis()
            return
        
        # Plots data
        if mk_type == 'shape':
            # represents the points in different shapes
            mcycle = it.cycle(markers)
            ccycle = it.cycle(mk_color)
            cedge = it.cycle(mk_edgecolors)
            
            for k, j in enumerate(self.items):
                if self.ix[j,i,'Peak Status'] in ['missing', 'unassigned'] \
                        and hide_missing:
                    next(mcycle)
                    next(ccycle)
                    next(cedge)
                
                elif self.ix[j,i,'Peak Status'] == 'missing':
                    axs[i].scatter(
                        self.ix[j,i,'H1_delta'],
                        self.ix[j,i,'N15_delta'],
                        marker=next(mcycle),
                        s=mksize,
                        c=next(ccycle),
                        edgecolors=mk_missing_color
                        )
                    next(cedge)
                
                else:
                    axs[i].scatter(
                        self.ix[j,i,'H1_delta'],
                        self.ix[j,i,'N15_delta'],
                        marker=next(mcycle),
                        s=mksize,
                        c=next(ccycle),
                        edgecolors=next(cedge)
                        )
        
        elif mk_type == 'color':
            # represents the points as circles with a gradient of color
            mk_color = self.linear_gradient(
                mk_start_color,
                finish_hex=mk_end_color,
                n=self.shape[0]
                )
            # this is used instead of passing a list to .scatter because
            # of colouring in red the missing peaks.
            mccycle = it.cycle(mk_color['hex'])
            
            for j in self.items:
                if self.ix[j,i,'Peak Status'] == 'missing':
                    axs[i].scatter(
                        self.ix[j,i,'H1_delta'],
                        self.ix[j,i,'N15_delta'],
                        marker='o',
                        s=mksize,
                        c=mk_missing_color,
                        edgecolors='none'
                        )
                
                else:
                    axs[i].scatter(
                        self.ix[j,i,'H1_delta'],
                        self.ix[j,i,'N15_delta'],
                        marker='o',
                        s=mksize,
                        c=next(mccycle),
                        edgecolors='none'
                        )
        
        measured = self.ix[:,i,'Peak Status'] == 'measured'
        xlimmin = \
            -scale*2 \
            if self.ix[measured,i,'H1_delta'].fillna(value=0).min() > -scale \
            else self.ix[measured,i,'H1_delta'].fillna(value=0).min()*1.5
        xlimmax = \
            scale*2 \
            if self.ix[measured,i,'H1_delta'].fillna(value=0).max() < scale \
            else self.ix[measured,i,'H1_delta'].fillna(value=0).max()*1.5
        ylimmin = \
            -scale*2 \
            if self.ix[measured,i,'N15_delta'].fillna(value=0).min() > -scale \
            else self.ix[measured,i,'N15_delta'].fillna(value=0).min()*1.5
        ylimmax = \
            scale*2 \
            if self.ix[measured,i,'N15_delta'].fillna(value=0).max() < scale \
            else self.ix[measured,i,'N15_delta'].fillna(value=0).max()*1.5
        axs[i].set_xlim(xlimmin, xlimmax)
        axs[i].set_ylim(ylimmin, ylimmax)
        ## Invert axes for representation as in a spectrum
        axs[i].invert_xaxis()
        axs[i].invert_yaxis()
        set_tick_labels()
        # draws axis 0 dotted line
        axs[i].hlines(
            0,
            -100,
            100,
            colors='black',
            linestyles='dotted',
            linewidth=0.25
            )
        axs[i].vlines(
            0,
            -100,
            100,
            colors='black',
            linestyles='dotted',
            linewidth=0.25
            )
        # draws center scale
        axs[i].hlines(
            0,
            -scale,
            scale,
            colors='darkblue',
            linestyles='-',
            linewidth=1
            )
        axs[i].vlines(
            0,
            -scale,
            scale,
            colors='darkblue',
            linestyles='-',
            linewidth=1
            )
        
        return
    
    def plot_cs_scatter_flower(
            self, axs,
            subtitle_fn='Arial',
            subtitle_fs=8,
            subtitle_pad=0.98,
            subtitle_weight='normal',
            x_label='1H (ppm)',
            x_label_fn='Arial',
            x_label_fs=3,
            x_label_pad=2,
            x_label_weight='normal',
            y_label='15N (ppm)',
            y_label_fn='Arial',
            y_label_fs=6 ,
            y_label_pad=2,
            y_label_weight='normal',
            x_ticks_fn='Arial',
            x_ticks_fs=5,
            x_ticks_pad=1,
            x_ticks_weight=1,
            x_ticks_rot=0,
            x_ticks_len=2,
            y_ticks_fn='Arial',
            y_ticks_fs=5,
            y_ticks_pad=1,
            y_ticks_weight=1,
            y_ticks_rot=0,
            y_ticks_len=2,
            xlim=1,
            ylim=1,
            mksize=2,
            color_grad=True,
            color_list=[],
            mk_start_color="#ff0000",
            mk_end_color='#30ff00',
            res_label_color='gold',
            titration_x_values='',
            perform_resevo_fitting=''):
        """
        Plots the chemical shift evolution normalized the reference
        experiment for all the residues in a single plot.
        
        Parameters:
            
            axs (matplotlib subplot axis): the subplot axis array.
        """
        
        # if the user wants a gradient of color
        if color_grad:
            mk_color = self.linear_gradient(
                mk_start_color,
                finish_hex=mk_end_color,
                n=len(self.items)
                )['hex']  # function returns a dictionary
        
        # otherwise the user has input a list of colors
        else: 
            mk_color = color_list
        
        for i, residue in enumerate(self.major_axis):
            
            if self.ix[0,residue,'Peak Status'] == 'unassigned':
                continue
            
            mesmask = self.loc[:,residue,'Peak Status'] == 'measured'
            axs[0].scatter(
                self.loc[mesmask,residue,'H1_delta'],
                self.loc[mesmask,residue,'N15_delta'],
                c=mk_color,
                s=mksize,
                zorder=9
                )
            axs[0].text(
                float(self.loc[mesmask,residue,'H1_delta'].tail(n=1))*1.05,
                float(self.loc[mesmask,residue,'N15_delta'].tail(n=1))*1.05,
                self.ix[0,residue,'ResNo'],
                fontsize=4,
                color=res_label_color,
                zorder=10
                )
        
        # Configure Axis Ticks
        axs[0].xaxis.tick_bottom()
        axs[0].tick_params(
            axis='x',
            pad=x_ticks_pad,
            length=x_ticks_len,
            direction='out'
            )
        axs[0].yaxis.tick_left()
        axs[0].tick_params(
            axis='y',
            pad=y_ticks_pad,
            length=y_ticks_len,
            direction='out'
            )
        ## Configure axes labels
        axs[0].set_xlabel(
            x_label,
            fontsize=x_label_fs,
            labelpad=x_label_pad,
            fontname=x_label_fn,
            weight=x_label_weight
            )
        ## Configure YY ticks/label
        axs[0].set_ylabel(
            y_label,
            fontsize=y_label_fs,
            labelpad=y_label_pad,
            fontname=y_label_fn,
            weight=y_label_weight
            )
        # draws axis 0 dotted line
        axs[0].hlines(
            0,
            -100,
            100,
            colors='black',
            linestyles='dotted',
            linewidth=0.25
            )
        axs[0].vlines(
            0,
            -100,
            100,
            colors='black',
            linestyles='dotted',
            linewidth=0.25
            )
        axs[0].set_xlim(-xlim, xlim)
        axs[0].set_ylim(-ylim, ylim)
        # remember in NMR spectra the ppm scale is 'inverted' :-)
        axs[0].invert_xaxis()
        axs[0].invert_yaxis()
        axs[0].locator_params(axis='both', tight=True, nbins=10)
        axs[0].set_xticklabels(
            axs[0].get_xticks(),
            fontname=x_ticks_fn,
            fontsize=x_ticks_fs,
            fontweight=x_ticks_weight,
            rotation=x_ticks_rot
            )
        axs[0].set_yticklabels(
            axs[0].get_yticks(),
            fontname=y_ticks_fn,
            fontsize=y_ticks_fs,
            fontweight=y_ticks_weight,
            rotation=y_ticks_rot
            )
        
        return
    
    def plot_DPRE_heatmap(
            self, calccol,
            fig, axs,
            i, experiment,
            y_lims=(0,1),
            vmin=0,
            vmax=1,
            ylabel='DELTA PRE',
            x_ticks_fs=4,
            x_ticks_rot=0,
            x_ticks_fn='Arial',
            x_ticks_pad=1,
            x_ticks_weight='normal',
            y_label_fs=6,
            y_label_pad=2,
            y_label_fn='Arial',
            y_label_weight='bold',
            right_margin=0.1,
            bottom_margin=0.1,
            top_margin=0.9,
            cbar_font_size=4,
            tag_line_color='red',
            tag_line_lw=0.3,
            tag_line_ls='-',
            rows=''):
        """
        Plots Delta PRE heatmaps.
        
        Arbesú, M. et al. The Unique Domain Forms a Fuzzy Intramolecular 
        Complex in Src Family Kinases. Structure 25, 630–640.e4 (2017).
        
        Parameters:
            calccol (str): the name of the column to plot.
            
            f: the matplotlib figure object.
            
            axs: matplotlib axis object.
            
            i (int): the index of the subplot axis.
            
            experiment (srt): the name of the data point.
        """
        
        Dcmap = np.array(
            (
                self.loc[experiment,:,calccol].fillna(0),
                self.loc[experiment,:,calccol].fillna(0)
                )
            )
        cleg = axs[i].pcolor(Dcmap, cmap='binary', vmin=vmin, vmax=vmax)
        axs[i].tick_params(axis='y', left='off')
        axs[i].tick_params(axis='x', bottom='off')
        # http://stackoverflow.com/questions/2176424/hiding-axis-text-in-matplotlib-plots
        axs[i].get_yaxis().set_ticks([])
        axs[i].get_xaxis().set_visible(False)
        axs[i].set_ylabel(
            experiment,
            fontsize=y_label_fs,
            labelpad=y_label_pad,
            fontname=y_label_fn,
            weight=y_label_weight
            )
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        self.plot_theo_pre(
            axs[i],
            experiment,
            2,
            bartype = 'hm',
            tag_color=tag_line_color,
            tag_ls=tag_line_ls,
            tag_lw=tag_line_lw
            )
        
        if i == len(self.items)-1:
            
            cbar = plt.colorbar(
                cleg,
                ticks=[vmin, vmax/4, vmax/4*2, vmax/4*3, vmax],
                orientation='vertical',
                cax = fig.add_axes(
                    [
                        right_margin+right_margin*0.05, 
                        bottom_margin, 
                        right_margin*0.05, 
                        top_margin-bottom_margin
                        ]
                    )
                )
            
            cbar.ax.tick_params(labelsize=cbar_font_size)
            axs[i].get_xaxis().set_visible(True)
            axs[i].tick_params(axis='x', bottom='on', length=1.5)
            initialresidue = int(self.ix[0, 0, 'ResNo'])
            finalresidue = int(self.loc[experiment,:,'ResNo'].tail(1))
            
            if self.shape[1] > 100:
                xtick_spacing = self.shape[1]//100*10
            
            else:
                xtick_spacing = 10
            
            first_tick = ceil(initialresidue/10)*xtick_spacing
            xtickarange = np.arange(first_tick, finalresidue+1, xtick_spacing)
            axs[i].set_xticks(xtickarange)
            # https://github.com/matplotlib/matplotlib/issues/6266
            axs[i].set_xticklabels(
                xtickarange,
                fontname=x_ticks_fn,
                fontsize=x_ticks_fs,
                fontweight=x_ticks_weight,
                rotation=x_ticks_rot
                )
            axs[i].tick_params(axis='x', which='major', pad=x_ticks_pad)
            fig.subplots_adjust(
                right=right_margin,
                bottom=bottom_margin,
                top=top_margin,
                hspace=0
                )
        
        return
    
    def plot_DPRE_plot(
            self, calccol,
            axs, i,
            experiment,
            ymax=1.0,
            y_label='DPRE',
            subtitle_fn='Arial',
            subtitle_fs=8,
            subtitle_pad=0.99,
            subtitle_weight='normal',
            x_label_fn='Arial',
            x_label_fs=8,
            x_label_pad=2,
            x_label_weight='bold',
            x_label_rot=0,
            y_label_fn='Arial',
            y_label_fs=8,
            y_label_pad=3,
            y_label_weight='bold',
            y_label_rot=90,
            x_ticks_fn='Arial',
            x_ticks_fs=5,
            x_ticks_weight='normal',
            x_ticks_pad=2,
            x_ticks_len=2,
            x_ticks_rot=0,
            y_ticks_fn='Arial',
            y_ticks_fs=7,
            y_ticks_rot=0,
            y_ticks_pad=1,
            y_ticks_weight='normal',
            y_ticks_len=2,
            y_ticks_nbins=8,
            y_grid_flag=True,
            y_grid_color='lightgrey',
            y_grid_linestyle='-',
            y_grid_linewidth=0.2,
            y_grid_alpha=1,
            tag_cartoon_color='blue',
            tag_cartoon_lw=0.5,
            tag_cartoon_ls=':',
            dpre_ms=2,
            dpre_alpha=0.5,
            smooth_lw=1,
            color=None,
            ref_color='black',
            color_init='#ff00ff',
            color_end='#0000ff',
            grid_color='grey',
            shade=False,
            shade_regions=[(23,37),(0,0),(0,0)],
            res_highlight=True,
            res_hl_list=[25,32,54,64,66,47],
            res_highlight_fs=4,
            res_highlight_y=0.9,
            theo_pre_color='',
            theo_pre_lw='',
            vspace='',
            rows='',
            width=''):
        """
        Plots the Delta PRE data in scatter points and the gaussian
        smoothed curved.
        
        Arbesú, M. et al. The Unique Domain Forms a Fuzzy Intramolecular 
        Complex in Src Family Kinases. Structure 25, 630–640.e4 (2017).
        
        Parameters:
            calccol (str): the name of the column to plot.
            
            axs: matplotlib axis object.
            
            i (int): the index of the subplot axis.
            
            experiment (srt): the name of the data point.
        """
       
        y_lims = (0, ymax)
        # to solve .find Attribute Error
        # http://stackoverflow.com/questions/29437305/how-to-fix-attributeerror-series-object-has-no-attribute-find
        # plots dpre for first point in comparison
        #pmaskr = self.ix[0,:,calccol] > 0
        axs[i].plot(
            self.ix[0,:,'ResNo'].astype(float),
            self.ix[0,:,calccol].astype(float),
            'o',
            markersize=dpre_ms,
            markeredgewidth=0.0,
            c=ref_color,
            alpha=dpre_alpha,
            zorder=10
            )
        # plots dpre for titration data point
        #pmaskd = self.loc[experiment,:,calccol] > 0
        axs[i].plot(
            self.loc[experiment,:,'ResNo'].astype(float),
            self.loc[experiment,:,calccol].astype(float),
            'o',
            c=color,
            markersize=dpre_ms,
            markeredgewidth=0.0,
            alpha=dpre_alpha,
            zorder=10
            )
        # plots dpre_smooth for first data point in comparison
        #pmaskr = self.ix[0,:,calccol+'_smooth'] > 0
        axs[i].plot(
            self.ix[0,:,'ResNo'].astype(float),
            self.ix[0,:,calccol+'_smooth'].astype(float),
            ls='-',
            lw=smooth_lw,
            c=ref_color,
            zorder=10
            )
        # plots dpre_smooth for data point
        #pmaskd = self.loc[experiment,:,calccol+'_smooth'] > 0
        axs[i].plot(
            self.loc[experiment,:,'ResNo'].astype(float),
            self.loc[experiment,:,calccol+'_smooth'].astype(float),
            ls='-',
            lw=smooth_lw,
            c=color,
            zorder=10
            )
        # Configure subplot title
        axs[i].set_title(
            experiment,
            y=subtitle_pad,
            fontsize=subtitle_fs,
            fontname=subtitle_fn,
            fontweight=subtitle_weight
            )
        # Set Ticks
        initialresidue = int(self.ix[0, 0, 'ResNo'])
        finalresidue = int(self.loc[experiment,:,'ResNo'].tail(1))
        
        if self.shape[1] > 100:
            xtick_spacing = self.shape[1]//100*10
        
        else:
            xtick_spacing = 10
        
        first_tick = ceil(initialresidue/10)*xtick_spacing
        xtickarange = np.arange(first_tick, finalresidue+1, xtick_spacing)
        axs[i].set_xticks(xtickarange)
        # https://github.com/matplotlib/matplotlib/issues/6266
        axs[i].set_xticklabels(
            xtickarange,
            fontname=x_ticks_fn,
            fontsize=x_ticks_fs,
            fontweight=x_ticks_weight,
            rotation=x_ticks_rot
            )
        # configures spines
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        # Configures YY ticks
        axs[i].set_ylim(y_lims[0], y_lims[1])
        axs[i].locator_params(axis='y', tight=True, nbins=y_ticks_nbins)
        axs[i].set_yticklabels(
            ['{:.2f}'.format(yy) for yy in axs[i].get_yticks()],
            fontname=y_ticks_fn,
            fontsize=y_ticks_fs,
            fontweight=y_ticks_weight,
            rotation=y_ticks_rot
            )
        # configures tick params
        axs[i].margins(x=0.01)
        axs[i].tick_params(
            axis='x',
            pad=x_ticks_pad,
            length=x_ticks_len,
            direction='out'
            )
        axs[i].tick_params(
            axis='y',
            pad=y_ticks_pad,
            length=y_ticks_len,
            direction='out'
            )
        # Set axes labels
        axs[i].set_xlabel(
            'Residue',
            fontname=x_label_fn,
            fontsize=x_label_fs,
            labelpad=x_label_pad,
            weight=x_label_weight,
            rotation=x_label_rot
            )
        axs[i].set_ylabel(
            y_label,
            fontsize=y_label_fs,
            labelpad=y_label_pad,
            fontname=y_label_fn,
            weight=y_label_weight,
            rotation=y_label_rot
            )
        
        # Adds grid
        if y_grid_flag:
            axs[i].yaxis.grid(
                color=y_grid_color,
                linestyle=y_grid_linestyle,
                linewidth=y_grid_linewidth,
                alpha=y_grid_alpha,
                zorder=0
                )
        
        if shade:
            for lmargin, rmargin in shade_regions:
                axs[i].fill(
                    [lmargin,rmargin,rmargin, lmargin],
                    [0,0,2,2],
                    grid_color,
                    alpha=0.2
                    )
        
        if res_highlight:
            for rr in res_hl_list:
                axs[i].axvline(x=rr, ls=':', lw=0.3, color=grid_color)
                rrmask = self.ix[0,:,'ResNo'] == str(rr)
                l1 = list(self.loc[experiment,rrmask,'1-letter'])
                axs[i].text(
                    rr,
                    y_lims[1]*res_highlight_y,
                    l1[0],
                    ha='center',
                    va='center',
                    fontsize=res_highlight_fs
                    )
        
        self.plot_theo_pre(
            axs[i],
            experiment,
            y_lims[1]*0.1,
            bartype = 'DPRE_plot',
            tag_color=tag_cartoon_color,
            tag_ls=tag_cartoon_ls,
            tag_lw=tag_cartoon_lw
            )
        
        return
    
    def clean_subplots(self, axs, start, end):
        """Hides/Removes the unused subplots from the plotting figure."""
        
        for i in range(start, end):
            axs[i].spines['bottom'].set_visible(False)
            axs[i].spines['top'].set_visible(False)
            axs[i].spines['right'].set_visible(False)
            axs[i].spines['left'].set_visible(False)
            axs[i].tick_params(
                axis='both',
                bottom='off',
                left='off',
                labelleft='off',
                labelbottom='off'
                )
            axs[i].patch.set_alpha(0)
        
        return
    
    def plot_base(
            self, calccol,
            plot_type, plot_style,
            param_dict,
            par_ylims=(0,1),
            ylabel='ppm or ratio',
            hspace=0.5,
            rows_per_page=5,
            cols_per_page=1,
            resonance_type='Backbone',
            fig_height=11.69,
            fig_width=8.69,
            fig_file_type='pdf',
            fig_dpi=300,
            header_fontsize=5):
        """
        The main function that calls and builds the different plots.
        
        Parameters:
            calccol (str): the column to plot.
            
            plot_type (str): {'exp', 'res', 'single'}. 
                'exp' if one subplot for each experiment in series;
                'res' if one subplot per residue;
                'single' if a single plot.
            
            plot_style (str): {'bar_extended', 'bar_compacted',
                'bar_vertical', 'res_evo', 'cs_scatter',
                'cs_scatter_flower', 'heat_map', 'DPRE_plot'}
            
            param_dict (dict): kwargs to be passed to each plotting
                function.
        """
        
        self.log_r('**Plotting** {} for {}...'.format(plot_style, calccol))
        # this to allow folder change in PRE_analysis
        folder = calccol
        
        if plot_type == 'exp':
            num_subplots = len(self.items)
        
        elif plot_type == 'res':
            num_subplots = len(self.major_axis)
        
        elif plot_type == 'single':
            num_subplots = 1
        
        else:
            raise ValueError('Not a valid Farseer plot type')
        
        numrows = ceil(num_subplots/cols_per_page) + 1 
        real_fig_height = (fig_height / rows_per_page) * numrows
        # http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
        fig, axs = plt.subplots(
            nrows=numrows,
            ncols=cols_per_page,
            figsize=(fig_width, real_fig_height)
            )
        axs = axs.ravel()
        plt.tight_layout(
            rect=[0.01,0.01,0.995,0.995],
            h_pad=fig_height/rows_per_page
            )
        # Plots yy axis title
        # http://www.futurile.net/2016/03/01/text-handling-in-matplotlib/
        if plot_style in ['bar_extended', 'bar_compacted']:
            for i, experiment in enumerate(self):
                self.plot_bar_horizontal(
                    plot_style,
                    calccol,
                    axs,
                    i,
                    experiment,
                    y_lims=par_ylims,
                    ylabel=ylabel,
                    **param_dict
                    )
                fig.subplots_adjust(hspace=hspace)
            
            else:
                self.clean_subplots(axs, num_subplots, len(axs))
        
        elif plot_style == 'bar_vertical':
            for i, experiment in enumerate(self):
                self.plot_bar_vertical(
                    calccol,
                    axs,
                    i,
                    experiment,
                    y_lims=par_ylims,
                    ylabel=ylabel,
                    **param_dict
                    )
            
            else:
                self.clean_subplots(axs, num_subplots, len(axs))
        
        elif plot_style == 'res_evo':
            for i, row_number in enumerate(self.major_axis):
                self.plot_res_evo(
                    calccol,
                    axs,
                    i,
                    row_number,
                    y_lims=par_ylims,
                    y_label=ylabel,
                    **param_dict
                    )
            
            else:
                self.clean_subplots(axs, num_subplots, len(axs))
        
        elif plot_style == 'cs_scatter':
            for i, row_number in enumerate(self.major_axis):
                self.plot_cs_scatter(axs, i, row_number, **param_dict)
            
            else:
                self.clean_subplots(axs, num_subplots, len(axs))
        
        elif plot_style == 'cs_scatter_flower':
            self.plot_cs_scatter_flower(axs, **param_dict)
            self.clean_subplots(axs, 1, len(axs))
        
        elif plot_style == 'heat_map':
            for i, experiment in enumerate(self):
                self.plot_DPRE_heatmap(
                    calccol,
                    fig,
                    axs,
                    i,
                    experiment,
                    y_lims=par_ylims,
                    ylabel=ylabel,
                    **param_dict
                    )
            else:
                self.clean_subplots(axs, num_subplots, len(axs))
            
            # to write all the PRE_analysis in the same folder
            folder='PRE_analysis'
            
        elif plot_style == 'DPRE_plot':
            dp_colors = self.linear_gradient(
                param_dict['color_init'],
                param_dict['color_end'],
                n=self.shape[0]
                )
            dp_color = it.cycle(dp_colors['hex'])
            
            for i, experiment in enumerate(self):
                self.plot_DPRE_plot(
                    calccol,
                    axs,
                    i,
                    experiment,
                    color=next(dp_color),
                    **param_dict
                    )
            
            else:
                self.clean_subplots(axs, num_subplots, len(axs))
            
            # to write all the PRE_analysis in the same folder
            folder='PRE_analysis'
            header_fontsize = 3.5
        
        self.write_plot(
            fig,
            header_fontsize,
            plot_style,
            folder,
            calccol,
            fig_file_type,
            fig_dpi
            )
        plt.close('all')
        
        return
    
    def write_plot(
            self, fig, header_fontsize,
            plot_name, folder,
            calccol, fig_file_type, 
            fig_dpi):
        """
        Saves plot figure to a file.
        
        Parameters:
            fig (matplotlib figure object):
            
            plot_name (str): the name of the plot file.
            
            folder (str): the name of the folder to write the plot.
            
            calccol (str): the data column name.
            
            fig_file_type (str): file extension.
            
            fig_dpi (int): the dpi resolution.
        """
        
        plot_folder = '{}/{}'.format(self.tables_and_plots_folder, folder)
        
        if not(os.path.exists(plot_folder)):
            os.makedirs(plot_folder)
        
        file_path = '{}/{}_{}.{}'.format(
            plot_folder,
            calccol,
            plot_name,
            fig_file_type
            )
        header = self.create_header(file_path=file_path)
        fig.text(0.01, 0.01, header, fontsize=header_fontsize)
        fig.savefig(file_path, dpi=fig_dpi)
        self.log_r('**Plot Saved** {}'.format(file_path))
        
        return
    
    def perform_fit(self, col, x_values, mindp, fit_function):
        """
        General workflow for fitting data along X axis.
        
        Note, only one fit can be performed at a time.
        If multiple fits have to be performed, run Faseer-NMR with
        different config files.
        
        Parameters:
            - col: the column containing the data to fit
            - x_values: the x data
            - mindp: minimum number of points to consider residue
                for fitting.
            - fit_function: fitting library name according to
                core.fslibs.fitting_functions.__init__.py
        """
        
        self.fit_performed = True
        
        try:
            to_fit = locate(
                'core.fslibs.fitting_functions.{}'.format(fit_function)
                )()
        
        except TypeError:
            msg = "Chosen fitting function <{}> not an available option.".\
                format(fit_function)
            self.log_r(fsw.gen_wet('ERROR', msg, 23))
            self.abort()
        
        self.log_r("*** Performing fit using function: {}".format(fit_function))
        # logging ###
        not_enough_data = to_fit.not_enough_data
        col_path = '{0}/{1}/'.format(self.tables_and_plots_folder, col)
        
        if not(os.path.exists(col_path)):
            os.makedirs(col_path)
        
        logfrep_name = '{0}/{1}/{1}_fit_report.log'.format(
            self.tables_and_plots_folder,
            col
            )
        logfreport = open(logfrep_name, 'w')
        logfreport.write(to_fit.fit_log_header(col))
        logftable_name = '{0}/{1}/{1}_fit_table.csv'.format(
            self.tables_and_plots_folder,
            col
            )
        logftable = open(logftable_name, 'w')
        logftable.write(to_fit.results_header())
        self.log_r('** Performing fitting for {}...'.format(col))
        measured_mask = self.loc[:,:, 'Peak Status'] == 'measured'
        self.xfit = np.linspace(0, x_values[-1], 200, endpoint=True)
        
        for row in self.major_axis:
            mmask = measured_mask.loc[row,:]
            res = int(self.loc[self.items[0],row, 'ResNo'])
            col_res = "{}_{}".format(col,res)
            xdata = pd.Series(x_values)[np.array(mmask)]
            # .fillna is used to avoid minpack.error:
            # Result from function call is not a proper array of floats.
            ydata = self.loc[mmask,row,col].fillna(value=0.0)
            xdata.index = ydata.index
            
            if mmask.sum() < mindp:
                # residue does not have enough data to perform fit
                logfreport.write(to_fit.not_enough_data(res, xdata, ydata))
                self.fit_okay[col_res] = False
                self.fit_plot_text[col_res] = "not enough data"
                self.fit_plot_ydata[col_res] = None
                continue
            
            a, b, c, d, e = \
                to_fit.fit_data(
                    xdata,
                    ydata,
                    res,
                    self.xfit
                    )
            logfreport.write(a)
            logftable.write(b)
            self.fit_plot_text[col_res] = c
            self.fit_okay[col_res] = d
            self.fit_plot_ydata[col_res] = e
        
        logfreport.close()
        self.log_r("*** Fit report log file written: {}".format(logfrep_name))
        logftable.close()
        self.log_r("*** Fit table log file written: {}".format(logftable_name))
        
        return
    
