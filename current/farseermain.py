"""
Optimal algorythm to run the Farseer-NMR method.

Usage as main script:

    python <path-to>/farseermain.py <path-to>/farseer-user-variables.py

Can be used as imported module. Contains several functions that aid in
managing the Farseer-NMR analysis routines.

Methods:
    .read_user_variables()
        .config_user_variables()
    .copy_Farseer_version()
    .log_time_stamp()
    .logs()
    .initial_checks()
    .checks_PRE_analysis_flags()
    .checks_cube_axes_flags()
    .checks_plotting_flags()
    .checks_calculation_flags()
    .checks_fit_input()
    .creates_farseer_dataset()
    .reads_peaklists()
    .inits_coords_names()
    .identify_residues()
    .correct_shifts()
    .fill_na()
    .expand_lost()
    .add_missing()
    .organize_columns()
    .init_fs_cube()
    .series_kwargs()
    .gen_series_dcts()
    .eval_series()
    .perform_calcs()
    .perform_fits()
    .PRE_analysis()
    .exports_series()
    .exports_chimera_att_files()
    .plots_data()
    .comparison_analysis_routines()
    .analyse_comparisons()
    .run_farseer()
"""

#  
import importlib.util
import sys
import os
import shutil
import datetime  # used to write the log file
import pandas as pd
#farseer_user_variables are imported in the if __main__ :
from current.fslibs import FarseerCube as fcube
from current.fslibs import FarseerSeries as fss
from current.fslibs import Comparisons as fsc
from current.fslibs import wet as fsw

def read_user_variables(path):
    """
    Reads user defined preferences from file and prepares the module of 
    variables necessary for Farseermain.
    
    Args:
        path (str): path to farseer_user_variables.py.
    
    Returns:
        fsuv (module): contains the user preferences.
    """
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    # IMPORTING FARSEER USER VARIABLES FROM CALCULATION DIR
    # I placed this here as a draft to make it work for now.
    # Simon: for sure with the JSON you will make it work differently :-P
    cwd =  os.path.abspath(path)
    
    # changes current directory to the directory where
    # farseer_user_variables is. In this way, output from calculations is
    # stored in that same directory
    os.chdir(cwd)
    
    spec = \
        importlib.util.spec_from_file_location(\
                            "farseer_user_variables",
                            "{}/farseer_user_variables.py".format(cwd))
    #
    fsuv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fsuv)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    fsuv.cwd = cwd
    fsuv.spectra_path = '{}/spectra'.format(cwd)
    
    fsuv = config_user_variables(fsuv)
    
    return fsuv

def config_user_variables(fsuv):
    """
    Reads user defined variables and converts them to 
    organized dicitonaries or DataFrames.
    
    Prepares helper variables for checking routines.
    
    Stores everything under fsuv module.
    
    Returns:
        fsuv
    """
    
    # does the user want to perform any analysis on the Farseer-NMR cube?
    fsuv.any_axis = any([fsuv.do_cond1, fsuv.do_cond2, fsuv.do_cond3])
    
    # sorted values to be used as x coordinates in the fitting routine
    fsuv.txv = sorted(fsuv.titration_x_values)
    
    # ORDERED names of the restraints that can be calculated
    fsuv.restraint_names = [fsuv.calccol_name_PosF1_delta,
                            fsuv.calccol_name_PosF2_delta,
                            fsuv.calccol_name_CSP,
                            fsuv.calccol_name_Height_ratio,
                            fsuv.calccol_name_Volume_ratio]
    
    # ORDERED calculation restraints flags
    fsuv.restraint_flags = [fsuv.calcs_PosF1_delta,
                            fsuv.calcs_PosF2_delta,
                            fsuv.calcs_CSP,
                            fsuv.calcs_Height_ratio,
                            fsuv.calcs_Volume_ratio]
    
    # does the user want to calculate any restraint?
    fsuv.calc_flags = any(fsuv.restraint_flags)
    
    # does the user want to draw any plot?
    fsuv.plotting_flags = any([fsuv.plots_extended_bar,
                               fsuv.plots_compacted_bar,
                               fsuv.plots_vertical_bar,
                               fsuv.plots_residue_evolution,
                               fsuv.plots_cs_scatter,
                               fsuv.plots_cs_scatter_flower])
    
    # flags which fsuv.apply_PRE_analysis deppends on
    fsuv.PRE_analysis_flags = \
                fsuv.do_cond3 and \
                (fsuv.calcs_Height_ratio or fsuv.calcs_Volume_ratio) and \
                fsuv.perform_comparisons
    
    restraint_settings_dct = {
        'calcs_restraint_flg'   : fsuv.restraint_flags,
                               
        'plt_y_axis_lbl': [fsuv.yy_label_PosF1_delta,
                               fsuv.yy_label_PosF2_delta,
                               fsuv.yy_label_CSP,
                               fsuv.yy_label_Height_ratio,
                               fsuv.yy_label_Volume_ratio],
                               
        'plt_y_axis_scl': [(-fsuv.yy_scale_PosF1_delta,
                                 fsuv.yy_scale_PosF1_delta),
                               (-fsuv.yy_scale_PosF2_delta,
                                 fsuv.yy_scale_PosF2_delta),
                               (0, fsuv.yy_scale_CSP),
                               (0, fsuv.yy_scale_Height_ratio),
                               (0, fsuv.yy_scale_Volume_ratio)]
                               }
    
    # A pd.DataFrame that organizes settings for each calculated restraint.
    # Index are the calculated params labels
    fsuv.restraint_settings = pd.DataFrame(restraint_settings_dct,
                                           index=fsuv.restraint_names)
    
    # configures dictionaries to be passed to plotting functions.
    fsuv.tplot_general_dict = {
        'subtitle_fn':fsuv.tplot_subtitle_fn,
        'subtitle_fs':fsuv.tplot_subtitle_fs,
        'subtitle_pad':fsuv.tplot_subtitle_pad,
        'subtitle_weight':fsuv.tplot_subtitle_weight,
        'x_label_fn':fsuv.tplot_x_label_fn,
        'x_label_fs':fsuv.tplot_x_label_fs,
        'x_label_pad':fsuv.tplot_x_label_pad,
        'x_label_weight':fsuv.tplot_x_label_weight,
        'y_label_fn':fsuv.tplot_y_label_fn,
        'y_label_fs':fsuv.tplot_y_label_fs,
        'y_label_pad':fsuv.tplot_y_label_pad,
        'y_label_weight':fsuv.tplot_y_label_weight,
        'x_ticks_pad':fsuv.tplot_x_ticks_pad,
        'x_ticks_len':fsuv.tplot_x_ticks_len,
        'y_ticks_fn':fsuv.tplot_y_ticks_fn,
        'y_ticks_fs':fsuv.tplot_y_ticks_fs,
        'y_ticks_pad':fsuv.tplot_y_ticks_pad,
        'y_ticks_weight':fsuv.tplot_y_ticks_weight,
        'y_ticks_rot':fsuv.tplot_y_ticks_rot,
        'y_ticks_len':fsuv.tplot_y_ticks_len,
        'y_ticks_nbins':fsuv.yy_scale_nbins,
        'y_grid_flag':fsuv.tplot_y_grid_flag,
        'y_grid_color':fsuv.tplot_y_grid_color,
        'y_grid_linestyle':fsuv.tplot_y_grid_linestyle,
        'y_grid_linewidth':fsuv.tplot_y_grid_linewidth,
        'y_grid_alpha':fsuv.tplot_y_grid_alpha,
        'PRE_flag':fsuv.apply_PRE_analysis,
        'pre_color':fsuv.pre_color,
        'pre_lw':fsuv.pre_lw,
        'tag_color':fsuv.tag_color,
        'tag_lw':fsuv.tag_lw,
        'tag_ls':fsuv.tag_ls
        }
    
    fsuv.bar_plot_general_dict = {
        'measured_color':fsuv.bar_measured_color,
        'status_color_flag':fsuv.bar_status_color_flag,
        'lost_color':fsuv.bar_lost_color,
        'unassigned_color':fsuv.bar_unassigned_color,
        'bar_width':fsuv.bar_width,
        'bar_alpha':fsuv.bar_alpha,
        'bar_linewidth':fsuv.bar_linewidth,
        'threshold_flag':fsuv.bar_threshold_flag,
        'threshold_color':fsuv.bar_threshold_color,
        'threshold_linewidth':fsuv.bar_threshold_linewidth,
        'threshold_alpha':fsuv.bar_threshold_alpha,
        'threshold_zorder':fsuv.bar_threshold_zorder,
        'mark_fontsize':fsuv.bar_mark_fontsize,
        'mark_prolines_flag':fsuv.bar_mark_prolines_flag,
        'mark_prolines_symbol':fsuv.bar_mark_prolines_symbol,
        'mark_user_details_flag':fsuv.bar_mark_user_details_flag,
        'color_user_details_flag':fsuv.bar_color_user_details_flag,
        'user_marks_dict':fsuv.bar_user_marks_dict,
        'user_bar_colors_dict':fsuv.bar_user_bar_colors_dict
        }
    
    fsuv.bar_ext_par_dict = {
        'x_ticks_fn':fsuv.ext_bar_x_ticks_fn,
        'x_ticks_fs':fsuv.ext_bar_x_ticks_fs,
        'x_ticks_rot':fsuv.ext_bar_x_ticks_rot,
        'x_ticks_weight':fsuv.ext_bar_x_ticks_weight,
        'x_ticks_color_flag':fsuv.ext_bar_x_ticks_color_flag
        }
    
    fsuv.comp_bar_par_dict = {
        'x_ticks_fn':fsuv.comp_bar_x_ticks_fn,
        'x_ticks_fs':fsuv.comp_bar_x_ticks_fs,
        'x_ticks_rot':fsuv.comp_bar_x_ticks_rot,
        'x_ticks_weight':fsuv.comp_bar_x_ticks_weight,
        'unassigned_shade':fsuv.comp_bar_unassigned_shade,
        'unassigned_shade_alpha':fsuv.comp_bar_unassigned_shade_alpha
        }
    
    fsuv.revo_plot_general_dict = {
        'subtitle_fn':fsuv.revo_subtitle_fn,
        'subtitle_fs':fsuv.revo_subtitle_fs,
        'subtitle_pad':fsuv.revo_subtitle_pad,
        'subtitle_weight':fsuv.revo_subtitle_weight,
        'x_label_fn':fsuv.revo_x_label_fn,
        'x_label_fs':fsuv.revo_x_label_fs,
        'x_label_pad':fsuv.revo_x_label_pad,
        'x_label_weight':fsuv.revo_x_label_weight,
        'y_label_fn':fsuv.revo_y_label_fn,
        'y_label_fs':fsuv.revo_y_label_fs,
        'y_label_pad':fsuv.revo_y_label_pad,
        'y_label_weight':fsuv.revo_y_label_weight,
        'x_ticks_fn':fsuv.revo_x_ticks_fn,
        'x_ticks_fs':fsuv.revo_x_ticks_fs,
        'x_ticks_pad':fsuv.revo_x_ticks_pad,
        'x_ticks_weight':fsuv.revo_x_ticks_weight,
        'x_ticks_rot':fsuv.revo_x_ticks_rot,
        'y_ticks_fn':fsuv.revo_y_ticks_fn,
        'y_ticks_fs':fsuv.revo_y_ticks_fs,
        'y_ticks_pad':fsuv.revo_y_ticks_pad,
        'y_ticks_weight':fsuv.revo_y_ticks_weight,
        'y_ticks_rot':fsuv.revo_y_ticks_rot,
        }
    
    fsuv.res_evo_par_dict = {
        'x_label':fsuv.res_evo_x_label,
        'set_x_values':fsuv.res_evo_set_x_values,
        'y_ticks_nbins':fsuv.yy_scale_nbins,
        'x_ticks_nbins':fsuv.res_evo_x_ticks_nbins,
        'line_style':fsuv.res_evo_line_style,
        'line_color':fsuv.res_evo_line_color,
        'marker_style':fsuv.res_evo_marker_style,
        'marker_color':fsuv.res_evo_marker_color,
        'marker_size':fsuv.res_evo_marker_size,
        'line_width':fsuv.res_evo_line_width,
        'fill_between':fsuv.res_evo_fill_between,
        'fill_color':fsuv.res_evo_fill_color,
        'fill_alpha':fsuv.res_evo_fill_alpha,
        'fit_perform':fsuv.perform_resevo_fit,
        'fit_line_color':fsuv.res_evo_fit_line_color,
        'fit_line_width':fsuv.res_evo_fit_line_width,
        'fit_line_style':fsuv.res_evo_fit_line_style,
        'titration_x_values':fsuv.txv
        }
    
    fsuv.cs_scatter_par_dict = {
        'x_label':fsuv.cs_scatter_x_label,
        'y_label':fsuv.cs_scatter_y_label,
        'mksize':fsuv.cs_scatter_mksize,
        'scale':fsuv.cs_scatter_scale,
        'mk_type':fsuv.cs_scatter_mk_type,
        'mk_start_color':fsuv.cs_scatter_mk_start_color,
        'mk_end_color':fsuv.cs_scatter_mk_end_color,
        'markers':fsuv.cs_scatter_markers,
        'mk_color':fsuv.cs_scatter_mk_color,
        'mk_edgecolors':fsuv.cs_scatter_mk_edgecolors,
        'mk_lost_color':fsuv.cs_scatter_mk_lost_color,
        'hide_lost':fsuv.cs_scatter_hide_lost
        }
    
    fsuv.cs_scatter_flower_dict = {
        'x_label':fsuv.cs_scatter_x_label,
        'y_label':fsuv.cs_scatter_y_label,
        'mksize':fsuv.cs_scatter_flower_mksize,
        'color_grad':fsuv.cs_scatter_flower_color_grad,
        'mk_start_color':fsuv.cs_scatter_flower_color_start,
        'mk_end_color':fsuv.cs_scatter_flower_color_end,
        'color_list':fsuv.cs_scatter_flower_color_list,
        'x_label_fn':fsuv.cs_scatter_flower_x_label_fn,
        'x_label_fs':fsuv.cs_scatter_flower_x_label_fs,
        'x_label_pad':fsuv.cs_scatter_flower_x_label_pad,
        'x_label_weight':fsuv.cs_scatter_flower_x_label_weight,
        'y_label_fn':fsuv.cs_scatter_flower_y_label_fn,
        'y_label_fs':fsuv.cs_scatter_flower_y_label_fs,
        'y_label_pad':fsuv.cs_scatter_flower_y_label_pad,
        'y_label_weight':fsuv.cs_scatter_flower_y_label_weight,
        'x_ticks_fn':fsuv.cs_scatter_flower_x_ticks_fn,
        'x_ticks_fs':fsuv.cs_scatter_flower_x_ticks_fs,
        'x_ticks_pad':fsuv.cs_scatter_flower_x_ticks_pad,
        'x_ticks_weight':fsuv.cs_scatter_flower_x_ticks_weight,
        'x_ticks_rot':fsuv.cs_scatter_flower_x_ticks_rot,
        'y_ticks_fn':fsuv.cs_scatter_flower_y_ticks_fn,
        'y_ticks_fs':fsuv.cs_scatter_flower_y_ticks_fs,
        'y_ticks_pad':fsuv.cs_scatter_flower_y_ticks_pad,
        'y_ticks_weight':fsuv.cs_scatter_flower_y_ticks_weight,
        'y_ticks_rot':fsuv.cs_scatter_flower_y_ticks_rot,
        'x_max':fsuv.yy_scale_PosF1_delta,
        'x_min':-fsuv.yy_scale_PosF1_delta,
        'y_max':fsuv.yy_scale_PosF2_delta,
        'y_min':-fsuv.yy_scale_PosF2_delta
        }
    
    fsuv.heat_map_dict = {
        'vmin':fsuv.heat_map_vmin,
        'vmax':fsuv.heat_map_vmax,
        'x_ticks_fn':fsuv.heat_map_x_ticks_fn,
        'x_ticks_fs':fsuv.heat_map_x_ticks_fs,
        'x_ticks_pad':fsuv.heat_map_x_ticks_pad,
        'x_ticks_weight':fsuv.heat_map_x_ticks_weight,
        'x_ticks_rot':fsuv.heat_map_x_ticks_rot,
        'y_label_fn':fsuv.heat_map_y_label_fn,
        'y_label_fs':fsuv.heat_map_y_label_fs,
        'y_label_pad':fsuv.heat_map_y_label_pad,
        'y_label_weight':fsuv.heat_map_y_label_weight,
        'right_margin':fsuv.heat_map_right_margin,
        'bottom_margin':fsuv.heat_map_bottom_margin,
        #'top_margin':fsuv.heat_map_top_margin,
        'cbar_font_size':fsuv.heat_map_cbar_font_size,
        'tag_color':fsuv.tag_color,
        'tag_lw':fsuv.tag_lw,
        'tag_ls':fsuv.tag_ls
        }
    
    fsuv.delta_osci_dict = {
        'y_label_fs':fsuv.dpre_osci_y_label_fs,
        'dpre_ms':fsuv.dpre_osci_dpre_ms,
        'dpre_alpha':fsuv.dpre_osci_dpre_alpha,
        'smooth_lw':fsuv.dpre_osci_smooth_lw,
        'ref_color':fsuv.dpre_osci_ref_color,
        'color_init':fsuv.dpre_osci_color_init,
        'color_end':fsuv.dpre_osci_color_end,
        'x_ticks_fn':fsuv.dpre_osci_x_ticks_fn,
        'x_ticks_fs':fsuv.dpre_osci_x_ticks_fs,
        'x_ticks_pad':fsuv.dpre_osci_x_ticks_pad,
        'x_ticks_weight':fsuv.dpre_osci_x_ticks_weight,
        'grid_color':fsuv.dpre_osci_grid_color,
        'shade':fsuv.dpre_osci_shade,
        'shade_regions':fsuv.dpre_osci_shade_regions,
        'res_highlight':fsuv.dpre_osci_res_highlight,
        'res_hl_list':fsuv.dpre_osci_res_hl_list,
        'res_highlight_fs':fsuv.dpre_osci_rh_fs,
        'res_highlight_y':fsuv.dpre_osci_rh_y,
        }
    
    return fsuv

def copy_Farseer_version(fsuv, file_name='farseer_version',
                              compress_type='zip'):
    """
    Makes a copy of the running version.
    
    Args:
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.cwd
    """
    
    script_wd = os.path.dirname(os.path.realpath(__file__))
    shutil.make_archive('{}/{}'.format(fsuv.cwd, file_name),
                        compress_type,
                        script_wd)
    
    return 

def log_time_stamp(logfile_name, mod='a', state='STARTED'):
    """Creates a time stamp for the log file."""
    log_title = \
        '{0}  \n**LOG {2}:** {1} \n{0}  \n'.\
            format(79*'*',
                   datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"),
                   state)
    
    logs(log_title, logfile_name, mod=mod)
    
    return

def logs(s, logfile_name, mod='a'):
    """
    Prints <s> and writes it to log file.
    
    Args:
        s (str): the string to write.
        
        logfile_name (str): the log file name.
        
        mod (str): python.open() arg mode.
    """
    print(s)
    
    with open(logfile_name, mod) as logfile:
        logfile.write(s)
    
    return

def initial_checks(fsuv):
    """
    Performs checks that are useful to be executed at the beginning of the
    Farseer-NMR calculation run.
    
    Args:
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.apply_PRE_analysis
    """
    # PRE routines take only place at advanced stages of the 
    # Farseer-NMR calculation. It would be a waste to have an error after 2h...
    if fsuv.apply_PRE_analysis:
        checks_PRE_analysis_flags(fsuv)
        
    return

def checks_PRE_analysis_flags(fsuv):
    """
    Checks flag compatibility in PRE Analysis routines.
    
    Args:
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.PRE_analysis_flags
    fsuv.logfile_name
    """
    # if all the flags upon which aplly_PRE_analysis depends on are
    # turned off:
    if not(fsuv.PRE_analysis_flags):
        #DO
        msg = "PRE Analaysis is set to <{}> and depends on the following variables: do_cond3 :: <{}> || calcs_Height_ratio OR calcs_Volume_ratio :: <{}> || perform_comparisons :: <{}>. All these variables should be set to True for PRE Analysis to be executed.".\
            format(fsuv.apply_PRE_analysis,
                   fsuv.do_cond3,
                   fsuv.calcs_Height_ratio or fsuv.calcs_Volume_ratio,
                   fsuv.perform_comparisons)
           
        logs(fsw.gen_wet('ERROR', msg, 1), fsuv.logfile_name)
        logs(fsw.abort_msg(), fsuv.logfile_name)
        fsw.abort()
        #DONE
    
    return

def checks_cube_axes_flags(fsuv):
    """
    Checks if the user wants to perform any analysis
    on the Farseer-NMR Cube.
    
    Args:
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.any_axis
    fsuv.logfile_name
    """
    if not(fsuv.any_axis):
        # DO
        msg = "Analysis over X, Y or Z Farseer-NMR Cube's axes are all deactivated. There is nothing to calculate. Confirm this is actually what you want."
        
        logs(fsw.gen_wet('NOTE', msg, 2), fsuv.logfile_name)
        # DONE
        return False
    else:
        return True
    return

def checks_plotting_flags(farseer_series, fsuv, resonance_type):
    """
    Checks whether any plotting flag is activated.
    
    Args:
        farseer_series (FarseerSeries instance): contains the experiments
            of the series.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
        
        resonance_type (str): {'Backbone', 'Sidechains'}
     
    Returns:
        True if any plotting flag is activated,
        False otherwise.
    """
    
    if not(fsuv.plotting_flags):
        # DO ++++
        for restraint in fsuv.restraint_settings.index:
            # DO export calculation tables
            if fsuv.restraint_settings.loc[restraint,'calcs_restraint_flg']:
                farseer_series.write_table(restraint,
                                           restraint,
                                            resonance_type=resonance_type)
            # DONE
        
        msg = "All potting flags are turned off. No plots will be drawn. Confirm in the Settings menu if this is the desired configuration. I won't leave you with empty hands though, all calculated restraints have been exported in nicely formated tables ;-)"
        
        farseer_series.log_r(fsw.gen_wet('NOTE', msg, 3))
        
        return False
        # DONE ++++
    
    return True

def checks_calculation_flags(fsuv):
    """
    Checks if the user wants to calculate any restraints.
    
    Args:
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    """
    ######## WET#14
    if not(fsuv.calc_flags):
        #DO
        msg = "All restraints calculation routines are deactivated. Nothing will be calculated."
        
        logs(fsw.gen_wet('WARNING', msg, 14), fsuv.logfile_name)
        #DONE
    ########
    return

def checks_fit_input(series, fsuv):
    """
    Checks whether required fit data and settings are provided correctly.
    
    Args:
        series (FarseerSeries instance):
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    """
    
    ######## WET#5, WET#6, WET#7
    if not(all([True if x>=0 else False for x in fsuv.txv])):
        # DO
        msg = 'There are negative values in titration_x_values variable. Fitting to the Hill Equation does not accept negative values. Please revisit your input'
        
        series.log_r(fsw.gen_wet('ERROR', msg, 6))
        series.abort()
        # DONE
    
    elif len(fsuv.txv) != len(series.items):
        # DO
        msg = "The number of coordinate values defined for fitting/data respresentation, <fitting_x_values> variable [{}], do not match the number of <cond1> data points,i.e. input peaklists. Please correct <fitting_x_values> variable or confirm you have not forgot any peaklist [{}].".format(txv, series.items)
        
        series.log_r(fsw.gen_wet('ERROR', msg, 5))
        series.abort()
        # DONE
        
    else:
        # DO
        msg = "The number of coordinate values for data fitting along X axis equals the number of input peaklists, and no negative value was found. Data fit to the Hill Equation will be performed with the following values: {}.".format(fsuv.txv)
        
        series.log_r(fsw.gen_wet('NOTE', msg, 7))
        # DONE
    return

def creates_farseer_dataset(fsuv):
    """
    Creates a Farseer-NMR dataset.
    
    Args:
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Returns:
        exp (FarseerCube class instance): contains all peaklist data.
    
    Depends on:
    fsuv.spectra_path
    fsuv.has_sidechains
    fsuv.FASTAstart
    fsuv.logfile_name
    """
    exp = fcube.FarseerCube(fsuv.spectra_path,
                            has_sidechains=fsuv.has_sidechains,
                            FASTAstart=fsuv.FASTAstart)
    
    exp.log_export_onthefly=True
    exp.log_export_name=fsuv.logfile_name
    
    return exp

def reads_peaklists(exp, fsuv):
    """
    Loads Peaklist's Tree.
    
    Args:
        exp (FarseerCube class instance): contains all peaklist data.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.applyFASTA
    """
    
    exp.load_experiments()
    
    if fsuv.applyFASTA:
        exp.load_experiments(filetype='.fasta')
    
    # even if the user does no want to analyse sidechains, Farseer-NMR
    # has to parse them out from the input peaklist if they exist
    if exp.has_sidechains:
        # str() is passed as a dummy function
        exp.load_experiments(resonance_type='Sidechains')
    
    return
    
def identify_residues(exp):
    """
    Reads Assignment information using FarseerCube.split_res_info().
    
    Args:
        exp (FarseerCube class instance): contains all peaklist data.
    """
    exp.split_res_info()
    
    return

def correct_shifts(exp, fsuv, resonance_type='Backbone'):
    """
    Corrects chemical shifts for all the peaklists to a reference peak
    in the (0,0,0) Farseer-NMR Cube coordinate.
    
    Uses FarseerCube.correct_shifts_*
    
    Args:
        exp (FarseerCube class instance): contains all peaklist data.
    
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.cs_correction_res_ref
    """
    
    if resonance_type == 'Backbone':
        exp.correct_shifts_backbone(fsuv.cs_correction_res_ref)
    
    elif resonance_type=='Sidechains':
        exp.correct_shifts_sidechains()
    
    return

def fill_na(peak_status, merit=0, details='None'):
    """
    A dictionary that configures how the fields of the
    added rows for missing residues are fill.
    
    Args:
        peak_status (str): {'lost', 'unassigned'}, how to fill 'Peak Status' column.
        
        merit (int/str): how to fill the 'Merit' column.
        
        details (str): how to fill the details column.
        
    Return:
        Dictionary of kwargs.
    """
    d = {
    'Peak Status': peak_status,
    'Merit': merit,
    'Details': details
    }
    return d

#def expand_lost(exp, dataset_dct, acoords, bcoords, refcoord, dim='z'):
def expand_lost(exp, resonance_type='Backbone', dim='z'):
    """
    Checks for 'lost' residues accross the reference experiments and
    along other axes (y or z).
    
    Uses FarseerCube.finds_missing.
    
    Compares reference peaklists along Y and Z axis of the Farseer-NMR
    Cube and generates the corresponding 'lost' residues.
    This function is useful when analysing dia/ and paramagnetic/ series
    along the Z axis.
    
    Args:
        exp (FarseerCube class instance): contains all peaklist data.
        
        dataset_dct (attribute of <exp>): the peaklist data set where effects
            take place.
    
        fsuv (module): contains all the user defined variables.
    """
    
    exp.compares_references(fill_na('lost'), along_axis=dim,
                            resonance_type=resonance_type)
    
    #if dim == 'y':
        #exp.log_r(\
        #'EXPANDS LOST RESIDUES TO CONDITIONS {}'.format(dim.upper()),
        #istitle = True)
        ## expands to yy (cond2) condition
        #for a in acoords:
            ##do
            #for b in bcoords:
                ##do
                #refscoords = {'z': a, 'y': refcoord}
                #exp.finds_missing(a, b, exp.xxref, 'expanding',
                               #dataset_dct, 
                               #dataset_dct,
                               #fill_na_lost('lost'),
                               #refscoords=refscoords)
    #if dim == 'z':
        #exp.log_r(\
        #'EXPANDS LOST RESIDUES TO CONDITIONS {}'.format(dim.upper()),
        #istitle = True)
        ## expands to yy (cond2) condition
        #for a in acoords:
            ##do
            #for b in bcoords:
                ##do
                #refscoords = {'z': refcoord, 'y': a}
                #exp.finds_missing(b, a, exp.xxref, 'expanding',
                               #dataset_dct, 
                               #dataset_dct,
                               #fill_na('lost'),
                               #refscoords=refscoords)
    
    return

def add_missing(exp, peak_status='lost', resonance_type='Backbone'):
    """
    Expands a <target> peaklist to the index of a <reference> peaklist.
    Uses finds_missing method of FarseerSet.py.
    
    Args:
        exp (FarseerCube class instance): contains all peaklist data.
        
        peak_status (str): {'lost', 'unassigned'} the peak status of the new
            generated entries for missing peaks.
        
        resonance_type (str): {'Backbone', 'Sidechains'}
    """
    
    exp.finds_missing(fill_na(peak_status), missing=peak_status,
                                         resonance_type=resonance_type)
    
    return

def organize_columns(exp, fsuv, resonance_type='Backbone'):
    """
    Uses FarseerSet.organize_cols().
    
    Args:
        exp (FarseerCube class instance): contains all peaklist data.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
        
        resonance_type (str): {'Backbone','Sidechains'}
    
    Depends on:
    fsuv.perform_cs_correction
    """
    
    exp.organize_cols(performed_cs_correction=fsuv.perform_cs_correction,
                      resonance_type=resonance_type)
    
    return

def init_fs_cube(exp, fsuv):
    """
    Inits Farseer-NMR Cube.
    The Cube is stored as an attribute of the FarseerCube instance.
    
    Args:
        exp (FarseerCube class instance): contains all peaklist data.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.use_sidechains
    """
    exp.init_Farseer_cube(use_sidechains=fsuv.use_sidechains)
    
    return

def series_kwargs(fsuv, rt='Backbone'):
    """
    Defines the kwargs dictionary that will be used to generate
    the FarseerSeries object based on the user defined preferences.
    
    Args:
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
        
        rt (str): {'Backbone', 'Sidechains'}, whether data corresponds to
            one or another.
    
    Depends on:
    fsuv.csp_alpha4res
    fsuv.csp_res_exceptions
    fsuv.cs_lost
    fsuv.restraint_names
    """
    dd = {'resonance_type':rt,
          'csp_alpha4res':fsuv.csp_alpha4res,
          'csp_res_exceptions':fsuv.csp_res_exceptions,
          'cs_lost':fsuv.cs_lost,
          'restraint_list':fsuv.restraint_names,
          'log_export_onthefly':True,
          'log_export_name':fsuv.logfile_name}
    
    return dd

def gen_series_dcts(exp, series_class, fsuv, resonance_type='Backbone'):
    """
    Generates a nested dictionary, <D>, containing all possible series over all the 
    three Farseer-NMR Cube axis.
    
    Args:
        exp (FarseerCube class instance): contains all peaklist data.
        
        series_class (FarseerSeries class): The class that will 
            initiate the series, normally fslibs/FarseerSeries.py
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
        
        resonance_type OPT (stg): {'Backbone', 'Sidechains'} depending on
            data in <exp>.
    
    
    <D> contains a first level key for each Farseer-NMR Cube's axis.
    Each of these keys contains a second nested dictionary enclosing
    all the experimental series along that axis as extracted from
    the Farseer-NMR Cube.
    
    Creates series only for user activated axis.
    
    The first level keys of the experimental series are the "next axis"
    datapoints, and the second level keys are the "previous axis" datapoints.
    
    Example:
        for X axis series, keys are:
            Y1
                Z1
                Z2
            Y2
                Z1
                Z2
        
        for Z axis series:
            X1
                Y1
                Y2
            X2
                Y1
                Y2
    
    Depends on:
    fsuv.do_cond1
    fsuv.do_cond2
    fsuv.do_cond3
    """
    
    if not(checks_cube_axes_flags(fsuv)):
        return None
    
    # initiates dictionary
    series_dct = {}
    
    # creates set of series for the first condition (1D)
    if exp.hasxx and fsuv.do_cond1:
        series_dct['cond1'] = \
            exp.export_series_dict_over_axis(\
                series_class,
                along_axis='x',
                resonance_type=resonance_type,
                series_kwargs=series_kwargs(fsuv, rt=resonance_type))
    
    # creates set of series for the second condition (2D)
    if exp.hasyy and fsuv.do_cond2:
        series_dct['cond2'] = \
            exp.export_series_dict_over_axis(\
                series_class,
                along_axis='y',
                resonance_type=resonance_type,
                series_kwargs=series_kwargs(fsuv, rt=resonance_type))

    # creates set of series for the third condition (3D)  
    if exp.haszz and fsuv.do_cond3:
        series_dct['cond3'] = \
            exp.export_series_dict_over_axis(\
                series_class,
                along_axis='z',
                resonance_type=resonance_type,
                series_kwargs=series_kwargs(fsuv, rt=resonance_type))
    
    return series_dct

def eval_series(series_dct, fsuv, resonance_type='Backbone'):
    """
    Executes the Farseer-NMR Analysis Routines over all the series of
    the activated Farseer-NMR Cube Axes.
    
    Args:
        series_dct (dict): a nested dictionary containing the FarseerSeries
            for every axis of the Farseer-NMR Cube.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
        resonance_type OPT (str): {'Backbone', 'Sidechains'} whether the data 
            in <series_dct> corresponds to backbone or sidechain resonances.
    """
    
    # for each kind of titration (cond{1,2,3})
    for cond in sorted(series_dct.keys()):
        # for each point in the corresponding second dimension/condition
        for dim2_pt in sorted(series_dct[cond].keys()):
            # for each point in the corresponding first dimension/condition
            for dim1_pt in sorted(series_dct[cond][dim2_pt].keys()):
                series_dct[cond][dim2_pt][dim1_pt].\
                    log_r('ANALYZING... [{}] - [{}][{}]'.format(cond,
                                                                dim2_pt,
                                                                dim1_pt),
                          istitle=True)
                # DO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # flags and checks are under each function.
                
                # performs the calculations
                perform_calcs(series_dct[cond][dim2_pt][dim1_pt], fsuv)
                
                # PERFORMS FITS
                perform_fits(series_dct[cond][dim2_pt][dim1_pt], fsuv)
                
                # Analysis of PRE data - only in cond3
                PRE_analysis(series_dct[cond][dim2_pt][dim1_pt], fsuv)
                
                # EXPORTS FULLY PARSED PEAKLISTS
                exports_series(series_dct[cond][dim2_pt][dim1_pt])
                
                # EXPORTS CHIMERA FILES
                exports_chimera_att_files(\
                    series_dct[cond][dim2_pt][dim1_pt], fsuv)
                
                # PLOTS DATA
                # plots data are exported together with the plots in
                # fsT.plot_base(), but can be used separatly with
                # fsT.write_table()
                plots_data(series_dct[cond][dim2_pt][dim1_pt],
                           fsuv, resonance_type=resonance_type)
                
                #DONE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                
    return

def perform_calcs(farseer_series, fsuv):
    """
    Calculates the NMR restraints according to the user specifications.
    
    Args:
        farseer_series (FarseerSeries class): a FarseerSeries class object
            containing all the experiments along a series previously
            selected from the Farseer-NMR Cube.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.calcs_PosF1_delta
    fsuv.calcs_PosF2_delta
    fsuv.calcs_CSP
    fsuv.calcs_Height_ratio
    fsuv.calcs_Volume_ratio
    fsuv.calccol_name_PosF1_delta
    fsuv.calccol_name_PosF2_delta
    fsuv.calccol_name_CSP
    fsuv.calccol_name_Height_ratio
    fsuv.calccol_name_Volume_ratio
    """
    
    checks_calculation_flags(fsuv)
    
    # if the user wants to calculate combined Chemical Shift Perturbations
    if fsuv.calcs_CSP:
        # calculate differences in chemical shift for each dimension
        farseer_series.calc_cs_diffs(fsuv.calccol_name_PosF1_delta,
                                      'Position F1')
        farseer_series.calc_cs_diffs(fsuv.calccol_name_PosF2_delta,
                                      'Position F2')
    
        # Calculates CSPs
        farseer_series.calc_csp(calccol=fsuv.calccol_name_CSP,
                                 pos1=fsuv.calccol_name_PosF1_delta,
                                 pos2=fsuv.calccol_name_PosF2_delta)
    
    # if the user only wants to calculate perturbation in single dimensions
    else:
        if fsuv.calcs_PosF1_delta:
            farseer_series.calc_cs_diffs(fsuv.calccol_name_PosF1_delta,
                                          'Position F1')
        if fsuv.calcs_PosF2_delta:
            farseer_series.calc_cs_diffs(fsuv.calccol_name_PosF2_delta,
                                          'Position F2')
    
    # Calculates Ratios
    if fsuv.calcs_Height_ratio:
        farseer_series.calc_ratio(fsuv.calccol_name_Height_ratio, 'Height')
    if fsuv.calcs_Volume_ratio:
        farseer_series.calc_ratio(fsuv.calccol_name_Volume_ratio, 'Volume')
    
    return

def perform_fits(farseer_series, fsuv): 
    """
    Performs fits for 1H, 15N and CSPs data along the X axis series.
    
    Args:
        farseer_series (FarseerSeries class): a FarseerSeries class object
            containing all the experiments along a series previously
            selected from the Farseer-NMR Cube.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.perform_resevo_fit
    fsuv.restraint_settings
    fsuv.txv
    """
    # fits are allowed only for X axis series
    if not(fsuv.perform_resevo_fit \
           and farseer_series.series_axis == 'cond1'):
        return
    
    checks_fit_input(farseer_series, fsuv)
    
    for restraint in fsuv.restraint_settings.index[:3]:
        
        if fsuv.restraint_settings.loc[restraint, 'calcs_restraint_flg']:
            
            farseer_series.perform_fit(calccol = restraint,
                                        x_values=fsuv.txv)
    return

def PRE_analysis(farseer_series, fsuv):
    """
    Optimized algorythm that performs all possible PRE analysis.
    
    Args:
        farseer_series (FarseerSeries class): a FarseerSeries class object
            containing all the experiments along a series previously
            selected from the Farseer-NMR Cube.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.apply_PRE_analysis
    fsuv.restraint_settings
    fsuv.gaussian_stddev
    fsuv.gauss_x_size
    fsuv.restraint_settings
    fsuv.heat_map_rows
    fsuv.fig_height
    fsuv.fig_width
    fsuv.dpre_osci_width
    fsuv.fig_file_type
    fsuv.fig_dpi
    """
    # if user do not wants PRE analysis, do nothing
    if not(fsuv.apply_PRE_analysis):
        return
    # if analysing cond3: performs calculations.
    if farseer_series.series_axis == 'cond3':
        farseer_series.load_theoretical_PRE(fsuv.spectra_path,
                                             farseer_series.prev_dim)
        
        for sourcecol, targetcol in zip(fsuv.restraint_settings.index[3:],\
                                        ['Hgt_DPRE', 'Vol_DPRE']):
        
            # only in the parameters allowed by the user
            if fsuv.restraint_settings.loc[sourcecol, 'calcs_restraint_flg']:
                farseer_series.calc_Delta_PRE(sourcecol, targetcol,
                                         gaussian_stddev=fsuv.gaussian_stddev,
                                         guass_x_size=fsuv.gauss_x_size)
    
    # plots the calculated Delta_PRE and Delta_PRE_smoothed analsysis
    # for cond3 and for comparison C3.
    if farseer_series.series_axis == 'cond3' \
            or (farseer_series.series_axis == 'C3' \
                and (farseer_series.prev_dim == 'para'\
                    or farseer_series.next_dim == 'para')):
        
        # do
        for sourcecol, targetcol in \
            zip(list(fsuv.restraint_settings.index[3:])*2,
                                        ['Hgt_DPRE',
                                         'Vol_DPRE',
                                         'Hgt_DPRE_smooth',
                                         'Vol_DPRE_smooth']):
            
            # only for the parameters allowed by the user
            if fsuv.restraint_settings.loc[sourcecol, 'calcs_restraint_flg']:
                
                farseer_series.plot_base(targetcol, 'exp', 'heat_map',
                    fsuv.heat_map_dict,
                    par_ylims=\
                    fsuv.restraint_settings.loc[sourcecol,'plt_y_axis_scl'],
                    ylabel=\
                    fsuv.restraint_settings.loc[sourcecol,'plt_y_axis_lbl'],
                    cols_per_page=1,
                    rows_per_page=fsuv.heat_map_rows,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
    
    # plots the DeltaPRE oscilation analysis only for <C3> comparison.
    # because DeltaPRE oscilation represents the results obtained only
    # for paramagnetic ('para') data.
    if farseer_series.series_axis == 'C3' \
        and (farseer_series.prev_dim == 'para' \
            or farseer_series.next_dim == 'para'):
        
        
        for sourcecol, targetcols in zip(fsuv.restraint_settings.index[3:],
                                         ['Hgt_DPRE', 'Vol_DPRE']):
            if fsuv.restraint_settings.loc[sourcecol, 'calcs_restraint_flg']:
                farseer_series.plot_base(targetcols, 'exp', 'delta_osci',
                    {**fsuv.tplot_general_dict,**fsuv.delta_osci_dict},
                    par_ylims=(0,fsuv.dpre_osci_ymax),
                    ylabel=fsuv.dpre_osci_y_label,
                    cols_per_page=1,
                    rows_per_page=fsuv.dpre_osci_rows,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width/fsuv.dpre_osci_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
    
    return

def exports_series(farseer_series):
    """
    Exports FarseerSeries to tsv files.
    
    Uses FarseerSeries.export_seres_to_tsv()
    
    Args:
        farseer_series (FarseerSeries instance)
    """
    farseer_series.export_series_to_tsv()
    return

def exports_chimera_att_files(farseer_series, fsuv):
    """
    Exports formatted UCSF Chimera Attribute files for the
    calculated restraints.
    
    http://www.cgl.ucsf.edu/chimera/docs/ContributedSoftware/defineattrib/defineattrib.html#attrfile
    
    Args:
        farseer_series (FarseerSeries instance): contains all the experiments
            of a Farseer-NMR Cube extracted series.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.restraint_settings
    fsuv.chimera_att_select_format
    """
    
    for restraint in fsuv.restraint_settings.index:
        # if the user wants to plot this parameter
        if fsuv.restraint_settings.loc[restraint,'calcs_restraint_flg']:
            # do export chimera attribute files
            farseer_series.write_Chimera_attributes(\
                    restraint,
                    resformat=fsuv.chimera_att_select_format)
    
    return

def plots_data(farseer_series, fsuv, resonance_type='Backbone'):
    """
    Walks through the plotting routines and plots according to user
    preferences.
    
    Args:
        farseer_series (FarseerSeries class): contains all the experiments
            of a Farseer-NMR Cube extracted series.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Depends on:
    fsuv.plots_extended_bar
    fsuv.plots_compacted_bar
    fsuv.plots_vertical_bar
    fsuv.plots_residue_evolution
    fsuv.plots_cs_scatter
    fsuv.plots_cs_scatter_flower
    fsuv.restraint_settings
    fsuv.tplot_general_dict
    fsuv.bar_plot_general_dict
    fsuv.bar_ext_par_dict
    fsuv.comp_bar_par_dict
    fsuv.revo_plot_general_dict
    fsuv.res_evo_par_dict
    fsuv.cs_scatter_par_dict
    fsuv.cs_scatter_flower_dict
    """
    
    are_plots = checks_plotting_flags(farseer_series, fsuv, resonance_type)
    
    if not(are_plots):
        return
    
    # PLOTS DATA
    for restraint in fsuv.restraint_settings.index:
        # if the user has calculated this restraint
        if fsuv.restraint_settings.loc[restraint,'calcs_restraint_flg']:
            if farseer_series.resonance_type == 'Backbone':
                
                # Plot Extended Bar Plot
                if fsuv.plots_extended_bar:
                    farseer_series.plot_base(
                        restraint, 'exp', 'bar_extended',
                        {**fsuv.tplot_general_dict,
                         **fsuv.bar_plot_general_dict,
                         **fsuv.bar_ext_par_dict},
                        par_ylims=\
                        fsuv.restraint_settings.loc[restraint,
                                                 'plt_y_axis_scl'],
                        ylabel=\
                        fsuv.restraint_settings.loc[restraint,
                                                 'plt_y_axis_lbl'],
                        hspace=fsuv.tplot_vspace,
                        cols_per_page=fsuv.ext_bar_cols_page,
                        rows_per_page=fsuv.ext_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
                
                # Plot Compacted Bar Plot
                if fsuv.plots_compacted_bar:
                    
                    farseer_series.plot_base(\
                        restraint, 'exp', 'bar_compacted',
                        {**fsuv.tplot_general_dict,
                         **fsuv.bar_plot_general_dict,
                         **fsuv.comp_bar_par_dict},
                        par_ylims=\
                        fsuv.restraint_settings.loc[restraint,
                                                 'plt_y_axis_scl'],
                        ylabel=\
                        fsuv.restraint_settings.loc[restraint,
                                                 'plt_y_axis_lbl'],
                        hspace=fsuv.tplot_vspace,
                        cols_per_page=fsuv.comp_bar_cols_page,
                        rows_per_page=fsuv.comp_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
            
                # Plot Vertical Bar Plot
                if fsuv.plots_vertical_bar:
                    farseer_series.plot_base(
                        restraint, 'exp', 'bar_vertical',
                        {**fsuv.tplot_general_dict,
                         **fsuv.bar_plot_general_dict,
                         **fsuv.bar_ext_par_dict},
                        par_ylims=\
                        fsuv.restraint_settings.loc[restraint,
                                                 'plt_y_axis_scl'],
                        ylabel=\
                        fsuv.restraint_settings.loc[restraint,
                                                 'plt_y_axis_lbl'],
                        cols_per_page=fsuv.vert_bar_cols_page,
                        rows_per_page=fsuv.vert_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
            
            # Sidechain data is represented in a different bar plot
            elif farseer_series.resonance_type == 'Sidechains'\
                and (fsuv.plots_extended_bar or fsuv.plots_compacted_bar):
                # DO ++++
                farseer_series.plot_base(
                    restraint, 'exp', 'bar_extended',
                    {**fsuv.tplot_general_dict,
                     **fsuv.bar_plot_general_dict,
                     **fsuv.bar_ext_par_dict},
                    par_ylims=\
                    fsuv.restraint_settings.loc[restraint,
                                             'plt_y_axis_scl'],
                    ylabel=\
                    fsuv.restraint_settings.loc[restraint,
                                             'plt_y_axis_lbl'],
                    hspace=fsuv.tplot_vspace,
                    cols_per_page=fsuv.ext_bar_cols_page,
                    rows_per_page=fsuv.ext_bar_rows_page,
                    resonance_type='Sidechains',
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width/2,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
                # DONE ++++
            
            # Plots Parameter Evolution Plot
            if fsuv.plots_residue_evolution:
                farseer_series.plot_base(\
                    restraint, 'res', 'res_evo',
                    {**fsuv.revo_plot_general_dict, **fsuv.res_evo_par_dict},
                    par_ylims=  
                    fsuv.restraint_settings.loc[restraint,
                                             'plt_y_axis_scl'],
                    ylabel=\
                    fsuv.restraint_settings.loc[restraint,
                                             'plt_y_axis_lbl'],
                    cols_per_page=fsuv.res_evo_cols_page,
                    rows_per_page=fsuv.res_evo_rows_page,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
            
    if fsuv.plots_cs_scatter \
        and ((fsuv.calcs_PosF1_delta and fsuv.calcs_PosF2_delta)\
            or fsuv.calcs_CSP):
        # DO ++++
        farseer_series.plot_base('15N_vs_1H', 'res', 'cs_scatter',
                            {**fsuv.revo_plot_general_dict,
                             **fsuv.cs_scatter_par_dict},
                            cols_per_page=fsuv.cs_scatter_cols_page,
                            rows_per_page=fsuv.cs_scatter_rows_page,
                            fig_height=fsuv.fig_height,
                            fig_width=fsuv.fig_width,
                            fig_file_type=fsuv.fig_file_type,
                            fig_dpi=fsuv.fig_dpi)
    
    if fsuv.plots_cs_scatter_flower \
        and ((fsuv.calcs_PosF1_delta and fsuv.calcs_PosF2_delta)\
            or fsuv.calcs_CSP):
        #DO ++++
        farseer_series.plot_base('15N_vs_1H', 'single', 'cs_scatter_flower',
                                  {**fsuv.revo_plot_general_dict,
                                   **fsuv.cs_scatter_flower_dict},
                                  cols_per_page=2,
                                  rows_per_page=3,
                                  fig_height=fsuv.fig_height,
                                  fig_width=fsuv.fig_width,
                                  fig_file_type=fsuv.fig_file_type,
                                  fig_dpi=fsuv.fig_dpi)
        # DONE ++++
    return

def comparison_analysis_routines(comp_panel, fsuv, resonance_type):
        """
        The set of routines that are run for each comparative series.
        
        Args:
            comp_panel (FarseerSeries instance generated from 
                Comparisons.gen_next_dim or gen_prev_dim): contains all the 
                experiments parsed along an axis and for a specific Farseer-NMR Cube's coordinates.
            
            fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
            
            resonance_type (str): {'Backbone', 'Sidechains'}, depending on
                data type.
        """
        # EXPORTS FULLY PARSED PEAKLISTS
        exports_series(comp_panel)
        
        # performs pre analysis
        PRE_analysis(comp_panel, fsuv)
        
        exports_chimera_att_files(comp_panel, fsuv)
        
        # plots data
        plots_data(comp_panel, fsuv, resonance_type='Backbone')
        
        return

def analyse_comparisons(series_dct, fsuv,
                        resonance_type='Backbone'):
    """
    Algorythm to perform data comparisons over analysed conditions.
    
    Args:
        series_dct (dict): a nested dictionary containing the FarseerSeries
            for every axis of the Farseer-NMR Cube.
        
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    
    Returns:
        comp_dct (dict): a dictionary containing all the comparison objects 
            created.
    """
    
    # kwargs passed to the parsed series of class fss.FarseerSeries
    comp_kwargs = series_kwargs(fsuv, rt=resonance_type)
    
    # ORDERED relation between dimension names
    # self: [next, prev]
    series_dim_keys = {'cond1':['cond2','cond3'],
                       'cond2':['cond3','cond1'],
                       'cond3':['cond1','cond2']}
    
    # stores all the comparison variables.
    comp_dct = {}
    
    # creates a Comparison object for each dimension that was evaluated
    # previously with fsuv.do_cond1, fsuv.do_cond2, fsuv.do_cond3
    for dimension in sorted(series_dct.keys()):
        # sends, cond1, cond2 and cond3.
        # DO
        
        # creates comparison
        c = fsc.Comparisons(series_dct[dimension].copy(),
                        selfdim=dimension,
                        other_dim_keys=series_dim_keys[dimension])
        
        c.log_export_onthefly = True
        c.log_export_name = fsuv.logfile_name
        ###
                
        # stores comparison in a dictionary
        comp_dct.setdefault(dimension, c)
        
        # generates set of PARSED FarseerSeries along the
        # next and previous dimensions
        c.gen_next_dim(fss.FarseerSeries, comp_kwargs)
        
        if c.has_points_next_dim:
            for dp2 in sorted(c.all_next_dim.keys()):
                
                for dp1 in sorted(c.all_next_dim[dp2].keys()):
                    
                    # writes log
                    c.all_next_dim[dp2][dp1].log_r(\
                        'COMPARING... [{}][{}] - [{}]'.format(\
                            dp2, dp1, list(c.hyper_panel.labels)),
                        istitle=True)
                    
                    # performs ploting routines
                    comparison_analysis_routines(\
                        c.all_next_dim[dp2][dp1],
                        fsuv, resonance_type)
                    
                    #c.log += c.all_next_dim[dim2_pt][dim1_pt].log
        
        c.gen_prev_dim(fss.FarseerSeries, comp_kwargs)
        
        if c.has_points_prev_dim:
            for dp2 in sorted(c.all_prev_dim.keys()):
                
                for dp1 in sorted(c.all_prev_dim[dp2].keys()):
                    
                    # writes log
                    c.all_prev_dim[dp2][dp1].log_r(\
                        'COMPARING... [{}][{}] - [{}]'.format(\
                            dp2, dp1, list(c.hyper_panel.cool)),
                        istitle=True)
                    
                    comparison_analysis_routines(\
                        c.all_prev_dim[dp2][dp1],
                        fsuv, resonance_type)
                    #c.log += c.allCcool[dim2_pt][dim1_pt].log
        
    return comp_dct

def run_farseer(fsuv):
    """
    Runs the whole Farseer-NMR standard algorithm.
    
    Args:
        fsuv (module): contains user defined variables (preferences) after
            .read_user_variables().
    """
    
    # Initiates the log
    log_time_stamp(fsuv.logfile_name, mod='w')
    
    # performs initial checks
    initial_checks(fsuv)
    
    # Initiates Farseer
    exp = creates_farseer_dataset(fsuv)
        
    # reads input
    reads_peaklists(exp, fsuv)
    
    #inits_coords_names(exp)
    
    # identify residues
    identify_residues(exp)
    
    # corrects chemical shifts
    if fsuv.perform_cs_correction:
        correct_shifts(exp, fsuv, resonance_type='Backbone')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            correct_shifts(exp, fsuv, resonance_type='Sidechains')
    
    # expands lost residues to other dimensions
    if fsuv.expand_lost_yy:
        expand_lost(exp, dim='y')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            expand_lost(exp, dim='y', resonance_type='Sidechains')
    
    if fsuv.expand_lost_zz:
        expand_lost(exp, dim='z')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            expand_lost(exp, dim='z', resonance_type='Sidechains')
    
    ## identifies lost residues
    add_missing(exp, peak_status='lost')
    
    if exp.has_sidechains and fsuv.use_sidechains:
        add_missing(exp, peak_status='lost', resonance_type='Sidechains')
    
    # adds fasta
    if fsuv.applyFASTA:
        add_missing(exp, peak_status='unassigned')
    
    #organize peaklist columns
    organize_columns(exp, fsuv)
    
    if exp.has_sidechains and fsuv.use_sidechains:
        organize_columns(exp, fsuv, resonance_type='Sidechains')
    
    init_fs_cube(exp, fsuv)
    
    # initiates a dictionary that contains all the series to be evaluated
    # along all the conditions.
    farseer_series_dct = \
        gen_series_dcts(exp, fss.FarseerSeries, fsuv,
                        resonance_type='Backbone')
    
    if not(farseer_series_dct):
        exp.exports_parsed_pkls()
    else:
        # evaluates the series and plots the data
        eval_series(farseer_series_dct, fsuv)
    
    if exp.has_sidechains and fsuv.use_sidechains:
        # DO
        farseer_series_SD_dict = \
            gen_series_dcts(exp, fss.FarseerSeries, fsuv,
                                resonance_type='Sidechains')
        
        if (farseer_series_SD_dict):
            eval_series(farseer_series_SD_dict, fsuv,
                        resonance_type='Sidechains')
        # DONE
    
    # Representing the results comparisons
    if fsuv.perform_comparisons and (farseer_series_dct):
        
        # analyses comparisons.
        comparison_dict = \
            analyse_comparisons(farseer_series_dct,
                                fsuv,
                                resonance_type='Backbone')
        
    if (fsuv.perform_comparisons and farseer_series_dct) and \
        (exp.has_sidechains and fsuv.use_sidechains):
        # DO
        comparison_dict_SD = \
            analyse_comparisons(farseer_series_SD_dict,
                                fsuv,
                                resonance_type='Sidechains')
        # DONE
    
    
    logs(fsw.end_good(), fsuv.logfile_name)
    log_time_stamp(fsuv.logfile_name, state='ENDED')
    
    return

if __name__ == '__main__':
    
    fsuv = read_user_variables(sys.argv[1])
    
    copy_Farseer_version(fsuv)
    
    # path evaluations now consider the absolute path, always.
    # in this way the user can run farseer from any folder taking the
    # input from any other folder.
    # path should be the folder where the 'spectra/' are stored and NOT the
    # path to the 'spectra/' folder.
    # if running from the actual folder, use:
    # $ python farseer_main.py .
    
    run_farseer(fsuv)
    
    print('Farseermain.py finished with __name__ == "__main__"')
