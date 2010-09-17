# -*- coding: utf-8 -*-

import logging
import random
from fifo import FIFO
from lru import LRU
from incstats import IncrementalStats

LOGFILE="run.log"

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

    result = []

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

#        if optimum != 0:
#            C = float(pfnum) / optimum
#        elif pfnum == 0:
#            C = 1
#        else:
#            C = 1e30000

        assert pfnum >= optimum

        result.append(pfnum)

#        print "%s: %d (C=%f)" % (alg, pfnum, C)
#    print "OPT: %d" % (optimum)

    result.append(optimum)
    return result

def run_iteration(num, algs, n=6, m=20, k=4):

    results = []

    alglen = len(algs)
    alg_stats = [IncrementalStats() for _ in range(alglen)]

    for i in range(num):

        for alg in algs:
            run = run_test(algs, n, m, k)
            opt = run[len(run)-1]
            if opt != 0:
                for a in range(len(run)-1):
                    C = 1.0 * run[a] / opt
                    alg_stats[a].add(C)
                    run += [alg_stats[a].avg(), alg_stats[a].min, alg_stats[a].max]
            results.append(run)
#            print results
#            print avg(results, 0)
#            quit()

    write_plot(LOGFILE, results, algs)

def write_plot(filename, results, algs):
    with open(filename, "w") as f:
        print >>f, "num", " ".join([x.__str__() for x in algs] + ["OPT"])
        for num, run in enumerate(results):
            print >>f, num+1, " ".join([str(x) for x in run])

#seed = 1234
#random.seed(seed)


fifo_alg = FIFO()
lru_alg = LRU()
run_iteration(100, [fifo_alg, lru_alg], 10, 100, 4)

