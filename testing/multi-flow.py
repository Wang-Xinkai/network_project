from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

from subprocess import Popen, PIPE
from argparse import ArgumentParser 

import sys
import os
import threading
from time import sleep, time

parser = ArgumentParser(description="Multiflow tests")

parser.add_argument('--bw-outer', '-B',
                    type=float,
                    help="Bandwidth of host links (Mb/s)",
                    default=1000)

parser.add_argument('--bw-inner', '-b',
                    type=float,
                    help="Bandwidth of bottleneck (network) link (Mb/s)",
                    default=100)

parser.add_argument('--delay-outer',
                    type=float,
                    help="Link propagation delay (ms)",
                    default=1)

parser.add_argument('--delay-inner',
                    type=float,
                    help="Link propagation delay (ms)",
                    default=13)

parser.add_argument('--dir', '-d',
                    help="Directory to store outputs",
                    default='logs_new')

parser.add_argument('--flow-time', '-t',
                    help="Duration of each flow",
                    type=int,
                    default=2000)

parser.add_argument('--offset',
                    help="Offset of the beginning of the next flow",
                    type=int,
                    default=500)

parser.add_argument('--maxq',
                    type=int,
                    help="Max buffer size of network interface in packets",
                    default=250)

parser.add_argument('--num-hosts',
                    type=int,
                    help="Number of hosts in the system",
                    default=4)
parser.add_argument('--algo',
                    help="Algorithm under which we are running the simulation",
                    required=True) 
args = parser.parse_args()

class MultiFlowTopo(Topo):
    def build(self):
        switch1 = self.addSwitch('switch1')
        switch2 = self.addSwitch('switch2')
        local_link_opts = {'bw':args.bw_outer, 'delay':str(args.delay_outer) + 'ms', 'use_htb':True}
        bottle_link_opts = {'bw':args.bw_inner, 'delay':str(args.delay_inner) + 'ms', 'use_htb':True, 'max_queue_size':args.maxq}

        for i in range(args.num_hosts):
            sender = self.addHost('s%s' % (i + 1))
            self.addLink(sender, switch1, **local_link_opts)

            receiver = self.addHost('r%s' % (i +1))
            self.addLink(receiver, switch2, **local_link_opts)
 
        self.addLink(switch1, switch2, **bottle_link_opts)
       
def launch_CUBIC_flow(sender, receiver, i):
    print("launching cubic flow")
    server = receiver.popen("iperf -s")
    client = sender.popen("iperf -c " + receiver.IP() +  " -i 1 -t "+ str(args.flow_time) +  "  > "+
                           args.dir + "/cubic_monitor_" + str(i) +".log", shell=True);

def launch_BBR_flow(sender, receiver, i):
    print("launching bbr flow")
    server = receiver.popen("iperf -s")
    client = sender.popen("iperf -c " + receiver.IP() +  " -i 1 -t "+ str(args.flow_time) +  "  > "+
                           args.dir + "/bbr_monitor_" + str(i) +".log", shell=True);

def launch_PCC_flow(sender, receiver, i):
    print("launching pcc flow")
    server = receiver.popen("iperf -s")
    client = sender.popen("iperf -c " + receiver.IP() +  " -i 1 -t "+ str(args.flow_time) +  "  > "+
                           args.dir + "/pcc_monitor_" + str(i) +".log", shell=True);
    
def multi_flow():
    topo = MultiFlowTopo()
    print("topo made")
    if not os.path.exists(args.dir):
        os.makedirs('logs_new')
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    dumpNodeConnections(net.switches)
    for i in range(args.num_hosts):
        sender_name = 's%s' % (i+1)
        receiver_name = 'r%s' % (i+1)
        if args.algo == 'cubic':
            print("cubic sending round" +str(i+1))
            launch_CUBIC_flow(net.getNodeByName(sender_name),net.getNodeByName(receiver_name), i)
        elif args.algo == 'bbr':
            print("bbr sending round" +str(i+1))
            launch_BBR_flow(net.getNodeByName(sender_name),net.getNodeByName(receiver_name), i)
        elif args.algo == 'pcc':
            print("pcc sending round" +str(i+1))
            launch_PCC_flow(net.getNodeByName(sender_name),net.getNodeByName(receiver_name), i)
        
        sleep(args.offset)

    sleep(args.flow_time - args.offset)
    net.stop()
    
if __name__ == "__main__":
    multi_flow()
    
