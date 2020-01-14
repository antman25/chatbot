import argparse
import logging
import os
import sys
from os import path, sep, getcwd, access, W_OK
from pathlib import Path
from platform import system

log = logging.getLogger(__name__)

def main():
    execution_dir = getcwd()

    # By default insert the execution path (useful to be able to execute Errbot from
    # the source tree directly without installing it.
    sys.path.insert(0, execution_dir)
    print ('Anthony')

if __name__ == "__main__":
    main()
