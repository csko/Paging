# -*- coding: utf-8 -*-

import logging
import random
from fifo import FIFO
from lru import LRU
from incstats import IncrementalStats

def find_optimum(case, k):
    """Computes the optimal offline paging cost using a naive method"""

    logging.debug("Finding optimum.")

    m = len(case)
    pfnum = 0
    store = [i + 1 for i in range(k)]

    for i, c in enumerate(case):
        logging.debug("State: %s" % store)
        logging.debug("Requesting piece %d." % c)
        if c not in store: # page fault, we need to replace a block
            logging.debug("Piece not found, page fault.")
            # if no repetition found, use any (let's say first) piece
            maxt = 0
            maxj = 0
            for j in range(k):
                found = False
                for t in range(i+1, m):
                    # found repetition
                    if store[j] == case[t]:
                        # is it the farthest known?
                        if maxt < t:
                            maxt = t
                            maxj = j
                        found = True
                        break

                # No element has been found in suffix, means we can freely use that space
                if not found:
                    logging.debug("No piece %d found in suffix, we can freely drop that piece, which we will do." % store[j])
                    maxj = j
                    maxt = m
                    break

            logging.debug("Piece %d comes up again the latest, in position %d. We are going to drop it." % (store[maxj], maxt+1))
            store[maxj] = c

            pfnum += 1
        else:
            logging.debug("Piece found.")
    return pfnum

def run_test(algs, n=6, m=20, k=4):
    """Runs a single test on all of the algorithms."""
    # n = external storage size
    # m = number of requests
    # k = internal storage size

    # generate the test case
    testcase = [random.randint(1, n) for _ in range(m)]

#    testcase = [1,2,2,4,5,2,2,4,5,1,2,4,3,1,4,5,1,4,6,1,2,1,4,5,6,3]
#    testcase = [2, 3, 5, 2, 5, 3, 6, 6, 4, 6, 3, 5, 6, 6, 1, 2, 3, 6, 2, 1]
#    m = len(testcase)

    logging.debug("Using test case [%s]" % (", ".join([str(x) for x in testcase])))

    optimum = find_optimum(testcase, k)

    logging.debug("Optimum is %d." % (optimum))

    result = []

    for alg in algs:
        logging.debug("Running algorithm %s with parameters n=%d, m=%d, k=%d" % (alg, n, m, k))

        state = [i + 1 for i in range(k)]
        pfnum = 0

        alg.init(n, k)

        for c in testcase:
            logging.debug("State: %s" % state)
            logging.debug("Requesting piece %d." % c)
            place = alg.request(c)
            if state[place] != c: # page fault
                logging.debug("Page fault detected, pos=%d, old=%d, new=%d" % (place, state[place], c))
                pfnum += 1
                state[place] = c
            else:
                logging.debug("Piece found.")
        logging.debug("END STATE: %s" % state)

        assert pfnum >= optimum

        result.append(pfnum)
        logging.debug("[%s] Number of page faults: %d" % (alg, pfnum))

    result.append(optimum)
    return result

def run_iteration(num, algs, n=6, m=20, k=4):
    """Runs a number of simulations and aggregates the results."""

    results = []

    alglen = len(algs)
    alg_stats = [IncrementalStats() for _ in range(alglen)]

    i = 0
    while i < num:
        run = run_test(algs, n, m, k)
        opt = run[alglen]

        # we don't consider cases where there are no page faults
        if opt != 0:
            i += 1
        else:
            continue

        for a in range(alglen):
            C = 1.0 * run[a] / opt
            alg_stats[a].add(C)
            run += [alg_stats[a].avg(), alg_stats[a].min, alg_stats[a].max]
        results.append(run)

    return results

def write_plot(filename, results, algs):
    with open(filename, "w") as f:
        print >>f, "num", " ".join([x.__str__() for x in algs] + ["OPT"])
        for num, run in enumerate(results):
            print >>f, num+1, " ".join([str(x) for x in run])



#LOGFILE="run.log"

#results = run_iteration(10000, algs, 5, 20, 4)
#print results[len(results)-1]
#write_plot(LOGFILE, results, algs)

def write_3dplot(filename, kmax, nmax, m, algs, runs=10):
    alglen = len(algs)
    with open(filename, "w") as f:

        # header
        print >>f, "k n m",
        print >>f, " ".join([" ".join(("%s_avg" % x, "%s_min" % x, "%s_max" % x)) for x in algs])

        # rows
        for k in range(2, kmax + 1):
            for n in range(k + 1, nmax + 1):

                results = run_iteration(runs, algs, n, m, k)

                assert len(results) > 0

                # we're only interested in the end result this time
                endresult = results[len(results) - 1]

                print >>f, k, n, m,
                print >>f, " ".join([str(endresult[i]) for i in range(alglen+1, len(endresult))])
            f.flush()

if __name__ == "__main__":

    fifo_alg = FIFO()
    lru_alg = LRU()
    algs = [fifo_alg, lru_alg]

    #logging.basicConfig(level=logging.DEBUG,
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s %(name)-11s %(levelname)-5s %(message)s',
        datefmt='%Y-%m-%d %H:%M')

    LOGTARGET="runs/run_%03d.txt"

    for m in range(3, 100 + 1):
        write_3dplot(LOGTARGET % m, 100, 100, m, algs, 100)
        print m

#LOGFILE2="run3d.log"
#write_3dplot(LOGFILE2, 10, 10, 20, algs, 100000)
