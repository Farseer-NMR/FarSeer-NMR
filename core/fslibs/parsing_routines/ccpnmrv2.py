"""
Copyright © 2017-2018 Farseer-NMR
Teixeira, J.M.C., Skinner, S.P., Arbesú, M. et al. J Biomol NMR (2018).
https://doi.org/10.1007/s10858-018-0182-5

João M.C. Teixeira and Simon P. Skinner

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

from core.fslibs.Peak import Peak

def parse_ccpnmrv2_peaklist(peaklist_file):
    """
    Bypasses CCPNMRv2 peaklists.
    
    This peaklist is not parsed to Peak, a list with one
    dummy Peak element is created with .format_ = ccpnmrv2
    so that it is bypassed directly to spectra in
    core.setup_farseer_calculation.py
    
    Parameters:
        - peaklist_file: path to peaklist file.
    
    Returns peakList object
    """
    
    peakList = list()
    
    peakList.append(
        Peak(
            peak_number=None,
            positions=None,
            atoms=None,
            residue_number=None,
            residue_type=None,
            linewidths=[None, None],
            height=None,
            volume=None,
            format_='ccpnmrv2'
            ))
    
    return peakList
    
