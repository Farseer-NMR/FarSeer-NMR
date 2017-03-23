import glob
import os
import numpy as np
import pandas as pd
from math import ceil
#import itertools as it
import farseer_user_variables as fsuv
import farseermain as fsm
import fslibs.parameters as fspar
import fslibs.utils as fsut
from matplotlib import pyplot as plt
#from matplotlib.colors import colorConverter
#from math import ceil as mceil

class Titration(pd.Panel):
    
    cs_lost = fsuv.cs_lost
    calc_parameters_list = 0
    calc_folder = 'Calculations'
    control_folder = 'Controls'
    tables_and_plots_folder = 'TablesAndPlots'
    chimera_att_folder = 'ChimeraAttributeFiles'
    export_tit_folder = 'FullPeaklists'
    
    csp_alpha4res = {key:fsuv.csp_alpha4res for key in 'ARNDCEQGHILKMFPSTWYV'}
    for k, v in fsuv.csp_res_exceptions.items():
        csp_alpha4res[k] = v
    
    
    #esto funciona
    #def __init__(self, x, owndims, nextdims1, nextdims2, *args, **kwargs):
        #super(Titration, self).__init__(x, *args, **kwargs)
    
    def create_titration_attributes(self, tittype='D', owndims=['foo'], nextdim1='bar', nextdim2='zoo', subcontrol='D0', resonance_type='Backbone'):
        #for item in 
        self.att_dict = owndims
        self.nextdim1 = nextdim1
        self.nextdim2 = nextdim2
        self.tittype = tittype
        self.subcontrol = subcontrol
        self.resonance_type = resonance_type
        self.res_info = self.loc[:,:,['Res#','1-letter','3-letter','Peak Status']]
        
        if tittype.startswith('D'):
            self.calc_path = '{}/{}/{}/{}/{}'.format(self.resonance_type,
                                                     self.calc_folder,
                                                     self.tittype,
                                                     self.nextdim2,
                                                     self.nextdim1)
        elif tittype.startswith('C'):
            self.calc_path = '{}/{}/{}/{}/{}/{}'.format(self.resonance_type,
                                                        self.control_folder,
                                                        self.tittype,
                                                        self.subcontrol,
                                                        self.nextdim2,
                                                        self.nextdim1)
        
        if not(os.path.exists(self.calc_path)):
            os.makedirs(self.calc_path)
        
        
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
        
        dir_path = '{}/{}'.format(self.calc_path, self.tables_and_plots_folder)
        
        if not(os.path.exists(dir_path)):
            os.makedirs(dir_path)
        
        file_path = '{}/{}.tsv'.format(dir_path, tablecol)
        fileout = open(file_path, 'w')
        
        fileout.write(table.to_csv(sep='\t', index=False, na_rep='NaN', float_format='%.4f'))
        
        fileout.close()
        
        fsut.write_log('*** File saved {}\n'.format('/'.join(file_path.split('/')[-2:])))
    
    def export_titration(self):
        """
        Exports the titration experiments (measured and calculated data) to .tsv
        files. These files are stored in the folder 'full_peaklists'.
        """
        write_path = '{}/{}'.format(self.calc_path, self.export_tit_folder)
        if not(os.path.exists(write_path)):
            os.makedirs(write_path)
        
        for item in self.items:
            file_path = '{}/{}.tsv'.format(write_path, item)
            fileout = open(file_path, 'w')
            fileout.write(self.loc[item].to_csv(sep='\t', index=False, na_rep='NaN', float_format='%.4f'))
            fileout.close()
            fsut.write_log('*** File saved {}\n'.format('/'.join(file_path.split('/')[-2:])))
    
    
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
    
    def text_marker(self, ax, axbar, condition_series, signs_bool, cond_str, cond_mark, v_scale, fs=4):
        """
        Marks Text over the bars of the plot.
        
        :param: ax, the subplot object where text will be drawn
        :param: axbar, the bars object. Contains the bars of the plot
        :param: condition_series, a pd.Series containing the conditions to be
                evaluated.
        :param: signs_bool, an booleans array where True if y value is positive
                False if y value is negative.
        :param: cond_str, the condition to be met by condition_series.
        :param: cond_mark, the string to be drawn in the plot
        :param: v_scale, the vertical scale adjustment to draw text under
                negative bars.
        :param optional: fs, fontsize of the drawn mark.
        """
        is_condition = condition_series == cond_str
        
        # adjust the vertical position according to the sign of the bar
        vpos_f = lambda v, s: v * 1 if s else 0#((v * -1) - fsuv.negative_text_scaling*v_scale)
        
        # future help: http://composition.al/blog/2015/11/29/a-better-way-to-add-labels-to-bar-charts-with-matplotlib/
        for isC, bar, sign in zip(is_condition, axbar, signs_bool):
            if isC:
                vpos = vpos_f(bar.get_height(), sign)
                hpos = bar.get_x() + bar.get_width() / 2.5
                ax.text(hpos, vpos, cond_mark, ha='center', va='bottom', fontsize=fs)

    def plot_bar_extended(self, idx, calccol, fig, axs, i, experiment,
    
                          apply_status_2_bar_color=True,
                          color_measured='k',
                          color_lost='red',
                          color_unassigned='grey',
                          bar_width=0.7,
                          bar_alpha=1,
                          bar_linewidth=0,
                          
                          title_y=1.05,
                          title_fs=10,
                          title_fn='Arial',
                          
                          plot_threshold=True,
                          plot_threshold_color='red',
                          plot_threshold_lw=1,
                          
                          x_ticks_rot=90,
                          x_ticks_fs=6,
                          x_ticks_fn='monospace',
                          x_ticks_pad=0.1,
                          
                          y_ticks_fs=9,
                          y_grid_color='lightgrey',
                          
                          mark_prolines=True,
                          proline_mark='P',
                          
                          mark_user_details=True):
        """
        :param: idx, calculated parameter, that is index to param_settings
        """
        
        # creates a list with the colors to be represented in bars and
        # Xticks. Colors are attributed according to the Peak Status.
        
        colors_dict = { 'measured':color_measured,
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
        
        axs[i].set_xticks(np.arange(float(self.loc[experiment,:,'Res#'].head(1)),
                                    float(self.loc[experiment,:,'Res#'].tail(1))+1,
                                    1))
        
        
        # https://github.com/matplotlib/matplotlib/issues/6266
        axs[i].set_xticklabels(self.loc[experiment,:,['Res#','1-letter']].apply(lambda x: ''.join(x), axis=1),
                               rotation=x_ticks_rot,
                               fontsize=x_ticks_fs,
                               fontname=x_ticks_fn)
                               
        for xtick, color in zip(axs[i].get_xticklabels(), item_colors):
            xtick.set_color(color)
        
        axs[i].set_xlim([-0.2, self.loc[experiment,:,'Res#'].size + 1.2])
        axs[i].xaxis.tick_bottom()
        axs[i].xaxis.set_tick_params(direction='out', length=2, pad=x_ticks_pad)
        #.xlabel('Residue', fontsize=xx_label_font_size, fontweight=xx_label_font_effect, fontname='Arial')
        
        axs[i].yaxis.grid(color=y_grid_color,zorder=0)
        axs[i].tick_params(axis='y', labelsize=y_ticks_fs)
        
        axs[i].set_ylim(fspar.param_settings.loc[idx,'plot_yy_axis_scale'][0],
                        fspar.param_settings.loc[idx,'plot_yy_axis_scale'][1])
        axs[i].yaxis.set_tick_params(length=2)
        
        if mark_prolines:
            # in the case of prolines, is necesary to input a bool array
            # where True is met for Prolines because by default bar.get_y()
            # goes negative.
            self.text_marker(axs[i], ax, self.loc[experiment,:,'1-letter'],
                             self.loc[experiment,:,'1-letter'] == proline_mark,
                             proline_mark, proline_mark, fspar.param_settings.loc[idx,'plot_yy_axis_scale'][1])
        
        if mark_user_details:
            for k, v in fsuv.user_marks_dict.items():
                self.text_marker(axs[i], ax, self.loc[experiment,:,'Details'],
                                 self.loc[experiment,:,calccol] >= 0, k, v, 
                                 fspar.param_settings.loc[idx,'plot_yy_axis_scale'][1])
    
    #def plot_bar_vertical(self, idx,
                          #apply_status_2_bar_color=True,
                          #colors_dict={'measured':'k',
                                       #'lost':'red',
                                       #'unassigned':'gray'},
                          #barWidth=0.7,
                          
                          #plot_threshold=True,
                          #mark_prolines=True,
                          #proline_mark='P',
                          
                          #mark_user_details=True,
                          
                          
                          #figdpi=300,
                          #figtype='pdf'):
        #"""
        #:param: idx, calculated parameter, that is index to param_settings
        #"""
        
        #calccol = fspar.param_settings.loc[idx,'calc_column_name']
        
        #num_subplots = len(self.items)
        
        #fig_width = (8.27 / 3) * num_subplots
        ## http://stackoverflow.com/questions/17210646/python-subplot-within-a-loop-first-panel-appears-in-wrong-position
        #fig, axs = plt.subplots(1, num_subplots, figsize=(fig_width, 11.69))
        
        #fig.subplots_adjust(hspace = .5, wspace=.5)
        
        #axs = axs.ravel()
        
        ## http://www.futurile.net/2016/03/01/text-handling-in-matplotlib/
        #plt.figtext(0.03, 0.5, 'Residue',
                    #fontsize=10, fontweight='bold', rotation=-90, va='center')
        
        #plt.figtext(0.5, 0.03, fspar.param_settings.loc[idx,'plot_yy_axis_label'], fontsize=10, fontweight='bold', fontname='Arial', ha='center')
        
        
        #for i, experiment in enumerate(self):
            ##someone suggests that parameters are better defined per subplot
            ## http://stackoverflow.com/questions/12946521/matplotlib-subplots-with-same-settings
            
            ## creates a list with the colors to be represented in bars and
            ## Xticks. Colors are attributed according to the Peak Status.
            #item_colors = self.set_item_colors(self.loc[experiment,:,'Peak Status'],
                                         #apply_status_2_bar_color,
                                         #colors_dict)
            
            #axs[i].set_title(experiment, y=1.05, fontsize=10, fontname='Arial')
            
            #axs[i].spines['bottom'].set_zorder(10)
            #axs[i].spines['top'].set_zorder(10)
            
            
            ## fillna(0) is added because nan conflicts with text_maker()
            ## in bat.get_height() which return nan
            #ax = axs[i].barh(self.loc[experiment,:,'Res#'].astype(float),
                       #self.loc[experiment,:,calccol].fillna(0),
                       #color=item_colors,
                       #align='center',
                       #alpha=1,
                       #linewidth=0,
                       #zorder=4)
                       ##width=barWidth,
                       
                       
            ## Adds red line to identify significant changes.
            #if calccol == 'CSP' and plot_threshold:
                #sorted_csp = self.loc[experiment,:, calccol].sort_values().dropna()
                #firstdecile = sorted_csp[0:int(0.1*len(sorted_csp))]
                #threshold = firstdecile.mean() + 5*firstdecile.std()
                #axs[i].axvline(x=threshold, color='red', linewidth=1, zorder=0)
            
            #axs[i].set_yticks(np.arange(float(self.loc[experiment,:,'Res#'].head(1)),
                                        #float(self.loc[experiment,:,'Res#'].tail(1))+1,
                                        #1))
            
            
            ## https://github.com/matplotlib/matplotlib/issues/6266
            #axs[i].set_yticklabels(self.loc[experiment,:,['Res#','1-letter']].apply(lambda x: ''.join(x), axis=1),
                                   #rotation=0,
                                   #fontsize=6,
                                   #fontname='monospace')
                                   
            #for xtick, color in zip(axs[i].get_xticklabels(), item_colors):
                #xtick.set_color(color)
            
            #axs[i].set_ylim([-0.2, self.loc[experiment,:,'Res#'].size + 1.2])
            #axs[i].yaxis.tick_left()
            #axs[i].xaxis.set_tick_params(direction='out', length=2)
            ##.xlabel('Residue', fontsize=xx_label_font_size, fontweight=xx_label_font_effect, fontname='Arial')
            
            #axs[i].xaxis.grid(color='grey',zorder=0)
            #axs[i].tick_params(axis='x', labelsize=9)
            
            #axs[i].set_xlim(fspar.param_settings.loc[idx,'plot_yy_axis_scale'][0],
                            #fspar.param_settings.loc[idx,'plot_yy_axis_scale'][1])
            #axs[i].xaxis.set_tick_params(length=2)
            
            #if mark_prolines:
                #self.text_marker(axs[i], ax, self.loc[experiment,:,'1-letter'], proline_mark, proline_mark)
            
            #if mark_user_details:
                #for k, v in fsuv.user_spectrum_notes.items():
                    #self.text_marker(axs[i], ax, self.loc[experiment,:,'Details'], k, v)
        
        #dir_path = '{}/{}'.format(self.calc_path, self.tables_and_plots_folder)
        
        #if not(os.path.exists(dir_path)):
            #os.makedirs(dir_path)
        
        #file_path = '{}/BarPlotVertical_{}.{}'.format(dir_path, calccol, figtype)
        
        #fig.savefig(file_path, dpi=figdpi)
        
        #fsut.write_log('*** Plot saved {}\n'.format('/'.join(file_path.split('/')[-2:])))
        #plt.close('all')
    
    def plot_bar_compacted(self, idx, calccol, fig, axs, i, experiment,
    
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
                          
                          x_ticks_rot=0,
                          x_ticks_fs=6,
                          x_ticks_fn='Arial',
                          x_ticks_pad=1,
                          
                          y_ticks_fs=9,
                          y_ticks_pad=-3,
                          y_grid_color='grey',
                          
                          mark_prolines=True,
                          proline_mark='P',
                          
                          mark_user_details=True,
                          
                          mark_fs=3,
                          
                          unassigned_shade=True,
                          unassigned_shade_color='grey',
                          unassigned_shade_alpha=0.5):
        """
        :param: idx, calculated parameter, that is index to param_settings
        """
        # creates a list with the colors to be represented in bars and
        # Xticks. Colors are attributed according to the Peak Status.
        colors_dict = { 'measured':color_measured,
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
        initialresidue = int(self.ix[0, 0, 'Res#'])
        #print(initialresidue)
        finalresidue = int(self.loc[experiment,:,'Res#'].tail(1))
        initialresidue = (initialresidue - 1) // 10 * 10 + 10
        
        #print(np.arange(10, self.loc[experiment].shape[0], 10))
        axs[i].set_xticks(np.arange(10, self.loc[experiment].shape[0], 10))
        
        
        # https://github.com/matplotlib/matplotlib/issues/6266
        #print(np.arange(initialresidue, finalresidue, 10))
        axs[i].set_xticklabels(np.arange(initialresidue, finalresidue, 10),
                               fontsize=x_ticks_fs,
                               rotation=x_ticks_rot,
                               fontname=x_ticks_fn)
                               
        
        
        
        axs[i].set_xlim([-0.2, self.loc[experiment,:,'Res#'].size + 1.2])
        axs[i].xaxis.tick_bottom()
        axs[i].xaxis.set_tick_params(direction='out', length=2)
        axs[i].tick_params(axis='x', which='major', pad=x_ticks_pad)
        #.xlabel('Residue', fontsize=xx_label_font_size, fontweight=xx_label_font_effect, fontname='Arial')
        
        axs[i].yaxis.grid(color=y_grid_color,zorder=0)
        axs[i].tick_params(axis='y', labelsize=8, direction='out', pad=y_ticks_pad)
        
        axs[i].set_ylim(fspar.param_settings.loc[idx,'plot_yy_axis_scale'][0],
                        fspar.param_settings.loc[idx,'plot_yy_axis_scale'][1])
        
        axs[i].yaxis.set_tick_params(length=2)
        
        
        # unassigned shade
        # sets a grey shade over unassigned residues
        if unassigned_shade:
            unassignedmask = self.loc[experiment, :, 'Peak Status'] == 'unassigned'

            for residue in self.loc[experiment, unassignedmask, 'Res#']:
                residue = int(residue) - 0.5
                axs[i].axvspan(residue, residue+1, color=unassigned_shade_color, alpha=unassigned_shade_alpha, lw=0)
        
        
        
        if mark_prolines:
            # in the case of prolines, is necesary to input a bool array
            # where True is met for Prolines because by default bar.get_y()
            # goes negative.
            self.text_marker(axs[i], ax, self.loc[experiment,:,'1-letter'],
                             self.loc[experiment,:,'1-letter'] == proline_mark,
                             proline_mark, proline_mark, fspar.param_settings.loc[idx,'plot_yy_axis_scale'][1], fs=mark_fs)
        
        if mark_user_details:
            for k, v in fsuv.user_spectrum_notes.items():
                self.text_marker(axs[i], ax, self.loc[experiment,:,'Details'],
                                 self.loc[experiment,:,calccol] >= 0, k, v, 
                                 fspar.param_settings.loc[idx,'plot_yy_axis_scale'][1], fs=mark_fs)
    
    def plot_res_evo(self, idx, calccol, fig, axs, i, row_number,
                     
                     title_y=0.97,
                     title_fs=8,
                     title_fn='Arial',
                     
                     set_x_values=False,
                     
                     x_ticks_pad=1,
                     x_ticks_fs=7,
                     xlabel_flag=False,
                     
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
                     fill_alpha=0.5):
        
        # enumerate() should not be necessary because
        # major_axis are always range(0,...) but just in case in the future
        # something changes with the major_axis
        
        #print(self.loc[:,row_number,calccol])
        
        title = self.ix[0,i,'Res#'] + self.ix[0,i,'1-letter']
        
        axs[i].set_title(title, y=title_y, fontsize=title_fs, fontname=title_fn)
        
        y = np.array(self.loc[:,row_number,calccol].fillna(value=0))
        
        if set_x_values and (self.tittype == 'D1' or self.subcontrol == 'D1'):
            x = np.array(fsuv.res_evo_x_values)
            axs[i].set_xlim(0, fsuv.res_evo_x_values[-1])
        elif (self.tittype in ['D2', 'D3']) or (self.subcontrol in ['D2', 'D3']):
            #x = self.items
            xlabel_flag = True
            x = np.arange(0, len(y))
            axs[i].xaxis.set_ticks(x)
        else:
            x = np.arange(0, len(y))
            axs[i].set_xlim(0, len(y)-1)
        
        axs[i].xaxis.tick_bottom()
        axs[i].xaxis.set_tick_params(direction='out', length=2, pad=x_ticks_pad)
        axs[i].tick_params(axis='x', labelsize=x_ticks_fs)
        
        axs[i].set_ylim(fspar.param_settings.loc[idx,'plot_yy_axis_scale'][0],
                        fspar.param_settings.loc[idx,'plot_yy_axis_scale'][1])
        axs[i].yaxis.tick_left()
        axs[i].yaxis.set_tick_params(direction='out', length=2, pad=y_ticks_pad)
        axs[i].tick_params(axis='y', labelsize=y_ticks_fs)
    
        if self.ix[0,row_number,'Peak Status'] == 'unassigned':
            ylim = axs[i].get_ylim()
            ycenter = (ylim[0]+ylim[1])/2
            axs[i].text(x[-1]/2, ycenter, 'unassigned', fontsize=8, fontname='Arial', va='center', ha='center')
            return
        
        #print(np.array(self.loc[:,row_number,'Peak Status'] == 'measured'))
        mes_mask = np.array(self.loc[:,row_number,'Peak Status'] != 'lost')
        
        y = y[mes_mask]
        x = x[mes_mask]
        
        axs[i].plot(x, y, ls=line_style,
                          color=plot_color,
                          marker=marker_style,
                          mfc=marker_color,
                          markersize=marker_size,
                          lw=line_width)
        
        if xlabel_flag:
            axs[i].set_xticklabels(self.items, rotation=45)
        
        if fill_between:
            axs[i].fill_between(x, 0, y, facecolor=fill_color, alpha=fill_alpha)
    
    def plot_base(self, idx, plot_type, plot_style, param_dict,
                     rows_per_page=5,
                     cols_per_page=1,
                     fig_height=11.69,
                     fig_weight=8.69,
                     
                     figsuptytitle_y=0.999,
                     figsuptytitle_fs=8,
                     figsuptitle_fw='bold',
                     figsuptitle_fn='Arial',
                     figsuptitle_ha='center',
                     
                     yy_txt_x=0.004,
                     yy_txt_y=0.5,
                     yy_txt_fs=10,
                     yy_txt_fw='bold',
                     yy_txt_rot=90,
                     yy_txt_va='center',
                     
                     xx_txt='Residue',
                     xx_txt_x=0.5,
                     xx_txt_y=0.01,
                     xx_txt_fs=10,
                     xx_txt_fw='bold',
                     xx_txt_rot=0,
                     xx_txt_ha='center',
                     
                     fig_file_type='pdf',
                     fig_dpi=300):
        
        calccol = fspar.param_settings.loc[idx,'calc_column_name']
        
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
                                figsize=(fig_weight, real_fig_height))
        
        axs = axs.ravel()
        
        fig.suptitle(calccol,
                     y=figsuptytitle_y,
                     fontsize=figsuptytitle_fs,
                     fontweight=figsuptitle_fw,
                     fontname=figsuptitle_fn,
                     ha=figsuptitle_ha)
        
        # Plots yy axis title
        # http://www.futurile.net/2016/03/01/text-handling-in-matplotlib/
        plt.figtext(yy_txt_x, yy_txt_y,
                    fspar.param_settings.loc[idx,'plot_yy_axis_label'],
                    fontsize=yy_txt_fs, fontweight=yy_txt_fw,
                    rotation=yy_txt_rot, va=yy_txt_va)
        
        plt.figtext(xx_txt_x, xx_txt_y, xx_txt,
                    fontsize=xx_txt_fs, fontweight=xx_txt_fw,
                    rotation=xx_txt_rot, ha=xx_txt_ha)
        
        plt.tight_layout(rect=[0.015,0.01,0.995,0.95], h_pad=fig_height/rows_per_page)
        
        
        if plot_style == 'bar_extended':
            
            for i, experiment in enumerate(self):
                self.plot_bar_extended(idx, calccol, fig, axs, i, experiment, **param_dict)
        
        elif plot_style == 'bar_compacted':
            
            for i, experiment in enumerate(self):
                self.plot_bar_compacted(idx, calccol, fig, axs, i, experiment, **param_dict)
        
        elif plot_style == 'res_evo':
            
            for i, row_number in enumerate(self.major_axis):
                self.plot_res_evo(idx, calccol, fig, axs, i, row_number, **param_dict)
        
        
        self.write_plot(fig, plot_style, calccol, fig_file_type, fig_dpi)
        plt.close('all')
    
    def write_plot(self, fig, plot_name, calccol, fig_file_type, fig_dpi):
        
        dir_path = '{}/{}'.format(self.calc_path, self.tables_and_plots_folder)
        
        if not(os.path.exists(dir_path)):
            os.makedirs(dir_path)
        
        file_path = '{}/{}_{}.{}'.format(dir_path, plot_name, calccol, fig_file_type)
        
        fig.savefig(file_path, dpi=fig_dpi)
        
        fsut.write_log('*** Plot saved {}\n'.format('/'.join(file_path.split('/')[-2:])))
    
    
    def fit_curve(self, x, y, whichfit='kd'):
        
        if wichfit == 'kd':
            pass
        
    
    def fit_kd(L0, P0, kd, ymax):
        """
        Fits to a non-linear regression analysis.

        :param P0: given by the user as the actual concentration of the protein
        :param ymax: is calculated along the fit and the value output refers to a P0 = 1.
                     to obtain the ymax for the actual P0 value, the function get_ymax() has
                     to be run.
        """
        y = ymax * (((kd + L0 + P0)-np.sqrt((kd + L0 + P0)**2 - (4*P0*L0)))/2*P0)
        return y
        
    def get_ymax(L0, P0, kd, y):
        """
        From fit_kd() the ymax obtained is that for P0=1.
        in case the P0 is different, the correct ymax has to be calculated.
        it is obtained form get_ymax().

        :param L0: A ligand concentration towards infinite
        :param P0: the actual protein concentration used in fit_kd()
        :param kd: the obtained kd from fit_kd()
        :param y: the ymax value obtained from fit_kd()
        :return: int
        """
        ymax = y / (((kd + L0 + P0) - np.sqrt((kd + L0 + P0) ** 2 - (4 * P0 * L0))) / 2 * P0)
        return ymax
        
    
    def write_Chimera_attributes(self, listpar, resformat=':',
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
        
        
        write_path = '{}/{}'.format(self.calc_path, self.chimera_att_folder)
        
        if not(os.path.exists(write_path)):
            os.makedirs(write_path)
        
        for item in self.items:
            mask_lost = self.loc[item,:,'Peak Status'] == 'lost'
            mask_unassigned = self.loc[item,:,'Peak Status'] == 'unassigned'
            mask_measured = self.loc[item,:,'Peak Status'] == 'measured'
            
            for column in listpar:
                file_path = '{}/{}_{}.att'.format(write_path, item, column)
                fileout = open(file_path, 'w')
                
                
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
             column)
             
                fileout.write(attheader)
                
                formatting[column] = colform
                
                #print(self.loc[item,mask_measured,['Res#',column]])
                
                to_write = self.loc[item,mask_measured,['Res#',column]].to_string(header=False, index=False,
                                formatters=formatting, col_space=0).replace(' ', '')
                
                
                fileout.write(to_write)
                
                fileout.close()
                fsut.write_log('*** File saved {}\n'.format('/'.join(file_path.split('/')[-2:])))
                


