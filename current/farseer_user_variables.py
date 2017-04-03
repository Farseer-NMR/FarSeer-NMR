import sys
#
spectra_path = sys.argv[1]  # where spectra peaklists .csv files are stored - relative path
#
logfile_name = 'file.log' #  the name of the log file
#
has_sidechains = False  # Are there sidechain entries in the peaklists?
use_sidechains = False  # Do you want to analyse those sidechains?
#
perform_cs_correction = False  # Aligns peaklists to a specific residue in the reference spectra
cs_correction_res_ref = 76  # To which residue?
#
expand_lost_yy = False  # Considers lost residue over yy references and xx reference
expand_lost_zz = False  # Considers lost residue over zz references and xx reference
#
applyFASTA = True  # complete the sequence with a FASTA file?
FASTAstart = 1  # Residue number for the first residue in the FASTA file?
#
do_titvar1 = True  # Analyse data in the first titration condition (dimension)
do_titvar2 = True  # Analyse data in the second titration condition (dimension)
do_titvar3 = False  # Analyse data in the thrid titration condition (dimension)
perform_comparisons = True  # Compares data obtained for condition experiment.
#
csp_alpha4res = 0.14  # General alpha normalization factor for CSP
csp_res_exceptions = {'G': 0.2}  # exceptions for the normalization factor
cs_lost = 'prev'  # how to represent the lost residues in CSPs [prev/full]
#
chimera_att_select_format = ':'  # format to select residues in Chimera
#
perform_resevo_fit = True  # Fit parameter evolution over titration experiment
fit_x_values = [0, 250, 500] # values for the x axis in the fitting procedure (ex. Ligand concentration)
# Perform PRE analysis
apply_PRE_analysis = False
#
plots_PosF1_delta = True # Plot nuclei 1 shift perturbation data
plots_PosF2_delta = True # Plot nuclei 2 shift perturbation data
plots_CSP = True  # Plot combined chemical shift perturbation data
plots_Height_ratio = True  # Plot Height ratio data
plots_Volume_ratio = True  # Plot Volume ratio data
#
plots_extended_bar = True  # Represent data in Extended Bar Plot style
plots_compacted_bar = True  # Represent data in Compacted Bar Plot style
plots_vertical_bar = True  # Represent data in Vertical Bar Plot style
plots_residue_evolution = True  # Represent Data Evolution per Residue style
plots_cs_scatter = True  # Represent chemical shift scatter data
#
yy_label_PosF1_delta = 'ppm'  # y axis label for nuclei 1
yy_label_PosF2_delta = 'ppm'  # y axis label for nuclei 2
yy_label_CSP = 'CSPs (ppm)'  # y axis label for combined chemical shift
yy_label_Height_ratio = 'Hi/H0'  # y axis label for height ratio
yy_label_Volume_ratio = 'Vi/V0'  # y axis label for volume ratio
#
calccol_name_PosF1_delta = 'H1_delta'  # column name for nuclei 1
calccol_name_PosF2_delta = 'N15_delta'  # column name for nuclei 2
calccol_name_CSP = 'CSP'  # column name for combined chemical shift perturbation data
calccol_name_Height_ratio = 'Height_ratio'  # column name for Height Ratio data
calccol_name_Volume_ratio = 'Vol_ratio'  # column name for Volume Ratio data
#
yy_scale_PosF1_delta = 0.06  # y axis sacle for nuclei 1
yy_scale_PosF2_delta = 0.2  # y axis scale for nuclei 2
yy_scale_CSP = 0.1  # y axis sacle for combined chemical shift
yy_scale_Height_ratio = 1.05 # y axis scale for height ratio
yy_scale_Volume_ratio = 1.05 # y axis scale for volume ratio
#
represent_user_marks = False  # draws user defined marks over bars in plots
user_marks_dict = {
    'foo': 'f',
    'bar': 'b',
    'zoo':'z'
}  # keys: the string in 'Details' column in input data, value: the character to be drawn
#
# Extended Bar Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
ext_bar_cols_page = 1  # number of columns of subplots per page
ext_bar_rows_page = 6  # number of rows of subplots per page
ext_bar_color_measured = 'k'  # color of the bars
ext_bar_apply_status_2_bar_color = True  # applies color to the 'lost' residue bars
ext_bar_color_lost = 'red'  # color of the 'lost' residues bar
ext_bar_color_unassigned = 'grey'  # color of unassigned residues
ext_bar_bar_width = 0.7  # bar width 
ext_bar_bar_alpha = 1  # bar transparency. 0-1 (transparent-opaque)
ext_bar_bar_linewidth = 0  # bar line width
ext_bar_title_y = 1.05  # subplot title padding
ext_bar_title_fn = 'Arial'  # subplot tittle font
ext_bar_title_fs = 8  # subplot tittle font size
ext_bar_plot_threshold = True  # applies stdev threshold
ext_bar_plot_threshold_color = 'red'  # stdev thresold color
ext_bar_plot_threshold_lw = 0.5  # stdev threshold width
ext_bar_x_label_fn='Arial'  # x label font
ext_bar_x_label_weight='bold'  # x label weight
ext_bar_x_label_fs=8  # x label fontsize
ext_bar_x_label_pad=2  # x label pad
ext_bar_x_ticks_fn = 'monospace'  # x ticks font type
ext_bar_x_ticks_fs = 6  # x ticks font size
ext_bar_x_ticks_rot = 90  # x ticks rotation
ext_bar_x_ticks_pad = 2  # x ticks pad
ext_bar_y_label_fn='Arial'  # y label font
ext_bar_y_label_fs=8  # y label font size
ext_bar_y_label_pad=2  # y label pad
ext_bar_y_label_weight='bold'  # y label weight
ext_bar_y_ticks_fn = 'Arial'  # y label font
ext_bar_y_ticks_fs = 9  # y ticks font size
ext_bar_y_ticks_pad = 3  # y ticks pad
ext_bar_y_ticks_len=2  # y ticks length
ext_bar_y_grid_color = 'lightgrey'  # grid color
ext_bar_mark_prolines = True  # mark prolines
ext_bar_proline_mark = 'P' # Proline marks
ext_bar_mark_user_details = True  # mark user details
ext_bar_mark_fs = 3  # mark font size
ext_bar_pre_color='green'  # theoretical PRE line color
ext_bar_pre_lw=1  # theoretical PRE line width
#
# Compacted Bar Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
comp_bar_cols_page = 3  # number of columns of subplots per page
comp_bar_rows_page = 5  # number of rows of subplots per page
comp_bar_color_measured='k'  # color of the bars
comp_bar_apply_status_2_bar_color=True  # applies color to the 'lost' residue bars
comp_bar_color_lost='red'  # color of the 'lost' residues bar
comp_bar_color_unassigned='grey'  # color of unassigned residues
comp_bar_bar_width=0.7  # bar width 
comp_bar_bar_alpha=1  # bar transparency. 0-1 (transparent-opaque)
comp_bar_bar_linewidth=0  # bar line width
comp_bar_title_y=1.01  # subplot title padding
comp_bar_title_fn='Arial'  # subplot tittle font
comp_bar_title_fs=8  # subplot tittle font size
comp_bar_plot_threshold=True  # applies stdev threshold
comp_bar_plot_threshold_color='red'  # stdev thresold color
comp_bar_plot_threshold_lw=1  # stdev threshold width
comp_bar_x_label_fn='Arial'  # x label font
comp_bar_x_label_fs=8  # x label fontsize
comp_bar_x_label_pad=2  # x label pad
comp_bar_x_label_weight='bold'  # y label weight
comp_bar_x_ticks_fn='Arial'  # x ticks font type
comp_bar_x_ticks_fs=6  # x ticks font size
comp_bar_x_ticks_rot=0  # x ticks rotation
comp_bar_x_ticks_pad=1  # x ticks pad
comp_bar_y_label_fn='Arial'  # y label font
comp_bar_y_label_weight='bold'  # y label weight
comp_bar_y_label_fs=8  # y label font size
comp_bar_y_label_pad=2  # y label pad
comp_bar_y_ticks_fs=6  # y ticks font size
comp_bar_y_ticks_pad=3  # y ticks pad
comp_bar_y_ticks_len=2  # y ticks length
comp_bar_y_grid_color='grey'  # grid color
comp_bar_mark_prolines=True  # mark prolines
comp_bar_proline_mark='P'  # Proline marks
comp_bar_mark_user_details=True  # mark user details
comp_bar_mark_fs=3  # mark font size
comp_bar_unassigned_shade=True  # displays shade for unassigned residues
comp_bar_unassigned_shade_color='grey'  # unassigned residues shade color
comp_bar_unassigned_shade_alpha=0.5  # unassigned residues shade transparency.
comp_bar_pre_color='blue'  # theoretical PRE line color
comp_bar_pre_lw=1  # theoretical PRE line width
#
# Vertical Bar plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
vert_bar_cols_page = 5  # number of columns of subplots per page
vert_bar_rows_page = 2  # number of rows of subplots per page
vert_bar_color_measured = 'k'  # color of the bars
vert_bar_apply_status_2_bar_color = True  # applies color to the 'lost' residue bars
vert_bar_color_lost = 'red'  # color of the 'lost' residues bar
vert_bar_color_unassigned = 'grey'  # color of unassigned residues
vert_bar_bar_width = 0.7  # bar width 
vert_bar_bar_alpha = 1  # bar transparency. 0-1 (transparent-opaque)
vert_bar_bar_linewidth = 0 # bar line width
vert_bar_title_y = 1.01  # subplot title padding
vert_bar_title_fn = 'Arial'  # subplot tittle font
vert_bar_title_fs = 8  # subplot tittle font size
vert_bar_plot_threshold = True  # applies stdev threshold
vert_bar_plot_threshold_color = 'red'  # stdev thresold color
vert_bar_plot_threshold_lw = 1  # stdev threshold width
vert_bar_x_label_fn='Arial'  # x label font
vert_bar_x_label_fs=8  # x label fontsize
vert_bar_x_label_pad=2  # x label pad
vert_bar_x_label_weight='bold'  # x label weight
vert_bar_x_ticks_fn = 'monospace'  # x ticks font type
vert_bar_x_ticks_fs = 5  # x ticks font size
vert_bar_x_ticks_pad = 2  # x ticks pad
vert_bar_x_ticks_len=2  # x ticks len
vert_bar_y_label_fn='Arial'  # y label font
vert_bar_y_label_fs=8  # y label font size
vert_bar_y_label_pad=9  # y label pad
vert_bar_y_label_weight='bold'  #  label weight
vert_bar_y_label_rot=-90  # y label rotation
vert_bar_y_ticks_fn='monospace'  # y ticks font
vert_bar_y_ticks_fs =4  # y ticks font size
vert_bar_y_ticks_pad=1  # y ticks pad
vert_bar_y_ticks_rot=0  # y ticks rotation
vert_bar_x_grid_color = 'lightgrey'  # grid color
vert_bar_mark_prolines = True  # mark proline residues
vert_bar_proline_mark = 'P'  # mark for proline residues
vert_bar_mark_user_details = True  # mark user details
vert_bar_mark_fs = 3  # mark font size
#
# Data Evolution per Residue Plot
# use a combination of cols_page and rows_page to achieve desired figure ratio
res_evo_cols_page = 5  # number of columns of subplots per page
res_evo_rows_page = 8  # number of rows of subplots per page
res_evo_title_y=0.97  # subplot title pad
res_evo_title_fn='Arial'  # subplot title font
res_evo_title_fs=8  # subplot title font size
res_evo_x_label='[Ligand]'  # x label
res_evo_set_x_values=True  # use user defined x values? Necessary for titration fitting.
res_evo_x_label_fn='Arial'  # x label font
res_evo_x_label_fs=6  # x label font size
res_evo_x_label_pad=2  # x label pad
res_evo_x_label_weight='normal'  # x label weight
res_evo_x_ticks_pad=1  # x ticks pad
res_evo_x_ticks_fs=7  # x ticks font size
res_evo_y_label_fn='Arial'  # y label font
res_evo_y_label_fs=6  # y label font size
res_evo_y_label_pad=2  # y label pad
res_evo_y_label_weight='normal'  # y label weight
res_evo_y_ticks_pad=1  # y ticks pad
res_evo_y_ticks_fs=7  # y ticks font size
res_evo_line_style='-'  # data line style
res_evo_plot_color='r'  # data line color
res_evo_marker_style='o'  # data marker style
res_evo_marker_color='darkred'  # data marker color
res_evo_marker_size=3  # data marker size
res_evo_line_width=1  # data line width
res_evo_fill_between=True  # draw data shade
res_evo_fill_color='pink'  # shade color
res_evo_fill_alpha=0.5  # shade transparency (0-1)
res_evo_fit_line_color = 'black'  # fit line color
res_evo_fit_line_width = 1  # fit line width
#
# Chemical Shift Scatter Plot
cs_scatter_cols_page = 5  # number of columns of subplots per page
cs_scatter_rows_page = 7  # number of rows of subplots per page
cs_scatter_title_y=0.97  # subplot title pad
cs_scatter_title_fn='Arial'  # subplot font
cs_scatter_title_fs=8  # subplot title font size
cs_scatter_x_label_fn='Arial'  # x label font
cs_scatter_x_label_fs=6  # x label font size
cs_scatter_x_label_pad=1.8  # x label pad
cs_scatter_x_label_weight='normal'  # x label weight
cs_scatter_x_ticks_pad=1  # x ticks pad
cs_scatter_x_ticks_fs=5  # x ticks font size
cs_scatter_y_label_fn='Arial'  # y label font
cs_scatter_y_label_fs=6  # y label font size
cs_scatter_y_label_pad=2  # y label pad
cs_scatter_y_label_weight='normal'  # y label weight
cs_scatter_y_ticks_pad=1  # y ticks pad
cs_scatter_y_ticks_fs=5  # y ticks font size
cs_scatter_mksize=20  # marker size
cs_scatter_scale=0.01  # scale representation
cs_scatter_mk_type='color' # 'color' or 'shape'
cs_scatter_mk_start_color='#cdcdcd' # start color for gradient [in hex notation] - color style
cs_scatter_mk_end_color='#000000' # end color for gradient [in hex notation] - color style
cs_scatter_mk_lost_color='red'  # color for lost data points - color style
cs_scatter_markers=['^','>','v','<','s','p','h','8','*','D']  # sequencial markers
cs_scatter_mk_color='none'  # marker inside color for shape style
cs_scatter_mk_edgecolors='black'  # marker edge color for shape style
cs_scatter_mk_edge_lost='red'  # marker edge color for lost data points in shape style.
#
# Figure Details
fig_width = 8.69  # Figure width in inches
fig_height = 11.69  # Figure height in inches
fig_file_type = 'pdf'  # Figure file type
fig_dpi = 300  # Figure resolution
#



import farseermain
