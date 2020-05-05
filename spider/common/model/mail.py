import hashlib
import time

class SHA(object):
    def __init__(self):
        self.__hash = hashlib.sha512()

    def getSha512(self, name):
        self.__hash.update(name.encode('utf-8'))
        return self.__hash.hexdigest()

class MailSuper(object):
    def __init__(self):
        pass

    def parse_response_data(self, json_load):
        pass

class Mail(object):
    def __init__(self, mail_id, _from, to, subject, sent_datetime, received_datetime, content = ""):
        self.mail_id = mail_id
        self._from = _from
        self.to = to
        self.subject = subject
        self.sent_datetime = sent_datetime
        self.received_datetime = received_datetime
        self.content = content
        self.hashcode = self.get_hashcode()
        self.update_datetime = time.strftime("%Y-%m-%d", time.localtime())

    def get_hashcode(self):
        return SHA().getSha512("{}-{}-{}-{}-{}-{}".format(self._from, self.to, self.subject, self.content, self.sent_datetime, self.received_datetime))

    def get_mysql_script(self):
        return """INSERT INTO mail(mail_id, from, to, subject, sent_datetime, received_datetime, hashcode, content) \
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(self.mail_id, self._from, self.to, self.subject, self.sent_datetime, self.received_datetime, self.hashcode, self.content)

    def get_mongo_sql_script(self):
        return {
            "mail_id": self.mail_id,
            "from": self._from,
            "to": self.to,
            "subject": self.subject,
            "sent_datetime": self.sent_datetime,
            "received_datetime": self.received_datetime,
            "hashcode": self.hashcode,
            "content": self.content,
            "update_datetime": self.update_datetime
        }