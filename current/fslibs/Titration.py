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
    Is a panel where each item is an experiment, and the progression along Items
    is the evolution of the titration.
    """
    
    cs_lost = fsuv.cs_lost
    calc_parameters_list = 0
    calc_folder = 'Calculations'
    comparison_folder = 'Comparisons'
    tables_and_plots_folder = 'TablesAndPlots'
    chimera_att_folder = 'ChimeraAttributeFiles'
    export_tit_folder = 'FullPeaklists'
    fitdf = {}
    #predf = {}
    
    csp_alpha4res = {key:fsuv.csp_alpha4res for key in 'ARNDCEQGHILKMFPSTWYV'}
    for k, v in fsuv.csp_res_exceptions.items():
        csp_alpha4res[k] = v
    
    
    def create_titration_attributes(self, tittype='titvar',
                                          owndim_pts=['foo'],
                                          dim1_pts='bar',
                                          dim2_pts='zoo',
                                          dim_comparison='not applied',
                                          resonance_type='Backbone'):
        #for item in 
        self.tittype = tittype
        self.att_dict = owndim_pts
        self.dim1_pts = dim1_pts
        self.dim2_pts = dim2_pts
        self.dim_comparison = dim_comparison
        self.resonance_type = resonance_type
        self.res_info = self.loc[:,:,['Res#','1-letter','3-letter','Peak Status']]
        
        
        if tittype.startswith('titvar'):
            self.calc_path = '{}/{}/{}/{}/{}'.format(self.resonance_type,
                                                     self.calc_folder,
                                                     self.tittype,
                                                     self.dim2_pts,
                                                     self.dim1_pts)
        elif tittype.startswith('C'):
            self.calc_path = '{}/{}/{}/{}/{}/{}'.format(self.resonance_type,
                                                        self.comparison_folder,
                                                        self.tittype,
                                                        self.dim_comparison,
                                                        self.dim2_pts,
                                                        self.dim1_pts)
        
        if not(os.path.exists(self.calc_path)):
            os.makedirs(self.calc_path)
        
        self.chimera_att_folder = '{}/{}'.format(self.calc_path, self.chimera_att_folder)
        if not(os.path.exists(self.chimera_att_folder)):
            os.makedirs(self.chimera_att_folder)
        
        
        self.tables_and_plots_folder = '{}/{}'.format(self.calc_path, self.tables_and_plots_folder)
        if not(os.path.exists(self.tables_and_plots_folder)):
            os.makedirs(self.tables_and_plots_folder)
        
        self.export_tit_folder = '{}/{}'.format(self.calc_path, self.export_tit_folder)
        if not(os.path.exists(self.export_tit_folder)):
            os.makedirs(self.export_tit_folder)
        
    @property
    def _constructor(self):
        return Titration
    #@property
    #def _constructor_sliced(self):
        #return SpectrumData
        
    
    def calc_cs_diffs(self, calccol, sourcecol):
        '''
        Calculates the difference between two columns along a Titration 
        using as reference the column from the reference experiment, 
        which is always stored in Item=0.
        
        Calculation result is stored in a new column of each DataFrame.
        '''
        self.loc[:,:,calccol] = self.loc[:,:,sourcecol].sub(self.ix[0,:,sourcecol], axis='index')
        
        if self.cs_lost == 'full':
            for item in self.items:
                mask_lost = self.loc[item,:,'Peak Status'] == 'lost'
                self.loc[item,mask_lost,calccol] = 1.
        
        elif self.cs_lost == 'prev':
            for iitem in range(1, len(self.items)):
                mask_lost = self.ix[iitem,:,'Peak Status'] == 'lost'
                self.ix[iitem,mask_lost,calccol] = self.ix[iitem-1,mask_lost,calccol]
        
        fsut.write_log('*** Calculated {}\n'.format(calccol))
    
    def calc_ratio(self, calccol, sourcecol):
        '''
        Calculates the ration between two columns along a Titration
        using as reference the column from the reference experiment, 
        which is always stored in Item=0.
        
        Calculation result is stored in a new column of each DataFrame.
        '''
        self.loc[:,:,calccol] = self.loc[:,:,sourcecol].div(self.ix[0,:,sourcecol], axis='index')
        fsut.write_log('*** Calculated {}\n'.format(calccol))
    
    def load_theoretical_PRE(self, spectra_path, dimpt):
        """
        Loads theoretical PRE values to represent in bar plots.
        """
        
        #print(spectra_path)
        target_folder = '{}/para/{}/'.format(spectra_path.strip('/'), dimpt)
        pre_file = glob.glob('{}*.pre'.format(target_folder))
        #print(pre_file)
        
        if len(pre_file) > 1:
            raise ValueError('@@@ There are more than one .pre file in the folder {}'.format(target_folder))
        elif len(pre_file) < 1:
            raise ValueError('@@@ There is no .pre file in folder {}'.format(target_folder))
        
        #print(pre_paths)
        self.predf = pd.read_csv(pre_file[0], sep='\s+', usecols=[1], names=['Theo PRE'])
        self.loc[:,:,'Theo PRE'] = 1
        self.loc['para',:,'Theo PRE'] = self.predf.loc[:,'Theo PRE']
        
        #print(self)
        #input()
        #self.predf = pd.concat([self.res_info.iloc[0,:,:], self.predf], axis=1)
        
        #print(self.predf['M1'])
        
    def calc_Delta_PRE(self, sourcecol, targetcol):
        
        self.loc[:,:,targetcol] = self.loc[:,:,'Theo PRE'].sub(self.loc[:,:,sourcecol])#, axis='index')
    
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
        return np.sqrt(0.5 * (s[1] ** 2 + (self.csp_alpha4res[s[0]] * s[2] ** 2)))
    
    def calc_csp(self, calccol='CSP',
                       pos1='PosF1_delta',
                       pos2='PosF2_delta'):
        """
        Calculates the Chemical Shift Perturbation (CSP) values based on a formula.
        """
        
        self.loc[:,:,calccol] = self.loc[:,:,['1-letter',pos1,pos2]].apply(lambda x: self.csp_willi(x), axis=2)
        fsut.write_log('*** Calculated {}\n'.format(calccol))
    

    
    def write_table(self, tablecol):
        '''
        Writes the values of a specific column along the titration to a tsv table.
        '''
        
        # concatenates the values of the table with the residues numbers
        table = pd.concat([self.res_info.iloc[0,:,[0]], self.loc[:,:,tablecol].astype(float)], axis=1)
        
        if not(os.path.exists('{}/{}'.format(self.tables_and_plots_folder, tablecol))):
            os.makedirs('{}/{}'.format(self.tables_and_plots_folder, tablecol))
        
        file_path = '{0}/{1}/{1}.tsv'.format(self.tables_and_plots_folder,
                                                 tablecol)
        
        fileout = open(file_path, 'w')
        
        
        if self.tittype.startswith('titvar'):
            header = \
"""# Table for '{0}' resonances.
# A titration results for variable '{1}'
# ranging datapoints '{2}', where:
# conditions '{3}' and '{4}' are kept constants.
# {5} data.
""".format(self.resonance_type, self.tittype, list(self.att_dict), self.dim2_pts, self.dim1_pts, tablecol)
        elif self.tittype.startswith('C'):
            header = \
"""# Table for '{0}' resonances.
# The comparison '{1}' of the results obtained for titrations 'titvar{7}'
# across variable '{2}' which ranges datapoints '{3}', where:
# conditions '{4}' and '{5}' are kept constants.
# {6} data.
""".format(self.resonance_type, self.tittype, self.dim_comparison, list(self.att_dict), self.dim2_pts, self.dim1_pts, tablecol, self.tittype[-1])
        
        fileout.write(header)
        fileout.write(table.to_csv(sep='\t', index=False, na_rep='NaN', float_format='%.4f'))
        fileout.close()
        fsut.write_log('*** File saved {}\n'.format(file_path))#('/'.join(file_path.split('/')[-2:])))
    
    def export_titration(self):
        """
        Exports the titration experiments (measured and calculated data) to .tsv
        files. These files are stored in the folder 'full_peaklists'.
        """
        for item in self.items:
            file_path = '{}/{}.tsv'.format(self.export_tit_folder, item)
            fileout = open(file_path, 'w')
            fileout.write(self.loc[item].to_csv(sep='\t', index=False, na_rep='NaN', float_format='%.4f'))
            fileout.close()
            fsut.write_log('*** File saved {}\n'.format(file_path))#('/'.join(file_path.split('/')[-2:])))
    
    
    def set_item_colors(self, peak_status_series, apply_bool, colors_dict):
        """
        Defines a list with the sequence of colors that will be attributed to a
        specific item in the plots.
        
        Usually, defines the bar colors or the XTicksLabels colors.
        
        """
        
        if apply_bool:
            item_colors = [colors_dict[stts] for stts in peak_status_series]
        else:
            item_colors = [bar_main_color] * peak_status_series.size

        return item_colors
    
    def text_marker(self, ax, axbar, condition_series, cond_str, cond_mark, yy_scale, fs=4, orientation='horizontal'):
        """
        Marks Text over the bars of the plot.
        
        :param: ax, the subplot object where text will be drawn
        :param: axbar, the bars object. Contains the bars of the plot
        :param: condition_series, a pd.Series containing the conditions to be
                evaluated.
        :param: cond_str, the condition to be met by condition_series.
        :param: cond_mark, the string to be drawn in the plot
        :param: yy_scale, the vertical scale adjustment to draw text under
                negative bars.
        :param optional: fs, fontsize of the drawn mark.
        :param: orientation: to diferentiate between horizontal or vertical bar plots.
        """
        
        # bool Series considering condition
        is_condition = condition_series == cond_str
        
        if orientation == 'horizontal':
            
            # adjust the position of the mark according to the sign of the bar
            vpos_sign = lambda x, y, z: x if y >= 0 else (x*-1)-(yy_scale/20)
            
            # future help: http://composition.al/blog/2015/11/29/a-better-way-to-add-labels-to-bar-charts-with-matplotlib/
            for isC, bar in zip(is_condition, axbar):
                if isC:
                    x0, y0 = bar.xy
                    vpos = vpos_sign(bar.get_height(), y0, yy_scale)
                    hpos = bar.get_x() + bar.get_width() / 2.5
                    ax.text(hpos, vpos, cond_mark, ha='center', va='bottom', fontsize=fs)
        
        elif orientation == 'vertical':
            
            # adjust the position of the mark according to the sign of the bar
            hpos_sign = lambda x, y, z: x+(yy_scale/20) if y >= 0 else (x*-1)-(yy_scale/20)
            
            # future help: http://composition.al/blog/2015/11/29/a-better-way-to-add-labels-to-bar-charts-with-matplotlib/
            for isC, bar in zip(is_condition, axbar):
                if isC:
                    x0, y0 = bar.xy
                    hpos = hpos_sign(bar.get_width(), x0, yy_scale)
                    vpos = bar.get_y() - bar.get_height() / 2.5
                    ax.text(hpos, vpos, cond_mark, ha='center', va='bottom', fontsize=fs)

    def plot_bar_extended(self, calccol, fig, axs, i, experiment,
    
                          apply_status_2_bar_color=True,
                          color_measured='k',
                          color_lost='red',
                          color_unassigned='grey',
                          bar_width=0.7,
                          bar_alpha=1,
                          bar_linewidth=0,
                          title_y=1.05,
                          title_fs=8,
                          title_fn='Arial',
                          plot_threshold=True,
                          plot_threshold_color='red',
                          plot_threshold_lw=1,
                          x_label_fs=8, 
                          x_label_pad=2,
                          x_label_fn='Arial',
                          x_label_weight='bold',
                          x_ticks_rot=90,
                          x_ticks_fs=6,
                          x_ticks_fn='monospace',
                          x_ticks_pad=2,
                          y_lims=(0,1),
                          ylabel='ppm or ratio',
                          y_label_fs=8, 
                          y_label_pad=2,
                          y_label_fn='Arial',
                          y_label_weight='bold',
                          y_ticks_fs=9,
                          y_ticks_pad=-3,
                          y_ticks_len=2,
                          y_ticks_fn='Arial',
                          y_grid_color='lightgrey',
                          mark_prolines=True,
                          proline_mark='P',
                          mark_user_details=True,
                          mark_fs=3,
                          theo_pre=False,
                          pre_color='red',
                          pre_lw=1):
        """
        :param: idx, calculated parameter, that is index to param_settings
        """
        
        # creates a list with the colors to be represented in bars and
        # Xticks. Colors are attributed according to the Peak Status.
        
        colors_dict = {'measured':color_measured,
                       'lost':color_lost,
                       'unassigned':color_unassigned}
        
        item_colors = self.set_item_colors(self.loc[experiment,:,'Peak Status'],
                                           apply_status_2_bar_color,
                                           colors_dict)
        
        axs[i].set_title(experiment, y=title_y, fontsize=title_fs, fontname=title_fn)
        
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        
        if self.resonance_type == 'Backbone':
            # fillna(0) is added because nan conflicts with text_maker()
            # in bat.get_height() which return nan
            ax = axs[i].bar(self.loc[experiment,:,'Res#'].astype(float),
                            self.loc[experiment,:,calccol].fillna(0),
                            color=item_colors,
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
                                   rotation=x_ticks_rot,
                                   fontsize=x_ticks_fs,
                                   fontname=x_ticks_fn)
            axs[i].set_xlim([float(self.loc[experiment,:,'Res#'].head(1)) - 1.2,
                             float(self.loc[experiment,:,'Res#'].tail(1)) + 1.2])
        
        elif self.resonance_type == 'Sidechains':
            ax = axs[i].bar(self.major_axis,
                            self.loc[experiment,:,calccol].fillna(0),
                            color=item_colors,
                            width=bar_width,
                            align='center',
                            alpha=bar_alpha,
                            linewidth=bar_linewidth,
                            zorder=4)
        
            # Configure XX ticks and Label
            axs[i].set_xticks(self.major_axis)
        
            ## https://github.com/matplotlib/matplotlib/issues/6266
            axs[i].set_xticklabels(self.loc[experiment,:,['Res#','1-letter', 'ATOM']].apply(lambda x: ''.join(x), axis=1),
                                   rotation=x_ticks_rot,
                                   fontsize=x_ticks_fs,
                                   fontname=x_ticks_fn)
        
                
        for xtick, color in zip(axs[i].get_xticklabels(), item_colors):
            xtick.set_color(color)
        
        axs[i].set_xlabel('Residue',
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          fontname=x_label_fn,
                          weight=x_label_weight)
        
        
        
        axs[i].xaxis.tick_bottom()
        axs[i].xaxis.set_tick_params(direction='out', length=2, pad=x_ticks_pad)
        ##.xlabel('Residue', fontsize=xx_label_font_size, fontweight=xx_label_font_effect, fontname='Arial')
        
        # Adds red line to identify significant changes.
        if plot_threshold and calccol in fspar.param_settings.index[:3]:
            
            sorted_cs = \
                self.loc[experiment,:, calccol].abs().sort_values().dropna()
            firstdecile = sorted_cs[0:ceil(0.1*len(sorted_cs))]
            threshold = firstdecile.mean() + 5*firstdecile.std()
            axs[i].axhline(y=threshold, color=plot_threshold_color, 
                           linewidth=plot_threshold_lw, zorder=0)
            axs[i].axhline(y=-threshold, color=plot_threshold_color, 
                           linewidth=plot_threshold_lw, zorder=0)
        
        # Configure YY ticks and Label
        axs[i].set_ylabel(ylabel,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight)
        
        axs[i].yaxis.grid(color=y_grid_color,zorder=0)
        axs[i].yaxis.set_tick_params(length=y_ticks_len, labelsize=y_ticks_fs, pad=y_ticks_pad, direction='out')
        
        axs[i].set_ylim(y_lims[0], y_lims[1])
        
        
        if mark_prolines:
            self.text_marker(axs[i],
                             ax,
                             self.loc[experiment,:,'1-letter'],
                             'P',
                             proline_mark,
                             y_lims[1],
                             fs=mark_fs)
        
        if mark_user_details:
            #k, what you find in the playlist Details column
            #v, which characater you want to draw
            for k, v in fsuv.user_marks_dict.items():
                self.text_marker(axs[i], ax,
                                 self.loc[experiment,:,'Details'],
                                 k,
                                 v, 
                                 y_lims[1],
                                 fs=mark_fs)
        
        if theo_pre and self.resonance_type == 'Backbone'\
            and ((self.tittype == 'titvar3' and experiment == 'para')\
            or self.tittype == 'C3'):
            # do
            axs[i].plot(self.loc[experiment,:,'Theo PRE'], zorder=10, color=pre_color, lw=pre_lw)
    
    def plot_bar_vertical(self, calccol, fig, axs, i, experiment,
    
                          apply_status_2_bar_color=True,
                          color_measured='k',
                          color_lost='red',
                          color_unassigned='grey',
                          
                          bar_height=0.7,
                          bar_alpha=1,
                          bar_linewidth=0,
                          
                          title_y=1.05,
                          title_fs=8,
                          title_fn='Arial',
                          
                          plot_threshold=True,
                          plot_threshold_color='red',
                          plot_threshold_lw=1,
                          
                          x_label_fs=6, 
                          x_label_pad=2,
                          x_label_fn='Arial',
                          x_label_weight='bold',
                          
                          x_lims=(0,1),
                          x_ticks_len=2,
                          x_ticks_fs=6,
                          x_ticks_fn='Arial',
                          x_ticks_pad=2,
                          x_grid_color='lightgrey',
                          
                          ylabel='ratio or ppm',
                          y_label_fs=6, 
                          y_label_pad=8,
                          y_label_fn='Arial',
                          y_label_weight='bold',
                          y_label_rot=-90,
                          
                          y_ticks_fs=7,
                          y_ticks_fn='monospace',
                          y_ticks_pad=-3,
                          y_ticks_rot=90,
                          
                          
                          mark_prolines=True,
                          proline_mark='P',
                          mark_user_details=True,
                          mark_fs=3):
        """
        :param: idx, calculated parameter, that is index to param_settings
        """
        #someone suggests that parameters are better defined per subplot
        # http://stackoverflow.com/questions/12946521/matplotlib-subplots-with-same-settings
        
        # creates a list with the colors to be represented in bars and
        # Xticks. Colors are attributed according to the Peak Status.
        colors_dict = {'measured':color_measured,
                       'lost':color_lost,
                       'unassigned':color_unassigned}
        
        item_colors = self.set_item_colors(self.loc[experiment,:,'Peak Status'],
                                           apply_status_2_bar_color,
                                           colors_dict)
        
        axs[i].set_title(experiment, y=title_y, fontsize=title_fs, fontname=title_fn)
        
        axs[i].spines['left'].set_zorder(10)
        axs[i].spines['right'].set_zorder(10)
        
        
        # fillna(0) is added because nan conflicts with text_maker() .iloc[::-1]
        # in bat.get_height() which return nan
        ax = axs[i].barh(self.loc[experiment,:,'Res#'].astype(float),
                         self.loc[experiment,:,calccol].fillna(0),
                         color=item_colors,
                         height=bar_height,
                         align='center',
                         alpha=bar_alpha,
                         linewidth=bar_linewidth,
                         zorder=4)
        
        # Adds red line to identify significant changes.
        if calccol == 'CSP' and plot_threshold:
            sorted_csp = self.loc[experiment,:, calccol].sort_values().dropna()
            firstdecile = sorted_csp[0:int(0.1*len(sorted_csp))]
            threshold = firstdecile.mean() + 5*firstdecile.std()
            axs[i].axvline(x=threshold, color='red', linewidth=1, zorder=0)
        
        # Configure YY ticks and Label
        
        axs[i].set_ylabel('Residue',
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight,
                          rotation=y_label_rot)
        
        axs[i].set_yticks(np.arange(float(self.loc[experiment,:,'Res#'].head(1)),
                                    float(self.loc[experiment,:,'Res#'].tail(1))+1,
                                    1))
        
        
        # https://github.com/matplotlib/matplotlib/issues/6266
        axs[i].set_yticklabels(self.loc[experiment,:,['Res#','1-letter']].apply(lambda x: ''.join(x), axis=1),
                               rotation=y_ticks_rot,
                               fontsize=y_ticks_fs,
                               fontname=y_ticks_fn)
                               
        for ytick, color in zip(axs[i].get_yticklabels(), item_colors):
            ytick.set_color(color)
        
        axs[i].set_ylim([float(self.loc[experiment,:,'Res#'].head(1)) - 1.2,
                         float(self.loc[experiment,:,'Res#'].tail(1)) + 1.2])
                         
        axs[i].yaxis.tick_left()
        axs[i].yaxis.set_tick_params(direction='out', length=2, pad=y_ticks_pad)
        #.xlabel('Residue', fontsize=xx_label_font_size, fontweight=xx_label_font_effect, fontname='Arial')
        
        # Configure XX ticks and Label
        
        axs[i].set_xlabel(ylabel,
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          fontname=x_label_fn,
                          weight=x_label_weight)
        
        
        axs[i].xaxis.grid(color=x_grid_color, zorder=0)
        axs[i].xaxis.set_tick_params(length=x_ticks_len, labelsize=x_ticks_fs, pad=x_ticks_pad, direction='out')
        
        axs[i].set_xlim(x_lims[0], x_lims[1])
        
        if mark_prolines:
            self.text_marker(axs[i],
                             ax,
                             self.loc[experiment,:,'1-letter'],
                             'P',
                             proline_mark,
                             x_lims[1],
                             fs=mark_fs,
                             orientation='vertical')
        
        if mark_user_details:
            #k, what you find in the playlist Details column
            #v, which characater you want to draw
            for k, v in fsuv.user_marks_dict.items():
                self.text_marker(axs[i], ax,
                                 self.loc[experiment,:,'Details'],
                                 k,
                                 v, 
                                 x_lims[1],
                                 fs=mark_fs,
                                 orientation='vertical')
        
    
    def plot_bar_compacted(self, calccol, fig, axs, i, experiment,
    
                          apply_status_2_bar_color=True,
                          color_measured='k',
                          color_lost='red',
                          color_unassigned='grey',
                          bar_width=0.7,
                          bar_alpha=1,
                          bar_linewidth=0,
                          title_y=1.01,
                          title_fs=8,
                          title_fn='Arial',
                          plot_threshold=True,
                          plot_threshold_color='red',
                          plot_threshold_lw=1,
                          x_label_fs=8, 
                          x_label_pad=2,
                          x_label_fn='Arial',
                          x_label_weight='bold',
                          x_ticks_rot=0,
                          x_ticks_fs=6,
                          x_ticks_fn='Arial',
                          x_ticks_pad=1,
                          y_lims=(0,1),
                          ylabel='ratio or ppms',
                          y_label_fs=8,
                          y_label_pad=2,
                          y_label_fn='Arial',
                          y_label_weight='bold',
                          y_ticks_fs=9,
                          y_ticks_pad=-3,
                          y_ticks_len=2,
                          y_grid_color='lightgrey',
                          mark_prolines=True,
                          proline_mark='P',
                          mark_user_details=True,
                          mark_fs=3,
                          unassigned_shade=True,
                          unassigned_shade_color='grey',
                          unassigned_shade_alpha=0.5,
                          theo_pre=False,
                          pre_color='red',
                          pre_lw=1):
        """
        :param: idx, calculated parameter, that is index to param_settings
        """
        # creates a list with the colors to be represented in bars and
        # Xticks. Colors are attributed according to the Peak Status.
        colors_dict = {'measured':color_measured,
                       'lost':color_lost,
                       'unassigned':color_unassigned}
        
        item_colors = self.set_item_colors(self.loc[experiment,:,'Peak Status'],
                                           apply_status_2_bar_color,
                                           colors_dict)
        
        axs[i].set_title(experiment, y=title_y, fontsize=title_fs, fontname=title_fn)
        
        axs[i].spines['bottom'].set_zorder(10)
        axs[i].spines['top'].set_zorder(10)
        
        
        
        # fillna(0) is added because nan conflicts with text_maker()
        # in bat.get_height() which return nan
        ax = axs[i].bar(self.loc[experiment,:,'Res#'].astype(float),
                        self.loc[experiment,:,calccol].fillna(0),
                   color=item_colors,
                   width=bar_width,
                   align='center',
                   alpha=bar_alpha,
                   linewidth=bar_linewidth,
                   zorder=4)
        
        # Adds red line to identify significant changes.
        if calccol == 'CSP' and plot_threshold:
            sorted_csp = self.loc[experiment,:, calccol].sort_values().dropna()
            firstdecile = sorted_csp[0:int(0.1*len(sorted_csp))]
            threshold = firstdecile.mean() + 5*firstdecile.std()
            axs[i].axhline(y=threshold, color=plot_threshold_color, linewidth=plot_threshold_lw, zorder=0)
        
        
        
        # Configure XX ticks and Label
        axs[i].set_xlabel('Residue',
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          fontname=x_label_fn,
                          weight=x_label_weight)
        
        
        initialresidue = int(self.ix[0, 0, 'Res#'])
        
        #print(initialresidue)
        finalresidue = int(self.loc[experiment,:,'Res#'].tail(1))
        first_tick = ceil(initialresidue/10)*10
        
        #print(np.arange(10, self.loc[experiment].shape[0], 10))
        axs[i].set_xticks(np.arange(first_tick, finalresidue+1, 10))
        
        
        # https://github.com/matplotlib/matplotlib/issues/6266
        #print(np.arange(initialresidue, finalresidue, 10))
        axs[i].set_xticklabels(np.arange(first_tick, finalresidue, 10),
                               fontsize=x_ticks_fs,
                               rotation=x_ticks_rot,
                               fontname=x_ticks_fn)
                               
        
        
        
        axs[i].set_xlim(initialresidue - 1.2, finalresidue + 1.2)
        
        axs[i].xaxis.tick_bottom()
        axs[i].xaxis.set_tick_params(direction='out', length=2, which='major', pad=x_ticks_pad)
        #axs[i].tick_params(axis='x', )
        #.xlabel('Residue', fontsize=xx_label_font_size, fontweight=xx_label_font_effect, fontname='Arial')
        
        # Configure YY ticks and Label
        
        axs[i].set_ylabel(ylabel,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight)
        
        axs[i].yaxis.grid(color=y_grid_color,zorder=0)
        axs[i].yaxis.set_tick_params(length=y_ticks_len, labelsize=y_ticks_fs, pad=y_ticks_pad, direction='out')
        
        axs[i].set_ylim(y_lims[0], y_lims[1])
        
        
        # unassigned shade
        # sets a grey shade over unassigned residues
        if unassigned_shade:
            unassignedmask = self.loc[experiment, :, 'Peak Status'] == 'unassigned'

            for residue in self.loc[experiment, unassignedmask, 'Res#']:
                residue = int(residue) - 0.5
                axs[i].axvspan(residue, residue+1, color=unassigned_shade_color, alpha=unassigned_shade_alpha, lw=0)
        
        
        
        if mark_prolines:
            self.text_marker(axs[i],
                             ax,
                             self.loc[experiment,:,'1-letter'],
                             'P',
                             proline_mark,
                             y_lims[1],
                             fs=mark_fs)
        
        if mark_user_details:
            #k, what you find in the playlist Details column
            #v, which characater you want to draw
            for k, v in fsuv.user_marks_dict.items():
                self.text_marker(axs[i], ax,
                                 self.loc[experiment,:,'Details'],
                                 k,
                                 v, 
                                 y_lims[1],
                                 fs=mark_fs)
        
        if theo_pre and ((self.tittype == 'titvar3' and experiment == 'para') or self.tittype == 'C3'):
            axs[i].plot(self.loc[experiment,:,'Theo PRE'], zorder=10, color=pre_color, lw=pre_lw)
    
    def plot_res_evo(self, calccol, fig, axs, i, row_number,
                     
                     title_y=0.97,
                     title_fs=8,
                     title_fn='Arial',
                     x_label='[Ligand]',
                     set_x_values=False,
                     tit_x_values=range(10),
                     x_label_fs=6, 
                     x_label_pad=2,
                     x_label_fn='Arial',
                     x_label_weight='normal',
                     x_ticks_pad=1,
                     x_ticks_fs=7,
                     y_lims=(0,1),
                     ylabel='ratio or ppm',
                     y_label_fs=8,
                     y_label_pad=2,
                     y_label_fn='Arial',
                     y_label_weight='normal',
                     y_ticks_pad=1,
                     y_ticks_fs=7,
                     line_style='-',
                     plot_color='r',
                     marker_style='o',
                     marker_color='darkred',
                     marker_size=3,
                     line_width=1,
                     fill_between=True,
                     fill_color='pink',
                     fill_alpha=0.5,
                     fit_perform=False,
                     fit_line_color='black',
                     fit_line_width=1):
        
        title = self.ix[0,i,'Res#'] + self.ix[0,i,'1-letter']
        axs[i].set_title(title, y=title_y, fontsize=title_fs, fontname=title_fn)
        
        y = np.array(self.loc[:,row_number,calccol].fillna(value=0))
        
        # if the user wants to represent the condition in the x axis
        # for the first dimension
        if set_x_values and (self.tittype == 'titvar1' or self.dim_comparison == 'titvar1'):
            x = np.array(tit_x_values)
            axs[i].set_xlim(0, tit_x_values[-1])
            #fit?
        
        # for 2D and 3D analysis this option is not available
        elif (self.tittype in ['titvar2', 'titvar3']) or (self.dim_comparison in ['titvar2', 'titvar3']):
            x = np.arange(0, len(y))
            axs[i].xaxis.set_ticks(x)
            axs[i].set_xticklabels(self.items, rotation=45)
        
        # just give a range for the x axis
        else:
            x = np.arange(0, len(y))
            axs[i].set_xlim(0, len(y)-1)
        
        #
        ## Configure XX ticks/label
        axs[i].set_xlabel(x_label,
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          fontname=x_label_fn,
                          weight=x_label_weight)
        
        
        axs[i].xaxis.tick_bottom()
        axs[i].xaxis.set_tick_params(direction='out', length=2, pad=x_ticks_pad, labelsize=x_ticks_fs)
        
        ## Configure YY ticks/label
        axs[i].set_ylabel(ylabel,
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight)
        
        axs[i].set_ylim(y_lims[0], y_lims[1])
        
        axs[i].yaxis.tick_left()
        axs[i].yaxis.set_tick_params(direction='out', length=2, pad=y_ticks_pad, labelsize=y_ticks_fs)
        
        # writes unassigned in the center of the plot for unassigned peaks
        if self.ix[0,row_number,'Peak Status'] == 'unassigned':
            ycenter = (y_lims[0]+y_lims[1])/2
            axs[i].text(x[-1]/2, ycenter, 'unassigned', fontsize=8, fontname='Arial', va='center', ha='center')
            return
        
        
        # do not represent the lost peaks.
        mes_mask = np.array(self.loc[:,row_number,'Peak Status'] != 'lost')
        
        if (len(mes_mask) != len(x)) or (len(mes_mask) != len(y)):
            raise ValueError('> The fitting_x_values variable length in farseer_user_variables.py does not match the number of data points in titvar1')
        
        y = y[mes_mask]
        x = x[mes_mask]
        
        axs[i].plot(x, y, ls=line_style,
                          color=plot_color,
                          marker=marker_style,
                          mfc=marker_color,
                          markersize=marker_size,
                          lw=line_width,
                          zorder=5)
        
        if fill_between:
            axs[i].fill_between(x, 0, y, facecolor=fill_color, alpha=fill_alpha)
        
        if fit_perform and self.tittype == 'titvar1'\
                and (calccol in fspar.param_settings.index[:3])\
                and self.fitdf[calccol].ix[i, 'fit'] == 'OK':
            
            # plot fit
            axs[i].plot(self.xfit, self.fitdf[calccol].ix[i, 'yfit'], '-', lw=1, c='black', zorder=6)
            
            # plot fit param grid lines
            fit_kwargs={'yline':{'ls':'-', 'lw':0.2,'color':'grey', 'zorder':1},
                        'kd':{'ls':'-', 'lw':0.2,'color':'grey','zorder':1}
                       }
            
            if self.fitdf[calccol].ix[i, 'kd'] > \
                (tit_x_values[-1]):
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
            #yhalfc = (tit_x_values[-1]*0.02, self.fitdf[calccol].ix[i, 'yhalf']+y_lims[1]*0.02)
            n_hillc = (tit_x_values[-1], y_lims[1]+y_lims[1]*0.015)
            
            # kd value label
            if tit_x_values[-1]/2 < self.fitdf[calccol].ix[i, 'kd'] < tit_x_values[-1]:
                kdc = (self.fitdf[calccol].ix[i, 'kd']-tit_x_values[-1]*0.02, y_lims[1]*0.02, int(round(self.fitdf[calccol].ix[i, 'kd'])))
            elif self.fitdf[calccol].ix[i, 'kd'] > tit_x_values[-1]:
                kdc = (tit_x_values[-1]-tit_x_values[-1]*0.02,y_lims[1]*0.02, 'kd {}'.format(int(round(self.fitdf[calccol].ix[i, 'kd']))))
            else:
                kdc = (self.fitdf[calccol].ix[i, 'kd']+tit_x_values[-1]*0.11, y_lims[1]*0.02, int(round(self.fitdf[calccol].ix[i, 'kd'])))
            
            # ymax value label
            if self.fitdf[calccol].ix[i, 'ymax'] > y_lims[1]:
                # places value label right bellow ylim[1]
                ymaxc = (tit_x_values[-1]*0.02, y_lims[1]-y_lims[1]*0.08, 'ymax {:.3f}'.format(self.fitdf[calccol].ix[i, 'ymax']))
            elif y_lims[1]*0.8 < self.fitdf[calccol].ix[i, 'ymax'] < y_lims[1]:
                # places value label at the position but bellow the line
                ymaxc = (tit_x_values[-1]*0.02, self.fitdf[calccol].ix[i, 'ymax']-y_lims[1]*0.08, '{:.3f}'.format(self.fitdf[calccol].ix[i, 'ymax']))
            elif self.fitdf[calccol].ix[i, 'ymax'] < y_lims[0]:
                # places value label right above ylim[0]
                ymaxc = (tit_x_values[-1]*0.02, y_lims[0]+y_lims[1]*0.08, 'ymax {:.3f}'.format(self.fitdf[calccol].ix[i, 'ymax']))
            else:
                # places value label where it is
                ymaxc = (tit_x_values[-1]*0.02,self.fitdf[calccol].ix[i, 'ymax']+y_lims[1]*0.02, '{:.3f}'.format(self.fitdf[calccol].ix[i, 'ymax']))
                
            
            
            #axs[i].text(yhalfc[0], yhalfc[1],
            #            '{:.3f}'.format(self.fitdf[calccol].ix[i, 'yhalf']),
            #            **txtkwargs)
            axs[i].text(n_hillc[0], n_hillc[1],
                        'n = {:.3f}'.format(self.fitdf[calccol].ix[i, 'n_hill']),
                        ha='right', **txtkwargs)
            axs[i].text(*ymaxc,
                        **txtkwargs)
            axs[i].text(*kdc, ha='right', **txtkwargs)
    
    
    
    def plot_cs_scatter(self, fig, axs, i, row_number,
                     
                     title_y=0.97,
                     title_fs=8,
                     title_fn='Arial',
                     
                     
                     x_label_fs=6,
                     x_label_pad=2,
                     x_label_fn='Arial',
                     x_label_weight='normal',
                     x_ticks_pad=1,
                     x_ticks_fs=7,
                     y_label_fs=6,
                     y_label_pad=2,
                     y_label_fn='Arial',
                     y_label_weight='normal',
                     y_ticks_pad=1,
                     y_ticks_fs=7,
                     
                     mksize=30,
                     scale=0.01,
                     mk_type='color',
                     mk_start_color='#FFFFFF',
                     mk_end_color='#d0d0d0',
                     mk_lost_color='red',
                     markers=['^','>','v','<','s','p','h','8','*','D'],
                     mk_color='none',
                     mk_edgecolors='black',
                     mk_edge_lost='red'):
        """
        Represents the peak evolution in chemical shift change along the titration.
        """
        
        # Set the title over each subplot
        title = self.ix[0,i,'Res#'] + self.ix[0,i,'1-letter']
        axs[i].set_title(title, y=title_y, fontsize=title_fs, fontname=title_fn)
        
        ## Configure XX ticks/label
        axs[i].set_xlabel('1H (ppm)',
                          fontsize=x_label_fs,
                          labelpad=x_label_pad,
                          fontname=x_label_fn,
                          weight=x_label_weight)
        
        
        axs[i].xaxis.tick_bottom()
        axs[i].xaxis.set_tick_params(direction='out', length=2, pad=x_ticks_pad, labelsize=x_ticks_fs)
        
        ## Configure YY ticks/label
        axs[i].set_ylabel('15N (ppm)',
                          fontsize=y_label_fs,
                          labelpad=y_label_pad,
                          fontname=y_label_fn,
                          weight=y_label_weight)
        
        axs[i].yaxis.tick_left()
        axs[i].yaxis.set_tick_params(direction='out', length=2, pad=y_ticks_pad, labelsize=y_ticks_fs)
        
        # check assignment
        # if residue is unassigned, identifies in the subplot
        if self.ix[0,row_number,'Peak Status'] == 'unassigned':
            axs[i].text(0, 0, 'unassigned', fontsize=7, fontname='Arial', va='center', ha='center')
            axs[i].set_xlim(-1,1)
            axs[i].set_ylim(-1,1)
            return
        elif not(self.ix[:,i,'H1_delta'].any()) and not(self.ix[:,i,'N15_delta'].any()):
            axs[i].text(0, 0, 'all data lost', fontsize=7, fontname='Arial', va='center', ha='center')
            axs[i].set_xlim(-1,1)
            axs[i].set_ylim(-1,1)
            return
        
        # draws axis 0 dotted line
        axs[i].hlines(0,-100,100, colors='black', linestyles='dotted', linewidth=0.25)
        axs[i].vlines(0,-100,100, colors='black', linestyles='dotted', linewidth=0.25)
    
        # draws center scale
        axs[i].hlines(0,-scale,scale, colors='darkblue', linestyles='-', linewidth=1)
        axs[i].vlines(0,-scale,scale, colors='darkblue', linestyles='-', linewidth=1)
        
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
        
        # adjust the ticks to a maximum of 4.
        # http://stackoverflow.com/questions/6682784/how-to-reduce-number-of-ticks-with-matplotlib
        axs[i].locator_params(axis='both', tight=True, nbins=4)
    
    def plot_base(self, calccol, plot_type, plot_style, param_dict,
                     par_ylims=(0,1),
                     ylabel='ppm or ratio',
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
        
        # Plots yy axis title
        # http://www.futurile.net/2016/03/01/text-handling-in-matplotlib/
        
        
        if plot_style == 'bar_extended':
            
            for i, experiment in enumerate(self):
                self.plot_bar_extended(calccol, fig, axs, i, experiment, y_lims=par_ylims, ylabel=ylabel, **param_dict)
        
        elif plot_style == 'bar_compacted':
            
            for i, experiment in enumerate(self):
                self.plot_bar_compacted(calccol, fig, axs, i, experiment, y_lims=par_ylims, ylabel=ylabel, **param_dict)
        
        elif plot_style == 'bar_vertical':
        
            for i, experiment in enumerate(self):
                self.plot_bar_vertical(calccol, fig, axs, i, experiment, x_lims=par_ylims, ylabel=ylabel, **param_dict)
        
        elif plot_style == 'res_evo':
            
            for i, row_number in enumerate(self.major_axis):
                self.plot_res_evo(calccol, fig, axs, i, row_number, y_lims=par_ylims, ylabel=ylabel, **param_dict)
        
        elif plot_style == 'cs_scatter':
            
            for i, row_number in enumerate(self.major_axis):
                self.plot_cs_scatter(fig, axs, i, row_number, **param_dict)
        
        elif plot_style == 'hit_map':
            pass
        
        plt.tight_layout(rect=[0.01,0.01,0.995,0.995], h_pad=fig_height/rows_per_page)
        
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
        
        def add_fit_results(a, b, c, d, e, f):
            dfres = pd.DataFrame(data=[[a, b, c, d, e, f]],
                                     index=[row_number],
                                     columns=['fit', 'ymax', 'yhalf','kd', 'n_hill', 'yfit'])
            self.fitdf[calccol] = self.fitdf[calccol].append(dfres)
        
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
            add_fit_results('Failed',np.NaN, np.NaN, np.NaN, np.NaN, np.NaN)
            
        
        
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
                add_fit_results('No Data',np.NaN, np.NaN, np.NaN, np.NaN, False)
                continue
            ###
            
            # starts Hill fit algorythm
            # http://www.physiologyweb.com/calculators/hill_equation_interactive_graph.html
            
            try:
                p_guess = [np.max(y), 1, np.median(x)]
                
                #raise ValueError('9999')
                popt, pcov = sciopt.curve_fit(fitting_hill, x, y, p0=p_guess)
                
                yfit = fitting_hill(self.xfit, *popt)
                
                ymax = popt[0]
                n_hill = popt[1]
                kd = popt[2]
                yhalf = ymax/2
                
                add_fit_results('OK', ymax, yhalf, kd, n_hill, yfit)
                
                s2w=\
"""
Res#:  {}
xdata: {}
ydata: {}
ymax: {}
yhalf: {}
K0.5: {}
n: {}
popt: {}
pcov: {}
**************************
""".format(self.ix[0, row_number,'Res#']+self.ix[0, row_number,'1-letter'], list(x), list(y), ymax, yhalf, kd, n_hill, popt, pcov)
                fsut.write_log(s2w, logfile_name=logf)
            
            except:
            #    pass
                write_fit_failed(x, y, row_number, logf)
        
        
        self.fitdf[calccol] = pd.concat([self.res_info.iloc[0,:,:], self.fitdf[calccol]], axis=1)
        self.fitdf[calccol].iloc[:,0:9].to_csv('{0}/{1}/{1}_fit_data.csv'.format(self.tables_and_plots_folder, calccol), index=False, float_format='%.3f')
        fsut.write_log('*** File Saved {}'.format('{0}/{1}/{1}_fit_data.csv'.format(self.tables_and_plots_folder, calccol)))
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
                


