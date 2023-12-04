# ---------------------------- JIRA ---------------------------- 

from jira import JIRA
from datetime import datetime
import speedtest
import psutil
import time
import os
import fcntl
import socket
import struct
import mysql.connector
import json

jira_token = "ATATT3xFfGF0UmWAi-LW5-Bx1_c9B-sQs5GV_f-eKkA6clUdYwh-r0hlBKeRg2EJQZ9d9YtVZbf4UsWfopgvkj8nBdiHjX_9vM_ZnBg2zmOnFLA-mH_Ri_efGg-QjKJFnSdZwDfem7vP3LDi8nDIiQG1GE3QEDrEN8tZZ8_xeWUVIm_VuGEgKJo=6345AAD2"
url = "https://greycloudtransactions.atlassian.net/rest/api/2/search"
server_name = "https://greycloudtransactions.atlassian.net"
email = 'GrayCloudTransactions@hotmail.com'

jira_connection = JIRA(
    basic_auth=(email, jira_token),
    server=server_name
)

# ---------------------------- CRAWLER ---------------------------- 
codigoServidor = input("Insira o código deste servidor:")


while True:
    from urllib.request import urlopen

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


    # ------------------ SpeedTest (vel_download, vel_upload, ping) -------------------


    st = speedtest.Speedtest()

    vel_download = st.download() / 10**6
    vel_upload = st.upload() / 10**6
    ping = st.results.ping

    print(f'  |Velocidade de download: {vel_download:.2f} Mbps|')
    print(f'  |Velocidade de upload: {vel_upload:.2f} Mbps|')
    print(f'  |Ping: {ping:.2f}|')
    print("----------------------------------------")



    # ------------------ PSUTIL (mac_address, IP, upload, download, dataRecv, dataSent) -------------------
    

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
# ------------------ Alertas no JIRA/Slack -------------------

    if(vel_download < 100 ):
        mensagemVel_download = {"text": f"""
            ⚙️ === ALERTA❗️
            Descrição => Envio de pacotes está sobrecarregando!
            """}
    chatMonitoramentoVel_download = "https://hooks.slack.com/services/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"
    postMsgVel_download = requests.post(chatMonitoramentoVel_download, data=json.dumps(mensagemVel_download))

    issue_dict = {
            'project': {'key': 'SUP'},
            'summary': f"Rede com velocidade de download abaixo de {vel_download:.2f} Mbps!!!",
            'description': f'A rede do servidor {codigoServidor} está  velocidade de download abaixo de {vel_download:.2f} Mbps!!!',
            'issuetype': {"id":"10022"},
        }
    new_issue = jira_connection.create_issue(fields=issue_dict)

    if(vel_upload < 100 ):
        mensagemVel_upload = {"text": f"""
            ⚙️ === ALERTA❗️
            Descrição => Envio de pacotes está sobrecarregando!
            """}
    chatMonitoramentoVel_upload = "https://hooks.slack.com/services/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"
    postMsgVel_upload = requests.post(chatMonitoramentoVel_upload, data=json.dumps(mensagemVel_upload))

    issue_dict = {
            'project': {'key': 'SUP'},
            'summary': f"Rede com velocidade de upload abaixo de {vel_upload:.2f} Mbps!!!",
            'description': f'A rede do servidor {codigoServidor} está  velocidade de upload abaixo de {vel_upload:.2f} Mbps!!!',
            'issuetype': {"id":"10022"},
        }
    new_issue = jira_connection.create_issue(fields=issue_dict)

    if(ping > 50 ):
        mensagemPing = {"text": f"""
            ⚙️ === ALERTA❗️
            Descrição => Envio de pacotes está sobrecarregando!
            """}
    chatMonitoramentoPing = "https://hooks.slack.com/services/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"
    postMsgPing = requests.post(chatMonitoramentoPing, data=json.dumps(mensagemPing))

    issue_dict = {
            'project': {'key': 'SUP'},
            'summary': f"Rede com ping acima de {ping:.2f}!!!",
            'description': f'A rede do servidor {codigoServidor} está com ping acima de {ping:.2f}!!!',
            'issuetype': {"id":"10022"},
        }
    new_issue = jira_connection.create_issue(fields=issue_dict)

    if(getSize(uploadStat) > 70 ):
        mensagemUploadStat = {"text": f"""
            ⚙️ === ALERTA❗️
            Descrição => Envio de pacotes está sobrecarregando!
            """}
    chatMonitoramentoUploadStat = "https://hooks.slack.com/services/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"
    postMsgUploadStat = requests.post(chatMonitoramentoUploadStat, data=json.dumps(mensagemUploadStat))
    
    issue_dict = {
            'project': {'key': 'SUP'},
            'summary': f"Rede com estado de upload acima de {getSize(uploadStat)}!!!",
            'description': f'A rede do servidor {codigoServidor} está estado de upload acima de {getSize(uploadStat)}!!!',
            'issuetype': {"id":"10022"},
        }
    new_issue = jira_connection.create_issue(fields=issue_dict)

    if(getSize(downloadStat) > 70 ):
        mensagemDownloadStat = {"text": f"""
            ⚙️ === ALERTA❗️
            Descrição => Estado de download está sobrecarregando!
            """}
    chatMonitoramentoDownloadStat = "https://hooks.slack.com/services/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"
    postMsgDownloadStat = requests.post(chatMonitoramentoDownloadStat, data=json.dumps(mensagemDownloadStat))
    
    issue_dict = {
            'project': {'key': 'SUP'},
            'summary': f"Rede com estado de download acima de {getSize(downloadStat)}!!!",
            'description': f'A rede do servidor {codigoServidor} está estado de download acima de {getSize(downloadStat)}!!!',
            'issuetype': {"id":"10022"},
        }
    new_issue = jira_connection.create_issue(fields=issue_dict)

    if(getSize(dataSent) > 200 ):
        mensagemDataSent = {"text": f"""
            ⚙️ === ALERTA❗️
            Descrição => Recebimento de pacotes está sobrecarregando!
            """}
    chatMonitoramentoDataSent = "https://hooks.slack.com/services/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"
    postMsgDataSent = requests.post(chatMonitoramentoDataSent, data=json.dumps(mensagemDataSent))
    
    issue_dict = {
            'project': {'key': 'SUP'},
            'summary': f"Rede com envio de pacotes acima de {getSize(dataSent)}!!!",
            'description': f'A rede do servidor {codigoServidor} está envio de pacotes acima de {getSize(dataSent)}!!!',
            'issuetype': {"id":"10022"},
        }
    new_issue = jira_connection.create_issue(fields=issue_dict)

    if(getSize(dataRecv) > 100 ):
        mensagemDataRecv = {"text": f"""
            ⚙️ === ALERTA❗️
            Descrição => Envio de pacotes está sobrecarregando!
            """}
    chatMonitoramentoDataRecv = "https://hooks.slack.com/services/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"
    postMsgDataRecv = requests.post(chatMonitoramentoDataRecv, data=json.dumps(mensagemDataRecv))
    
    issue_dict = {
            'project': {'key': 'SUP'},
            'summary': f"Rede com recebimento de pacotes acima de {getSize(dataRecv)}!!!",
            'description': f'A rede do servidor {codigoServidor} está recebimento de pacotes acima de {getSize(dataRecv)}!!!',
            'issuetype': {"id":"10022"},
        }
    new_issue = jira_connection.create_issue(fields=issue_dict)

# ------------------ Inserindo no BD -------------------

    # mycursor.execute(f"INSERT INTO rede (mac_address, ip_publico, vel_upload, vel_download, ping, uploadStat, downloadStat, dataSent, dataRecv, data_registro, codigo) VALUES ('{mac_address}', '{ip_address}',, {vel_upload:.2f}, {vel_download:.2f}, {ping:.2f}, {getSize(uploadStat)}, {getSize(downloadStat)}, {getSize(dataSent)}, {getSize(dataRecv)}, '{dataHoraNow}', {codigoServidor});")
    # mydb.commit()
    # print(mycursor.rowcount, "rede inserted.")

    # mycursor.execute(f"INSERT INTO temperatura (valor_temperatura, data_registro, codigo) VALUES ('{valorTemperatura}', '{dataHoraNow}', {codigoServidor});")
    # mydb.commit()
    # print(mycursor.rowcount, "temperatura inserted.")