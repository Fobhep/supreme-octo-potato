# author: Matthias Dellweg
# (c) 2017

import re
import logging
import sys
import subprocess
import pyperclip


def sop_plugin():
    return QrWifi()


class QrWifi:
    match_pattern = r"WIFI:S:(?P<ssid>[^;]*);T:(?P<type>[^;]*);P:(?P<passphrase>[^;]{0,63});;"

    class CopyHandler:
        def __init__(self, ssid, passphrase):
            self.ssid = ssid
            self.passphrase = passphrase

        def handle(self):
            pyperclip.copy(self.passphrase)

        def msg(self):
            return "Copy passphrase for wifi {} to clipboard.".format(self.ssid)

    class ConnectHandler:
        def __init__(self, ssid, passphrase):
            self.ssid = ssid
            self.passphrase = passphrase

        def handle(self):
            subprocess.run(['nmcli', 'device', 'wifi', 'connect', self.ssid, 'password', self.passphrase])

        def msg(self):
            return "Connect to wifi {}.".format(self.ssid)

    def __init__(self):
        self.matcher = re.compile(self.match_pattern)
        logging.debug("QrWifi aktiviert")

    def get_handlers(self, message):
        match = self.matcher.match(message)
        if match:
            ssid = match.group('ssid')
            passphrase = match.group('passphrase')
            return [self.CopyHandler(ssid, passphrase), self.ConnectHandler(ssid, passphrase)]
        return []
