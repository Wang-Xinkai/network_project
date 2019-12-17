# network_project



This is the project of CS339 Computer Network. It contains three parts:

+  PCC-Kernel-Module

+  Shallow-Buffer Test

+  Multi-Flow Test



## Installation

To install the pcc module and essential components. Make sure that your Linux kernel $\ge$ 4.10(for bbr module) and $\le$ 4.15(for tcp_probe module). 

### Install PCC Module

Installation of PCC module is easy. Just enter the `network_project` and type in  `sudo ./install_pcc.sh` in your shell and pcc will appear as a congestition protocol in your system. You can use `sysctl net.ipv4.tcp_available_congestion_control`  and you can see pcc(together with cubic and bbr). 

### Install Essential Components 

To install mininet and matlotlib for test and plot, you can enter the `network_project` and type in `sudo ./start.sh` in your shell and essential components will be fine. To know more about mininet, you can go to [mininet](http://mininet.org) to get more information. To know more about matplotlib, you can go to [matplotlib](https://matplotlib.org) to get more Information. 

## PCC Kernel Module

### PCC Usage

Now you can use `pcc` as a congestion algorithm:

```java
import socket

TCP_CONGESTION = getattr(socket, 'TCP_CONGESTION', 13)

s = socket.socket()
s.setsockopt(socket.IPPROTO_TCP, TCP_CONGESTION, 'pcc')

# Use of pcc algorithm
```

### Implementation Overview

### Code

All PCC code resides under `PCC_module/src/tcp_pcc.c`

Code is compatible with the [conventions](https://www.kernel.org/doc/html/v4.10/process/coding-style.html) of the Linux kernel



### Congestion Hooks

The Linux kernel allows creating "modular" CAs.

This is achieved by a set of hooks which must or can be implemented by the CA module.

For the complete set of hooks - see `struct tcp_congestion_ops` definition in the Linux kernel.

PCC uses the main hook `cong_control` introduced by BBR.

The hook has two purposes in regard to the current PCC implementation:

- A periodic hook which is called on each ack - allowing us to "slice" intervals.
- A hook, that on each ack, reports "acks" and "losses" of sent packets - allowing us to accumulate statistics for "Monitor Intervals" (MIs) and eventually calculate utility.

The entire PCC logic resides in the following hook, under the `pcc_main` function.



### Utility calculation

At the moment the utility from the paper is being used.

The utility is calculated using a variation of `fixedptc.h`.

Noticed that the sigmoid is calculated as follows `1/(1+e^x)`.

If `x` is very big (> 21) we might overflow.

A check is placed in order to avoid this situation.

Alternatively, the sigmoid can be calculated as `e^-x/(1+e^-x)` avoiding this.

This was the previous implementation by Mo and Tomer - and should be returned.



### Congestion windows

The PCC article does not specify anything regarding the congestion window size.

This is natural since PCC does not limit its throughput using the congestion window (cwnd) like cubic does, but rather employs pacing.

Still, a cwnd must be given - since the cwnd value limits the number of packets in flight.

We use a similar implementation as BBR - just set cwnd to twice the pacing rate in packets: `cwnd = 2 * rate * rtt / mss` - this value is updated upon every ack and should guarantee that pacing is not limited by the cwnd on one hand and that the cwnd is not too big on the other hand.

This logic was not tested thoroughly - but rather used as "common sense".



### Edge cases

The PCC article does not specify cases where the rates are close to zero or maxint.

When rates are close to zero - rate changes, which are epsilon away from each other, don't change significantly, resulting in irrelevant measurements. In order to overcome this - we use a minimal step of 4K bytes.

This number was not tested thoroughly - but rather used as "common sense".



## Shallow Buffer Test

### Network Topology

In the test we use mininet to establish our network environment for the lack of Emulab. The topology of the test network is h1-s0-h2 and the parameters of the link can be modified. 

### Usage

To run our test, you can use `small-queue.sh` to execute **iperf** test for different buffer size and different congestion control algorithm (cubic, bbr, pcc). The results are in `Results/buffer-size-test/` and the figure is in the `Results/Pics/`.



## Multi-Flow Test

### Network Topology

The network topology is as same as above.

### Usage

To run this test, you can use `multi-flow.sh` to execute **iperf** test of 4 flows for different congestion control algorithm (cubic, bbr, pcc). The results are in `Results/multi-flow-test/` and the figures are in the `Results/Pics/`.

