# network_project

This is the project of CS339 Computer Network. It contains three parts:
+ PCC-Kernel-Module
+ Shallow-Buffer Test
+ Multi-Flow Test

## Installation
To install the pcc module and essential components. Make sure that your Linux kernel $\ge$ 4.10(for bbr module) and $\le$ 4.15(for tcp_probe module). 
### Install PCC Module
Installation of PCC module is easy. Just execute the **install_pcc.sh** in your shell and pcc will appear as a congestition protocol in your system. You can use '''{r, engine='bash', count_lines} 
sysctl net.ipv4.tcp_available_congestion_control
''' and you can see pcc(together with cubic and bbr).
