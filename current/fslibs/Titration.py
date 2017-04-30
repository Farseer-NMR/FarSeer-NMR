import glob
import os
import numpy as np
import pandas as pd
from math import ceil
import scipy.optimize as sciopt
import itertools as it
from matplotlib import pyplot as plt

import farseer_user_variables as fsuv
import farseermain as fsm
import fslibs.parameters as fspar
import fslibs.utils as fsut

#from matplotlib.colors import colorConverter
#from math import ceil as mceil

class Titration(pd.Panel):
    """
    The titration object inherits a pd.Panel.
    Is a panel where each item is an experiment,
    and the progression along Items is the evolution of the titration.
    """
    # how to represent lost values
    cs_lost = fsuv.cs_lost
    calc_parameters_list = 0
    # folder to store titration calculations
    calc_folder = 'Calculations'  
    # folder to store comparisons among calculations
    comparison_folder = 'Comparisons'  
    # subfolder to store tables and plots
    tables_and_plots_folder = 'TablesAndPlots'
    # subfolder to store ChimeraAttributeFiles
    chimera_att_folder = 'ChimeraAttributeFiles'
    # subfolder to store full formatted peaklists
    export_tit_folder = 'FullPeaklists'
    # dictionary to store dataframes with information on fitting results
    fitdf = {}
    # prepares dictionary that stores alpha values to use in CSPs calculations
    # to correct 15N dimension
    csp_alpha4res = {key:fsuv.csp_alpha4res for key in 'ARNDCEQGHILKMFPSTWYV'}
    for k, v in fsuv.csp_res_exceptions.items():
        csp_alpha4res[k] = v
    
    def create_titration_attributes(self, tittype='cond',
                                          owndim_pts=['foo'],
                                          dim1_pts='bar',
                                          dim2_pts='zoo',
                                          dim_comparison='not applied',
                                          resonance_type='Backbone'):
        # I think I created this function because I couldn't initialise all
        # these parameters with the init()
        
        # variables that store characteristics of the titration.
        self.tittype = tittype
        self.att_dict = owndim_pts
        self.dim1_pts = dim1_pts
        self.dim2_pts = dim2_pts
        self.dim_comparison = dim_comparison
        self.resonance_type = resonance_type
        self.res_info = \
            self.loc[:,:,['Res#','1-letter','3-letter','Peak Status']]
        
        # defines the path to store the calculations
        # if stores the result of a calculation
        if tittype.startswith('cond'):
            self.calc_path = '{}/{}/{}/{}/{}'.format(self.resonance_type,
                                                     self.calc_folder,
                                                     self.tittype,
                                                     self.dim2_pts,
                                                     self.dim1_pts)
        # if stores comparisons among calculations
        elif tittype.startswith('C'):
            self.calc_path = '{}/{}/{}/{}/{}/{}'.format(self.resonance_type,
                                                        self.comparison_folder,
                                                        self.tittype,
                                                        self.dim_comparison,
                                                        self.dim2_pts,
                                                        self.dim1_pts)
        
        # Create all the folder necessary to store the data.
        # folders are created here when generating the object to avoind having
        # os.makedirs spread over the code, in this way all the folders created
        # are here summarized
        if not(os.path.exists(self.calc_path)):
            os.makedirs(self.calc_path)
        
        self.chimera_att_folder = '{}/{}'.format(self.calc_path,
                                                 self.chimera_att_folder)
        if not(os.path.exists(self.chimera_att_folder)):
            os.makedirs(self.chimera_att_folder)
        
        self.tables_and_plots_folder = \
            '{}/{}'.format(self.calc_path, self.tables_and_plots_folder)
        if not(os.path.exists(self.tables_and_plots_folder)):
            os.makedirs(self.tables_and_plots_folder)
        
        self.export_tit_folder = '{}/{}'.format(self.calc_path,
                                                self.export_tit_folder)
        if not(os.path.exists(self.export_tit_folder)):
            os.makedirs(self.export_tit_folder)
        
    @property
    def _constructor(self):
        # because Titration inherits a pd.Panel.
        return Titration
    
    def calc_cs_diffs(self, calccol, sourcecol):
        '''
        Calculates the difference between two columns along a Titration 
        using as reference the column from the reference experiment, 
        which is always stored in Item=0.
        
        Calculation result is stored in a new column of each DataFrame.
        '''
        self.loc[:,:,calccol] = \
            self.loc[:,:,sourcecol].sub(self.ix[0,:,sourcecol], axis='index')
        
        # sets lost peaks results according to the fsuv.cs_lost
        if self.cs_lost == 'full':
            for item in self.items:
                mask_lost = self.loc[item,:,'Peak Status'] == 'lost'
                self.loc[item,mask_lost,calccol] = 1.
        
        elif self.cs_lost == 'prev':
            for iitem in range(1, len(self.items)):
                mask_lost = self.ix[iitem,:,'Peak Status'] == 'lost'
                self.ix[iitem,mask_lost,calccol] = \
                    self.ix[iitem-1,mask_lost,calccol]
        
        fsut.write_log('*** Calculated {}\n'.format(calccol))
    
    def calc_ratio(self, calccol, sourcecol):
        '''
        Calculates the ration between two columns along a Titration
        using as reference the column from the reference experiment, 
        which is always stored in Item=0.
        
        Calculation result is stored in a new column of each DataFrame.
        '''
        self.loc[:,:,calccol] = \
            self.loc[:,:,sourcecol].div(self.ix[0,:,sourcecol], axis='index')
        fsut.write_log('*** Calculated {}\n'.format(calccol))
    
    def load_theoretical_PRE(self, spectra_path, dimpt):
        """
        Loads theoretical PRE values to represent in bar plots.
        Theorital PRE files (*.pre) should be stored in a 'para' folder
        at the cond3 hierarchy level.
        
        Reads information on the tag position which should be inpu in the
        *.pre file as an header comment, for example, '#40'.
        
        """
        
        target_folder = '{}/para/{}/'.format(spectra_path.strip('/'), dimpt)
        pre_file = glob.glob('{}*.pre'.format(target_folder))
        
        if len(pre_file) > 1:
            raise ValueError(   
                '@@@ There are more than one .pre file in the folder {}'.\
                format(target_folder))
        elif len(pre_file) < 1:
            raise ValueError('@@@ There is no .pre file in folder {}'.\
                format(target_folder))
        
        # loads theoretical PRE data to 'Theo PRE' new column
        # sets 1 to the diamagnetic Item.
        self.predf = pd.read_csv(pre_file[0], sep='\s+', usecols=[1],
                                 names=['Theo PRE'], comment='#')
        fsut.write_log(\
            '*** Added Theoretical PRE file {}\n'.format(pre_file[0]))
        fsut.write_log(\
            '*** Theoretical PRE for diamagnetic set to 1 by default\n')
        self.loc[:,:,'Theo PRE'] = 1
        self.loc['para',:,'Theo PRE'] = self.predf.loc[:,'Theo PRE']
        
        # reads information on the tag position.
        tagf = open(pre_file[0], 'r')
        tag = tagf.readline().strip().strip('#')
        self.loc['para',:,'tag'] = ''
        tagmask = self.loc['para',:,'Res#'] == tag
        self.loc['para',tagmask,'tag'] = '*'
        tagf.close()
        
        
    def calc_Delta_PRE(self, sourcecol, targetcol,
                       apply_smooth=True,
                       gaussian_stddev=1,
                       guass_x_size=7):
        
        # astropy is imported to avoind demanding import when not necessary
        from astropy.convolution import Gaussian1DKernel, convolve
        
        # http://docs.astropy.org/en/stable/api/astropy.convolution.Gaussian1DKernel.html
        gauss = Gaussian1DKernel(gaussian_stddev, x_size=guass_x_size)
        
        self.loc[:,:,targetcol] = \
            self.loc[:,:,'Theo PRE'].sub(self.loc[:,:,sourcecol])
        
        fsut.write_log(\
            '*** Calculated DELTA PRE for source {} in target {}\n'.\
            format(sourcecol, targetcol))
        
        for exp in self.items:
            # converts to 0 negative values
            negmask = self.loc[exp,:,targetcol] < 0
            self.loc[exp,negmask,targetcol] = 0
            
            if apply_smooth:
                # aplies convolution with a normalized 1D Gaussian kernel
                smooth_col = '{}_smooth'.format(targetcol)
                self.loc[exp,:,smooth_col] = \
                    convolve(np.array(self.loc[exp,:,targetcol]),
                             gauss,
                             boundary='extend',
                             normalize_kernel=True)
        
        fsut.write_log(\
        '*** Calculated DELTA PRE Smoothed for source {} in target {} \
with window size {} and stdev {} \n'.\
            format(sourcecol, targetcol, guass_x_size, gaussian_stddev))
    
    def csp_willi(self, s):
        """
        This function performs the CSP calculation.

        np.sqrt(0.5*(H1**2 + (alpha*N15)**2))

        where the proportional normalization factor (alpha) of the 15N
        dimension is set by default to 0.2 for Glycine and 0.14 for all
        the other residues.

        Williamson, M. P. Using chemical shift perturbation to
        characterise ligand binding. Prog. Nuc. Magn. Res. Spect.
        73, 1–16 (2013). SEE CORRIGENDUM
        """
        return np.sqrt(0.5*(s[1]**2+(self.csp_alpha4res[s[0]]*s[2]**2)))
    
    def calc_csp(self, calccol='CSP',
                       pos1='PosF1_delta',
                       pos2='PosF2_delta'):
        """
        Calculates the Chemical Shift Perturbation (CSP) values
        based on a formula.
        """
        
        self.loc[:,:,calccol] = \
            self.loc[:,:,['1-letter',pos1,pos2]].\
                apply(lambda x: self.csp_willi(x), axis=2)
        fsut.write_log('*** Calculated {}\n'.format(calccol))
    
    def write_table(self, tablecol):
        '''
        Writes the values of a specific column along the titration to a tsv table.
        '''
        
        # concatenates the values of the table with the residues numbers
        table = pd.concat([self.res_info.iloc[0,:,[0]], self.loc[:,:,tablecol].astype(float)], axis=1)
        
        if not(os.path.exists('{}/{}'.format(self.tables_and_plots_folder,
                                             tablecol))):
            os.makedirs('{}/{}'.format(self.tables_and_plots_folder, tablecol))
        
        file_path = '{0}/{1}/{1}.tsv'.format(self.tables_and_plots_folder,
                                                 tablecol)
        
        fileout = open(file_path, 'w')
        
        if self.tittype.startswith('cond'):
            header = \
"""# Table for '{0}' resonances.
# A titration results for variable '{1}'
# ranging datapoints '{2}', where:
# conditions '{3}' and '{4}' are kept constants.
# {5} data.
""".format(self.resonance_type, self.tittype, list(self.att_dict),
           self.dim2_pts, self.dim1_pts, tablecol)
        
        elif self.tittype.startswith('C'):
            header = \
"""# Table for '{0}' resonances.
# The comparison '{1}': for the results obtained for titrations 'cond{7}'
# across variable '{2}' which ranges datapoints '{3}', where:
# conditions '{4}' and '{5}' are kept constants.
# {6} data.
""".format(self.resonance_type, self.tittype, self.dim_comparison,
           list(self.att_dict), self.dim2_pts, self.dim1_pts, tablecol,
           self.tittype[-1])
        
        fileout.write(header)
        fileout.write(table.to_csv(sep='\t', index=False,
                      na_rep='NaN', float_format='%.4f'))
        fileout.close()
        fsut.write_log('*** File saved {}\n'.format(file_path))
    
    def export_titration(self):
        """
        Exports the titration experiments (measured and
        calculated data) to .tsv files. These files are stored
        in the folder 'full_peaklists'.
        """
        for item in self.items:
            file_path = '{}/{}.tsv'.format(self.export_tit_folder, item)
            fileout = open(file_path, 'w')
            fileout.write(self.loc[item].to_csv(sep='\t',
                                                index=False,
                                                na_rep='NaN',
                                                float_format='%.4f'))
            fileout.close()
            fsut.write_log('*** File saved {}\n'.format(file_path))
    
    def set_item_colors(self, items, series, d):
        """
        Creates a list of colors based on a series of items and a
        dictionary to translate the series keys to a value.
        """
        for i, it in enumerate(items):
            if series[i] in d.keys():
                it.set_color(d[series[i]])
            else:
                continue
    
    def text_marker(self, ax, axbar, series, d, yy_scale,
                          fs=3,
                          orientation='horizontal'):
        """Places a text mark over the bars of a Bar Plot."""
        def vpos_sign(x, y):
            """Scales to the vertical position positive and negative."""
            if y>=0:
                return x
            else:
                return (x*-1)-(yy_scale/20)
        
        def hpos_sign(x, y):
            """Scales to the horizontal position positive and negative."""
            if y >= 0:
                return x+(yy_scale/20)
            else:
                return (x*-1)-(yy_scale/20)
            
        for i, bar in enumerate(axbar):
            if series[i] in d.keys():
                x0, y0 = bar.xy
                if orientation == 'vertical':
                    hpos = hpos_sign(bar.get_width(), x0)
                    vpos = bar.get_y() - bar.get_height() / 2.5
                elif orientation == 'horizontal':
                    vpos = vpos_sign(bar.get_height(), y0)
                    hpos = bar.get_x() + bar.get_width() / 2.5
                ax.text(hpos, vpos, d[series[i]],
                        ha='center', va='bottom', fontsize=fs)
            else:
                continue
    
    def plot_threshold(self, ax, series, color, lw, alpha,
                       orientation = 'horizontal'):
        """Plots threshold line that identifies relevant perturnations."""
        
        sorted_cs = series.abs().sort_values().dropna()
        firstdecile = sorted_cs[0:ceil(0.1*len(sorted_cs))]
        threshold = firstdecile.mean() + 5*firstdecile.std()
        if orientation == 'horizontal':
            ax.axhline(y=threshold, color=color, 
                       linewidth=lw, alpha=alpha, zorder=0)
            
            # in case there are negative numbers, plots the threshold,
            # if there are not negative numbers, this line is never displayed
            ax.axhline(y=-threshold, color=color, 
                       linewidth=lw, alpha=alpha, zorder=0)
        if orientation == 'vertical':
            ax.axvline(x=threshold, color=color, 
                       linewidth=lw, alpha=alpha, zorder=0)
            
            # in case there are negative numbers, plots the threshold,
            # if there are not negative numbers, this line is never displayed
            ax.axvline(x=-threshold, color=color, 
                       linewidth=lw, alpha=alpha, zorder=0)
    
    def theo_pre_plot(self, axs, exp, y,
                      bartype='h',
                      pre_color='lightblue',
                      pre_lw=1,
                      tag_color='red',
                      tag_ls='-',
                      tag_lw=0.1
                      ):
        
        if (self.tittype == 'cond3' and exp == 'para') \
            or (self.tittype == 'C3' \
                and ( self.dim1_pts == 'para' or self.dim2_pts == 'para')):
            # plot theoretical PRE
            if bartype == 'v':
                axs.plot(self.loc[exp,:,'Theo PRE'],
                         self.loc[exp,::-1,'Res#'].astype(float),
                         zorder=9, color=pre_color, lw=pre_lw)
            elif bartype == 'h':
                axs.plot(self.loc[exp,:,'Res#'].astype(float),
                         self.loc[exp,:,'Theo PRE'],
                         zorder=9, color=pre_color, lw=pre_lw)
            
            # plot tag position
            xtagm = self.loc[exp,:,'tag']=='*'
            xtag = self.loc[exp,xtagm,'Res#'].astype(float)
            
            if bartype in ['h', 'osci']:
                axs.vlines(xtag, 0, y,
                          colors=tag_color, linestyle=tag_ls,
                          linewidth=tag_lw, zorder=10)
                axs.plot(xtag,
                         y, 'o',
                         zorder=10, color='red', markersize=2)
            
            elif bartype == 'v':
                xtag = self.shape[1]-xtag+1
                axs.hlines(xtag, 0, y,
                          colors=tag_color, linestyle=tag_ls,
                          linewidth=tag_lw, zorder=10)
                axs.plot(y, xtag,
                         'o',
                         zorder=10, color='red', markersize=2)
            
            elif bartype == 'hm':
                
                axs.vlines(xtag-0.5, 0, y,
                          colors=tag_color, linestyle=tag_ls,
                          linewidth=tag_lw, zorder=10)
        
        else:
            return
    
    def plot_bar_horizontal(self, plot_style, calccol, fig, axs, i, experiment,
                          y_lims=(0,1),
                          ylabel='ppm or ratio',
                          
                          measured_color='black',
                          status_color_flag=True,
                          lost_color='red',
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
                          PRE_flag=False,
                          pre_color='red',
                          pre_lw=0.2,
                          tag_color='magenta',
                          tag_lw=0.2,
                          tag_ls=':',
                          
                          x_ticks_color_flag=True,
                          x_ticks_fn='monospace',
                          x_ticks_fs=6,
                          x_ticks_weight='normal',
                          x_ticks_rot=90,
                          unassigned_shade=False,
                          unassigned_shade_alpha=0.5):
        """
        :param: idx, calculated parameter, that is index to param_settings
        """
        
        if plot_style == 'bar_extended' and self.resonance_type == 'Backbone':
            # fillna(0) is added because nan conflicts with text_maker()
            # in bat.get_height() which return nan
            bars = axs[i].bar(self.loc[experiment,:,'Res#'].astype(float),
                            self.loc[experiment,:,calccol].fillna(0),
                            width=bar_width,
                            align='center',
                            alpha=bar_alpha,
                            linewidth=bar_linewidth,
                            zorder=4)
        
            # Configure XX ticks and Label
            axs[i].set_xticks(np.arange(float(self.loc[experiment,:,'Res#'].head(1)),
                                        float(self.loc[experiment,:,'Res#'].tail(1))+1,
                                        1))
        
            ## https://github.com/matplotlib/matplotlib/issues/6266
            axs[i].set_xticklabels(self.loc[experiment,:,['Res#','1-letter']].apply(lambda x: ''.join(x), axis=1),
                                 fontname=x_ticks_fn,
                                 fontsize=x_ticks_fs,
                                 fontweight=x_ticks_weight,
                                 rotation=x_ticks_rot)
            # defines xticks colors
            if x_ticks_color_flag:
                self.set_item_colors(axs[i].get_xticklabels(), self.loc[experiment, :, 'Peak Status'],
                                  {'measured':measured_color,
                                   'lost':lost_color,
                                   'unassigned':unassigned_color})
            
        elif plot_style == 'bar_extended' and self.resonance_type == 'Sidechains':
            bars = axs[i].bar(self.major_axis,
                            self.loc[experiment,:,calccol].fillna(0),
                            width=bar_width,
                            align='center',
                            alpha=bar_alpha,
                            linewidth=bar_linewidth,
                            zorder=4)
        
            # Configure XX ticks and Label
            axs[i].set_xticks(self.major_axis)
        
            ## https://github.com/matplotlib/matplotlib/issues/6266
            axs[i].set_xticklabels(self.loc[experiment,:,['Res#','1-letter', 'ATOM']].apply(lambda x: ''.join(x), axis=1),
                                   fontname=x_ticks_fn,
                                 fontsize=x_ticks_fs,
                                 fontweight=x_ticks_weight,
                                 rotation=x_ticks_rot)
            # defines xticks colors
            if x_ticks_color_flag:
                self.set_item_colors(axs[i].get_xticklabels(), self.loc[experiment, :, 'Peak Status'],
                                  {'measured':measured_color,
                                   'lost':lost_color,
                                   'unassigned':unassigned_color})
        
        elif plot_style == 'bar_compacted':
            bars = axs[i].bar(self.loc[experiment,:,'Res#'].astype(float),
                              self.loc[experiment,:,calccol].fillna(0),
                               width=bar_width,
                               align='center',
                               alpha=bar_alpha,
                               linewidth=bar_linewidth,
                               zorder=4)
            
            initialresidue = int(self.ix[0, 0, 'Res#'])
            finalresidue = int(self.loc[experiment,:,'Res#'].tail(1))
            first_tick = ceil(initialresidue/10)*10
            axs[i].set_xticks(np.arange(first_tick, finalresidue+1, 10))
            # https://github.com/matplotlib/matplotlib/issues/6266
            axs[i].set_xticklabels(np.arange(first_tick, finalresidue, 10),
                                   fontname=x_ticks_fn,
                                   fontsize=x_ticks_fs,
                                   fontweight=x_ticks_weight,
                                   rotation=x_ticks_rot)
            
            
            if unassigned_shade:
                unassignedmask = self.loc[experiment, :, 'Peak Status'] == 'unassigned'
                for residue in self.loc[experiment, unassignedmask, 'Res#']:
                    residue = int(residue) - 0.5
                    axs[i].axvspan(residue, residue+1,
                                   color=unassigned_color,
                                   alpha=unassigned_shade_alpha,
                                   lw=0)
        
        # Set subplot titles
        axs[i].set_title(experiment, y=subtitle_pad, fontsize=subtitle_fs, fontname=subtitle_fn, weight=subtitle_weight)
        
        # defines bars colors
        self.set_item_colors(bars, self.loc[experiment,:,'Peak Status'],
                              {'measured':measured_color,
                               'lost':lost_color,
                               'unassigned':unassigned_color})
        
        # configures spines
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        
        
        # cConfigures YY ticks
        axs[i].set_ylim(y_lims[0], y_lims[1])
        axs[i].locator_params(axis='y', tight=True, nbins=y_ticks_nbins)
        axs[i].set_yticklabels(['{:.2f}'.format(yy) for yy in axs[i].get_yticks()],
                               fontname=y_ticks_fn,
                               fontsize=y_ticks_fs,
                               fontweight=y_ticks_weight,
                               rotation=y_ticks_rot)
        
        # configures tick params
        axs[i].margins(x=0.01)
        axs[i].tick_params(axis='x',
                           pad=x_ticks_pad,
                           length=x_ticks_len,
                           direction='out')
                           
        axs[i].tick_params(axis='y',
                           pad=y_ticks_pad,
                           length=y_ticks_len,
                           direction='out')
        
        # Set axes labels
        axs[i].set_xlabel('Residue',
                          fontname=x_label_fn,
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          weight=x_label_weight,
                          rotation=x_label_rot)
        
        axs[i].set_ylabel(ylabel,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight,
                          rotation=y_label_rot)
        
        # Adds grid
        if y_grid_flag:
            axs[i].yaxis.grid(color=y_grid_color,
                              linestyle=y_grid_linestyle,
                              linewidth=y_grid_linewidth,
                              alpha=y_grid_alpha,
                              zorder=0)
                              
        # Adds red line to identify significant changes.
        if threshold_flag and calccol in fspar.param_settings.index[:3]:
            self.plot_threshold(axs[i], self.loc[experiment,:,calccol], threshold_color,
                                threshold_linewidth, threshold_alpha)
        
        if mark_prolines_flag:
            self.text_marker(axs[i],
                              bars,
                              self.loc[experiment,:,'1-letter'],
                              {'P':mark_prolines_symbol},
                              y_lims[1],
                              fs=mark_fontsize)
        
        if mark_user_details_flag:
            self.text_marker(axs[i],
                              bars,
                              self.loc[experiment,:,'Details'],
                              user_marks_dict,
                              y_lims[1],
                              fs=mark_fontsize)
                          
        if color_user_details_flag:
            self.set_item_colors(bars, self.loc[experiment,:,'Details'],
                                  user_bar_colors_dict)
        
        if PRE_flag and (calccol in fspar.param_settings.index[3:]):
            self.theo_pre_plot(axs[i], experiment, y_lims[1]*0.05,
                              bartype='h',
                              pre_color=pre_color,
                              pre_lw=pre_lw,
                              tag_color=tag_color,
                              tag_ls=tag_ls,
                              tag_lw=tag_lw)
    
    def plot_bar_vertical(self, calccol, fig, axs, i, experiment,
                          y_lims=(0,1),
                          ylabel='ppm or ratio',
                          
                          measured_color='black',
                          status_color_flag=True,
                          lost_color='red',
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
                          PRE_flag=False,
                          pre_color='red',
                          pre_lw=0.2,
                          tag_color='magenta',
                          tag_lw=0.2,
                          tag_ls=':',
                          
                          x_ticks_color_flag=True,
                          x_ticks_fn='monospace',
                          x_ticks_fs=6,
                          x_ticks_weight='normal',
                          x_ticks_rot=0):
        """
        :param: idx, calculated parameter, that is index to param_settings
        """

        # fillna(0) is added because nan conflicts with text_maker() .iloc[::-1]
        # in bat.get_height() which return nan
        bars = axs[i].barh(self.loc[experiment,::-1,'Res#'].astype(float),
                         self.loc[experiment,::-1,calccol].fillna(0),
                         height=bar_width,
                         align='center',
                         alpha=bar_alpha,
                         linewidth=bar_linewidth,
                         zorder=4)
        
        # Set subplot titles
        axs[i].set_title(experiment, y=subtitle_pad, fontsize=subtitle_fs, fontname=subtitle_fn, weight=subtitle_weight)
        
        # defines bars colors
        self.set_item_colors(bars, self.loc[experiment,::-1,'Peak Status'].reset_index(drop=True),
                              {'measured':measured_color,
                               'lost':lost_color,
                               'unassigned':unassigned_color})
        
        # configures spines
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        
        # Configure XX ticks and Label
        axs[i].margins(y=0.01)
        
        axs[i].set_yticks(np.arange(float(self.loc[experiment,:,'Res#'].head(1)),
                                    float(self.loc[experiment,:,'Res#'].tail(1))+1,
                                    1))
    
        ## https://github.com/matplotlib/matplotlib/issues/6266
        axs[i].set_yticklabels(self.loc[experiment,::-1,['Res#','1-letter']].apply(lambda x: ''.join(x), axis=1),
                             fontname=x_ticks_fn,
                             fontsize=x_ticks_fs-2,
                             fontweight=x_ticks_weight,
                             rotation=0)
        # defines xticks colors
        if x_ticks_color_flag:
            self.set_item_colors(axs[i].get_yticklabels(),
                                 self.loc[experiment,::-1,'Peak Status'].reset_index(drop=True),
                                  {'measured':measured_color,
                                   'lost':lost_color,
                                   'unassigned':unassigned_color})
        
        
        
        # cConfigures YY ticks
        axs[i].set_xlim(y_lims[0], y_lims[1])
        axs[i].locator_params(axis='x', tight=True, nbins=y_ticks_nbins)
        axs[i].set_xticklabels(['{:.2f}'.format(xx) for xx in axs[i].get_xticks()],
                               fontname=y_ticks_fn,
                               fontsize=y_ticks_fs,
                               fontweight=y_ticks_weight,
                               rotation=-45)
        
        # configures tick params
        axs[i].tick_params(axis='y',
                           pad=x_ticks_pad,
                           length=x_ticks_len,
                           direction='out')
                           
        axs[i].tick_params(axis='x',
                           pad=y_ticks_pad,
                           length=y_ticks_len,
                           direction='out')
        
        # Set axes labels
        axs[i].set_ylabel('Residue',
                          fontname=x_label_fn,
                          fontsize=x_label_fs,
                          labelpad=x_label_pad+6,
                          weight=x_label_weight,
                          rotation=x_label_rot)
        
        axs[i].set_xlabel(ylabel,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight,
                          rotation=0)
        
        # Adds grid
        if y_grid_flag:
            axs[i].xaxis.grid(color=y_grid_color,
                              linestyle=y_grid_linestyle,
                              linewidth=y_grid_linewidth,
                              alpha=y_grid_alpha,
                              zorder=0)
        
        # Adds red line to identify significant changes.
        if threshold_flag and calccol in fspar.param_settings.index[:3]:
            self.plot_threshold(axs[i],
                                self.loc[experiment,:,calccol],
                                threshold_color,
                                threshold_linewidth,
                                threshold_alpha,
                                orientation='vertical')
        
        if mark_prolines_flag:
            self.text_marker(axs[i],
                              bars,
                              self.loc[experiment,::-1,'1-letter'].reset_index(drop=True),
                              {'P':mark_prolines_symbol},
                              y_lims[1]*0.6,
                              fs=mark_fontsize,
                              orientation='vertical')
        
        if mark_user_details_flag:
            self.text_marker(axs[i],
                              bars,
                              self.loc[experiment,::-1,'Details'].reset_index(drop=True),
                              user_marks_dict,
                              y_lims[1],
                              fs=mark_fontsize,
                              orientation='vertical')
        
        if color_user_details_flag:
            self.set_item_colors(bars, self.loc[experiment,::-1,'Details'].reset_index(drop=True),
                                  user_bar_colors_dict)
        
        if PRE_flag and (calccol in fspar.param_settings.index[3:]):
            self.theo_pre_plot(axs[i], experiment, y_lims[1]*0.1,
                              bartype='v',
                              pre_color=pre_color,
                              pre_lw=pre_lw,
                              tag_color=tag_color,
                              tag_ls=tag_ls,
                              tag_lw=tag_lw)
    
    
    def plot_res_evo(self, calccol, fig, axs, i, row_number,
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
                     fit_perform=False,
                     fit_line_color = 'black',
                     fit_line_width = 1,
                     fit_line_style = '-',
                     
                     titration_x_values=None):
        
        
        # Draws subplot title
        subtitle = self.ix[0,i,'Res#'] + self.ix[0,i,'1-letter']
        axs[i].set_title(subtitle, y=subtitle_pad, fontsize=subtitle_fs, fontname=subtitle_fn, fontweight=subtitle_weight)
        
        
        # PREPARING DATA
        y = np.array(self.loc[:,row_number,calccol].fillna(value=0))
        
        # if the user wants to represent the condition in the x axis
        # for the first dimension
        if set_x_values and (self.tittype == 'cond1' or self.dim_comparison == 'cond1'):
            if len(titration_x_values) != len(self.items):
                raise ValueError('> The titration_x_values variable length in farseer_user_variables.py does not match the number of data points for cond1')
            x = np.array(titration_x_values)
            xmax = titration_x_values[-1]
            
        
        # for 2D and 3D analysis this option is not available
        elif (self.tittype in ['cond2', 'cond3']) or (self.dim_comparison in ['cond2', 'cond3']):
            x = np.arange(0, len(y))
            xmax = len(y)-1
            axs[i].set_xticks(x)
            xlabels = self.items
            x_ticks_rot=45
        
        # just give a range for the x axis
        # in case representing the cond1 without titration_x_values
        else:
            x = np.arange(0, len(y))
            axs[i].set_xticks(x)
            xmax = len(y)-1
            xlabels = x
        
        # Configure Axis Ticks
        axs[i].set_xlim(0, xmax)
        axs[i].set_ylim(y_lims[0], y_lims[1])
        
        if set_x_values and (self.tittype == 'cond1' or self.dim_comparison == 'cond1'):
            axs[i].locator_params(axis='x', tight=True, nbins=x_ticks_nbins)
            xlabels = [int(n) for n in axs[i].get_xticks()]
        
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        axs[i].spines['left'].set_zorder(10)
        axs[i].spines['right'].set_zorder(10)
        
        axs[i].set_xticklabels(xlabels,
                               fontname=x_ticks_fn,
                               fontsize=x_ticks_fs,
                               fontweight=x_ticks_weight,
                               rotation=x_ticks_rot)
        
        axs[i].locator_params(axis='y', tight=True, nbins=y_ticks_nbins)
        axs[i].set_yticklabels(['{:.2f}'.format(yy) for yy in axs[i].get_yticks()],
                               fontname=y_ticks_fn,
                               fontsize=y_ticks_fs,
                               fontweight=y_ticks_weight,
                               rotation=y_ticks_rot)
                               
        axs[i].xaxis.tick_bottom()
        axs[i].yaxis.tick_left()
        axs[i].tick_params(axis='x',
                           pad=x_ticks_pad,
                           length=x_ticks_len,
                           direction='out')
        axs[i].tick_params(axis='y',
                           pad=y_ticks_pad,
                           length=y_ticks_len,
                           direction='out')
        
        ## Configure axes labels
        axs[i].set_xlabel(x_label,
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          fontname=x_label_fn,
                          weight=x_label_weight)
        
        ## Configure YY ticks/label
        axs[i].set_ylabel(y_label,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight)
        
        # writes unassigned in the center of the plot for unassigned peaks
        # and plots nothing
        if self.ix[0,row_number,'Peak Status'] == 'unassigned':
            axs[i].text((x[0] + x[-1]) / 2, (y_lims[0]+y_lims[1])/2, 'unassigned', fontsize=8, fontname='Arial', va='center', ha='center')
            return
        
        # do not represent the lost peaks.
        mes_mask = np.array(self.loc[:,row_number,'Peak Status'] != 'lost')
        y = y[mes_mask]
        x = x[mes_mask]
        
        
        
        # Plots data
        axs[i].plot(x, y, ls=line_style,
                          color=line_color,
                          marker=marker_style,
                          mfc=marker_color,
                          markersize=marker_size,
                          lw=line_width,
                          zorder=5)
        
        
        
        if fill_between:
            axs[i].fill_between(x, 0, y, facecolor=fill_color, alpha=fill_alpha)
        
        if fit_perform \
                and self.tittype == 'cond1'\
                and (calccol in fspar.param_settings.index[:3])\
                and self.fitdf[calccol].ix[i, 'fit'] == 'OK':
            
            # plot fit
            axs[i].plot(self.xfit, self.fitdf[calccol].ix[i, 'yfit'],
                        fit_line_style, lw=fit_line_width, color=fit_line_color, zorder=6)
            
            # plot fit param grid lines
            fit_kwargs={'yline':{'ls':'-', 'lw':0.2,'color':'grey', 'zorder':1},
                        'kd':{'ls':'-', 'lw':0.2,'color':'grey','zorder':1}
                       }
            
            if self.fitdf[calccol].ix[i, 'kd'] > \
                (titration_x_values[-1]):
                    fit_kwargs['yline']['ls'] = 'dotted'
            
                
            ## ymax horizontal line
            axs[i].plot((0, self.fitdf[calccol].ix[i, 'kd']),
                        (self.fitdf[calccol].ix[i, 'ymax'], self.fitdf[calccol].ix[i, 'ymax']),
                         **fit_kwargs['yline'])
            ## ymax horizontal line
            axs[i].plot((0, self.fitdf[calccol].ix[i, 'kd']),
                        (self.fitdf[calccol].ix[i, 'yhalf'],self.fitdf[calccol].ix[i, 'yhalf']),
                         **fit_kwargs['yline'])
            ## kd vertical line
            axs[i].plot((self.fitdf[calccol].ix[i, 'kd'], self.fitdf[calccol].ix[i, 'kd']),
                        (0, self.fitdf[calccol].ix[i, 'ymax']),
                         **fit_kwargs['kd'])
                         
            
            # plot fit param numbers
            txtkwargs = {'fontsize':4}
            #yhalfc = ( titration_x_values[-1]*0.02, self.fitdf[calccol].ix[i, 'yhalf']+y_lims[1]*0.02)
            n_hillc = ( titration_x_values[-1], y_lims[1]+y_lims[1]*0.015)
            r_sq = ( titration_x_values[0], y_lims[1]+y_lims[1]*0.015)
            
            # kd value label
            if  titration_x_values[-1]/2 < self.fitdf[calccol].ix[i, 'kd'] <  titration_x_values[-1]:
                kdc = (self.fitdf[calccol].ix[i, 'kd']- titration_x_values[-1]*0.02, y_lims[1]*0.02, int(round(self.fitdf[calccol].ix[i, 'kd'])))
            elif self.fitdf[calccol].ix[i, 'kd'] >  titration_x_values[-1]:
                kdc = ( titration_x_values[-1]- titration_x_values[-1]*0.02,y_lims[1]*0.02, 'kd {}'.format(int(round(self.fitdf[calccol].ix[i, 'kd']))))
            else:
                kdc = (self.fitdf[calccol].ix[i, 'kd']+ titration_x_values[-1]*0.11, y_lims[1]*0.02, int(round(self.fitdf[calccol].ix[i, 'kd'])))
            
            # ymax value label
            if self.fitdf[calccol].ix[i, 'ymax'] > y_lims[1]:
                # places value label right bellow ylim[1]
                ymaxc = (titration_x_values[-1]*0.02, y_lims[1]-y_lims[1]*0.08, 'ymax {:.3f}'.format(self.fitdf[calccol].ix[i, 'ymax']))
            elif y_lims[1]*0.8 < self.fitdf[calccol].ix[i, 'ymax'] < y_lims[1]:
                # places value label at the position but bellow the line
                ymaxc = (titration_x_values[-1]*0.02, self.fitdf[calccol].ix[i, 'ymax']-y_lims[1]*0.08, '{:.3f}'.format(self.fitdf[calccol].ix[i, 'ymax']))
            elif self.fitdf[calccol].ix[i, 'ymax'] < y_lims[0]:
                # places value label right above ylim[0]
                ymaxc = (titration_x_values[-1]*0.02, y_lims[0]+y_lims[1]*0.08, 'ymax {:.3f}'.format(self.fitdf[calccol].ix[i, 'ymax']))
            else:
                # places value label where it is
                ymaxc = (titration_x_values[-1]*0.02,self.fitdf[calccol].ix[i, 'ymax']+y_lims[1]*0.02, '{:.3f}'.format(self.fitdf[calccol].ix[i, 'ymax']))
                
            
            axs[i].text(n_hillc[0], n_hillc[1],
                        'n = {:.3f}'.format(self.fitdf[calccol].ix[i, 'n_hill']),
                        ha='right', **txtkwargs)
            axs[i].text(r_sq[0], r_sq[1],
                        'r**2 = {:.3f}'.format(self.fitdf[calccol].ix[i, 'r_sq']),
                        ha='left', **txtkwargs)
            axs[i].text(*ymaxc,
                        **txtkwargs)
            axs[i].text(*kdc, ha='right', **txtkwargs)
    
    
    def plot_cs_scatter(self, fig, axs, i, row_number,
                     
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
                     mk_color='none',
                     mk_edgecolors='black',
                     mk_lost_color='red'):
        """
        Represents the peak evolution in chemical shift change along the titration.
        """
        def set_tick_labels():
            # adjust the ticks to a maximum of 4.
            # http://stackoverflow.com/questions/6682784/how-to-reduce-number-of-ticks-with-matplotlib
            axs[i].locator_params(axis='both', tight=True, nbins=4)
            
            axs[i].set_xticklabels(axs[i].get_xticks(),
                               fontname=x_ticks_fn,
                               fontsize=x_ticks_fs,
                               fontweight=x_ticks_weight,
                               rotation=x_ticks_rot)
        
            axs[i].set_yticklabels(axs[i].get_yticks(),
                               fontname=y_ticks_fn,
                               fontsize=y_ticks_fs,
                               fontweight=y_ticks_weight,
                               rotation=y_ticks_rot)
        
        # Configure subtitle
        subtitle = self.ix[0,i,'Res#'] + self.ix[0,i,'1-letter']
        axs[i].set_title(subtitle, y=subtitle_pad, fontsize=subtitle_fs, fontname=subtitle_fn, fontweight=subtitle_weight)
        
        # Configure Axis Ticks
        axs[i].xaxis.tick_bottom()
        axs[i].tick_params(axis='x',
                           pad=x_ticks_pad,
                           length=x_ticks_len,
                           direction='out')
        axs[i].yaxis.tick_left()
        axs[i].tick_params(axis='y',
                           pad=y_ticks_pad,
                           length=y_ticks_len,
                           direction='out')
        
        ## Configure axes labels
        axs[i].set_xlabel(x_label,
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          fontname=x_label_fn,
                          weight=x_label_weight)
        
        ## Configure YY ticks/label
        axs[i].set_ylabel(y_label,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight)
        
        # check assignment
        # if residue is unassigned, identifies in the subplot
        if self.ix[0,row_number,'Peak Status'] == 'unassigned':
            axs[i].text(0, 0, 'unassigned', fontsize=7, fontname='Arial', va='center', ha='center')
            axs[i].set_xlim(-1,1)
            axs[i].set_ylim(-1,1)
            set_tick_labels()
            return
        elif not(self.ix[:,i,'H1_delta'].any()) and not(self.ix[:,i,'N15_delta'].any()):
            axs[i].text(0, 0, 'all data lost', fontsize=7, fontname='Arial', va='center', ha='center')
            axs[i].set_xlim(-1,1)
            axs[i].set_ylim(-1,1)
            set_tick_labels()
            return
        
        # Plots data
        if mk_type == 'shape':
            # represents the points in different shapes
            mcycle = it.cycle(markers)
            
            for j in self.items:
                if self.ix[j,i,'Peak Status'] == 'lost':
                    axs[i].scatter(self.ix[j,i,'H1_delta'], self.ix[j,i,'N15_delta'],
                               marker=next(mcycle),
                               s=mksize, color=mk_color, edgecolors=mk_edge_lost)
                
                else:
                    axs[i].scatter(self.ix[j,i,'H1_delta'], self.ix[j,i,'N15_delta'],
                               marker=next(mcycle), s=mksize, color=mk_color,
                               edgecolors=mk_edgecolors)
        
        elif mk_type == 'color':
            # represents the points as circles with a gradient of color
            mk_color = fsut.linear_gradient(mk_start_color, finish_hex=mk_end_color,
                                            n=self.shape[0])
            # this is used instead of passing a list to .scatter because
            # of colouring in red the lost peaks.
            mccycle = it.cycle(mk_color['hex'])
            
            for j in self.items:
                if self.ix[j,i,'Peak Status'] == 'lost':
                    axs[i].scatter(self.ix[j,i,'H1_delta'], self.ix[j,i,'N15_delta'],
                               marker='o',
                               s=mksize, c=mk_lost_color, edgecolors='none')
                else:
                    axs[i].scatter(self.ix[j,i,'H1_delta'], self.ix[j,i,'N15_delta'],
                               marker='o', s=mksize, c=next(mccycle),
                               edgecolors='none')
        
        
        xlimmin = -scale*2 if self.ix[:,i,'H1_delta'].fillna(value=0).min() > -scale else self.ix[:,i,'H1_delta'].fillna(value=0).min()*1.5
        xlimmax = scale*2 if self.ix[:,i,'H1_delta'].fillna(value=0).max() < scale else self.ix[:,i,'H1_delta'].fillna(value=0).max()*1.5
        
        ylimmin = -scale*2 if self.ix[:,i,'N15_delta'].fillna(value=0).min() > -scale else self.ix[:,i,'N15_delta'].fillna(value=0).min()*1.5
        ylimmax = scale*2 if self.ix[:,i,'N15_delta'].fillna(value=0).max() < scale else self.ix[:,i,'N15_delta'].fillna(value=0).max()*1.5
        
        axs[i].set_xlim(xlimmin, xlimmax)
        axs[i].set_ylim(ylimmin, ylimmax)
        
        set_tick_labels()
        
        # draws axis 0 dotted line
        axs[i].hlines(0,-100,100, colors='black', linestyles='dotted', linewidth=0.25)
        axs[i].vlines(0,-100,100, colors='black', linestyles='dotted', linewidth=0.25)
    
        # draws center scale
        axs[i].hlines(0,-scale,scale, colors='darkblue', linestyles='-', linewidth=1)
        axs[i].vlines(0,-scale,scale, colors='darkblue', linestyles='-', linewidth=1)
        
    
    def plot_DPRE_heatmap(self, calccol, fig, axs, i, experiment,
                          y_lims=(0,1),
                          vmin=0,
                          vmax=1,
                          ylabel='DELTA PRE',
                          x_ticks_fs=6,
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
                          top_margin=0.1,
                          cbar_font_size=4,
                          tag_color='red',
                          tag_lw=0.3,
                          tag_ls='-'):
        
        Dcmap = np.array((self.loc[experiment,:,calccol].fillna(0),
                         self.loc[experiment,:,calccol].fillna(0)))
        cleg = axs[i].pcolor(Dcmap, cmap='binary', vmin=vmin, vmax=vmax)
        
        axs[i].tick_params(axis='y', left='off')
        axs[i].tick_params(axis='x', bottom='off')
        # http://stackoverflow.com/questions/2176424/hiding-axis-text-in-matplotlib-plots
        axs[i].get_yaxis().set_ticks([])
        axs[i].get_xaxis().set_visible(False)
        
        axs[i].set_ylabel(experiment,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight)
        
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        
        self.theo_pre_plot(axs[i], experiment, 2,
                           bartype = 'hm',
                           tag_color=tag_color,
                           tag_ls=tag_ls,
                           tag_lw=tag_lw)
        
        
        if i == len(self.items)-1:
            cbar = plt.colorbar(cleg, ticks=[vmin, vmax/4, vmax/4*2, vmax/4*3, vmax], orientation='vertical',
                                cax = fig.add_axes([right_margin+right_margin*0.05, 
                                                    bottom_margin, 
                                                    right_margin*0.05, 
                                                    top_margin-bottom_margin]))
            cbar.ax.tick_params(labelsize=cbar_font_size)
            axs[i].get_xaxis().set_visible(True)
            axs[i].tick_params(axis='x', bottom='on')
            initialresidue = int(self.ix[0, 0, 'Res#'])
            finalresidue = int(self.loc[experiment,:,'Res#'].tail(1))
            first_tick = ceil(initialresidue/10)*10
            axs[i].set_xticks(np.arange(first_tick-0.5, finalresidue+1, 10))
            axs[i].set_xticklabels(np.arange(first_tick, finalresidue, 10),
                               fontsize=x_ticks_fs,
                               rotation=x_ticks_rot,
                               fontname=x_ticks_fn,
                               fontweight=x_ticks_weight)
            axs[i].tick_params(axis='x', which='major', pad=x_ticks_pad)
            fig.subplots_adjust(right=right_margin,
                                bottom=bottom_margin,
                                top=top_margin,
                                hspace=0)
            
        pass
    
    def plot_delta_osci(self, calccol, fig, axs, i ,experiment,
                        y_lims=(0,1),
                        ylabel='DPRE',
                        
                        subtitle_fn= 'Arial',
                        subtitle_fs= 8,
                        subtitle_pad= 0.99,
                        subtitle_weight= 'normal',
                        x_label_fn= 'Arial',
                        x_label_fs= 8,
                        x_label_pad= 2,
                        x_label_weight= 'bold',
                        x_label_rot=0,
                        y_label_fn= 'Arial',
                        y_label_fs= 8,
                        y_label_pad=3,
                        y_label_weight= 'bold',
                        y_label_rot=90,
                        x_ticks_fn='Arial',
                        x_ticks_fs=5,
                        x_ticks_weight = 'normal',
                        x_ticks_pad=2,
                        x_ticks_len=2,
                        x_ticks_rot=0,
                        y_ticks_fn='Arial',
                        y_ticks_fs=7,
                        y_ticks_rot=0,
                        y_ticks_pad=1,
                        y_ticks_weight= 'normal',
                        y_ticks_len=2,
                        y_ticks_nbins=8,
                        y_grid_flag=True,
                        y_grid_color='lightgrey',
                        y_grid_linestyle='-',
                        y_grid_linewidth=0.2,
                        y_grid_alpha=1,
                        PRE_flag=None,
                        pre_color='red',
                        pre_lw=1,
                        tag_color='blue',
                        tag_lw=0.5,
                        tag_ls=':',
                        
                        dpre_ms=2,
                        dpre_alpha=0.5,
                        smooth_lw=1,
                        color=None,
                        ref_color='black',
                        color_init='#ff00ff',
                        color_end='#0000ff',
                        grid_color='grey',
                        shade = False,
                        shade_regions = [(23,37),(0,0),(0,0)],
                        res_highlight=True,
                        res_hl_list=[25,32,54,64,66,47],
                        res_highlight_fs=4,
                        res_highlight_y=0.9):
        """
        Plots the Delta_PRE data in scatter points and the gaussian
        smoothed curved, comparing the data point with the reference.
        """
        
        # to solve .find Attribute Error
        # http://stackoverflow.com/questions/29437305/how-to-fix-attributeerror-series-object-has-no-attribute-find
        # plots dpre for first point in comparison
        #pmaskr = self.ix[0,:,calccol] > 0
        axs[i].plot(self.ix[0,:,'Res#'].astype(float),
                    self.ix[0,:,calccol].astype(float),
                    'o',
                    markersize=dpre_ms,
                    markeredgewidth=0.0,
                    c=ref_color,
                    alpha=dpre_alpha,
                    zorder=10)
        
        # plots dpre for titration data point
        #pmaskd = self.loc[experiment,:,calccol] > 0
        axs[i].plot(self.loc[experiment,:,'Res#'].astype(float),
                    self.loc[experiment,:,calccol].astype(float),
                    'o',
                    c=color,
                    markersize=dpre_ms,
                    markeredgewidth=0.0,
                    alpha=dpre_alpha,
                    zorder=10)
        
        
        # plots dpre_smooth for first data point in comparison
        #pmaskr = self.ix[0,:,calccol+'_smooth'] > 0
        axs[i].plot(self.ix[0,:,'Res#'].astype(float),
                    self.ix[0,:,calccol+'_smooth'].astype(float),
                    ls='-',
                    lw=smooth_lw,
                    c=ref_color,
                    zorder=10)
        
        # plots dpre_smooth for data point
        #pmaskd = self.loc[experiment,:,calccol+'_smooth'] > 0
        axs[i].plot(self.loc[experiment,:,'Res#'].astype(float),
                    self.loc[experiment,:,calccol+'_smooth'].astype(float),
                    ls='-',
                    lw=smooth_lw,
                    c=color,
                    zorder=10)
        
        # Configure subplot title
        axs[i].set_title(experiment, y=subtitle_pad, fontsize=subtitle_fs, fontname=subtitle_fn, fontweight=subtitle_weight)
        
        # Set Ticks
        initialresidue = int(self.ix[0, 0, 'Res#'])
        finalresidue = int(self.loc[experiment,:,'Res#'].tail(1))
        first_tick = ceil(initialresidue/10)*10
        axs[i].set_xticks(np.arange(first_tick, finalresidue+1, 10))
        # https://github.com/matplotlib/matplotlib/issues/6266
        axs[i].set_xticklabels(np.arange(first_tick, finalresidue, 10),
                               fontname=x_ticks_fn,
                               fontsize=x_ticks_fs,
                               fontweight=x_ticks_weight,
                               rotation=x_ticks_rot)
        
        
        # Set subplot titles
        axs[i].set_title(experiment, y=subtitle_pad, fontsize=subtitle_fs, fontname=subtitle_fn, weight=subtitle_weight)
        
        # configures spines
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        
        
        # Configures YY ticks
        axs[i].set_ylim(y_lims[0], y_lims[1])
        axs[i].locator_params(axis='y', tight=True, nbins=y_ticks_nbins)
        axs[i].set_yticklabels(['{:.2f}'.format(yy) for yy in axs[i].get_yticks()],
                               fontname=y_ticks_fn,
                               fontsize=y_ticks_fs,
                               fontweight=y_ticks_weight,
                               rotation=y_ticks_rot)
        
        # configures tick params
        axs[i].margins(x=0.01)
        axs[i].tick_params(axis='x',
                           pad=x_ticks_pad,
                           length=x_ticks_len,
                           direction='out')
                           
        axs[i].tick_params(axis='y',
                           pad=y_ticks_pad,
                           length=y_ticks_len,
                           direction='out')
        
        # Set axes labels
        axs[i].set_xlabel('Residue',
                          fontname=x_label_fn,
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          weight=x_label_weight,
                          rotation=x_label_rot)
        
        axs[i].set_ylabel(ylabel,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight,
                          rotation=y_label_rot)
        
        # Adds grid
        if y_grid_flag:
            axs[i].yaxis.grid(color=y_grid_color,
                              linestyle=y_grid_linestyle,
                              linewidth=y_grid_linewidth,
                              alpha=y_grid_alpha,
                              zorder=0)
        
        if shade:
            for lmargin, rmargin in shade_regions:
                axs[i].fill([lmargin,rmargin,
                             rmargin, lmargin],
                            [0,0,2,2], grid_color, alpha=0.2)
        if res_highlight:
            for rr in res_hl_list:
                axs[i].axvline(x=rr,ls=':', lw=0.3,  color=grid_color)
                rrmask = self.ix[0,:,'Res#'] == str(rr)
                l1 = list(self.loc[experiment,rrmask,'1-letter'])
                axs[i].text(rr, y_lims[1]*res_highlight_y,
                            l1[0],
                            ha='center', va='center', fontsize=res_highlight_fs)
        
        self.theo_pre_plot(axs[i], experiment, y_lims[1]*0.1,
                           bartype = 'osci',
                           tag_color=tag_color,
                           tag_ls=tag_ls,
                           tag_lw=tag_lw)
        
    
    def plot_base(self, calccol, plot_type, plot_style, param_dict,
                     par_ylims=(0,1),
                     ylabel='ppm or ratio',
                     hspace=0.5,
                     rows_per_page=5,
                     cols_per_page=1,
                     fig_height=11.69,
                     fig_width=8.69,
                     
                     fig_file_type='pdf',
                     fig_dpi=300):
        
        #calccol = fspar.param_settings.loc[idx,'calc_column_name']
        
        if plot_type == 'exp':
            num_subplots = len(self.items)
        elif plot_type == 'res':
            num_subplots = len(self.major_axis)
        elif plot_type == 'single':
            num_subplots = 1
        else:
            raise ValueError('Not a valid Farseer plot type')
        
        numrows = ceil(num_subplots/cols_per_page)
        real_fig_height = (fig_height / rows_per_page) * numrows
        
        
        # http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
        fig, axs = plt.subplots(nrows=numrows, ncols=cols_per_page,
                                figsize=(fig_width, real_fig_height))
        
        axs = axs.ravel()
        plt.tight_layout(rect=[0.01,0.01,0.995,0.995], h_pad=fig_height/rows_per_page)
        # Plots yy axis title
        # http://www.futurile.net/2016/03/01/text-handling-in-matplotlib/
        
        if plot_style in ['bar_extended', 'bar_compacted']:
            
            for i, experiment in enumerate(self):
                self.plot_bar_horizontal(plot_style, calccol, fig, axs, i, experiment, y_lims=par_ylims, ylabel=ylabel, **param_dict)
                fig.subplots_adjust(hspace=hspace)
                
        elif plot_style == 'bar_vertical':
        
            for i, experiment in enumerate(self):
                self.plot_bar_vertical(calccol, fig, axs, i, experiment, y_lims=par_ylims, ylabel=ylabel, **param_dict)
        
        elif plot_style == 'res_evo':
            
            for i, row_number in enumerate(self.major_axis):
                self.plot_res_evo(calccol, fig, axs, i, row_number, y_lims=par_ylims, y_label=ylabel, **param_dict)
        
        elif plot_style == 'cs_scatter':
            
            for i, row_number in enumerate(self.major_axis):
                self.plot_cs_scatter(fig, axs, i, row_number, **param_dict)
        
        elif plot_style == 'heat_map':
            for i, experiment in enumerate(self):
                self.plot_DPRE_heatmap(calccol, fig, axs, i, experiment, y_lims=par_ylims, ylabel=ylabel, **param_dict)
            
        elif plot_style == 'delta_osci':
            
            dp_colors = fsut.linear_gradient(param_dict['color_init'],
                                            param_dict['color_end'],
                                            n=self.shape[0])
            
            print(param_dict.keys())
            
            dp_color = it.cycle(dp_colors['hex'])
            
            for i, experiment in enumerate(self):
                self.plot_delta_osci(calccol, fig, axs, i, experiment,
                                     y_lims=par_ylims,
                                     ylabel=ylabel,
                                     color=next(dp_color),
                                     **param_dict)
            
        
        
        
        self.write_plot(fig, plot_style, calccol, fig_file_type, fig_dpi)
        plt.close('all')
    
    def write_plot(self, fig, plot_name, calccol, fig_file_type, fig_dpi):
        
        
        if not(os.path.exists('{}/{}'.format(self.tables_and_plots_folder, calccol))):
            os.makedirs('{}/{}'.format(self.tables_and_plots_folder, calccol))
        
        file_path = '{0}/{1}/{1}_{2}.{3}'.format(self.tables_and_plots_folder,
                                                 calccol, plot_name, fig_file_type)
        
        fig.savefig(file_path, dpi=fig_dpi)
        
        fsut.write_log('*** Plot saved {}\n'.format(file_path))#('/'.join(file_path.split('/')[-2:])))
    
    def perform_fit(self, calccol='CSP', x_values=None):
        """
        Controls the general fitting workflow.
        :calccol: the parameter column to perform the fit
        :x_values: the titration variable values
        """
        #def fitting_quadratic(L0, P0, kd, ymax):
            #"""
            #Fits hyperbolic Michaelis-Menten
            #"""
            #return ymax * (((kd + L0 + P0)-np.sqrt((kd + L0 + P0)**2 - (4*P0*L0)))/2*P0)
        
        def fitting_hill(L0, Vmax, n, K):
            return (Vmax*L0**n)/(K**n+L0**n)
        
        #def add_fit_results(a, b, c, d, e, f):
        # ['fit', 'ymax', 'yhalf','kd', 'n_hill', 'yfit']
        def add_fit_results(param_list, name_list):
            dfres = pd.DataFrame(data=[param_list],
                                     index=[row_number],
                                     columns=name_list)
            self.fitdf[calccol] = self.fitdf[calccol].append(dfres)
        
        
        def calc_r_squared(x, y , f, popt):
            """
            Calculates R**2
            http://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit
            
            returns [r_squared, ss_res, ss_tot]
            """
            residuals = y.sub(f(x, *popt))
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((y-np.mean(y))**2)
            r_squared = 1 - (ss_res / ss_tot)
            
            return [r_squared, ss_res, ss_tot]
        
        def write_fit_failed(x, y, row_number, logf):
            str2write=\
"""
Res#:  {}
xdata: {}
ydata: {}
!¡FIT FAILED TO FIND MINIMIZATION!¡
**************************
""".format(self.ix[0, row_number,'Res#']+self.ix[0, row_number,'1-letter'], list(x), list(y))
            fsut.write_log(str2write, logfile_name=logf)
            add_fit_results(['Failed'] + [np.NaN]*6,
                            ['fit', 'ymax', 'yhalf','kd', 'n_hill', 'r_sq', 'yfit'])
            
        
        
        # sets an x linear space
        self.xfit=np.linspace(0, 10000, 100000+1)
        
        # creates data frame to store fiting results.
        self.fitdf[calccol] = pd.DataFrame()
        
        # open fit logs
        if not(os.path.exists('{}/{}'.format(self.tables_and_plots_folder, calccol))):
            os.makedirs('{}/{}'.format(self.tables_and_plots_folder, calccol))
        logf = '{0}/{1}/{1}_fit_report.log'.format(self.tables_and_plots_folder, calccol)
        s2w = \
"""# fitting for parameter: '{}'
fit performed: Hill Equation
(Vmax*[S]**n)/(K0.5**n+[S]**n)
""".format(calccol)
        fsut.write_log(s2w, logfile_name=logf, mod='w')

        # for each assigned residue
        for row_number in (self.major_axis[self.ix[0,:, 'Peak Status'] != 'unassigned']):
            
            # gets only the measured datapoints and discards the 'lost'
            lostmask = np.array(self.loc[:,row_number,'Peak Status'] == 'measured')
            # .fillna is user to avoid error:
            # minpack.error: Result from function call is not a proper array of floats.
            y = self.loc[lostmask,row_number,calccol].fillna(value=0.0)
            x = pd.Series(x_values)[lostmask]
            x.index = y.index
            resnum = self.ix[0, row_number,'Res#']
            ###
            
            # makes no sense to perform a fitting in only 2 or less datapoints
            if len(x) <= 2: 
                str2write=\
"""
Res#:  {}
xdata: {}
ydata: {}
!¡NOT ENOUGH DATA POINTS - FIT NOT PERFORMED!¡
**************************
""".format(self.ix[0, row_number,'Res#']+self.ix[0, row_number,'1-letter'], x, y)
                fsut.write_log(str2write, logfile_name=logf)
                add_fit_results(['No Data',np.nan, np.nan, np.nan, np.nan, np.nan, False],
                                ['fit', 'ymax', 'yhalf','kd', 'n_hill', 'r_sq', 'yfit'])
                continue
            ###
            
            # starts Hill fit algorythm
            # http://www.physiologyweb.com/calculators/hill_equation_interactive_graph.html
            
            try:
                p_guess = [np.max(y), 1, np.median(x)]
                
                #raise ValueError('9999')
                popt, pcov = sciopt.curve_fit(fitting_hill, x, y, p0=p_guess)
                
                yfit = fitting_hill(self.xfit, *popt)
                
                rsq = calc_r_squared(x, y, fitting_hill, popt)
                r_squared = rsq[0]
                
                ymax = popt[0]
                n_hill = popt[1]
                kd = popt[2]
                yhalf = ymax/2
                
                add_fit_results(\
                    ['OK', ymax, yhalf, kd, n_hill, r_squared, yfit],
                    ['fit', 'ymax', 'yhalf','kd', 'n_hill', 'r_sq', 'yfit'])
                
                s2w=\
"""
Res#:  {}
xdata: {}
ydata: {}
ymax: {}
yhalf: {}
K0.5: {}
n: {}
r**2: {}
popt: {}
pcov: {}
rsq: {}
**************************
""".format(self.ix[0, row_number,'Res#']+self.ix[0, row_number,'1-letter'], list(x), list(y), ymax, yhalf, kd, n_hill, r_squared, popt, pcov, rsq)
                fsut.write_log(s2w, logfile_name=logf)
            
            except:
            #    pass
                write_fit_failed(x, y, row_number, logf)
        
        
        self.fitdf[calccol] = pd.concat([self.res_info.iloc[0,:,:], self.fitdf[calccol]], axis=1)
        self.fitdf[calccol].iloc[:,0:9].to_csv('{0}/{1}/{1}_fit_data.csv'.format(self.tables_and_plots_folder, calccol), index=False, float_format='%.3f')
        fsut.write_log('*** File Saved {}\n'.format('{0}/{1}/{1}_fit_data.csv'.format(self.tables_and_plots_folder, calccol)))
        #raise ValueError('9999')
    
    def write_Chimera_attributes(self, calccol, resformat=':',
                                 colformat='{:.5f}'):
        """
        
        :param resformat: the formating options for the 'Res#' column. This must
        match the residue selection command in Chimera. See:
        www.cgl.ucsf.edu/chimera/docs/UsersGuide/midas/frameatom_spec.html
        this is defined in the Chimera_ATT_Res_format variable in
        farseer_user_variables.
        
        :param listpar: a list with the names of the columns that are 
        to be written to chimera.
        
        Writes one Chimera Attribute file to each calculated parameter
        and for each titration point. Generated files are stored in the folder
        'ChimeraAttributeFiles'.
        
        This function was written this way because it
        is easier to generate all the files at one than to make several calls
        for each desired column.
        """
        
        resform = lambda x: "\t{}{}\t".format(resformat, x)
        colform = lambda x: colformat.format(x)
        
        formatting = {'Res#': resform}
        
        ####
        
        
        for item in self.items:
            mask_lost = self.loc[item,:,'Peak Status'] == 'lost'
            mask_unassigned = self.loc[item,:,'Peak Status'] == 'unassigned'
            mask_measured = self.loc[item,:,'Peak Status'] == 'measured'
            
            #for column in listpar:
            file_path = '{}/{}'.format(self.chimera_att_folder, calccol)
            if not(os.path.exists(file_path)):
                os.makedirs(file_path)
            
            file_name = '{}/{}_{}.att'.format(file_path, item, calccol)
            fileout = open(file_name, 'w')
                
                
            attheader = """#
#
# lost peaks {}
#
# unassigned peaks {}
#
attribute: {}
match mode: 1-to-1
recipient: residues
\t""".format(resformat + self.loc[item,mask_lost,'Res#'].to_string(header=False, index=False).replace(' ', '').replace('\n', ','),
             resformat + self.loc[item,mask_unassigned,'Res#'].to_string(header=False, index=False).replace(' ', '').replace('\n', ','),
             calccol.lower())
             
            fileout.write(attheader)
                
            formatting[calccol] = colform
                
            #print(self.loc[item,mask_measured,['Res#',column]])
                
            to_write = self.loc[item,mask_measured,['Res#',calccol]].to_string(header=False, index=False,
                                formatters=formatting, col_space=0).replace(' ', '')
                
                
            fileout.write(to_write)
                
            fileout.close()
            fsut.write_log('*** File saved {}\n'.format(file_name))#('/'.join(file_path.split('/')[-2:]))) #
                


