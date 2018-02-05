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

Functions that format error messages.
"""
import sys
import textwrap

def title(s=''):
    return "    {:@^72}  ".format(" " + s + " ")

def bottom():
    return "    {:@^72}  ".format('')

def line(s=''):
    return "    @{:^70}@  ".format(s)

def referwet(n):
    return line("+ Refer to WET #{} +".format(n))

def format_msg(string):
    return "    @{:^70}@  ".format(string)

def gen_wet(t, s, n):
    
    ws = """
{}
{}
{}
{}
{}
{}

""".\
        format(
            title(t),
            line(),
             "\n".join(map(format_msg, textwrap.wrap(s, width=67))),
            line(),
            referwet(n),
            bottom()
            )
    
    return ws

def continue_abort():
    """ Asks user to decide behaviour. """
    choice = 'z'
    
    while not(choice in ['A', 'C']):
        choice = \
            input('> What do you want to do? [C]ontinue or [A]bort? ').upper()
    
    if choice == 'A':
        abort(abort_msg)
    
    elif choice == 'C':
        return 'Continuing...'

def abort(m=''):
    sys.exit(m)
    return

def end_good():
    s = \
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
    
    return s

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
