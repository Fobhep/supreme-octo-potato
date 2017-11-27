#!/bin/env/python3
# authors: Matthias Dellweg & Bernhard Hopfenmüller
# (c) 2017

import subprocess
import re

qr_wifi_match_pattern = r"QR-Code:WIFI:S:(?P<ssid>[^;]*);T:(?P<type>[^;]*);P:(?P<passphrase>[^;]{0,63});;"


def read_code():
    process = subprocess.Popen(['zbarcam', '/dev/video1'],
                               stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_str = output.strip().decode("utf8")
            match = re.match(qr_wifi_match_pattern, output_str)
            if match:
                process.kill()
                subprocess.Popen(["echo" ,'-n' ,'\a'])
                return match.group('ssid'), match.group('passphrase')
        rc = process.poll()

if __name__ == "__main__":
    ssid,passphrase = read_code()
    subprocess.run(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', passphrase])
