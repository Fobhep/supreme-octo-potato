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
    def __init__(self):
        self.matcher = re.compile(self.match_pattern)
        #logging.debug("QrWifi aktiviert")

    def handle(self, message):
        print (message)
        match = self.matcher.match(message)
        if match:
            fingerprint = match.group('fingerprint')
            gpg = gnupg.GPG()
            gpg_dict = gpg.search_keys(fingerprint)
            if
            #passphrase = match.group('passphrase')
            #subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', passphrase])
            return True
        return False
