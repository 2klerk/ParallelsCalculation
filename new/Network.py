import platform
import subprocess
import re
import socket
# import keyboard
import threading
from Brute import Brute
import pickle


class Network:
    def __init__(self):
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.port = "8080"
        self.OS = platform.system()  # Операционная система
        self.addr = []  # Все адреса в локальной сети
        self.bots = {}  # Список ботов в ботнете и статус получения данных
        self.server = ""  # Для клиента ip сервера
        self.Action = ""

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
            # print(self.addr)

    # перед работой сделать udp запросы по адресам, которые есть в self.addr
    def FindBots(self):
        for i in self.addr:
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = {"Id": None, "Action": "Auth"}
            dest_address = (i, int(self.port))
            udp.sendto(pickle.dumps(message), dest_address)

    def SendBot(self, bot, data):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        dest_address = (bot, int(self.port))
        udp.sendto(data, dest_address)

    def GetAcceptBot(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind(('0.0.0.0', int(self.port)))
        server_socket.settimeout(3)
        while True:
            try:
                data, addr = server_socket.recvfrom(1024)
                message = pickle.loads(data)
                if addr[0] not in self.bots and message == True:
                    self.bots[addr[0]] = {"Status": False, "Data": None}
                    print("Получено сообщение от {0}: {1}".format(addr, message))
            except socket.timeout:
                print("Таймаут - больше нет сообщений")
                break

    def __Info(self):
        return "#########Choice#########\n" \
               "#(1)   CHECK IN LAN (1)#\n" \
               "#(2)Find BOTS IN LAN(2)#\n" \
               "#(3)  START BOTNET  (3)#\n" \
               "#(p)   Print Bots   (p)#\n" \
               "#(e)     EXIT       (e)#\n" \
               "#########Choice#########\n"

    def __ActionInfo(self):
        return "#########Choice#########\n" \
               "#(b) BruteForce     (b)#\n" \
               "#(s) SortArray      (s)#\n" \
               "#(m) MessageToBots  (m)#\n" \
               "#(E) BotNetStop     (E)#\n" \
               "#(e)    Back        (e)#\n" \
               "#########Choice#########\n"

    def CreateAction(self, id, action, array=None):
        data = {"Id": id, "Action": action}
        if array is not None:
            data["Array"] = array
        return pickle.dumps(data)

    def StartParallels(self, action, array=None):
        for i, bot in (enumerate(self.bots)):
            data = self.CreateAction(i, action, array)
            self.SendBot(bot=bot, data=data)

    def AcceptingAction(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind(('0.0.0.0', int(self.port)))
        while True:
            data, addr = server_socket.recvfrom(1024)
            message = pickle.loads(data)
            print("Получено сообщение от {0}: {1}".format(addr[0], message))
            self.bots[addr[0]]["Status"] = True
            self.bots[addr[0]]["Data"] = message
            if self.Action == "B":
                print(message)
                break

    def StartAction(self, action, array=None):
        StartParallels_threading = threading.Thread(target=self.StartParallels, args=(action, array))
        AcceptingAction_threading = threading.Thread(target=self.AcceptingAction)
        StartParallels_threading.start()
        AcceptingAction_threading.start()
        StartParallels_threading.join()
        # AcceptingAction_threading.join()

    def StartServer(self):
        while True:
            print(self.__Info())
            x = str(input())
            match x:
                case "1":
                    self.FindDevices()
                case "2":
                    validate_threading = threading.Thread(target=self.FindBots)
                    accept_threading = threading.Thread(target=self.GetAcceptBot)
                    accept_threading.start()
                    validate_threading.start()
                    accept_threading.join()
                    validate_threading.join()
                case "3":
                    if len(self.bots) > 0:
                        print(self.__ActionInfo())
                        a = str(input())
                        match a:
                            case "b":
                                self.Action = "B"
                                length = int(input("Write password length: "))
                                self.StartAction(action="Brute", array=length)
                            case "m":
                                self.Action = "M"
                                self.StartAction(action="Message")
                            case "s":
                                self.Action = "S"
                                self.StartAction(action="Sorting")
                            case "BE":
                                self.Action = "BE"
                                self.StartAction(action="BotEnd")
                            case "e":
                                print()
                            case _:
                                print("This action not found!")
                    else:
                        print("You have 0 bots in botnet")
                case "p":
                    print(f"Bots in botnet: {len(self.bots)}")
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
        # ip_address = socket.gethostbyname(self.ip)
        # получаем адрес подсети
        # subnet_address = '.'.join(ip_address.split('.')[:-1]) + '.0'
        # broadcast_address = f"<{subnet_address}>"  # здесь необходимо указать адрес подсети для броадкаста
        # привязываем сокет к адресу и порту
        server_socket.bind(('0.0.0.0', int(self.port)))
        # слушаем порт
        # получаем сообщения
        while True:
            data, addr = server_socket.recvfrom(1024)  # получаем сообщение и адрес отправителя
            self.server = addr[0]
            data = pickle.loads(data)
            print("Получено сообщение от {0}: {1}".format(addr, data))  # выводим данные
            match data["Action"]:
                case "Auth":
                    server_socket.sendto(pickle.dumps(True), (self.server, int(self.port)))
                case "BotEnd":
                    print("Command BE - BotNet stopped!")
                    exit(6)
                case "Brute":
                    Id = int(data["Id"])
                    x = int(data["Array"])
                    print(x, Id)
                    t = (x * (Id - 1), x * Id)
                    f = Brute(pw="BruteP")
                    # if data["Chars"] is not None:
                    #     f.setChars(data["Chars"])
                    f = f.brute(abs(t[0]), abs(t[1]))
                    server_socket.sendto(pickle.dumps(f), (self.server, int(self.port)))
                case "Message":
                    print(f"{addr[0]} send {data}")
                case _:
                    print(f"Unknown command from {addr[0]}")

# Будущие фиксы
# сервер отправляет сам себе запросы! Удалить адрес сервера self.ip из self.addr
