import poplib
poplib._MAXLINE=20480
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
    finally:
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
    for header in ['From', 'To', 'Subject', 'Received']:
        value = msg.get(header, '')
        if value and (decode_str(value) if type(value) == bytes else value) != '"':
            if header == 'Subject':
                try:
                    result = decode_str(value)
                    if type(result) == bytes:
                        raise Exception("subject analyze issue")
                    value = result
                except Exception as e:
                    print("subject analyze issue")
                # print(value)
            elif header == 'Received':
                value = value[-36:]
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
            # if filename != None or filename != '':
                # print('Accessory: ' + filename)
                # savefile(filename, data, mypath)
        else:
            email_content_type = ''
            content = ''
            if content_type == 'text/plain':
                email_content_type = 'text'
            elif content_type == 'text/html':
                email_content_type = 'html'
            if charset:
                content = part.get_payload(decode=True).decode(charset)
            # print(email_content_type + ' ' + content)

if __name__ == "__main__":

    email = '18182428724@sina.cn'
    password = 'jal891012'
    pop3_server = 'pop.sina.cn'
    mypath = 'D://email/'

    # 163, sina
    server = poplib.POP3(pop3_server)
    # QQ
    # server = poplib.POP3(pop3_server, 995)
    

    server.set_debuglevel(1)

    print(server.getwelcome())
    server.user(email)
    server.pass_(password)
    print('Message: %s. Size: %s' % server.stat())

    resp0, mails0, octets0 = server.list()
    print(resp0)
    print(mails0)
    print(octets0)
    #print(mails)
    index = len(mails0)
    for i in range(1, index):
        resp, lines, octets = server.retr(i)
        lists = []
        # index_of_lines = 0
        for e in lines:
            # index_of_lines += 1
            # if index_of_lines > 35:
            #     break
            rs = e.decode()
            # print(rs)
            lists.append(rs)
        msg_content = '\r\n'.join(lists)
        msg = Parser().parsestr(msg_content)
        print_info(msg)
        #server.dele(index)
    server.quit()