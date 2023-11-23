import psutil
import time
import os
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "aluno",
    password = "sptech",
    port = 3306,
    database = "testeAPI"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS registro(id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,  mac_address VARCHAR(100), speed INT, mtu DECIMAL(5,2)," 
                 "isup VARCHAR(3), uploadStat DECIMAL(5,2), downloadStat DECIMAL(5,2), dataSent DECIMAL(5,2), dataRecv DECIMAL(5,2))")

size = ['bytes', 'KB', 'MB', 'GB', 'TB']
def getSize(bytes):
    for unit in size:
        if bytes < 1024:
            return f"{bytes:.1f}"
        bytes /= 1024

# netStats1 = psutil.net_io_counters()
# stats = psutil.net_if_stats()

# dataSent = netStats1.bytes_sent
# dataRecv = netStats1.bytes_recv


# addresses = psutil.net_if_addrs()

import fcntl
import socket
import struct


def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])

while True:
    netStats1 = psutil.net_io_counters()
    dataSent = netStats1.bytes_sent
    dataRecv = netStats1.bytes_recv
    addresses = psutil.net_if_addrs()
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    time.sleep(1)
    os.system("clear")

    

    for name in addresses:
        try:
            mac_address = getHwAddr(name)
        except:
            mac_address = "No mac_address found"
    print("mac address = ", mac_address)

    for nic, addrs in psutil.net_if_addrs().items():
            print("%s:" % (nic))
            if nic in stats:
                st = stats[nic]
                print("    stats          : ", end='')
                print("speed=%sMB, mtu=%s, up=%s" % (
                    st.speed, st.mtu,
                    "yes" if st.isup else "no"))
    print("\n")
    print("-"*30)
    print("\n")
    netStats2 = psutil.net_io_counters()
    
    uploadStat = netStats2.bytes_sent - dataSent
    downloadStat = netStats2.bytes_recv - dataRecv
    
    
    totalDataSent = netStats2.bytes_sent
    totalDataRecv = netStats2.bytes_recv

    # print("Upload", getSize(uploadStat)) #KB
    # print("Download", getSize(downloadStat)) #KB
    print("Data Sent", getSize(dataSent)) #MB
    print("Data Recive", getSize(dataRecv)) #MB
    print(st.speed)
    # mycursor.execute(f"INSERT INTO registro (mac_address, dataSent, dataRecv) VALUES"
    #              f"('{mac_address}', {getSize(dataSent)}, {getSize(dataRecv)})")
    # mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    