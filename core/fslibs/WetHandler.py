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

import logging
import logging.config
import core.fslibs.log_config as fslogconf

class WetHandler:
    """Handles Warning, Errors and Troubleshooting messages"""
    
    def __init__(self, msg_type='', msg='', wet_num=0):
        
        # initiates log
        self.logger = fslogconf.getLogger(__name__)
        logging.config.dictConfig(fslogconf.farseer_log_config)
        self.logger.debug('logger initiated')
        
        if not msg_type:
            self.logger.debug('WET Message type not provided')
        
        if not msg:
            self.logger.debug('WET Message not provided')
        
        if not wet_num:
            self.logger.debug('WET Number not provided')
        
        self.msg_type = msg_type
        self.msg = msg
        self.wet_num = wet_num
        self.logger.debug('Type, MSG and NUM configured correctly')
        
        self.generate_wet()
    
    def _title(self, msg_type=''):
        return "    {:@^72}  ".format(" " + msg_type + " ")
    
    def _bottom(self):
        return "    {:@^72}  ".format('')

    def _line(self, s=''):
        return "    @{:^70}@  ".format(s)

    def referwet(self, n):
        return line("+ Refer to WET #{} +".format(n))

    def _format_msg(self, s):
        return "    @{:^70}@  ".format(s)

    def generate_wet(self, title='', msg='', wet_num=0):
        """
        Generates wet message box. Message type, message and 
        WET number are optional, default to class instantiation.
        
        Parameters:
            - title (str): the message type: ERROR, Trouble, WARNING, ...
            - msg (str): the WET full message
            . wet_num (int): the documentation index WET number of the message
        
        Returns:
            - None. Assigns self.wet
        """
    
        t = title or self.msg_title
        msg = msg or self.msg
        wet_num = wet_num or self.wet_num
        
        self.wet = """
{}
{}
{}
{}
{}
{}
{}
{}

    """.\
            format(
                _title(t),
                _line(),
                 "\n".join(map(_format_msg, textwrap.wrap(msg, width=67))),
                _line(),
                referwet(n),
                _line(s="please visit"),
                _line(
                    s="github.com/joaomcteixeira/FarSeer-NMR/wiki/WET-List#wet{}".\
                        format(n)
                    ),
                _bottom()
                )
        
        self.logger.debug('WET Msg generated correctly')
        
        return None
    
    def print_wet(self):
        """Prints WET message"""
        print(self.wet)
        return None

    def continue_abort(self, choice=z):
        """
        Asks user to decide behaviour. A predifined choice can be given.
        
        Parameters:
            - choice (str): ['A', 'C']. 
        """
    
        while not(choice in ['A', 'C']):
            self.logger.debug('Entered while cycle correctly')
            choice = \
                input('> What do you want to do? [C]ontinue or [A]bort? ').\
                    upper()
        
        self.logger.debug('Choice selected "{}"'.format(choice))
        
        if choice == 'A':
            self.abort(abort_msg)
        
        elif choice == 'C':
            return 'Continuing...'

    def abort(self, m=''):
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
