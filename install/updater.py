"""
Manages software updates.

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
python_version = sys.version_info[0]

# necessary to keep Windows terminal popups openned before sys.exit
if python_version == 3:
    user_input = input
elif python_version == 2:
    user_input = raw_input

if python_version != 3:
    python_version_error = """
Python 3 is required. Press ENTER to terminate.
"""
    user_input(python_version_error)
    sys.exit(1)

import os
import shutil
import zipfile
import time

from install import logger
from install import commons
from install import messages

_new_version_url = \
    "https://github.com/Farseer-NMR/FarSeer-NMR/archive/master.zip"
_new_version_zip = "master.zip"
_folders_to_remove = ["Documentation", "gui", "core", "install", ".idea"]


class Updater():
    """
    Controls version Updating methods.
    
    Strategy:
        Downloads master branch .zip file from project repository.
        Unzips.
        Removes old files and folders.
        Replaces with new version files and folders.
        Maintains install configuration, namely Miniconda installation
            and Python executable paths on bin files.
    """
    
    def __init__(
            self,
            install_wd,
            update_log="update.log",
            new_version_url=_new_version_url,
            new_version_zip=_new_version_zip,
            folders_to_remove=_folders_to_remove
            ):
        """
        
        Parameters:
            - install_wd (str): the software installation directory
            
            - update_log (opt): the name of the log file (df: 'update.log')
            
            - new_version_url (opt): link to new version
                (df: https://github.com/<archive>/master.zip)
            
            - new_version_zip (opt): ZIP file to temporarily save new version
                (df: 'master.zip')
            
            - folders_to_remove (opt): list of folders to remove from
                old version.
            
        """
        
        self.log = logger.InstallLogger(__name__).gen_logger()
        self.log.debug("Initiated Updater instance")
        
        self.set_install_wd(install_wd)
        
        self.set_new_version_url(new_version_url)
        self.set_new_version_zip(os.path.join(install_wd, new_version_zip))
        self.set_folders_to_remove(folders_to_remove)
        self.set_zip_folder(None)
        
        return
    
    def get_new_version_url(self):
        """Returns URL for the software new version."""
        return self._new_version_url
    
    def get_new_version_zip(self):
        """Returns name of ZIP file for software's new version."""
        return self._new_version_zip
    
    def get_folders_to_remove(self):
        """
        Returns list of old folders to remove
        when updating to software's new version.
        """
        return self._folders_to_remove
    
    def get_zip_folder(self):
        """Returns the name of the main folder in new version ZIP."""
        if self._zip_folder:
            return self._zip_folder
        else:
            self.log.info("- zip folder not yet defined.")
            self.log.info("- a zip file should firstly be unpacked")
            return None
    
    def get_install_wd(self):
        """
        Returns software's installation directory to be updated
        to the new version.
        """
        return self._install_wd
    
    def set_new_version_url(self, new_version):
        """Sets URL for the new version."""
        self._new_version_url = new_version
        self.log.debug("<new_version_url>: {}".format(self._new_version_url))
        return
    
    def set_new_version_zip(self, new_version_zip):
        """Sets the ZIP file new to save new version."""
        self._new_version_zip = new_version_zip
        self.log.debug("<new_version_zip>: {}".format(self._new_version_zip))
        return
    
    def set_folders_to_remove(self, folders):
        """Defines folders to remove from old version."""
        self._folders_to_remove = folders
        self.log.debug(
            "<folders_to_remove>: {}".format(self._folders_to_remove)
            )
        return
    
    def set_install_wd(self, folder):
        """Sets software's installation (update) folder."""
        
        if not os.path.exists(folder):
            e = "* ERROR * Folder does not exist: '{}'".format(folder)
            self.log.info(e)
            self.log.info(messages.something_wrong)
            self.log.info(messages.additional_help)
            raise AttributeError(e)
        
        else:
            self._install_wd = os.path.abspath(folder)
            self.log.debug("<install_wd>: {}".format(self._install_wd))
        
        return
    
    def set_zip_folder(self, zip_folder):
        """Sets main folder after ZIP unpack."""
        self._zip_folder = zip_folder
        self.log.debug("<zip_folder>: {}".format(zip_folder))
        return
    
    def download_software(self):
        """Downloads the software's new version."""
        
        self.log.info("* Starting software's new version download.")
        
        commons.download_file(
            self.get_new_version_url(),
            os.path.join(self.get_install_wd(), self.get_new_version_zip())
            )
        
        self.log.info("    OKAY\n")
        time.sleep(0.5)
        
        return
    
    def remove_old_version(self):
        """Removes previous software's folders"""
        
        self.log.info("* Removing old folders...")
        self.log.debug("install_wd: {}".format(self.get_install_wd()))
        self.log.debug(
            "folder_to_remove: {}".format(self.get_folders_to_remove())
            )
        
        for f in self.get_folders_to_remove():
            ff = os.path.join(self.get_install_wd(), f)
            if os.path.exists(ff):
                shutil.rmtree(ff)
                self.log.debug("* '{}' removed".format(ff))
        
        self.log.info("    OKAY\n")
        time.sleep(0.5)
        
        return
    
    def unzip_new_version(self):
        """Unzips new version"""
        
        # lists current files/folders in installation folder
        previous_dirs = set(os.listdir(self.get_install_wd()))
        self.log.debug("<previous_dirs>: {}".format("\n".join(previous_dirs)))
        
        # removes previous .zip from previous updates (if existent)
        if self.get_new_version_zip() in previous_dirs:
            info_msg = "* A previous version of {} was found"
            self.log.info(info_msg.format(self.get_new_version_zip()))
            self.log.info("    ... removing.")
            os.remove(self.get_new_version_zip())
            self.log.debug("removed")
        
        # extracts downloaded .zip file
        self.log.info("* Unpacking {}".format(self.get_new_version_zip()))
        self.log.debug("* to ... {}".format(self.get_install_wd()))
        zip_ref = zipfile.ZipFile(self.get_new_version_zip(), 'r')
        zip_ref.extractall(self.get_install_wd())
        zip_ref.close()
        
        # lists files/folders in installation folder
        new_dirs = set(os.listdir(self.get_install_wd()))
        self.log.debug("<new_dirs> set: {}".format("\n".join(new_dirs)))
        
        # identifies the new folder
        # expects to find the newly created folder after zip.extractall()
        new_dirs.difference_update(previous_dirs)
        self.log.debug("sets diff update: {}".format(new_dirs))
        self.log.debug("len new_dirs: {}".format(len(new_dirs)))
        
        # only ONE newly created folder can exist
        if len(new_dirs) == 1:
            self.set_zip_folder(
                os.path.join(
                    self.get_install_wd(),
                    "".join(new_dirs)  # set does not support indexing
                    )
                )
        
        else:
            self.log.info(
                "* ERROR * The new zip folder couldn't be identified"
                )
            self.log.info(messages.additional_help)
            self.log.info(messages.abort)
            commons.sys_exit()
        
        self.log.info("    OKAY\n")
        time.sleep(0.5)
        
        return
    
    def move_new_files(self):
        """
        Moves new files to software's installation directory.
        """
        
        self.log.info("* Moving new files...")
        
        if not(self.get_zip_folder()):
            self.log.info("* ERROR * Can't move new files.")
            self.log.info("* ERROR * zip folder not defined.")
            self.log.info(messages.additional_help)
            self.log.info(messages.abort)
            commons.sys_exit()
        elif not(os.path.exists(self.get_zip_folder())):
            self.log.info("* ERROR * Can't move new files.")
            self.log.info("* ERROR * new extract folder does NOT exist")
            self.log.info(messages.additional_help)
            self.log.info(messages.abort)
            commons.sys_exit()
        
        source_folder = self.get_zip_folder()
        self.log.debug("<source_folder>: {}".format(source_folder))
        
        files = os.listdir(source_folder)
        self.log.debug("files list: {}".format(files))
        
        for f in files:
            s = os.path.join(source_folder, f)
            d = os.path.join(self.get_install_wd(), f)
            self.log.debug("moving '{}' to '{}'".format(s, d))
            try:
                shutil.move(s, d)
            except Exception as e:
                self.log.info("* ERROR * Couldn't move {}".format(s))
                self.log.debug(e)
                self.log.info(messages.something_wrong)
                self.log.info(messages.abort)
                commons.sys_exit()
        
        self.log.info("    OKAY\n")
        time.sleep(0.5)
        
        return
    
    def clean_files(self):
        """Removes unnecessary files after updating."""
        
        self.log.info("* Cleaning unnecessary files...")
        
        self.log.debug("removing: {}".format(self.get_zip_folder()))
        try:
            os.rmdir(self.get_zip_folder())
        except OSError as e:
            self.log.info("* WARNNING * zip folder not found.")
            self.log.debug(e)
            self.log.info(messages.something_wrong)
            self.log.info("* continuing...")
        except TypeError as e:
            self.log.info(
                "* WARNNING * zip folder not defined. Nothing to remove"
                )
            self.log.debug(e)
            self.log.info("* continuing...")
        except Exception as e:
            self.log.info("* ERROR * Something strange happened")
            self.log.debug(e)
            self.log.info(messages.something_wrong)
            self.log.info(messages.additional_help)
            self.log.info(messages.abort)
            commons.sys_exit()
        
        self.log.debug("removing: {}".format(self.get_new_version_zip()))
        try:
            os.remove(self.get_new_version_zip())
        except FileNotFoundError as e:
            self.log.info("* ERROR * Couldn't remove new version zip file")
            self.log.debug(e)
            self.log.info("* continuing...")
        except Exception as e:
            self.log.info("* ERROR * Something strange happened")
            self.log.debug(e)
            self.log.info(messages.additional_help)
            self.log.info(messages.abort)
            commons.sys_exit()

        self.log.info("    OKAY\n")
        time.sleep(0.5)
        
        return
    
    def run(self):
        """Runs standard update algorythm."""
        self.log.info("\n*** Starting update ***\n")
        self.download_software()
        self.unzip_new_version()
        self.remove_old_version()
        self.move_new_files()
        self.clean_files()
        self.log.info("\n*** Update Completed ***\n")
        return


if __name__ == "__main__":
    
    print("I am updater")
