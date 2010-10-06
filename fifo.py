# -*- coding: utf-8 -*-

import logging
from alg import Algorithm

logger = logging.getLogger('fifo')


class FIFO(Algorithm):
    def init(self, n, k):
        self.k = k
        self.store = [i + 1 for i in range(k)]
#        logger.debug("INITIAL STORE: %s" % self.store)

        self.lastpos = 0

    def find(self, piece):
        try:
            pos = self.store.index(piece)
            return pos
        except ValueError:
            return -1

    def request(self, piece):
        pos = self.find(piece)

#        logger.debug(piece)
#        logger.debug(self.store)
        if pos == -1: # piece not found, page fault
            # FIFO behavior, changing the i%k -th  element in round i
            drop = self.lastpos
            self.store[drop] = piece
            self.lastpos += 1
            self.lastpos %= self.k
            return drop
        else: # piece found
            return pos

    def __str__(self):
        return "FIFO"
