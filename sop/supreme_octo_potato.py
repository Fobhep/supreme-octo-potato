# authors: Matthias Dellweg & Bernhard Hopfenmüller
# (c) 2017-2018

import importlib
import pkgutil
import subprocess
import sys
import os
import logging
import click
import re

import sop.plugins


def read_code(plugins):
    process = subprocess.Popen(['zbarcam', '/dev/video0'],
                               stdout=subprocess.PIPE)

    for output in iter(process.stdout.readline, b''):
        output_str_w_prefix = output.strip().decode("utf8")
        output_str = re.sub(r'^.*?:', '', output_str_w_prefix)
        handlers = []
        for plugin in plugins:
            handlers.extend(plugin.get_handlers(output_str))
        if len(handlers) > 0:
            process.kill()
            sys.stdout.write("\a")  # Beep
            choices = []
            for i, handler in enumerate(handlers):
                click.echo("{}\t{}".format(i, handler.msg()), err=True)
                choices.append(str(i))
            click.echo("q\tAbort", err=True)
            choices.append("q")
            choice = click.prompt("Choose an action", default="0", type=click.Choice(choices), err=True)
            if choice != "q":
                handlers[int(choice)].handle()
            break


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
