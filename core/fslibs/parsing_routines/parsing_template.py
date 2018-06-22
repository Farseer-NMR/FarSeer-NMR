"""
YOUR DESCRIPTION HERE

To add your parsing routine, you sould:

1) code your funcion in this file
2) add a import statment in the __init__.py file according to the
    given examples.
3) code the identification snipet in core.fslibs.parsing.get_peaklist_format()
    Add, if necessary, a file extention to the list:
        core.fslibs.parsing.file_extensions
4) if your peaklist requires a FASTA file to read residue types, add your
    peaklist format code (defined in 3) in the list:
        core.fslibs.setup_farseer_calculation.peaklist_format_requires_fasta
"""
from core.fslibs.Peak import Peak

def parse_user_peaklist_NUM(peaklist_file):
    """
    Parses YOUR FORMAT peaklist.
    
    According to the format:
    
        * paste an example of your format here*
    
    Parameters:
        - peaklist_file (str): path to peaklist
    
    Returns:
        peakList (list): a list of Peak objects.
    """
    peakList = []
    return peakList
