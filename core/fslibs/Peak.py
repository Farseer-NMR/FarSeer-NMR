"""
Copyright © 2017-2018 Farseer-NMR
Simon P. Skinner and João M.C. Teixeira

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
class Peak(object):
    """
    Contains information about a Peak.
    """

    def __init__(self,
        peak_number,
        positions,
        atoms,
        residue_type,
        residue_number,
        linewidths,
        height,
        volume,
        format_,
        fit_method=None,
        merit=None,
        volume_method=None,
        details=None
        ):
        
        # a counter for the peak
        self.peak_number = peak_number
        # chemical shift positions
        self.positions = positions  # list
        # atoms type (H, N, C, ...)
        # atoms and positions must match.
        self.atoms = atoms  #list
        # residue type: Cys, Ala, Met, ...
        self.residue_type = residue_type
        self.residue_number = residue_number
        self.linewidths = linewidths
        self.height = height
        self.volume = volume
        self.fit_method = fit_method
        self.merit = merit
        self.volume_method = volume_method
        self.details = details
        # the original format of the input peaklist
        self.format_ = format_
        

