"""
Copyright © 2017-2018 Farseer-NMR

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

Farseer-NMR is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Farseer-NMR is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Farseer-NMR. If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np
from matplotlib import pyplot as plt
from math import ceil

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.plotting.ExperimentPlot import ExperimentPlot
from core.fslibs.plotting.BarPlotBase import BarPlotBase
from core.fslibs.WetHandler import WetHandler as fsw

class DeltaPREHeatmap(ExperimentPlot, BarPlotBase):
    """
    DeltaPRE Heatmap plotting template.
    
    Parameters:
        - data (np.array(dtype=float) of shape [z,y,x]): multidimensional array
            containain the dataset to be plot. Where:
                X) length=1. Is the column containing the calculated or observed NMR
                    parameter to be used as Y axis in plots,
                Y) are rows containing the X information for each residue
                Z) is [Y,X] for each experiment.
            Data can be further treated with data_select() method.
        
        - data_info (np.array(dtype=str) of shape [z,y,x]): same as <data>
            but for columns ResNo, 1-letter, 3-letter, Peak Status, Merit,
            Fit Method, Vol. Method, Details; in this order.
        
        - config (opt, dict): a dictionary containing all the configuration
            parameters required for this plotting routine. If None provided
            uses the default configuraton. Access the default configuration
            via the default_config class attribute.
        
        - data_extra (opt, np.ndarray of shape [z,y,x]): extra ndarray to help
            on plotting the data passed as <data>.
                In the case of plotting theoretical PRE data, data_extra
                columns should be [tag position].
        
        - partype (opt {'ppm', 'ratio'}, defaults None): 
            indicates the type of data that is being plotted, so that
            special option can be activated.
        
        - exp_names (opt, sequence of str): names of each experiment.
        
        - additional kwargs can be passed as **kwargs.
    
    """
    
    default_config = {
        "cols_page": 1,
        "rows_page": 20,
        
        "vmin": 0.05,
        "vmax": 1.0,
        
        "x_ticks_fn": "Arial",
        "x_ticks_fs": 4,
        "x_ticks_pad": 1,
        "x_ticks_len": 1.5,
        "x_ticks_weight": "normal",
        "x_ticks_rot": 0,
        
        "y_label_fn": "Arial",
        "y_label_fs": 3,
        "y_label_pad": 2,
        "y_label_weight": "bold",
        
        "top_margin":0.9,
        "right_margin": 0.22,
        "bottom_margin": 0,
        
        "cbar_font_size": 4,
        
        "tag_line_color": "red",
        "tag_line_ls": "-",
        "tag_line_lw": 0.8,
        
        "hspace": 0,
        "rightspace": 0.3
    }
    
    # right margin and bottom margin are depecrated
    
    def __init__(self,
            data,
            data_info,
            config=None,
            data_extra=None,
            exp_names="",
            **kwargs
            ):
        super().__init__(
            data,
            data_info,
            config=config,
            exp_names=exp_names,
            **kwargs
            )
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("BarExtendedVertical initiated")
        
        
        self.data_extra = data_extra
    
    def plot_subplots(self):
        
        i = super().plot_subplots()
        
        self.final_subplot(self.axs[i], self.data[i], self.data_info[i])
        
        return
    
    def subplot(self, ax, data, data_info, exp_name, data_extra=None):
        """
        """
        
        c = self.config
        col = self.info_cols
        k = self.kwargs
        
        vmin = c["vmin"]
        vmax = c["vmax"]
        
        Dcmap = np.array((np.nan_to_num(data), np.nan_to_num(data)))
        
        self.cleg = ax.pcolor(Dcmap, cmap='binary', vmin=vmin, vmax=vmax)
        ax.tick_params(axis='y', left='off')
        ax.tick_params(axis='x', bottom='off')
        # http://stackoverflow.com/questions/2176424/hiding-axis-text-in-matplotlib-plots
        ax.get_yaxis().set_ticks([])
        ax.get_xaxis().set_visible(False)
        ax.set_ylabel(
            exp_name,
            fontsize=c["y_label_fs"],
            labelpad=c["y_label_pad"],
            fontname=c["y_label_fn"],
            weight=c["y_label_weight"]
            )
        ax.spines['bottom'].set_zorder(10)
        ax.spines['top'].set_zorder(10)
        
        is_valid = self._validades_for_PRE_data(exp_name)
        
        if is_valid:
            
            tag_position = self._finds_para_tag(data_extra)
            # position is shifts 0.5 units
            tag_position += 0.5
        
            self._draw_paramagnetic_tag(
                ax,
                tag_position,
                2,
                plottype = 'heatmap',
                tag_color=c["tag_line_color"],
                tag_ls=c["tag_line_ls"],
                tag_lw=c["tag_line_lw"]
                )
        
        return
    
    def final_subplot(self, ax, data, data_info):
        
        c = self.config
        col = self.info_cols
        k = self.kwargs
        vmin = c["vmin"]
        vmax = c["vmax"]
        
        bottom_margin = 1/self.data.shape[0]
        
        cbar = plt.colorbar(
            self.cleg,
            ticks=[vmin, vmax/4, vmax/4*2, vmax/4*3, vmax],
            orientation='vertical',
            cax = self.figure.add_axes(
                [
                    c["rightspace"]+0.01, 
                    bottom_margin,
                    0.01, 
                    c["top_margin"]-bottom_margin
                    ]
                )
            )
        
        cbar.ax.tick_params(labelsize=c["cbar_font_size"])
        ax.get_xaxis().set_visible(True)
        ax.tick_params(
            axis='x',
            bottom='on',
            length=c["x_ticks_len"],
            pad=c["x_ticks_pad"]
            )
        
        # ticks positions:
        if data.size > 100:
            xtick_spacing = data.size//100*10
        
        else:
            xtick_spacing = 10
            
        self.logger.debug("xtick_spacing set to: {}".format(xtick_spacing))
        xticks = range(
            xtick_spacing,
            data.size,
            xtick_spacing
            )
        
        # is this plot ticks are shifted in comparison with other barplots.
        xticks = [i-0.5 for i in xticks]
        
        self.logger.debug("Setting xticks: {}".format([a for a in xticks]))
        # -1 needs to be given because xticks star from 0
        ax.set_xticks(xticks)
        self.logger.debug("set_xticks: OK")
        
        # xtick labels
        initialresidue = int(data_info[0, col['ResNo']])
        finalresidue = int(data_info[-1, col['ResNo']])
        
        first_tick = ceil(initialresidue/10)*xtick_spacing
        xticklabels = np.arange(first_tick, finalresidue, xtick_spacing)
        self.logger.debug("xticklabels: {}".format(xticklabels))
        
        ## https://github.com/matplotlib/matplotlib/issues/6266
        ax.set_xticklabels(
            xticklabels,
            fontname=c["x_ticks_fn"],
            fontsize=c["x_ticks_fs"],
            fontweight=c["x_ticks_weight"],
            rotation=c["x_ticks_rot"]
            )
        self.logger.debug("set_xticklabels: OK")
        return
    
    def adjust_subplots(self):
        self.figure.subplots_adjust(
            hspace=self.config["hspace"],
            right=self.config["rightspace"]
            )

if __name__ == "__main__":
    
    import os
    
    file_name = os.path.realpath(__file__)
    
    dataset_path = os.path.join(
        os.path.dirname(file_name),
        'testing',
        'dpre_plot'
        )
        
    print("testing dataset: {}".format(dataset_path))
    
    a = []
    for f in sorted(os.listdir(dataset_path)):
        print("reading: {}".format(f))
        a.append(
            np.genfromtxt(
                os.path.join(dataset_path, f),
                delimiter=',',
                skip_header=1,
                dtype=str,
                missing_values='NaN'
                )
            )
    
    full_data_set = np.stack(a, axis=0)
    print("dataset shape: {}".format(full_data_set.shape))
    
    pre_args = {
        "PRE_loaded":True,
        "series_axis":'Cz',
        "next_dim":"01_para",
        "paramagnetic_names":["01_para"]
        }
    
    plot = DeltaPREHeatmap(
        full_data_set[:,:,24].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        data_extra=full_data_set[:,:,22],
        exp_names=["ref", "d10", "d20"],
        **pre_args
        )
    
    plot.plot()
    plot.save_figure("dpre_heatmap.pdf")
