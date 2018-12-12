# -*- coding: utf-8 -*-
"""
INFORMATIVE MESSAGES FOR FARSEER-NMR INSTALLATION AND UPDATE.

Copyright © 2017-2019 Farseer-NMR Project

Find us at:

- J. BioMol NMR Publication:
    https://link.springer.com/article/10.1007/s10858-018-0182-5

- GitHub: https://github.com/Farseer-NMR

- Mail list: https://groups.google.com/forum/#!forum/farseer-nmr
    email: farseer-nmr@googlegroups.com

- Research Gate: https://goo.gl/z8dPJU

- Twitter: https://twitter.com/farseer_nmr

THIS FILE IS PART OF THE FARSEER-NMR PROJECT.

Contributors to this file:
- João M.C. Teixeira (https://github.com/joaomcteixeira)

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

install_wiki = "https://github.com/Farseer-NMR/FarSeer-NMR/wiki/Download,-Install-and-Update"
windows_wiki = "https://github.com/Farseer-NMR/FarSeer-NMR/wiki/Documentation#running-on-windows"
maillist_mail = "farseer-nmr@googlegroups.com"

# configure textwrapper

tw = textwrap.TextWrapper()
tw.fix_sentence_endings = False
tw.break_long_words = False
tw.drop_whitespace = True
tw.initial_indent = "* "
tw.subsequent_indent = "* "
tw.width=70


def _formats_message_body(s):
    """
    s is a string
    """
    
    body = '\n*\n'.join(
        [tw.fill(line) for line in s.splitlines() if line.strip() != '']
        )
    
    return body+"\n"


def _formats_main_title(s):
    
    star = 72*'*'
    title = "*** {: ^64} ***".format(s.upper())
    return "{}\n{}\n{}\n".format(star, title, star)


def _formats_short_title(s):
    """
    s is a string
    """
    s = " {} ".format(s.upper())
    return "{:*^72}\n".format(s)

# GENERAL

query = "-> provide a valid option: "

big_query = """
- [Press ENTER to continue]
- Type any '{}' to abort
""".format(", ".join(system.deny))

gen_files_msg_head = \
    _formats_main_title("Generated Farseer-NMR executable files")

gen_files_msg_tail = _formats_message_body("""
Three executable files were generated inside the Farseer-NMR installation folder:
{} <- runs GUI interface (recommended)
{} <- runs command line (advanced)
{} <- updates Farseer-NMR
""".format(
        os.path.join('bin', system.gui_file),
        os.path.join('bin', system.cmd_file),
        os.path.join('bin', system.update_file)
        )
    )

_windows_advice = \
"""
Farseer-NMR is EXPECTED to work on Windows machines tough, support for Windows is limited.

You are advised to read the additional instructions on HOW TO run Farseer-NMR on windows before proceeding,

please visit:
"""

windows_additional_support = (
    _formats_short_title("WINDOWS USERS") +
    _formats_message_body(_windows_advice) +
    "* {}\n".format(windows_wiki) +
    _formats_message_body("Thank you :-)") +
    72*'*'+"\n"
    )

_install_perfect = \
"""
Farseer-NMR installation COMPLETED successfully
Press ENTER to finish
"""

install_completed = (
    _formats_main_title("perfect") +
    _formats_message_body(_install_perfect)
    )

# INSTALLATION

start_install = _formats_message_body("Starting Installation of Farseer-NMR")

install_header = (
    _formats_short_title("The required Python libraries must be installed") +
    _formats_message_body("Choose an installation option")
    )

install_options_full = """
[1] Automatically configure Python dependencies and executables (recommended)
[2] I want to manually configure Python dependencies and executables (advanced)
[3] Abort Installation
[4] Show help
"""

# MINICONDA INSTALL

_auto_install_message = """
Miniconda (https://www.anaconda.com/) along with the Farseer-NMR Python dependencies will be installed in the Farseer-NMR folder where the install_farseernmr.py file resides.

{}

This Miniconda installation will serve ONLY Farseer-NMR, not interfeering with your system's Python installation.

Miniconda will be installed in SILENT mode, without additional queries to the user. If you continue, you accept Anaconda License and Terms and Conditions.

You can READ Anaconda Terms and Conditions in the link bellow:

https://anaconda.org/about/legal/terms

If you do NOT agree type 'exit', 'no', or 'abort' to abort installation.

You can, instead, choose to install the required Python libraries manually and independently of the Anaconda distribution, just restart the installation process and choose install option [2].

If you AGREE with Anaconda Terms just press ENTER to continue the installation.

""".format(system.installation_folder)

install_miniconda_terms_and_conditions = (
    _formats_short_title("NOTICE") +
    _formats_message_body(_auto_install_message)
    )

install_miniconda_proceed = _formats_message_body(
    "A dedicated Miniconda distribution for Farseer-NMR will be installed"
    )

_query_miniconda_reinstall = """
A Miniconda installation already exists in the Farseer-NMR folder.
Do you want to reinstall Miniconda for Farseer-NMR?

If YES, the current Miniconda will be DELETED and a NEW one installed.
If NO, the installation will abort.

[YES/no]: 
"""

query_miniconda_reinstall = (
    _formats_short_title("QUERY") +
    _formats_message_body(_query_miniconda_reinstall)
    )

reinstall_canceled = """
* You chose not to reinstall Miniconda.
* Installation CANCELED
"""

envs_okay = "* OK * The Farseer-NMR Anaconda Environment installed SUCCESSFULLY"

# MANUAL INSTALL

_manual_install = \
"""
You chose to configure Farseer-NMR installation manually, no Python libraries will be installed now.

We assume that you are a proficient Python user and you can and want to READ, UNDERSTAND and INSTALL the required dependencies on your own.

You can check the required Python libraries in the '.yml' env file inside the 'install' folder. Use this file to create your own Anaconda environment if you use Anaconda or as a guide to know which are the Python dependencies of Farseer-NMR.

The installer will now generate TEMPLATE executable files. You may WISH or NEED to MODIFY the Farseer-NMR executable files according to your system's and Python preferences.

If you don't install the required Python libraries and don't correctly configure the executable files, Farseer-NMR MIGHT NOT WORK.
"""

manual_install = (
    _formats_short_title("notice") +
    _formats_message_body(_manual_install)
    )

# UPDATER

_update_perfect = \
"""
Farseer-NMR update COMPLETED successfully
Press ENTER to finish
"""

update_completed = (
    _formats_main_title("perfect") +
    _formats_message_body(_update_perfect)
    )

# HELP MESSAGES

_add_help = \
"""
For additional help, please:
- contact us via mailing list ({}) providing the .log file  created during the installation/update process.

- or check out our installation wiki page:
""".format(maillist_mail)

additional_help = (
    _formats_short_title("help") +
    _formats_message_body(_add_help) +
    "* {}\n".format(install_wiki) +
    72*'*'+"\n"
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
* ERROR * The Farseer-NMR Anaconda Environment COULD NOT be installed.
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
""".format(maillist_mail)

abort = """
*** Aborting installation ***
"""

# http://patorjk.com/software/taag/#p=display&h=1&f=Doom&t=---------%0AFarSeer-NMR%0Av1.3.0%0A---------
banner = \
"""
                                                                            
                                                                            
 ______  ______  ______  ______  ______  ______  ______  ______  ______     
|______||______||______||______||______||______||______||______||______|    
                                                                            
                                                                            
                                                                            
                                                                            
______           _____                            _   _ ___  _________      
|  ___|         /  ___|                          | \ | ||  \/  || ___ \     
| |_  __ _  _ __\ `--.   ___   ___  _ __  ______ |  \| || .  . || |_/ /     
|  _|/ _` || '__|`--. \ / _ \ / _ \| '__||______|| . ` || |\/| ||    /      
| | | (_| || |  /\__/ /|  __/|  __/| |           | |\  || |  | || |\ \      
\_|  \__,_||_|  \____/  \___| \___||_|           \_| \_/\_|  |_/\_| \_|     
                                                                            
                                                                            
        __      _____   _____                                               
       /  |    |____ | |  _  |                                              
__   __`| |        / / | |/' |                                              
\ \ / / | |        \ \ |  /| |                                              
 \ V / _| |_ _ .___/ /_\ |_/ /                                              
  \_/  \___/(_)\____/(_)\___/                                               
                                                                            
                                                                            
                                                                            
                                                                            
 ______  ______  ______  ______  ______  ______  ______  ______  ______     
|______||______||______||______||______||______||______||______||______|    
                                                                            
                                                                            
                                                                            
                                                                            
"""

if __name__ == "__main__":
    print(query)
    print(big_query)
    print(gen_files_msg_head)
    print(gen_files_msg_tail)
    print(windows_additional_support)
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
    print(update_completed)
    print(additional_help)
    print(not_enough_space)
    print(unknown_python)
    print(url_error)
    print(url_unknown)
    print(fs_env_failed)
    print(abort)
    print(banner)
