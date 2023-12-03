# ---------------------------- CRAWLER ---------------------------- 
codigoServidor = input("Insira o código deste servidor:")


while True:
    from urllib.request import urlopen
    from datetime import datetime

    try:
        import requests
        ip_address = requests.get('https://api.ipify.org').text
        print(f'IP Público: {ip_address}')

        if ip_address:
            url = f"http://ip-api.com/json/{ip_address}?fields=1821"

            request = urlopen(url)
            data = request.read().decode()

            data = eval(data)
            # DATA é um "json", dict é o nome
            estado = (list(data.values())[1]) # Estado (sigla)
            cidade = (list(data.values())[3]) # Cidade

    except Exception as ex:
        print(f"Error: {ex}")

    from bs4 import BeautifulSoup

    busca =f"A Previsão do tempo em {cidade} é de "
    url = f"https://www.google.com/search?q={busca}"
    r = requests.get(url)
    s= BeautifulSoup(r.text, "html.parser")
    valorTemperatura = s.find("div",class_="BNeawe").text
    valorTemperatura = valorTemperatura[0:2]
    print(f"Temperatura: {valorTemperatura}")


    # ------------------ PSUTIL (mac_address, IP, upload, download, dataRecv, dataSent) -------------------

    import speedtest

    st = speedtest.Speedtest()

    vel_download = st.download() / 10**6
    vel_upload = st.upload() / 10**6
    ping = st.results.ping

    print(f'  |Velocidade de download: {vel_download:.2f} Mbps|')
    print(f'  |Velocidade de upload: {vel_upload:.2f} Mbps|')
    print(f'  |Ping: {ping:.2f}|')
    print("----------------------------------------")



    # ------------------ PSUTIL (mac_address, IP, upload, download, dataRecv, dataSent) -------------------
    import psutil
    import time
    import os
    import mysql.connector

    mydb = mysql.connector.connect(
        host = "localhost",
        user = "aluno",
        password = "sptech",
        port = 3306,
        database = "ScriptGCT"
    )

    mycursor = mydb.cursor()

    # mycursor.execute("CREATE TABLE IF NOT EXISTS temperatura(id_temperatura INT PRIMARY KEY AUTO_INCREMENT NOT NULL, valor_temperatura DECIMAL(4,2), data_registro DATETIME, fk_servidor INT NOT NULL, FOREIGN KEY (fk_servidor) REFERENCES servidor (id_servidor));")

    # mycursor.execute("CREATE TABLE IF NOT EXISTS rede(id_rede INT PRIMARY KEY AUTO_INCREMENT NOT NULL,  mac_address VARCHAR(100), ip_publico VARCHAR(100), vel_upload DECIMAL(4,2), vel_download DECIMAL(4,2), ping DECIMAL(4,2), uploadStat DECIMAL(5,2), downloadStat DECIMAL(5,2), dataSent DECIMAL(5,2), dataRecv DECIMAL(5,2), data_registro DATETIME, fk_servidor INT NOT NULL, FOREIGN KEY (fk_servidor) REFERENCES servidor (id_servidor));")

    size = ['bytes', 'KB', 'MB', 'GB', 'TB']
    def getSize(bytes):
        for unit in size:
            if bytes < 1024:
                return f"{bytes:.1f}"
            bytes /= 1024

    netStats1 = psutil.net_io_counters()
    stats = psutil.net_if_stats()

    dataSent = netStats1.bytes_sent
    dataRecv = netStats1.bytes_recv


    addresses = psutil.net_if_addrs()

    import fcntl
    import socket
    import struct


    def getHwAddr(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
        return ':'.join('%02x' % b for b in info[18:24])

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

    print("Upload", getSize(uploadStat)) #KB
    print("Download", getSize(downloadStat)) #KB

    print("Data Sent", getSize(dataSent)) #MB
    print("Data Recive", getSize(dataRecv)) #MB
    print(st.speed)

    dataHoraNow = datetime.now()    


    mycursor.execute(f"INSERT INTO rede (mac_address, ip_publico, vel_upload, vel_download, ping, uploadStat, downloadStat, dataSent, dataRecv, data_registro, codigo) VALUES ('{mac_address}', '{ip_address}',, {vel_upload:.2f}, {vel_download:.2f}, {ping:.2f}, {getSize(uploadStat)}, {getSize(downloadStat)}, {getSize(dataSent)}, {getSize(dataRecv)}, '{dataHoraNow}', {codigoServidor});")
    mydb.commit()
    print(mycursor.rowcount, "rede inserted.")

    mycursor.execute(f"INSERT INTO temperatura (valor_temperatura, data_registro, codigo) VALUES ('{valorTemperatura}', '{dataHoraNow}', {codigoServidor});")
    mydb.commit()
    print(mycursor.rowcount, "temperatura inserted.")