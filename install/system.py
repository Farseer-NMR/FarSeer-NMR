"""
MANAGES SYSTEM INFORMATION AND OTHER NECESSARY PARAMETERS
    FOR FARSEER-NMR INSTALLATION AND UPDATE.

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
import platform as pltfrm
import os

farseer_version = (1, 3, 0)  # v1.3.0

min_space_allowed = 3  # GB

_platforms = {"Linux": "Linux", "Darwin": "MacOSX", "Windows": "Windows"}
_executable_file_extensions = {"Linux": None, "MacOSX": None, "Windows": "py"}

platform = _platforms[pltfrm.system()]
bits = "x86_64" if (pltfrm.machine().endswith('64')) else "x86"

exec_file_extension = _executable_file_extensions[platform]

approve = ["Y", "YES"]
deny = ["N", "NO", "EXIT", "E", "A", "ABORT"]

gui_file = 'farseer_gui'
cmd_file = 'farseer_cmd'
update_file = 'farseer_update'

if exec_file_extension:
    gui_file += '.{}'.format(exec_file_extension)
    cmd_file += '.{}'.format(exec_file_extension)
    update_file += '.{}'.format(exec_file_extension)

_file_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

installation_folder = os.path.abspath(os.path.join(_file_path, os.pardir))

latest_env_file = os.path.join(_file_path, 'farseernmr.yml')

with open(os.path.join(_file_path, latest_env_file)) as f:
    for line in f:
        if line.startswith('name:'):
            latest_env_name = line.strip().split()[-1]
        elif line.startswith('# version:'):
            latest_env_version = int(line.strip().split()[-1])

miniconda_folder = 'miniconda'
base_miniconda_web_link = "https://repo.continuum.io/miniconda/"
_miniconda_file_extensions = {
    "Linux": "sh",
    "MacOSX": "sh",
    "Windows": "exe"
    }
miniconda_file_extension = _miniconda_file_extensions[platform]

# https://stackoverflow.com/questions/6943208/activate-a-virtualenv-with-a-python-script
# https://halotis.com/running-python-code-in-windows-batch-file-trick/
# https://docs.python.org/3.3/using/windows.html
# finally, shebangs can be used on Windows10
# allow double click execution

run_gui = """#! {}
import sys
import os

farseernmr_folder = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir
        )
    )

sys.path.append(farseernmr_folder)

if sys.version_info[0] != 3:
    sys.stderr.write("Python 3 is required to run Farseer-NMR")
    sys.exit(1)

import gui.main
gui.main.run(sys.argv)
"""

run_cmd = """#! {}
'''
Executes Farseer-NMR command line.

REQUIRES PYTHON 3

Read further at:
https://github.com/Farseer-NMR/FarSeer-NMR/wiki/Documentation#running-command-line

usage:
    farseer_cmd CONFIG.JSON [opt, PATH TO SPECTRA FOLDER]
    
    - PATH TO SPECTRA FOLDER, folder where 'spectra' folder resides

example:
    farseer_cmd my_config.json
    farseer_cwd my_config.json .
    
'''
import sys
import os

farseernmr_folder = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir
        )
    )

sys.path.append(farseernmr_folder)

if sys.version_info[0] != 3:
    sys.stderr.write("Python 3 is required to run Farseer-NMR")
    sys.exit(1)

import core.farseermain

if len(sys.argv) == 2:
    farseer = core.farseermain.FarseerNMR(sys.argv[1])
elif len(sys.argv) == 3:
    farseer = core.farseermain.FarseerNMR(
        sys.argv[1],
        spectra_folder_path=sys.argv[2]
        )
else:
    sys.stderr.write(__doc__)
    sys.exit(1)

farseer.run()
"""

update_script = """#! {}

import sys
import os
import importlib

farseernmr_folder = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        os.pardir
        )
    )

sys.path.append(farseernmr_folder)

if sys.version_info[0] != 3:
    sys.stderr.write("Python 3 is required to run Farseer-NMR")
    sys.exit(1)

from install import logger
from install import messages

try:
    import install_reg
except ModuleNotFoundError as e:
    print("* ERROR * install_reg.py file not found")
    print("* ERROR * this file has created during installation")
    print("* ERROR * and is required for UPDATING")
    print("* ERROR * Reinstall Farseer-NMR to repair updating functions")
    print(messages.additional_help)
    print(messages.abort)
    sys.exit(1)

update_log = install_reg.install_wd.joinpath('update.log')

if update_log.exists():
    update_log.unlink()

log = logger.InstallLogger(__name__, log_file_name=update_log).gen_logger()

log.debug("start updating")

from install import updater
from install import commons
from install import miniconder

upf = updater.FarseerUpdater(install_reg.install_wd)
upf.run()

# reloads the updated version of system lib
from install import system
importlib.reload(system)

log.info("* Checking Conda environment...")

env_exec_new = install_reg.python_exec
install_option_new = install_reg.install_option

if system.latest_env_version > install_reg.farseer_env_version:

    log.info("* A NEW Python environment version is available")
    log.info("* Farseer-NMR dependencies must be updated")
    
    if install_reg.conda_exec and install_reg.install_option == 1:
    
        log.info("* Miniconda installation found")
        log.info("   ... starting env update")
        
        upc = miniconder.CondaManager(cwd=install_reg.install_wd)
        upc.set_conda_exec(install_reg.conda_exec)
        upc.set_env_name(install_reg.farseer_env_name)
        upc.remove_env()
        upc.set_env_file(system.latest_env_file)
        upc.install_env()
        upc.logs_env_information()
        upc.add_install_folder_to_site_packages()
        log.info("... Conda env UPDATED")
        
        env_exec_new = upc.get_env_python_exec()
        install_option_new = 1
    
    elif not(install_reg.conda_exec) and install_reg.install_option == 2:
        log.info("* You have previously configured Python libraries mannually")
        log.info("* You should update Farseer-NMR Python dependencies")
        log.info("* consult .yml file in 'install' folder")
    
    else:
        log.info("* ERROR* We couldn't access install information")
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys.exit(1)
    
else:
    log.info("   ...Conda env already in latest version")
    log.info("")

log.info("* Updating executable files...")

commons.create_executables(
    install_reg.install_wd,
    env_exec_new
    )

commons.register_install_vars(
    install_reg.install_wd,
    env_exec=env_exec_new,
    install_option=install_option_new,
    conda_exec=install_reg.conda_exec,
    env_name=system.latest_env_name,
    env_version=system.latest_env_version,
    miniconda_folder=system.miniconda_folder
    )

log.info(messages.update_completed)
commons.sys_exit()
"""
