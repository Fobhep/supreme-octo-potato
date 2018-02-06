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


def get_plugin_names():
    sop_plugin_names = [
        name
        for finder, name, ispkg
        in pkgutil.iter_modules(sop.plugins.__path__, sop.plugins.__name__ + '.')
    ]
    return sop_plugin_names


def load_plugins(plugin_names):
    sop_plugins = []
    for name in plugin_names:
        try:
            sop_plugins.append(importlib.import_module(name).sop_plugin())
            logging.info("Successfully loaded plugin {}.".format(name))
        except ImportError as e:
            logging.warn("Failed to load plugin {}.\n{}".format(name, e))
    return sop_plugins


@click.command()
@click.option('-p', '--plugin', help='Select the plugin to use')
@click.option('-l', '--list-plugins', help='List available plugins', is_flag=True)
def main(list_plugins, plugin):
    plugin_names = get_plugin_names()
    if list_plugins:
        click.echo("Available plugins:")
        for name in plugin_names:
            click.echo("\t" + name.split('.')[-1])
        return 0
    if plugin:
        plugin_names = [name for name in plugin_names if name.endswith('.' + plugin)]
    sop_plugins = load_plugins(plugin_names)
    if len(sop_plugins) == 0:
        logging.warn("No plugins loaded!")
        return 1
    read_code(sop_plugins)
    return 0


if __name__ == "__main__":
    sys.exit(main())
