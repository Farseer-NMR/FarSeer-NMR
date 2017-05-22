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
                 reso_type='Backbone'):
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
        self.reso_type = reso_type
        
        # the dictionaries containing the fst.Titrations of the dimensions
        # along which to be compared.
        self.allClabels = {}
        self.allCcool = {}
        
        # initially considers that there are no points to compare with
        # in the labels and cool dimensions
        # becomes true after gen_comparison_*()
        self.haslabels = False
        self.hascool = False
        
        # registers log
        self.log = ''
    
    
    def log_r(self, logstr):
        """
        Registers the log and prints to the user.
        
        :logstring: the string to be registered in the log
        """
        logstr = '{}\n'.format(logstr)
        print(logstr)
        self.log += logstr
        return
    
    def log_t(self, titlestr):
        """Formats a title for log."""
        log_title = \
            '\n\n{0} {1}\n'.format('*'*5, titlestr)
        print(log_title)
        self.log += log_title
        return
    
    def write_log(self, mod='a', path='farseer.log'):
        with open(path, mod) as logfile:
            logfile.write(self.log)
        return
        
    def gen_comparison_labels(self, titration_class):
        """
        Generates dictionary with all the comparisons over the labels.
        """
        
        self.log_t(\
            'GENERATING COMPARISONS FOR **{}** ALONG LABELS: {}'.format(\
                    self.dimension, list(self.hyper_panel.labels)))
        
        if len(self.hyper_panel.labels) > 1:
            for dim2_pt in self.hyper_panel.items:
                self.allClabels.setdefault(dim2_pt, {})
                for dim1_pt in self.hyper_panel.cool:
                    
                    comparison = \
                        titration_class(\
                            np.array(\
                                self.hyper_panel.loc[dim1_pt,:,dim2_pt,:,:]),
                            items=self.hyper_panel.labels,
                            minor_axis=self.hyper_panel.minor_axis,
                            major_axis=self.hyper_panel.major_axis)
                    
                    comparison.create_titration_attributes(\
                        titration_type='C{}'.format(self.dimension[-1]), 
                        owndim_pts=self.hyper_panel.labels, 
                        dim1_pts=dim1_pt,
                        dim2_pts=dim2_pt,
                        dim_comparison=self.other_dim_keys[0],
                        resonance_type=self.reso_type)
                    
                    self.allClabels[dim2_pt].setdefault(dim1_pt, comparison)
                    
            self.log_r('** Generated comparison dictionary')
            
            self.haslabels = True
            
        elif len(self.hyper_panel.labels) <= 1:
            self.log_r('*** There are no points to compare for {}\n'.\
                format(self.other_dim_keys[0]))
                    
        return
    
    def gen_comparison_cool(self, titration_class):
        """
        Generates dictionary with all the comparisons over the cools.
        """
        
        self.log_t('GENERATING COMPARISONS FOR **{}** ALONG COOLs: {}'.format(\
                    self.dimension, list(self.hyper_panel.cool)))
        
        if len(self.hyper_panel.cool) > 1:
            for dim2_pt in self.hyper_panel.labels:
                self.allCcool.setdefault(dim2_pt, {})
                for dim1_pt in self.hyper_panel.items:
                    
                    comparison = \
                        titration_class(\
                            np.array(\
                                self.hyper_panel.loc[:,dim2_pt,dim1_pt,:,:]),
                            items=self.hyper_panel.cool,
                            minor_axis=self.hyper_panel.minor_axis,
                            major_axis=self.hyper_panel.major_axis)
                    
                    comparison.create_titration_attributes(\
                        titration_type='C{}'.format(self.dimension[-1]), 
                        owndim_pts=self.hyper_panel.cool, 
                        dim1_pts=dim1_pt,
                        dim2_pts=dim2_pt,
                        dim_comparison=self.other_dim_keys[1],
                        resonance_type=self.reso_type)
                    
                    self.allCcool[dim2_pt].setdefault(dim1_pt, comparison)
            
            self.log_r('** Generated comparison dictionary')
            
            self.hascool = True
            
        elif len(self.hyper_panel.labels) <= 1:
            self.log_r('*** There are no points to compare for {}\n'.\
                format(self.other_dim_keys[1]))
                    
        return
    
    def transfer_log(self):
        if self.haslabels:
            for dim2_pt in sorted(self.allClabels.keys()):
                for dim1_pt in sorted(self.allClabels[dim2_pt].keys()):
                    self.log += self.allClabels[dim2_pt][dim1_pt].log
        if self.hascool:
            for dim2_pt in sorted(self.allCcool.keys()):
                for dim1_pt in sorted(self.allCcool[dim2_pt].keys()):
                    self.log += self.allCcool[dim2_pt][dim1_pt].log
