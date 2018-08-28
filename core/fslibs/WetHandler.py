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

#import logging
#import logging.config
#import core.fslibs.log_config as fslogconf
from core.fslibs.Logger import FarseerLogger

#from core.fslibs.Logger import FarseerLogger

class WetHandler:
    """Handles Warning, Errors and Troubleshooting messages"""
    
    def __init__(
            self,
            msg_title='WET title not provided',
            msg='WET Message not provided',
            wet_num='WET Number not provided',
            text_wrap_width=67,
            gen=True):
        """
        Parameters (all optional):
            - msg_title (str): the WET title (WARNING, ERROR, etc..)
            - msg (str): the full WET message
            - wet_num (int): the number of the WET according to the WET list
                https://github.com/joaomcteixeira/FarSeer-NMR/wiki/WET-List
            - text_wrap_width (int): the width of the text box
            - gen (bool): wether generates WET message (defaults: True)
        """
        
        # initiates log
        self.logger = FarseerLogger(__name__).setup_log()
        self.logger.debug('logger initiated')
        
        # sets variables
        self.msg_title = msg_title
        self.msg = msg
        self.wet_num = wet_num
        self.gen = gen
        # these variables are normally unused but they can be set nonetheless
        self.text_wrap_width = text_wrap_width
        self.title_bottom_width = text_wrap_width + 5
        self.line_width = text_wrap_width + 3
        
        # configures link or the lack of it
        if isinstance(wet_num, int):
            self.web_link = \
                "github.com/joaomcteixeira/FarSeer-NMR/wiki/WET-List#wet{}".\
                        format(self.wet_num)
        else:
            self.web_link = 'Web link not provided'
        
        self.logger.debug('Type, MSG and NUM configured correctly')
        
        # generate_wet() is used when a WET message is wanted. If only 
        # a end_well or abort_msg is required the user can instantiate the
        # class without generating the WET message.
        if self.gen:
            self.generate_wet()
        else:
            self.wet = 'No WET defined'
    
    def _title(self, msg_title='', width=0):
        """
        Returns a title marker of @ chars
        
        Parameters:
            - msg_title (opt, str): the title message
            - width (opt, int): the width of the marker
        """
        width = width or self.title_bottom_width
        a = "    {:@^" + str(width) + "}  "
        
        return a.format(" " + msg_title + " ")
    
    def _bottom(self, width=0):
        """
        Returns a bottom marker of @ chars
        
        Parameters:
            - width (opt, int): the width of the marker
        """
        width = width or self.title_bottom_width
        a = "    {:@^" + str(width) + "}  "
        
        return a.format('')

    def _line(self, s='', line_width=0):
        """
        Formats a line of the message box.
        
        Parameters:
            - s (str): the string the goes to the line
            - line_width (opt, int): the char width of the line
            
        Returns:
            - the formatted line (str)
        """
        line_width = line_width or self.line_width
        a = "    @{:^" + str(line_width) + "}@  "
        return a.format(s)
    
    def referwet(self, n):
        return self._line("+ Refer to WET #{} +".format(n))
    
    def generate_wet(
            self,
            title='',
            msg='',
            wet_num=0,
            text_wrap_width=0,
            ):
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
        text_wrap_width = text_wrap_width or self.text_wrap_width
        
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
                self._title(msg_title=t),
                self._line(),
                "\n".join(map(
                    self._line,
                    textwrap.wrap(msg, width=text_wrap_width))),
                self._line(),
                self.referwet(wet_num),
                self._line(s="please visit"),
                self._line(s=self.web_link),
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
            - choice (str): ['A', 'C']. Defaults to 'Z'
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
        """Exists with a message.
        
        Parameters:
            - m (str): message. default to self.abort_msg()
        """
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
    
    def print_wet_handlers(wet):
        wet.print_wet()
        if not wet.gen:
            print(wet.end_well())
            print(wet.abort_msg())
    
    # a series of very simple tests
    
    wet1 = WetHandler(
        msg_title='c00l',
        msg='Does everything looks good?',
        wet_num=999)
    
    wet2 = WetHandler()
    
    super_message = \
"""
this is a supermessage
of multiline
without any restrictions on size and whatever it does not matter just going very big in the same line for the sake of testing.
"""
    
    wet3 = WetHandler(
        msg_title='Super Mega hyper c00l',
        msg=super_message,
        wet_num=9999999999)
    
    wet4 = WetHandler(gen=False)
    
    print_wet_handlers(wet1)
    print_wet_handlers(wet2)
    print_wet_handlers(wet3)
    print_wet_handlers(wet4)
    
    wet1.continue_abort(choice='C')
    print('continuing automatically...')
    wet1.continue_abort()
    print('continuing mannually...')
    print('going to abort...')
    wet1.continue_abort(choice='A')
