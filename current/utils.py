#import farseer_user_variables as fsuv

#def write_title(title, onlytitle=False):
    #'''
    #:param onlytitle: False to identify is is only to generate title
                      #or to print to log
    #'''

    #str2write = '\n\n\n{}\n{:^80}\n{}\n'.format(titlesperator,
                                                #title, titlesperator)

    #if onlytitle:
        #return str2write

    #else:
        #write_log(str2write)

#def write_log(str2write, mod='a', logfile_name = fsuv.logfile_name):
    #"""
    #str, str -> None

    #:param logfilename: the string with the name of the output log file
    #:param towrite: the string to write in the log file
    #:return: None
    #"""
    #with open(logfile_name, mod) as logfile:
        #logfile.write(str2write)

    #print(str2write)


#def dim_sperator(item2write, layer):
    #layer_dict = {'top': 10,
                  #'midle': 6,
                  #'own': 2}
    #if layer=='own':
        #return '{0}> {1}'.format('='*layer_dict[layer], item2write) 
    #else:
        #return '{0}> {1} <{0}\n'.format('='*layer_dict[layer], item2write) 


#def hex_to_RGB(hex):
    #''' http://bsou.io/posts/color-gradients-with-python
    #"#FFFFFF" -> [255,255,255] '''
    ## Pass 16 to the integer function for change of base
    #return [int(hex[i:i+2], 16) for i in range(1,6,2)]


#def RGB_to_hex(RGB):
    #''' http://bsou.io/posts/color-gradients-with-python
    #[255,255,255] -> "#FFFFFF" '''
    ## Components need to be integers for hex to make sense
    #RGB = [int(x) for x in RGB]
    #return "#"+"".join(["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in RGB])

#def color_dict(gradient):
    #''' http://bsou.io/posts/color-gradients-with-python
    #Takes in a list of RGB sub-lists and returns dictionary of
    #colors in RGB and hex form for use in a graphing function
    #defined later on '''
    #return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
        #"r":[RGB[0] for RGB in gradient],
        #"g":[RGB[1] for RGB in gradient],
        #"b":[RGB[2] for RGB in gradient]}


#def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    #''' http://bsou.io/posts/color-gradients-with-python
    #returns a gradient list of (n) colors between
    #two hex colors. start_hex and finish_hex
    #should be the full six-digit color string,
    #inlcuding the number sign ("#FFFFFF") '''
    ## Starting and ending colors in RGB form
    #s = hex_to_RGB(start_hex)
    #f = hex_to_RGB(finish_hex)
    ## Initilize a list of the output colors with the starting color
    #RGB_list = [s]
    ## Calcuate a color at each evenly spaced value of t from 1 to n
    #for t in range(1, n):
        ## Interpolate RGB vector for color at the current value of t
        #curr_vector = [
            #int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
            #for j in range(3)
        #]
        ## Add it to our list of output colors
        #RGB_list.append(curr_vector)
    #return color_dict(RGB_list)





#titlesperator = '*'*80


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

def combine_dicts(dictionaries):
    tmp_dict = {}
    for dictionary in dictionaries:
        tmp_dict.update(dictionary)
    return tmp_dict

def exp_set_is_valid(variables):
    if not variables["experimental_dataset"]:
        return False
    else:
        if variables["conditions"]["z"] in list(variables["experimental_dataset"].keys()):
            if all(variables["conditions"]["y"] in list(variables["experimental_dataset"][z].keys()) for z in variables["conditions"]["z"]):
                if all(variables["conditions"]["x"] in list(variables["experimental_dataset"][z][y].keys()) for z in variables["conditions"]["y"]):
                    return True
