#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sys import argv
from env import run_iteration2
from fifo import FIFO
from lru import LRU


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
    #logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)-11s %(levelname)-5s %(message)s',
        datefmt='%Y-%m-%d %H:%M')

    if len(argv) < 5:
        print "usage: single.py N M K TRIES"
        exit(1)
    try:
        n = int(argv[1])
        m = int(argv[2])
        k = int(argv[3])
        tries = int(argv[4])
    except:
        logging.critical("Invalid argument.")
        exit(2)

    assert n > 0 and m > 0 and k > 0 and tries > 0

    fifo_alg = FIFO()
    lru_alg = LRU()
    algs = [fifo_alg, lru_alg]

    x = run_iteration2(10, algs, n, m, k)
    for i in x:
        logging.info("FIFO: %d (C=%f), LRU: %d (C=%f), OPT: %d" % (i[0], 1.0*i[0] / i[2], i[1], 1.0*i[1] / i[2], i[2]))
