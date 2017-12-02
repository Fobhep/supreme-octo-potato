# author: Matthias Dellweg
# (c) 2017

import re
import logging
import sys
import subprocess

def sop_plugin():
    return QrWifi()


class QrWifi:
    match_pattern = r"QR-Code:WIFI:S:(?P<ssid>[^;]*);T:(?P<type>[^;]*);P:(?P<passphrase>[^;]{0,63});;"

    def __init__(self):
        self.matcher = re.compile(self.match_pattern)
        logging.debug("QrWifi aktiviert")

    def handle(self, message):
        match = self.matcher.match(message)
        if match:
            ssid = match.group('ssid')
            passphrase = match.group('passphrase')
            subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', passphrase])
            return True
        return False

