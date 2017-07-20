#  
import importlib.util
import sys
import os
import shutil
import datetime  # used to write the log file
import pandas as pd
#farseer_user_variables are imported in the if __main__ :
from current06.fslibs import FarseerSet as fset
from current06.fslibs import Titration as fst
from current06.fslibs import Comparisons as fsc
from current06.fslibs import wet as fsw

def read_user_variables(path):
    """
    Reads user defined variables from file.
    """
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    return fsuv, cwd

def copy_Farseer_version(cwd, file_name='farseer_version',
                         compress_type='zip'):
    """MAKES COPY OF THE RUNNING VERSION"""
    
    script_wd = os.path.dirname(os.path.realpath(__file__))
    shutil.make_archive('{}/{}'.format(cwd, file_name),
                        compress_type,
                        script_wd)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    return 

def init_log(logfile_name, mod='a', state='STARTED'):
    """Starts the log file."""
    log_title = \
        '{0}  \n**LOG {2}:** {1} \n{0}  \n'.\
            format(79*'*',
                   datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"),
                   state)
    
    with open(logfile_name, mod) as logfile:
        logfile.write(log_title)
    return

def close_log(farseerset=False, 
              backbone_titration=False,
              sidechain_titration=False,
              backbone_comparison=False,
              sidechain_comparison=False,
              logfile_name='farseer.log',
              mod='a'):
    
    def tdictcycle(td):
        """:td: titration dictionary"""
        for cond in sorted(td.keys()):
            # for each point in the corresponding second dimension/condition
            for dim2_pt in sorted(td[cond].keys()):
                # for each point in the corresponding first dimension/condition
                for dim1_pt in sorted(td[cond][dim2_pt].keys()):
                    
                    td[cond][dim2_pt][dim1_pt].\
                        write_log(mod=mod, path=logfile_name)
        return
    
    
    if farseerset:
        farseerset.write_log(mod=mod, path=logfile_name)
    
    if backbone_titration:
        tdictcycle(backbone_titration)
    
    if sidechain_titration:
        tdictcycle(sidechain_titration)
    
    if backbone_comparison:
        for cond in sorted(backbone_comparison.keys()):
            #backbone_comparison[cond].transfer_log()
            backbone_comparison[cond].write_log(mod=mod, path=logfile_name)
    
    if sidechain_comparison:
        for cond in sorted(sidechain_comparison.keys()):
            #sidechain_comparison[cond].transfer_log()
            sidechain_comparison[cond].write_log(mod=mod, path=logfile_name)
    
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    init_log(logfile_name, state='ENDED')
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    return

def init_params(fsuv):
    """Reads user defined variables and converts them to 
    organized dicitonaries or DataFrames.
    """
    
    if fsuv.apply_PRE_analysis \
        and not(fsuv.do_cond3 \
                and (fsuv.calcs_Height_ratio or fsuv.calcs_Volume_ratio) \
                and fsuv.perform_comparisons):
        #DO
        fsw.wet1(fsuv.apply_PRE_analysis, fsuv.do_cond3,
                 fsuv.calcs_Height_ratio, fsuv.calcs_Volume_ratio,
                 fsuv.perform_comparisons)
        pass
    
    general_variables = {}
    general_variables['txv'] = sorted(fsuv.titration_x_values)
    
    
    calculated_params = [fsuv.calccol_name_PosF1_delta,
                     fsuv.calccol_name_PosF2_delta,
                     fsuv.calccol_name_CSP,
                     fsuv.calccol_name_Height_ratio,
                     fsuv.calccol_name_Volume_ratio
                    ]


    param_settings_d = {
    'plot_param_flag':    [fsuv.calcs_PosF1_delta,
                           fsuv.calcs_PosF2_delta,
                           fsuv.calcs_CSP,
                           fsuv.calcs_Height_ratio,
                           fsuv.calcs_Volume_ratio],
                           
    'plot_yy_axis_label': [fsuv.yy_label_PosF1_delta,
                           fsuv.yy_label_PosF2_delta,
                           fsuv.yy_label_CSP,
                           fsuv.yy_label_Height_ratio,
                           fsuv.yy_label_Volume_ratio],
                           
    'plot_yy_axis_scale': [(-fsuv.yy_scale_PosF1_delta, fsuv.yy_scale_PosF1_delta),
                           (-fsuv.yy_scale_PosF2_delta, fsuv.yy_scale_PosF2_delta),
                           (0, fsuv.yy_scale_CSP),
                           (0, fsuv.yy_scale_Height_ratio),
                           (0, fsuv.yy_scale_Volume_ratio)]
                           }
    
    # An array of settings that are local for each parameter
    # the index of this dataframe are the calculated parameters.
    param_settings = pd.DataFrame(param_settings_d, index=calculated_params)
    
    
    tplot_general_dict = {
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
    
    bar_plot_general_dict = {
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
    
    bar_ext_par_dict = {
        'x_ticks_fn':fsuv.ext_bar_x_ticks_fn,
        'x_ticks_fs':fsuv.ext_bar_x_ticks_fs,
        'x_ticks_rot':fsuv.ext_bar_x_ticks_rot,
        'x_ticks_weight':fsuv.ext_bar_x_ticks_weight,
        'x_ticks_color_flag':fsuv.ext_bar_x_ticks_color_flag
        }
    
    comp_bar_par_dict = {
        'x_ticks_fn':fsuv.comp_bar_x_ticks_fn,
        'x_ticks_fs':fsuv.comp_bar_x_ticks_fs,
        'x_ticks_rot':fsuv.comp_bar_x_ticks_rot,
        'x_ticks_weight':fsuv.comp_bar_x_ticks_weight,
        'unassigned_shade':fsuv.comp_bar_unassigned_shade,
        'unassigned_shade_alpha':fsuv.comp_bar_unassigned_shade_alpha
        }
    
    revo_plot_general_dict = {
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
    
    res_evo_par_dict = {
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
        'titration_x_values':general_variables['txv']
        }
    
    cs_scatter_par_dict = {
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
    
    cs_scatter_flower_dict = {
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
    
    heat_map_dict = {
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
    
    delta_osci_dict = {
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
    
    general_plot_params = [tplot_general_dict,
                                   bar_plot_general_dict,
                                   bar_ext_par_dict,
                                   comp_bar_par_dict,
                                   revo_plot_general_dict, 
                                   res_evo_par_dict,
                                   cs_scatter_par_dict,
                                   cs_scatter_flower_dict]
    
    pre_plot_params = [heat_map_dict,
                       delta_osci_dict]
    
    
    return calculated_params, param_settings,\
           general_plot_params, pre_plot_params, general_variables

def init_farseer(path, has_sidechains=False, FASTAstart=1):
    '''Initiates the Farseer data set.'''
    exp = fset.FarseerSet(path,
                          has_sidechains=has_sidechains,
                          FASTAstart=FASTAstart)
    
    return exp

def reads_input(exp, fsuv):
    """Loads the tree of peaklists."""
    
    exp.load_experiments(target=exp.allpeaklists)
    
    if fsuv.applyFASTA:
        exp.load_experiments(target=exp.allFASTA,
                                    f=exp.read_FASTA,
                                    filetype='.fasta')
    
    if exp.has_sidechains:
        # str() is passed as a dummy function
        exp.load_experiments(target=exp.allsidechains,
                                    f=str,
                                    filetype='.csv')
    return

def inits_conditions(exp):
    exp.init_conditions()
    return
    
def identify_residues(exp):
    '''
    Reads Assignment information and generates split
    columns with information on residue number, and aminoacid
    1 and 3 letter code.
    '''
    exp.tricicle(exp.zzcoords,
                 exp.yycoords,
                 exp.xxcoords,
                 exp.split_res_info,
                 title=\
                    'IDENTIFIES RESIDUE INFORMATION FROM ASSIGNMENT COLUMN')
    
    return

def correct_shifts(exp, res_ref=1, reso_type='Backbone'):
    
    if reso_type == 'Backbone':
        ctitle = 'CORRECTS BACKBONE CHEMICAL SHIFTS BASED ON A REFERENCE PEAK'
        exp.tricicle(exp.zzcoords, 
                     exp.yycoords, 
                     exp.xxcoords, 
                     exp.correct_shifts_backbone,
                     kwargs={'ref_res':str(res_ref)},
                     title=ctitle)
    
    elif reso_type=='Sidechains':
        ctitle = \
            'CORRECTS SIDECHAINS CHEMICAL SHIFTS BASED ON A REFERENCE PEAK'
        exp.tricicle(exp.zzcoords, 
                     exp.yycoords, 
                     exp.xxcoords, 
                     exp.correct_shifts_sidechains,
                     title=ctitle)
    return

def fill_na_lost(peak_status):
    """
    A dictionary that configures how the fields of the
    lost residues are fill.
    """
    d = {
    'Peak Status': peak_status,
    'Merit': 0,
    'Details': 'None'
    }
    return d

def expand_lost(exp, titration_set, acoords, bcoords, refcoord, dim='z'):
    """
    Expands lost residues for the reference experiments
    over the other conditions of the titration.
    """
    
    
    if dim == 'y':
        exp.log_t(\
        'EXPANDS LOST RESIDUES TO CONDITIONS {}'.format(dim.upper()))
        # expands to yy (cond2) condition
        for a in acoords:
            #do
            for b in bcoords:
                #do
                refscoords = {'z': a, 'y': refcoord}
                exp.seq_expand(a, b, exp.xxref, 'expanding',
                               titration_set, 
                               titration_set,
                               fill_na_lost('lost'),
                               refscoords=refscoords)
    if dim == 'z':
        exp.log_t(\
        'EXPANDS LOST RESIDUES TO CONDITIONS {}'.format(dim.upper()))
        # expands to yy (cond2) condition
        for a in acoords:
            #do
            for b in bcoords:
                #do
                refscoords = {'z': refcoord, 'y': a}
                exp.seq_expand(b, a, exp.xxref, 'expanding',
                               titration_set, 
                               titration_set,
                               fill_na_lost('lost'),
                               refscoords=refscoords)
    
    
    return

def add_lost(exp, refdata, targetdata,
             peak_status='lost',
             ref='REFERENCE',
             kwargs={}):
    """Adds lots residues to the peaklists based on a reference.
    """
    
    ctitle = 'ADDS LOST RESIDUES BASED ON THE {}'.format(ref)
    
    exp.tricicle(exp.zzcoords, exp.yycoords, exp.xxcoords, exp.seq_expand,
                 args=[refdata, targetdata, fill_na_lost(peak_status)],
                 kwargs=kwargs,
                 title=ctitle)
    
    return

def organize_columns(exp, titration_set,
                     performed_cs_correction=False,
                     scbool=False):
    """Organizes the columns order."""
    ctitle = "ORGANIZING PEAKLIST COLUMNS' ORDER"
    exp.tricicle(exp.zzcoords, exp.yycoords, exp.xxcoords, 
                 exp.organize_cols,
                 args=[titration_set],
                 kwargs={'performed_cs_correction':performed_cs_correction,
                         'sidechains':scbool},
                 title=ctitle)
    
    return

def init_fs_cube(exp, sidechains=False):
    """
    Generates a 5 dimension cube containing all the information
    of the titration experiment set. The cube is stored
    as a variable of the FarseerSet class.
    """
    exp.init_Farseer_cube(use_sidechains=sidechains)
    
    return

def titration_kwargs(fsuv, rt='Backbone', cp=None):
    """
    Defines the kwargs dictionary that will be used to generate
    the Titration class object. The aim of this dictionary
    is to avoid fst.Titration to import anything from
    farseer_user_variables.
    """
    dd = {'resonance_type':rt,
          'csp_alpha4res':fsuv.csp_alpha4res,
          'csp_res_exceptions':fsuv.csp_res_exceptions,
          'cs_lost':fsuv.cs_lost,
          'calculated_params':cp}
    
    return dd

def gen_titration_dicts(exp, data_hyper_cube,
                        cond1=False,
                        cond2=False,
                        cond3=False,
                        titration_class=None,
                        titration_kwargs={}):
    """
    Returns a dictionary containing all the titrations to be analysed.
    
    primary keys: 'cond1', 'cond2', 'cond3'.
    
    :exp: the FarseerSet object with all the titration data
    :data_hyper_cube: the 5D cube with all the titration data
    :reso_type: default:'Backbone', labels the data according
                to its resonance of origin (Backbone or Sidechain).
    """
    
    # to facilitate the analysis with for loops, all the different
    # titrations experiments we are going to analyse will be stored 
    # in a dictionary
    titrations_dict = {}

    # creates the titrations for the first condition (1D)
    if exp.hasxx and cond1:
        titrations_dict['cond1'] = \
            exp.gen_titration_dict(\
                                data_hyper_cube,
                                'cond1', 
                                exp.xxcoords,
                                exp.yycoords,
                                exp.zzcoords,
                                titration_class,
                                titration_kwargs)
    
    # creates the titrations for the second condition (2D)
    if exp.hasyy and cond2:
        titrations_dict['cond2'] = \
            exp.gen_titration_dict(\
                                data_hyper_cube.transpose(2,0,1,3,4),
                                'cond2',
                                exp.yycoords,
                                exp.zzcoords,
                                exp.xxcoords,
                                titration_class,
                                titration_kwargs)

    # creates the titrations for the third condition (3D)  
    if exp.haszz and cond3:
        titrations_dict['cond3'] = \
            exp.gen_titration_dict(\
                                data_hyper_cube.transpose(1,2,0,3,4),
                                'cond3',
                                exp.zzcoords,
                                exp.xxcoords,
                                exp.yycoords,
                                titration_class,
                                titration_kwargs)
    
    if not(cond1 or cond2 or cond3):
        exp.tricicle(exp.zzcoords, exp.yycoords, exp.xxcoords,
                     exp.exports_parsed_pkls,
                     title='EXPORTED PARSED PEAKLISTS')
        exp.log_r(fsw.wet2(cond1, cond2, cond3))
    
    return titrations_dict

def eval_titrations(titration_dict,
                    fsuv,
                    general_variables,
                    spectra_path='spectra/',
                    atomtype='Backbone',
                    param_settings = [],
                    general_plot_params = [],
                    pre_plot_params = []):
    """
    Executes a set of functions for each titration panel
    navigating throught the nested for loop cycle accross the three
    titration conditions.
    
    :titration_dict: the dictionary containing the information of all
                     the titrations to be analysed.
    :sidechains: whether the data analysis corresponds to sidechain
                 resonances.
    """
    
    # for each kind of titration (cond{1,2,3})
    for cond in sorted(titration_dict.keys()):
        # for each point in the corresponding second dimension/condition
        
        for dim2_pt in sorted(titration_dict[cond].keys()):
            # for each point in the corresponding first dimension/condition
            for dim1_pt in sorted(titration_dict[cond][dim2_pt].keys()):
                titration_dict[cond][dim2_pt][dim1_pt].log_t('ANALYZING... ')
                # DO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # performs the calculations
                perform_calcs(titration_dict[cond][dim2_pt][dim1_pt],
                              fsuv)
                
                # PERFORMS FITS
                perform_fits(titration_dict[cond][dim2_pt][dim1_pt],
                             param_settings=param_settings,
                             txv=general_variables['txv'])
                
                # Analysis of PRE data - only in cond3
                PRE_analysis(titration_dict[cond][dim2_pt][dim1_pt],
                             fsuv,
                             general_plot_params[0],
                             *pre_plot_params,
                             param_settings=param_settings,
                             spectra_path=spectra_path)
                
                # EXPORTS FULLY PARSED PEAKLISTS
                exports_titration(titration_dict[cond][dim2_pt][dim1_pt])
                
                # EXPORTS CALCULATIONS
                exports_data_tables(titration_dict[cond][dim2_pt][dim1_pt],
                                    param_settings=param_settings, fsuv=fsuv)
                
                # PLOTS TITRATION DATA
                plots_data(titration_dict[cond][dim2_pt][dim1_pt],
                           fsuv,
                           *general_plot_params,
                           param_settings=param_settings,
                           atomtype=atomtype)
                
                #DONE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                
    return

def perform_calcs(titration_panel, fsuv):
    """
    Calculates the NMR restraints according to the user specifications.
    """
    # if the user wants to calculate combined Chemical Shift Perturbations
    if fsuv.calcs_CSP:
        # calculate differences in chemical shift for each dimension
        titration_panel.calc_cs_diffs(fsuv.calccol_name_PosF1_delta,
                                      'Position F1')
        titration_panel.calc_cs_diffs(fsuv.calccol_name_PosF2_delta,
                                      'Position F2')
    
        # Calculates CSPs
        titration_panel.calc_csp(calccol=fsuv.calccol_name_CSP,
                                 pos1=fsuv.calccol_name_PosF1_delta,
                                 pos2=fsuv.calccol_name_PosF2_delta)
    
    # if the user only wants to calculate perturbation in single dimensions
    else:
        if fsuv.calcs_PosF1_delta:
            titration_panel.calc_cs_diffs(fsuv.calccol_name_PosF1_delta,
                                          'Position F1')
        if fsuv.calcs_PosF2_delta:
            titration_panel.calc_cs_diffs(fsuv.calccol_name_PosF2_delta,
                                          'Position F2')
    
    # Calculates Ratios
    if fsuv.calcs_Height_ratio:
        titration_panel.calc_ratio(fsuv.calccol_name_Height_ratio, 'Height')
    if fsuv.calcs_Volume_ratio:
        titration_panel.calc_ratio(fsuv.calccol_name_Volume_ratio, 'Volume')
    
    return

def perform_fits(titration_panel, param_settings=None, txv=[]):
    """Performs fits for 1H, 15N and CSPs data."""
    # runs only for CSPs, 1H and 15N.
    
    # *fits are allowed only to cond1 titrations
    if not(fsuv.perform_resevo_fit \
           and titration_panel.titration_type == 'cond1'):
        return
    
    # sanity check ############################################################
    try: 
        if not(all([False for x in txv if x<0])):
            titration_panel.log_r(fsw.wet6(txv))
            fsw.end_bad()
        elif set([(int(x)) for x in titration_panel.items]).\
            symmetric_difference(txv):
            #DO
            titration_panel.log_r(fsw.wet4(txv, titration_panel.items))
            choice = '.'
            while not(choice in ['U', 'A']):
                choice = input('=> type: [U]se cond1 variable \
names as x values or [A]bort: ').upper()
            if choice == 'U':
                txv = [(int(x)) for x in titration_panel.items]
                
            elif choice == 'A':
                titration_panel.log_r(fsw.end_bad())
    
    except SystemExit:
        titration_panel.log_r(fsw.end_bad())
    
    except:
        if len(txv) != len(titration_panel.items):
            titration_panel.log_r(fsw.wet5(txv, titration_panel.items))
            titration_panel.log_r(fsw.end_bad())
        else:
            titration_panel.log_r(fsw.wet7(txv))
    
    ###########################################################################
    
    for calculated_parameter in param_settings.index[:3]:
        
        if param_settings.loc[calculated_parameter, 'plot_param_flag']:
            
            titration_panel.perform_fit(calccol = calculated_parameter,
                                        x_values=txv)
    return

def PRE_analysis(titration_panel,
                 fsuv,
                 tplot_general_dict,
                 heat_map_dict,
                 delta_osci_dict,
                 param_settings=None,
                 spectra_path='spectra/'):
    """
    Performs dedicated PRE analysis on the cond3 dimension.
    Data can be represented under the calculations of cond3 or when
    <comparing> the data for 'C3'.
    """
    # if user do not wants PRE analysis, do nothing
    if not(fsuv.apply_PRE_analysis):
        return
    # if analysing cond3: performs calculations.
    if titration_panel.titration_type == 'cond3':
        titration_panel.load_theoretical_PRE(spectra_path,
                                             titration_panel.dim2_pts)
        
        for sourcecol, targetcol in zip(param_settings.index[3:],\
                                        ['Hgt_DPRE', 'Vol_DPRE']):
        
            # only in the parameters allowed by the user
            if param_settings.loc[sourcecol, 'plot_param_flag']:
                titration_panel.calc_Delta_PRE(sourcecol, targetcol,
                                         gaussian_stddev=fsuv.gaussian_stddev,
                                         guass_x_size=fsuv.gauss_x_size)
    
    # plots the calculated Delta_PRE and Delta_PRE_smoothed analsysis
    # for cond3 and for comparison C3.
    if titration_panel.titration_type == 'cond3' \
            or (titration_panel.titration_type == 'C3' \
                and (titration_panel.dim2_pts == 'para'\
                    or titration_panel.dim1_pts == 'para')):
        
        # do
        for sourcecol, targetcol in zip(list(param_settings.index[3:])*2,
                                        ['Hgt_DPRE',
                                         'Vol_DPRE',
                                         'Hgt_DPRE_smooth',
                                         'Vol_DPRE_smooth']):
            
            # only for the parameters allowed by the user
            if param_settings.loc[sourcecol, 'plot_param_flag']:
                
                titration_panel.plot_base(targetcol, 'exp', 'heat_map',
                    heat_map_dict,
                    par_ylims=\
                    param_settings.loc[sourcecol,'plot_yy_axis_scale'],
                    ylabel=\
                    param_settings.loc[sourcecol,'plot_yy_axis_label'],
                    cols_per_page=1,
                    rows_per_page=fsuv.heat_map_rows,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
    
    # plots the DeltaPRE oscilation analysis only for <C3> comparison.
    # because DeltaPRE oscilation represents the results obtained only
    # for paramagnetic ('para') data.
    if titration_panel.titration_type == 'C3' \
        and (titration_panel.dim2_pts == 'para' \
            or titration_panel.dim1_pts == 'para'):
        
        
        for sourcecol, targetcols in zip(param_settings.index[3:],
                                         ['Hgt_DPRE', 'Vol_DPRE']):
            if param_settings.loc[sourcecol, 'plot_param_flag']:
                titration_panel.plot_base(targetcols, 'exp', 'delta_osci',
                    {**tplot_general_dict,**delta_osci_dict},
                    par_ylims=(0,fsuv.dpre_osci_ymax),
                    ylabel=fsuv.dpre_osci_y_label,
                    cols_per_page=1,
                    rows_per_page=fsuv.dpre_osci_rows,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width/fsuv.dpre_osci_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
    
    
    return

def exports_titration(titration_panel):
    titration_panel.export_titration()
    return

def exports_data_tables(titration_panel,
                        param_settings=[],
                        fsuv=None):
    """Exports tables with calculated parameters."""
    
    for calculated_parameter in param_settings.index:
        # if the user wants to plot this parameter
        if param_settings.loc[calculated_parameter,'plot_param_flag']:
            # do export chimera attribute files
            titration_panel.write_Chimera_attributes(\
                    calculated_parameter,
                    resformat=fsuv.chimera_att_select_format)
    
    return

def plots_data(titration_panel, fsuv,
               tplot_general_dict,
               bar_plot_general_dict,
               bar_ext_par_dict,
               comp_bar_par_dict,
               revo_plot_general_dict,
               res_evo_par_dict,
               cs_scatter_par_dict,
               cs_scatter_flower_dict,
               param_settings=None,
               atomtype='Backbone'):
    '''
    This function was written because it serves normal titrations and
    control titrations.
    '''
    # checks if there are any plot flags activated
    # and if not outputs eh respective message.
    if not(any([fsuv.plots_extended_bar,
                fsuv.plots_compacted_bar,
                fsuv.plots_vertical_bar,
                fsuv.plots_residue_evolution,
                fsuv.plots_cs_scatter,
                fsuv.plots_cs_scatter_flower])):
        
        for calculated_parameter in param_settings.index:
        # if the user wants to plot this parameter
            if param_settings.loc[calculated_parameter,'plot_param_flag']:
                titration_panel.write_table(calculated_parameter,
                                            calculated_parameter,
                                            atomtype=atomtype)
        
        titration_panel.log_r(fsw.wet3())
    
    # PLOTS DATA
    for calculated_parameter in param_settings.index:
        # if the user wants to plot this parameter
        if param_settings.loc[calculated_parameter,'plot_param_flag']:
            #input('plooooot {}'.format(titration_panel.resonance_type))
            if titration_panel.resonance_type == 'Backbone':
                
                # Plot Extended Bar Plot
                if fsuv.plots_extended_bar:
                    titration_panel.plot_base(
                        calculated_parameter, 'exp', 'bar_extended',
                        {   **tplot_general_dict,
                            **bar_plot_general_dict,
                            **bar_ext_par_dict},
                        par_ylims=\
                        param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_scale'],
                        ylabel=\
                        param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_label'],
                        hspace=fsuv.tplot_vspace,
                        cols_per_page=fsuv.ext_bar_cols_page,
                        rows_per_page=fsuv.ext_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
                
                # Plot Compacted Bar Plot
                if fsuv.plots_compacted_bar:
                    
                    titration_panel.plot_base(\
                        calculated_parameter, 'exp', 'bar_compacted',
                        {**tplot_general_dict,
                         **bar_plot_general_dict,
                         **comp_bar_par_dict},
                        par_ylims=\
                        param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_scale'],
                        ylabel=\
                        param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_label'],
                        hspace=fsuv.tplot_vspace,
                        cols_per_page=fsuv.comp_bar_cols_page,
                        rows_per_page=fsuv.comp_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
            
                # Plot Vertical Bar Plot
                if fsuv.plots_vertical_bar:
                    titration_panel.plot_base(
                        calculated_parameter, 'exp', 'bar_vertical',
                        {**tplot_general_dict,
                         **bar_plot_general_dict,
                         **bar_ext_par_dict},
                        par_ylims=\
                        param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_scale'],
                        ylabel=\
                        param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_label'],
                        cols_per_page=fsuv.vert_bar_cols_page,
                        rows_per_page=fsuv.vert_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
            
            # Sidechain data is represented in a different bar plot
            elif titration_panel.resonance_type == 'Sidechains'\
                and (fsuv.plots_extended_bar or fsuv.plots_compacted_bar):
                #do - dedicated single plot for sidechains
                titration_panel.plot_base(
                    calculated_parameter, 'exp', 'bar_extended',
                    {**tplot_general_dict,
                     **bar_plot_general_dict,
                     **bar_ext_par_dict},
                    par_ylims=\
                    param_settings.loc[calculated_parameter,
                                             'plot_yy_axis_scale'],
                    ylabel=\
                    param_settings.loc[calculated_parameter,
                                             'plot_yy_axis_label'],
                    hspace=fsuv.tplot_vspace,
                    cols_per_page=fsuv.ext_bar_cols_page,
                    rows_per_page=fsuv.ext_bar_rows_page,
                    atomtype='Sidechains',
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width/2,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
            
            # Plots Parameter Evolution Plot
            if fsuv.plots_residue_evolution:
                titration_panel.plot_base(\
                    calculated_parameter, 'res', 'res_evo',
                    {**revo_plot_general_dict,**res_evo_par_dict},
                    par_ylims=  
                    param_settings.loc[calculated_parameter,
                                             'plot_yy_axis_scale'],
                    ylabel=\
                    param_settings.loc[calculated_parameter,
                                             'plot_yy_axis_label'],
                    cols_per_page=fsuv.res_evo_cols_page,
                    rows_per_page=fsuv.res_evo_rows_page,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
            
    if fsuv.plots_cs_scatter \
        and ((fsuv.calcs_PosF1_delta and fsuv.calcs_PosF2_delta)\
            or fsuv.calcs_CSP):
        titration_panel.plot_base('15N_vs_1H', 'res', 'cs_scatter',
                            {**revo_plot_general_dict,
                             **cs_scatter_par_dict},
                            cols_per_page=fsuv.cs_scatter_cols_page,
                            rows_per_page=fsuv.cs_scatter_rows_page,
                            fig_height=fsuv.fig_height,
                            fig_width=fsuv.fig_width,
                            fig_file_type=fsuv.fig_file_type,
                            fig_dpi=fsuv.fig_dpi)
    
    if fsuv.plots_cs_scatter_flower \
        and ((fsuv.calcs_PosF1_delta and fsuv.calcs_PosF2_delta)\
            or fsuv.calcs_CSP):
        #DO
        titration_panel.plot_base('15N_vs_1H', 'single', 'cs_scatter_flower',
                                  {**revo_plot_general_dict,
                                    **cs_scatter_flower_dict},
                                  cols_per_page=2,
                            rows_per_page=3,
                            fig_height=fsuv.fig_height,
                            fig_width=fsuv.fig_width,
                            fig_file_type=fsuv.fig_file_type,
                            fig_dpi=fsuv.fig_dpi)
    return

def analyse_comparisons(exp, titration_dict, fsuv,
                        gpp=[],
                        ppp=[],
                        ps=[],
                        reso_type='Backbone'):
    """Algorythm to perform data comparisons over titration conditions."""
    
    def run_comparative(comp_panel):
        # EXPORTS FULLY PARSED PEAKLISTS
        exports_titration(comp_panel)
    
        # EXPORTS CALCULATIONS
        exports_data_tables(comp_panel, param_settings=ps, fsuv=fsuv)
        
        # performs pre analysis
        PRE_analysis(comp_panel, fsuv, gpp[0], *ppp, param_settings=ps)
        
        # plots data
        plots_data(comp_panel, fsuv, *gpp, param_settings=ps)
        
        return
        
    titration_dim_keys = {'cond1':['cond2','cond3'],
                          'cond2':['cond3','cond1'],
                          'cond3':['cond1','cond2']}
    
    cp = {} # dictionary stored comparisons over dimensions
    
    for dimension in sorted(titration_dict.keys()):
        # this send, cond1, cond2, cond3 ...
        c = fsc.Comparisons(titration_dict[dimension].copy(),
                        selfdim=dimension,
                        other_dim_keys=titration_dim_keys[dimension],
                        reso_type=reso_type)
        
        # stores comparison in a dictionary
        cp.setdefault(dimension, c)
        
        c.gen_comparison_labels(fst.Titration)
        
        #print(c.allClabels)
        #input('dimension {}'.format(dimension))
        
        if c.haslabels:
            for dim2_pt in sorted(c.allClabels.keys()):
                
                for dim1_pt in sorted(c.allClabels[dim2_pt].keys()):
                    
                    c.allClabels[dim2_pt][dim1_pt].log_t('COMPARING...')
                    
                    run_comparative(c.allClabels[dim2_pt][dim1_pt])
                    
                    c.log += c.allClabels[dim2_pt][dim1_pt].log
        
        c.gen_comparison_cool(fst.Titration)
        
        if c.hascool:
            for dim2_pt in sorted(c.allCcool.keys()):
                
                for dim1_pt in sorted(c.allCcool[dim2_pt].keys()):
                    c.allCcool[dim2_pt][dim1_pt].log_t('COMPARING...')
                    run_comparative(c.allCcool[dim2_pt][dim1_pt])
                    c.log += c.allCcool[dim2_pt][dim1_pt].log
        
    return cp

def run_farseer(spectra_path, fsuv):
    """
    Runs all the standard Farseer algorithm.
    Function calls here should give all the inputs to the functions.
    Other functions should not rely on external variables besides those
    received in parameters.
    """
    
    # Initiates the log
    init_log(fsuv.logfile_name, mod='w')
    
    # reads parameters into dictionaries and DataFrames
    calculated_params, \
    param_settings, \
    general_plot_params, \
    pre_plot_params, \
    general_variables = init_params(fsuv)
    
    # Initiates Farseer
    exp = init_farseer(spectra_path,
                       has_sidechains=fsuv.has_sidechains,
                       FASTAstart=fsuv.FASTAstart)
        
    # reads input
    reads_input(exp, fsuv)
    
    inits_conditions(exp)
    
    # identify residues
    identify_residues(exp)
    
    # corrects chemical shifts
    if fsuv.perform_cs_correction:
        correct_shifts(exp,
                       reso_type='Backbone',
                       res_ref=fsuv.cs_correction_res_ref)
        
        if exp.has_sidechains and fsuv.use_sidechains:
            correct_shifts(exp, reso_type='Sidechains')
    
    # expands lost residues to other dimensions
    if fsuv.expand_lost_yy:
        expand_lost(exp,
                    exp.allpeaklists,
                    exp.zzcoords,
                    exp.yycoords,
                    exp.yyref,
                    dim='y')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            expand_lost(exp,
                        exp.allsidechains,
                        exp.zzcoords,
                        exp.yycoords,
                        exp.yyref,
                        dim='y')
    
    if fsuv.expand_lost_zz:
        expand_lost(exp,
                    exp.allpeaklists,
                    exp.yycoords,
                    exp.zzcoords,
                    exp.zzref,
                    dim='z')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            expand_lost(exp,
                        exp.allsidechains,
                        exp.yycoords,
                        exp.zzcoords,
                        exp.zzref,
                        dim='z')
    
    ## expands peaklists to lost residues
    add_lost(exp, exp.allpeaklists, exp.allpeaklists,
             peak_status='lost',
             ref='REFERENCE')
    
    if exp.has_sidechains and fsuv.use_sidechains:
        add_lost(exp, exp.allsidechains, exp.allsidechains,
                       peak_status='lost',
                       ref='REFERENCE FOR SIDECHAINS',
                       kwargs={'atomtype':'Sidechain'})
    
    # adds fasta
    if fsuv.applyFASTA:
        add_lost(exp, exp.allFASTA, exp.allpeaklists,
                 peak_status='unassigned', ref='FASTA')
    
    #organize peaklist columns
    organize_columns(exp, exp.allpeaklists,
                     performed_cs_correction=fsuv.perform_cs_correction)
    
    if exp.has_sidechains and fsuv.use_sidechains:
        organize_columns(exp, exp.allsidechains, 
                         performed_cs_correction=fsuv.perform_cs_correction,
                         scbool=True)
    
    init_fs_cube(exp, sidechains=fsuv.use_sidechains)
    
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # init the dictionaries,
    # this is just to ease the call of close_log()
    Farseer_titration_dict = False
    Farseer_SD_titrations_dict = False
    comparison_dict = False
    comparison_dict_SD =False
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    # initiates a dictionary that contains all the titration to be evaluated
    # along all the conditions.
    Farseer_titration_dict = \
        gen_titration_dicts(\
            exp,
            exp.peaklists_p5d,
            cond1=fsuv.do_cond1,
            cond2=fsuv.do_cond2,
            cond3=fsuv.do_cond3,
            titration_class=fst.Titration,
            titration_kwargs=\
                titration_kwargs(fsuv,
                                 rt='Backbone',
                                 cp=calculated_params))
    
    # evaluates the titrations and plots the data
    eval_titrations(Farseer_titration_dict,
                    fsuv,
                    general_variables,
                    spectra_path=spectra_path,
                    param_settings = param_settings,
                    general_plot_params = general_plot_params,
                    pre_plot_params = pre_plot_params)
    
    if exp.has_sidechains and fsuv.use_sidechains:
        Farseer_SD_titrations_dict = \
            gen_titration_dicts(\
                exp,
                exp.sidechains_p5d,
                cond1=fsuv.do_cond1,
                cond2=fsuv.do_cond2,
                cond3=fsuv.do_cond3,
                titration_class=fst.Titration,
                titration_kwargs=\
                    titration_kwargs(fsuv,
                                     rt='Sidechains',
                                     cp=calculated_params))
        
        
        eval_titrations(Farseer_SD_titrations_dict,
                        fsuv,
                        general_variables,
                        atomtype='Sidechains',
                        spectra_path=spectra_path,
                        param_settings = param_settings,
                        general_plot_params = general_plot_params,
                        pre_plot_params = pre_plot_params)
    
    # Representing the results comparisons
    if fsuv.perform_comparisons:
        #fsut.write_title('WRITES TITRATION COMPARISONS')
        
        # analyses comparisons.
        comparison_dict = \
            analyse_comparisons(exp,
                                Farseer_titration_dict,
                                fsuv,
                                gpp=general_plot_params,
                                ps=param_settings,
                                ppp=pre_plot_params,
                                reso_type='Backbone')
        
        if exp.has_sidechains and fsuv.use_sidechains:
            #fsut.write_title('WRITES TITRATION COMPARISONS FOR SIDECHAINS')
            comparison_dict_SD = \
                analyse_comparisons(exp,
                                    Farseer_SD_titrations_dict,
                                    fsuv,
                                    gpp=general_plot_params,
                                    ps=param_settings,
                                    ppp=pre_plot_params,
                                    reso_type='Sidechains')
    
    # writes all the logs to a txt file.
    close_log(farseerset=exp, 
              backbone_titration=Farseer_titration_dict,
              sidechain_titration=Farseer_SD_titrations_dict,
              backbone_comparison=comparison_dict,
              sidechain_comparison=comparison_dict_SD,
              logfile_name=fsuv.logfile_name,
              mod='a')
    
    return

if __name__ == '__main__':
    
    fsuv, cwd = read_user_variables(sys.argv[1])
    
    copy_Farseer_version(cwd)
    
    # path evaluations now consider the absolute path, always.
    # in this way the user can run farseer from any folder taking the
    # input from any other folder.
    # path should be the folder where the 'spectra/' are stored and NOT the
    # path to the 'spectra/' folder.
    # if running from the actual folder, use:
    # $ python farseer_main.py .
    
    run_farseer('{}/spectra'.format(cwd), fsuv)
    
    fsw.end_good()
