"""
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
