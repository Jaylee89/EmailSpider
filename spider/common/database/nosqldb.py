# !/usr/bin/python3
# -*- coding:utf8 -*-

import pymongo
from spider.common.configuration.config import NoSQLConfig

class NoSql:
    def __init__(self, logger):
        self.logger = logger
        self._config = NoSQLConfig().get_config()
        self._client = pymongo.MongoClient(("%s" % (self._config[0])), self._config[4])
        self._db = self._client[self._config[3]]

    def get_db_obj(self):
        return self._db

    def get_client_obj(self):
        return self._client

    def close_connection(self):
        self._client.close()

    def insert_one(self, *args, **kwargs):
        topic = self.get_db_obj()[args[0]]
        result = None
        if len(kwargs) is 0:
            return None
        try:
            r = topic.insert_one(kwargs)
            result = r.inserted_ids
            self.logger.debug("insert_one -> result is %d" % result)
        except:
            self.logger.debug("insert_one have except")
            self.logger.debug("have except")
        finally:
            return result

    def insert_many(self, *args):
        topic = self.get_db_obj()[args[0]]
        result = False
        if len(args[1]) is 0:
            return result
        try:
            r = topic.insert_many(args[1])
            result = r.acknowledged
            self.logger.debug("insert_many -> result is {}, records are {}".format(result, len(r.inserted_ids)))
        except:
            self.logger.debug("insert_many have except")
            self.logger.debug("have except")
        finally:
            return result

    def fetch_collections(self, *args, **kwargs):
        """
        :param args: topic
        :return: array
        :sort: .sort("alexa"), .sort("alexa", -1)
        :condiftional:
            1. return special col, { "_id": 0, "name": 1, "alexa": 1 }
            2. search special col, { "name": "RUNOOB" }
            3. $gt, { "name": { "$gt": "H" } }
            4. $regex, { "name": { "$regex": "^R" } }
        """
        topic = self.get_db_obj()[args[0]]
        array_list = []
        if kwargs is not None:
            limit = kwargs.get("limit") if kwargs.get("limit") is not None else 1000
        try:
            if kwargs is None:
                result = topic.find().limit(limit)
                if isinstance(result, []) is not True:
                    array_list.append(result)
                for x in result:
                    self.logger.debug("fetch_collections -> one of data -> ", x)
            else:
                array_list = topic.find().limit(limit)
        except:
            self.logger.debug("fetch_collections have except")
            self.logger.debug("have except")
        finally:
            return array_list

    def update_many(self, *args, **kwargs):
        """
        :param args:  topic
        :param kwargs:  query and new
        :return:
        : conditional
            1. query: { "$get": { "alexa": "10000" } }
               new:   { "$set": { "$set": { "alexa": "12345" } } }
        """
        topic = self.get_db_obj()[args[0]]
        is_change = False
        try:
            # topic.update_one(kwargs["$get"], "$set")
            topic.update_many(kwargs["$get"], "$set")
            is_change = True
        except:
            is_change = False
            self.logger.debug("update_many have except")
            self.logger.debug("have except")
        finally:
            return is_change

    def delete_many(self, *args, **kwargs):
        """
        :param args:  topic
        :param kwargs:  query and new
        :return:
        : conditional
            1. query: { { "alexa": "10000" } }
        """
        topic = self.get_db_obj()[args[0]]
        is_delete = False
        try:
            # topic.update_one(kwargs["$get"], "$set")
            result = topic.delete_many(kwargs)
            self.logger.debug("delete_many -> result is %d" % result.deleted_count)
            is_delete = True
        except:
            is_delete = False
            self.logger.debug("delete_many have except")
            self.logger.debug("have except")
        finally:
            return is_delete

    def get_existing_one(self, *args, **kwargs):
        """
        :param args: topic
        :return: array
        :sort: .sort("alexa"), .sort("alexa", -1)
        :condiftional:
            1. return special col, { "_id": 0, "name": 1, "alexa": 1 }
            2. search special col, { "name": "RUNOOB" }
            3. $gt, { "name": { "$gt": "H" } }
            4. $regex, { "name": { "$regex": "^R" } }
        """
        topic = self.get_db_obj()[args[0]]
        result = None
        if kwargs is None:
            return result
        try:
            query = kwargs.get("query") if kwargs.get("query") is not None else ""
            result = topic.find_one(query, sort=[('update_datetime', -1)])
        except Exception as e:
            self.logger.debug("get_existing_one have except", e)
        finally:
            return result
