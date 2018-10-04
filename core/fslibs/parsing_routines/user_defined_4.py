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
from core.utils import aal1tol3

def parse_user_peaklist_4(peaklist_file):
    """
    Parses YOUR FORMAT peaklist.
    
    According to the format:
    
      Assignment         w1         w2     w1 (Hz)    w2 (Hz)  Data Height 

            M1N-H    119.667      8.365    7280.78    5022.12     48464896 
            A2N-H    125.482      8.439    7634.58    5066.55     45516156 
            R3N-H    118.707      8.101    7222.37    4863.62     55723680 
            D4N-H    121.903      8.116    7416.82    4872.63     46697320 
            K6N-H    123.208      9.104    7496.22    5465.80     21862474 
    
    Parameters:
        - peaklist_file (str): path to peaklist
    
    Returns:
        peakList (list): a list of Peak objects.
    """
    fin = open(peaklist_file, 'r')
    peakList = []
    
    # reads header line
    fin.readline()
    # reads blank line between header and peak information
    fin.readline()
    
    counter = 0
    
    for line in fin:
        
        if not line:
            continue
        
        counter += 1
        ls = line.strip().split()
        
        peakList.append(Peak(
            peak_number=counter,
            positions=[ls[2],ls[1]],
            atoms=["H","N"],
            residue_type=aal1tol3[ls[0][0]],
            residue_number=ls[0][1:-3],
            linewidths=[ls[4], ls[3]],
            height=ls[-1],
            volume=0,
            format_='user_pkl_4',
            fit_method=None,
            merit=None,
            volume_method=None,
            details=None
            ))
    
    fin.close()
    return peakList

if __name__ == "__main__":
    import sys
    
    parse_user_peaklist_4(sys.argv[1])
