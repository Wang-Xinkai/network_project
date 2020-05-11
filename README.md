# Network Project

This project is reproduction of [PCC-Vivace](https://www.usenix.org/conference/nsdi18/presentation/dong). It uses online learning to better network congestion control. 

## Project Structure

`start.sh` is the script to install essential dependency for compliing module and testing.

`install_pcc.sh` is the script to install pcc module into Linux system. 

`PCC_module` is source code of PCC-vivace implementation.

`testing` is the test code for PCC module in buffer-size and multi-flow.

`Results` is the results of our experiments.

## Implementation Overview

### Code

All PCC code resides under `PCC_modulesrc/tcp_pcc.c`
Code is compatible with the [conventions](https://www.kernel.org/doc/html/v4.10/process/coding-style.html) of the Linux kernel
#### Congestion Hooks

The Linux kernel allows creating "modular" CAs.
This is achieved by a set of hooks which must or can be implemented by the CA module.
For the complete set of hooks - see `struct tcp_congestion_ops` definition in the Linux kernel.
PCC uses the main hook `cong_control` introduced by BBR.

The hook has two purposes in regard to the current PCC implementation:

+ A periodic hook which is called on each ack - allowing us to "slice" intervals.
+ A hook, that on each ack, reports "acks" and "losses" of sent packets - allowing us to accumulate statistics for "Monitor Intervals" (MIs) and eventually calculate utility.
The entire PCC logic resides in the following hook, under the `pcc_main` function.
#### Utility calculation

At the moment the utility from the paper is being used.

The utility is calculated using a variation of fixedptc.h.

Noticed that the sigmoid is calculated as follows `1/(1+e^x)`.
If x is very big (> 21) we might overflow.
A check is placed in order to avoid this situation.

Alternatively, the sigmoid can be calculated as `e^-x/(1+e^-x)` avoiding this.
This was the previous implementation by Mo and Tomer - and should be returned.
#### Congestion windows

The PCC article does not specify anything regarding the congestion window size.

This is natural since PCC does not limit its throughput using the congestion window (cwnd) like cubic does, but rather employs pacing.

Still, a cwnd must be given - since the cwnd value limits the number of packets in flight.

We use a similar implementation as BBR - just set cwnd to twice the pacing rate in packets: `cwnd = 2 * rate * rtt / mss` - this value is updated upon every ack and should guarantee that pacing is not limited by the cwnd on one hand and that the cwnd is not too big on the other hand.

This logic was not tested thoroughly - but rather used as "common sense".

See this discussion for more information:

https://groups.google.com/forum/#!topic/bbr-dev/bC-8XoQB7pQ

#### Edge cases

The PCC article does not specify cases where the rates are close to zero or maxint.

When rates are close to zero - rate changes, which are epsilon away from each other, don't change significantly, resulting in irrelevant measurements. In order to overcome this - we use a minimal step of 4K bytes.

This number was not tested thoroughly - but rather used as "common sense".
