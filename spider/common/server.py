class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def get_host(self):
        return self.host
    def get_port(self):
        return self.port

class MailType(object):
    def __init__(self):
        pass