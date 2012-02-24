Online Paging problem
=====================
This is a student project for simulating solutions for the
[online paging problem](http://en.wikipedia.org/wiki/Page_replacement_algorithm). Also contains an implementation of the optimal offline algorithm for approximating the competitive ratio. The two algorithms are:

* [Least Recently Used (LRU)](http://en.wikipedia.org/wiki/Page_replacement_algorithm#Least_recently_used)
* [First In, First Out (FIFO)](http://en.wikipedia.org/wiki/Page_replacement_algorithm#First-in.2C_first-out)


Example usage
============
* ``
  ./single.py 5 20 3
``

    A single run of both algorithms with 5 pages, 20 input pages, and internal storage size 3.

* ``./average.py 1000 200 100 50``

    Calculates the average over 50 tries for 1000 pages, 200 input pages, and internal storage size 100.


* ``./env.py``

    Runs extensive simulations over many parameters.

Contents
========
* ``doc/``

  Documentation in PDF format. Also includes the source in LyX and LaTeX.

* ``alg.py``

  Base class for algorithms.

* ``lru.py``

  Implementation of the LRU algorithm.

* ``fifo.py``

  Implementation of the FIFO algorithm.

* ``incstats.py``

  Class for calculating average incrementally.

* ``env.py``

  General environment for running tests. Contains the optimal offline solution implementation.

* ``single.py``

  Script for calculating a single run.

* ``average.py``

  Script for calculating average over runs.

* ``stats.gp``

  gnuplot script for plotting the results of ``env.py``.



Documentation
=============

Some additional documentation is provided in the doc/ directory,
however, most of it's in Hungarian.


