#!/usr/bin/gnuplot

set terminal png giant size 1024,768
#set terminal postscript eps enhanced color solid
set output "stats.png"

#set size 5/5., 4/3.
#set format xy "$%g$"
#set yrange [0.80:0.89]
#set xrange [0:6287]

set size ratio 0.6
set logscale x
set title "FIFO, LRU stats"
set ylabel "C = online / OPT"
set xlabel "Number of runs"
#set encoding iso_8859_2

plot    "run.log" using 1:5 with lines title 'avg(FIFO)', \
        "run.log" using 1:6 with lines title 'min(FIFO)', \
        "run.log" using 1:7 with lines title 'max(FIFO)', \
        "run.log" using 1:8 with lines title 'avg(LRU)', \
        "run.log" using 1:9 with lines title 'min(LRU)', \
        "run.log" using 1:10 with lines title 'max(LRU)'
