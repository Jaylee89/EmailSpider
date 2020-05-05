#!/usr/bin/env python3

import argparse
import contextlib
import os, re, subprocess, sys

from spider._163 import MAIL163
from spider.qq import MAILQQ

from spider.common.util import Util

from spider.common.const import Const
import spider.common.log as log

Const.mysql = "mysql"
Const.mongo = "mongo"
Const.host = "host"
Const.port = "port"
Const.username = "username"
Const.password = "password"
Const.collection = "collection"

class EmailSpider(object):

    def __init__(self):
        self.logger = log
        self.is_mock = False
        self.mail_type = None
        self.username = None
        self.password = None
        self.authorization_code = None

    def _163(self):
        MAIL163(self.logger, self.is_mock, self.username, self.password).execute()

    def qq(self):
        pass

    def quit(self):
        sys.exit()

    def execute(self):
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-q", "--quiet", action="store_true")
        parser.add_argument("-m", "--mock", default=False, help="run in mock")
        parser.add_argument("-v", "--vendor", choices=["163", "qq"], help="choice mail vendor")
        parser.add_argument("-t", "--mailtype", choices=["pop", "imap"], help="choice mail type")
        parser.add_argument("-u", "--username", required = True, help="please input your username")
        parser.add_argument("-p", "--password", required = True, help="please input your password")
        parser.add_argument("-ac", "--authorizationcode", required = False, default = "", help="please input your authorization code from your mail's settings")
        args = parser.parse_args()

        vendor = args.vendor
        self.is_mock = (args.mock or "").lower() == 'true'
        self.mail_type = args.mailtype
        self.username = args.username
        self.password = args.password
        self.authorization_code = args.authorizationcode

        if args.quiet:
            self.quiet()
        elif vendor and self.mail_type and ((self.username and self.password) or (self.username and self.authorization_code)):
            self.logger.debug("vendor is {}, type is {}, username is {}, password is {}, authorization_code is {}".format(vendor, self.mail_type, self.username, self.password, self.authorization_code))
        else:
            self.logger.debug("\nTry './start -h' to get more. \n")
            self.quit()
        getattr(self, Util.appendUnderLinePrefix(vendor))()