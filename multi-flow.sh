#!/bin/bash

offset=500
bw_inner=100
bw_outer=1000
num_hosts=4
flow_time=2000
dir=multi-flow-test

sysctl -w net.ipv4.tcp_congestion_control=cubic
python multi-flow.py -B $bw_outer -b $bw_inner --offset $offset --num-hosts $num_hosts -d $dir --flow-time $flow_time --algo cubic

sysctl -w net.ipv4.tcp_congestion_control=pcc
python multi-flow.py -B $bw_outer -b $bw_inner --offset $offset --num-hosts $num_hosts -d $dir --flow-time $flow_time --algo pcc

sysctl -w net.ipv4.tcp_congestion_control=bbr
python multi-flow.py -B $bw_outer -b $bw_inner --offset $offset --num-hosts $num_hosts -d $dir --flow-time $flow_time --algo bbr

python multi-flow-plot.py --num-hosts $num_hosts -d $dir --offset $offset --flow-time $flow_time
