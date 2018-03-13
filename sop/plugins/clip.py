# author: Matthias Dellweg
# (c) 2017

import logging
import pyperclip


def sop_plugin():
    return BarClip()


class BarClip:
    class Handler:
        def __init__(self, message):
            self.message = message

        def handle(self):
            pyperclip.copy(self.message)

        def msg(self):
            return "Copy barcode to clipboard."

    def __init__(self):
        logging.debug("Clipboard plugin activated")

    def get_handlers(self, message):
        return [self.Handler(message)]

    def handle(self, message):
        pyperclip.copy(message)
        return True
