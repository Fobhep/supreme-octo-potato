# author: Bernhard Hopfenmüller
# (c) 2017

import re
import logging
import sys
import subprocess
import gnupg


def sop_plugin():
    return QrPGP()

class QrPGP:
    match_pattern = r"QR-Code:OPENPGP4FPR:(?P<fingerprint>[0-9A-Fa-f]{40})"

    class Handler():
        def __init__(self, fingerprint):
            self.fingerprint = fingerprint

        def handle(self):
            gpg = gnupg.GPG()
            gpg_dict = gpg.search_keys(self.fingerprint)

        def msg(self):
            return "Download the corresponding GPG key."

    def __init__(self):
        self.matcher = re.compile(self.match_pattern)
        logging.debug("Downloading Gpg key")

    def get_handlers(self, message):
        match = self.matcher.match(message)
        if match:
            fingerprint = match.group('fingerprint')
            return [self.Handler(fingerprint)]
        return []

