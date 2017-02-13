# -*- coding: utf-8 -*-


import ConfigParser
import logging
import os
import pkg_resources
import shutil
import sys
from xdg import BaseDirectory

config_files_directory = BaseDirectory.save_config_path('ipp-macro-series-parser')

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def check_template_config_files():
    config_ini_path = os.path.join(config_files_directory, 'config.ini')
    config_template_ini_path = os.path.join(config_files_directory, 'config_template.ini')

    if os.path.exists(config_files_directory):
        if not os.path.exists(config_ini_path):
            if not os.path.exists(config_template_ini_path):
                log.info("Creating configuration template files in {}".format(config_files_directory))
                templates_config_files_directory = os.path.join(
                    pkg_resources.get_distribution('ipp-macro-series-parser').location)
                shutil.copy(
                    os.path.join(templates_config_files_directory, 'config_template.ini'),
                    os.path.join(config_files_directory, 'config_template.ini'),
                    )
            print("Rename and fill the template files in {}".format(config_files_directory))
            return False
    else:
        os.makedirs(config_files_directory)
        return check_template_config_files()

    return True


class Config(ConfigParser.SafeConfigParser):
    config_ini = None

    def __init__(self):
        ConfigParser.SafeConfigParser.__init__(self)
        if not check_template_config_files():
            print("Problem with the configuration directory {}: cannot proceed and thus exiting\n".format(
                config_files_directory))
            sys.exit()
        config_ini = os.path.join(config_files_directory, 'config.ini')
        if os.path.exists(config_ini):
            self.config_ini = config_ini
        self.read(config_ini)

    def save(self):
        assert self.config_ini, "configuration file paths are not defined"
        if self.config_ini and os.path.exists(self.config_ini):
            config_file = open(self.config_ini, 'w')
        self.write(config_file)
        config_file.close()
