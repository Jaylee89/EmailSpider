from spider.common.util import Util

from spider.common.model.mail import Mail

class Convert:
    def __init__(self):
        pass

    def NeteaseToMail(self, mail):
        _id = mail.get("id")
        _from = mail.get("from")
        subject = mail.get("subject")
        sent_date = Util.stringToDate4Netease(mail.get("sentDate"))
        to = mail.get("to")
        received_date = Util.stringToDate4Netease(mail.get("receivedDate"))
        return Mail(_id, _from, to, subject, sent_date, received_date)