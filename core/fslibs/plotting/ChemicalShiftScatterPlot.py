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

import core.fslibs.Logger as Logger
from core.fslibs.plotting.ResiduePlot import ResiduePlot
from core.fslibs.WetHandler import WetHandler as fsw

class ChemicalShiftScatterPlot(ResiduePlot):
    """
    Represents the evolution of a given parameter along the whole series
    for each residue separately.
    
    Parameters:
        - data (np.array(dtype=float) of shape [z,y,x]): multidimensional array
            containain the dataset to be plot. Where:
                x) of length 2. Two columns containing the calculated or observed NMR
                    parameters to be used as for X and Y axis in plots.
                    For example: F1 delta (ppm) and F2 delta (ppm) data.
                    Index 0 is plotted in the X axis and index 1 in the Y.
                    
                y) are rows representing residues
                
                z) the progression of the data. Each y residue has X data
                along Z.
                
        
        - data_info (np.array(dtype=str) of shape [z,y,x]): same as <data>
            but x represent columns ResNo, 1-letter, 3-letter, Peak Status,
            Merit, Fit Method, Vol. Method, Details; in this order according
            to self.info_cols.
        
        - config (opt, dict): a dictionary containing all the configuration
            parameters required for this plotting routine. If None provided
            uses the default configuraton. Access the default configuration
            via the default_config class attribute.
        
        - exp_names (opt, sequence of str): names of each experiment.
        
        - data_extra (opt, np.array): can be used to pass additional data
            required for specific implementations.
        
        - additional kwargs can be passed as **kwargs.
    """
    
    default_config = {
        
        "cols_page": 5,
        "rows_page": 8,
        
        "hspace": 0.5,
        "wspace": 0.5,
        
        "subtitle_fn": "Arial",
        "subtitle_fs": 8,
        "subtitle_pad": 0.98,
        "subtitle_weight": "normal",
        
        "x_label_fn": "Arial",
        "x_label_fs": 6,
        "x_label_pad": 2,
        "x_label_weight": "normal",
        "x_label": "1H (ppm)",
        
        "y_label_fn": "Arial",
        "y_label_fs": 6,
        "y_label_pad": 10,
        "y_label_weight": "normal",
        "y_label": "15N (ppm)",
        
        "x_ticks_fn": "Arial",
        "x_ticks_fs": 5,
        "x_ticks_pad": 1,
        "x_ticks_weight": "normal",
        "x_ticks_rot": 30,
        "x_ticks_len":2,
        
        "y_ticks_fn": "Arial",
        "y_ticks_fs": 5,
        "y_ticks_pad": 1,
        "y_ticks_weight": "normal",
        "y_ticks_rot": 0,
        "y_ticks_len":2,
        
        "ticks_nbins": 5,
        "scale": 0.01,
        
        "mk_type": "color",
        "markers": [
            "^",
            ">",
            "v",
            "<",
            "s",
            "p",
            "h",
            "8",
            "*",
            "D"
        ],
        "mksize": 20,
        "mk_start_color": "#696969",
        "mk_end_color": "#000000",
        "mk_color": ["none"],
        "mk_edgecolors": ["black"],
        "mk_missing_color": "red",
        "hide_missing": False
        }
    
    def __init__(self,
            data,
            data_info,
            config=None,
            data_extra=None,
            exp_names=None,
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
        self.logger.debug("ChemicalShiftScatter initiated")
        
        self.data_extra = data_extra
        self.logger.debug("Data extra saved as {}".format(data_extra))
        
        return
    
    def subplot(self, ax, data, data_info):
        """
        Encloses subplot architecture.
        
        - Parameters:
            - ax: matplotlib axis single object
            - data (np.ndarray of shape (x,2), dtype float): with data for
                Y axis where [:,0] is the "F1_delta" and [:,1] is "F2_delta".
            - data_info (np.ndarray, dtype str): with all other relevant
                information in the form where cols are described by
                self.info_cols.
        """
        
        c = self.config
        col = self.info_cols
        k = self.kwargs
        
        def set_tick_labels():
            # adjust the ticks to a maximum of 4.
            # http://stackoverflow.com/questions/6682784/how-to-reduce-number-of-ticks-with-matplotlib
            ax.locator_params(axis='both', tight=True, nbins=c["ticks_nbins"])
            ax.set_xticklabels(
                ax.get_xticks(),
                fontname=c["x_ticks_fn"],
                fontsize=c["x_ticks_fs"],
                fontweight=c["x_ticks_weight"],
                rotation=c["x_ticks_rot"]
                )
            ax.set_yticklabels(
                ax.get_yticks(),
                fontname=c["y_ticks_fn"],
                fontsize=c["y_ticks_fs"],
                fontweight=c["y_ticks_weight"],
                rotation=c["y_ticks_rot"]
                )
        
                # defines subplot title
        subtitle = \
            np.core.defchararray.add(
                np.copy(data_info[0,col['ResNo']]),
                np.copy(data_info[0,col['1-letter']])
                )
        
        ax.set_title(
            subtitle,
            y=c["subtitle_pad"],
            fontsize=c["subtitle_fs"],
            fontname=c["subtitle_fn"],
            fontweight=c["subtitle_weight"]
            )
        # Configure Axis Ticks
        ax.xaxis.tick_bottom()
        ax.tick_params(
            axis='x',
            pad=c["x_ticks_pad"],
            length=c["x_ticks_len"],
            direction='out'
            )
        ax.yaxis.tick_left()
        ax.tick_params(
            axis='y',
            pad=c["y_ticks_pad"],
            length=c["y_ticks_len"],
            direction='out'
            )
        ## Configure axes labels
        ax.set_xlabel(
            c["x_label"],
            fontsize=c["x_label_fs"],
            labelpad=c["x_label_pad"],
            fontname=c["x_label_fn"],
            weight=c["x_label_weight"]
            )
        ## Configure YY ticks/label
        ax.set_ylabel(
            c["y_label"],
            fontsize=c["y_label_fs"],
            labelpad=c["y_label_pad"],
            fontname=c["y_label_fn"],
            weight=c["y_label_weight"],
            rotation=-90
            )
        
        # check assignment
        # if residue is unassigned, identifies in the subplot
        if data_info[0,col['Peak Status']] == 'unassigned':
            ax.text(
                0,
                0,
                'unassigned',
                fontsize=7,
                fontname='Arial',
                va='center',
                ha='center'
                )
            ax.set_xlim(-1,1)
            ax.set_ylim(-1,1)
            set_tick_labels()
            ax.invert_xaxis()
            ax.invert_yaxis()
            return
        
        elif not(np.any(data[:,0].any())) and not(np.any(data[:,1])) \
                or not(np.any(data_info[:,col['Peak Status']] == 'measured')):
            ax.text(
                0,
                0,
                'all data lost',
                fontsize=7,
                fontname='Arial',
                va='center',
                ha='center'
                )
            ax.set_xlim(-1,1)
            ax.set_ylim(-1,1)
            set_tick_labels()
            ax.invert_xaxis()
            ax.invert_yaxis()
            return
        
        # Plots data
        if c["mk_type"] == 'shape':
            # represents the points in different shapes
            mcycle = it.cycle(c["markers"])
            ccycle = it.cycle(c["mk_color"])
            cedge = it.cycle(c["mk_edgecolors"])
            
            for i in range(data.shape[0]):
                print('here')
                if data_info[i,col["Peak Status"]] in ['missing', 'unassigned'] \
                        and c["hide_missing"]:
                    next(mcycle)
                    next(ccycle)
                    next(cedge)
                    print('hiding_missing')
                
                elif data_info[i,col['Peak Status']] == 'missing':
                    print('elif1')
                    ax.scatter(
                        data[i,0],
                        data[i,1],
                        marker=next(mcycle),
                        s=c["mk_size"],
                        c=next(ccycle),
                        edgecolors=c["mk_missing_color"]
                        )
                    next(cedge)
                
                else:
                    print('else')
                    ax.scatter(
                        data[i,0],
                        data[i,1],
                        marker=next(mcycle),
                        s=c["mk_size"],
                        c=next(ccycle),
                        edgecolors=next(cedge)
                        )
        
        elif c["mk_type"] == 'color':
            # represents the points as circles with a gradient of color
            mk_color = self._linear_gradient(
                c["mk_start_color"],
                finish_hex=c["mk_end_color"],
                n=data.shape[0]
                )
            # this is used instead of passing a list to .scatter because
            # of colouring in red the missing peaks.
            mccycle = it.cycle(mk_color['hex'])
            
            for j in range(data.shape[0]):
                if data_info[j,col['Peak Status']] == 'missing':
                    if c["hide_missing"]:
                        continue
                    ax.scatter(
                        data[j,0],
                        data[j,1],
                        marker='o',
                        s=c["mk_size"],
                        c=c["mk_missing_color"],
                        edgecolors='none'
                        )
                
                else:
                    ax.scatter(
                        data[j,0],
                        data[j,1],
                        marker='o',
                        s=c["mk_size"],
                        c=next(mccycle),
                        edgecolors='none'
                        )
        
        measured = data_info[:,col['Peak Status']] == 'measured'
        self.logger.debug("Measured mask: {}".format(measured))
        xlimmin = \
            -c["scale"]*2 \
            if np.ndarray.min(np.nan_to_num(data[measured,0])) > -c["scale"] \
            else np.ndarray.min(np.nan_to_num(data[measured,0]))*1.5
        xlimmax = \
            c["scale"]*2 \
            if np.ndarray.max(np.nan_to_num(data[measured,0])) < c["scale"] \
            else np.ndarray.max(np.nan_to_num(data[measured,0]))*1.5
        ylimmin = \
            -c["scale"]*2 \
            if np.ndarray.min(np.nan_to_num(data[measured,1])) > -c["scale"] \
            else np.ndarray.min(np.nan_to_num(data[measured,1]))*1.5
        ylimmax = \
            c["scale"]*2 \
            if np.ndarray.max(np.nan_to_num(data[measured,1])) < c["scale"] \
            else np.ndarray.max(np.nan_to_num(data[measured,1]))*1.5
        
        ax.set_xlim(xlimmin, xlimmax)
        ax.set_ylim(ylimmin, ylimmax)
        ## Invert axes for representation as in a spectrum
        ax.invert_xaxis()
        ax.invert_yaxis()
        set_tick_labels()
        # draws axis 0 dotted line
        ax.hlines(
            0,
            -100,
            100,
            colors='black',
            linestyles='dotted',
            linewidth=0.25
            )
        ax.vlines(
            0,
            -100,
            100,
            colors='black',
            linestyles='dotted',
            linewidth=0.25
            )
        # draws center scale
        ax.hlines(
            0,
            -c["scale"],
            c["scale"],
            colors='darkblue',
            linestyles='-',
            linewidth=1
            )
        ax.vlines(
            0,
            -c["scale"],
            c["scale"],
            colors='darkblue',
            linestyles='-',
            linewidth=1
            )
        
        return
        
if __name__ == "__main__":
    
    import os
    
    file_name = os.path.realpath(__file__)
    
    ######################################################################## 1
    
    print("### testing {}".format(file_name))
    
    dataset_path = os.path.join(
        os.path.dirname(file_name),
        'testing',
        'csps'
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
    
    plot = ChemicalShiftScatterPlot(
        full_data_set[:,:,[19,20]].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        exp_names=["0","25","50","100","200","400","500"]
        )
    
    plot.plot()
    plot.save_figure('cs_scatter.pdf')
    
    c = {
        "mk_type": "color",
        "mk_start_color": "#e5ff00",
        "mk_end_color": "#021056",
        "mk_missing_color": "magenta",
        "hide_missing": True
    }
    
    plot = ChemicalShiftScatterPlot(
        full_data_set[:,:,[19,20]].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        config=c,
        exp_names=["0","25","50","100","200","400","500"]
        )
    
    plot.plot()
    plot.save_figure('cs_scatter_color.pdf')
