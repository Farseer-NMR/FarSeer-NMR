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

import core.fslibs.Logger as Logger
from core.fslibs.plotting.PlottingBase import PlottingBase
from core.fslibs.plotting.ExperimentPlot import ExperimentPlot
from core.fslibs.plotting.BarPlotBase import BarPlotBase
from core.fslibs.WetHandler import WetHandler as fsw

class BarExtendedSideChains(ExperimentPlot, BarPlotBase):
    """
    Horizontal Extended Bar plotting template for Sidechains.
    
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
            Fit Method, Vol. Method, Details, ATOM; in this order.
        
        - config (opt, dict): a dictionary containing all the configuration
            parameters required for this plotting routine. If None provided
            uses the default configuraton. Access the default configuration
            via the default_config class attribute.
        
        - data_extra (opt, np.ndarray of shape [z,y,x]): extra ndarray to help
            on plotting the data passed as <data>.
                In the case of plotting theoretical PRE data, data_extra
                columns should be [Theo PRE, tag position].
        
        - partype (opt {'ppm', 'ratio'}, defaults None): 
            indicates the type of data that is being plotted, so that
            special option can be activated.
        
        - exp_names (opt, sequence type): list of the experiment names.
        
        - additional kwargs can be passed as **kwargs.
    
    """
    
    default_config = {
        "cols_page": 1,
        "rows_page": 6,
        
        "y_lims":(0,0.3),
        "ylabel":"CSPs",
        
        "subtitle_fn": "Arial",
        "subtitle_fs": 8,
        "subtitle_pad": 0.99,
        "subtitle_weight": "normal",
        
        "x_label_fn": "Arial",
        "x_label_fs": 8,
        "x_label_pad": 2,
        "x_label_weight": "bold",
        
        "y_label_fn": "Arial",
        "y_label_fs": 8,
        "y_label_pad": 3,
        "y_label_weight": "bold",
        "y_label_rot":90,
        
        "x_ticks_pad": 2,
        "x_ticks_len": 2,
        "x_ticks_fn": "monospace",
        "x_ticks_fs": 6,
        "x_ticks_rot": 90,
        "x_ticks_weight": "normal",
        "x_ticks_color_flag":True,
        
        "y_ticks_fn": "Arial",
        "y_ticks_fs": 6,
        "y_ticks_rot": 0,
        "y_ticks_pad": 1,
        "y_ticks_weight": "normal",
        "y_ticks_len": 2,
        
        "y_grid_flag": True,
        "y_grid_color": "lightgrey",
        "y_grid_linestyle": "-",
        "y_grid_linewidth": 0.2,
        "y_grid_alpha": 0.8,
        
        "theo_pre_color": "red",
        "theo_pre_lw": 1.0,
        
        "tag_cartoon_color": "black",
        "tag_cartoon_lw": 1.0,
        "tag_cartoon_ls": "-",
        
        "measured_color": "black",
        "missing_color": "red",
        "unassigned_color": "lightgrey",
        
        "bar_width": 0.8,
        "bar_alpha": 1,
        "bar_linewidth": 0,
        
        "threshold_flag": True,
        "threshold_color": "red",
        "threshold_linewidth": 0.5,
        "threshold_alpha": 0.8,
        "threshold_zorder":10,
        
        "mark_fontsize": 4,
        "mark_prolines_flag": True,
        "mark_prolines_symbol": "P",
        "mark_user_details_flag": True,
        "color_user_details_flag": True,
        "user_marks_dict": {
            "foo": "f",
            "mal": "m",
            "bem": "b"
        },
        "user_bar_colors_dict": {
            "foo": "green",
            "mal": "yellow",
            "bem": "magenta"
        },
        
        "hspace": 0.5,
        "wspace": 0.5
    }
    
    def __init__(self,
            data,
            data_info,
            config=None,
            data_extra=None,
            partype="",
            exp_names="",
            **kwargs
            ):
        super().__init__(
            data,
            data_info,
            config=config,
            partype=partype,
            exp_names=exp_names,
            **kwargs
            )
        
        self.logger = Logger.FarseerLogger(__name__).setup_log()
        self.logger.debug("BarExtendedHorizontal initiated")
        
        
        self.data_extra = data_extra
    
    def subplot(self, ax, data, data_info, exp_name, data_extra=None):
        """Configures subplot."""
        
        c = self.config
        col = self.info_cols
        self.logger.debug("Starting Subplot ###### {}".format(exp_name))
        
        data = np.nan_to_num(data)
        
        self.logger.debug(data)
        self.logger.debug(data_info)
        self.logger.debug(data_extra)
        
        number_of_residues_to_plot = data.size
        
        self.logger.debug(
            "Number of residues to plot: {}".format(number_of_residues_to_plot)
            )
        
        bars = ax.bar(
            range(number_of_residues_to_plot),
            data,
            width=c["bar_width"],
            align='center',
            alpha=c["bar_alpha"],
            linewidth=c["bar_linewidth"],
            zorder=4
            )
        
        self.logger.debug("Created bar plot: OK")
        
        # ticks positions:
        # this is used to fit both applyFASTA=True or False
        # reduces xticks to 100 as maximum to avoid ticklabel overlap
        if number_of_residues_to_plot > 100:
            xtick_spacing = number_of_residues_to_plot//100
        
        else:
            xtick_spacing = 1
        
        self.logger.debug("xtick_spacing set to: {}".format(xtick_spacing))
        
        self.logger.debug("data ResNo: {}".format(data_info[0::xtick_spacing,col['ResNo']]))
        self.logger.debug("data 1-letter: {}".format(data_info[0::xtick_spacing,col['1-letter']]))
        self.logger.debug("data ATOM: {}".format(data_info[0::xtick_spacing,col['ATOM']]))
        
        ticklabels = \
            np.core.defchararray.add(
                np.copy(data_info[0::xtick_spacing,col['ResNo']]).astype(str),
                np.copy(data_info[0::xtick_spacing,col['1-letter']]).astype(str)
                )
                
        ticklabels = \
            np.core.defchararray.add(
                ticklabels,
                np.copy(data_info[0::xtick_spacing,col['ATOM']]).astype(str)
                )
        
        self.logger.debug("Number of xticklabels: {}".format(len(ticklabels)))
        self.logger.debug("X Tick Labels. {}".format(ticklabels))
        
        # Configure XX ticks and Label
        ax.set_xticks(range(number_of_residues_to_plot))
        self.logger.debug("set_xticks: OK")
        
        ## https://github.com/matplotlib/matplotlib/issues/6266
        ax.set_xticklabels(
            ticklabels,
            fontname=c["x_ticks_fn"],
            fontsize=c["x_ticks_fs"],
            fontweight=c["x_ticks_weight"],
            rotation=c["x_ticks_rot"]
            )
        self.logger.debug("set_xticklabels: OK")
        
        # defines xticks colors
        if c["x_ticks_color_flag"]:
            self.logger.debug("Configuring x_ticks_color_flag...")
            self._set_item_colors(
                ax.get_xticklabels(),
                data_info[0::xtick_spacing,col['Peak Status']],
                {
                    'measured':c["measured_color"],
                    'missing':c["missing_color"],
                    'unassigned':c["unassigned_color"]
                    }
                )
            self.logger.debug("...Done")
        
        # Set subplot titles
        ax.set_title(
            exp_name,
            y=c["subtitle_pad"],
            fontsize=c["subtitle_fs"],
            fontname=c["subtitle_fn"],
            weight=c["subtitle_weight"]
            )
        self.logger.debug("Set title: OK")
        
        # defines bars colors
        self._set_item_colors(
            bars,
            data_info[:,col['Peak Status']],
            {
                'measured': c["measured_color"],
                'missing': c["missing_color"],
                'unassigned': c["unassigned_color"]
                }
            )
        self.logger.debug("set_item_colors: OK")
        
        # configures spines
        ax.spines['bottom'].set_zorder(10)
        ax.spines['top'].set_zorder(10)
        self.logger.debug("Spines set: OK")
        # cConfigures YY ticks
        ax.set_ylim(c["y_lims"][0], c["y_lims"][1])
        ax.locator_params(axis='y', tight=True, nbins=8)
        self.logger.debug("Set Y limits: OK")
        
        ax.set_yticklabels(
            ['{:.2f}'.format(yy) for yy in ax.get_yticks()],
            fontname=c["y_ticks_fn"],
            fontsize=c["y_ticks_fs"],
            fontweight=c["y_ticks_weight"],
            rotation=c["y_ticks_rot"]
            )
        self.logger.debug("Set Y tick labels: OK")
        
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
        self.logger.debug("Configured X and Y tick params: OK")
            
        # Set axes labels
        ax.set_xlabel(
            'Residue',
            fontname=c["x_label_fn"],
            fontsize=c["x_label_fs"],
            labelpad=c["x_label_pad"],
            weight=c["x_label_weight"],
            rotation=0
            )
        ax.set_ylabel(
            c["ylabel"],
            fontsize=c["y_label_fs"],
            labelpad=c["y_label_pad"],
            fontname=c["y_label_fn"],
            weight=c["y_label_weight"],
            rotation=c["y_label_rot"]
            )
        self.logger.debug("Configured X and Y labels")
        
        # Adds grid
        if c["y_grid_flag"]:
            ax.yaxis.grid(
                color=c["y_grid_color"],
                linestyle=c["y_grid_linestyle"],
                linewidth=c["y_grid_linewidth"],
                alpha=c["y_grid_alpha"],
                zorder=0
                )
            self.logger.debug("Configured grid: OK")
        
        # Adds red line to identify significant changes.
        if c["threshold_flag"] and self.ppm_data:
            self.logger.debug("... Starting Threshold draw")
            self._plot_threshold(
                ax,
                data,
                c["threshold_color"],
                c["threshold_linewidth"],
                c["threshold_alpha"],
                zorder=c["threshold_zorder"]
                )
            self.logger.debug("Threshold: OK")
        
        if c["mark_prolines_flag"]:
            self.logger.debug("... Starting Prolines Mark")
            self._text_marker(
                ax,
                range(number_of_residues_to_plot),
                data,
                data_info[:,col['1-letter']],
                {'P':c["mark_prolines_symbol"]},
                fs=c["mark_fontsize"]
                )
            self.logger.debug("Prolines Marked: OK")
        
        if c["mark_user_details_flag"]:
            self.logger.debug("... Starting User Details Mark")
            self._text_marker(
                ax,
                range(number_of_residues_to_plot),
                data,
                data_info[:,col['Details']],
                c["user_marks_dict"],
                fs=c["mark_fontsize"]
                )
            self.logger.debug("User marks: OK")
        
        if c["color_user_details_flag"]:
            self.logger.debug("... Starting User Colors Mark")
            self._set_item_colors(
                bars,
                data_info[:,col["Details"]],
                c["user_bar_colors_dict"]
                )
            self.logger.debug("Color user details: OK")
        
        return

if __name__ == "__main__":
    import os
    
    file_name = os.path.realpath(__file__)
    
    ######################################################################## 1
    
    print("### testing {}".format(file_name))
    
    
