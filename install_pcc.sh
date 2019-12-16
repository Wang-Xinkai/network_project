cd PCC_module/PCC-Vivace-Latency/src
sudo modprobe tcp_bbr
make
sudo insmod tcp_pcc.ko
cd ../../..