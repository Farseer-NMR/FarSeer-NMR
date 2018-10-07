# official formats
from core.fslibs.parsing_routines.ansig import parse_ansig_peaklist as ansig
from core.fslibs.parsing_routines.ccpnmrv2 import parse_ccpnmrv2_peaklist as ccpnmrv2
from core.fslibs.parsing_routines.nmrdraw import parse_nmrdraw_peaklist as nmrdraw
from core.fslibs.parsing_routines.nmrview import parse_nmrview_peaklist as nmrview
from core.fslibs.parsing_routines.sparky import parse_sparky_peaklist as sparky
# user defined formats
from core.fslibs.parsing_routines.user_defined_1 import parse_user_peaklist_1 as user_pkl_1
from core.fslibs.parsing_routines.user_defined_2 import parse_user_peaklist_2 as user_pkl_2
from core.fslibs.parsing_routines.user_defined_3 import parse_user_peaklist_3 as user_pkl_3
from core.fslibs.parsing_routines.user_defined_4 import parse_user_peaklist_4 as user_pkl_4
from core.fslibs.parsing_routines.user_defined_5 import parse_user_peaklist_5 as user_pkl_5
#from core.fslibs.parsing_routines.YOUR_FILE import parse_YOUR_FORMAT_peaklist as YOUR_FORMAT
