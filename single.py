#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sys import argv
from env import run_test
from fifo import FIFO
from lru import LRU


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO,
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(name)-11s %(levelname)-5s %(message)s',
        datefmt='%Y-%m-%d %H:%M')

    if len(argv) < 4:
        print "usage: single.py N M K"
        exit(1)
    try:
        n = int(argv[1])
        m = int(argv[2])
        k = int(argv[3])
    except:
        logging.critical("Invalid argument.")
        exit(2)

    assert n > 0 and m > 0 and k > 0

    fifo_alg = FIFO()
    lru_alg = LRU()
    algs = [fifo_alg, lru_alg]

    run_test(algs, n, m, k)
