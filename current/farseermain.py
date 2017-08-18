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
    Reads user defined variables from file.
    
    And configures user variables necessary for farseermain.
    """
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    # IMPORTING FARSEER USER VARIABLES FROM CALCULATION DIR
    # I placed this here as a draft to make it work for now.
    # Simon: for sure with the JSON you will make it work differently :-P
    cwd =  os.path.abspath(path)
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
    
    #fsuv.general_plot_params = [fsuv.tplot_general_dict,
    #                            fsuv.bar_plot_general_dict,
    #                            fsuv.bar_ext_par_dict,
    #                            fsuv.comp_bar_par_dict,
    #                            fsuv.revo_plot_general_dict, 
    #                            fsuv.res_evo_par_dict,
    #                            fsuv.cs_scatter_par_dict,
    #                            fsuv.cs_scatter_flower_dict]
    # 
    #fsuv.pre_plot_params = [fsuv.heat_map_dict, fsuv.delta_osci_dict]
    
    
    return fsuv

def copy_Farseer_version(cwd, file_name='farseer_version',
                              compress_type='zip'):
    """Makes a copy of the running version."""
    
    script_wd = os.path.dirname(os.path.realpath(__file__))
    shutil.make_archive('{}/{}'.format(cwd, file_name),
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
    """Prints <s> and writes it to log file."""
    print(s)
    
    with open(logfile_name, mod) as logfile:
        logfile.write(s)
    
    return

def initial_checks(fsuv):
    """
    Performs checks that are useful to be executed at the beginning of the
    Farseer-NMR calculation run.
    
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
    
    Depends on:
    fsuv.PRE_analysis_flags
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
           
        logs(fsw.gen_wet('WARNING', msg, 1), fsuv.logfile_name)
        fsw.continue_abort()
        #DONE
    return

def checks_cube_axes_flags(fsuv):
    """
    Checks if the user wants to perform any analysis
    on the Farseer-NMR Cube.
    
    Depends on:
    fsuv.any_axis
    """
    if not(fsuv.any_axis):
        # DO
        msg = "Analysis over X, Y or Z Farseer-NMR Cube's axes are all deactivated. There is nothing to calculate. Confirm this is actually what you want."
        
        exp.log_r(fsw.gen_wet('NOTE', msg, 2))
        # DONE
    return

def checks_plotting_flags(fsuv):
    """Checks whether any plotting flag is activated."""
    
    if not(fsuv.plotting_flags):
        # DO ++++ export calculation tables
        for restraint in fsuv.restraint_settings.index:
        # if the user calculated this restraint
            if fsuv.restraint_settings.loc[restraint,'calcs_restraint_flg']:
                farseer_series.write_table(restraint,
                                            restraint,
                                            resonance_type=resonance_type)
        
        msg = "All potting flags are turned off. No plots will be drawn. Confirm in the Settings menu if this is the desired configuration. I won't leave you with empty hands though, all calculated restraints have been exported in nicely formated tables ;-)"
        
        farseer_series.log_r(fsw.gen_wet('NOTE', msg, 3))
        # DONE ++++
    
    return

def checks_calculation_flags(fsuv):
    """Checks if the user wants to calculate any restraints."""
    ######## WET#14
    if not(fsuv.calc_flags):
        #DO
        msg = "All restraints calculation routines are deactivated. Nothing will be calculated."
        
        logs(fsw.gen_wet('WARNING', msg, 14), fsuv.logfile_name)
        #DONE
    ########
    return

def checks_fit_input(series, fsuv):
    """Checks whether required fit data and settings are provided correctly."""
    
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
    
    Depends on:
    fsuv.spectra_path
    fsuv.has_sidechains
    fsuv.FASTAstart
    fsuv.logfile_name
    """
    exp = fcube.FarseerCube(fsuv.spectra_path,
                            fsuv.has_sidechains,
                            fsuv.FASTAstart)
    
    exp.log_export_onthefly = True
    exp.log_export_name = fsuv.logfile_name
    
    return exp

def reads_peaklists(exp, fsuv):
    """
    Loads Peaklist's Tree.
    
    Depends on:
    fsuv.applyFASTA
    """
    
    exp.load_experiments(target=exp.allpeaklists)
    
    if fsuv.applyFASTA:
        exp.load_experiments(target=exp.allFASTA,
                                    f=exp.read_FASTA,
                                    filetype='.fasta')
    
    # even if the user does no want to analyse sidechains, Farseer-NMR
    # has to parse them out from the input peaklist if they exist
    if exp.has_sidechains:
        # str() is passed as a dummy function
        exp.load_experiments(target=exp.allsidechains,
                                    f=str,
                                    filetype='.csv')
    return

def inits_coords_names(exp):
    """Initiates coordinate names of the Farseer-NMR Cube Axes."""
    exp.init_coords_names()
    return
    
def identify_residues(exp):
    """
    Reads Assignment information and generates split
    columns with information on residue number, and aminoacid
    1 and 3 letter code.
    """
    exp.tricicle(exp.zzcoords,
                 exp.yycoords,
                 exp.xxcoords,
                 exp.split_res_info,
                 title=\
                    'IDENTIFIES RESIDUE INFORMATION FROM ASSIGNMENT COLUMN')
    
    return

def correct_shifts(exp, fsuv, resonance_type='Backbone'):
    """
    Corrects chemical shifts for all the peaklists to a reference peak
    in the (0,0,0) Farseer-NMR Cube coordinate.
    
    Depends on:
    fsuv.cs_correction_res_ref
    """
    
    if resonance_type == 'Backbone':
        ctitle = 'CORRECTS BACKBONE CHEMICAL SHIFTS BASED ON A REFERENCE PEAK'
        exp.tricicle(exp.zzcoords, 
                     exp.yycoords, 
                     exp.xxcoords, 
                     exp.correct_shifts_backbone,
                     kwargs={'ref_res':str(fsuv.cs_correction_res_ref)},
                     title=ctitle)
    
    elif resonance_type=='Sidechains':
        ctitle = \
            'CORRECTS SIDECHAINS CHEMICAL SHIFTS BASED ON A REFERENCE PEAK'
        exp.tricicle(exp.zzcoords, 
                     exp.yycoords, 
                     exp.xxcoords, 
                     exp.correct_shifts_sidechains,
                     title=ctitle)
    return

def fill_na(peak_status, merit=0, details='None'):
    """
    A dictionary that configures how the fields of the
    added rows for missing residues are fill.
    """
    d = {
    'Peak Status': peak_status,
    'Merit': merit,
    'Details': details
    }
    return d

def expand_lost(exp, dataset_dct, acoords, bcoords, refcoord, dim='z'):
    """
    Compares reference peaklists along Y and Z axis of the Farseer-NMR
    Cube and generates the corresponding 'lost' residues.
    This function is useful when analysing dia/ and paramagnetic/ series
    along the Z axis.
    """
    
    if dim == 'y':
        exp.log_r(\
        'EXPANDS LOST RESIDUES TO CONDITIONS {}'.format(dim.upper()),
        istitle = True)
        # expands to yy (cond2) condition
        for a in acoords:
            #do
            for b in bcoords:
                #do
                refscoords = {'z': a, 'y': refcoord}
                exp.seq_expand(a, b, exp.xxref, 'expanding',
                               dataset_dct, 
                               dataset_dct,
                               fill_na_lost('lost'),
                               refscoords=refscoords)
    if dim == 'z':
        exp.log_r(\
        'EXPANDS LOST RESIDUES TO CONDITIONS {}'.format(dim.upper()),
        istitle = True)
        # expands to yy (cond2) condition
        for a in acoords:
            #do
            for b in bcoords:
                #do
                refscoords = {'z': refcoord, 'y': a}
                exp.seq_expand(b, a, exp.xxref, 'expanding',
                               dataset_dct, 
                               dataset_dct,
                               fill_na('lost'),
                               refscoords=refscoords)
    
    
    return

def add_lost(exp, reference, target,
             peak_status='lost',
             ref='REFERENCE',
             kwargs={}):
    """
    Uses seq_expand method of FarseerSet.py.
    Expands a <target> peaklist to the index of a <reference> peaklist.
    """
    
    ctitle = 'ADDS LOST RESIDUES BASED ON THE {}'.format(ref)
    
    exp.tricicle(exp.zzcoords, exp.yycoords, exp.xxcoords, exp.seq_expand,
                 args=[reference, target, fill_na(peak_status)],
                 kwargs=kwargs,
                 title=ctitle)
    
    return

def organize_columns(exp, dataset_dct, fsuv,
                     sidechains=False):
    """
    Uses FarseerSet.organize_cols().
    
    Depends on:
    fsuv.perform_cs_correction
    """
    
    ctitle = "ORGANIZING PEAKLIST COLUMNS' ORDER"
    exp.tricicle(exp.zzcoords, exp.yycoords, exp.xxcoords, 
                 exp.organize_cols,
                 args=[dataset_dct],
                 kwargs={'performed_cs_correction':fsuv.perform_cs_correction,
                         'sidechains':sidechains},
                 title=ctitle)
    
    return

def init_fs_cube(exp, fsuv):
    """
    Inits Farseer-NMR Cube.
    The cube is stored as a variable of the FarseerSet class.
    
    Depends on:
    fsuv.use_sidechains
    """
    exp.init_Farseer_cube(use_sidechains=fsuv.use_sidechains)
    
    return

def series_kwargs(fsuv, rt='Backbone'):
    """
    Defines the kwargs dictionary that will be used to generate
    the Titration class object based on the user defined preferences.
    
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
    Returns a nested dictionary <D> that contains all the series
    to be evaluated along all the conditions.
    
    <D> contains a first level key for each Farseer-NMR Cube's axis.
    Each of these keys contains a second nested dictionary enclosing
    all the experimental series along that axis as extracted from
    the Farseer-NMR Cube.
    
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
    
    :series_class: The class that will initiate the series, normally
                   fslibs/FarseerSeries.py
    
    Depends on:
    fsuv.do_cond1
    fsuv.do_cond2
    fsuv.do_cond3
    """
    
    checks_cube_axes_flags(fsuv)
    
    # initiates dictionary
    series_dct = {}
    
    if fsuv.any_axis:
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
    
    :series_dct: the dictionary containing all the series of an axis.
    :fsuv: a module containing all the variables.
    :resonance_type: whether the data corresponds to backbone or sidechain
                 resonances.
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
    
    Depends on:
    fsuv.perform_resevo_fit
    fsuv.restraint_settings
    fsuv.txv
    """
    # runs only for CSPs, 1H and 15N.
    
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
    Performs dedicated PRE analysis on the cond3 dimension.
    """
    # if user do not wants PRE analysis, do nothing
    if not(fsuv.apply_PRE_analysis):
        return
    # if analysing cond3: performs calculations.
    if farseer_series.series_axis == 'cond3':
        farseer_series.load_theoretical_PRE(fsuv.spectra_path,
                                             farseer_series.dim2_pts)
        
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
                and (farseer_series.dim2_pts == 'para'\
                    or farseer_series.dim1_pts == 'para')):
        
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
        and (farseer_series.dim2_pts == 'para' \
            or farseer_series.dim1_pts == 'para'):
        
        
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
    farseer_series.export_series_to_tsv()
    return

def exports_chimera_att_files(farseer_series, fsuv):
    """
    Exports tables with calculated restraints.
    
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
    An algorythm that receives an experimental series and 
    walks through the plotting routines.
    
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
    # checks if there are any plot flags activated
    # and if not outputs eh respective message.
    
    checks_plotting_flags(fsuv)
        
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
                        restraint_settings.loc[restraint,
                                                 'plt_y_axis_scl'],
                        ylabel=\
                        restraint_settings.loc[restraint,
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

def analyse_comparisons(exp, series_dct, fsuv,
                        gpp=[],
                        ppp=[],
                        ps=[],
                        resonance_type='Backbone'):
    """Algorythm to perform data comparisons over analysed conditions."""
    
    def run_comparative(comp_panel):
        # EXPORTS FULLY PARSED PEAKLISTS
        exports_titration(comp_panel)
    
        # EXPORTS CALCULATIONS
        exports_data_tables(comp_panel, restraint_settings=ps, fsuv=fsuv)
        
        # performs pre analysis
        PRE_analysis(comp_panel, fsuv, gpp[0], *ppp, restraint_settings=ps)
        
        # plots data
        plots_data(comp_panel, fsuv, *gpp, restraint_settings=ps)
        
        return
        
    series_dim_keys = {'cond1':['cond2','cond3'],
                          'cond2':['cond3','cond1'],
                          'cond3':['cond1','cond2']}
    
    cp = {} # dictionary stored comparisons over dimensions
    
    for dimension in sorted(series_dct.keys()):
        # this send, cond1, cond2, cond3 ...
        c = fsc.Comparisons(series_dct[dimension].copy(),
                        selfdim=dimension,
                        other_dim_keys=series_dim_keys[dimension],
                        resonance_type=resonance_type)
        
        # stores comparison in a dictionary
        cp.setdefault(dimension, c)
        
        c.gen_comparison_labels(fst.Titration)
        
        #print(c.allClabels)
        #input('dimension {}'.format(dimension))
        
        if c.haslabels:
            for dim2_pt in sorted(c.allClabels.keys()):
                
                for dim1_pt in sorted(c.allClabels[dim2_pt].keys()):
                    
                    c.allClabels[dim2_pt][dim1_pt].log_t('COMPARING...',
                                                         istitle=True)
                    
                    run_comparative(c.allClabels[dim2_pt][dim1_pt])
                    
                    c.log += c.allClabels[dim2_pt][dim1_pt].log
        
        c.gen_comparison_cool(fst.Titration)
        
        if c.hascool:
            for dim2_pt in sorted(c.allCcool.keys()):
                
                for dim1_pt in sorted(c.allCcool[dim2_pt].keys()):
                    c.allCcool[dim2_pt][dim1_pt].log_r('COMPARING...',
                                                       istitle=True)
                    run_comparative(c.allCcool[dim2_pt][dim1_pt])
                    c.log += c.allCcool[dim2_pt][dim1_pt].log
        
    return cp

def run_farseer(fsuv):
    """
    Runs the whole Farseer-NMR standard algorithm.
    
    Depends on:
    fsuv, a module containing all the required variables.
    """
    
    # Initiates the log
    log_time_stamp(fsuv.logfile_name, mod='w')
    
    # performs initial checks
    initial_checks(fsuv)
    
    # Initiates Farseer
    exp = creates_farseer_dataset(fsuv)
        
    # reads input
    reads_peaklists(exp, fsuv)
    
    inits_coords_names(exp)
    
    # identify residues
    identify_residues(exp)
    
    # corrects chemical shifts
    if fsuv.perform_cs_correction:
        correct_shifts(exp, fsuv, resonance_type='Backbone')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            correct_shifts(exp, fsuv, resonance_type='Sidechains')
    
    # expands lost residues to other dimensions
    if fsuv.expand_lost_yy:
        expand_lost(exp, exp.allpeaklists, exp.zzcoords, exp.yycoords,
                    exp.yyref, dim='y')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            expand_lost(exp, exp.allsidechains, exp.zzcoords, exp.yycoords,
                        exp.yyref, dim='y')
    
    if fsuv.expand_lost_zz:
        expand_lost(exp, exp.allpeaklists, exp.yycoords, exp.zzcoords,
                    exp.zzref, dim='z')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            expand_lost(exp, exp.allsidechains, exp.yycoords, exp.zzcoords,
                        exp.zzref, dim='z')
    
    ## identifies lost residues
    add_lost(exp, exp.allpeaklists, exp.allpeaklists,
             peak_status='lost',
             ref='REFERENCE')
    
    if exp.has_sidechains and fsuv.use_sidechains:
        add_lost(exp, exp.allsidechains, exp.allsidechains,
                       peak_status='lost',
                       ref='REFERENCE FOR SIDECHAINS',
                       kwargs={'resonance_type':'Sidechain'})
    
    # adds fasta
    if fsuv.applyFASTA:
        add_lost(exp, exp.allFASTA, exp.allpeaklists,
                 peak_status='unassigned', ref='FASTA')
    
    #organize peaklist columns
    organize_columns(exp, exp.allpeaklists, fsuv)
    
    if exp.has_sidechains and fsuv.use_sidechains:
        organize_columns(exp, exp.allsidechains, fsuv,
                         sidechains=True)
    
    init_fs_cube(exp, fsuv)
    
    # initiates a dictionary that contains all the series to be evaluated
    # along all the conditions.
    farseer_series_dct = \
        gen_series_dcts(exp, fss.FarseerSeries, fsuv,
                            resonance_type='Backbone')
    
    # evaluates the series and plots the data
    eval_series(farseer_series_dct, fsuv)
    
    if exp.has_sidechains and fsuv.use_sidechains:
        # DO
        farseer_series_SD_dict = \
            gen_series_dcts(exp, fss.FarseerSeries, fsuv,
                                resonance_type='Sidechains')
        
        eval_series(farseer_series_SD_dict,
                        fsuv, resonance_type='Sidechains')
        # DONE
    
    # Representing the results comparisons
    if fsuv.perform_comparisons:
        
        # analyses comparisons.
        comparison_dict = \
            analyse_comparisons(exp,
                                farseer_series_dct,
                                fsuv,
                                gpp=general_plot_params,
                                ps=restraint_settings,
                                ppp=pre_plot_params,
                                resonance_type='Backbone')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            comparison_dict_SD = \
                analyse_comparisons(exp,
                                    Farseer_SD_series_dct,
                                    fsuv,
                                    gpp=general_plot_params,
                                    ps=restraint_settings,
                                    ppp=pre_plot_params,
                                    resonance_type='Sidechains')
    
    
    logs(fsw.end_good(), fsuv.logfile_name)
    log_time_stamp(fsuv.logfile_name, state='ENDED')
    
    return

if __name__ == '__main__':
    
    fsuv = read_user_variables(sys.argv[1])
    
    copy_Farseer_version(fsuv.cwd)
    
    # path evaluations now consider the absolute path, always.
    # in this way the user can run farseer from any folder taking the
    # input from any other folder.
    # path should be the folder where the 'spectra/' are stored and NOT the
    # path to the 'spectra/' folder.
    # if running from the actual folder, use:
    # $ python farseer_main.py .
    
    run_farseer(fsuv)
    
    print('Farseermain.py finished with __name__ == "__main__"')
