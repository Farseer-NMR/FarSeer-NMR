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


    fsuv = """
    import sys
    #
    spectra_path = {0}  # where spectra peaklists .csv files are stored - relative path
    #
    logfile_name = '{1}  # the name of the log file
    #
    has_sidechains = {2}  # Are there sidechain entries in the peaklists?
    use_sidechains = {3}  # Do you want to analyse those sidechains?
    #
    perform_cs_correction = {4}  # Aligns peaklists to a specific residue in the reference spectra
    cs_correction_res_ref = {5}  # To which residue?
    #
    expand_lost_yy = {6}  # Considers lost residue over yy references and xx reference
    expand_lost_zz = {7}  # Considers lost residue over zz references and xx reference
    #
    applyFASTA = {8}  # complete the sequence with a FASTA file?
    FASTAstart = {9} # Residue number for the first residue in the FASTA file?
    #
    do_titvar1 = {10}  # Analyse data in the first titration condition (dimension)
    do_titvar2 = {11}  # Analyse data in the second titration condition (dimension)
    do_titvar3 = {12}  # Analyse data in the thrid titration condition (dimension)
    perform_comparisons = True  # Compares data obtained for condition experiment.
    #
    csp_alpha4res = {13}  # General alpha normalization factor for CSP
    csp_res_exceptions = {14}  # exceptions for the normalization factor
    cs_lost = {15}  # how to represent the lost residues in CSPs [prev/full]
    #
    chimera_att_select_format = ':'  # format to select residues in Chimera
    #
    perform_resevo_fit = {16}  # Fit parameter evolution over titration experiment
    fit_x_values = [0, 250, 500]  # values for the x axis in the fitting procedure (ex. Ligand concentration)
    # Perform PRE analysis

    apply_PRE_analysis = {17}
    apply_smooth = {18}
    gaussian_stddev = {19}
    gauss_x_size = {20}
    d_pre_y_max = {21}  # y axis max scale
    d_pre_y_label = {22}
    d_pre_rows = {23}
    pre_color = {24}  # theoretical PRE line color
    pre_lw = {25}  # theoretical PRE line width
    tag_color = {26}
    tag_lw = {27}
    tag_ls = {28}

    #
    plots_PosF1_delta = {29}  # Plot nuclei 1 shift perturbation data
    plots_PosF2_delta = {30}  # Plot nuclei 2 shift perturbation data
    plots_CSP = {31}  # Plot combined chemical shift perturbation data
    plots_Height_ratio = {32}  # Plot Height ratio data
    plots_Volume_ratio = {33}  # Plot Volume ratio data
    #
    plots_extended_bar = {34}  # Represent data in Extended Bar Plot style
    plots_compacted_bar = {35}  # Represent data in Compacted Bar Plot style
    plots_vertical_bar = {36}  # Represent data in Vertical Bar Plot style
    plots_residue_evolution = {37}  # Represent Data Evolution per Residue style
    plots_cs_scatter = {38}  # Represent chemical shift scatter data
    #
    yy_label_PosF1_delta = {39}  # y axis label for nuclei 1
    yy_label_PosF2_delta = {40}  # y axis label for nuclei 2
    yy_label_CSP = {41}  # y axis label for combined chemical shift
    yy_label_Height_ratio = {42}  # y axis label for height ratio
    yy_label_Volume_ratio = {43}  # y axis label for volume ratio
    #
    calccol_name_PosF1_delta = {44}  # column name for nuclei 1
    calccol_name_PosF2_delta = {45}  # column name for nuclei 2
    calccol_name_CSP = {46}  # column name for combined chemical shift perturbation data
    calccol_name_Height_ratio = {47}  # column name for Height Ratio data
    calccol_name_Volume_ratio = {48}  # column name for Volume Ratio data
    #
    yy_scale_PosF1_delta = {49}  # y axis sacle for nuclei 1
    yy_scale_PosF2_delta = {50}  # y axis scale for nuclei 2
    yy_scale_CSP = {51}  # y axis sacle for combined chemical shift
    yy_scale_Height_ratio = {52}  # y axis scale for height ratio
    yy_scale_Volume_ratio = {53}  # y axis scale for volume ratio
    #
    represent_user_marks = {54}  # draws user defined marks over bars in plots
    user_marks_dict = {55}
    # keys: the string in 'Details' column in input data, value: the character to be drawn
    #
    # Extended Bar Plot
    # use a combination of cols_page and rows_page to achieve desired figure ratio
    ext_bar_cols_page = {56}  # number of columns of subplots per page
    ext_bar_rows_page = {57}  # number of rows of subplots per page
    ext_bar_color_measured = {57}  # color of the bars
    ext_bar_apply_status_2_bar_color = {58}  # applies color to the 'lost' residue bars
    ext_bar_color_lost = {59}  # color of the 'lost' residues bar
    ext_bar_color_unassigned = {60}  # color of unassigned residues
    ext_bar_bar_width = {61}  # bar width
    ext_bar_bar_alpha = {62}  # bar transparency. 0-1 (transparent-opaque)
    ext_bar_bar_linewidth = {63}  # bar line width
    ext_bar_title_y = {64}  # subplot title padding
    ext_bar_title_fn = {65}  # subplot tittle font
    ext_bar_title_fs = {66}  # subplot tittle font size
    ext_bar_plot_threshold = {67}  # applies stdev threshold
    ext_bar_plot_threshold_color = {68}  # stdev thresold color
    ext_bar_plot_threshold_lw = {69}  # stdev threshold width
    ext_bar_x_label_fn = {70}  # x label font
    ext_bar_x_label_weight = {71}  # x label weight
    ext_bar_x_label_fs = {72}  # x label fontsize
    ext_bar_x_label_pad = {73}  # x label pad
    ext_bar_x_ticks_fn = {74}  # x ticks font type
    ext_bar_x_ticks_fs = {75}  # x ticks font size
    ext_bar_x_ticks_rot = {76}  # x ticks rotation
    ext_bar_x_ticks_pad = {77}  # x ticks pad
    ext_bar_y_label_fn = {78}  # y label font
    ext_bar_y_label_fs = {79}  # y label font size
    ext_bar_y_label_pad = {80}  # y label pad
    ext_bar_y_label_weight = {81}  # y label weight
    ext_bar_y_ticks_fn = {82}  # y label font
    ext_bar_y_ticks_fs = {83}  # y ticks font size
    ext_bar_y_ticks_pad = {84}  # y ticks pad
    ext_bar_y_ticks_len = {85}  # y ticks length
    ext_bar_y_grid_color = {86}  # grid color
    ext_bar_mark_prolines = {87}  # mark prolines
    ext_bar_proline_mark = {88}  # Proline marks
    ext_bar_mark_user_details = {89}  # mark user details
    ext_bar_mark_fs = {90}  # mark font size
    #
    # Compacted Bar Plot
    # use a combination of cols_page and rows_page to achieve desired figure ratio
    comp_bar_cols_page = {91}  # number of columns of subplots per page
    comp_bar_rows_page = {92}  # number of rows of subplots per page
    comp_bar_color_measured = {93}  # color of the bars
    comp_bar_apply_status_2_bar_color = {94}  # applies color to the 'lost' residue bars
    comp_bar_color_lost = {95}  # color of the 'lost' residues bar
    comp_bar_color_unassigned = {96}  # color of unassigned residues
    comp_bar_bar_width = {97}  # bar width
    comp_bar_bar_alpha = {98}  # bar transparency. 0-1 (transparent-opaque)
    comp_bar_bar_linewidth = {99}  # bar line width
    comp_bar_title_y = {100}  # subplot title padding
    comp_bar_title_fn = {101}  # subplot tittle font
    comp_bar_title_fs = {102}  # subplot tittle font size
    comp_bar_plot_threshold = {103}  # applies stdev threshold
    comp_bar_plot_threshold_color = {104}  # stdev thresold color
    comp_bar_plot_threshold_lw = {105}  # stdev threshold width
    comp_bar_x_label_fn = {106}  # x label font
    comp_bar_x_label_fs = {107}  # x label fontsize
    comp_bar_x_label_pad = {108}  # x label pad
    comp_bar_x_label_weight = {109}  # y label weight
    comp_bar_x_ticks_fn = {110}  # x ticks font type
    comp_bar_x_ticks_fs = {111}  # x ticks font size
    comp_bar_x_ticks_rot = {112}  # x ticks rotation
    comp_bar_x_ticks_pad = {113}  # x ticks pad
    comp_bar_y_label_fn = {114}  # y label font
    comp_bar_y_label_weight = {115}  # y label weight
    comp_bar_y_label_fs = {116}  # y label font size
    comp_bar_y_label_pad = {117}  # y label pad
    comp_bar_y_ticks_fs = {118}  # y ticks font size
    comp_bar_y_ticks_pad = {119}  # y ticks pad
    comp_bar_y_ticks_len = {120}  # y ticks length
    comp_bar_y_grid_color = {121}  # grid color
    comp_bar_mark_prolines = {122}  # mark prolines
    comp_bar_proline_mark = {123}  # Proline marks
    comp_bar_mark_user_details = {124}  # mark user details
    comp_bar_mark_fs = {125}  # mark font size
    comp_bar_unassigned_shade = {126}  # displays shade for unassigned residues
    comp_bar_unassigned_shade_color = {127}  # unassigned residues shade color
    comp_bar_unassigned_shade_alpha = {128}  # unassigned residues shade transparency.
    #
    # Vertical Bar plot
    # use a combination of cols_page and rows_page to achieve desired figure ratio
    vert_bar_cols_page = 5  # number of columns of subplots per page
    vert_bar_rows_page = 2  # number of rows of subplots per page
    vert_bar_color_measured = 'k'  # color of   the bars
    vert_bar_apply_status_2_bar_color = True  # applies color to the 'lost' residue bars
    vert_bar_color_lost = 'red'  # color of the 'lost' residues bar
    vert_bar_color_unassigned = 'grey'  # color of unassigned residues
    vert_bar_bar_width = 0.7  # bar width
    vert_bar_bar_alpha = 1  # bar transparency. 0-1 (transparent-opaque)
    vert_bar_bar_linewidth = 0  # bar line width
    vert_bar_title_y = 1.01  # subplot title padding
    vert_bar_title_fn = 'Arial'  # subplot tittle font
    vert_bar_title_fs = 8  # subplot title font size
    vert_bar_plot_threshold = True  # applies stdev threshold
    vert_bar_plot_threshold_color = 'red'  # stdev thresold color
    vert_bar_plot_threshold_lw = 1  # stdev threshold width
    vert_bar_x_label_fn = 'Arial'  # x label font
    vert_bar_x_label_fs = 8  # x label fontsize
    vert_bar_x_label_pad = 2  # x label pad
    vert_bar_x_label_weight = 'bold'  # x label weight
    vert_bar_x_ticks_fn = 'monospace'  # x ticks font type
    vert_bar_x_ticks_fs = 5  # x ticks font size
    vert_bar_x_ticks_pad = 2  # x ticks pad
    vert_bar_x_ticks_len = 2  # x ticks len
    vert_bar_y_label_fn = 'Arial'  # y label font
    vert_bar_y_label_fs = 8  # y label font size
    vert_bar_y_label_pad = 9  # y label pad
    vert_bar_y_label_weight = 'bold'  # label weight
    vert_bar_y_label_rot = -90  # y label rotation
    vert_bar_y_ticks_fn = 'monospace'  # y ticks font
    vert_bar_y_ticks_fs = 4  # y ticks font size
    vert_bar_y_ticks_pad = 1  # y ticks pad
    vert_bar_y_ticks_rot = 0  # y ticks rotation
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
    res_evo_title_y = 0.98  # subplot title pad
    res_evo_title_fn = 'Arial'  # subplot title font
    res_evo_title_fs = 8  # subplot title font size
    res_evo_x_label = '[Ligand]'  # x label
    res_evo_set_x_values = True  # use user defined x values? Necessary for titration fitting.
    res_evo_x_label_fn = 'Arial'  # x label font
    res_evo_x_label_fs = 6  # x label font size
    res_evo_x_label_pad = 2  # x label pad
    res_evo_x_label_weight = 'normal'  # x label weight
    res_evo_x_ticks_pad = 1  # x ticks pad
    res_evo_x_ticks_fs = 7  # x ticks font size
    res_evo_y_label_fn = 'Arial'  # y label font
    res_evo_y_label_fs = 6  # y label font size
    res_evo_y_label_pad = 2  # y label pad
    res_evo_y_label_weight = 'normal'  # y label weight
    res_evo_y_ticks_pad = 1  # y ticks pad
    res_evo_y_ticks_fs = 7  # y ticks font size
    res_evo_line_style = '-'  # data line style
    res_evo_plot_color = 'r'  # data line color
    res_evo_marker_style = 'o'  # data marker style
    res_evo_marker_color = 'darkred'  # data marker color
    res_evo_marker_size = 3  # data marker size
    res_evo_line_width = 1  # data line width
    res_evo_fill_between = True  # draw data shade
    res_evo_fill_color = 'pink'  # shade color
    res_evo_fill_alpha = 0.5  # shade transparency (0-1)
    res_evo_fit_line_color = 'black'  # fit line color
    res_evo_fit_line_width = 1  # fit line width
    #
    # Chemical Shift Scatter Plot
    cs_scatter_cols_page = 5  # number of columns of subplots per page
    cs_scatter_rows_page = 7  # number of rows of subplots per page
    cs_scatter_title_y = 0.97  # subplot title pad
    cs_scatter_title_fn = 'Arial'  # subplot font
    cs_scatter_title_fs = 8  # subplot title font size
    cs_scatter_x_label_fn = 'Arial'  # x label font
    cs_scatter_x_label_fs = 6  # x label font size
    cs_scatter_x_label_pad = 1.8  # x label pad
    cs_scatter_x_label_weight = 'normal'  # x label weight
    cs_scatter_x_ticks_pad = 1  # x ticks pad
    cs_scatter_x_ticks_fs = 5  # x ticks font size
    cs_scatter_y_label_fn = 'Arial'  # y label font
    cs_scatter_y_label_fs = 6  # y label font size
    cs_scatter_y_label_pad = 2  # y label pad
    cs_scatter_y_label_weight = 'normal'  # y label weight
    cs_scatter_y_ticks_pad = 1  # y ticks pad
    cs_scatter_y_ticks_fs = 5  # y ticks font size
    cs_scatter_mksize = 20  # marker size
    cs_scatter_scale = 0.01  # scale representation
    cs_scatter_mk_type = 'color'  # 'color' or 'shape'
    cs_scatter_mk_start_color = '#cdcdcd'  # start color for gradient [in hex notation] - color style
    cs_scatter_mk_end_color = '#000000'  # end color for gradient [in hex notation] - color style
    cs_scatter_mk_lost_color = 'red'  # color for lost data points - color style
    cs_scatter_markers = ['^', '>', 'v', '<', 's', 'p', 'h', '8', '*', 'D']  # sequencial markers
    cs_scatter_mk_color = 'none'  # marker inside color for shape style
    cs_scatter_mk_edgecolors = 'black'  # marker edge color for shape style
    cs_scatter_mk_edge_lost = 'red'  # marker edge color for lost data points in shape style.
    #
    # DELTA PRE Heat Maps
    heat_map_rows = 20
    heat_map_vmin = 0.0
    heat_map_vmax = 1.0
    heat_map_x_ticks_fs = 6
    heat_map_x_ticks_rot = 0
    heat_map_x_ticks_fn = 'Arial'
    heat_map_x_tick_pad = 1
    heat_map_y_label_fs = 6
    heat_map_y_label_pad = 2
    heat_map_y_label_fn = 'Arial'
    heat_map_y_label_weight = 'bold'
    heat_map_right_margin = 0.2
    heat_map_bottom_margin = 0.5
    heat_map_top_margin = 0.9
    heat_map_cbar_font_size = 4
    #
    # DELTA PRE oscilations Plot
    dpre_osci_width = 3  # scale factor for the width
    dpre_osci_title_y = 1  # subplot title pad
    dpre_osci_title_fs = 6  # subplot title font size
    dpre_osci_title_fn = 'Arial'  # subplot title font
    dpre_osci_dpre_ms = 2  # DELTA_PRE circle marker size
    dpre_osci_dpre_alpha = 0.5  # DELTA_PRE alpha
    dpre_osci_smooth_lw = 1  # smooted DPRE line width
    dpre_osci_ref_color = 'black'  # color for the reference data
    dpre_osci_color_init = '#ff00ff'  # initial color for data points color gradient
    dpre_osci_color_end = '#0000ff'  # final color for data points color gradient
    dpre_osci_x_ticks_fs = 5  # x ticks font size
    dpre_osci_x_ticks_fn = 'Arial'  # xticks font
    dpre_osci_y_label_fs = 6  # y axis label font size
    dpre_osci_y_label_pad = 1  # y axis label pad
    dpre_osci_y_label_fn = 'Arial'  # y axis label font
    dpre_osci_y_label_weight = 'normal'  # y axis label weight
    dpre_osci_y_ticks_len = 1  # y ticks length
    dpre_osci_y_ticks_fs = 4  # y ticks font size
    dpre_osci_y_ticks_pad = 1  # y ticks pad
    dpre_osci_grid_color = 'grey'  # grid color
    dpre_osci_res_shade = True  # applies shade to highlight residues
    dpre_osci_res_highlight = [(24, 1.5), (37, 3), (3, 1.5), (65, 6)]  # residues to highlight (res, shade width)
    dpre_osci_rh_fs = 4  # font size for residue highlight
    dpre_osci_rh_y = 0.9  # y scaling for residue 1-letter representation
    #
    # Figure Details
    fig_width = 8.69  # Figure width in inches
    fig_height = 11.69  # Figure height in inches
    fig_file_type = 'pdf'  # Figure file type
    fig_dpi = 300  # Figure resolution
    #
    import farseermain
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
        dict(user),
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






    )
    print(fsuv)

json_to_fsuv(open("/Users/fbssps/PycharmProjects/FarSeer-NMR/current/default_config.json", 'r'))