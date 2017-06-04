defaults = {
  "general_settings": {
          "spectrum_path": "sys.argv[1]",
          "logfile_name": "file.log",
          "has_sidechains": False,
          "use_sidechains": False,
          "chimera_att_select_format": ":",
          "fig_file_type": "pdf",
          "fig_dpi": 300,
          "fig_height": 11.69,
          "fig_width": 8.69
  },
  
  "fitting_settings": {
          "do_titvar1": True,
          "do_titvar2": True,
          "do_titvar3": True,
          "expand_lost_yy": False,
          "expand_lost_zz": False,
          "perform_controls": True,
          "perform_comparisons": True,
          "perform_resevo_fitting": False,
          "fit_line_color": "black",
          "fit_line_width": 1,
          "include_user_annotations": False
  },          

  "cs_settings": {
          "perform_cs_correction": False,
          "cs_correction_res_ref": 76
  },

  "csp_settings": {
          "csp_res4alpha": 0.14,
          "csp_res_exceptions": "{'G': 0.2}",
          "cs_lost": "'prev'"
  },

  "fasta_settings": {
          "applyFASTA": True,
          "FASTAstart": 1
  },
  "pre_settings": {
          "apply_PRE_analysis": False,
          "apply_smooth": True,
          "gaussian_stdev": 1,
          "gauss_x_size": 7,
          "d_pre_y_max": 1,
          "d_pre_y_label": "r'$\\Delta$PRE$_(rc-exp)$'",
          "d_pre_rows": 10,
          "pre_color": "'red'",
          "pre_lw": 1,
          "tag_color": "'blue'",
          "tag_lw": 0.3,
          "tag_ls": "'-'"
    
  },

  "titration_plot_settings": {
        "tplot_subtitle_fn": 'Arial',
        "tplot_subtitle_fs": 8,
        "tplot_subtitle_pad": 0.99,
        "tplot_subtitle_weight": "normal",
        "tplot_x_label_fn": 'Arial',
        "tplot_x_label_fs": 8,
        "tplot_x_label_pad": 2,
        "tplot_x_label_weight": 'bold',
        "tplot_y_label_fn": 'Arial',
        "tplot_y_label_fs": 8,
        "tplot_y_label_pad": 3,
        "tplot_y_label_weight": "bold",
        "tplot_x_ticks_pad": 2,
        "tplot_x_ticks_len": 2,
        "tplot_y_ticks_fn": "Arial",
        "tplot_y_ticks_fs": 5,
        "tplot_y_ticks_rot": 0,
        "tplot_y_ticks_pad": 1,
        "tplot_y_ticks_weight": "normal",
        "tplot_y_ticks_len": 2,
        "tplot_y_grid_flag": True,
        "tplot_y_grid_color": "lightgrey",
        "tplot_y_grid_linestyle": "-",
        "tplot_y_grid_linewidth": 0.2,
        "tplot_y_grid_alpha": 0.8,
        "tplot_vspace": 0.5

  },
  "bar_plot_settings": {
        "bar_measured_color": "black",
        "bar_status_color_flag": True,
        "bar_lost_color": "red",
        "bar_unassigned_color": "lightgrey",
        "bar_width": 0.6,
        "bar_alpha": 1,
        "bar_linewidth": 0,
        "bar_threshold_flag": True,
        "bar_threshold_color": "red",
        "bar_threshold_linewidth": 0.5,
        "bar_threshold_alpha": 0.8,
        "bar_mark_fontsize": 3,
        "bar_mark_prolines_flag": True,
        "bar_mark_prolines_symbol": "P",
        "bar_mark_user_details_flag": False,
        "bar_color_user_details_flag": False
  },
  "extended_bar_settings": {
          "do_ext_bar": True,
          "ext_bar_cols_page": 5,
          "ext_bar_rows_page": 10,
          "ext_bar_x_ticks_fn": "monospace",
          "ext_bar_x_ticks_fs": 6,
          "ext_bar_x_ticks_rot": 90,
          "ext_bar_x_ticks_pad": 2,
          "ext_bar_x_ticks_weight": "normal",
          "ext_bar_x_ticks_color_flag": True,
  },
  
  "compact_bar_settings": {
          "do_comp_bar": True,
          "comp_bar_cols_page": 3,
          "comp_bar_rows_page": 5,
          "comp_bar_color_measured": "k",
          "comp_bar_x_ticks_fn": "Arial",
          "comp_bar_x_ticks_fs": 8,
          "comp_bar_x_ticks_pad": 2,
          "comp_bar_x_ticks_rot": 0,
          "comp_bar_x_ticks_weight": "normal",
          "comp_bar_unassigned_shade": True,
          "comp_bar_unassigned_shade_alpha": 0.5
  },
  
  
  "vert_bar_settings": {
          "do_vert_bar": True,
          "vert_bar_cols_page": 5,
          "vert_bar_rows_page": 2,
  },
  
  "plots_PosF1_settings":{
          "plots_PosF1_delta": True,
          "yy_label_PosF1_delta": "ppm",
          "calccol_name_PosF1_delta": "H1_delta",
          "yy_scale_PosF1_delta": 0.1
  },
  
  "plots_PosF2_settings":{
          "plots_PosF2_delta": True,
          "yy_label_PosF2_delta": "ppm",
          "calccol_name_PosF2_delta": "N15_delta",
          "yy_scale_PosF2_delta": 0.25
  },
  
  "plots_CSP_settings":{
           "plots_CSP": True,
           "yy_label_CSP": "CSPs (ppm)",
           "calccol_name_CSP": "CSP",
           "yy_scale_CSP": 0.1
  },
  
  "plots_Height_ratio_settings":{
            "plots_Height_ratio": True,
            "yy_label_Height_ratio": "Hi/H0",
            "calccol_name_Height_ratio": "Height_ratio",
            "yy_scale_Height_ratio": 1.5
  },
  
  "plots_Volume_ratio_settings": {
            "plots_Volume_ratio": True,
            "yy_label_Volume_ratio": "Vi/V0",
            "calccol_name_Volume_ratio": "Vol_ratio",
            "yy_scale_Volume_ratio": 1.5
  },

  "revo_settings": {
        "revo_subtitle_fn": "Arial",
        "revo_subtitle_fs": 8,
        "revo_subtitle_pad": 0.98,
        "revo_subtitle_weight": "normal",
        "revo_x_label_fn": "Arial",
        "revo_x_label_fs": 6,
        "revo_x_label_pad": 2,
        "revo_x_label_weight": "normal",
        "revo_y_label_fn": "Arial",
        "revo_y_label_fs": 6,
        "revo_y_label_pad": 2,
        "revo_y_label_weight": "normal",
        "revo_x_ticks_fn": "Arial",
        "revo_x_ticks_fs": 5,
        "revo_x_ticks_pad": 1,
        "revo_x_ticks_weight": "normal",
        "revo_x_ticks_rot": 30,
        "revo_y_ticks_fn": "Arial",
        "revo_y_ticks_fs": 5,
        "revo_y_ticks_pad": 1,
        "revo_y_ticks_weight": "normal",
        "revo_y_ticks_rot": 0,
        "titration_x_values": [0, 125, 250, 500, 1000, 2000, 2500]
  },
  "res_evo_settings": {
          "do_res_evo": True,
          "res_evo_cols_page":  5,
          "res_evo_rows_page":  8,
          "res_evo_x_ticks_nbins": 5,
          "res_evo_x_label": "[RNF125]",
          "res_evo_set_x_values": True,
          "res_evo_line_style": "-",
          "res_evo_line_width": 1,
          "res_evo_line_color": "r",
          "res_evo_marker_style": "o",
          "res_evo_marker_color": "darkred",
          "res_evo_marker_size": 3,
          "res_evo_fill_between": True,
          "res_evo_fill_color": "pink",
          "res_evo_fill_alpha": 0.5,
          "res_evo_fit_line_color":  "black",
          "res_evo_fit_line_width":  1,
          "res_evo_fit_line_style": "-"
  },
  
  "user_mark_settings":  {
          "H0": "V",
          "V0": "H",
          "low": "L",
          "p1": "1",
          "p2": "2",
          "p3": "3",
          "p4": "4",
          "p5": "5",
          "p6": "6",
          "p7": "7",
          "p8": "8",
          "p9": "9",
          "p10": "10",
          "z": "z"
  },

  "cs_scatter_settings": {
          "do_cs_scatter": True,
          "cs_scatter_cols_page": 5,
          "cs_scatter_rows_page": 7,
          "cs_scatter_x_label": '1H (ppm)',
          "cs_scatter_y_label": '15N (ppm)',
          "cs_scatter_mksize": 20,
          "cs_scatter_scale": 0.01,
          "cs_scatter_mk_type": "color",
          "cs_scatter_mk_start_color": "#cdcdcd",
          "cs_scatter_mk_end_color": "#000000",
          "cs_scatter_mk_lost_color": "red",
          "cs_scatter_markers": [
            "^",
            ">",
            "v",
            "<",
            "s",
            "p",
            "h",
            "8",
            "*",
            "D"
          ],
          "cs_scatter_mk_color": "grey",
          "cs_scatter_mk_edgecolors": "black",
          "cs_scatter_mk_edge_lost": "red",
          "cs_scatter_hide_lost": False
  },
  "cs_scatter_flower_settings": {
        "cs_scatter_flower_x_label": "1H (ppm)",
        "cs_scatter_flower_y_label": "15N (ppm)",
        "cs_scatter_flower_mksize": 8,
        "cs_scatter_flower_color_grad": True,
        "cs_scatter_flower_color_start": "#e7e7e7",
        "cs_scatter_flower_color_end": "#000000",
        "cs_scatter_flower_color_list": [],
        "cs_scatter_flower_x_label_fn": "Arial",
        "cs_scatter_flower_x_label_fs": 10,
        "cs_scatter_flower_x_label_pad": 2,
        "cs_scatter_flower_x_label_weight": "normal",
        "cs_scatter_flower_y_label_fn": "Arial",
        "cs_scatter_flower_y_label_fs": 10,
        "cs_scatter_flower_y_label_pad": 2,
        "cs_scatter_flower_y_label_weight": "normal",
        "cs_scatter_flower_x_ticks_fn": "Arial",
        "cs_scatter_flower_x_ticks_fs": 8,
        "cs_scatter_flower_x_ticks_pad": 1,
        "cs_scatter_flower_x_ticks_weight": "normal",
        "cs_scatter_flower_x_ticks_rot": 0,
        "cs_scatter_flower_y_ticks_fn": "Arial",
        "cs_scatter_flower_y_ticks_fs": 8,
        "cs_scatter_flower_y_ticks_pad": 1,
        "cs_scatter_flower_y_ticks_weight": "normal",
        "cs_scatter_flower_y_ticks_rot": 0
  },

  "heat_map_settings": {
          "do_heat_map": True,
          "heat_map_rows": 20,
          "heat_map_vmin": 0.2,
          "heat_map_vmax": 0.7,
          "heat_map_x_ticks_fs": 6,
          "heat_map_x_ticks_rot": 0,
          "heat_map_x_ticks_fn": "Arial",
          "heat_map_x_tick_pad": 1,
          "heat_map_y_label_fs": 3,
          "heat_map_y_label_pad": 2,
          "heat_map_y_label_fn": "Arial",
          "heat_map_y_label_weight": "bold",
          "heat_map_right_margin": 0.2,
          "heat_map_bottom_margin": 0.5,
          "heat_map_top_margin": 0.9,
          "heat_map_cbar_font_size": 4
  },

  "dpre_osci_settings": {
          "do_dpre": True,
          "dpre_osci_width": 3,
          "dpre_osci_title_y": 1,
          "dpre_osci_title_fs": 6,
          "dpre_osci_title_fn": "Arial",
          "dpre_osci_dpre_ms": 2,
          "dpre_osci_dpre_alpha": 0.5,
          "dpre_osci_smooth_lw": 1,
          "dpre_osci_ref_color": "black",
          "dpre_osci_color_init": "#ff00ff",
          "dpre_osci_color_end": "#0000ff",
          "dpre_osci_x_ticks_fs": 5,
          "dpre_osci_x_ticks_fn": "Arial",
          "dpre_osci_y_label_fs": 6,
          "dpre_osci_y_label_pad": 1,
          "dpre_osci_y_label_fn": "Arial",
          "dpre_osci_y_label_weight": "normal",
          "dpre_osci_y_ticks_len": 1,
          "dpre_osci_y_ticks_fs": 4,
          "dpre_osci_y_ticks_pad": 1,
          "dpre_osci_grid_color": "grey",
          "dpre_osci_res_shade": False,
          "dpre_osci_res_highlight": [
            [
              24,
              1.5
            ],
            [
              37,
              3
            ],
            [
              3,
              1.5
            ],
            [
              65,
              6
            ]
          ],
          "dpre_osci_rh_fs": 4,
          "dpre_osci_rh_y": 0.9
  }
}
