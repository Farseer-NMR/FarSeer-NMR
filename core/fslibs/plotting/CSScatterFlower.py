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
from core.fslibs.plotting.SinglePlot import SinglePlot
from core.fslibs.WetHandler import WetHandler as fsw


class CSScatterFlower(SinglePlot):
    """
    """
    
    default_config = {
    
        "cols_page": 2,
        "rows_page": 3,
        
        "x_label": "1H (ppm)",
        "y_label": "15N (ppm)",
        
        "xlim":1,
        "ylim":1,
        
        "mk_size": 8,
        
        "color_grad": True,
        "mk_start_color": "#696969",
        "mk_end_color": "#000000",
        "color_list": [],
        
        "res_label_color": "gold",
        
        "x_label_fn": "Arial",
        "x_label_fs": 10,
        "x_label_pad": 5,
        "x_label_weight": "normal",
        
        "y_label_fn": "Arial",
        "y_label_fs": 10,
        "y_label_pad": 10,
        "y_label_weight": "normal",
        "y_label_rot":-90,
        
        "x_ticks_fn": "Arial",
        "x_ticks_fs": 8,
        "x_ticks_pad": 1,
        "x_ticks_len":2,
        "x_ticks_weight": "normal",
        "x_ticks_rot": 0,
        
        "y_ticks_fn": "Arial",
        "y_ticks_fs": 8,
        "y_ticks_pad": 1,
        "y_ticks_len":2,
        "y_ticks_weight": "normal",
        "y_ticks_rot": 0,
        
        "hspace": 0.1,
        "wspace": 0.1
    }
    
    def __init__(
            self,
            data,
            data_info,
            config=None,
            data_extra=None,
            **kwargs
            ):
        
        super().__init__(
            data,
            data_info,
            config=config,
            data_extra=data_extra,
            **kwargs
            )
        
        return
    
    def subplot(self, ax, data, data_info):
        
        c = self.config
        col = self.info_cols
        k = self.kwargs
        
        self.logger.debug("data.shape[0]: {}".format(data.shape[0]))
        if c["color_grad"]:
            mk_color = self._linear_gradient(
                c["mk_start_color"],
                finish_hex=c["mk_end_color"],
                n=data.shape[0]
                )['hex']  # function returns a dictionary
        
        # otherwise the user has input a list of colors
        else: 
            mk_color = c["color_list"]
                
        for residue in range(data.shape[1]):
            
            self.logger.debug("Plotting residue:{}".format(data_info[:,residue,col['ResNo']]))
            
            if data_info[0,residue,col['Peak Status']] in ('unassigned','missing'):
                continue
            
            mesmask = data_info[:,residue,col['Peak Status']] == 'measured'
            
            self.logger.debug("Measured mask: {}".format(mesmask))
            # data is 0 1H and 1 15N
            
            are_there_nan = np.any(np.isnan(data[:,residue,[0,1]]))
            if are_there_nan:
                
                self.logger.debug("Found NaN: {}".format(are_there_nan))
                
                msg = "Information for residue {} was kept out of this plot.\
This is because a NaN value was identified in the chemical shift information.\
This can be explained if this residues was missing in the reference peaklist \
but measured in a subsequent peaklist".\
                    format(np.array2string(data_info[mesmask,residue,col['ResNo']]))
                
                wet36 = fsw(msg_title='NOTE', msg=msg, wet_num=36)
                self.logger.info(wet36.wet)
                continue
            
            ax.scatter(
                data[mesmask,residue,0],
                data[mesmask,residue,1],
                c=mk_color,
                s=c["mk_size"],
                zorder=9
                )
            ax.text(
                float(data[mesmask,residue,0][-1])*1.05,
                float(data[mesmask,residue,1][-1])*1.05,
                data_info[0,residue,col['ResNo']],
                fontsize=4,
                color=c["res_label_color"],
                zorder=10
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
            rotation=c["y_label_rot"]
            )
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
        ax.set_xlim(-c["xlim"], c["xlim"])
        ax.set_ylim(-c["ylim"], c["ylim"])
        # remember in NMR spectra the ppm scale is 'inverted' :-)
        ax.invert_xaxis()
        ax.invert_yaxis()
        ax.locator_params(axis='both', tight=True, nbins=10)
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
    
    plot = CSScatterFlower(
        full_data_set[:,:,[19,20]].astype(float),
        full_data_set[:,:,[0,1,2,3,4,11,12,15]],
        )
    
    plot.plot()
    plot.save_figure("scatter_flower.pdf")
