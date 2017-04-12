import datetime  # used to write the log file
import shutil
import os
import numpy as np
import pandas as pd
#
import farseer_user_variables as fsuv
import fslibs.parameters as fspar
import fslibs.FarseerSet as fsFS
import fslibs.Titration as fsT
import fslibs.utils as fsut

def gen_dim_tit_dict(farseer_set, data_hyper_cube, reso_type='Backbone'):
    """
    Returns a dictionary containing all the titrations to be analysed.
    
    primary keys: 'cond1', 'cond2', 'cond3'.
    
    :farseer_set: the FarseerSet object with all the titration data
    :data_hyper_cube: the 5D cube with all the titration data
    :reso_type: default:'Backbone', labels the data according
                to its resonance of origin (Backbone or Sidechain).
    """
    
    # to facilitate the analysis with for loops, all the different
    # titrations experiments we are going to analyse will be stored 
    # in a dictionary
    titrations_dict = {}

    # creates the titrations for the first condition (1D)
    if farseer_set.hasxx and fsuv.do_cond1:
        titrations_dict['cond1'] = \
            farseer_set.gen_titration_dict(\
                data_hyper_cube,
                'cond1', 
                farseer_set.xxcoords,
                farseer_set.yycoords,
                farseer_set.zzcoords,
                reso_type)
    
    # creates the titrations for the second condition (2D)
    if farseer_set.hasyy and fsuv.do_cond2:
        titrations_dict['cond2'] = \
            farseer_set.gen_titration_dict(\
                data_hyper_cube.transpose(2,0,1,3,4),
                'cond2',
                farseer_set.yycoords,
                farseer_set.zzcoords,
                farseer_set.xxcoords,
                reso_type)

    # creates the titrations for the third condition (3D)  
    if farseer_set.haszz and fsuv.do_cond3:
        titrations_dict['cond3'] = \
            farseer_set.gen_titration_dict(\
                data_hyper_cube.transpose(1,2,0,3,4),
                'cond3',
                farseer_set.zzcoords,
                farseer_set.xxcoords,
                farseer_set.yycoords,
                reso_type)
    
    return titrations_dict

def dimension_loop(titration_dict, sidechains=False):
    """
    Executes a standard nested for loop cycle accross the three
    titration conditions.
    
    :titration_dict: the dictionary containing the information of all
                     the titrations to be analysed.
    :sidechains: whether the data analysis corresponds to sidechain
                 resonances.
    """
    # for each kind of titration (cond{1,2,3})
    for cond in sorted(titration_dict.keys()):
        fsut.write_log(fsut.dim_sperator(cond, 'top'))
        
        # for each point in the corresponding second dimension/condition
        for dim2_pt in sorted(titration_dict[cond].keys()):
            fsut.write_log(fsut.dim_sperator(dim2_pt, 'midle'))
            
            # for each point in the corresponding first dimension/condition
            for dim1_pt in sorted(titration_dict[cond][dim2_pt].keys()):
                fsut.write_log(fsut.dim_sperator(dim1_pt, 'own'))
                fsut.write_log('\n')  #exception
                
                # performs the calculations
                perform_calcs(titration_dict[cond][dim2_pt][dim1_pt])
            
                # PERFORMS FITS
                # *fits are blocked to cond1 titrations
                if fsuv.perform_resevo_fit \
                    and titration_dict[cond][dim2_pt][dim1_pt].\
                        tittype == 'cond1':
                    # do
                    if len(fsuv.fit_x_values) != \
                        titration_dict[cond][dim2_pt][dim1_pt].shape[0]:
                        raise ValueError(\
'!!! Values given for x axis in fitting (fitting_x_values) do not match length\
of cond1 variables.')
                    else:
                        perform_fits(\
                            titration_dict[cond][dim2_pt][dim1_pt])
                
                # Analysis of PRE data - only in cond3
                PRE_analysis(titration_dict[cond][dim2_pt][dim1_pt], 
                             spectra_path=fsuv.spectra_path)
                
                # EXPORTS AND PLOTS TITRATION DATA
                plot_tit_data(titration_dict[cond][dim2_pt][dim1_pt])

def perform_calcs(tit_panel):
    """
    Calculates the NMR restraints according to the user specifications.
    """
    # if the user wants to calculate combined Chemical Shift Perturbations
    if fsuv.plots_CSP:
        # calculate differences in chemical shift for each dimension
        tit_panel.calc_cs_diffs(fsuv.calccol_name_PosF1_delta, 'Position F1')
        tit_panel.calc_cs_diffs(fsuv.calccol_name_PosF2_delta, 'Position F2')
    
        # Calculates CSPs
        tit_panel.calc_csp(calccol=fsuv.calccol_name_CSP,
                        pos1=fsuv.calccol_name_PosF1_delta,
                        pos2=fsuv.calccol_name_PosF2_delta)
    
    # if the user only wants to calculate perturbation in single dimensions
    else:
        if fsuv.plots_PosF1_delta:
            tit_panel.calc_cs_diffs(fsuv.calccol_name_PosF1_delta,
                                    'Position F1')
        if fsuv.plots_PosF2_delta:
            tit_panel.calc_cs_diffs(fsuv.calccol_name_PosF2_delta,
                                    'Position F2')
    
    # Calculates Ratios
    if fsuv.plots_Height_ratio:
        tit_panel.calc_ratio(fsuv.calccol_name_Height_ratio, 'Height')
    if fsuv.plots_Volume_ratio:
        tit_panel.calc_ratio(fsuv.calccol_name_Volume_ratio, 'Volume')
    
def PRE_analysis(tit_panel, spectra_path=None):
    """
    Performs dedicated PRE analysis on the cond3 dimension.
    Data can be represented under the calculations of cond3 or when
    <comparing> the data for 'C3'.
    """
    # if user do not wants PRE analysis, do nothing
    if not(fsuv.apply_PRE_analysis):
        return
    
    # if analysing cond3: performs calculations.
    if tit_panel.tittype == 'cond3':
        tit_panel.load_theoretical_PRE(spectra_path, tit_panel.dim2_pts)
        for sourcecol, targetcol in zip(fspar.param_settings.index[3:],\
                                        ['H_DPRE', 'V_DPRE']):
            # only in the parameters allowed by the user
            if fspar.param_settings.loc[sourcecol, 'plot_param_flag']:
                tit_panel.calc_Delta_PRE(sourcecol, targetcol,
                                         apply_smooth=fsuv.apply_smooth,
                                         gaussian_stddev=fsuv.gaussian_stddev,
                                         guass_x_size=fsuv.gauss_x_size)
    
    # plots the calculated Delta_PRE and Delta_PRE_smoothed analsysis
    # for cond3 and for comparison C3.
    if tit_panel.tittype == 'cond3' \
            or (tit_panel.tittype == 'C3' \
                and (tit_panel.dim2_pts == 'para'\
                    or tit_panel.dim1_pts == 'para')):
        
        # do
        for sourcecol, targetcol in zip(list(fspar.param_settings.index[3:])*2,
                                        ['H_DPRE',
                                         'V_DPRE',
                                         'H_DPRE_smooth',
                                         'V_DPRE_smooth']):
            
            # only for the parameters allowed by the user
            if fspar.param_settings.loc[sourcecol, 'plot_param_flag']:
                
                tit_panel.write_table(targetcol)
                tit_panel.plot_base(targetcol, 'exp', 'heat_map',
                    fspar.heat_map_dict,
                    par_ylims=\
                    fspar.param_settings.loc[sourcecol,'plot_yy_axis_scale'],
                    ylabel=\
                    fspar.param_settings.loc[sourcecol,'plot_yy_axis_label'],
                    cols_per_page=1,
                    rows_per_page=fsuv.heat_map_rows,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
    
    # plots the DeltaPRE oscilation analysis only for <C3> comparison.
    # because DeltaPRE oscilation represents the results obtained only
    # for paramagnetic ('para') data.
    if tit_panel.tittype == 'C3' \
        and (tit_panel.dim2_pts == 'para' \
            or tit_panel.dim1_pts == 'para'):
        
        
        for sourcecol, targetcols in zip(fspar.param_settings.index[3:],
                                         ['H_DPRE', 'V_DPRE']):
            if fspar.param_settings.loc[sourcecol, 'plot_param_flag']:
                tit_panel.plot_base(targetcols, 'exp', 'delta_osci',
                    fspar.delta_osci_dict,
                    par_ylims=(0,fsuv.d_pre_y_max),
                    ylabel=fsuv.d_pre_y_label,
                    cols_per_page=1,
                    rows_per_page=fsuv.d_pre_rows,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width/fsuv.dpre_osci_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)

def perform_fits(tit_panel):
    """Performs fits for 1H, 15N and CSPs data."""
    # runs only for CSPs, 1H and 15N.
    for calculated_parameter in fspar.param_settings.index[:3]:
        
        if fspar.param_settings.loc[calculated_parameter, 'plot_param_flag']:
            tit_panel.perform_fit(calccol = calculated_parameter,
                                  x_values=fsuv.fit_x_values)

def plot_tit_data(tit_panel):
    '''
    This function was written because it serves normal titrations and
    control titrations.
    '''
    # EXPORTS CALCULATIONS
    tit_panel.export_titration()
    
    # PLOTS DATA
    for calculated_parameter in fspar.param_settings.index:
        # if the user wants to plot this parameter
        if fspar.param_settings.loc[calculated_parameter,'plot_param_flag']:
            # writes titration data table
            tit_panel.write_table(calculated_parameter)
            # writes chimera attribute files
            tit_panel.write_Chimera_attributes(calculated_parameter,
                                    resformat=fsuv.chimera_att_select_format)
            
            if tit_panel.resonance_type == 'Backbone':
            
                # Plot Extended Bar Plot
                if fsuv.plots_extended_bar:
                    tit_panel.plot_base(
                        calculated_parameter, 'exp', 'bar_extended',
                        fspar.bar_ext_par_dict,
                        par_ylims=\
                        fspar.param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_scale'],
                        ylabel=\
                        fspar.param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_label'],
                        cols_per_page=fsuv.ext_bar_cols_page,
                        rows_per_page=fsuv.ext_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
                
                # Plot Compacted Bar Plot
                if fsuv.plots_compacted_bar:
                    tit_panel.plot_base(\
                        calculated_parameter, 'exp', 'bar_compacted',
                        fspar.comp_bar_par_dict,
                        par_ylims=\
                        fspar.param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_scale'],
                        ylabel=\
                        fspar.param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_label'],
                        cols_per_page=fsuv.comp_bar_cols_page,
                        rows_per_page=fsuv.comp_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
            
                # Plot Vertical Bar Plot
                if fsuv.plots_vertical_bar:
                    tit_panel.plot_base(
                        calculated_parameter, 'exp', 'bar_vertical',
                        fspar.bar_vert_par_dict,
                        par_ylims=\
                        fspar.param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_scale'],
                        ylabel=\
                        fspar.param_settings.loc[calculated_parameter,
                                                 'plot_yy_axis_label'],
                        cols_per_page=fsuv.vert_bar_cols_page,
                        rows_per_page=fsuv.vert_bar_rows_page,
                        fig_height=fsuv.fig_height,
                        fig_width=fsuv.fig_width,
                        fig_file_type=fsuv.fig_file_type,
                        fig_dpi=fsuv.fig_dpi)
            
            # Sidechain data is represented in a different bar plot
            elif tit_panel.resonance_type == 'Sidechains'\
                and fsuv.plots_extended_bar:
                #do - dedicated single plot for sidechains
                tit_panel.plot_base(
                    calculated_parameter, 'exp', 'bar_extended',
                    fspar.bar_ext_par_dict,
                    par_ylims=\
                    fspar.param_settings.loc[calculated_parameter,
                                             'plot_yy_axis_scale'],
                    ylabel=\
                    fspar.param_settings.loc[calculated_parameter,
                                             'plot_yy_axis_label'],
                    cols_per_page=fsuv.ext_bar_cols_page,
                    rows_per_page=fsuv.ext_bar_rows_page,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width/2,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
            
            # Plots Parameter Evolution Plot
            if fsuv.plots_residue_evolution:
                tit_panel.plot_base(\
                    calculated_parameter, 'res', 'res_evo',
                    fspar.res_evo_par_dict,
                    par_ylims=  
                    fspar.param_settings.loc[calculated_parameter,
                                             'plot_yy_axis_scale'],
                    ylabel=\
                    fspar.param_settings.loc[calculated_parameter,
                                             'plot_yy_axis_label'],
                    cols_per_page=fsuv.res_evo_cols_page,
                    rows_per_page=fsuv.res_evo_rows_page,
                    fig_height=fsuv.fig_height,
                    fig_width=fsuv.fig_width,
                    fig_file_type=fsuv.fig_file_type,
                    fig_dpi=fsuv.fig_dpi)
            
    if fsuv.plots_cs_scatter:
        tit_panel.plot_base('15N_vs_1H', 'res', 'cs_scatter',
                            fspar.cs_scatter_par_dict,
                            cols_per_page=fsuv.cs_scatter_cols_page,
                            rows_per_page=fsuv.cs_scatter_rows_page,
                            fig_height=fsuv.fig_height,
                            fig_width=fsuv.fig_width,
                            fig_file_type=fsuv.fig_file_type,
                            fig_dpi=fsuv.fig_dpi)

def analyse_comparisons(tit_dict, p5d, reso_type='Backbone'):
    """Algorythm to perform data comparisons over titration conditions."""
    # dictionary with titration variable dimension order.
    # cond 1 has cond2 as next 1st dimension
    # and cond 3 as next 2nd dimension
    # etc...
    tit_dim_keys = {'cond1':['cond2','cond3'],
                    'cond2':['cond3','cond1'],
                    'cond3':['cond1','cond2']}
    
    for dimension in sorted(tit_dict.keys()):
        fsut.write_log(fsut.dim_sperator(dimension, 'top'))
        
        Farseer_comparisons_hyper_panel = p5d(tit_dict[dimension])
        # performs comparisons only if there are points to which compare to
        if len(Farseer_comparisons_hyper_panel.labels) > 1:
        
            for dim2_pt in Farseer_comparisons_hyper_panel.items:
                fsut.write_log(fsut.dim_sperator(dim2_pt, 'midle'))
                
                for dim1_pt in Farseer_comparisons_hyper_panel.cool:
                    fsut.write_log(fsut.dim_sperator(dim1_pt, 'own'))
                    fsut.write_log('\n')
                    
                    control = fsT.Titration(\
                        np.array(Farseer_comparisons_hyper_panel.\
                            loc[dim1_pt,:,dim2_pt,:,:]),
                        items=Farseer_comparisons_hyper_panel.labels,
                        minor_axis=Farseer_comparisons_hyper_panel.minor_axis,
                        major_axis=Farseer_comparisons_hyper_panel.major_axis)
                    
                    control.create_titration_attributes(
                                  tittype='C'+ dimension[-1], 
                                  owndim_pts=\
                                  Farseer_comparisons_hyper_panel.labels, 
                                  dim1_pts=dim1_pt, 
                                  dim2_pts=dim2_pt,
                                  dim_comparison=tit_dim_keys[dimension][0],
                                  resonance_type=reso_type)
                    
                    # performs pre analysis
                    PRE_analysis(control)
                    # plots data
                    plot_tit_data(control)
        else:
            
            fsut.write_log('*** There are no points to compare with in {}\n'.\
                format(tit_dim_keys[dimension][0]))
            
        if len(Farseer_comparisons_hyper_panel.cool) > 1:
            
            for dim2_pt in Farseer_comparisons_hyper_panel.labels:
                fsut.write_log(fsut.dim_sperator(dim2_pt, 'midle'))
                for dim1_pt in Farseer_comparisons_hyper_panel.items:
                    fsut.write_log(fsut.dim_sperator(dim1_pt, 'own'))
                    
                    control = fsT.Titration(\
                        np.array(Farseer_comparisons_hyper_panel.\
                            loc[:,dim2_pt,dim1_pt,:,:]),
                        items=Farseer_comparisons_hyper_panel.cool,
                        minor_axis=Farseer_comparisons_hyper_panel.minor_axis,
                        major_axis=Farseer_comparisons_hyper_panel.major_axis)
                                            
                    control.create_titration_attributes(\
                        tittype='C'+ dimension[-1],
                        owndim_pts=Farseer_comparisons_hyper_panel.cool, 
                        dim1_pts=dim1_pt, 
                        dim2_pts=dim2_pt,
                        dim_comparison=tit_dim_keys[dimension][1],
                        resonance_type=reso_type)
                    
                    # performs pre analysis
                    PRE_analysis(control)
                    # plots data
                    plot_tit_data(control)
        else:
            
            fsut.write_log('*** There are no points to compare with in {}\n'.\
                format(tit_dim_keys[dimension][1]))

# Starts Log
ltitle = fsut.write_title('LOG STARTED', onlytitle=True)
startlog = "{}{}\n".format(ltitle,
                           datetime.\
                            datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
fsut.write_log(startlog, mod='w')

# backups code
cwd = os.getcwd()
script_wd = os.path.dirname(os.path.realpath(__file__))

fsut.write_log('\n-> Farseer base dictory: {}\n'.format(script_wd))
fsut.write_log('-> current working directiory: {}\n'.format(cwd))

# creates farseer backup of the version user for the calculations
shutil.make_archive(cwd+'/farseer_used_version', 'zip', script_wd)


# Reads spectra peaklists, .csv files.
# creates an FarseerSet object
ttt = fsFS.FarseerSet(fsuv.spectra_path,
                      has_sidechains=fsuv.has_sidechains,
                      applyFASTA=fsuv.applyFASTA,
                      FASTAstart=fsuv.FASTAstart)

# writelog titration coordinates
str2write = \
'''{}> xx (1D) :: {} :: {}
> yy (2D) :: {} :: {}
> zz (3D) :: {} :: {}
{}'''.format(fsut.write_title('AXIS :: FOUND :: ALLOWED', onlytitle=True),
             ttt.hasxx, fsuv.do_cond1,
             ttt.hasyy, fsuv.do_cond2,
             ttt.haszz, fsuv.do_cond3,
             fsut.titlesperator)
fsut.write_log(str2write)

# Reads Residue information
fsut.write_title('ADDS Res#, 1-letter, 3-letter code, Peak Status COLUMNS')
ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords, ttt.split_res_info)

# Corrects chemical shifts based on a specific peak
# i.e. applies an internal reference
if fsuv.perform_cs_correction:
    fsut.write_title('CORRECTS CHEMICAL SHIFTS BASED ON A REFERENCE PEAK')
    ttt.tricicle(ttt.zzcoords, 
                 ttt.yycoords, 
                 ttt.xxcoords, 
                 ttt.correct_shifts,
                 kwargs={'ref_res':str(fsuv.cs_correction_res_ref)})

# Identifies lost residues across the titration
# information to fill 'lost' residues entry
fillnalost = {
'Peak Status': 'lost',
'Merit': 0,
'Details': 'None'}

## 1st) expands the residue 'lost' information to other dimensions
# this operation has to be perform prior to identify the lost residues in the
# same dimension. Normally used for diamagnetic/paramagnetic cases, which
# are set in zz(cond3) dimension, though it is also possible to use for the
# yy(cond2) dimension.
if fsuv.expand_lost_yy or fsuv.expand_lost_zz:
    fsut.write_title('EXPANDS LOST RESIDUES TO OTHER CONDITIONS/DIMENSIONS')
    
    # expands to yy (cond2) condition
    if fsuv.expand_lost_yy:
        for z in ttt.zzcoords:
            fsut.write_log(fsut.dim_sperator(z, 'top'))
            for y in ttt.yycoords:
                fsut.write_log(fsut.dim_sperator(y, 'own'))
                refscoords = {'z': z, 'y': ttt.yyref}
                ttt.seq_expand(z, y, ttt.xxref, 'expanding',
                               ttt.allpeaklists, 
                               ttt.allpeaklists,
                               fillnalost, refscoords=refscoords)
    
    # expands to zz (cond3) condition
    if fsuv.expand_lost_zz:
        for y in ttt.yycoords:
            fsut.write_log(fsut.dim_sperator(y, 'top'))
            for z in ttt.zzcoords:
                fsut.write_log(fsut.dim_sperator(z, 'own'))
                refscoords = {'z': ttt.zzref, 'y': y}
                ttt.seq_expand(z, y, ttt.xxref, 'expanding',
                               ttt.allpeaklists, 
                               ttt.allpeaklists,
                               fillnalost, refscoords=refscoords)
    
    # if there are sidechains to be used
    if ttt.has_sidechains and fsuv.use_sidechains:
        fsut.write_title('SIDECHAINS: \
                         EXPANDS LOST RESIDUES TO OTHER CONDITIONS/DIMENSIONS')
        
        if fsuv.expand_lost_yy:
            for z in ttt.zzcoords:
                fsut.write_log(fsut.dim_sperator(z, 'top'))
                for y in ttt.yycoords:
                    fsut.write_log(fsut.dim_sperator(y, 'own'))
                    refscoords = {'z': z, 'y': ttt.yyref}
                    ttt.seq_expand(z, y, ttt.xxref, 'expanding',
                                   ttt.allsidechains, 
                                   ttt.allsidechains,
                                   fillnalost, refscoords=refscoords)
            
        if fsuv.expand_lost_zz:
            for y in ttt.yycoords:
                fsut.write_log(fsut.dim_sperator(y, 'top'))
                for z in ttt.zzcoords:
                    fsut.write_log(fsut.dim_sperator(z, 'own'))
                    refscoords = {'z': ttt.zzref, 'y': y}
                    ttt.seq_expand(z, y, ttt.xxref, 'expanding',
                                   ttt.allsidechains, 
                                   ttt.allsidechains,
                                   fillnalost, refscoords=refscoords)

## Identifies lost residues across the titration
fsut.write_title('ADDS LOST RESIDUES BASED ON THE REFERENCE LIST')
ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords, 
             ttt.seq_expand,
             [ttt.allpeaklists, ttt.allpeaklists, fillnalost])

## the same for the sidechains if exist
if ttt.has_sidechains and fsuv.use_sidechains:
    # Identifies lost residues across the titration
    fsut.write_title(\
        'ADDS LOST SIDE CHAIN RESIDUES BASED ON THE REFERENCE LIST')
    
    ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords, 
                 ttt.seq_expand,
                 args=[ttt.allsidechains, ttt.allsidechains, fillnalost])

# Adds unassigned residues to the peaklists based on a FASTA file
if fsuv.applyFASTA:

    fsut.write_title('ADDS UNASSIGNED RESIDUES BASED ON THE FASTA FILE')
        
    fillnaunassigned = {
    'Peak Status': 'unassigned',
    'Merit': 0,
    'Details': 'None'}
    
    
    ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords, 
                 ttt.seq_expand,
                 args=[ttt.allFASTA, ttt.allpeaklists, fillnaunassigned])

# organizes peaklists dataframe columns
fsut.write_title("ORGANIZING PEAKLIST COLUMNS' ORDER")
ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords, 
             ttt.column_organizor,
             args=[ttt.allpeaklists],
             kwargs={'performed_cs_correction':fsuv.perform_cs_correction})

## writes the parsed peaklists corresponding to the sidechains information
if ttt.has_sidechains and fsuv.use_sidechains:
    
    fsut.write_title("ORGANIZING PEAKLIST COLUMNS' ORDER FOR SIDECHAINS")
    ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords, 
                 ttt.column_organizor, args=[ttt.allsidechains],
                 kwargs={'sidechains':True})

# Generates Farseer cube. Which is a pd.Panel of all the peaklists
# that constitute the Fareer Experiment Set.
# The cube can be generated now because all the peaklists (pd.DataFrame)
# in the allpeaklists{} have now the same shape.
fsut.write_title('Farseer Cube Generated')
ttt.gen_Farseer_cube(use_sidechains=fsuv.use_sidechains)


#### Generates Titrations
# Farseer_titrations_dict stores the titrations that are to be evaluated.
# 'cond1' key would store all the titrations that progress in the
# first dimension
# aka first condition - usually the concentration range of the ligand.
#
# 'cond2' stores titrations in the second dimention,
# aka progresion along different mutants (default case)
#
# 'cond3', stores titrations along the third dimension,
# aka external conditions, for instance, dia and paramagnetic,
# temperature, etc...
fsut.write_title('GENERATING TITRATION DICTIONARIES')
Farseer_titrations_dict = gen_dim_tit_dict(ttt, ttt.peaklists_p5d)

# Perfors calculations and plots data
fsut.write_title('PERFORMS CALCULATIONS')
dimension_loop(Farseer_titrations_dict)


if ttt.has_sidechains and fsuv.use_sidechains:
    fsut.write_title('GENERATING TITRATION DICTIONARIES FOR SIDECHAINS')
    Farseer_SD_titrations_dict = gen_dim_tit_dict(ttt,
                                                  ttt.sidechains_p5d,
                                                  reso_type='Sidechains')
    fsut.write_title('PERFORMS CALCULATIONS FOR SIDECHAINS')
    dimension_loop(Farseer_SD_titrations_dict, sidechains=True)

# Representing the results comparisons
if fsuv.perform_comparisons:
    fsut.write_title('WRITES TITRATION COMPARISONS')
    
    # analyses comparisons.
    analyse_comparisons(Farseer_titrations_dict, fspar.p5d)
    
    if ttt.has_sidechains and fsuv.use_sidechains:
        fsut.write_title('WRITES TITRATION COMPARISONS FOR SIDECHAINS')
        analyse_comparisons(Farseer_SD_titrations_dict,
                            fspar.p5d, 
                            reso_type='Sidechains')

fsut.write_title('LOG ENDED')
fsut.write_log(datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
