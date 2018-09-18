# author: Matthias Dellweg
# (c) 2017

import re
import logging
import sys
import subprocess


def sop_plugin():
    return QrUrl()


class QrUrl:
    match_pattern = r"https?://.*"

    class Handler:
        def __init__(self, message):
            self.message = message

        def handle(self):
            subprocess.run(['sensible-browser', self.message])

        def msg(self):
            return "Open barcode in web-browser. ('{}')".format(self.message)

    def __init__(self):
        self.matcher = re.compile(self.match_pattern)
        logging.debug("Url plugin activated")

    def get_handlers(self, message):
        match = self.matcher.match(message)
        if match:
            return [self.Handler(message)]
        return []

    def handle(self, message):
        match = self.matcher.match(message)
        if match:
            subprocess.run(['sensible-browser', message])
            return True
        return False
