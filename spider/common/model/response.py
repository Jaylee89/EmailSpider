from spider.common.model.mail import Mail

class Response(object):
    def __init__(self, status = False, mails: [Mail] = []):
        self.status = status
        self.mails = mails