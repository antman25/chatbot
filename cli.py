#!/usr/bin/python3

import argparse
import logging
import os
import sys
from os import path, sep, getcwd, access, W_OK
from pathlib import Path
from platform import system

from logs import root_logger

log = logging.getLogger(__name__)

def get_config(config_path):
    config_fullpath = config_path
    if not path.exists(config_fullpath):
        log.error('I cannot find the config file %s.' % config_fullpath)
        log.error('You can change this path with the -c parameter see --help')
        exit(-1)

    try:
        config = __import__(path.splitext(path.basename(config_fullpath))[0])
        log.info('Config check passed...')
        return config
    except Exception:
        log.exception('I could not import your config from %s, please check the error below...' % config_fullpath)
        exit(-1)


def main():
    logging.basicConfig(level=logging.DEBUG)
    execution_dir = getcwd()

    # By default insert the execution path (useful to be able to execute Errbot from
    # the source tree directly without installing it.
    sys.path.insert(0, execution_dir)
    
    parser = argparse.ArgumentParser(description='The main entry point of the chatbot.')
    parser.add_argument('-c', '--config', default=None, help='Full path to your config.py (default: config.py in current working directory).')

    args = vars(parser.parse_args())
    #print (args)

    config_path = args['config']
    # setup the environment to be able to import the config.py
    if config_path:
        # appends the current config in order to find config.py
        sys.path.insert(0, path.dirname(path.abspath(config_path)))
    else:
        config_path = execution_dir + sep + 'config.py'
    #print (config_path)
    config = get_config(config_path)
    #print (config)
    if not path.exists(config.BOT_DATA_DIR):
        raise Exception(f'The data directory "{config.BOT_DATA_DIR}" for the bot does not exist.')
    if not access(config.BOT_DATA_DIR, W_OK):
        raise Exception(f'The data directory "{config.BOT_DATA_DIR}" should be writable for the bot.')
    restore = None

    from bootstrap import bootstrap
    #import bootstrap
    bootstrap("mattermost", root_logger, config, restore)

if __name__ == "__main__":
    main()
