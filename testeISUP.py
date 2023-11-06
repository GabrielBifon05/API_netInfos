from __future__ import print_function

import socket
import psutil
from psutil._common import bytes2human

teste = psutil.net_if_stats()


stats = psutil.net_if_stats()
io_counters = psutil.net_io_counters(pernic=True)
for nic, addrs in psutil.net_if_addrs().items():
        print("%s:" % (nic))
        if nic in stats:
            st = stats[nic]
            print("    stats          : ", end='')
            print("speed=%sMB, mtu=%s, up=%s" % (
                st.speed, st.mtu,
                "yes" if st.isup else "no"))

# print("up=%s" % ("yes" if teste[nic].isup else "no"))


