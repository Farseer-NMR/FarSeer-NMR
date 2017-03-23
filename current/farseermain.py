import datetime  # used to write the log file
import numpy as np
import pandas as pd
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
    if farseer_set.hasxx and fsuv.do1D:
        titrations_dict['D1'] = \
            farseer_set.gen_titration_dict(data_hyper_cube, 'D1', 
                                           farseer_set.xxcoords,
                                           farseer_set.yycoords,
                                           farseer_set.zzcoords,
                                           reso_type)
        

    # creates the titrations for the second condition (2D)
    if farseer_set.hasyy and fsuv.do2D:
        titrations_dict['D2'] = \
            farseer_set.gen_titration_dict(data_hyper_cube.transpose(2,0,1,3,4),
                                           'D2',
                                           farseer_set.yycoords,
                                           farseer_set.zzcoords,
                                           farseer_set.xxcoords,
                                           reso_type)

    # creates the titrations for the third condition (3D)  
    if farseer_set.haszz and fsuv.do3D:
        titrations_dict['D3'] = \
            farseer_set.gen_titration_dict(data_hyper_cube.transpose(1,2,0,3,4),
                                           'D3',
                                           farseer_set.zzcoords,
                                           farseer_set.xxcoords,
                                           farseer_set.yycoords,
                                           reso_type)
    
    return titrations_dict

def dimension_loop(titration_dict, sidechains=False):
    
    for dimension in sorted(titration_dict.keys()):
        fsut.write_log(fsut.dim_sperator(dimension, 'top'))
    
        for nextdim2 in sorted(titration_dict[dimension].keys()):
            fsut.write_log(fsut.dim_sperator(nextdim2, 'midle'))
            
            for nextdim1 in sorted(titration_dict[dimension][nextdim2].keys()):
                fsut.write_log(fsut.dim_sperator(nextdim1, 'own'))
                fsut.write_log('\n')  #exception
                
                perform_calcs(titration_dict[dimension][nextdim2][nextdim1])
            
                # PERFORMS FITS
                
                # EXPORTS AND PLOTS TITRATION DATA
                plot_tit_data(titration_dict[dimension][nextdim2][nextdim1])
                

def perform_calcs(tit_panel):
    
    for calccol, sourcecol in zip([fspar.param_settings.loc['PosF1_delta','calc_column_name'],
                                   fspar.param_settings.loc['PosF2_delta','calc_column_name']],
                                   ['Position F1','Position F2']):
                                                    
        tit_panel.calc_cs_diffs(calccol, sourcecol)
        

    for calccol, sourcecol in zip([fspar.param_settings.loc['Height_ratio','calc_column_name'],
                                   fspar.param_settings.loc['Vol_ratio','calc_column_name']],
                                   ['Height','Volume']):
                
        tit_panel.calc_ratio(calccol, sourcecol)
            
            
    tit_panel.calc_csp(calccol=fspar.param_settings.loc[fspar.calcparam_name_CSP,'calc_column_name'],
                       pos1=fspar.param_settings.loc[fspar.calcparam_name_PosF1_delta,'calc_column_name'],
                       pos2=fspar.param_settings.loc[fspar.calcparam_name_PosF2_delta,'calc_column_name'])
    

def plot_tit_data(tit_panel):
    '''
    This function was written because it serves normal titrations and
    control titrations.
    '''
    
    # EXPORTS CALCULATIONS
    tit_panel.export_titration()
    tit_panel.write_Chimera_attributes(fspar.param_settings.loc[:,'calc_column_name'],
                                       resformat=fsuv.chimera_att_select_format)
    
    # PLOTS DATA
    for calculated_parameter in fspar.param_settings.index:
        
        tit_panel.write_table(\
            fspar.param_settings.loc\
                [calculated_parameter, 'calc_column_name'])
        
        # if the user wants to plot this parameter
        if fspar.param_settings.loc[calculated_parameter,'plot_param_flag']:
            
            # Plot Extended Bar Plot
            if fsuv.plots_extended_bar:
                tit_panel.plot_base(calculated_parameter, 'exp', 'bar_extended',
                                    fspar.bar_ext_par_dict,
                                    cols_per_page=fsuv.ext_bar_cols_page,
                                    rows_per_page=fsuv.ext_bar_rows_page)
            
            # Plot Compacted Bar Plot
            if fsuv.plots_compacted_bar:
                tit_panel.plot_base(calculated_parameter, 'exp', 'bar_compacted',
                                    fspar.comp_bar_par_dict,
                                    cols_per_page=fsuv.comp_bar_cols_page,
                                    rows_per_page=fsuv.comp_bar_rows_page)
            
            # Plot Vertical Bar Plot
            if fsuv.plots_vertical_bar:
                tit_panel.plot_bar_vertical(calculated_parameter)
            
            # Plots Parameter Evolution Plot
            if fsuv.plots_residue_evolution:
                tit_panel.plot_base(calculated_parameter, 'res', 'res_evo',
                                    fspar.res_evo_par_dict,
                                    cols_per_page=fsuv.res_evo_cols_page,
                                    rows_per_page=fsuv.res_evo_rows_page)


def analyse_controls(tit_dict, reso_type='Backbone'):
    
    tit_dim_keys = {'D1':['D2','D3'],
                    'D2':['D3','D1'],
                    'D3':['D1','D2']}
    
    
    
    for dimension in sorted(tit_dict.keys()):
        fsut.write_log(fsut.dim_sperator(dimension, 'top'))
        
        Farseer_controls_hyper_panel = Panel5D_controls(tit_dict[dimension])
        
        if len(Farseer_controls_hyper_panel.labels) > 1:
        
            for nextdim2 in Farseer_controls_hyper_panel.items:
                fsut.write_log(fsut.dim_sperator(nextdim2, 'midle'))
                
                for nextdim1 in Farseer_controls_hyper_panel.cool:
                    fsut.write_log(fsut.dim_sperator(nextdim1, 'own'))
                    
                    control = fsT.Titration(np.array(Farseer_controls_hyper_panel.loc[nextdim1,:,nextdim2,:,:]),
                                            items=Farseer_controls_hyper_panel.labels,
                                            minor_axis=Farseer_controls_hyper_panel.minor_axis,
                                            major_axis=Farseer_controls_hyper_panel.major_axis)
                    
                    control.create_titration_attributes(
                                  tittype='C'+ dimension[-1], 
                                  owndims=Farseer_controls_hyper_panel.labels, 
                                  nextdim1=nextdim1, 
                                  nextdim2=nextdim2,
                                  subcontrol=tit_dim_keys[dimension][0],
                                  resonance_type=reso_type)
                    
                    
                    plot_tit_data(control)
                
        if len(Farseer_controls_hyper_panel.cool) > 1:
            
            for nextdim2 in Farseer_controls_hyper_panel.labels:
                fsut.write_log(fsut.dim_sperator(nextdim2, 'midle'))
                for nextdim1 in Farseer_controls_hyper_panel.items:
                    fsut.write_log(fsut.dim_sperator(nextdim1, 'own'))
                    
                    control = fsT.Titration(np.array(Farseer_controls_hyper_panel.loc[:,nextdim2,nextdim1,:,:]),
                                            items=Farseer_controls_hyper_panel.cool,
                                            minor_axis=Farseer_controls_hyper_panel.minor_axis,
                                            major_axis=Farseer_controls_hyper_panel.major_axis)
                                            
                    control.create_titration_attributes(tittype='C'+ dimension[-1],
                                  owndims=Farseer_controls_hyper_panel.cool, 
                                  nextdim1=nextdim1, 
                                  nextdim2=nextdim2,
                                  subcontrol=tit_dim_keys[dimension][1],
                                  resonance_type=reso_type)
                    
                    plot_tit_data(control)




# Starts Log
ltitle = fsut.write_title('LOG STARTED', onlytitle=True)
startlog = "{}{}\n".format(ltitle,
                           datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
fsut.write_log(startlog, mod='w')


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
             ttt.hasxx, fsuv.do1D,
             ttt.hasyy, fsuv.do2D,
             ttt.haszz, fsuv.do3D,
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
                 kwargs={'ref_res':fsuv.cs_correction_res_ref})

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
fsut.write_title('WRITTING PARSED PEAKLISTS IN .TSV FILES')
ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords,
             ttt.write_parsed_pkl, args=[ttt.allpeaklists])

## writes the parsed peaklists corresponding to the sidechains information
if ttt.has_sidechains and fsuv.use_sidechains:
    
    fsut.write_title("ORGANIZING PEAKLIST COLUMNS' ORDER FOR SIDECHAINS")
    ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords, 
                 ttt.column_organizor, args=[ttt.allsidechains])
    
    ttt.tricicle(ttt.zzcoords, ttt.yycoords, ttt.xxcoords,
                 ttt.write_parsed_pkl,
                 args=[ttt.allsidechains],
                 kwargs={'tsv_path':'Sidechains/parsed_sidechains_peaklists'})

# Generates Farseer cube. Which is a pd.Panel of all the peaklists
# that constitute the Fareer Experiment Set.
# The cube can be generated now because all the peaklists (pd.DataFrame)
# in the allpeaklists{} have now the same shape.
fsut.write_title('Farseer Cube Generated')
ttt.gen_Farseer_cube(use_sidechains=fsuv.use_sidechains)


#### Generates Titrations
fsut.write_title('GENERATING TITRATION DICTIONARIES')
# Farseer_titrations_dict stores the titrations that are to be evaluated.
# 'D1' key would store all the titrations that progress in the first dimension
# aka first condition - usually the concentration range of the ligand.
#
# 'D2' stores titrations in the second dimention, aka progresion along different
# mutants (default case)
#
# 'D3', stores titrations along the third dimension, aka external conditions,
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
if fsuv.perform_controls:
    
    fsut.write_title('WRITES CONROLS')
    
    Panel5D_controls = pd.core.panelnd.create_nd_panel_factory(klass_name='Panel5D',
                                                  orders=['cool', 'labels', 'items', 'major_axis', 'minor_axis'],
                                                  slices={'labels': 'labels',
                                                          'items': 'items',
                                                          'major_axis': 'major_axis',
                                                          'minor_axis': 'minor_axis'},
                                                  slicer=pd.Panel4D,
                                                  aliases={'major': 'index', 'minor': 'minor_axis'},
                                                  stat_axis=2)

    #Farseer_controls_dict = {}
    
    analyse_controls(Farseer_titrations_dict)
    
    if ttt.has_sidechains and fsuv.use_sidechains:
        analyse_controls(Farseer_SD_titrations_dict, reso_type='Sidechains')



fsut.write_title('LOG ENDED')
#endlog = "*** log ended: {}\n".format(datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
fsut.write_log(datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
