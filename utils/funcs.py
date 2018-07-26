"""
Copyright Â© 2017-2018 Farseer-NMR
Simon P. Skinner and JoÃ£o M.C. Teixeira

@ResearchGate https://goo.gl/z8dPJU
@Twitter https://twitter.com/farseer_nmr

This file is part of Farseer-NMR.

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
import logging
import logging.config
import json

logger = logging.getLogger(__name__)
logging.config.dictConfig(json.load(open('log_config.json')))

def get_util_confs(conf_file_name):
    """
    Returns the path to a configuration file in utils/
    
    Parameters:
        - conf_file_name (str): the name of the config file.
    
    Used to get default_config.json or log_config.json, or others.
    """
    logger.debug("Parameter OK: %", type(conf_file_name) == str)
    current_path = os.path.dirname(__file__)
    return os.path.join(current_path, conf_file_name)