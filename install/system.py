"""
MANAGES SYSTEM INFORMATION AND OTHER NECESSARY PARAMETERS
    FOR INSTALLATION AND UPDATE.

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

import platform as pltfrm
import os

# configure accordingly to the host project
software_name = "Farseer-NMR"
software_version = (1, 3, 4)  # v1.0.0
min_space_allowed = 3  # min GB required to install your software
installation_log_name = "install.log"
update_log_name = "update.log"
_lastest_env_file = "farseernmr.yml"
_miniconda_folder = "miniconda"

# about the default installation folder
_file_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
installation_folder = os.path.abspath(os.path.join(_file_path, os.pardir))

# about the running system
_platforms = {"Linux": "Linux", "Darwin": "MacOSX", "Windows": "Windows"}
_executable_file_extensions = {"Linux": "", "MacOSX": "", "Windows": "py"}

platform = _platforms[pltfrm.system()]
bits = "x86_64" if (pltfrm.machine().endswith('64')) else "x86"
exec_file_extension = _executable_file_extensions[platform]

# about conda env
latest_env_file = os.path.join(_file_path, _lastest_env_file)
default_miniconda_folder = os.path.join(installation_folder, _miniconda_folder)

with open(latest_env_file, 'r') as f:
    for line in f:
        if line.startswith('name:'):
            latest_env_name = line.strip().split()[-1]
        elif line.startswith('# version:'):
            latest_env_version = int(line.strip().split()[-1])


# about downloading Miniconda
base_miniconda_web_link = "https://repo.continuum.io/miniconda/"
_miniconda_file_extensions = {
    "Linux": "sh",
    "MacOSX": "sh",
    "Windows": "exe"
    }
miniconda_file_extension = _miniconda_file_extensions[platform]


# other variables
approve = ["Y", "YES"]
deny = ["N", "NO", "EXIT", "E", "A", "ABORT"]
