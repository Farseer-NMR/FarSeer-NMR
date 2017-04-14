import json

def fsuv_to_json(fsuv):


    pass

def json_to_fsuv(json_file):

    js = json.load(json_file)
    fout = open("test_user_variables.py", 'w')
    gen = js["general_settings"]
    fit = js["fitting_settings"]
    cs = js["cs_settings"]
    csp = js["csp_settings"]
    fasta = js["fasta_settings"]
    pre = js["pre_settings"]
    ext = js["extended_bar_settings"]
    comp = js["compact_bar_settings"]
    vert = js["vert_bar_settings"]
    pf1 = js["plots_PosF1_settings"]
    pf2 = js["plots_PosF2_settings"]
    p_csp = js["plots_CSP_settings"]
    p_height = js["plots_Height_ratio_settings"]
    p_vol = js["plots_Volume_ratio_settings"]
    res_evo = js["res_evo_settings"]
    user = js["user_mark_settings"]
    scatter = js["cs_scatter_settings"]
    heat_map = js["heat_map_settings"]
    dpre = js["dpre_osci_settings"]


    fsuv1 = """import sys
#
spectra_path = {}  # where spectra peaklists .csv files are stored - relative path
#
logfile_name = '{}'  # the name of the log file
#
has_sidechains = {}  # Are there sidechain entries in the peaklists?
use_sidechains = {}  # Do you want to analyse those sidechains?
#
perform_cs_correction = {}  # Aligns peaklists to a specific residue in the reference spectra
cs_correction_res_ref = {}  # To which residue?
#
expand_lost_yy = {}  # Considers lost residue over yy references and xx reference
expand_lost_zz = {}  # Considers lost residue over zz references and xx reference
#
applyFASTA = {}  # complete the sequence with a FASTA file?
FASTAstart = {}  # Residue number for the first residue in the FASTA file?
#
do_cond1 = {}  # Analyse data in the first titration condition (dimension)
do_cond2 = {}  # Analyse data in the second titration condition (dimension)
do_cond3 = {}  # Analyse data in the thrid titration condition (dimension)
perform_comparisons = True  # Compares data obtained for condition experiment.
#
csp_alpha4res = {}  # General alpha normalization factor for CSP
csp_res_exceptions = {}  # exceptions for the normalization factor
cs_lost = {}  # how to represent the lost residues in CSPs [prev/full]
#
chimera_att_select_format = ':'  # format to select residues in Chimera
#
perform_resevo_fit = {}  # Fit parameter evolution over titration experiment
fit_x_values = [0, 250, 500]  # values for the x axis in the fitting procedure (ex. Ligand concentration)
# Perform PRE analysis

apply_PRE_analysis = {}
apply_smooth = {}
gaussian_stddev = {}
gauss_x_size = {}
d_pre_y_max = {}  # y axis max scale
d_pre_y_label = {}
d_pre_rows = {}
pre_color = {}  # theoretical PRE line color
pre_lw = {}  # theoretical PRE line width
tag_color = {}
tag_lw = {}
tag_ls = {}

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
represent_user_marks = {}  # draws user defined marks over bars in plots
user_marks_dict = {}
# keys: the string in 'Details' column in input data, value: the character to be drawn
#
# Extended Bar Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
ext_bar_cols_page = {}  # number of columns of subplots per page
ext_bar_rows_page = {}  # number of rows of subplots per page
ext_bar_color_measured = '{}'  # color of the bars
ext_bar_apply_status_2_bar_color = {}  # applies color to the 'lost' residue bars
ext_bar_color_lost = '{}'  # color of the 'lost' residues bar
ext_bar_color_unassigned = '{}'  # color of unassigned residues
ext_bar_bar_width = {}  # bar width
ext_bar_bar_alpha = {}  # bar transparency. 0-1 (transparent-opaque)
ext_bar_bar_linewidth = {}  # bar line width
ext_bar_title_y = {}  # subplot title padding
ext_bar_title_fn = '{}'  # subplot tittle font
ext_bar_title_fs = {}  # subplot tittle font size
ext_bar_plot_threshold = {}  # applies stdev threshold
ext_bar_plot_threshold_color = '{}'  # stdev thresold color
ext_bar_plot_threshold_lw = {}  # stdev threshold width
ext_bar_x_label_fn = '{}'  # x label font
ext_bar_x_label_weight = '{}'  # x label weight
ext_bar_x_label_fs = {}  # x label fontsize
ext_bar_x_label_pad = {}  # x label pad
ext_bar_x_ticks_fn = '{}'  # x ticks font type
ext_bar_x_ticks_fs = {}  # x ticks font size
ext_bar_x_ticks_rot = {}  # x ticks rotation
ext_bar_x_ticks_pad = {}  # x ticks pad
ext_bar_y_label_fn = '{}'  # y label font
ext_bar_y_label_fs = {}  # y label font size
ext_bar_y_label_pad = {}  # y label pad
ext_bar_y_label_weight = '{}'  # y label weight
ext_bar_y_ticks_fn = '{}'  # y label font
ext_bar_y_ticks_fs = {}  # y ticks font size
ext_bar_y_ticks_pad = {}  # y ticks pad
ext_bar_y_ticks_len = {}  # y ticks length
ext_bar_y_grid_color = '{}'  # grid color
ext_bar_mark_prolines = {}  # mark prolines
ext_bar_proline_mark = '{}'  # Proline marks
ext_bar_mark_user_details = {}  # mark user details
ext_bar_mark_fs = {}  # mark font size
#
# Compacted Bar Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
comp_bar_cols_page = {}  # number of columns of subplots per page
comp_bar_rows_page = {}  # number of rows of subplots per page
comp_bar_color_measured = '{}'  # color of the bars
comp_bar_apply_status_2_bar_color = {}  # applies color to the 'lost' residue bars
comp_bar_color_lost = '{}'  # color of the 'lost' residues bar
comp_bar_color_unassigned = '{}'  # color of unassigned residues
comp_bar_bar_width = {}  # bar width
comp_bar_bar_alpha = {}  # bar transparency. 0-1 (transparent-opaque)
comp_bar_bar_linewidth = {}  # bar line width
comp_bar_title_y = {}  # subplot title padding
comp_bar_title_fn = '{}'  # subplot tittle font
comp_bar_title_fs = {}  # subplot tittle font size
comp_bar_plot_threshold = {}  # applies stdev threshold
comp_bar_plot_threshold_color = '{}'  # stdev thresold color
comp_bar_plot_threshold_lw = {}  # stdev threshold width
comp_bar_x_label_fn = '{}'  # x label font
comp_bar_x_label_fs = {}  # x label fontsize
comp_bar_x_label_pad = {}  # x label pad
comp_bar_x_label_weight = '{}'  # y label weight
comp_bar_x_ticks_fn = '{}'  # x ticks font type
comp_bar_x_ticks_fs = {}  # x ticks font size
comp_bar_x_ticks_rot = {}  # x ticks rotation
comp_bar_x_ticks_pad = {}  # x ticks pad
comp_bar_y_label_fn = '{}'  # y label font
comp_bar_y_label_weight = '{}'  # y label weight
comp_bar_y_label_fs = {}  # y label font size
comp_bar_y_label_pad = {}  # y label pad
comp_bar_y_ticks_fs = {}  # y ticks font size
comp_bar_y_ticks_pad = {}  # y ticks pad
comp_bar_y_ticks_len = {}  # y ticks length
comp_bar_y_grid_color = '{}'  # grid color
comp_bar_mark_prolines = {}  # mark prolines
comp_bar_proline_mark = '{}'  # Proline marks
comp_bar_mark_user_details = {}  # mark user details
comp_bar_mark_fs = {}  # mark font size
comp_bar_unassigned_shade = {}  # displays shade for unassigned residues
comp_bar_unassigned_shade_color = '{}'  # unassigned residues shade color
comp_bar_unassigned_shade_alpha = {}  # unassigned residues shade transparency.
#
# Vertical Bar plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
vert_bar_cols_page = {}  # number of columns of subplots per page
vert_bar_rows_page = {}  # number of rows of subplots per page
vert_bar_color_measured = '{}'  # color of the bars
vert_bar_apply_status_2_bar_color = {}  # applies color to the 'lost' residue bars
vert_bar_color_lost = '{}'  # color of the 'lost' residues bar
vert_bar_color_unassigned = '{}'  # color of unassigned residues
vert_bar_bar_width = {}  # bar width
vert_bar_bar_alpha = {}  # bar transparency. 0-1 (transparent-opaque)
vert_bar_bar_linewidth = {}  # bar line width
vert_bar_title_y = {}  # subplot title padding
vert_bar_title_fn = '{}'  # subplot tittle font
vert_bar_title_fs = {}  # subplot title font size
vert_bar_plot_threshold = {}  # applies stdev threshold
vert_bar_plot_threshold_color = '{}'  # stdev thresold color
vert_bar_plot_threshold_lw = {}  # stdev threshold width
vert_bar_x_label_fn = '{}'  # x label font
vert_bar_x_label_fs = {}  # x label fontsize
vert_bar_x_label_pad = {}  # x label pad
vert_bar_x_label_weight = '{}'  # x label weight
vert_bar_x_ticks_fn = '{}'  # x ticks font type
vert_bar_x_ticks_fs = {}  # x ticks font size
vert_bar_x_ticks_pad = {}  # x ticks pad
vert_bar_x_ticks_len = {}  # x ticks len
vert_bar_y_label_fn = '{}'  # y label font
vert_bar_y_label_fs = {}  # y label font size
vert_bar_y_label_pad = {}  # y label pad
vert_bar_y_label_weight = '{}'  # label weight
vert_bar_y_label_rot = {}  # y label rotation
vert_bar_y_ticks_fn = '{}'  # y ticks font
vert_bar_y_ticks_fs = {}  # y ticks font size
vert_bar_y_ticks_pad = {}  # y ticks pad
vert_bar_y_ticks_rot = {}  # y ticks rotation
vert_bar_x_grid_color = '{}'  # grid color
vert_bar_mark_prolines = {}  # mark proline residues
vert_bar_proline_mark = '{}'  # mark for proline residues
vert_bar_mark_user_details = {}  # mark user details
vert_bar_mark_fs = {}  # mark font size
#
# Data Evolution per Residue Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
res_evo_cols_page = {}  # number of columns of subplots per page
res_evo_rows_page = {}  # number of rows of subplots per page
res_evo_title_y = {}  # subplot title pad
res_evo_title_fn = '{}'  # subplot title font
res_evo_title_fs = {}  # subplot title font size
res_evo_x_label = '{}'  # x label
res_evo_set_x_values = {}  # use user defined x values? Necessary for titration fitting.
res_evo_x_label_fn = '{}'  # x label font
res_evo_x_label_fs = {}  # x label font size
res_evo_x_label_pad = {}  # x label pad
res_evo_x_label_weight = '{}'  # x label weight
res_evo_x_ticks_pad = {}  # x ticks pad
res_evo_x_ticks_fs = {}  # x ticks font size
res_evo_y_label_fn = '{}'  # y label font
res_evo_y_label_fs = {}  # y label font size
res_evo_y_label_pad = {}  # y label pad
res_evo_y_label_weight = '{}'  # y label weight
res_evo_y_ticks_pad = {}  # y ticks pad
res_evo_y_ticks_fs = {}  # y ticks font size
res_evo_line_style = '{}'  # data line style
res_evo_plot_color = '{}'  # data line color
res_evo_marker_style = '{}'  # data marker style
res_evo_marker_color = '{}'  # data marker color
res_evo_marker_size = {}  # data marker size
res_evo_line_width = {}  # data line width
res_evo_fill_between = {}  # draw data shade
res_evo_fill_color = '{}'  # shade color
res_evo_fill_alpha = {}  # shade transparency (0-1)
res_evo_fit_line_color = '{}'  # fit line color
res_evo_fit_line_width = {}  # fit line width
#
# Chemical Shift Scatter Plot
cs_scatter_cols_page = {}  # number of columns of subplots per page
cs_scatter_rows_page = {}  # number of rows of subplots per page
cs_scatter_title_y = {}  # subplot title pad
cs_scatter_title_fn = '{}'  # subplot font
cs_scatter_title_fs = {}  # subplot title font size
cs_scatter_x_label_fn = '{}'  # x label font
cs_scatter_x_label_fs = {}  # x label font size
cs_scatter_x_label_pad = {}  # x label pad
cs_scatter_x_label_weight = '{}'  # x label weight
cs_scatter_x_ticks_pad = {}  # x ticks pad
cs_scatter_x_ticks_fs = {}  # x ticks font size
cs_scatter_y_label_fn = '{}'  # y label font
cs_scatter_y_label_fs = {}  # y label font size
cs_scatter_y_label_pad = {}  # y label pad
cs_scatter_y_label_weight = '{}'  # y label weight
cs_scatter_y_ticks_pad = {}  # y ticks pad
cs_scatter_y_ticks_fs = {}  # y ticks font size
cs_scatter_mksize = {}  # marker size
cs_scatter_scale = {}  # scale representation
cs_scatter_mk_type = '{}'  # 'color' or 'shape'
cs_scatter_mk_start_color = '{}'  # start color for gradient [in hex notation] - color style
cs_scatter_mk_end_color = '{}'  # end color for gradient [in hex notation] - color style
cs_scatter_mk_lost_color = '{}'  # color for lost data points - color style
cs_scatter_markers = {}  # sequential markers
cs_scatter_mk_color = '{}'  # marker inside color for shape style
cs_scatter_mk_edgecolors = '{}'  # marker edge color for shape style
cs_scatter_mk_edge_lost = '{}'  # marker edge color for lost data points in shape style.
#
# DELTA PRE Heat Maps
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
        gen["spectrum_path"],
        gen["logfile_name"],
        gen["has_sidechains"],
        gen["use_sidechains"],
        cs["perform_cs_correction"],
        cs["cs_correction_res_ref"],
        fit["expand_lost_yy"],
        fit["expand_lost_zz"],
        fasta["applyFASTA"],
        fasta["FASTAstart"],
        fit["do_titvar1"],
        fit["do_titvar2"],
        fit["do_titvar3"],
        csp["csp_res4alpha"],
        csp["csp_res_exceptions"],
        csp["cs_lost"],
        fit["perform_resevo_fitting"],
        pre["apply_PRE_analysis"],
        pre["apply_smooth"],
        pre["gaussian_stdev"],
        pre["gauss_x_size"],
        pre["d_pre_y_max"],
        pre["d_pre_y_label"],
        pre["d_pre_rows"],
        pre["pre_color"],
        pre["pre_lw"],
        pre["tag_color"],
        pre["tag_lw"],
        pre["tag_ls"],
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
        fit["include_user_annotations"],
        user,
        ext["ext_bar_cols_page"],
        ext["ext_bar_rows_page"],
        ext["ext_bar_color_measured"],
        ext["ext_bar_apply_status_2_bar_color"],
        ext["ext_bar_color_lost"],
        ext["ext_bar_color_unassigned"],
        ext["ext_bar_bar_width"],
        ext["ext_bar_bar_alpha"],
        ext["ext_bar_bar_linewidth"],
        ext["ext_bar_title_y"],
        ext["ext_bar_title_fn"],
        ext["ext_bar_title_fs"],
        ext["ext_bar_plot_threshold"],
        ext["ext_bar_plot_threshold_color"],
        ext["ext_bar_plot_threshold_lw"],
        ext["ext_bar_x_label_fn"],
        ext["ext_bar_x_label_weight"],
        ext["ext_bar_x_label_fs"],
        ext["ext_bar_x_label_pad"],
        ext["ext_bar_x_ticks_fn"],
        ext["ext_bar_x_ticks_fs"],
        ext["ext_bar_x_ticks_rot"],
        ext["ext_bar_x_ticks_pad"],
        ext["ext_bar_y_label_fn"],
        ext["ext_bar_y_label_fs"],
        ext["ext_bar_y_label_pad"],
        ext["ext_bar_y_label_weight"],
        ext["ext_bar_y_ticks_fn"],
        ext["ext_bar_y_ticks_fs"],
        ext["ext_bar_y_ticks_pad"],
        ext["ext_bar_y_ticks_len"],
        ext["ext_bar_y_grid_color"],
        ext["ext_bar_mark_prolines"],
        ext["ext_bar_proline_mark"],
        ext["ext_bar_mark_user_details"],
        ext["ext_bar_mark_fs"],
        comp["comp_bar_cols_page"],
        comp["comp_bar_rows_page"],
        comp["comp_bar_color_measured"],
        comp["comp_bar_apply_status_2_bar_color"],
        comp["comp_bar_color_lost"],
        comp["comp_bar_color_unassigned"],
        comp["comp_bar_bar_width"],
        comp["comp_bar_bar_alpha"],
        comp["comp_bar_bar_linewidth"],
        comp["comp_bar_title_y"],
        comp["comp_bar_title_fn"],
        comp["comp_bar_title_fs"],
        comp["comp_bar_plot_threshold"],
        comp["comp_bar_plot_threshold_color"],
        comp["comp_bar_plot_threshold_lw"],
        comp["comp_bar_x_label_fn"],
        comp["comp_bar_x_label_fs"],
        comp["comp_bar_x_label_pad"],
        comp["comp_bar_x_label_weight"],
        comp["comp_bar_x_ticks_fn"],
        comp["comp_bar_x_ticks_fs"],
        comp["comp_bar_x_ticks_rot"],
        comp["comp_bar_x_ticks_pad"],
        comp["comp_bar_y_label_fn"],
        comp["comp_bar_y_label_weight"],
        comp["comp_bar_y_label_fs"],
        comp["comp_bar_y_label_pad"],
        comp["comp_bar_y_ticks_fs"],
        comp["comp_bar_y_ticks_pad"],
        comp["comp_bar_y_ticks_len"],
        comp["comp_bar_y_grid_color"],
        comp["comp_bar_mark_prolines"],
        comp["comp_bar_proline_mark"],
        comp["comp_bar_mark_user_details"],
        comp["comp_bar_mark_fs"],
        comp["comp_bar_unassigned_shade"],
        comp["comp_bar_unassigned_shade_color"],
        comp["comp_bar_unassigned_shade_alpha"],
        vert["vert_bar_cols_page"],
        vert["vert_bar_rows_page"],
        vert["vert_bar_color_measured"],
        vert["vert_bar_apply_status_2_bar_color"],
        vert["vert_bar_color_lost"],
        vert["vert_bar_color_unassigned"],
        vert["vert_bar_bar_width"],
        vert["vert_bar_bar_alpha"],
        vert["vert_bar_bar_linewidth"],
        vert["vert_bar_title_y"],
        vert["vert_bar_title_fn"],
        vert["vert_bar_title_fs"],
        vert["vert_bar_plot_threshold"],
        vert["vert_bar_plot_threshold_color"],
        vert["vert_bar_plot_threshold_lw"],
        vert["vert_bar_x_label_fn"],
        vert["vert_bar_x_label_fs"],
        vert["vert_bar_x_label_pad"],
        vert["vert_bar_x_label_weight"],
        vert["vert_bar_x_ticks_fn"],
        vert["vert_bar_x_ticks_fs"],
        vert["vert_bar_x_ticks_pad"],
        vert["vert_bar_x_ticks_len"],
        vert["vert_bar_y_label_fn"],
        vert["vert_bar_y_label_fs"],
        vert["vert_bar_y_label_pad"],
        vert["vert_bar_y_label_weight"],
        vert["vert_bar_y_label_rot"],
        vert["vert_bar_y_ticks_fn"],
        vert["vert_bar_y_ticks_fs"],
        vert["vert_bar_y_ticks_pad"],
        vert["vert_bar_y_ticks_rot"],
        vert["vert_bar_x_grid_color"],
        vert["vert_bar_mark_prolines"],
        vert["vert_bar_proline_mark"],
        vert["vert_bar_mark_user_details"],
        vert["vert_bar_mark_fs"],
        res_evo["res_evo_cols_page"],
        res_evo["res_evo_rows_page"],
        res_evo["res_evo_title_y"],
        res_evo["res_evo_title_fn"],
        res_evo["res_evo_title_fs"],
        res_evo["res_evo_x_label"],
        res_evo["res_evo_set_x_values"],
        res_evo["res_evo_x_label_fn"],
        res_evo["res_evo_x_label_fs"],
        res_evo["res_evo_x_label_pad"],
        res_evo["res_evo_x_label_weight"],
        res_evo["res_evo_x_ticks_pad"],
        res_evo["res_evo_x_ticks_fs"],
        res_evo["res_evo_y_label_fn"],
        res_evo["res_evo_y_label_fs"],
        res_evo["res_evo_y_label_pad"],
        res_evo["res_evo_y_label_weight"],
        res_evo["res_evo_y_ticks_pad"],
        res_evo["res_evo_y_ticks_fs"],
        res_evo["res_evo_line_style"],
        res_evo["res_evo_plot_color"],
        res_evo["res_evo_marker_style"],
        res_evo["res_evo_marker_color"],
        res_evo["res_evo_marker_size"],
        res_evo["res_evo_line_width"],
        res_evo["res_evo_fill_between"],
        res_evo["res_evo_fill_color"],
        res_evo["res_evo_fill_alpha"],
        res_evo["res_evo_fit_line_color"],
        res_evo["res_evo_fit_line_width"],
        scatter["cs_scatter_cols_page"],
        scatter["cs_scatter_rows_page"],
        scatter["cs_scatter_title_y"],
        scatter["cs_scatter_title_fn"],
        scatter["cs_scatter_title_fs"],
        scatter["cs_scatter_x_label_fn"],
        scatter["cs_scatter_x_label_fs"],
        scatter["cs_scatter_x_label_pad"],
        scatter["cs_scatter_x_label_weight"],
        scatter["cs_scatter_x_ticks_pad"],
        scatter["cs_scatter_x_ticks_fs"],
        scatter["cs_scatter_y_label_fn"],
        scatter["cs_scatter_y_label_fs"],
        scatter["cs_scatter_y_label_pad"],
        scatter["cs_scatter_y_label_weight"],
        scatter["cs_scatter_y_ticks_pad"],
        scatter["cs_scatter_y_ticks_fs"],
        scatter["cs_scatter_mksize"],
        scatter["cs_scatter_scale"],
        scatter["cs_scatter_mk_type"],
        scatter["cs_scatter_mk_start_color"],
        scatter["cs_scatter_mk_end_color"],
        scatter["cs_scatter_mk_lost_color"],
        scatter["cs_scatter_markers"],
        scatter["cs_scatter_mk_color"],
        scatter["cs_scatter_mk_edgecolors"],
        scatter["cs_scatter_mk_edge_lost"],
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
    fsuv2 = """
# DELTA PRE oscilations Plot
dpre_osci_width = {}  # scale factor for the width
dpre_osci_title_y = {}  # subplot title pad
dpre_osci_title_fs = {}  # subplot title font size
dpre_osci_title_fn = '{}'  # subplot title font
dpre_osci_dpre_ms = {}  # DELTA_PRE circle marker size
dpre_osci_dpre_alpha = {}  # DELTA_PRE alpha
dpre_osci_smooth_lw = {}  # smooted DPRE line width
dpre_osci_ref_color = '{}'  # color for the reference data
dpre_osci_color_init = '{}'  # initial color for data points color gradient
dpre_osci_color_end = '{}'  # final color for data points color gradient
dpre_osci_x_ticks_fs = {}  # x ticks font size
dpre_osci_x_ticks_fn = '{}'  # xticks font
dpre_osci_y_label_fs = {}  # y axis label font size
dpre_osci_y_label_pad = {}  # y axis label pad
dpre_osci_y_label_fn = '{}'  # y axis label font
dpre_osci_y_label_weight = '{}'  # y axis label weight
dpre_osci_y_ticks_len = {}  # y ticks length
dpre_osci_y_ticks_fs = {}  # y ticks font size
dpre_osci_y_ticks_pad = {}  # y ticks pad
dpre_osci_grid_color = '{}'  # grid color
dpre_osci_res_shade = {}  # applies shade to highlight residues
dpre_osci_res_highlight = {}  # residues to highlight (res, shade width)
dpre_osci_rh_fs = {}  # font size for residue highlight
dpre_osci_rh_y = {}  # y scaling for residue 1-letter representation
#
# Figure Details
fig_width = {}  # Figure width in inches
fig_height = {}  # Figure height in inches
fig_file_type = '{}'  # Figure file type
fig_dpi = {}  # Figure resolution
#
import farseermain""".format(
        dpre["dpre_osci_width"],
        dpre["dpre_osci_title_y"],
        dpre["dpre_osci_title_fs"],
        dpre["dpre_osci_title_fn"],
        dpre["dpre_osci_dpre_ms"],
        dpre["dpre_osci_dpre_alpha"],
        dpre["dpre_osci_smooth_lw"],
        dpre["dpre_osci_ref_color"],
        dpre["dpre_osci_color_init"],
        dpre["dpre_osci_color_end"],
        dpre["dpre_osci_x_ticks_fs"],
        dpre["dpre_osci_x_ticks_fn"],
        dpre["dpre_osci_y_label_fs"],
        dpre["dpre_osci_y_label_pad"],
        dpre["dpre_osci_y_label_fn"],
        dpre["dpre_osci_y_label_weight"],
        dpre["dpre_osci_y_ticks_len"],
        dpre["dpre_osci_y_ticks_fs"],
        dpre["dpre_osci_y_ticks_pad"],
        dpre["dpre_osci_grid_color"],
        dpre["dpre_osci_res_shade"],
        dpre["dpre_osci_res_highlight"],
        dpre["dpre_osci_rh_fs"],
        dpre["dpre_osci_rh_y"],
        gen["fig_width"],
        gen["fig_height"],
        gen["fig_file_type"],
        gen["fig_dpi"]
    )
    fout.write(fsuv1)
    fout.write(fsuv2)
    fout.close()

json_to_fsuv(open("current/default_config.json", 'r'))
