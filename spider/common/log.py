#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Level	Numeric Value    Function	Used to
CRITICAL	50	logging.critical()	Show a serious error, the program may be unable to continue running
ERROR	    40	logging.error()	    Show a more serious problem
WARNING	    30	logging.warning()	Indicate something unexpected happened, or could happen
INFO	    20	logging.info()	    Confirm that things are working as expected
DEBUG	    10	logging.debug()	    Diagnose problems, show detailed information
"""

import logging, os
from logging.handlers import RotatingFileHandler

def get_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

root_dir = get_root() + os.sep + "logs" + os.sep
if not os.path.isdir(root_dir):
    os.mkdir(root_dir)

file_path = root_dir + 'autolog.log'

# file_dir = os.path.split(os.path.realpath(__file__))[0] + os.sep
# if not os.path.isdir(file_dir):
#     os.mkdir(file_dir)
# file_path = file_dir + filename

# logging.basicConfig(level=logging.DEBUG) #print log in console
# logging.basicConfig(filename="test.log", level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=file_path,
                    filemode='w')

Rthandler = RotatingFileHandler(file_path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8")
Rthandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
Rthandler.setFormatter(formatter)
logging.getLogger('mail').addHandler(Rthandler)

def debug(msg, *args, **kwargs):
    logging.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logging.info(msg, *args, **kwargs)
