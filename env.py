# -*- coding: utf-8 -*-

import logging
import random
from fifo import FIFO
from alg import Algorithm

#logging.basicConfig(level=logging.DEBUG,
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(name)-11s %(levelname)-5s %(message)s',
    datefmt='%Y-%m-%d %H:%M')

def find_optimum(case, k):
    m = len(case)
    pfnum = 0
    store = [i + 1 for i in range(k)]

    for i, c in enumerate(case):
        if c not in store: # page fault
#            print store, c
            # if no repetition found, use any (let's say first) piece
            maxt = 0
            maxj = 0
            for j in range(k):
#                print "looking for", j, store[j]
                found = False
                for t in range(i+1, m):
                    if store[j] == case[t]:
#                        print "found %d at %d" % (case[t], t)
                        if maxt < t:
                            maxt = t
                            maxj = j
                        found = True
                        break

                # element not found in suffix, means we can freely use that space
                if not found:
                    maxj = j
                    maxt = m
                    break

#            print "maxt = %d, maxj = %d, piece = %d" % (maxt, maxj, store[maxj])

            store[maxj] = c

            pfnum += 1
    return pfnum

def run_test(algs, n=6, m=20, k=4):
    # n = külső tár mérete
    # m = kérések száma
    # k = belső tár mérete

    # generate the test case
    testcase = [random.randint(1, n) for _ in range(m)]

#    testcase = [1,2,2,4,5,2,2,4,5,1,2,4,3,1,4,5,1,4,6,1,2,1,4,5,6,3]
#    testcase = [2, 3, 5, 2, 5, 3, 6, 6, 4, 6, 3, 5, 6, 6, 1, 2, 3, 6, 2, 1]
#    m = len(testcase)

    optimum = find_optimum(testcase, k)
#    print testcase
#    print optimum
#    quit()

#    logging.debug("Using seed %d" % (seed))
    logging.debug("Using test case %s" % (", ".join([str(x) for x in testcase])))

    for alg in algs:
        logging.debug("Run alg=%s, n=%d, m=%d, k=%d" % (alg, n, m, k))

        state = [i + 1 for i in range(k)]
        pfnum = 0

        alg.init(n, k)

        for c in testcase:
            place = alg.request(c)
            if state[place] != c: # page fault
                logging.debug("Page fault detected, pos=%d, old=%d, new=%d" % (place, state[place], c))
                pfnum += 1
                state[place] = c

        if optimum != 0:
            C = float(pfnum) / optimum
        elif pfnum == 0:
            C = 1
        else:
            C = 1e30000
        print "%s: %d (C=%f)" % (alg, pfnum, C)
    print "OPT: %d" % (optimum)

def run_iteration(num, algs, n=6, m=20, k=4):
    for i in range(num):
        for alg in algs:
            run_test(algs, n, m, k)

#seed = 1234
#random.seed(seed)


fifo_alg = FIFO()
run_iteration(10, [fifo_alg])

