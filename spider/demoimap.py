# https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/

import imaplib
mail = imaplib.IMAP4_SSL('imap.sina.cn')
mail.login('xxx@sina.cn', 'xxx')
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

# Getting all mail and fetching the latest
result, data = mail.search(None, "ALL")
ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
latest_email_id = id_list[-1] # get the latest
 
result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
 
raw_email = data[0][1] # here's the body, which is raw text of the whole email
# including headers and alternate payloads

# Using UIDs instead of volatile sequential ids
result, data = mail.uid('search', None, "ALL") # search and return uids instead
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]

# Parsing Raw Emails
import email
email_message = email.message_from_string(raw_email)
 
print(email_message['To'])
print(email.utils.parseaddr(email_message['From'])) # for parsing "Yuji Tomita" <yuji@grovemade.com>
print(email_message.items()) # print all headers
 
# note that if you want to get text content (body) and the email contains
# multiple payloads (plaintext/ html), you must parse each message separately.
# use something like the following: (taken from a stackoverflow post)
def get_first_text_block(self, email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

# Search any header
mail.uid('search', None, '(HEADER Subject "My Search Term")')
mail.uid('search', None, '(HEADER Received "localhost")')

# Search for emails since in the past day
import datetime
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))

# Limit by date, search for a subject, and exclude a sender
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
result, data = mail.uid('search', None, '(SENTSINCE {date} HEADER Subject "My Subject" NOT FROM "yuji@grovemade.com")'.format(date=date))

# Get Gmail thread ID
result, data = mail.uid('fetch', uid, '(X-GM-THRID X-GM-MSGID)')

# Get a header key only
result, data = mail.uid('fetch', uid, '(BODY[HEADER.FIELDS (DATE SUBJECT)]])')

# Fetch multiple
result, data = mail.uid('fetch', '1938,2398,2487', '(X-GM-THRID X-GM-MSGID)')

# Use a regex to parse fetch results
import re
result, data = mail.uid('fetch', uid, '(X-GM-THRID X-GM-MSGID)')
re.search('X-GM-THRID (?P<X-GM-THRID>\d+) X-GM-MSGID (?P<X-GM-MSGID>\d+)', data[0]).groupdict()
# this becomes an organizational lifesaver once you have many results returned.

