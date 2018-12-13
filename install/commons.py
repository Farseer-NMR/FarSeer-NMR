# -*- coding: utf-8 -*-
"""
COMMON FUNCTIONS TO FARSEER-NMR INSTALLATION AND UPDATE ROUTINES.

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
import subprocess
import stat
import shutil
import ctypes

from install import logger
from install import system
from install import messages

log = logger.InstallLogger(__name__).gen_logger()

python_version = sys.version_info[0]
log.debug("* Python version: {}".format(python_version))

if python_version < 3:
    import urllib as url
    url_not_found_error = IOError
    user_input = raw_input

elif python_version == 3:
    import urllib
    import urllib.request as url
    url_not_found_error = urllib.error.URLError
    user_input = input

else:
    log.info(messages.unknown_python)
    log.info("* You are running Python version: {}".format(python_version))
    log.info(messages.something_wrong)
    log.info(messages.additional_help)
    log.info(messages.abort)
    user_input("Press ENTER to Terminate")
    sys.exit(1)


def check_available_disk_space(min_space=None):
    """
    Returns True if disk space is higher than <min_space>, False
    otherwise.
    
    Parameters:
    
        - min_space (float): the minimum space allowed in GBs.
            Defaults to system.min_space_allowed
    
    """
    
    min_space = min_space or system.min_space_allowed
    log.debug("<min_space>: {}".format(min_space))
    
    try:
        min_space = float(min_space)
    except ValueError as e:
        log.debug(e)
        log.info("<min_space> should be integer")
        sys_exit()
    
    log.info("* Checking available diskspace...")
    
    dirname = os.path.expanduser("~")
    
    if system.platform == "Windows":
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(dirname),
            None,
            None,
            ctypes.pointer(free_bytes)
            )
        free_space_GB = int(free_bytes.value / 1024 / 1024 / 1024)
    
    else:
        statvfs = os.statvfs(dirname)
        free_space_GB = \
            int(statvfs.f_frsize * statvfs.f_bavail / 1024 / 1024 / 1024)
    
    log.info("* ... available space: approx. {} GB".format(free_space_GB))
    
    if free_space_GB > min_space:
        log.info("* Enough disk space. Continuing...\n")
        return True
    
    elif free_space_GB <= min_space:
        return False
        
    else:  # expect the unexpected
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()


def reporthook(blocknum, blocksize, totalsize):
    """
    Modified from:
    
    https://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
    """
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("\r downloaded... %d" % (readsofar,))


def download_file(link, destination):
    """
    Downloads file.
    
    Parameters:
        - link (str): the file URL
        - destination (str): where to save file in computer
    """
    log.info("* Downloading {}...".format(link))
    log.info("* ... to destination: {}".format(destination))
    
    try:
        url.urlretrieve(
            link,
            destination,
            reporthook
            )
    except url_not_found_error as e:
        log.info(messages.url_error)
        log.info(messages.something_wrong)
        log.debug(e)
        log.info(messages.abort)
        sys_exit()
    except ValueError as e:
        log.info(messages.url_unkown)
        log.debug(e)
        log.info(messages.something_wrong)
        log.info(messages.abort)
        sys_exit()
    except Exception as e:
        log.debug(e)
        log.info(messages.something_wrong)
        log.info(messages.abort)
        sys_exit()
    
    if os.path.exists(destination):
        log.debug("destination file found: {}".format(destination))
        log.info("... Download completed")
    
    else:
        log.info("* ERROR * Couldn't find the downloaded file")
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()
    
    return


def change_permissions_777(file_):
    """
    Changes <file_> permissions to 777.
    """
    
    if not(os.path.exists(file_)):
        log.info("* ERROR * File '{}' not found!".format(file_))
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()
    
    log.debug("changing permissions to file: {}".format(file_))
    os.chmod(file_, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    log.debug("... OKAY")
    
    return


def remove_folders(folder_list):
    """
    Removes a list of folders
    
    Parameters:
        - folder_list (list)
    """
    
    if not(isinstance(folder_list, list)):
        log.info("*ERROR * folder_list parameters should be list")
        log.info("*ERROR * found instance of {}".format(type(folder_list)))
        sys_exit()
    
    log.debug("removing folders: {}".format("\n".join(folder_list)))
    
    for folder in folder_list:
        
        if os.path.exists(folder) and os.path.isdir(folder):
            log.debug("removing folder: {}".format(folder))
            shutil.rmtree(folder)
            log.info("*** Removed folder: {}".format(folder))
        
        else:
            log.debug("folder '{}' not found or is not dir".format(folder))
    
    log.debug("folders removed OKAY")
    
    return


def sub_call(exec_line):
    """
    Executes a subprocess.
    
    Parameters:
        
        - exec_line (str): the command to execute
    
    Returns the output of execution.
    """
    log.info("* Executing ...{}".format(exec_line))
    args = exec_line.strip().split()
    log.debug("args passed: {}".format(args))
    
    try:
        # maintains compatiblity with Python3 < 3.5
        # https://docs.python.org/3.5/library/subprocess.html#call-function-trio
        proc = subprocess.check_output(args)
    
    except FileNotFoundError as e:
        log.info("* ERROR * Could not find '{}'".format(args[0]))
        log.debug(e)
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()
    
    except subprocess.CalledProcessError as e:
        log.info("* ERROR * subprocess.CalledProcessError ocurred.")
        log.debug(e)
        log.info(messages.something_wrong)
        log.info(messages.additional_help)
        log.info(messages.abort)
        sys_exit()
    
    return proc


def create_executables(installation_folder, env_exec):
    """
    Creates Farseer-NMR executables based on install.system lib.
    
    Parameters:
    
        - installation_folder (str): the Farseer-NMR installation folder,
            where the 'bin' folder will reside
        
        - env_exec (str): the full path for the python executable
    """
    
    log.info(messages.gen_files_msg_head)
    
    bin_folder = os.path.join(installation_folder, 'bin')
    if not os.path.exists(bin_folder):
        os.mkdir(bin_folder)
        log.debug("'bin' folder didn't exists, created")
    
    else:
        log.debug("'bin' folder already existed")
    
    log.debug("<env_exec>: {}".format(env_exec))
    
    dict_of_execs = {
        'gui': (system.gui_file, system.run_gui),
        'cmd': (system.cmd_file, system.run_cmd),
        'updater': (system.update_file, system.update_script)
        }
    
    for key, executable in dict_of_execs.items():
        
        exec_file = os.path.join(bin_folder, executable[0])
        
        fout = open(exec_file, 'w')
        log.debug("opened {}".format(exec_file))
        
        fout.write(executable[1].format(env_exec))
        fout.close()
        
        change_permissions_777(exec_file)
    
    log.info(messages.gen_files_msg_tail)
    
    return


def register_install_vars(
        install_dir,
        env_exec=None,
        install_option=None,
        conda_exec=None,
        env_name=None,
        env_version=None,
        miniconda_folder=None
        ):
    """
    Writes installation variables to .py file.
    """
    
    install_reg_name = os.path.join(install_dir, 'install_reg.py')
    
    fout = open(install_reg_name, 'w')
    log.debug("install_reg.py openned: {}".format(install_reg_name))
    
    install_register = """
# This file registers the installation variables
# which are required for update purposes.
#
# Please do not delete it from the Farseer-NMR folder
#
# For additional help, please write us at:
# {}

from pathlib import Path

install_option = {}
install_wd = Path(r'{}')
conda_exec = {}
python_exec = {}
miniconda_folder = {}
farseer_env_name = {}
farseer_env_version = {}
""".format(
        messages.maillist_mail,
        install_option,
        install_dir,
        "Path(r'{}')".format(conda_exec) if conda_exec else None,
        "Path(r'{}')".format(env_exec) if env_exec else None,
        "Path(r'{}')".format(miniconda_folder) if miniconda_folder else None,
        "'{}'".format(env_name) if env_name else None,
        env_version
        )
    
    log.debug(install_register)
    
    fout.write(install_register)
    fout.close()
    log.debug("install_reg created")
    
    return


def sys_exit(number=1):
    user_input("Press ENTER to TERMINATE")
    sys.exit(number)
    return
