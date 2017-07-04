import sys

def title(s=''):
    return "{:@^62}".format(s)

def line(s=''):
    return "@{:^60}@".format(s)

def referwet(n):
    return line("+ Refer to WET #{} +".format(n))

def wet1(pre_flag, c3_flag, plot_h_flag, plot_v_flag, comp_flag):

    input("""
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
           line(""),
           line('PRE Analaysis is set to <{}>'.format(pre_flag)),
           line('and it depends on the following variables:'),
           line(),
           line('do_cond3 :: {}'.format(c3_flag)),
           line('plots_Height_ratio :: {}'.format(plot_h_flag)),
           line('plots_Volume_ratio :: {}'.format(plot_v_flag)),
           line('perform_comparisons :: {}'.format(comp_flag)),
           line(),
           referwet(1),
           title()))
    
    return

def wet2(cond1, cond2, cond3):
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
""".format(title(' WARNING '),
           line(),
           line('All possible Farseer data analysis routines'),
           line('are set to <False>'),
           line('in the farseer_user_variables file:'),
           line(),
           line('condition 1 :: <{}>'.format(cond1)),
           line('condition 2 :: <{}>'.format(cond2)),
           line('condition 3 :: <{}>'.format(cond3)),
           line(),
           line('There is nothing to calculate or plot.'),
           line('Confirm that this is actually what you want'),
           line(),
           referwet(2),
           line(),
           line('Parsed Peaklists have been exported.'),
           title())
    
    return strwet

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
""".format(title(' WARNING '),
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

def wet5():
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
""".format(title(' ERROR '),
           line('X Axis values set for fitting (fitting_x_values variable)'),
           line('do not match the number of <cond1> data points'),
           line(),
           line('Names of .csv files could not be converted to int values.'),
           line(),
           line('Please correct fitting_x_values variable or'),
           line('the number of input peaklists'),
           line(),
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
""".format(title(' WARNING '),
           line(),
           line('There are values in titration_x_values'),
           line('which are negative'),
           line(),
           line(str(values)),
           line(),
           line('Confirm that is according your preferences'),
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

def end_bad():
    sys.exit("""
{}
{}
{}
{}
""".format(title(), 
             line('Farseer-NMR aborted'),
             line('Bye :-('),
             title()))
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
