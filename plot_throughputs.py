import os
#some help functions
from helper import *

rootdir = 'buffer-size-test'
#plot pcc line
def plot_pcc_throughputs(ax):
    pcc_queue_sizes = []
    pcc_throughputs = []

    for i in os.listdir(rootdir + '/PCC'):
        if i.endswith(".log"):
            f = open(rootdir + '/PCC/' + i, 'r')
            
            throughput = gather_info(f)
            f.close()
            pcc_throughputs.append(throughput)
            file_names = i.split('.')
            pcc_queue_sizes.append(int(file_names[0]) * 1.5 )

    together = sorted(zip(pcc_queue_sizes, pcc_throughputs))
    qsize_sort = zip(*together)[0]
    tput_sort = zip(*together)[1]
           

    ax.plot(qsize_sort, tput_sort, label='PCC')
#plot bbr line
def plot_bbr_throughputs(ax):
    bbr_queue_sizes = []
    bbr_throughputs = []

    for i in os.listdir(rootdir + '/BBR'):
        if i.endswith(".log"):
            f = open(rootdir + '/BBR/' + i, 'r')
            
            throughput = gather_info(f)
            f.close()
            bbr_throughputs.append(throughput)
            file_names = i.split('.')
            bbr_queue_sizes.append(int(file_names[0]) * 1.5 )

    together = sorted(zip(bbr_queue_sizes, bbr_throughputs))
    qsize_sort = zip(*together)[0]
    tput_sort = zip(*together)[1]
           

    ax.plot(qsize_sort, tput_sort, label='BBR')
#plot cubic line
def plot_cubic_throughputs(ax):
    cubic_queue_sizes = []
    cubic_throughputs = []

    for i in os.listdir(rootdir + '/CUBIC'):
        if i.endswith(".log"):
            f = open(rootdir + '/CUBIC/' + i, 'r')
            
            throughput = gather_info(f)
            f.close()
            cubic_throughputs.append(throughput)
            file_names = i.split('.')
            cubic_queue_sizes.append(int(file_names[0]) * 1.5 )

    together = sorted(zip(cubic_queue_sizes, cubic_throughputs))
    qsize_sort = zip(*together)[0]
    tput_sort = zip(*together)[1]
           

    ax.plot(qsize_sort, tput_sort, label='TCP CUBIC')
#function for plot
def gather_info(f):
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    necessary_line = f.readline()

    return float(necessary_line[34:39])
    
m.rc('figure', figsize=(16, 6))

fig = plt.figure(figsize=[8, 6])
plots = 1

axPlot = fig.add_subplot(1, plots, 1)
plot_pcc_throughputs(axPlot)
plot_cubic_throughputs(axPlot)
plot_bbr_throughputs(axPlot)
plt.legend(loc='lower right')
axPlot.set_xlabel("Buffer size (KB)")
axPlot.set_ylabel("Throughput (Mbps)")

plt.title('Shallow buffered Comparison')
plt.savefig("Results/Pics/Shallow_Buffer.png")
