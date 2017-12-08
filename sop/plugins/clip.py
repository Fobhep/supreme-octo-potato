# author: Matthias Dellweg
# (c) 2017

import logging
import pyperclip


def sop_plugin():
    return BarClip()


class BarClip:
    def __init__(self):
        logging.debug("Clip aktiviert")

    def handle(self, message):
        pyperclip.copy(message)
        return True
