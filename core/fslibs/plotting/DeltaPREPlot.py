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
import itertools as it
import numpy as np
from matplotlib import pyplot as plt
from math import ceil


import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.plotting.ExperimentPlot import ExperimentPlot
from core.fslibs.plotting.BarPlotBase import BarPlotBase
from core.fslibs.WetHandler import WetHandler as fsw

class DeltaPREPlot(ExperimentPlot, BarPlotBase):
    """
    DeltaPRE Plot.
    
    Parameters:
        - data (np.array(dtype=int) of shape [z,y,x]): multidimensional array
            containain the dataset to be plot. Where:
                X) length=1. Is the column containing the calculated or observed NMR
                    parameter to be used as Y axis in plots,
                Y) are rows containing the X information for each residue
                Z) is [Y,X] for each experiment.
            Data can be further treated with data_select() method.
        
        - data_info (np.array(dtype=str) of shape [z,y,x]): same as <data>
            but for columns ResNo, 1-letter, 3-letter, Peak Status, Merit,
            Fit Method, Vol. Method, Details; in this order.
        
        - data_extra (np.ndarray of shape [z,y,x]): extra ndarray to help
            on plotting the data passed as <data> of shape [z, y, 2] where
                axis 3 is [tag position, Smooth PRE].
        
        - config (opt, dict): a dictionary containing all the configuration
            parameters required for this plotting routine. If None provided
            uses the default configuraton. Access the default configuration
            via the default_config class attribute.
        
        - exp_names (opt, sequence of str): names of each experiment.
        
        - additional kwargs can be passed as **kwargs.
    """
    
    default_config = {
        "cols_page": 3,
        "rows_page": 5,
        
        "ymax":1,
        "y_label": "$\\Delta$PRE$_(rc-exp)$",
        
        "subtitle_fn": "Arial",
        "subtitle_fs": 8,
        "subtitle_pad": 0.99,
        "subtitle_weight": "normal",
        
        "x_label_fn": "Arial",
        "x_label_fs": 8,
        "x_label_pad": 2,
        "x_label_weight": "bold",
        "x_label_rot": 0,
        
        "y_label_fn": "Arial",
        "y_label_fs": 8,
        "y_label_pad": 3,
        "y_label_weight": "bold",
        "y_label_rot":90,
        
        "x_ticks_pad": 0.5,
        "x_ticks_len": 2,
        "x_ticks_fn": "Arial",
        "x_ticks_fs": 6,
        "x_ticks_rot": 0,
        "x_ticks_weight": "normal",
        
        "y_ticks_fn": "Arial",
        "y_ticks_fs": 6,
        "y_ticks_rot": 0,
        "y_ticks_pad": 1,
        "y_ticks_weight": "normal",
        "y_ticks_len": 2,
        "y_ticks_nbins": 8,
        
        "y_grid_flag": True,
        "y_grid_color": "lightgrey",
        "y_grid_linestyle": "-",
        "y_grid_linewidth": 0.2,
        "y_grid_alpha": 0.8,
        
        "tag_cartoon_color": "black",
        "tag_cartoon_lw": 1.0,
        "tag_cartoon_ls": "-",
        
        "dpre_ms": 2,
        "dpre_alpha": 0.5,
        "smooth_lw": 1,
        "ref_color": "black",
        "color_init": "#000080",
        "color_end": "#FFD700",
        "grid_color": "grey",
        "shade": False,
        "shade_regions": [
            [
                0,
                10
            ],
            [
                20,
                25
            ]
        ],
        "res_highlight": False,
        "res_hl_list": [
            1,
            2
        ],
        "res_highlight_fs": 4,
        "res_highlight_y": 0.9,
        
        "hspace": 0.5,
        "wspace": 0.5
    }
    
    def __init__(self,
            data,
            data_info,
            data_extra,
            config=None,
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
        self.logger.debug("DeltaPREPlot initiated")
        
        
        self.data_extra = data_extra
    
    def plot_subplots(self):
        """
        Replaces BarPlotBase.plot_subplots method.
        """
        
        dp_colors = self._linear_gradient(
            self.config['color_init'],
            self.config['color_end'],
            n=self.data.shape[0]
            )
        dp_color = it.cycle(dp_colors['hex'])
        
        for i in range(self.data.shape[0]):
            
            self.logger.debug("Starting subplot no: {}".format(i))
            
            self.subplot(
                self.axs[i],
                self.data[0],
                self.data[i],
                self.data_info[i],
                self.experiment_names[i],
                self.data_extra[0],
                self.data_extra[i],
                color=next(dp_color)
                )
        
        return
    
    def subplot(
            self,
            ax,
            data_ref,
            data,
            data_info,
            experiment,
            data_extra_ref,
            data_extra,
            color='red'
            ):
        """
        Plots the Delta PRE data in scatter points and the gaussian
        smoothed curved.
        
        More information on this plot can be found in:
        Arbesú, M. et al. The Unique Domain Forms a Fuzzy Intramolecular 
        Complex in Src Family Kinases. Structure 25, 630–640.e4 (2017).
        
        Parameters:
            ax: matplotlib axis SINGLE object.
            
            data_ref: np.ndarray single axis): representing the reference
                Y data.
            
            data (np.ndarray single axis): represents current Y data
            
            data_info (np.ndarray of 2 axes, dtype=str): with all other
                relevant information in the form where cols are described by
                self.info_cols.
            
            experiment (str): experiment name given to subplot title.
            
            data_extra_ref: (np.ndarray single axis): representing the
                reference extra data.
            
            data (np.ndarray single axis): represents current extra data
            
            color (str): the color to plot the current data.
        """
        c = self.config
        col = self.info_cols
        k = self.kwargs
        
        number_of_residues_to_plot = data.size
        
        y_lims = (0, c["ymax"])
        self.logger.debug("ylims set to: {}".format(y_lims))
        # to solve .find Attribute Error
        # http://stackoverflow.com/questions/29437305/how-to-fix-attributeerror-series-object-has-no-attribute-find
        # plots dpre for first point in comparison
        #pmaskr = self.ix[0,:,calccol] > 0
        
        xdata = data_info[:,col['ResNo']].astype(float)
        
        self.logger.debug("xdata set to: {}".format(xdata))
        self.logger.debug("ydata set to: {}".format(data))
        
        ax.plot(
            xdata,
            data_ref,
            'o',
            markersize=c["dpre_ms"],
            markeredgewidth=0.0,
            c=c["ref_color"],
            alpha=c["dpre_alpha"],
            zorder=10
            )
        # plots dpre for titration data point
        #pmaskd = self.loc[experiment,:,calccol] > 0
        ax.plot(
            xdata,
            data,
            'o',
            c=color,
            markersize=c["dpre_ms"],
            markeredgewidth=0.0,
            alpha=c["dpre_alpha"],
            zorder=10
            )
        # plots dpre_smooth for first data point in comparison
        #pmaskr = self.ix[0,:,calccol+'_smooth'] > 0
        ysmooth = data_extra[:,1].astype(float)
        ysmooth_ref = data_extra_ref[:,1].astype(float)
        self.logger.debug("y smoothe data set to {}".format(ysmooth))
        self.logger.debug("y smoothe data set to {}".format(ysmooth_ref))
        
        ax.plot(
            xdata,
            ysmooth_ref,
            ls='-',
            lw=c["smooth_lw"],
            c=c["ref_color"],
            zorder=10
            )
        # plots dpre_smooth for data point
        #pmaskd = self.loc[experiment,:,calccol+'_smooth'] > 0
        ax.plot(
            xdata,
            ysmooth,
            ls='-',
            lw=c["smooth_lw"],
            c=color,
            zorder=10
            )
        # Configure subplot title
        ax.set_title(
            experiment,
            y=c["subtitle_pad"],
            fontsize=c["subtitle_fs"],
            fontname=c["subtitle_fn"],
            fontweight=c["subtitle_weight"]
            )
        # Set Ticks        
        if data.size > 100:
            xtick_spacing = data.size//100*10
        
        else:
            xtick_spacing = 10
        self.logger.debug("xtick_spacing set to: {}".format(xtick_spacing))
        
        xticks = range(
            xtick_spacing-1,
            number_of_residues_to_plot,
            xtick_spacing
            )
        ax.set_xticks(xticks)
        self.logger.debug("Setting xticks: {}".format([a for a in xticks]))
        
        initialresidue = int(data_info[0, col['ResNo']])
        finalresidue = int(data_info[-1, col['ResNo']])
        
        self.logger.debug("Initial residue: {}".format(initialresidue))
        self.logger.debug("Final residue: {}".format(finalresidue))
        
        first_tick = ceil(initialresidue/10)*xtick_spacing
        xticklabels = np.arange(first_tick, finalresidue, xtick_spacing)
        self.logger.debug("xticklabels: {}".format(xticklabels))
        
        # https://github.com/matplotlib/matplotlib/issues/6266
        ax.set_xticklabels(
            xticklabels,
            fontname=c["x_ticks_fn"],
            fontsize=c["x_ticks_fs"],
            fontweight=c["x_ticks_weight"],
            rotation=c["x_ticks_rot"]
            )
        # configures spines
        ax.spines['bottom'].set_zorder(10)
        ax.spines['top'].set_zorder(10)
        # Configures YY ticks
        ax.set_ylim(y_lims[0], y_lims[1])
        ax.locator_params(axis='y', tight=True, nbins=c["y_ticks_nbins"])
        ax.set_yticklabels(
            ['{:.2f}'.format(yy) for yy in ax.get_yticks()],
            fontname=c["y_ticks_fn"],
            fontsize=c["y_ticks_fs"],
            fontweight=c["y_ticks_weight"],
            rotation=c["y_ticks_rot"]
            )
        # configures tick params
        ax.margins(x=0.01)
        ax.tick_params(
            axis='x',
            pad=c["x_ticks_pad"],
            length=c["x_ticks_len"],
            direction='out'
            )
        ax.tick_params(
            axis='y',
            pad=c["y_ticks_pad"],
            length=c["y_ticks_len"],
            direction='out'
            )
        # Set axes labels
        ax.set_xlabel(
            'Residue',
            fontname=c["x_label_fn"],
            fontsize=c["x_label_fs"],
            labelpad=c["x_label_pad"],
            weight=c["x_label_weight"],
            rotation=c["x_label_rot"]
            )
        ax.set_ylabel(
            c["y_label"],
            fontsize=c["y_label_fs"],
            labelpad=c["y_label_pad"],
            fontname=c["y_label_fn"],
            weight=c["y_label_weight"],
            rotation=c["y_label_rot"]
            )
        
        # Adds grid
        if c["y_grid_flag"]:
            ax.yaxis.grid(
                color=c["y_grid_color"],
                linestyle=c["y_grid_linestyle"],
                linewidth=c["y_grid_linewidth"],
                alpha=c["y_grid_alpha"],
                zorder=0
                )
        
        if c["shade"]:
            for lmargin, rmargin in c["shade_regions"]:
                ax.fill(
                    [lmargin,rmargin,rmargin, lmargin],
                    [0,0,2,2],
                    c["grid_color"],
                    alpha=0.2
                    )
        
        if c["res_highlight"]:
            for rr in c["res_hl_list"]:
                ax.axvline(x=rr, ls=':', lw=0.3, color=c["grid_color"])
                rrmask = data_info[0,col['ResNo']] == str(rr)
                l1 = list(data_info[rrmask,col['1-letter']])
                ax.text(
                    rr,
                    y_lims[1]*c["res_highlight_y"],
                    l1[0],
                    ha='center',
                    va='center',
                    fontsize=c["res_highlight_fs"]
                    )
        
        self.logger.debug("tag: {}".format(data_extra[:,0]))
        where_tag = np.where(data_extra[:,0]=="*")
        self.logger.debug("where position: {}".format(where_tag))
        tag_position = list(range(number_of_residues_to_plot))[where_tag[0][0]]
        self.logger.debug("tag position: {}".format(tag_position))
        
        self._draw_paramagnetic_tag(
            ax,
            tag_position,
            y_lims[1],
            plottype='h',
            tag_color=c["tag_cartoon_color"],
            tag_ls=c["tag_cartoon_ls"],
            tag_lw=c["tag_cartoon_lw"]
            )
        self.logger.debug("Tag drawn")
        
        return

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
    
    plot = DeltaPREPlot(
        full_data_set[:,:,23].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        data_extra=full_data_set[:,:,[22, 24]],
        exp_names=["ref", "d10", "d20"]
        )
    
    plot.plot()
    plot.save_figure("dpre.pdf")
