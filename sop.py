#!/usr/bin/env python3
# authors: Matthias Dellweg & Bernhard Hopfenmüller
# (c) 2017

import importlib
import pkgutil
import subprocess
import sys
import os

import sop.plugins


def read_code(plugins):
    process = subprocess.Popen(['zbarcam', '/dev/video0'],
                               stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_str = output.strip().decode("utf8")
            for plugin in plugins:
                if plugin.handle(output_str):
                    process.kill()
                    sys.stdout.write("\a")  # Beep
                    return
        rc = process.poll()

if __name__ == "__main__":
    sop_plugins = [
        importlib.import_module(name).sop_plugin()
        for finder, name, ispkg
        in pkgutil.iter_modules(sop.plugins.__path__, sop.plugins.__name__ + '.')
    ]

    read_code(sop_plugins)
    sys.exit(0)
