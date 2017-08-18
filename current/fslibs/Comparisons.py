import numpy as np
import pandas as pd

class Comparisons:
    """
    This class stores the Titration data of all the titrations
    and parsed it so that results are compared accross titrations.
    """
    def __init__(self,
                 dimension_dict,
                 selfdim='cond',
                 other_dim_keys=['condy','condz'],
                 resonance_type='Backbone'):
        """
        :dimension_dict: is a dictionary containing all the titrations
                         for that dimension.
        """
        self.p5d = pd.core.panelnd.create_nd_panel_factory(\
            klass_name='Panel5D',
            orders=['cool', 'labels', 'items', 'major_axis', 'minor_axis'],
            slices={'labels': 'labels',
                    'items': 'items',
                    'major_axis': 'major_axis',
                    'minor_axis': 'minor_axis'},
            slicer=pd.Panel4D,
            aliases={'major': 'index', 'minor': 'minor_axis'},
            stat_axis=2)
        
        # condition/dimension over which the calculations where
        # performed
        self.dimension = selfdim
        
        # generates a p5d with all the titrations passed
        # 
        self.hyper_panel = self.p5d(dimension_dict)
        
        
        # stores the dimension keys over which the comparisons
        # will be performed
        self.other_dim_keys = other_dim_keys
        
        # resonance typel. Either Backbone or Sidechain.
        self.resonance_type = resonance_type
        
        # the dictionaries containing the fss.FarseerSeries of the dimensions
        # along which to be compared.
        self.all_next_dim = {}
        self.all_prev_dim = {}
        
        # initially considers that there are no points to compare with
        # in the labels and cool dimensions
        # becomes true after gen_comparison_*()
        self.has_points_next_dim = False
        self.has_points_prev_dim = False
        

        self.log = ''  # all log goes here
        self.log_export_onthefly = False
        self.log_export_name = 'Comparison_log.md'
    
    
    def log_r(self, logstr, istitle=False):
        """
        Registers the log and prints to the user.
        
        :logstr: the string to be registered in the log
        :istitle: flag to format logstr as a title
        """
        if istitle:
            logstr = """
{0}  
{1}  
{0}  
""".format('*'*79, logstr)
        else:
            logstr += '  \n'
        
        print(logstr)
        self.log += logstr
        
        # appends log to external file on the fly
        if self.log_export_onthefly:
            with open(self.log_export_name, 'a') as logfile:
                logfile.write(logstr)
        return
    
    def exports_log(self, mod='w', logfile_name='FarseerSet_log.md'):
        """ Exports log to external file. """
        with open(logfile_name, mod) as logfile:
            logfile.write(self.log)
        return
    
    def abort(self):
        self.log_r(fsw.abort_string)
        fsw.abort()
        return
        
    def gen_next_dim(self, series_class, comp_kwargs):
        """
        Generates dictionary with the Series parsed along the next dimension
        of the <self.selfdim>. Series are of class <series_class>, usually
        fss.FarseerSeries.
        """
        
        self.log_r(\
            'GENERATING COMPARISONS FOR **{}** ALONG LABELS: {}'.format(\
                    self.dimension, list(self.hyper_panel.labels)),
            istitle=True)
        
        if len(self.hyper_panel.labels) > 1:
            # DO
            for dp2 in self.hyper_panel.items:
                self.all_next_dim.setdefault(dp2, {})
                for dp1 in self.hyper_panel.cool:
                    # DO
                    comparison = \
                        series_class(\
                            np.array(\
                                self.hyper_panel.loc[dp1,:,dp2,:,:]),
                            items=self.hyper_panel.labels,
                            minor_axis=self.hyper_panel.minor_axis,
                            major_axis=self.hyper_panel.major_axis)
                    
                    comparison.create_attributes(\
                        series_axis='C{}'.format(self.dimension[-1]), 
                        owndim_pts=self.hyper_panel.labels, 
                        dim1_pts=dp1,
                        dim2_pts=dp2,
                        dim_comparison=self.other_dim_keys[0],
                        resonance_type=self.resonance_type,
                        **comp_kwargs)
                    
                    self.all_next_dim[dp2].setdefault(dp1, comparison)
                    # DONE
            
            self.log_r('** Generated comparison dictionary')
            
            self.has_points_next_dim = True
            # DONE
        elif len(self.hyper_panel.labels) <= 1:
            self.log_r('*** There are no points to compare along {}'.\
                format(self.other_dim_keys[0]))
                    
        return
    
    def gen_prev_dim(self, series_class, comp_kwargs):
        """
        Generates dictionary with the Series parsed along the previrous
        dimension of the <self.selfdim>. Series are of class <series_class>, 
        usually fss.FarseerSeries.
        """
        
        self.log_r(\
            'GENERATING COMPARISONS FOR **{}** ALONG COOLs: {}'.format(\
                    self.dimension, list(self.hyper_panel.cool)),
            istitle=True)
        
        if len(self.hyper_panel.cool) > 1:
            for dp2 in self.hyper_panel.labels:
                self.all_prev_dim.setdefault(dp2, {})
                for dp1 in self.hyper_panel.items:
                    
                    comparison = \
                        series_class(\
                            np.array(\
                                self.hyper_panel.loc[:,dp2,dp1,:,:]),
                            items=self.hyper_panel.cool,
                            minor_axis=self.hyper_panel.minor_axis,
                            major_axis=self.hyper_panel.major_axis)
                    
                    comparison.create_attributes(\
                        series_axis='C{}'.format(self.dimension[-1]), 
                        owndim_pts=self.hyper_panel.cool, 
                        dim1_pts=dp1,
                        dim2_pts=dp2,
                        dim_comparison=self.other_dim_keys[1],
                        resonance_type=self.resonance_type,
                        **comp_kwargs)
                    
                    self.all_prev_dim[dp2].setdefault(dp1, comparison)
            
            self.log_r('** Generated comparison dictionary')
            
            self.has_points_prev_dim = True
            
        elif len(self.hyper_panel.labels) <= 1:
            self.log_r('*** There are no points to compare along {}'.\
                format(self.other_dim_keys[1]))
                    
        return
    
    def transfer_log(self):
        """
        Transfers logs from the comparison Series to the main class object.
        """
        if self.has_points_next_dim:
            for dim2_pt in sorted(self.all_next_dim.keys()):
                for dim1_pt in sorted(self.all_next_dim[dim2_pt].keys()):
                    self.log += self.all_next_dim[dim2_pt][dim1_pt].log
        if self.has_points_prev_dim:
            for dim2_pt in sorted(self.all_prev_dim.keys()):
                for dim1_pt in sorted(self.all_prev_dim[dim2_pt].keys()):
                    self.log += self.all_prev_dim[dim2_pt][dim1_pt].log
