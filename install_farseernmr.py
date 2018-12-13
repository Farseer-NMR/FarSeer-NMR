# -*- coding: utf-8 -*-
"""
FARSEER-NMR INSTALLER.

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
import sys
import os
import time  # used to give a more human feeling to the install process

installation_folder = \
    os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# appends 'install' folder to allow lib import
sys.path.append(os.path.join(installation_folder, "install"))

from install import logger

logfile_name = os.path.join(installation_folder, 'install.log')

if os.path.exists(logfile_name):
    os.remove(logfile_name)

log = logger.InstallLogger(__name__, log_file_name=logfile_name).gen_logger()
log.debug("install_farseernmr.py initiated")
log.debug("<installation_folder>: {}".format(installation_folder))

from install import system
from install import messages
from install import commons
from install import miniconder

python_version = sys.version_info[0]
log.debug("* Python version: {}".format(python_version))

if python_version == 2:
    user_input = raw_input

elif python_version == 3:
    user_input = input

else:
    log.info(messages.unknown_python)
    log.info("* You are running Python version: {}".format(python_version))
    log.info("Farseer-NMR setup.py requires Python 2.7 or 3.x to execute")
    log.info(messages.additional_help)
    log.info(messages.abort)
    commons.sys_exit()

if installation_folder.find(" ") > 0:
    log.info(messages.path_with_spaces.format(installation_folder))
    log.info(messages.additional_help)
    log.info(messages.abort)
    commons.sys_exit()

# STARTS INSTALLATION

log.info(messages.banner)
log.info(messages.start_install)
time.sleep(0.5)

# Queries installation option
log.info(messages.install_header)
log.info(messages.install_options_full)

choice = None
while choice not in ("1", "2", "3"):
    choice = user_input(messages.query)
    log.debug("install_choice: {}".format(choice))
    if choice == "4":
        log.info(messages.additional_help)
        log.info(messages.install_options_full)

log.debug("final install_choice: {}".format(choice))
log.info("\n")
time.sleep(0.5)

# Applies choice
if choice == "1":  # installs Miniconda and Farseer-NMR Environment
    
    log.debug("entered install option 1")
    
    miniconda_handler = miniconder.CondaManager(cwd=installation_folder)
    
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
            choice = user_input(messages.query).upper()
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
    
    if not(commons.check_available_disk_space()):  # requires 3GB minimum
        log.info(messages.not_enough_space)
        log.info(messages.additional_help)
        log.info(messages.abort)
        commons.sys_exit()
    
    # Queries user to agree with Anaconda Terms and Conditions
    log.info(messages.install_miniconda_terms_and_conditions)
    choice = 1
    while not(choice in system.approve) \
            and not(choice in system.deny) \
            and not(choice == ""):
        
        choice = user_input(messages.query).upper()
    
    if choice in system.approve or choice == "":
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
    env_exec = miniconda_handler.get_env_python_exec()
    miniconda_folder = miniconda_handler.get_miniconda_install_folder()
    
    # cleans
    miniconda_install_file = miniconda_handler.get_miniconda_install_file()
    os.remove(miniconda_install_file)
    log.debug("removed: {}".format(miniconda_install_file))

elif choice == "2":  # Manual Python libs installation
    
    log.info(messages.manual_install)
    choice = user_input(messages.big_query).upper()
    
    if choice in system.deny:
        log.info(messages.additional_help)
        log.info(messages.abort)
        commons.sys_exit()
    
    # registers installation variables
    install_option = 2
    env_exec = sys.executable
    conda_exec = None
    miniconda_folder = None

elif choice == "3":
    log.info(messages.additional_help)
    log.info(messages.abort)
    commons.sys_exit()

else:  # expecting the unexpected
    log.info(messages.something_wrong)
    log.info(messages.abort)
    commons.sys_exit()

time.sleep(1)

# creates Farseer-NMR executable files
commons.create_executables(installation_folder, env_exec)

# registers installation variables in a file.py
commons.register_install_vars(
    install_dir=installation_folder,
    env_exec=env_exec,
    install_option=install_option,
    conda_exec=conda_exec,
    env_name=system.latest_env_name,
    env_version=system.latest_env_version,
    miniconda_folder=miniconda_folder
    )

log.info(messages.install_completed)
user_input()
