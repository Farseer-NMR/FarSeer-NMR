import pandas as pd
import farseer_user_variables as fsuv

calculated_params = [fsuv.calccol_name_PosF1_delta,
                     fsuv.calccol_name_PosF2_delta,
                     fsuv.calccol_name_CSP,
                     fsuv.calccol_name_Height_ratio,
                     fsuv.calccol_name_Volume_ratio
                    ]


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

p5d = pd.core.panelnd.create_nd_panel_factory(\
            klass_name='Panel5D',
            orders=['cool', 'labels', 'items', 'major_axis', 'minor_axis'],
            slices={'labels': 'labels',
                    'items': 'items',
                    'major_axis': 'major_axis',
                    'minor_axis': 'minor_axis'},
            slicer=pd.Panel4D,
            aliases={'major': 'index', 'minor': 'minor_axis'},
            stat_axis=2)

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
    'titration_x_values':fsuv.titration_x_values
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
    'mk_lost_color':fsuv.cs_scatter_mk_lost_color
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
    'top_margin':fsuv.heat_map_top_margin,
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
