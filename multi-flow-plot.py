import matplotlib
matplotlib.use('Agg') # To avoid needing to ssh -X
import matplotlib.pyplot as plt

from argparse import ArgumentParser

parser = ArgumentParser(description="Multiflow tests")

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

parser.add_argument('--num-hosts',
                    type=int,
                    help="Number of hosts in th system",
                    default=4)

args = parser.parse_args()

def parse_iperf_log(logfilename):
    tps = []
    with open(logfilename) as f:
        lines = f.readlines()
        for line in lines[6:6 + args.flow_time]:
            tpstr = line.split()[6]
            if not tpstr[0].isdigit():
                tpstr = line.split()[7]
            tps.append(float(tpstr)) 
    return tps 

def plot_pcc_multi_flow(labels):
    offset = args.offset 
    fnames = [args.dir + '/pcc_monitor_' + str(i)+'.log' for i in range(args.num_hosts)]
    for i, name in enumerate(fnames):
        tp = parse_iperf_log(name)
        start = offset*i
        times = [t for t in range(start, start + len(tp))]
        plt.plot(times, tp, label=labels[i],lw = 0.5)

def plot_cubic_multi_flow(labels):
    offset = args.offset 
    fnames = [args.dir + '/cubic_monitor_' + str(i)+'.log' for i in range(args.num_hosts)]
    for i, name in enumerate(fnames):
        tp = parse_iperf_log(name)
        start = offset*i
        times = [t for t in range(start, start + len(tp))]
        plt.plot(times, tp, label=labels[i], lw=0.5)

def plot_bbr_multi_flow(labels):
    offset = args.offset 
    fnames = [args.dir + '/bbr_monitor_' + str(i)+'.log' for i in range(args.num_hosts)]
    for i, name in enumerate(fnames):
        tp = parse_iperf_log(name)
        start = offset*i
        times = [t for t in range(start, start + len(tp))]
        plt.plot(times, tp, label=labels[i],lw = 0.5)



def main():
    labels = []
    fig = plt.figure(figsize=[8, 6])
    for i in range(args.num_hosts):
        labels.append('Flow ' +  str(i+1))
    plot_pcc_multi_flow(labels)
    plt.legend(loc='upper center')
    plt.xlabel('Time (s)')
    plt.ylabel('Throughput (Mbps)')
    plt.title('PCC Multi-Flow ')
    plt.savefig('pccmulti.png')
    plt.clf()
    fig = plt.figure(figsize=[8, 6])
    plot_cubic_multi_flow(labels)
    plt.legend(loc='upper center')
    plt.xlabel('Time (s)')
    plt.title('CUBIC Multi-Flow')
    plt.ylabel('Throughput (Mbps)')
    plt.savefig('cubicmulti.png')
    plt.clf()
    fig = plt.figure(figsize=[8, 6])
    plot_bbr_multi_flow(labels)
    plt.legend(loc='upper center')
    plt.xlabel('Time (s)')
    plt.title('BBR Multi-Flow')
    plt.ylabel('Throughput (Mbps)')
    plt.savefig('bbrmulti.png')



if __name__ == "__main__":
    main()



