# -*- coding: utf-8 -*-

import logging
from alg import Algorithm

logger = logging.getLogger('lru')

class LRU(Algorithm):
    def init(self, n, k):
        self.k = k
        self.store = [i + 1 for i in range(k)]
        self.usage = [i for i in range(k)]
#        logger.debug(self.store)
#        logger.debug(self.usage)

        # round counter
        self.round = k - 1

        self.lastpos = 0

    def find(self, piece):
        try:
            pos = self.store.index(piece)
            return pos
        except ValueError:
            return -1

    def request(self, piece):

        self.round += 1

        pos = self.find(piece)

#        logger.debug(piece)
#        logger.debug(self.store)
#        logger.debug(self.usage)
        if pos == -1: # piece not found, page fault
            # find the least recently used slot:
            minpos = -1
            mintime = self.round

            for i, j in enumerate(self.usage):
                if j < mintime: # found a new minimum
                    minpos = i
                    mintime = j

            self.store[minpos] = piece
            self.usage[minpos] = self.round
            return minpos
        else: # piece found
            # actualize last used time for this piece
            self.usage[pos] = self.round
            return pos

    def __str__(self):
        return "LRU"
