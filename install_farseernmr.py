"""
Farseer-NMR installer.

Copyright © 2017-2019 Farseer-NMR Project

THIS FILE WAS ADAPTED FROM TREE-OF-LIFE PROJECT (version 1.0.0 - LGPLv3)
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
import sys
import os
import time  # used to give a more human feeling to the install process

libs_folder = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# appends 'install' folder to allow lib import
sys.path.append(os.path.join(libs_folder, "install"))

from install import system
from install import messages
# logging is required before importing the other package libs
from install import logger

# STARTS LOGGING
logfile_name = os.path.join(
    system.installation_folder,
    system.installation_log_name
    )

if os.path.exists(logfile_name):
    os.remove(logfile_name)

log = logger.InstallLogger(__name__, log_file_name=logfile_name).gen_logger()

# CONFIRMS PYTHON VERSION
python_version = sys.version_info[0]
log.debug("* Python version: {}".format(python_version))

if python_version == 2:
    user_input = raw_input

elif python_version == 3:
    user_input = input

else:
    log.info(messages.unknown_python)
    log.info("* You are running Python version: {}".format(python_version))
    _name = system.software_name
    log.info("* {} requires Python 2.7 or 3.x to execute".format(_name))
    log.info(messages.additional_help)
    log.info(messages.abort)
    user_input(messages.terminate)
    sys.exit(1)

if system.installation_folder.find(" ") > 0:
    log.info(messages.path_with_spaces.format(system.installation_folder))
    log.info(messages.additional_help)
    log.info(messages.abort)
    user_input(messages.terminate)
    sys.exit(1)

# continues importing log dependent libs
from install import commons
from install import condamanager

# STARTS INSTALLATION
log.debug("{} installation initiated".format(system.software_name))
log.debug("<installation_folder>: {}".format(system.installation_folder))
log.info(messages.banner)
log.info(messages.start_install)
time.sleep(0.5)

log.info(messages.install_header)
log.info(messages.install_options_full)

# Queries installation option
install_choice = None
while install_choice not in ("1", "2", "3"):
    install_choice = user_input(messages.query).strip()
    log.debug("install_choice: {}".format(install_choice))
    if install_choice == "4":
        log.info(messages.additional_help)
        log.info(messages.install_options_full)

log.debug("final install_choice: {}".format(install_choice))
log.info("\n")

time.sleep(0.5)

# Applies choice
if install_choice == "1":  # installs Miniconda and Python Environment
    
    log.debug("entered install option 1")
    
    miniconda_handler = condamanager.CondaManager(
        cwd=system.installation_folder,
        env=system.latest_env_file
        )
    
    # returns name of folder, if found.
    previous_miniconda_folder = \
        miniconda_handler.check_previous_miniconda_folder()
        
    log.debug(
        "<previous_miniconda_folder>: {}".format(previous_miniconda_folder)
        )
    
    if previous_miniconda_folder:
        # Queries user to reinstall Miniconda
        # if approved, the previous Miniconda folder will be removed.
        
        log.debug("found previous miniconda folder")
        
        log.info(messages.query_miniconda_reinstall)
        
        choice = None
        while not(choice in system.approve) and not(choice in system.deny):
            choice = user_input(messages.query).strip().upper()
            log.debug("<choice>: {}".format(choice))
        
        log.debug("Resinstall option chosen: {}".format(choice))
            
        if choice in system.approve:
            log.info(messages.install_miniconda_proceed)
            commons.remove_folders([previous_miniconda_folder])
        
        elif choice in system.deny:
            log.info(messages.reinstall_canceled)
            log.info(messages.additional_help)
            log.info(messages.abort)
            commons.sys_exit()
        
        # expect the unexpected
        else:
            log.info(messages.something_wrong)
            log.info(messages.additional_help)
            log.info(messages.abort)
            commons.sys_exit()
    
    log.info(messages.install_miniconda_proceed)
    
    if not(commons.check_available_disk_space()):
        log.info(messages.not_enough_space)
        log.info(messages.additional_help)
        log.info(messages.abort)
        commons.sys_exit()
    
    # Queries user to agree with Anaconda Terms and Conditions
    mf = os.path.abspath(system.default_miniconda_folder)
    log.info(messages.install_miniconda_terms_and_conditions.format(mf))
    choice = 1
    approve = system.approve + [""]
    
    while choice not in approve and choice not in system.deny:
        choice = user_input(messages.query).strip().upper()
    
    if choice in approve:
        log.info("continuing...")
    
    elif choice in system.deny:
        log.info(messages.additional_help)
        log.info(messages.abort)
        commons.sys_exit()
    
    # Starts Miniconda Installation
    miniconda_handler.download_miniconda()
    miniconda_handler.install_miniconda()
    miniconda_handler.install_env()
    miniconda_handler.logs_env_information()
    
    # registers installation variables
    install_option = 1
    conda_exec = miniconda_handler.get_conda_exec()
    python_exec = miniconda_handler.get_env_python_exec()
    env_file = miniconda_handler.get_env_file()
    env_name = miniconda_handler.get_env_name()
    env_version = miniconda_handler.get_env_version()
    miniconda_folder = miniconda_handler.get_miniconda_install_folder()
    
    # cleans
    miniconda_install_file = miniconda_handler.get_miniconda_install_file()
    os.remove(miniconda_install_file)
    log.debug("removed: {}".format(miniconda_install_file))

elif install_choice == "2":  # Manual Python libs installation
    
    log.info(messages.manual_install)
    choice = user_input(messages.big_query).strip().upper()
    
    if choice in system.deny:
        log.info(messages.additional_help)
        log.info(messages.abort)
        commons.sys_exit()
    
    # registers installation variables
    install_option = 2
    python_exec = sys.executable
    env_file = None
    env_name = None
    env_version = None
    conda_exec = None
    miniconda_folder = None

elif install_choice == "3":
    log.info(messages.additional_help)
    log.info(messages.abort)
    commons.sys_exit()

else:  # expecting the unexpected
    log.info(messages.something_wrong)
    log.info(messages.abort)
    commons.sys_exit()

time.sleep(1)

# creates executable files
commons.create_executables(system.installation_folder, python_exec)

# registers installation variables in a file.py
commons.register_install_vars(
    install_dir=system.installation_folder,
    python_exec=python_exec,
    install_option=install_option,
    conda_exec=conda_exec,
    env_file=env_file,
    env_name=env_name,
    env_version=env_version,
    miniconda_folder=miniconda_folder
    )

log.info(messages.install_completed)
user_input(messages.terminate)
