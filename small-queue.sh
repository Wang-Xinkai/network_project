#!/bin/bash                                                                                                                                       

#parameters for the mininet topology and test
time=60
bwnet=100                                           
delay=5
dir=buffer-size-test
iperf_port=5001

for qsize in 5 10 15 20 25 30 35 40 45 50 60 70 80 90 100 110 120 130 140 150 160 170 180 190 200 225 250 275 300 350 400 500; do
    # PCC and corresponding plots                                               
    python small-queue.py -b $bwnet -t $time --delay $delay  --maxq $qsize --dir $dir --algo pcc
    python plot_queue.py -f $dir/PCC/$qsize-q.txt -o $dir/PCC/$qsize-q.eps

    # TCP cubic and corresponding plots                                         
    python small-queue.py -b $bwnet -t $time --delay $delay  --maxq $qsize --dir $dir --algo cubic
    python plot_queue.py -f $dir/CUBIC/$qsize-q.txt -o $dir/CUBIC/$qsize-q.png

    #BBR and corresponding plots
    python small-queue.py -b $bwnet -t $time --delay $delay  --maxq $qsize --dir $dir --algo bbr
    python plot_queue.py -f $dir/PCC/$qsize-q.txt -o $dir/BBR/$qsize-q.png

done
#plot relation between buffer-size and throughput for different algorithm
python plot_throughputs.py
