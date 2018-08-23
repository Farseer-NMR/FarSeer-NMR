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
import sys
import textwrap

import logging
import logging.config
import core.fslibs.log_config as fslogconf

class WetHandler:
    """Handles Warning, Errors and Troubleshooting messages"""
    
    def __init__(
            self,
            msg_title='WET title not provided',
            msg='WET Message not provided',
            wet_num='WET Number not provided',
            gen=True):
        
        # initiates log
        self.logger = fslogconf.getLogger(__name__)
        logging.config.dictConfig(fslogconf.farseer_log_config)
        self.logger.debug('logger initiated')
        
        self.msg_title = msg_title
        self.msg = msg
        self.wet_num = wet_num
        if isinstance(wet_num, int):
            self.web_link = \
                "github.com/joaomcteixeira/FarSeer-NMR/wiki/WET-List#wet{}".\
                        format(self.wet_num)
        else:
            self.web_link = 'Web link not provided'
        
        self.logger.debug('Type, MSG and NUM configured correctly')
        
        if gen:
            self.generate_wet()
        else:
            sefl.wet = 'No WET defined'
    
    def _title(self, msg_title=''):
        return "    {:@^72}  ".format(" " + msg_title + " ")
    
    def _bottom(self):
        return "    {:@^72}  ".format('')

    def _line(self, s=''):
        return "    @{:^70}@  ".format(s)

    def referwet(self, n):
        return self._line("+ Refer to WET #{} +".format(n))

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
                self._title(t),
                self._line(),
                 "\n".join(map(self._format_msg, textwrap.wrap(msg, width=67))),
                self._line(),
                self.referwet(wet_num),
                self._line(s="please visit"),
                self._line(self.web_link),
                self._bottom()
                )
        
        self.logger.debug('WET Msg generated correctly')
        
        return None
    
    def print_wet(self):
        """Prints WET message"""
        print(self.wet)
        return None

    def continue_abort(self, choice='Z'):
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
            self.abort()
        
        elif choice == 'C':
            return 'Continuing...'

    def abort(self, m=''):
        abort_msg = m or self.abort_msg()
        sys.exit(abort_msg)
        return
    
    def end_well(self):
        """Returns the message annoucing Farseer-NMR performed correctly."""
        end_well = \
    """
{}
{}
{}
{}
    """.\
            format(
                self._bottom(), 
                self._line('Farseer-NMR completed correctly'),
                self._line('Bye :-)'),
                self._bottom()
                )
        return end_well

    def abort_msg(self):
        """Returns the abort message."""
        abort_msg = \
        """
{}
{}
{}
{}
        """.\
            format(
                self._bottom(), 
                self._line('Farseer-NMR aborted'),
                self._line('Bye :-('),
                self._bottom()
                )
        
        return abort_msg

if __name__ == '__main__':
    
    wet1 = WetHandler(
        msg_title='c00l',
        msg='Does everything looks good?',
        wet_num=999)
    
    wet2 = WetHandler()
    
    wet1.wet
    wet1.print_wet()
    
    wet2.wet
    wet2.print_wet()
    
    print(wet1.end_well())
    print(wet1.abort_msg())
    
    wet1.continue_abort(choice='C')
    print('continuing automatically...')
    wet1.continue_abort()
    print('continuing mannually...')
    wet1.continue_abort(choice='A')
