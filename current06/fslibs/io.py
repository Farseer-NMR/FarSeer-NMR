import json

def fsuv_to_json(fsuv):


    pass

def json_to_fsuv(fsuv_file_path, json_file=None, variables=None):

    if json_file:
        js = json.load(json_file)
    elif variables:
        js = variables
    else:
        pass
    fout = open(fsuv_file_path, 'w')
    gen = js["general_settings"]
    fit = js["fitting_settings"]
    cs = js["cs_settings"]
    csp = js["csp_settings"]
    fasta = js["fasta_settings"]
    pre = js["pre_settings"]
    ext = js["extended_bar_settings"]
    comp = js["compact_bar_settings"]
    vert = js["vert_bar_settings"]
    flower = js["cs_scatter_flower_settings"]
    tplot = js["titration_plot_settings"]
    bar_plot = js["bar_plot_settings"]
    pf1 = js["plots_PosF1_settings"]
    pf2 = js["plots_PosF2_settings"]
    p_csp = js["plots_CSP_settings"]
    p_height = js["plots_Height_ratio_settings"]
    p_vol = js["plots_Volume_ratio_settings"]
    res_evo = js["res_evo_settings"]
    scatter = js["cs_scatter_settings"]
    heat_map = js["heat_map_settings"]
    dpre = js["dpre_osci_settings"]


    fsuv_general = """import sys
#
logfile_name = '{}'  # the name of the log file
#
has_sidechains = {}  # Are there sidechain entries in the peaklists?
use_sidechains = {}  # Do you want to analyse those sidechains?
#
chimera_att_select_format = ':'  # format to select residues in Chimera
""".format(
        gen["logfile_name"],
        gen["has_sidechains"],
        gen["use_sidechains"])
    fsuv_cs = """
perform_cs_correction = {}  # Aligns peaklists to a specific residue in the reference spectra
cs_correction_res_ref = {}  # To which residue?
#
""".format(cs["perform_cs_correction"],
        cs["cs_correction_res_ref"])

    fsuv_fit="""
expand_lost_yy = {}  # Considers lost residue over yy references and xx reference
expand_lost_zz = {}  # Considers lost residue over zz references and xx reference
#
do_cond1 = {}  # Analyse data in the first titration condition (dimension)
do_cond2 = {}  # Analyse data in the second titration condition (dimension)
do_cond3 = {}  # Analyse data in the thrid titration condition (dimension)
perform_comparisons = True  # Compares data obtained for condition experiment.
#
perform_resevo_fit = {}  # Fit parameter evolution over titration experiment
#
titration_x_values = {} # values for the x axis in the fitting procedure (ex. Ligand concentration)

""".format(
        fit["expand_lost_yy"],
        fit["expand_lost_zz"],
        fit["do_titvar1"],
        fit["do_titvar2"],
        fit["do_titvar3"],
        revo["perform_resevo_fit"],
        revo["titration_x_values"]
    )


    fsuv_fasta = """
applyFASTA = {}  # complete the sequence with a FASTA file?
FASTAstart = {}  # Residue number for the first residue in the FASTA file?
""".format(
        fasta["applyFASTA"],
        fasta["FASTAstart"])

    fsuv_csp = """
csp_alpha4res = {}  # General alpha normalization factor for CSP
csp_res_exceptions = {}  # exceptions for the normalization factor
cs_lost = {}  # how to represent the lost residues in CSPs [prev/full]
#
""".format(csp["csp_res4alpha"],
        csp["csp_res_exceptions"],
        csp["cs_lost"])


    fsuv_pre = """
# Perform PRE analysis
apply_PRE_analysis = {}
apply_smooth = {}
gaussian_stddev = {}
gauss_x_size = {}
pre_color = {}  # theoretical PRE line color
pre_lw = {}  # theoretical PRE line width
tag_color = {}
tag_lw = {}
tag_ls = {}""".format(
        pre["apply_PRE_analysis"],
        pre["apply_smooth"],
        pre["gaussian_stdev"],
        pre["gauss_x_size"],
        pre["pre_color"],
        pre["pre_lw"],
        pre["tag_color"],
        pre["tag_lw"],
        pre["tag_ls"],
    )

    fsuv_plots = """
#
plots_PosF1_delta = {}  # Plot nuclei 1 shift perturbation data
plots_PosF2_delta = {}  # Plot nuclei 2 shift perturbation data
plots_CSP = {}  # Plot combined chemical shift perturbation data
plots_Height_ratio = {}  # Plot Height ratio data
plots_Volume_ratio = {}  # Plot Volume ratio data
#
plots_extended_bar = {}  # Represent data in Extended Bar Plot style
plots_compacted_bar = {}  # Represent data in Compacted Bar Plot style
plots_vertical_bar = {}  # Represent data in Vertical Bar Plot style
plots_residue_evolution = {}  # Represent Data Evolution per Residue style
plots_cs_scatter = {}  # Represent chemical shift scatter data
plots_cs_scatter_flower = {}
#
#
yy_label_PosF1_delta = '{}'  # y axis label for nuclei 1
yy_label_PosF2_delta = '{}'  # y axis label for nuclei 2
yy_label_CSP = '{}'  # y axis label for combined chemical shift
yy_label_Height_ratio = '{}'  # y axis label for height ratio
yy_label_Volume_ratio = '{}'  # y axis label for volume ratio
#
calccol_name_PosF1_delta = '{}'  # column name for nuclei 1
calccol_name_PosF2_delta = '{}'  # column name for nuclei 2
calccol_name_CSP = '{}'  # column name for combined chemical shift perturbation data
calccol_name_Height_ratio = '{}'  # column name for Height Ratio data
calccol_name_Volume_ratio = '{}'  # column name for Volume Ratio data
#
yy_scale_PosF1_delta = {}  # y axis sacle for nuclei 1
yy_scale_PosF2_delta = {}  # y axis scale for nuclei 2
yy_scale_CSP = {}  # y axis sacle for combined chemical shift
yy_scale_Height_ratio = {}  # y axis scale for height ratio
yy_scale_Volume_ratio = {}  # y axis scale for volume ratio
#
""".format(
    pf1["plots_PosF1_delta"],
    pf2["plots_PosF2_delta"],
    p_csp["plots_CSP"],
    p_height["plots_Height_ratio"],
    p_vol["plots_Volume_ratio"],
    ext["do_ext_bar"],
    comp["do_comp_bar"],
    vert["do_vert_bar"],
    res_evo["do_res_evo"],
    scatter["do_cs_scatter"],
    flower["do_cs_flower"],
    pf1["yy_label_PosF1_delta"],
    pf2["yy_label_PosF2_delta"],
    p_csp["yy_label_CSP"],
    p_height["yy_label_Height_ratio"],
    p_vol["yy_label_Volume_ratio"],
    pf1["calccol_name_PosF1_delta"],
    pf2["calccol_name_PosF2_delta"],
    p_csp["calccol_name_CSP"],
    p_height["calccol_name_Height_ratio"],
    p_vol["calccol_name_Volume_ratio"],
    pf1["yy_scale_PosF1_delta"],
    pf2["yy_scale_PosF2_delta"],
    p_csp["yy_scale_CSP"],
    p_height["yy_scale_Height_ratio"],
    p_vol["yy_scale_Volume_ratio"],
    )

    fsuv_tplot = """
#### Plot configuration variables
### General Titration Plots Variables
tplot_subtitle_fn= 'Arial'  # font type for the subplot titles.
tplot_subtitle_fs= 8  # font size for the subplot titles.
tplot_subtitle_pad= 0.99  # subplot title separation from y
tplot_subtitle_weight= 'normal'  # subplot title font weight: bold, italic, etc...
tplot_x_label_fn= 'Arial'  # x-label font
tplot_x_label_fs= 8  # x-label font size
tplot_x_label_pad= 2  # x-label separation from axis
tplot_x_label_weight= 'bold'  #x_label font weight: bold, italic, etc...
tplot_y_label_fn= 'Arial'  # y-label font
tplot_y_label_fs= 8  # y-label font size
tplot_y_label_pad=3  # y-label separation from ayis
tplot_y_label_weight= 'bold'  #y_label font weight: bold, italic, etc...
tplot_x_ticks_pad=2  # x ticks pad
tplot_x_ticks_len=2  # length of xticks
tplot_y_ticks_fn='Arial'  # y-tick font name
tplot_y_ticks_fs=5  # y-tick font size
tplot_y_ticks_rot=0
tplot_y_ticks_pad=1  # y-tick separati
tplot_y_ticks_weight= 'normal'  #x_label font weight: bold, italic, etc...on
tplot_y_ticks_len=2  # length of y ticks
tplot_y_grid_flag=True  # ON/OFF horizontal grid
tplot_y_grid_color='lightgrey'  # grid color
tplot_y_grid_linestyle='-'  # style of grid line
tplot_y_grid_linewidth=0.2  # grid line width
tplot_y_grid_alpha=0.8  # grid transparency
tplot_vspace=0.5 # vertical spacing between plots
    """.format(
        tplot["tplot_subtitle_fn"],
        tplot["tplot_subtitle_fs"],
        tplot["tplot_subtitle_pad"],
        tplot["tplot_subtitle_weight"],
        tplot["tplot_vspace"],
        tplot["tplot_x_label_fn"],
        tplot["tplot_x_label_fs"],
        tplot["tplot_x_label_pad"],
        tplot["tplot_x_label_weight"],
        tplot["tplot_x_ticks_len"],
        tplot["tplot_x_ticks_pad"],
        tplot["tplot_y_grid_alpha"],
        tplot["tplot_y_grid_color"],
        tplot["tplot_y_grid_flag"],
        tplot["tplot_y_grid_linestyle"],
        tplot["tplot_y_grid_linewidth"],
        tplot["tplot_y_label_fn"],
        tplot["tplot_y_label_fs"],
        tplot["tplot_y_label_pad"],
        tplot["tplot_y_label_weight"],
        tplot["tplot_y_ticks_fn"],
        tplot["tplot_y_ticks_fs"],
        tplot["tplot_y_ticks_len"],
        tplot["tplot_y_ticks_pad"],
        tplot["tplot_y_ticks_rot"],
        tplot["tplot_y_ticks_weight"]
    )

    fsuv_bar_plot = """
## General Bar Plots Variables
bar_measured_color = {}  # bar color for measured peaks
bar_status_color_flag = {}  # applies color to the 'lost' residues
bar_lost_color = {} # bar color for the lost residues
bar_unassigned_color = {}  # xticks and shade color for unassigned residues.
bar_width = {}  # bar width
bar_alpha = {}  # 0 is full transparency, 1 full opacity
bar_linewidth = {}  # bar border line width, 0 to desable
bar_threshold_flag = {}  # applies stdev thresold
bar_threshold_color = {} # threshold color
bar_threshold_linewidth = {}  # threshold line width
bar_threshold_alpha = {}  # threshold transparency
bar_mark_fontsize = {}  # user defined marks fontsize
bar_mark_prolines_flag = {}  # mark prolines ON/OFF
bar_mark_prolines_symbol = {}  # symbol to mark prolines
bar_mark_user_details_flag = {}  # mark user details ON/OFF
bar_color_user_details_flag = {}  # color bars according to user detail marks ON/OFF
bar_user_marks_dict = {}  # keys: the string in 'Details' column in input data, value: the character to be drawn
bar_user_bar_colors_dict = {}  # keys: the string in 'Details' column in input data, value: the character to be drawn
    """.format(
        bar_plot["bar_alpha"],
        bar_plot["bar_color_user_details_flag"],
        bar_plot["bar_linewidth"],
        bar_plot["bar_lost_color"],
        bar_plot["bar_mark_fontsize"],
        bar_plot["bar_mark_prolines_flag"],
        bar_plot["bar_mark_prolines_symbol"],
        bar_plot["bar_mark_user_details_flag"],
        bar_plot["bar_measured_color"],
        bar_plot["bar_status_color_flag"],
        bar_plot["bar_threshold_alpha"],
        bar_plot["bar_threshold_color"],
        bar_plot["bar_threshold_flag"],
        bar_plot["bar_threshold_linewidth"],
        bar_plot["bar_unassigned_color"],
        bar_plot["bar_width"]
    )


    fsuv_ext = """
# Extended Bar Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
ext_bar_cols_page = {}  # number of columns of subplots per page
ext_bar_rows_page = {}  # number of rows of subplots per page
ext_bar_x_ticks_fn = {}  # x ticks font type
ext_bar_x_ticks_fs = {}  # x ticks font size
ext_bar_x_ticks_rot = {}  # x ticks rotation
ext_bar_x_ticks_weight = {}  # x ticks rotation
ext_bar_x_ticks_color_flag = {}
#
#
""".format(
    ext["ext_bar_cols_page"],
    ext["ext_bar_rows_page"],
    ext["ext_bar_x_ticks_color_flag"],
    ext["ext_bar_x_ticks_fn"],
    ext["ext_bar_x_ticks_fs"],
    ext["ext_bar_x_ticks_pad"],
    ext["ext_bar_x_ticks_rot"],
    ext["ext_bar_x_ticks_weight"]
    )

    fsuv_comp = """
# Specific details for Compacted Bar Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
comp_bar_cols_page = {}  # number of columns of subplots per page
comp_bar_rows_page = {} # number of rows of subplots per page
comp_bar_x_ticks_fn = {}  # x ticks font type
comp_bar_x_ticks_fs = {}  # x ticks font size
comp_bar_x_ticks_rot = {}  # x ticks rotation
comp_bar_x_ticks_weight = {}  # x ticks pad
comp_bar_unassigned_shade = {}  # displays shade for unassigned residues
comp_bar_unassigned_shade_alpha = {}  # unassigned residues shade transparency.
""".format(
        comp["comp_bar_color_measured"],
        comp["comp_bar_cols_page"],
        comp["comp_bar_rows_page"],
        comp["comp_bar_unassigned_shade"],
        comp["comp_bar_unassigned_shade_alpha"],
        comp["comp_bar_x_ticks_fn"],
        comp["comp_bar_x_ticks_weight"],
        comp["comp_bar_x_ticks_fs"],
        comp["comp_bar_x_ticks_pad"],
        comp["comp_bar_x_ticks_rot"],
    )
    fsuv_vert = """
# Specific details for Vertical Bar plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
vert_bar_cols_page = {}  # number of columns of subplots per page
vert_bar_rows_page = {} # number of rows of subplots per page
#
""".format(
        vert["vert_bar_cols_page"],
        vert["vert_bar_rows_page"]
    )

    fsuv_dpre = """
# Specific details for DELTA PRE oscilations Plot
dpre_osci_rows = {}
dpre_osci_width = {}  # scale factor for the width of the plot
dpre_osci_y_label = {}
dpre_osci_y_label_fs = {}
dpre_osci_dpre_ms = {}  # DELTA_PRE circle marker size
dpre_osci_ymax = {}
dpre_osci_dpre_alpha = {}  # DELTA_PRE alpha
dpre_osci_smooth_lw = {}  # smooted DPRE line width
dpre_osci_ref_color= {}  # color for the reference data
dpre_osci_color_init = {}  # initial color for data points color gradient
dpre_osci_color_end = {}  # final color for data points color gradient
dpre_osci_x_ticks_fn = {}  # xticks font
dpre_osci_x_ticks_fs = {}  # x ticks font size
dpre_osci_x_ticks_pad = {}
dpre_osci_x_ticks_weight = {}
dpre_osci_grid_color = {}  # grid color
dpre_osci_shade = {}  # applies shade to regions
dpre_osci_shade_regions = {}  # defines shade regions
dpre_osci_res_highlight = {}  # flags residue highlight
dpre_osci_res_hl_list = {}  # residues to highlight (res, shade width)
dpre_osci_rh_fs = {}  # font size for residue highlight
dpre_osci_rh_y = {}  # y position for residue 1-letter representation
""".format(
        dpre["do_dpre"],
        dpre["dpre_osci_color_end"],
        dpre["dpre_osci_color_init"],
        dpre["dpre_osci_dpre_alpha"],
        dpre["dpre_osci_dpre_ms"],
        dpre["dpre_osci_grid_color"],
        dpre["dpre_osci_ref_color"],
        dpre["dpre_osci_res_highlight"],
        dpre["dpre_osci_res_shade"],
        dpre["dpre_osci_rh_fs"],
        dpre["dpre_osci_rh_y"],
        dpre["dpre_osci_smooth_lw"],
        dpre["dpre_osci_title_fn"],
        dpre["dpre_osci_title_fs"],
        dpre["dpre_osci_title_y"],
        dpre["dpre_osci_width"],
        dpre["dpre_osci_x_ticks_fn"],
        dpre["dpre_osci_x_ticks_fs"],
        dpre["dpre_osci_y_label_fn"],
        dpre["dpre_osci_y_label_fs"],
        dpre["dpre_osci_y_label_pad"],
        dpre["dpre_osci_y_label_weight"],
        dpre["dpre_osci_y_ticks_fs"],
        dpre["dpre_osci_y_ticks_len"],
        dpre["dpre_osci_y_ticks_pad"]
    )

    fsuv_revo = """
## General Variables for Evolution per Residue
revo_subtitle_fn = {}  # subplot title font
revo_subtitle_fs = {}  # subplot title font size
revo_subtitle_pad = {}  # subplot title pad
revo_subtitle_weight = {}
revo_x_label_fn = {} # x label font
revo_x_label_fs = {} # x label font size
revo_x_label_pad = {}  # x label pad
revo_x_label_weight = {}  # x label weight
revo_y_label_fn = {}  # y label font
revo_y_label_fs = {}  # y label font size
revo_y_label_pad = {}  # y label pad
revo_y_label_weight = {}  # y label weight
revo_x_ticks_fn = {}  # x ticks font
revo_x_ticks_fs = {}  # x ticks font size
revo_x_ticks_pad = {}  # x ticks pad
revo_x_ticks_weight = {}  # x ticks font style
revo_x_ticks_rot = {}  # ticks label rotation
revo_y_ticks_fn = {}  # x ticks font
revo_y_ticks_fs = {}  # x ticks font size
revo_y_ticks_pad = {}  # x ticks pad
revo_y_ticks_weight = {}  # x ticks font style
revo_y_ticks_rot = {}
    """.format(
        revo["revo_subtitle_fn"],
        revo["revo_subtitle_fs"],
        revo["revo_subtitle_pad"],
        revo["revo_subtitle_weight"],
        revo["revo_x_label_fn"],
        revo["revo_x_label_fs"],
        revo["revo_x_label_pad"],
        revo["revo_x_label_weight"],
        revo["revo_x_ticks_fn"],
        revo["revo_x_ticks_fs"],
        revo["revo_x_ticks_pad"],
        revo["revo_x_ticks_rot"],
        revo["revo_x_ticks_weight"],
        revo["revo_y_label_fn"],
        revo["revo_y_label_fs"],
        revo["revo_y_label_pad"],
        revo["revo_y_label_weight"],
        revo["revo_y_ticks_fn"],
        revo["revo_y_ticks_fs"],
        revo["revo_y_ticks_pad"],
        revo["revo_y_ticks_rot"],
        revo["revo_y_ticks_weight"],
    )
    fsuv_res_evo = """
res_evo_cols_page = {}  # number of columns of subplots per page
res_evo_rows_page = {}  # number of rows of subplots per page
res_evo_x_label = '{}'  # x label
res_evo_set_x_values = {}  # use user defined x values? Necessary for titration fitting.
res_evo_x_ticks_nbins = {}  #adjust number of ticks
res_evo_line_style = '{}'  # data line style
res_evo_line_width = {}  # data line width
res_evo_line_color = {}  # data line width
res_evo_marker_style = '{}'  # data marker style
res_evo_marker_color = '{}'  # data marker color
res_evo_marker_size = {}  # data marker size
res_evo_fill_between = {}  # draw data shade
res_evo_fill_color = '{}'  # shade color
res_evo_fill_alpha = {}  # shade transparency (0-1)
res_evo_fit_line_color = '{}'  # fit line color
res_evo_fit_line_width = {}  # fit line width
res_evo_fit_line_style = {}  # fit line style
#
    """.format(
        res_evo["res_evo_cols_page"],
        res_evo["res_evo_rows_page"],
        res_evo["res_evo_x_label"],
        res_evo["res_evo_set_x_values"],
        res_evo["res_evo_x_ticks_nbins"],
        res_evo["res_evo_line_style"],
        res_evo["res_evo_line_width"],
        res_evo["res_evo_line_color"],
        res_evo["res_evo_marker_style"],
        res_evo["res_evo_marker_color"],
        res_evo["res_evo_marker_size"],
        res_evo["res_evo_fill_between"],
        res_evo["res_evo_fill_color"],
        res_evo["res_evo_fill_alpha"],
        res_evo["res_evo_fit_line_color"],
        res_evo["res_evo_fit_line_width"],
        res_evo["res_evo_fit_line_style"],
    )

    fsuv_scatter = """
# Specific details for Chemical Shift Scatter Plot
cs_scatter_cols_page = {}  # number of columns of subplots per page
cs_scatter_rows_page = {}  # number of rows of subplots per page
cs_scatter_x_label = {}
cs_scatter_y_label = {}
cs_scatter_mksize = {}  # marker size
cs_scatter_scale = {}  # scale representation
cs_scatter_mk_type = {} # 'color' or 'shape'
cs_scatter_mk_start_color = {} # start color for gradient [in hex notation] - color style
cs_scatter_mk_end_color = {} # end color for gradient [in hex notation] - color style
cs_scatter_markers = {}  # sequential markers
cs_scatter_mk_color = {}  # marker inside color for shape style - SHOULD BE LIST
cs_scatter_mk_edgecolors = {}  # marker edge color for shape style - SHOULD BE LIST
cs_scatter_mk_lost_color = {}  # color for lost data points - color style
cs_scatter_hide_lost = {}
    """.format(
        scatter["cs_scatter_cols_page"],
        scatter["cs_scatter_rows_page"],
        scatter["cs_scatter_x_label"],
        scatter["cs_scatter_y_label"],
        scatter["cs_scatter_mksize"],
        scatter["cs_scatter_scale"],
        scatter["cs_scatter_mk_type"],
        scatter["cs_scatter_mk_start_color"],
        scatter["cs_scatter_mk_end_color"],
        scatter["cs_scatter_markers"],
        scatter["cs_scatter_mk_color"],
        scatter["cs_scatter_mk_edgecolors"],
        scatter["cs_scatter_mk_lost_color"],
        scatter["cs_scatter_hide_lost"],
    )

    fsuv_flower = """
cs_scatter_x_label = {}
cs_scatter_y_label = {}
cs_scatter_flower_mksize = {}  # marker size
cs_scatter_flower_color_grad = {}
cs_scatter_flower_color_start = {}
cs_scatter_flower_color_end = {}
cs_scatter_flower_color_list = {}
cs_scatter_flower_x_label_fn = {}  # y label font
cs_scatter_flower_x_label_fs = {} # x label font size
cs_scatter_flower_x_label_pad = {}  # x label pad
cs_scatter_flower_x_label_weight = {}  # x label weight
cs_scatter_flower_y_label_fn = {}  # y label font
cs_scatter_flower_y_label_fs = {}  # y label font size
cs_scatter_flower_y_label_pad = {}  # y label pad
cs_scatter_flower_y_label_weight = {}  # y label weight
cs_scatter_flower_x_ticks_fn = {}  # x ticks font
cs_scatter_flower_x_ticks_fs = {}  # x ticks font size
cs_scatter_flower_x_ticks_pad = {}  # x ticks pad
cs_scatter_flower_x_ticks_weight = {}  # x ticks font style
cs_scatter_flower_x_ticks_rot = {}  # ticks label rotation
cs_scatter_flower_y_ticks_fn = {}  # x ticks font
cs_scatter_flower_y_ticks_fs = {}  # x ticks font size
cs_scatter_flower_y_ticks_pad = {}  # x ticks pad
cs_scatter_flower_y_ticks_weight = {}  # x ticks font style
cs_scatter_flower_y_ticks_rot = {}
#
    """.format(
        flower["cs_scatter_flower_x_label"],
        flower["cs_scatter_flower_y_label"],
        flower["cs_scatter_flower_mksize"],
        flower["cs_scatter_flower_color_grad"],
        flower["cs_scatter_flower_color_start"],
        flower["cs_scatter_flower_color_end"],
        flower["cs_scatter_flower_color_list"],
        flower["cs_scatter_flower_x_label_fn"],
        flower["cs_scatter_flower_x_label_fs"],
        flower["cs_scatter_flower_x_label_pad"],
        flower["cs_scatter_flower_x_label_weight"],
        flower["cs_scatter_flower_x_label"],
        flower["cs_scatter_flower_y_label_fn"],
        flower["cs_scatter_flower_y_label_fs"],
        flower["cs_scatter_flower_y_label_pad"],
        flower["cs_scatter_flower_y_label_weight"],
        flower["cs_scatter_flower_x_ticks_fn"],
        flower["cs_scatter_flower_x_ticks_fs"],
        flower["cs_scatter_flower_x_ticks_pad"],
        flower["cs_scatter_flower_x_ticks_weight"],
        flower["cs_scatter_flower_x_ticks_rot"],
        flower["cs_scatter_flower_y_ticks_fn"],
        flower["cs_scatter_flower_y_ticks_fs"],
        flower["cs_scatter_flower_y_ticks_pad"],
        flower["cs_scatter_flower_y_ticks_weight"],
        flower["cs_scatter_flower_y_ticks_rot"]
    )

    fsuv_heatmap = """
 DELTA PRE Heat Maps
heat_map_rows = {}
heat_map_vmin = {}
heat_map_vmax = {}
heat_map_x_ticks_fs = {}
heat_map_x_ticks_rot = {}
heat_map_x_ticks_fn = '{}'
heat_map_x_tick_pad = {}
heat_map_y_label_fs = {}
heat_map_y_label_pad = {}
heat_map_y_label_fn = '{}'
heat_map_y_label_weight = '{}'
heat_map_right_margin = {}
heat_map_bottom_margin = {}
heat_map_top_margin = {}
heat_map_cbar_font_size = {}
#
    """.format(
        heat_map["heat_map_rows"],
        heat_map["heat_map_vmin"],
        heat_map["heat_map_vmax"],
        heat_map["heat_map_x_ticks_fs"],
        heat_map["heat_map_x_ticks_rot"],
        heat_map["heat_map_x_ticks_fn"],
        heat_map["heat_map_x_tick_pad"],
        heat_map["heat_map_y_label_fs"],
        heat_map["heat_map_y_label_pad"],
        heat_map["heat_map_y_label_fn"],
        heat_map["heat_map_y_label_weight"],
        heat_map["heat_map_right_margin"],
        heat_map["heat_map_bottom_margin"],
        heat_map["heat_map_top_margin"],
        heat_map["heat_map_cbar_font_size"],
    )

    fsuv_gen2 = """
# Figure Details
fig_width = {}  # Figure width in inches
fig_height = {}  # Figure height in inches
fig_file_type = '{}'  # Figure file type
fig_dpi = {}  # Figure resolution
#
    """.format(
        gen["fig_width"],
        gen["fig_height"],
        gen["fig_file_type"],
        gen["fig_dpi"]
    )

    fout.write(fsuv_general)
    fout.write(fsuv_cs)
    fout.write(fsuv_fit)
    fout.write(fsuv_fasta)
    fout.write(fsuv_csp)
    fout.write(fsuv_pre)
    fout.write(fsuv_plots)
    fout.write(fsuv_tplot)
    fout.write(fsuv_bar_plot)
    fout.write(fsuv_ext)
    fout.write(fsuv_comp)
    fout.write(fsuv_vert)
    fout.write(fsuv_dpre)
    fout.write(fsuv_revo)
    fout.write(fsuv_res_evo)
    fout.write(fsuv_scatter)
    fout.write(fsuv_flower)
    fout.write(fsuv_heatmap)
    fout.write(fsuv_gen2)
    fout.close()
# json_to_fsuv(open("/Users/fbssps/PycharmProjects/FarSeer-NMR/current/default_config.json", 'r'))

