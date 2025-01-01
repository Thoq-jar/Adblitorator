"""
Adbliterator.py: The library for Adbliterator.
@author: Thoq
@since: December 31st, 2024
"""

import logging
import os
import pyfiglet
import yaml


def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


script_dir = os.path.dirname(os.path.abspath(__file__))
config = load_yaml(os.path.join(script_dir, '../adbliterator/ad_list.yaml'))
settings = load_yaml(os.path.join(script_dir, '../adbliterator/config.yaml'))

BANNER = pyfiglet.figlet_format("Adbliterator", font="fire_font-s")

AD_KEYWORDS = config.get('AD_KEYWORDS', [])
KNOWN_HOSTS = config.get('KNOWN_HOSTS', [])
KNOWN_PATHS = config.get('KNOWN_PATHS', [])
FLASH_EXTENSIONS = config.get('FLASH_EXTENSIONS', [])
FLASH_MIME_TYPES = config.get('FLASH_MIME_TYPES', [])
SETTINGS = settings.get('SETTINGS', {})


def get_bool_settings_value(key) -> bool:
    return str(SETTINGS.get(key, 'false')).lower() == 'true'


def get_bool_config_value(key) -> bool:
    return str(SETTINGS.get(key, 'false')).lower() == 'true'


debug = get_bool_config_value('debug')
default_config = get_bool_config_value('default')
if debug:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
else:
    logging.basicConfig(level=logging.CRITICAL)


def write_log(message):
    if debug:
        logging.info(message)
