#!/usr/bin/env python3
# authors: Matthias Dellweg & Bernhard Hopfenmüller
# (c) 2017

import importlib
import pkgutil
import subprocess
import sys
import os
import logging
import click

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


def load_plugins(plugin_name=None):
    sop_plugin_names = [
        name
        for finder, name, ispkg
        in pkgutil.iter_modules(sop.plugins.__path__, sop.plugins.__name__ + '.')
        if plugin_name is None or name.endswith('.' + plugin_name)
    ]
    sop_plugins = []
    for name in sop_plugin_names:
        try:
            sop_plugins.append(importlib.import_module(name).sop_plugin())
            logging.info("Successfully loaded plugin {}.".format(name))
        except ImportError as e:
            logging.warn("Failed to load plugin {}.\n{}".format(name, e))
    return sop_plugins


@click.command()
@click.option('-p', '--plugin', help='Select the plugin to use')
def main(plugin):
    sop_plugins = load_plugins(plugin_name=plugin)
    if len(sop_plugins) == 0:
        logging.warn("No plugins loaded!")
        return 1
    read_code(sop_plugins)
    return 0


if __name__ == "__main__":
    sys.exit(main())
