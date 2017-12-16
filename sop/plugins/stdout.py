# author: Matthias Dellweg
# (c) 2017

import logging


def sop_plugin():
    return BarOut()


class BarOut:
    def __init__(self):
        logging.debug("Out aktiviert")

    def handle(self, message):
        print(message)
        return True
