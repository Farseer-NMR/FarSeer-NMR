import pandas as pd
import farseer_user_variables as fsuv

# calculated parameters
#calcparam_name_PosF1_delta = 'PosF1_delta'
#calcparam_name_PosF2_delta = 'PosF2_delta'
#calcparam_name_CSP = 'CSP'
#calcparam_name_Height_ratio = 'Height_ratio'
#calcparam_name_Volume_ratio = 'Vol_ratio'

calculated_params = [fsuv.calccol_name_PosF1_delta,
                     fsuv.calccol_name_PosF2_delta,
                     fsuv.calccol_name_CSP,
                     fsuv.calccol_name_Height_ratio,
                     fsuv.calccol_name_Volume_ratio
                    ]

#calculated_params = [calcparam_name_PosF1_delta, 
                     #calcparam_name_PosF2_delta,
                     #calcparam_name_CSP,
                     #calcparam_name_Height_ratio,
                     #calcparam_name_Volume_ratio]


#'calc_column_name':   [fsuv.calccol_name_PosF1_delta, fsuv.calccol_name_PosF2_delta, fsuv.calccol_name_CSP, fsuv.calccol_name_Height_ratio, fsuv.calccol_name_Volume_ratio],
param_settings_d = {
'plot_param_flag':    [fsuv.plots_PosF1_delta, fsuv.plots_PosF2_delta, fsuv.plots_CSP, fsuv.plots_Height_ratio, fsuv.plots_Volume_ratio],
'plot_yy_axis_label': [fsuv.yy_label_PosF1_delta, fsuv.yy_label_PosF2_delta, fsuv.yy_label_CSP, fsuv.yy_label_Height_ratio, fsuv.yy_label_Volume_ratio],
'plot_yy_axis_scale': [(-fsuv.yy_scale_PosF1_delta, fsuv.yy_scale_PosF1_delta),
                       (-fsuv.yy_scale_PosF2_delta, fsuv.yy_scale_PosF2_delta),
                       (0, fsuv.yy_scale_CSP),
                       (0, fsuv.yy_scale_Height_ratio),
                       (0, fsuv.yy_scale_Volume_ratio)]
                       }

# An array of settings that are local for each parameter
# the index of this dataframe are the calculated parameters.
param_settings = pd.DataFrame(param_settings_d, index=calculated_params)

bar_ext_par_dict = {
    'apply_status_2_bar_color':fsuv.ext_bar_apply_status_2_bar_color,
    'color_measured':fsuv.ext_bar_color_measured,
    'color_lost':fsuv.ext_bar_color_lost,
    'color_unassigned':fsuv.ext_bar_color_unassigned,
    'bar_width':fsuv.ext_bar_bar_width,
    'bar_alpha':fsuv.ext_bar_bar_alpha,
    'bar_linewidth':fsuv.ext_bar_bar_linewidth,
    'title_y':fsuv.ext_bar_title_y,
    'title_fs':fsuv.ext_bar_title_fs,
    'title_fn':fsuv.ext_bar_title_fn,
    'plot_threshold':fsuv.ext_bar_plot_threshold,
    'plot_threshold_color':fsuv.ext_bar_plot_threshold_color,
    'plot_threshold_lw':fsuv.ext_bar_plot_threshold_lw,
    'x_label_fs':fsuv.ext_bar_x_label_fs,
    'x_label_pad':fsuv.ext_bar_x_label_pad,
    'x_label_fn':fsuv.ext_bar_x_label_fn,
    'x_label_weight':fsuv.ext_bar_x_label_weight,
    'x_ticks_rot':fsuv.ext_bar_x_ticks_rot,
    'x_ticks_fs':fsuv.ext_bar_x_ticks_fs,
    'x_ticks_fn':fsuv.ext_bar_x_ticks_fn,
    'x_ticks_pad':fsuv.ext_bar_x_ticks_pad,
    'y_label_fs':fsuv.ext_bar_y_label_fs,
    'y_label_pad':fsuv.ext_bar_y_label_pad,
    'y_label_fn':fsuv.ext_bar_y_label_fn,
    'y_label_weight':fsuv.ext_bar_y_label_weight,
    'y_ticks_fs':fsuv.ext_bar_y_ticks_fs,
    'y_ticks_pad':fsuv.ext_bar_y_ticks_pad,
    'y_ticks_len':fsuv.ext_bar_y_ticks_len,
    'y_ticks_fn':fsuv.ext_bar_y_ticks_fn,
    'y_grid_color':fsuv.ext_bar_y_grid_color,
    'mark_prolines':fsuv.ext_bar_mark_prolines,
    'proline_mark':fsuv.ext_bar_proline_mark,
    'mark_user_details':fsuv.ext_bar_mark_user_details,
    'mark_fs':fsuv.ext_bar_mark_fs,
    'theo_pre':fsuv.apply_PRE_analysis,
    'pre_color':fsuv.ext_bar_pre_color,
    'pre_lw':fsuv.ext_bar_pre_lw
    }

comp_bar_par_dict = {
    'apply_status_2_bar_color':fsuv.comp_bar_apply_status_2_bar_color,
    'color_measured':fsuv.comp_bar_color_measured,
    'color_lost':fsuv.comp_bar_color_lost,
    'color_unassigned':fsuv.comp_bar_color_unassigned,
    'bar_width':fsuv.comp_bar_bar_width,
    'bar_alpha':fsuv.comp_bar_bar_alpha,
    'bar_linewidth':fsuv.comp_bar_bar_linewidth,
    'title_y':fsuv.comp_bar_title_y,
    'title_fs':fsuv.comp_bar_title_fs,
    'title_fn':fsuv.comp_bar_title_fn,
    'plot_threshold':fsuv.comp_bar_plot_threshold,
    'plot_threshold_color':fsuv.comp_bar_plot_threshold_color,
    'plot_threshold_lw':fsuv.comp_bar_plot_threshold_lw,
    'x_label_fs':fsuv.comp_bar_x_label_fs,
    'x_label_pad':fsuv.comp_bar_x_label_pad,
    'x_label_fn':fsuv.comp_bar_x_label_fn,
    'x_label_weight':fsuv.comp_bar_x_label_weight,
    'x_ticks_rot':fsuv.comp_bar_x_ticks_rot,
    'x_ticks_fs':fsuv.comp_bar_x_ticks_fs,
    'x_ticks_fn':fsuv.comp_bar_x_ticks_fn,
    'x_ticks_pad':fsuv.comp_bar_x_ticks_pad,
    'y_label_fs':fsuv.comp_bar_y_label_fs,
    'y_label_pad':fsuv.comp_bar_y_label_pad,
    'y_label_fn':fsuv.comp_bar_y_label_fn,
    'y_label_weight':fsuv.comp_bar_y_label_weight,
    'y_ticks_fs':fsuv.comp_bar_y_ticks_fs,
    'y_ticks_pad':fsuv.comp_bar_y_ticks_pad,
    'y_ticks_len':fsuv.comp_bar_y_ticks_len,
    'y_grid_color':fsuv.comp_bar_y_grid_color,
    'mark_prolines':fsuv.comp_bar_mark_prolines,
    'proline_mark':fsuv.comp_bar_proline_mark,
    'mark_user_details':fsuv.comp_bar_mark_user_details,
    'mark_fs':fsuv.comp_bar_mark_fs,
    'unassigned_shade':fsuv.comp_bar_unassigned_shade,
    'unassigned_shade_color':fsuv.comp_bar_unassigned_shade_color,
    'unassigned_shade_alpha':fsuv.comp_bar_unassigned_shade_alpha,
    'theo_pre':fsuv.apply_PRE_analysis,
    'pre_color':fsuv.comp_bar_pre_color,
    'pre_lw':fsuv.comp_bar_pre_lw
    }

bar_vert_par_dict = {
    'apply_status_2_bar_color':fsuv.vert_bar_apply_status_2_bar_color,
    'color_measured':fsuv.vert_bar_color_measured,
    'color_lost':fsuv.vert_bar_color_lost,
    'color_unassigned':fsuv.vert_bar_color_unassigned,
    'bar_height':fsuv.vert_bar_bar_width,
    'bar_alpha':fsuv.vert_bar_bar_alpha,
    'bar_linewidth':fsuv.vert_bar_bar_linewidth,
    'title_y':fsuv.vert_bar_title_y,
    'title_fs':fsuv.vert_bar_title_fs,
    'title_fn':fsuv.vert_bar_title_fn,
    'plot_threshold':fsuv.vert_bar_plot_threshold,
    'plot_threshold_color':fsuv.vert_bar_plot_threshold_color,
    'plot_threshold_lw':fsuv.vert_bar_plot_threshold_lw,
    'x_label_fs':fsuv.vert_bar_x_label_fs,
    'x_label_pad':fsuv.vert_bar_x_label_pad,
    'x_label_fn':fsuv.vert_bar_x_label_fn,
    'x_label_weight':fsuv.vert_bar_x_label_weight,
    'x_ticks_len':fsuv.vert_bar_x_ticks_len,
    'x_ticks_fs':fsuv.vert_bar_x_ticks_fs,
    'x_ticks_fn':fsuv.vert_bar_x_ticks_fn,
    'x_ticks_pad':fsuv.vert_bar_x_ticks_pad,
    'x_grid_color':fsuv.vert_bar_x_grid_color,
    'y_label_fs':fsuv.vert_bar_y_label_fs,
    'y_label_pad':fsuv.vert_bar_y_label_pad,
    'y_label_fn':fsuv.vert_bar_y_label_fn,
    'y_label_weight':fsuv.vert_bar_y_label_weight,
    'y_label_rot':fsuv.vert_bar_y_label_rot,
    'y_ticks_fs':fsuv.vert_bar_y_ticks_fs,
    'y_ticks_fn':fsuv.vert_bar_y_ticks_fn,
    'y_ticks_pad':fsuv.vert_bar_y_ticks_pad,
    'y_ticks_rot':fsuv.vert_bar_y_ticks_rot,
    'x_grid_color':fsuv.vert_bar_x_grid_color,
    'mark_prolines':fsuv.vert_bar_mark_prolines,
    'proline_mark':fsuv.vert_bar_proline_mark,
    'mark_user_details':fsuv.vert_bar_mark_user_details,
    'mark_fs':fsuv.vert_bar_mark_fs
    }

res_evo_par_dict = {
    'title_y':fsuv.res_evo_title_y,
    'title_fs':fsuv.res_evo_title_fs,
    'title_fn':fsuv.res_evo_title_fn,
    'set_x_values':fsuv.res_evo_set_x_values,
    'tit_x_values':fsuv.fit_x_values,
    'x_label':fsuv.res_evo_x_label,
    'x_ticks_pad':fsuv.res_evo_x_ticks_pad,
    'x_ticks_fs':fsuv.res_evo_x_ticks_fs,
    'y_ticks_pad':fsuv.res_evo_y_ticks_pad,
    'y_ticks_fs':fsuv.res_evo_y_ticks_fs,
    'line_style':fsuv.res_evo_line_style,
    'plot_color':fsuv.res_evo_plot_color,
    'marker_style':fsuv.res_evo_marker_style,
    'marker_color':fsuv.res_evo_marker_color,
    'marker_size':fsuv.res_evo_marker_size,
    'line_width':fsuv.res_evo_line_width,
    'fill_between':fsuv.res_evo_fill_between,
    'fill_color':fsuv.res_evo_fill_color,
    'fill_alpha':fsuv.res_evo_fill_alpha,
    'fit_perform':fsuv.perform_resevo_fit,
    'fit_line_color':fsuv.res_evo_fit_line_color,
    'fit_line_width':fsuv.res_evo_fit_line_width
    }

cs_scatter_par_dict = {
    'title_y':fsuv.cs_scatter_title_y,
    'title_fs':fsuv.cs_scatter_title_fs,
    'title_fn':fsuv.cs_scatter_title_fn,
    'x_label_fs':fsuv.cs_scatter_x_label_fs, 
    'x_label_pad':fsuv.cs_scatter_x_label_pad,
    'x_label_fn':fsuv.cs_scatter_x_label_fn,
    'x_label_weight':fsuv.cs_scatter_x_label_weight,
    'x_ticks_pad':fsuv.cs_scatter_x_ticks_pad,
    'x_ticks_fs':fsuv.cs_scatter_x_ticks_fs,
    'y_label_fs':fsuv.cs_scatter_y_label_fs,
    'y_label_pad':fsuv.cs_scatter_y_label_pad,
    'y_label_fn':fsuv.cs_scatter_y_label_fn,
    'y_label_weight':fsuv.cs_scatter_y_label_weight,
    'y_ticks_pad':fsuv.cs_scatter_y_ticks_pad,
    'y_ticks_fs':fsuv.cs_scatter_y_ticks_fs,
    'mksize':fsuv.cs_scatter_mksize,
    'scale':fsuv.cs_scatter_scale,
    'markers':fsuv.cs_scatter_markers,
    'mk_type':fsuv.cs_scatter_mk_type,
    'mk_lost_color':fsuv.cs_scatter_mk_lost_color,
    'mk_start_color':fsuv.cs_scatter_mk_start_color,
    'mk_end_color':fsuv.cs_scatter_mk_end_color,
    'mk_color':fsuv.cs_scatter_mk_color,
    'mk_edgecolors':fsuv.cs_scatter_mk_edgecolors,
    'mk_edge_lost':fsuv.cs_scatter_mk_edge_lost
    }
                     
