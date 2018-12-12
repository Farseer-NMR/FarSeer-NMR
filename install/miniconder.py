# -*- coding: utf-8 -*-
"""
A MODULE TO MANAGE FARSEER-NMR PYTHON DEPENDENCIES VIA MINICONDA.

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
import re

python_version = sys.version_info[0]
if python_version == 2:
    import urlparse

elif python_version == 3:
    import urllib.parse as urlparse

else:
    sys.exit("* ABORTING * You are using a Python '{}', \
you should use versions 2 or 3.".format(python_version))

from install import system
from install import logger
from install import messages
from install import commons


class CondaManager():
    """
    Manages Miniconda installation and ENV configuration for
    Farseer-NMR.
    """
    
    def __init__(self, cwd=None):
        """
        Parameters:
            
            - cwd (opt, str): the Miniconda installation path.
                Defaults to os.get_cwd()
        """
        
        self.log = logger.InstallLogger(__name__).gen_logger()
        
        cwd = cwd or os.get_cwd()
        self.set_install_folder(cwd)
        
        self.set_miniconda_base_web_link(system.base_miniconda_web_link)
        
        self.set_miniconda_web_file(
            "Miniconda3-latest-{}-{}.{}".format(
                system.platform,
                system.bits,
                system.miniconda_file_extension
                )
            )
        
        self.set_miniconda_download_link(
            urlparse.urljoin(
                self.get_miniconda_base_web_link(),
                self.get_miniconda_web_file()
                )
            )
        
        self.set_miniconda_install_file(
            os.path.join(
                self.get_install_folder(),
                self.get_miniconda_web_file()
                )
            )
        
        self.set_miniconda_install_folder(
            os.path.join(
                self.get_install_folder(),
                system.miniconda_folder
                )
            )
        
        self.set_env_file(system.latest_env_file)
        
        self.set_env_version(system.latest_env_version)
        
        return
    
    def set_install_folder(self, folder):
        """
        Sets current working directory, where installation will take place.
        
        Parameters:
            - folder (str): folder path
        """
        self._install_folder = folder
    
        return
    
    def set_miniconda_base_web_link(self, link):
        """
        Sets the base web link where to download Miniconda.
        
        Parameters:
        
            - link (str): web link
        
        Example:
            https://repo.continuum.io/miniconda/
        """
        self._miniconda_base_web_link = link
        
        debug_msg = "<miniconda_web_base_link> set to: {}"
        self.log.debug(debug_msg.format(self._miniconda_base_web_link))
        
        return
    
    def set_miniconda_web_file(self, file_name):
        """
        Sets Miniconda download file.
        
        Parameters:
        
            - file_name (str): the name of the file.
        """
        
        self._miniconda_web_file = file_name
        
        debug_msg = "<miniconda_web_file> set to: {}"
        self.log.debug(debug_msg.format(self._miniconda_web_file))
        
        return
    
    def set_miniconda_download_link(self, link):
        """
        Sets Miniconda full download URL.
        """
        
        self._miniconda_download_link = link
        
        debug_msg = "<miniconda_download_link> set to: {}"
        self.log.debug(debug_msg.format(self._miniconda_download_link))
        
        return
    
    def set_miniconda_install_file(self, exec_file):
        """
        Sets Miniconda installation file.
        """
        
        self._miniconda_install_file = exec_file
        
        debug_msg = "<miniconda_install_file> set to: {}"
        self.log.debug(debug_msg.format(self._miniconda_install_file))
        return
    
    def set_miniconda_install_folder(self, folder):
        """
        Sets Miniconda installation folder.
        
        Parameters:
        
            - folder (str): the main folder where to place Miniconda
                install folder.
        """
        self._miniconda_install_folder = folder
        
        debug_msg = "<miniconda_install_folder> set to: {}"
        self.log.debug(debug_msg.format(self._miniconda_install_folder))
        
        return
    
    def set_env_file(self, env_file):
        """
        Sets Miniconda Farseer-NMR environment file.
        
        Parameters:
        
            - env_file (str): path to Anaconda Env (.yml) file.
        """
        
        self.log.debug("reading env_file: {}".format(env_file))
        
        valid_file = bool(
            isinstance(env_file, str)
            and env_file.endswith('.yml')
            and os.path.exists(env_file)
            and os.path.isfile(env_file)
            )
        
        self.log.debug("<valid_file>: {}".format(valid_file))
            
        if valid_file:
            
            self._env_file = env_file
            
            with open(self._env_file, 'r') as f:
                for line in f:
                    
                    if line.startswith("name:"):
                        env_name = line.strip().split()[-1]
                        self.set_env_name(env_name)
                    
                    elif line.startswith("# version:"):
                        env_version = line.strip().split()[-1]
                        self.set_env_version(env_version)
        
        elif not(isinstance(env_file, str)):
            raise ValueError("Miniconda env file name not a string")
        
        elif not(env_file.endswith('.yml')):
            err_msg = "* ERROR * '{}' should have .yml extension"
            self.log.info(err_msg.format(env_file))
            raise ValueError("Miniconda env file not valid")
        
        elif not(os.path.exists(env_file)):
            self.log.info("* ERROR * '{}' does not exists.".format(env_file))
            raise ValueError("Miniconda env file not valid")
        
        elif not(os.path.isfile(env_file)):
            self.log.info("* ERROR * '{}' is not a file.".format(env_file))
            raise ValueError("Miniconda env file not valid")
        
        self.log.debug("<env_file>: {}".format(self._env_file))
        
        return
    
    def set_conda_exec(self, conda_exec):
        """
        Sets path to Miniconda 'conda' executable.
        """
        
        if not(os.path.exists(conda_exec)):
            err_msg = "* ERROR * conda exec file does NOT exist: {}"
            self.log.info(err_msg.format(conda_exec))
            self.log.info(messages.something_wrong)
            self.log.info(messages.additional_help)
            self.log.info(messages.abort)
            commons.sys_exit()
        
        self._conda_exec = conda_exec
        debug_msg = "Miniconda conda bin exec set to: {}"
        self.log.debug(debug_msg.format(self._conda_exec))
    
        return
    
    def set_env_name(self, name='farseernmr'):
        """
        Sets Farseer-NMR Conda environment name.
        """
        
        self._env_name = name
        self.log.debug("<env_name>: {}".format(self._env_name))
        return
    
    def set_env_python_exec(self, python_exec):
        """
        Defines Python executable for Farseer-NMR environment.
        """
        
        self._env_python_exec = python_exec
        
        self.log.debug("<env_python_exec>: {}".format(self._env_python_exec))
        
        return
    
    def set_env_version(self, env_version):
        """
        Sets Farsee-NMR Miniconda environment version.
        Should be integer.
        """
        try:
            int(env_version)
        except ValueError as e:
            self.log.info(
                "* ERROR * Farseer-NMR Python environment version"
                "should be integer type"
                )
            self.log.info("* ERROR * env version not set")
            self.log.debug(e)
            commons.sys_exit()
            return
        
        self._env_version = env_version
        self.log.debug("<env_version>: {}".format(self._env_version))
        return
    
    def set_env_folder(self, env_folder):
        """
        Defines an existent ENV folder
        """
        
        if not(os.path.exists(env_folder)):
            self.log.info(
                "* ERROR* folder does NOT exists: {}".format(env_folder)
                )
            self.log.info(messages.something_wrong)
            self.log.info(messages.additional_help)
            self.log.info(messages.abort)
            commons.sys_exit()
        
        self._env_folder = env_folder
        self.log.debug("<env_folder>: {}".format(self._env_folder))
        return
    
    def get_install_folder(self):
        return self._install_folder
    
    def get_miniconda_base_web_link(self):
        return self._miniconda_base_web_link
    
    def get_miniconda_web_file(self):
        return self._miniconda_web_file
    
    def get_miniconda_download_link(self):
        return self._miniconda_download_link
    
    def get_miniconda_install_file(self):
        return self._miniconda_install_file
    
    def get_miniconda_install_folder(self):
        return self._miniconda_install_folder
    
    def get_env_file(self):
        return self._env_file
    
    def get_env_reference_file(self):
        return self._env_reference_file
    
    def get_conda_exec(self):
        return self._conda_exec
    
    def get_env_name(self):
        return self._env_name
    
    def get_env_python_exec(self):
        return self._env_python_exec
    
    def get_python_version_folder(self):
        return self._python_version_folder
    
    def get_env_version(self):
        return self._env_version
    
    def get_env_folder(self):
        return self._env_folder
    
    def check_previous_miniconda_folder(self, folder='[M|m]iniconda.*'):
        """
        Checks if a Miniconda related folder exists inside
        the Farseer-NMR folder. Accepts regex.
        
        Returns folder name, False otherwise.
        """
        self.log.debug("checking if miniconda install exists")
        
        list_dir = os.listdir(self.get_install_folder())
        dirlist = [a for a in list_dir if os.path.isdir(a)]
        self.log.debug("<dirlist>: {}".format("\n".join(dirlist)))
        
        mask = re.compile(folder)
        miniconda_folder = [a for a in dirlist if mask.match(a)]
        self.log.debug("<miniconda_folder>: {}".format(miniconda_folder))
        
        if miniconda_folder:
            if len(miniconda_folder) == 1:
                self.log.debug("returning: {}".format(miniconda_folder[0]))
                return miniconda_folder[0]
            
            else:
                self.log.info("More than one Miniconda folder found")
                self.log.info("You may wish to remove them manually")
                self.log.info(messages.something_wrong)
                self.log.info(messages.abort)
                commons.sys_exit()
                return
        
        else:
            self.log.debug("returning False")
            return False
    
    def download_miniconda(self):
        """
        Downloads Miniconda installation file.
        """
        
        self.log.info("* Downloading Miniconda...")
        self.log.debug("url: {}".format(self.get_miniconda_download_link()))
        self.log.debug(
            "destination: {}".format(self.get_miniconda_install_file())
            )
        
        commons.download_file(
            self.get_miniconda_download_link(),
            self.get_miniconda_install_file()
            )
        
        commons.change_permissions_777(self.get_miniconda_install_file())
        self.log.debug("permissions changed")
        
        return
    
    def install_miniconda(self):
        """
        Routine to install Miniconda.
        """
        
        unix_exec_line = " ".join(
            [
                self.get_miniconda_install_file(),
                '-b',
                '-p',
                self.get_miniconda_install_folder()
                ]
            )
        
        # prepares execution line
        if system.platform in ("Linux", "MacOSX"):
            exec_line = unix_exec_line
        
        elif system.platform in ("Windows"):
            # https://conda.io/docs/user-guide/install/windows.html
            exec_line = " ".join(
                [
                    self.get_miniconda_install_file(),
                    "/InstallationType=JustMe",
                    "/RegisterPython=0",
                    "/S",
                    "/D=" + self.get_miniconda_install_folder()
                    ]
                )
        
        else:
            warning_message = """
* WARNING * Your platform is not Linux, MacOSX or Windows
* WARNING * Miniconda installation command will be
* WARNING * same as if this was a UNIX machine.
* WARNING * if the installation fails please contact us for support
"""
            self.log.info(warning_message)
            exec_line = unix_exec_line
        
        self.log.debug("<exec_line>: {}".format(exec_line))
        
        # installs miniconda
        commons.sub_call(exec_line)
        
        # sets miniconda conda exec file
        if system.platform in ("Windows"):
            # https://stackoverflow.com/questions/37117571/where-does-anaconda-python-install-on-windows
            # https://stackoverflow.com/questions/44597662/conda-command-is-not-recognized-on-windows-10
            # https://stackoverflow.com/questions/28612500/why-anaconda-does-not-recognize-conda-command
            self.set_conda_exec(
                os.path.join(
                    self.get_miniconda_install_folder(),
                    'Scripts',
                    'conda.exe'
                    )
                )
        
        else:  # UNIX systems
            self.set_conda_exec(
                os.path.join(
                    self.get_miniconda_install_folder(),
                    'bin',
                    'conda'
                    )
                )
        
        return
    
    def install_package(self, package):
        """
        Install a given package in Miniconda.
        
        Parameters:
        
            - package (str): the name of the package.
                If desired, version can be given, example:
                    'conda-build=3.16.0'
        """
        
        # https://conda.io/docs/user-guide/tasks/manage-pkgs.html#installing-packages
        
        self.log.debug("installing package: {}".format(package))
        
        exec_line = "{} install -y {}".format(
            self.get_conda_exec(),
            package
            )
        
        exec_output = commons.sub_call(exec_line).decode("utf-8").split('\n')
        
        self.log.debug("\n".join(exec_output))
        
        self.log.debug("package installaged")
        
        self.logs_package_installation(package)
        
        return
    
    def logs_package_installation(self, package):
        """
        Logs package installation with 'conda list'
        """
        
        package_name = package.split('=')[0]
        
        exec_line = "{} list {}".format(
            self.get_conda_exec(),
            package_name
            )
        
        exec_output = commons.sub_call(exec_line).decode("utf-8").split('\n')
        
        self.log.debug("\n".join(exec_output))
        
        return
    
    def install_env(self):
        """
        Installs Anaconda Environment.
        """
        
        self.log.info("* Starts Miniconda Environment Installation")
        
        # defines command to create environment from .yml file
        exec_line = '{} env create -f {}'.format(
            self.get_conda_exec(),
            self.get_env_file()
            )
        
        self.log.debug("<exec_line>: {}".format(exec_line))
        
        commons.sub_call(exec_line)
        
        # sets python env variables
        
        self.set_env_folder(
            os.path.join(
                self.get_miniconda_install_folder(),
                'envs',
                self.get_env_name()
                )
            )
        
        if system.platform in ("Windows"):
            # https://docs.anaconda.com/anaconda/user-guide/tasks/integration/python-path/
            self.set_env_python_exec(
                os.path.join(
                    self.get_env_folder(),
                    'python.exe'
                    )
                )
        
        else:  # UNIX systems
            self.set_env_python_exec(
                os.path.join(
                    self.get_env_folder(),
                    'bin',
                    'python'
                    )
                )
        
        # self.set_python_version_folder()
        
        return
    
    def logs_env_information(self):
        """
        Register installed env to log file.
        """
        self.log.info("* Registering environment...")
        
        # confirm environment was installed correctly
        exec_line = "{} list -n {}".format(
            self.get_conda_exec(),
            self.get_env_name()
            )
        
        # https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
        installed_env = commons.sub_call(exec_line).decode("utf-8").split('\n')
        
        self.log.debug("\n".join(installed_env))
        
        return
    
    def add_install_folder_to_site_packages(self):
        """
        Adds Farseer-NMR directory to Miniconda Farseer-NMR environment.
        """
        
        # https://stackoverflow.com/questions/37006114/anaconda-permanently-include-external-packages-like-in-pythonpath
        # https://stackoverflow.com/questions/32715261/how-to-add-folder-to-search-path-for-a-given-anaconda-environment
        # https://conda.io/docs/commands/build/conda-develop.html
        
        exec_line = " ".join(
            [
                self.get_conda_exec(),
                'develop',
                '-p',
                self.get_env_folder(),
                self.get_install_folder()
                ]
            )
        
        result = commons.sub_call(exec_line).decode("utf-8").split('\n')
        
        self.log.debug("\n".join(result))
        self.log.debug("Farseer-NMR folder added to site-packges")
    
        return
    
    def remove_env(self):
        """
        Removes Miniconda Environment.
        """
        self.log.info("* Removing Miniconda Environment")
        
        exec_line = '{} remove -vy --name {} --all'.format(
            self.get_conda_exec(),
            self.get_env_name()
            )
        
        commons.sub_call(exec_line)
        
        return


if __name__ == "__main__":
    
    print('I am Miniconder')
