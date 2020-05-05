# !/usr/bin/python3
# -*- coding:utf8 -*-

import pymysql
from spider.common.configuration.config import MYSQLConfig as mysqlconfig


class MYSql:
    def __init__(self, logger):
        self.logger = logger
        self.__config = mysqlconfig().get_config()
        self.__db = pymysql.connect(host=self.__config[0], user=self.__config[1], password=self.__config[2],
                                    database=self.__config[3], port=self.__config[4], connect_timeout=20)
        self.__cursor = self.__db.cursor()

    def close_connection(self):
        self.__db.close()
        self.__cursor.close()

    def update_data(self, sql):
        try:
            self.__cursor.execute(sql)
            self.__db.commit()
            self.logger.debug("self.__db.commit() done")
        except:
            self.logger.debug("self.__db.commit() have except")
            self.__db.rollback()

    def get_existing_data(self, sql):
        data = None
        try:
            self.__cursor.execute(sql)
            data = self.__cursor.fetchone()
            self.logger.debug("get_existing_data method, data is ", data)
            return data
        except:
            self.logger.debug("self.__db.commit() have except")
            self.__db.rollback()
