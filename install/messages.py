"""
Informative messages for the installation and update processes.

2017-2019 Farseer-NMR Project.

THIS FILE WAS ADAPTED FROM TREE-OF-LIFE PROJECT (version 1.0.1 - LGPLv3)
AND MODIFIED ACCORDINGLY TO THE NEEDS OF THE FARSEER-NMR PROJECT.

Visit the original Tree-of-Life project at:

https://github.com/joaomcteixeira/Tree-of-Life

Find Farseer-NMR project at:
- J. BioMol NMR Publication:
    https://link.springer.com/article/10.1007/s10858-018-0182-5

- GitHub: https://github.com/Farseer-NMR

- Mail list: https://groups.google.com/forum/#!forum/farseer-nmr
    email: farseer-nmr@googlegroups.com

- Research Gate: https://goo.gl/z8dPJU

- Twitter: https://twitter.com/farseer_nmr

THIS FILE IS PART OF THE FARSEER-NMR PROJECT.

Contributors to this file:
- Joao M.C. Teixeira (https://github.com/joaomcteixeira)

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
import os
import textwrap

from install import system
from install import executables

# provide a link and e-mail with further documentation on the install process
install_wiki = "https://github.com/Farseer-NMR/FarSeer-NMR/wiki"
mailist = "farseer-nmr@googlegroups.com"

# configure textwrapper

tw = textwrap.TextWrapper()
tw.fix_sentence_endings = False
tw.break_long_words = False
tw.drop_whitespace = True
tw.initial_indent = "* "
tw.subsequent_indent = "* "
tw.width = 70


def _formats_message_body(s):
    """
    s is a string
    """
    
    body = '\n*\n'.join(
        [tw.fill(line) for line in s.splitlines() if line.strip() != '']
        )
    
    return body + "\n"


def _formats_main_title(s):
    
    star = 72 * '*'
    title = "*** {: ^64} ***".format(s.upper())
    return "{}\n{}\n{}\n".format(star, title, star)


def _formats_short_title(s):
    """
    s is a string
    """
    s = " {} ".format(s.upper())
    return "{:*^72}\n".format(s)


# GENERAL MESSAGES
query = "-> provide a valid option: "

big_query = """
- [Press ENTER to continue]
- Type any '{}' to abort
""".format(", ".join(system.deny))

gen_files_msg_head = _formats_main_title("Generated executable files")


list_of_files = ""
for file_ in executables.executable_files.keys():
    list_of_files += "-> {}\n".format(os.path.join('bin', file_))

gen_files_msg_tail = _formats_message_body(
    "Executable files were generated inside the installation folder:\n"
    + list_of_files
    )

# SUCCESS MESSAGES

_install_perfect = """
The software installation COMPLETED successfully
"""

install_completed = (
    _formats_main_title("perfect")
    + _formats_message_body(_install_perfect)
    )

# INSTALLATION

start_install = _formats_message_body("Starting installation...")

install_header = (
    _formats_short_title("The required Python libraries must be installed")
    + _formats_message_body("Choose an installation option")
    )

install_options_full = """
[1] Automatically configure Python dependencies and executables (recommended)
[2] I want to manually configure Python dependencies and executables (advanced)
[3] Abort Installation
[4] Show help
"""

# MINICONDA INSTALL

_auto_install_message = (
    "Miniconda (https://www.anaconda.com/) along with the "
    "Python dependencies will be installed in the following folder:\n"
    "{}\n"
    "This Miniconda installation will serve ONLY this folder "
    "not interfeering with your system's Python installation.\n"
    "\n"
    "Miniconda will be installed in SILENT mode, "
    "without additional queries to the user. If you continue, "
    "you accept Anaconda License and Terms and Conditions."
    "\n"
    "You can READ Anaconda Terms and Conditions in the link bellow:\n"
    "\n"
    "https://anaconda.org/about/legal/terms\n"
    "\n"
    "If you do NOT agree type 'exit', 'no', or 'abort' to abort installation. "
    "You can, instead, choose to install the required Python libraries "
    "manually and independently of the Anaconda distribution, "
    "just restart the installation process and choose install option [2].\n"
    "If you AGREE with Anaconda Terms just press ENTER to continue "
    "the installation.\n"
    )

install_miniconda_terms_and_conditions = (
    _formats_short_title("NOTICE")
    + _formats_message_body(_auto_install_message)
    )

install_miniconda_proceed = _formats_message_body(
    "A dedicated Miniconda distribution will be installed"
    )

_query_miniconda_reinstall = """
A Miniconda installation already exists in this folder.
Do you want to reinstall Miniconda"?

If YES, the current Miniconda will be DELETED and a NEW one installed.
If NO, the installation will abort.

[YES/no]:
"""

query_miniconda_reinstall = (
    _formats_short_title("QUERY")
    + _formats_message_body(_query_miniconda_reinstall)
    )

reinstall_canceled = """
* You chose not to reinstall Miniconda.
* Installation CANCELED
"""

envs_okay = "* OK * The Anaconda Environment installed SUCCESSFULLY"

# MANUAL INSTALL

_manual_install = (
    "You chose to configure {} manually, ".format(system.software_name)
    + "no Python libraries will be installed now.\n"
    "\n"
    "We assume that you are a proficient Python user and "
    "you can and want to READ, UNDERSTAND and INSTALL the "
    "required dependencies on your own.\n"
    "\n"
    "You can check the required Python libraries in the '.yml' env file "
    "inside the 'install' folder. Use this file to create your own "
    "Anaconda environment if you use Anaconda or as a guide to know "
    "which are the Python dependencies for {}.\n".format(system.software_name)
    + "\n"
    "The installer will now generate TEMPLATE executable files. You may "
    "WISH or NEED to MODIFY {}'s".format(system.software_name)
    + " executable files according to "
    "your system's and Python preferences.\n"
    "If you don't install the required Python libraries and don't correctly "
    "configure the executable files, "
    "{} MIGHT NOT WORK.".format(system.software_name)
    )

manual_install = (
    _formats_short_title("notice")
    + _formats_message_body(_manual_install)
    )

# UPDATER

update_var_missing = (
    _formats_short_title("error")
    + _formats_message_body(
        "An installation variable necessary for UPDATING"
        " is missing or broken in installation_vars.py"
        )
    )

update_continues = """
* Despite the ERRORS the update will continue
"""

consider_reinstall = (
    _formats_short_title("notice")
    + _formats_message_body(
        "Something went wrong during the updating process. "
        "The easiest method to solve this issue is to reinstall "
        "the software."
        )
    )

_update_perfect = """
{} update COMPLETED successfully
Press ENTER to finish
""".format(system.software_name)

update_completed = (
    _formats_main_title("perfect")
    + _formats_message_body(_update_perfect)
    )

# HELP MESSAGES

_add_help = (
    "For additional help, please:\n"
    "- contact us via mailing list ({}) ".format(mailist)
    + "providing the .log file "
    "created during the installation/update process.\n"
    "- or check out our installation wiki page:\n"
    "{}".format(install_wiki)
    )

additional_help = (
    _formats_short_title("help")
    + _formats_message_body(_add_help)
    + 72 * '*'
    + "\n"
    )

# ERRORS

not_enough_space = """
* Not enought space available to install the required Miniconda packages.
* At lest {} GB are necessary.
""".format(system.min_space_allowed)

unknown_python = """
* ERROR * We detected a Python version that is not 2 nor 3.
"""

url_error = """
* ERROR * Could not reach the Miniconda URL
* ERROR * {}
"""

url_unknown = """
* ERROR * URL not found
* ERROR * {}
"""

fs_env_failed = """
* ERROR * The Anaconda Environment COULD NOT be installed.
* ERROR * Check the following error mensage:

{}
"""

path_with_spaces = """
* ERROR * the installation path '{}'
* ERROR * contains spaces. This is NOT allowed!
* ERROR * Please choose another folder
* ERROR * or rename this one.
"""

something_wrong = """
* ERROR * Something went wrong and we could not identify it
* ERROR * Please contact us via {}
* ERROR * and provide the log file created during the process
* ERROR * so that we can help you solve this problem
* ERROR * Thank you!
""".format(mailist)

abort = """
*** Aborting installation ***
"""

terminate = "Press ENTER to TERMINATE"

# http://patorjk.com/software/taag/#p=display&h=1&f=Doom&t=---------%0AFarseer-NMR%0Av1.3.3%0A---------
banner = r"""
                                                                        
                                                                        
 ______  ______  ______  ______  ______  ______  ______  ______  ______ 
|______||______||______||______||______||______||______||______||______|
                                                                        
                                                                        
                                                                        
                                                                        
______           _____                            _   _ ___  _________  
|  ___|         /  ___|                          | \ | ||  \/  || ___ \ 
| |_  __ _  _ __\ `--.   ___   ___  _ __  ______ |  \| || .  . || |_/ / 
|  _|/ _` || '__|`--. \ / _ \ / _ \| '__||______|| . ` || |\/| ||    /  
| | | (_| || |  /\__/ /|  __/|  __/| |           | |\  || |  | || |\ \  
\_|  \__,_||_|  \____/  \___| \___||_|           \_| \_/\_|  |_/\_| \_| 
                                                                        
                                                                        
        __      _____    _____                                          
       /  |    |____ |  |  ___|                                         
__   __`| |        / /  |___ \                                          
\ \ / / | |        \ \      \ \                                         
 \ V / _| |_ _ .___/ /_ /\__/ /                                         
  \_/  \___/(_)\____/(_)\____/                                          
                                                                        
                                                                        
                                                                        
                                                                        
 ______  ______  ______  ______  ______  ______  ______  ______  ______ 
|______||______||______||______||______||______||______||______||______|
                                                                        
                                                                        
                                                                        
                                                                        
"""

if __name__ == "__main__":
    print(query)
    print(big_query)
    print(gen_files_msg_head)
    print(gen_files_msg_tail)
    print(install_completed)
    print(start_install)
    print(install_header)
    print(install_options_full)
    print(install_miniconda_terms_and_conditions)
    print(install_miniconda_proceed)
    print(query_miniconda_reinstall)
    print(reinstall_canceled)
    print(envs_okay)
    print(manual_install)
    print(update_var_missing)
    print(update_completed)
    print(update_continues)
    print(consider_reinstall)
    print(additional_help)
    print(not_enough_space)
    print(unknown_python)
    print(url_error)
    print(url_unknown)
    print(fs_env_failed)
    print(abort)
    print(banner)
