"""
Copyright © 2017-2018 Farseer-NMR
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
end_good = \
"""
{}
{}
{}
{}
""".\
        format(
            bottom(), 
            line('Farseer-NMR completed correctly'),
            line('Bye :-)'),
            bottom()
            )

abort_msg = \
"""
{}
{}
{}
{}
""".\
    format(
        bottom(), 
        line('Farseer-NMR aborted'),
        line('Bye :-('),
        bottom()
        )
