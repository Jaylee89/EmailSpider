#!/usr/bin/env python3

# import logging

from spider import EmailSpider

# logging.basicConfig(format="%(asctime)s, %(msecs)d,  %(message)s",
#                     datefmt="%d-%m-%Y:%H:%M:%S",
#                     level=logging.DEBUG)

# logger = logging.getLogger("mail")
EmailSpider().execute()
# logger.debug("Completed!")