# author: Matthias Dellweg
# (c) 2017

import logging


def sop_plugin():
    return BarOut()


class BarOut:
    class Handler:
        def __init__(self, message):
            self.message = message

        def handle(self):
            print(self.message)

        def msg(self):
            return "Print barcode to stdout."

    def __init__(self):
        logging.debug("Output plugin activated")

    def get_handlers(self, message):
        return [self.Handler(message)]
