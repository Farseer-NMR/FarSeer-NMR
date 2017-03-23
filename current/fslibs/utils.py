import farseer_user_variables as fsuv

def write_title(title, onlytitle=False):
    '''
    :param onlytitle: False to identify is is only to generate title
                or to print to log
    '''
    
    str2write = '\n\n\n{}\n{:^80}\n{}\n'.format(titlesperator, title, titlesperator)
    
    if onlytitle:
        return str2write
        
    else:
        write_log(str2write)

def write_log(str2write, mod='a', logfile_name = fsuv.logfile_name):
    """
    str, str -> None

    :param logfilename: the string with the name of the output log file
    :param towrite: the string to write in the log file
    :return: None
    """
    with open(logfile_name, mod) as logfile:
        logfile.write(str2write)

    print(str2write)


def dim_sperator(item2write, layer):
    layer_dict = {'top': 10,
                  'midle': 6,
                  'own': 2}
    if layer=='own':
        return '{0}> {1} '.format('='*layer_dict[layer], item2write) 
    else:
        return '{0}> {1} <{0}\n'.format('='*layer_dict[layer], item2write) 



titlesperator = '*'*80


# variables necessary for the functions
aal3tol1 = {
"Ala": "A",
"Arg": "R",
"Asn": "N",
"Asp": "D",
"Cys": "C",
"Glu": "E",
"Gln": "Q",
"Gly": "G",
"His": "H",
"Ile": "I",
"Leu": "L",
"Lys": "K",
"Met": "M",
"Phe": "F",
"Pro": "P",
"Ser": "S",
"Thr": "T",
"Trp": "W",
"Tyr": "Y",
"Val": "V"}

aal1tol3 = {
"A": "Ala",
"R": "Arg",
"N": "Asn",
"D": "Asp",
"C": "Cys",
"E": "Glu",
"Q": "Gln",
"G": "Gly",
"H": "His",
"I": "Ile",
"L": "Leu",
"K": "Lys",
"M": "Met",
"F": "Phe",
"P": "Pro",
"S": "Ser",
"T": "Thr",
"W": "Trp",
"Y": "Tyr",
"V": "Val"}
