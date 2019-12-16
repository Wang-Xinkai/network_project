#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

time=200
bwnet=1.5
# TODO: If you want the RTT to be 20ms what should the delay on each
# link be?  Set this value correctly.
delay=5

iperf_port=5001

for qsize in 20 30 100; do
    dir=bb-q$qsize

    # TODO: Run bufferbloat.py here...
    python bufferbloat.py -B 1000 -b $bwnet --delay $delay -d $dir -t $time --maxq $qsize
    # TODO: Ensure the input file names match the ones you use in
    # bufferbloat.py script.  Also ensure the plot file names match
    # the required naming convention when submitting your tarball.
    python plot_tcpprobe.py -f $dir/cwnd.txt -o $dir/cwnd-iperf.png -p $iperf_port
    python plot_queue.py -f $dir/q.txt -o $dir/q.png
#    python plot_ping.py -f $dir/ping.txt -o $dir/rtt.png
done

