from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI

from subprocess import Popen, PIPE
from argparse import ArgumentParser
from monitor import monitor_qlen
from multiprocessing import Process

import sys
import os
import threading
from time import sleep, time

parser = ArgumentParser(description="Shallow queue tests")

parser.add_argument('--bw-net', '-b',
                    type=float,
                    help="Bandwidth of bottleneck (network) link (Mb/s)",
                    required=True)

parser.add_argument('--delay',
                    type=float,
                    help="Link propagation delay (ms)",
                    required=True)

parser.add_argument('--dir', '-d',
                    help="Directory to store outputs",
                    required=True)

parser.add_argument('--time', '-t',
                    help="Duration (sec) to run the experiment",
                   type=int,
                    default=10)

parser.add_argument('--maxq',
                    type=int,
                    help="Max buffer size of network interface in packets",
                    required=True)

parser.add_argument('--algo',
                    help="Algorithm under which we are running the simulation",
                    required=True) 


args = parser.parse_args()

class ShallowQueueTopo(Topo):
    '''
    Single switch connecting a sender and receiver with a small 
    queue
    '''
    def build(self, n=2):
        switch = self.addSwitch('s0')
        h1linkopts = {'bw':1000, 'delay': str(args.delay) + 'ms', 'use_htb':True}
        h2linkopts = {'bw':args.bw_net, 'delay': str(args.delay) + 'ms', 'use_htb':True, 
                      'max_queue_size':args.maxq}
        host1 = self.addHost('sender')
        host2 = self.addHost('receiver')
        self.addLink(host1, switch, **h1linkopts)
        self.addLink(host2, switch, **h2linkopts)
        

def RunPCC(net, algo):
    start_server(net)
    start_client(net, algo)

def RunCubic(net, algo):
    start_server(net)
    start_client(net, algo)

def RunBBR(net, algo):
    start_server(net)
    start_client(net, algo)

def simpleRun():
    print "Queue Size is %d" % args.maxq
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
    if not os.path.exists(args.dir + "/CUBIC"):
        os.makedirs(args.dir + "/CUBIC")
    if not os.path.exists(args.dir + "/PCC"):
        os.makedirs(args.dir + "/PCC")
    if not os.path.exists(args.dir + "/BBR"):
        os.makedirs(args.dir + "/BBR")


    if args.algo == 'cubic':
        os.system("sysctl -w net.ipv4.tcp_congestion_control=cubic")
    elif args.algo == 'bbr':
        os.system("sysctl -w net.ipv4.tcp_congestion_control=bbr")
    elif args.algo == 'pcc':
        os.system("sysctl -w net.ipv4.tcp_congestion_control=pcc")
 
    topo = ShallowQueueTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    if args.algo  == 'pcc':
        start_tcpprobe("cwnd.txt")
        qmon = start_qmon(iface='s0-eth2', outfile='%s/PCC/%s-q.txt' % (args.dir, str(args.maxq)))
        RunPCC(net,"pcc")
        qmon.terminate()
        stop_tcpprobe()

    elif args.algo == 'cubic':

        start_tcpprobe("cwnd.txt")
        qmon = start_qmon(iface='s0-eth2', outfile='%s/CUBIC/%s-q.txt' % (args.dir, str(args.maxq)))
        RunCubic(net, "cubic")
        qmon.terminate()
        stop_tcpprobe()

    elif args.algo == 'bbr':
        start_tcpprobe("cwnd.txt")
        qmon = start_qmon(iface='s0-eth2', outfile='%s/BBR/%s-q.txt' % (args.dir, str(args.maxq)))
        RunBBR(net, "bbr")
        qmon.terminate()
        stop_tcpprobe()
    net.stop()

# Probing for congestion window plots
def start_tcpprobe(outfile="cwnd.txt"):
    os.system("rmmod tcp_probe; modprobe tcp_probe full=1;")
    sleep(1)
    if args.algo == 'cubic':
        Popen("cat /proc/net/tcpprobe > %s/CUBIC/%s-%s" % (args.dir, str(args.maxq), outfile),
              shell=True)
    elif args.algo == 'bbr':
        Popen("cat /proc/net/tcpprobe > %s/BBR/%s-%s" % (args.dir, str(args.maxq), outfile),
              shell=True)
    elif args.algo == 'pcc':
        Popen("cat /proc/net/tcpprobe > %s/PCC/%s-%s" % (args.dir, str(args.maxq), outfile),
              shell=True)

def stop_tcpprobe():
    Popen("killall -9 cat", shell=True).wait()
                     
def start_qmon(iface, interval_sec=0.1, outfile="q.txt"):
    monitor = Process(target=monitor_qlen,
                      args=(iface, interval_sec, outfile))
    monitor.start()
    return monitor

def start_server(net):
    receiver = net.get('receiver')
    print("Starting server")
    receiver.popen('iperf -s -w 16m')
    print("Server started")
    sleep(1)

def start_client(net, algo):
    sender = net.get('sender')
    receiver = net.get('receiver')
    print("Starting client for " + str(args.time) + " seconds")
    if algo == "cubic":
        print("Running cubic iperf now")
        client = sender.cmd("iperf -c " + receiver.IP() + " -t " + str(args.time) + " > " + args.dir 
                              + "/CUBIC/" + str(args.maxq)  + ".log");
    elif algo == "pcc":
        print("Running pcc iperf now")
        client = sender.cmd("iperf -c " + receiver.IP() + " -t " + str(args.time) + " > " + args.dir 
                              + "/PCC/" + str(args.maxq)  + ".log")
    elif algo == "bbr":
        print("Running bbr iperf now")
        client = sender.cmd("iperf -c " + receiver.IP() + " -t " + str(args.time) + " > " + args.dir 
                              + "/BBR/" + str(args.maxq)  + ".log")
    sleep(args.time)
                
if __name__ == '__main__':
    simpleRun()
