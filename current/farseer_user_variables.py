import sys
import shutil
import os
#
spectra_path = sys.argv[1]  # where spectra peaklists .csv files are stored - relative path
print(spectra_path)
#
logfile_name = 'file.log' #  the name of the log file
#
has_sidechains = False  # Are there sidechain entries in the peaklists?
use_sidechains = False  # Do you want to analyse those sidechains?
#
perform_cs_correction = False  # Normalize peaklists to specific residue, CS for that residue over a titration will be zero. # i.e. applies an internal reference
cs_correction_res_ref = '76'  # To which residue?
#
expand_lost_yy = False  # Analyse lost residue over yy
expand_lost_zz = False  # Analyse lost residues over zz
#
applyFASTA = True  # complete the sequence with a FASTA file?
FASTAstart = 1  # What is the residue number for the first residue in the FASTA file?
#
do1D = True  # Analyse data in the first dimension (for the 1st condition)
do2D = True  # Analyse data in the second dimension (for the 2nd condition)
do3D = True  # Analyse data in the thrid dimension (for the 3rd condition)
perform_controls = True  # concatenates data obtained for experiment in each dimension.
#
csp_alpha4res = 0.14  # alpha normalization factor for CS
csp_res_exceptions = {'G': 0.2}  # exception for the normalization factor
cs_lost = 'prev'  # how to represent the lost residues in CSPs [prev/full]
#
chimera_att_select_format = ':'  # format to select residues in Chimera
#
perform_resevo_fitting = False  # Fit parameter evolution over titration experiment
fitting_protein_concentration = 50  # P0 value for fiting funtion (same units as x_values)
fitting_x_values = [0, 12.5, 25, 37.5, 50.0, 75.0, 100.0, 150.0, 300.0]  # x values for parameter evolution (ex. ligand concentration)
fit_line_color = 'black'
fit_line_width = 1
#
plots_extended_bar = False
plots_compacted_bar = False
plots_vertical_bar = False
plots_residue_evolution = False
#
plots_PosF1_delta = True
plots_PosF2_delta = True
plots_CSP = True
plots_Height_ratio = True
plots_Volume_ratio = True
#
yy_label_PosF1_delta = 'ppm'
yy_label_PosF2_delta = 'ppm'
yy_label_CSP = 'CSPs (ppm)'
yy_label_Height_ratio = 'Hi/H0'
yy_label_Volume_ratio = 'Vi/V0'
#
calccol_name_PosF1_delta = 'H1_delta'
calccol_name_PosF2_delta = 'N15_delta'
calccol_name_CSP = 'CSP'
calccol_name_Height_ratio = 'Height_ratio'
calccol_name_Volume_ratio = 'Vol_ratio'
#
yy_scale_PosF1_delta = 0.1
yy_scale_PosF2_delta = 0.25
yy_scale_CSP = 0.05
yy_scale_Height_ratio = 1.0
yy_scale_Volume_ratio = 1.0
#
represent_user_marks = False  # draws over bars user defined marks
negative_marks_scaling = 0.15  # scaling factor to adjust drawing for negative markers
user_marks_dict = {
    'H0': 'H',
    'V0': 'V',
    'low':'l',
    'p1': '1',
    'p2': '2',
    'p3': '3',
    'p4': '4',
    'p5': '5',
}  # keys: the string in 'Details' column in input data, value: the character to be drawn
#
ext_bar_cols_page = 1
ext_bar_rows_page = 6
ext_bar_apply_status_2_bar_color = True
ext_bar_color_measured = 'k'
ext_bar_color_lost = 'red'
ext_bar_color_unassigned = 'grey'
ext_bar_bar_width = 0.7
ext_bar_bar_alpha = 1
ext_bar_bar_linewidth = 0
ext_bar_title_y = 1.05
ext_bar_title_fs = 10
ext_bar_title_fn = 'Arial'
ext_bar_plot_threshold = True
ext_bar_plot_threshold_color = 'red'
ext_bar_plot_threshold_lw = 1
ext_bar_x_ticks_rot = 90
ext_bar_x_ticks_fs = 6
ext_bar_x_ticks_fn = 'monospace'
ext_bar_x_ticks_pad = 0.1
ext_bar_y_ticks_fs = 9
ext_bar_y_grid_color = 'grey'
ext_bar_mark_prolines = True
ext_bar_proline_mark = 'P'
ext_bar_mark_user_details = True
#
comp_bar_cols_page = 3
comp_bar_rows_page = 5
comp_bar_apply_status_2_bar_color=True
comp_bar_color_measured='k'
comp_bar_color_lost='red'
comp_bar_color_unassigned='grey'
comp_bar_bar_width=0.7
comp_bar_bar_alpha=1
comp_bar_bar_linewidth=0
comp_bar_title_y=1.01
comp_bar_title_fs=8
comp_bar_title_fn='Arial'
comp_bar_plot_threshold=True
comp_bar_plot_threshold_color='red'
comp_bar_plot_threshold_lw=1
comp_bar_x_ticks_rot=0
comp_bar_x_ticks_fs=6
comp_bar_x_ticks_fn='Arial'
comp_bar_x_ticks_pad=1
comp_bar_y_ticks_fs=9
comp_bar_y_ticks_pad=-3
comp_bar_y_grid_color='grey'
comp_bar_mark_prolines=True
comp_bar_proline_mark='P'
comp_bar_mark_user_details=True
comp_bar_mark_fs=3
comp_bar_unassigned_shade=True
comp_bar_unassigned_shade_color='grey'
comp_bar_unassigned_shade_alpha=0.5
#
vert_bar_cols_page = 6
vert_bar_rows_page = 1
#
res_evo_cols_page = 4
res_evo_rows_page = 6
res_evo_title_y=0.97
res_evo_title_fs=8
res_evo_title_fn='Arial'
res_evo_set_x_values=True  # depends on fitting_x_values variable
res_evo_x_ticks_pad=1
res_evo_x_ticks_fs=7
res_evo_xlabel_flag=False
res_evo_y_ticks_pad=1
res_evo_y_ticks_fs=7
res_evo_line_style='-'
res_evo_plot_color='r'
res_evo_marker_style='o'
res_evo_marker_color='darkred'
res_evo_marker_size=3
res_evo_line_width=1
res_evo_fill_between=True
res_evo_fill_color='pink'
res_evo_fill_alpha=0.5
#
fig_file_type = 'pdf'
fig_dpi = 300
#


cwd = os.getcwd()
script_wd = os.path.dirname(os.path.realpath(__file__))

print('-> Farseer base dictory: {}'.format(script_wd))
print('-> current working directiory: {}'.format(cwd))

shutil.make_archive(cwd+'/farseer_used_version', 'zip', script_wd)
import farseermain
