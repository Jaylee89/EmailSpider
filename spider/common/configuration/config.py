#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from spider.common.util import Util
from spider.common.const import Const

class MYSQLConfig(object):
    def __init__(self):
        json = Util.load_json(file_name = Const.mysql)
        self.__host = json.get(Const.host)
        self.__port = json.get(Const.port)
        self.__username = os.getenv(Const.username, json.get(Const.username))
        self.__password = os.getenv(Const.password, json.get(Const.password))
        self.__db_name = json.get(Const.collection)

    def get_config(self):
        return [self.__host, self.__username, self.__password, self.__db_name, self.__port]


class NoSQLConfig(object):
    def __init__(self):
        json = Util.load_json(file_name = Const.mongo)
        self.__host = json.get(Const.host)
        self.__port = json.get(Const.port)
        self.__username = os.getenv(Const.username, json.get(Const.username))
        self.__password = os.getenv(Const.password, json.get(Const.password))
        self.__db_name = json.get(Const.collection)

    def get_config(self):
        return [self.__host, self.__username, self.__password, self.__db_name, self.__port]
