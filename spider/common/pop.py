import poplib
import sys
from importlib import reload
from email.parser import Parser
from email.parser import BytesParser
from email.header import decode_header
from email.utils import parseaddr
import email.iterators

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def savefile(filename, data, path):
    try:
        filepath = path + filename
        print('Save as: ' + filepath)
        f = open(filepath, 'wb')
    except:
        print(filepath + ' open failed')
    else:
        f.write(data)
    finally
        f.close()

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset

def print_info(msg):
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            else:
                hdr, addr = parseaddr(value)
                name = decode_str(addr)
                value = name + ' < ' + addr + ' > '
        print(header + ':' + value)
    for part in msg.walk():
        filename = part.get_filename()
        content_type = part.get_content_type()
        charset = guess_charset(part)
        if filename:
            filename = decode_str(filename)
            data = part.get_payload(decode = True)
            if filename != None or filename != '':
                print('Accessory: ' + filename)
                savefile(filename, data, mypath)
        else:
            email_content_type = ''
            content = ''
            if content_type == 'text/plain':
                email_content_type = 'text'
            elif content_type == 'text/html':
                email_content_type = 'html'
            if charset:
                content = part.get_payload(decode=True).decode(charset)
            print(email_content_type + ' ' + content)

email = 'email_name@163.com'
password = 'email_passwd'
pop3_server = 'pop.163.com'
mypath = 'D://email/'

server = poplib.POP3(pop3_server, 110)
server.user(email)
server.pass_(password)
print('Message: %s. Size: %s' % server.stat())

resp, mails, objects = server.list()

index = len(mails)

resp, lines, octets = server.retr(index)

lists = []
for e in lines:
    lists.append(e.decode())
msg_content = '\r\n'.join(lists)
msg = Parser().parsestr(msg_content)
print_info(msg)
#server.dele(index)
server.quit()

class POP3Customize(object):
    def __init__(self):
        self.pop3 = None
    def execute(self) -> POP3:
        if self.pop3:
            return self.pop3
        server = poplib.POP3(pop3_server, 110)
        server.user(email)
        server.pass_(password)
        return server
    
    def get_stat_of_mail(self):
        return self.pop3.list()

    def get_all_info_one_of_mail(self, index: int):
        assert type(index) == int and index > 0
        return self.pop3.retr(index)
    
    def quit(self):
        self.pop3.quit()
        self.pop3 = None