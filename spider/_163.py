#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
import re
import json
import urllib3
import traceback

from spider.common.util import Util

from spider.common.model.mail import MailSuper
from spider.common.model.response import Response
from spider.common.model.convert import Convert

from spider.common.database.nosqldb import NoSql

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MAIL163(MailSuper):
    def __init__(self, logger, is_mock, username, password):
        self.logger = logger
        self.is_mock = is_mock
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.sid = None

    def login(self):
        if self.is_mock:
            self.sid = "mock data"
            return
        loginUrl = "https://mail.163.com/entry/cgi/ntesdoor?style=-1&df=mail163_letter&net=&language=-1&from=web&race=&iframe=1&product=mail163&funcid=loginone&passtype=1&allssl=true&url2=https://mail.163.com/errorpage/error163.htm"
        headers = {
            'Referer': "https://mail.163.com/",
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
        }

        postData = {
            'savelogin': "0",
            'url2': "http://mail.163.com/errorpage/error163.htm",
            'username': self.username,
            'password': self.password
        }

        response = self.session.post(loginUrl, headers=headers, data=postData, verify=False)
        pattern = re.compile(r'sid=(.*?)&', re.S)
        # need to catch exception as logon failed
        self.sid = re.search(pattern, response.text).group(1)

    def loadMessageList(self):
        listUrl = 'https://mail.163.com/js6/s?sid=%s&func=mbox:listMessages' % self.sid
        Headers = {
            'Accept': "text/javascript",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "mail.163.com",
            'Referer': "https://mail.163.com/js6/main.jsp?sid=%s&df=mail163_letter" % self.sid,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
        }

        response_data = Response()
        if not self.is_mock:
            response = self.session.post(listUrl, headers=Headers, verify=False)
            response.raise_for_status()

            # pattern = re.compile("id..'(.*?)',.*?from..'(.*?)',.*?to..'(.*?)',.*?subject..'(.*?)',.*?sentDate..(.*?),\n.*?receivedDate..(.*?),.*?hmid..(.*?),\n", re.S)
            # mails = re.findall(pattern, response.text)
            # for mail in mails:
            #     mid = mail[0]
            #     print('-' * 45)
            #     print('id:', mid)
            #     print('发件人:', mail[1], '主题:', mail[3], '发送时间:', mail[4])
            #     print('收件人:', mail[2], u'接收时间:', mail[5])
            #     self.message(mid)

            response_data = self.parse_response_data(response.text)
        else:
            json_data = Util.load_json(parent_path = "mock", sufix = ".txt", file_name = "Netease")
            response_data = self.parse_response_data(json_data)
        if response_data.status:
            convert = Convert()
            mail_list = []
            for mail in response_data.mails:
                mail_list.append(convert.NeteaseToMail(mail))
            self.operate_database(mail_list)

    def message(self, mid):
        Headers = {
            'Accept': "text/javascript",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "mail.163.com",
            'Referer': "https://mail.163.com/js6/main.jsp?sid=%s&df=mail163_letter" % self.sid,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
        }

        cookie = {
            'Coremail.sid': self.sid,
        }

        url = 'https://mail.163.com/js6/read/readhtml.jsp?mid=%s&userType=ud&font=15&color=064977' % mid
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookie)
        response = self.session.get(url, headers=Headers, verify=False)

        self.logger.debug(response.text)

    def parse_response_data(self, text):
        response_object = Response()
        response_json_string = text
        if self.is_mock:
            response_json_string = text.replace("\\n", "").replace("\"", "").replace('\\\'', "\"").replace("new Date(", "\"").replace("),", "\",")
        else:
            response_json_string = text.replace("\n", "").replace("\"", "").replace('\'', "\"").replace("new Date(", "\"").replace("),", "\",")
        mail_object = json.loads(response_json_string)
        response_object.status = mail_object.get("code") == "S_OK"
        mails = mail_object.get("var") or []
        mails.reverse()
        response_object.mails = mails
        return response_object

    def operate_database(self, mails):
        if len(mails) == 0:
            return
        nosql_client_insert = NoSql(self.logger)
        nosql_client_fetch = NoSql(self.logger)
        insert_script = []

        has_reproduce = False
        for mail in mails:
            if has_reproduce:
                break
            query = { "hashcode": { "$eq": ("%s" % mail.hashcode) } }
            try:
                retult = nosql_client_fetch.get_existing_one("mails", query=query)
                if retult:
                    has_reproduce = True
                    continue
                insert_script.append(mail.get_mongo_sql_script())
                insert_data_count = len(insert_script)
                if insert_data_count % 100 == 0:
                    nosql_client_insert.insert_many("mails", insert_script)
                    insert_script = []
                    self.logger.debug("insert {} records to database".format(insert_data_count))
            except Exception as e:
                self.logger.debug("Error: ", e)
                traceback.print_exc()

        remail_insert_count = len(insert_script)
        if remail_insert_count != 0:
            try:
                result = nosql_client_insert.insert_many("mails", insert_script)
                self.logger.debug("result is {}, insert remain {} records to database".format(result, remail_insert_count))
            except Exception as e:
                self.logger.debug("remain insert data, Error: ", e)
                traceback.print_exc()
        nosql_client_insert.close_connection()
        nosql_client_fetch.close_connection()

    def execute(self):
        self.login()
        self.loadMessageList()
