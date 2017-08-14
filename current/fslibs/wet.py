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
""".format(title(t),
           line(),
           "\n".join(map(format_msg, textwrap.wrap(s, width=67))),
           line(),
           referwet(n),
           bottom())
    return ws

def continue_abort():
    """ Asks user to decide behaviour. """
    choice = 'z'
    while not(choice in ['A', 'C']):
        choice = \
            input('> What do you want to do? [C]ontinue or [A]bort? ').upper()
    
    if choice == 'A':
        end_bad()
    elif choice == 'C':
        return 'Continuing...'

def wet3():
    strwet = """
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
""".format(title(' NOTE '),
           line(),
           line('All potting flags are turned off.'),
           line('No plots will be drawn'),
           line('Check if this is the desired configuration.'),
           line(),
           line('Farseer exported all the calculated'),
           line('parameters so that you can use your'),
           line('own external plotting tool.'),
           line(),
           referwet(3),
           title())
    return strwet

def wet4(xvalues, items):
    
    strwet = """
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
""".format(title(' ERROR '),
           line(),
           line('Values set for fitting (fitting_x_values variable)'),
           line('do not match those referenced for <cond1> data point names'),
           line(),
           line('list of user defined x values for <cond1> variables'),
           line(", ".join(map(str, xvalues))),
           line(),
           line('<cond1> data points names'),
           line(", ".join([str(int(x)) for x in items])),
           line(),
           line('lists differ in values:'),
           line(", ".join(sorted(set([str(int(x)) for x in items]).\
                                 symmetric_difference(set(map(str, xvalues))))
                                 )),
           line(),
           referwet(4),
           line(),
           title()
          )
    
    return strwet

def wet5(values, pkls):
    strwet = """
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
""".format(title(' ERROR '),
           line('Coordinate values defined for fitting/data respresentation'),
           line('(fitting_x_values variable).'),
           line(str(values)),
           line(),
           line('do not match the number of <cond1> data points,'),
           line('a.k.a, input peaklists.'),
           line(str(list(pkls))),
           line(),
           line('Please correct fitting_x_values variable or'),
           line('confirm you have not forgot to input any peaklist'),
           line(),
           referwet(5),
           title())
           
    return strwet

def wet6(values):
    strwet = """
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
""".format(title(' WARNING '),
           line(),
           line('There are values in titration_x_values'),
           line('which are negative'),
           line(),
           line(str(values)),
           line(),
           line('This is not expected considering fitting data with'),
           line('the Hill equation.'),
           line('Please revisit your input'),
           line(),
           referwet(6),
           title())
    return strwet

def wet7(values):
    strwet = """
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
{}
""".format(title(' NOTE '),
           line(),
           line('Farseer could not confirm agreement between input'),
           line('fitting x values and the .csv files'),
           line('tough, both lists have the same length'),
           line(),
           line('These are the values defined for fitting'),
           line(str(values)),
           line(),
           line('If the fitting does not perform correctly,'),
           line('check the input values/spectra'),
           line(),
           referwet(7),
           title())
    return strwet

def wet8(f, s):
    ss = """
{}
{}
{}
{}
{}
{}
{}

{}
{}
{}
{}
{}
""".format(title(' ERROR '),
           line(),
           line('The no. of files of type {}'.format(f)),
           line('is not the same for every titration folder.'),
           line('Below a table with the files input.'),
           line('Check for the missing ones!'),
           line(),
           s,
           line(),
           line(),
           referwet(8),
           title())
    return ss

def wet9(f):
    strwet = """
{}
{}
{}
{}
{}
""".format(title(' ERROR '),
           line('There are no files in spectra/ with extension {}'.format(f)),
           line(),
           referwet(9),
           title())
    return strwet

def end_bad():
    sys.exit("""
{}
{}
{}
{}
""".format(bottom(), 
             line('Farseer-NMR aborted'),
             line('Bye :-('),
             bottom()))
    return

def end_good():
    print("""
{}
{}
{}
{}
""".format(title(), 
             line('Farseer-NMR completed correctly'),
             line('Bye :-)'),
             title()))
    return
