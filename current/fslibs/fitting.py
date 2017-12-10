import scipy.optimize as sciopt
import numpy as np

# FITTING EQUATIONS:
def hill_equation(L0, Vmax, n, kd):
            """
            The Hill Equation.
            
            https://en.wikipedia.org/wiki/Hill_equation_(biochemistry)
            
            http://www.physiologyweb.com/calculators/hill_equation_interactive_graph.html
            """
            return (Vmax*L0**n)/(kd**n+L0**n)

# FITTING LOG FILES HEAD:

def fit_log_head(fit, col):
    if fit == 'hill':
        s2w = \
"""# fitting for parameter: '{}'
#fit performed: Hill Equation
#(Vmax*[S]**n)/(K0.5**n+[S]**n)
""".format(col)
        return s2w

# FITTING RESULTS FILE HEAD

def fit_results_head(fit):
    if fit == 'hill':
        return "#res,fit,ymax,yhalf,kd,n\n"
        

# FITTING LOG FILE OKAY TEXT:

def hill_log_okay(res, x, y, popt, pcov):
    s2w = \
"""
Res:  {}
xdata: {}
ydata: {}
ymax: {}
K0.5: {}
n: {}
popt: {}
pcov: {}
**************************
""".format(res,list(x),list(y),popt[0],popt[2], popt[1], popt, pcov)
    
    return s2w

# FITTING RESULTS TEXT:

def hill_results(res,popt,yhalf,status='okay'):
    if status == 'okay':
        return "{},{},{},{},{},{}\n".format(res,status,popt[0],
                                          yhalf,popt[2],popt[1])
    elif status == 'failed':
        return "{},{},,,,,".format(res,status)



# FITTING TEXT TO GO IN PLOT:

def hill_txt_plot():
    s2w = \
"""
ymax: {}
yhalf: {}
K0.5: {}
n: {}
""".format(popt[0],yhalf,popt[2],popt[1])
    return s2w

# FITTING LOG FILE FAILED:

def fit_failed(res, x, y):
    s2w = \
"""
Res#:  {}
xdata: {}
ydata: {}
!¡FIT FAILED TO FIND MINIMIZATION!¡
**************************
""".format(res, list(x), list(y))
    return s2w


# FITTING WORKFLOWS:

def fitting_hill(x, y, res):
    """Workflow for fitting data with the Hill Equation."""
    
    p_guess = [np.max(y), 1, np.median(x)]
    
    try:
        popt, pcov = sciopt.curve_fit(hill_equation, x, y, p0=p_guess)
        
        yhalf = popt[0]/2
        
        print("*** Fit residue {} - OK!".format(res))
        
        a = hill_log_okay(res, x, y, popt, pcov)
        b = hill_results(res, popt, yhalf)
        c = hill_txt_plot
    
    except:
        print("*** Fit residue {} - Failed!".format(res))
        a = fit_failed(res, x, y)
        b = hill_results(res, popt, yhalf, status='failed')
        c = "fit failed"
    
    return a, b, c
