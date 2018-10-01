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
import glob
import os
import numpy as np
import pandas as pd
import itertools as it
from pydoc import locate
from math import ceil
from matplotlib import pyplot as plt
import datetime 

import core.fslibs.plotting as fsplot
import core.fslibs.Logger as Logger
from core.fslibs.WetHandler import WetHandler as fsw


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
                ]
            ):
        """Creates the instance attributes."""
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
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
        
        self.info_export = {
            "series_axis":self.series_axis,
            "series_datapoints":self.series_datapoints,
            "next_dim":self.next_dim,
            "prev_dim":self.prev_dim,
            "dim_comparison":self.dim_comparison,
            "para_name":self.para_name,
            "fit_plot_text":self.fit_plot_text,
            "fit_plot_ydata":self.fit_plot_ydata,
            "fit_okay":self.fit_okay,
            "fit_performed":self.fit_performed,
            "PRE_loaded":self.PRE_loaded,
            "paramagnetic_names":self.paramagnetic_names
            }
        
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
        
    def _abort(self, wet):
        """
        Aborts run with message. Writes message to log.
        
        Parameters:
            - wet (WetHandler)
        """
        self.logs(wet.wet)
        self.logs(wet.abort_msg())
        wet.abort()
        
        return None
    
    def _create_header(self, extra_info="", file_path=""):
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
    
    def logs(self, logstr, istitle=False):
        """
        Registers the log string and prints it.
        
        Parameters:
            logstr (str): the string to be registered in the log.
            
            istitle (opt, bool): flag to format logstr as a title.
        """
        
        if istitle:
            logstr = \
"""
{0}  
{1}  
{0}  
""".format('*'*79, logstr)
        
        self.logger.info(logstr)
        
        return None
    
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
        
        self.logs('**Calculated** {}'.format(calccol))
        
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
        self.logs('**Calculated** {}'.format(calccol))
        
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
        self.logs('**Calculated** {}'.format(calccol))
        
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
            self._abort(fsw(
                msg_title="ERROR",
                msg="Paramagnetic Z axis name incorrect",
                wet_num=1
                ))
            return
        self.PRE_loaded = True
        self.info_export["PRE_loaded"] = self.PRE_loaded
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
        self.logs('**Added Theoretical PRE file** {}'.format(pre_file[0]))
        self.logs('*Theoretical PRE for diamagnetic set to 1 by default*')
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
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=15))
        
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
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=17))
        
        self.loc[self.para_name,:,'tag'] = ''
        tagmask = self.loc[self.para_name,:,'ResNo'] == tag
        self.loc[self.para_name,tagmask,'tag'] = '*'
        tagf.close()
        self.logs('**Tag position found** at residue {}'.format(tag_num))
        
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
        self.logs('**Calculated DELTA PRE** for source {} in target {}'.\
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
        self.logs(\
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
        header += self._create_header(
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
        self.logs('**Exported data table:** {}'.format(file_path))
        
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
            header = self._create_header(file_path=file_name)
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
            self.logs('**Exported Chimera Att** {}'.format(file_name))
        
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
            header = self._create_header(
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
            self.logs('**Exported parsed peaklist** {}'.format(file_path))
            fileout.close()
        
        return
    
    def plot_base(
            self,
            calccol,
            plot_style,
            config={"dummy":"var"},
            resonance_type='Backbone',
            header_fontsize=5,
            fig_file_type='pdf'
            ):
        """
        The main function that calls and builds the different plots.
        
        Parameters:
            calccol (str): the column to plot selected from the dataframe.
            
            plot_style (str): {'bar_extended', 'bar_compacted',
                'bar_vertical', 'res_evo', 'cs_scatter',
                'cs_scatter_flower', 'heat_map', 'DPRE_plot'}
            
            config (dict): config dictionary passed to the plotting function.
                Updates the default plotting config.
            
            header_fontsize (int): the font size of the information header
                printed to the plot.
            
            fig_file_type (str): file type of the saved plot file.
        """
        
        self.logs('**Plotting** {} for {}...'.format(plot_style, calccol))
        # this to allow folder change in PRE_analysis
        
        kwargs = {
            **self.info_export,
            "calccol":calccol
            }
        
        self.logger.debug("...Preparing figure information")
        if plot_style in ["DPRE_plot"]:
            folder='PRE_analysis'
        else:
            folder = calccol
        
        plot_folder = os.path.join(
            self.tables_and_plots_folder,
            folder
            )
        
        if not(os.path.exists(plot_folder)):
            os.makedirs(plot_folder)
        
        file_name = '{}_{}.{}'.format(
            calccol,
            plot_style,
            fig_file_type
            )
        
        file_path = os.path.join(
            plot_folder,
            file_name
            )
        
        header = self._create_header(file_path=file_path)
        
        config = {
            **config,
            "figure_header":header,
            "header_fontsize":header_fontsize,
            "figure_path":file_path
            }
        
        if resonance_type == 'Backbone':
            
            col_labels = [
                "ResNo",
                "1-letter",
                "3-letter",
                "Peak Status",
                "Merit",
                "Fit Method",
                "Vol. Method",
                "Details"
                ]
        
        elif resonance_type == 'Sidechains':
            
            col_labels = [
                "ResNo",
                "1-letter",
                "3-letter",
                "Peak Status",
                "Merit",
                "Fit Method",
                "Vol. Method",
                "Details",
                "ATOM"
                ]
            
        data_info = np.array(self.loc[:,:,col_labels].fillna('NaN').astype(str))
        
        if plot_style in [
                'bar_extended',
                'bar_compacted',
                'bar_vertical',
                'res_evo'
                ]:
            if calccol in ["H1_delta", "N15_delta", "CSP"]:
                partype = 'ppm'
            elif calccol in ["Height_ratio", "Vol_ratio"]:
                partype = 'ratio'
            
            if self.PRE_loaded:
                kwargs["data_extra"] = \
                    np.array(self.loc[:,:,["Theo PRE","tag"]].fillna('NaN'))
                
            data = np.array(self.loc[:,:,calccol]).astype(float).T
            
            if resonance_type == 'Sidechains':
                
                plot = fsplot.BarExtendedSideChains(
                    data,
                    data_info,
                    partype=partype,
                    config=config,
                    exp_names=list(self.items),
                    **kwargs
                    )
            
            elif resonance_type == 'Backbone':
                
                if plot_style == 'bar_extended':
                    
                    plot = fsplot.BarExtendedHorizontal(
                        data,
                        data_info,
                        partype=partype,
                        config=config,
                        exp_names=list(self.items),
                        **kwargs
                        )
                
                elif plot_style == 'bar_compacted':
                    
                    plot = fsplot.BarCompacted(
                        data,
                        data_info,
                        config=config,
                        partype=partype,
                        exp_names=list(self.items),
                        **kwargs
                        )
                
                elif plot_style == 'bar_vertical':
                    plot = fsplot.BarExtendedVertical(
                        data,
                        data_info,
                        config=config,
                        partype=partype,
                        exp_names=list(self.items),
                        **kwargs
                        )
        
                elif plot_style == 'res_evo':
                    plot = fsplot.ResEvoPlot(
                        data,
                        data_info,
                        config=config,
                        exp_names=list(self.items),
                        **kwargs
                        )
        
        elif plot_style == 'cs_scatter':
            plot = fsplot.ChemicalShiftScatterPlot(
                np.array(self.loc[:,:,["H1_delta","N15_delta"]]).astype(float),
                data_info,
                config=config,
                exp_names=list(self.items),
                **kwargs
                )
        
        elif plot_style == 'cs_scatter_flower':
            plot = fsplot.CSScatterFlower(
                np.array(self.loc[:,:,["H1_delta","N15_delta"]]).astype(float),
                data_info,
                config=config,
                exp_names=list(self.items),
                **kwargs
                )
        
        elif plot_style == 'heat_map':
            
            kwargs["data_extra"] = \
                np.array(self.loc[:,:,"tag"].fillna('NaN')).T
            
            config["header_fontsize"] = 3.5
            
            plot = fsplot.DeltaPREHeatmap(
                np.array(self.loc[:,:,calccol]).astype(float).T,
                data_info,
                config=config,
                exp_names=list(self.items),
                **kwargs
                )
        
        elif plot_style == 'DPRE_plot':
            
            config["header_fontsize"] = 3.5
            
            smooth = "{}_smooth".format(calccol)
            
            kwargs["data_extra"] = \
                np.array(self.loc[:,:,["tag",smooth]])
            
            plot = fsplot.DeltaPREPlot(
                np.array(self.loc[:,:,calccol]).astype(float).T,
                data_info,
                config=config,
                exp_names=list(self.items),
                **kwargs
                )
                
        
        else:
            msg = "You asked for some plot definitions that can't be done. Plot_tyle {}".format(plot_style)
            wet = fsw(msg=msg, msg_title="WARNING", wet_num=99)
            self._abort(wet)
        
        plot.plot()
        plot.save_figure()
        plt.close(plot.figure)
        
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
            self._abort(fsw(msg_title='ERROR', msg=msg, wet_num=23))
        
        self.logs("*** Performing fit using function: {}".format(fit_function))
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
        self.logs('** Performing fitting for {}...'.format(col))
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
        self.logs("*** Fit report log file written: {}".format(logfrep_name))
        logftable.close()
        self.logs("*** Fit table log file written: {}".format(logftable_name))
        
        self.fit_data_dict = {
            "fit_performed":self.fit_performed,
            "xfit":self.xfit,
            "fit_plot_text":self.fit_plot_text,
            "fit_plot_ydata":self.fit_plot_ydata,
            "fit_okay":self.fit_okay
            }
        
        self.info_export.update(self.fit_data_dict)
        
        return
    
if __name__ == "__main__":
    
    print('FarseerSeries')
