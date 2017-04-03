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
    :farseer_set: the FarseerSet object with all the data of the titrations
    :data_hyper_cube: the 5D cube with all the titration data Pandas.Series
    :reso_type: identifies if we are dealing with Backbone or Sidechain data
                data idenified this is will be stored in different folders
    """
    
    # to facilitate the analysis with for loops, all the different
    # titrations experiments we are going to analyse will be stored 
    # in a dictionary
    titrations_dict = {}

    # creates the titrations for the first condition (1D)
    if farseer_set.hasxx and fsuv.do_titvar1:
        titrations_dict['titvar1'] = \
            farseer_set.gen_titration_dict(data_hyper_cube, 'titvar1', 
                                           farseer_set.xxcoords,
                                           farseer_set.yycoords,
                                           farseer_set.zzcoords,
                                           reso_type)
        

    # creates the titrations for the second condition (2D)
    if farseer_set.hasyy and fsuv.do_titvar2:
        titrations_dict['titvar2'] = \
            farseer_set.gen_titration_dict(data_hyper_cube.transpose(2,0,1,3,4),
                                           'titvar2',
                                           farseer_set.yycoords,
                                           farseer_set.zzcoords,
                                           farseer_set.xxcoords,
                                           reso_type)

    # creates the titrations for the third condition (3D)  
    if farseer_set.haszz and fsuv.do_titvar3:
        titrations_dict['titvar3'] = \
            farseer_set.gen_titration_dict(data_hyper_cube.transpose(1,2,0,3,4),
                                           'titvar3',
                                           farseer_set.zzcoords,
                                           farseer_set.xxcoords,
                                           farseer_set.yycoords,
                                           reso_type)
    
    return titrations_dict

def dimension_loop(titration_dict, sidechains=False):
    
    for dimension in sorted(titration_dict.keys()):
        fsut.write_log(fsut.dim_sperator(dimension, 'top'))
    
        for dim2_pts in sorted(titration_dict[dimension].keys()):
            fsut.write_log(fsut.dim_sperator(dim2_pts, 'midle'))
            
            for dim1_pts in sorted(titration_dict[dimension][dim2_pts].keys()):
                fsut.write_log(fsut.dim_sperator(dim1_pts, 'own'))
                fsut.write_log('\n')  #exception
                
                
                
                
                perform_calcs(titration_dict[dimension][dim2_pts][dim1_pts])
            
                # PERFORMS FITS
                # only if analysing the first condition
                # which is the one defined to analyse concentration ranges.
                if fsuv.perform_resevo_fit and \
                    titration_dict[dimension][dim2_pts][dim1_pts].tittype == 'titvar1':
                    
                    if len(fsuv.fit_x_values) != \
                        titration_dict[dimension][dim2_pts][dim1_pts].shape[0]:
                        raise ValueError('!!! Values given for x axis in fitting (fitting_x_values) do not match length of titvar1 variables.')
                    else:
                        perform_fits(titration_dict[dimension][dim2_pts][dim1_pts])
                
                
                # Loads theoretical PRE file only if analysing the third dimension.
                if fsuv.apply_PRE_analysis and \
                    titration_dict[dimension][dim2_pts][dim1_pts].tittype == 'titvar3':
                        
                    PRE_analysis(titration_dict[dimension][dim2_pts][dim1_pts], fsuv.spectra_path, dim2_pts)
                
                # EXPORTS AND PLOTS TITRATION DATA
                plot_tit_data(titration_dict[dimension][dim2_pts][dim1_pts])
                
                
                

def perform_calcs(tit_panel):
    """
    Performs the calculations.
    """
    
    if fsuv.plots_CSP:
    
        #diffs
        tit_panel.calc_cs_diffs(fsuv.calccol_name_PosF1_delta, 'Position F1')
        tit_panel.calc_cs_diffs(fsuv.calccol_name_PosF2_delta, 'Position F2')
    
        #csps
        tit_panel.calc_csp(calccol=fsuv.calccol_name_CSP,
                        pos1=fsuv.calccol_name_PosF1_delta,
                        pos2=fsuv.calccol_name_PosF2_delta)
    
    else:
        if fsuv.plots_PosF1_delta:
            tit_panel.calc_cs_diffs(fsuv.calccol_name_PosF1_delta, 'Position F1')
        if fsuv.plots_PosF2_delta:
            tit_panel.calc_cs_diffs(fsuv.calccol_name_PosF2_delta, 'Position F2')
        
    #ratios
    if fsuv.plots_Height_ratio:
        tit_panel.calc_ratio(fsuv.calccol_name_Height_ratio, 'Height')
    if fsuv.plots_Volume_ratio:
        tit_panel.calc_ratio(fsuv.calccol_name_Volume_ratio, 'Volume')
    
def PRE_analysis(tit_panel, spectra_path, conditions):
    
    tit_panel.load_theoretical_PRE(spectra_path, conditions)
    for sourcecol, targetcol in zip(fspar.param_settings.index[3:],\
                                    ['H_DPRE', 'V_DPRE']):
        tit_panel.calc_Delta_PRE(sourcecol, targetcol)
    pass

def perform_fits(tit_panel):
    """
    Performs fits in H1, 15N and CSPs.
    """
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
            
            tit_panel.write_table(calculated_parameter)
            
            tit_panel.write_Chimera_attributes(calculated_parameter,
                                       resformat=fsuv.chimera_att_select_format)
            
            if tit_panel.resonance_type == 'Backbone':
            
                # Plot Extended Bar Plot
                if fsuv.plots_extended_bar:
                    tit_panel.plot_base(calculated_parameter, 'exp', 'bar_extended',
                                    fspar.bar_ext_par_dict,
                                    par_ylims=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_scale'],
                                    ylabel=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_label'],
                                    cols_per_page=fsuv.ext_bar_cols_page,
                                    rows_per_page=fsuv.ext_bar_rows_page,
                                    fig_height=fsuv.fig_height,
                                    fig_width=fsuv.fig_width,
                                    fig_file_type=fsuv.fig_file_type,
                                    fig_dpi=fsuv.fig_dpi)
            
                # Plot Compacted Bar Plot
                if fsuv.plots_compacted_bar:
                    tit_panel.plot_base(calculated_parameter, 'exp', 'bar_compacted',
                                    fspar.comp_bar_par_dict,
                                    par_ylims=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_scale'],
                                    ylabel=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_label'],
                                    cols_per_page=fsuv.comp_bar_cols_page,
                                    rows_per_page=fsuv.comp_bar_rows_page,
                                    fig_height=fsuv.fig_height,
                                    fig_width=fsuv.fig_width,
                                    fig_file_type=fsuv.fig_file_type,
                                    fig_dpi=fsuv.fig_dpi)
            
                # Plot Vertical Bar Plot
                if fsuv.plots_vertical_bar:
                    tit_panel.plot_base(calculated_parameter, 'exp', 'bar_vertical',
                                    fspar.bar_vert_par_dict,
                                    par_ylims=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_scale'],
                                    ylabel=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_label'],
                                    cols_per_page=fsuv.vert_bar_cols_page,
                                    rows_per_page=fsuv.vert_bar_rows_page,
                                    fig_height=fsuv.fig_height,
                                    fig_width=fsuv.fig_width,
                                    fig_file_type=fsuv.fig_file_type,
                                    fig_dpi=fsuv.fig_dpi)
            
            # Sidechain data is represented in a different bar plot
            elif tit_panel.resonance_type == 'Sidechains'\
                and fsuv.plots_extended_bar:
                #do
                tit_panel.plot_base(calculated_parameter, 'exp', 'bar_extended',
                                    fspar.bar_ext_par_dict,
                                    par_ylims=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_scale'],
                                    ylabel=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_label'],
                                    cols_per_page=fsuv.ext_bar_cols_page,
                                    rows_per_page=fsuv.ext_bar_rows_page,
                                    fig_height=fsuv.fig_height,
                                    fig_width=fsuv.fig_width/2,
                                    fig_file_type=fsuv.fig_file_type,
                                    fig_dpi=fsuv.fig_dpi)
            
            # Plots Parameter Evolution Plot
            if fsuv.plots_residue_evolution:
                tit_panel.plot_base(calculated_parameter, 'res', 'res_evo',
                                    fspar.res_evo_par_dict,
                                    par_ylims=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_scale'],
                                    ylabel=fspar.param_settings.loc[calculated_parameter,'plot_yy_axis_label'],
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


def analyse_comparisons(tit_dict, reso_type='Backbone'):
    
    tit_dim_keys = {'titvar1':['titvar2','titvar3'],
                    'titvar2':['titvar3','titvar1'],
                    'titvar3':['titvar1','titvar2']}
    
    
    
    for dimension in sorted(tit_dict.keys()):
        fsut.write_log(fsut.dim_sperator(dimension, 'top'))
        
        Farseer_comparisons_hyper_panel = Panel5D_comparisons(tit_dict[dimension])
        
        if len(Farseer_comparisons_hyper_panel.labels) > 1:
        
            for dim2_pts in Farseer_comparisons_hyper_panel.items:
                fsut.write_log(fsut.dim_sperator(dim2_pts, 'midle'))
                
                for dim1_pts in Farseer_comparisons_hyper_panel.cool:
                    fsut.write_log(fsut.dim_sperator(dim1_pts, 'own'))
                    fsut.write_log('\n')
                    
                    control = fsT.Titration(np.array(Farseer_comparisons_hyper_panel.loc[dim1_pts,:,dim2_pts,:,:]),
                                            items=Farseer_comparisons_hyper_panel.labels,
                                            minor_axis=Farseer_comparisons_hyper_panel.minor_axis,
                                            major_axis=Farseer_comparisons_hyper_panel.major_axis)
                    
                    control.create_titration_attributes(
                                  tittype='C'+ dimension[-1], 
                                  owndim_pts=Farseer_comparisons_hyper_panel.labels, 
                                  dim1_pts=dim1_pts, 
                                  dim2_pts=dim2_pts,
                                  dim_comparison=tit_dim_keys[dimension][0],
                                  resonance_type=reso_type)
                    
                    
                    plot_tit_data(control)
        else:
            
            fsut.write_log('*** There are no points to compare with in {}\n'.format(tit_dim_keys[dimension][0]))
            
        if len(Farseer_comparisons_hyper_panel.cool) > 1:
            
            for dim2_pts in Farseer_comparisons_hyper_panel.labels:
                fsut.write_log(fsut.dim_sperator(dim2_pts, 'midle'))
                for dim1_pts in Farseer_comparisons_hyper_panel.items:
                    fsut.write_log(fsut.dim_sperator(dim1_pts, 'own'))
                    
                    control = fsT.Titration(np.array(Farseer_comparisons_hyper_panel.loc[:,dim2_pts,dim1_pts,:,:]),
                                            items=Farseer_comparisons_hyper_panel.cool,
                                            minor_axis=Farseer_comparisons_hyper_panel.minor_axis,
                                            major_axis=Farseer_comparisons_hyper_panel.major_axis)
                                            
                    control.create_titration_attributes(tittype='C'+ dimension[-1],
                                  owndim_pts=Farseer_comparisons_hyper_panel.cool, 
                                  dim1_pts=dim1_pts, 
                                  dim2_pts=dim2_pts,
                                  dim_comparison=tit_dim_keys[dimension][1],
                                  resonance_type=reso_type)
                    
                    plot_tit_data(control)
        else:
            
            fsut.write_log('*** There are no points to compare with in {}\n'.format(tit_dim_keys[dimension][1]))


# Starts Log
ltitle = fsut.write_title('LOG STARTED', onlytitle=True)
startlog = "{}{}\n".format(ltitle,
                           datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
fsut.write_log(startlog, mod='w')

# backups code
cwd = os.getcwd()
script_wd = os.path.dirname(os.path.realpath(__file__))

fsut.write_log('\n-> Farseer base dictory: {}\n'.format(script_wd))
fsut.write_log('-> current working directiory: {}\n'.format(cwd))

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
             ttt.hasxx, fsuv.do_titvar1,
             ttt.hasyy, fsuv.do_titvar2,
             ttt.haszz, fsuv.do_titvar3,
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
fillnalost = {
'Peak Status': 'lost',
'Merit': 0,
'Details': 'None'}

## 1st) expands the residue 'lost' information to other dimensions
# this operation has to be perform prior to identify the lost residues in the
# same dimension
if fsuv.expand_lost_yy or fsuv.expand_lost_zz:
    fsut.write_title('EXPANDS LOST RESIDUES TO OTHER CONDITIONS/DIMENSIONS')
    
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

    if ttt.has_sidechains and fsuv.use_sidechains:
        fsut.write_title('SIDECHAINS: EXPANDS LOST RESIDUES TO OTHER CONDITIONS/DIMENSIONS')
        
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
    fsut.write_title('ADDS LOST SIDE CHAIN RESIDUES BASED ON THE REFERENCE LIST')
    
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

# writes parsed peaklists in ccpnmv2 format Farseer extended
#fsut.write_title('WRITTING PARSED PEAKLISTS IN .TSV FILES')
#ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords,
             #ttt.write_parsed_pkl, args=[ttt.allpeaklists])

## writes the parsed peaklists corresponding to the sidechains information
if ttt.has_sidechains and fsuv.use_sidechains:
    
    fsut.write_title("ORGANIZING PEAKLIST COLUMNS' ORDER FOR SIDECHAINS")
    ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords, 
                 ttt.column_organizor, args=[ttt.allsidechains],
                 kwargs={'sidechains':True})
    
    #ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords,
                 #ttt.write_parsed_pkl,
                 #args=[ttt.allsidechains],
                 #kwargs={'tsv_path':'Sidechains/parsed_sidechains_peaklists'})

# Generates Farseer cube. Which is a pd.Panel of all the peaklists
# that constitute the Fareer Experiment Set.
# The cube can be generated now because all the peaklists (pd.DataFrame)
# in the allpeaklists{} have now the same shape.
fsut.write_title('Farseer Cube Generated')
ttt.gen_Farseer_cube(use_sidechains=fsuv.use_sidechains)


#### Generates Titrations
fsut.write_title('GENERATING TITRATION DICTIONARIES')
# Farseer_titrations_dict stores the titrations that are to be evaluated.
# 'titvar1' key would store all the titrations that progress in the first dimension
# aka first condition - usually the concentration range of the ligand.
#
# 'titvar2' stores titrations in the second dimention, aka progresion along different
# mutants (default case)
#
# 'titvar3', stores titrations along the third dimension, aka external conditions,
# for instance, dia and paramagnetic, temperature, etc...
Farseer_titrations_dict = gen_dim_tit_dict(ttt, ttt.peaklists_p5d)

# Performing calculations and plotting data
fsut.write_title('PERFORMS CALCULATIONS')
dimension_loop(Farseer_titrations_dict)


if ttt.has_sidechains and fsuv.use_sidechains:
    fsut.write_title('GENERATING TITRATION DICTIONARIES FOR SIDECHAINS')
    Farseer_SD_titrations_dict = gen_dim_tit_dict(ttt,
                                                  ttt.sidechains_p5d,
                                                  reso_type='Sidechains')
    fsut.write_title('PERFORMS CALCULATIONS FOR SIDECHAINS')
    dimension_loop(Farseer_SD_titrations_dict, sidechains=True)



# Performing Controls
if fsuv.perform_comparisons:
    
    fsut.write_title('WRITES TITRATION COMPARISONS')
    
    Panel5D_comparisons = pd.core.panelnd.create_nd_panel_factory(klass_name='Panel5D',
                                                  orders=['cool', 'labels', 'items', 'major_axis', 'minor_axis'],
                                                  slices={'labels': 'labels',
                                                          'items': 'items',
                                                          'major_axis': 'major_axis',
                                                          'minor_axis': 'minor_axis'},
                                                  slicer=pd.Panel4D,
                                                  aliases={'major': 'index', 'minor': 'minor_axis'},
                                                  stat_axis=2)

    #Farseer_comparisons_dict = {}
    
    analyse_comparisons(Farseer_titrations_dict)
    
    if ttt.has_sidechains and fsuv.use_sidechains:
        fsut.write_title('WRITES TITRATION COMPARISONS FOR SIDECHAINS')
        analyse_comparisons(Farseer_SD_titrations_dict, reso_type='Sidechains')



fsut.write_title('LOG ENDED')
#endlog = "*** log ended: {}\n".format(datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
fsut.write_log(datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
