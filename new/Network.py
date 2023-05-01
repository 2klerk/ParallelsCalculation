# import multiprocessing
from pprint import pprint
import pyopencl as cl
import random
import platform
from cpuinfo import get_cpu_info
import subprocess
import re
import socket
import threading
from Brute import Brute
import pickle
from Sort import Sort
import time
import os


class Network:
    def __init__(self):
        self.large = None
        self.buffer = 1024
        self.start = None
        self.CPU = None
        self.GPU = None
        self.host = socket.gethostname()
        self.ip = socket.gethostbyname(self.host)
        self.port = 8080
        self.reserved_port = 8091
        self.OS = platform.system()  # Операционная система
        self.addr = []  # Все адреса в локальной сети
        self.bots = {}  # Список ботов в ботнете и статус получения данных
        self.server = None  # Для клиента ip сервера
        self.Action = None
        self.ready = 0

    def MyComputer(self):
        return {"CPU": self.CPU, "GPU": self.GPU}

    def getRange(self, x):
        return x // len(self.bots)

    def ResetAction(self):
        self.Action = None
        self.large = None
        self.ready = 0

    def setSpecs(self):
        path = "PC.pickle"
        if not os.path.isfile(path):
            self.CPU = {
                "Info": get_cpu_info()["brand_raw"],
                "cores": get_cpu_info()["count"]
            }
            pl = cl.get_platforms()[0]
            devices = pl.get_devices()
            self.GPU = {}
            for i, dev in enumerate(devices):
                self.GPU[f"GPU{i + 1}"] = {
                    "name": dev.name,
                    "type": cl.device_type.to_string(dev.type),
                    "memory": (dev.global_mem_size // 1024 // 1024)
                }
            f = open(path, "wb")
            f.write(pickle.dumps(self.MyComputer()))
        else:
            f = open(path, "rb")
            s = pickle.loads(f.read())
            self.CPU = s["CPU"]
            self.GPU = s["GPU"]

    def FindDevices(self):
        if self.OS == "Windows":
            addr = subprocess.check_output("arp -a", shell=True, encoding="cp1251")
            ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
            addr = set(re.findall(ip_regex, addr))
            self.addr = addr

    # перед работой сделать udp запросы по адресам, которые есть в self.addr
    def FindBots(self):
        for i in self.addr:
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = {"Id": None, "Action": "Auth"}
            dest_address = (i, self.port)
            udp.sendto(pickle.dumps(message), dest_address)

    def SendBot(self, bot, data, port):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        dest_address = (bot, port)
        udp.sendto(data, dest_address)

    # Получение данных авторизационных данных
    def GetAcceptBot(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.settimeout(3)
        while True:
            try:
                data, addr = server_socket.recvfrom(self.buffer)
                message = pickle.loads(data)
                print(addr[0], message)
                if addr[0] not in self.bots and "Status" in message and message["Status"] is True:
                    self.bots[addr[0]] = {"name": addr[1], "Status": False, "PC": message["PC"], "Data": None}
                    print("Получено сообщение от {0}: {1}".format(addr, message))
            except socket.timeout:
                print("Таймаут - больше нет сообщений")
                break

    def __Info(self):
        return "#########Choice##########\n" \
               "#(1)    CheckInLan   (1)#\n" \
               "#(2)  FindBotsInLan  (2)#\n" \
               "#(3)   StartBotnet   (3)#\n" \
               "#(p)    PrintBots    (p)#\n" \
               "#(PC)  ComputerInfo (PC)#\n" \
               "#(e)      EXIT       (e)#\n" \
               "#########Choice##########\n"

    def __ActionInfo(self):
        return "#########Choice#########\n" \
               "#(b) BruteForce     (b)#\n" \
               "#(s) SortArray      (s)#\n" \
               "#(m) MessageToBots  (m)#\n" \
               "#(BE) BotNetStop   (BE)#\n" \
               "#(e)    Back        (e)#\n" \
               "#########Choice#########\n"

    def CreateAction(self, data):
        return pickle.dumps(data)

    # Разделение массивов на n частей, где n число ботов
    def createSubArrays(self, array):
        L = self.getRange(len(array))
        subarrays = []
        for i in range(len(self.bots) - 1):
            subarrays.append(array[i * L: (i + 1) * L])
        subarrays.append(array[(len(self.bots) - 1) * L:])
        return subarrays

    # Отправка запросов клиентам
    def StartParallels(self, action, array=None):
        for i, bot in (enumerate(self.bots)):
            if array is not None and self.large is False:
                action["array"] = array[i]
                print(action["array"])
            action["Id"] = i
            data = self.CreateAction(action)
            self.SendBot(bot=bot, data=data, port=self.port)
            if self.large is True:
                if len(self.bots) > 1:
                    self.TCP_SEND(ip=bot, port=self.reserved_port, array=array[i])
                else:
                    self.TCP_SEND(ip=bot, port=self.reserved_port, array=array)
            time.sleep(0.01)

    # обработка расределённых действий
    def AcceptingAction(self, array=None):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind(('0.0.0.0', self.port))
        while True:
            data, addr = server_socket.recvfrom(self.buffer)
            message = pickle.loads(data)
            print("Получено сообщение от {0}: {1}".format(addr[0], message))
            if "Action" in message and message["Action"] == "W" and self.large is True:
                array = self.TCP_GET(self.reserved_port)
                self.bots[addr[0]]["Data"] = array
                self.bots[addr[0]]["Status"] = True
                self.ready += 1
            elif self.Action == "B":
                print(message)
                break
            if self.Action == "S" and self.ready == len(self.bots):
                break
        if self.Action == "S":
            a = Sort()
            if 0 > len(self.bots) > 1:
                array = a.mergeArray(arrayList=self.bots)
                array = Sort.merge_sort(array)
                self.ResetAction()
            print(f"Time BotNet sort: {time.time() - self.start}")
            return array

    def StartAction(self, action, array=None):
        action["Action"] = self.Action
        self.start = time.time()
        StartParallels_threading = threading.Thread(target=self.StartParallels, args=(action, array))
        AcceptingAction_threading = threading.Thread(target=self.AcceptingAction)
        if self.large is True:
            print("Custom TCP: ", self.large)
            StartParallels_threading.start()
            # StartParallels_threading.join()  # True
            print("Packets sends!")
            AcceptingAction_threading.start()
            AcceptingAction_threading.join()
        else:
            print("Custom TCP: ", self.large)
            StartParallels_threading.start()
            AcceptingAction_threading.start()
            # StartParallels_threading.join()  # Для self.large is False
            AcceptingAction_threading.join()

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
                        action = {"Id": None, "Action": None}
                        match a:
                            case "b":
                                self.Action = "B"
                                length = int(input("Write password length: "))
                                action["Range"] = self.getRange(length)
                                action["PSW"] = str(input("Write test password: "))
                                self.StartAction(action=action)
                            case "m":
                                self.Action = "M"
                                self.StartAction(action=action)
                            case "s":
                                self.Action = "S"
                                length = int(input("Array size: "))
                                self.large = True
                                array = [random.randint(0, 100) for i in range(length)]
                                if len(self.bots) > 1:
                                    array = self.createSubArrays(array=array)
                                print(len(array))
                                self.StartAction(action=action, array=array)
                            case "BE":
                                self.Action = "BE"
                                self.StartAction(action=action)
                            case "e":
                                self.Action = "BE"
                                self.StartAction(action=action)
                                print()
                            case _:
                                print("This action not found!")
                    else:
                        print("You have 0 bots in botnet")
                case "p":
                    print(f"Bots in botnet: {len(self.bots)}")
                    pprint(self.bots)
                case "PC":
                    if self.GPU is None:
                        self.setSpecs()
                    print(self.MyComputer())
                case "IP":
                    print(self.ip)
                case "e":
                    exit(4)
                case "t":
                    self.Action = "S"
                    self.large = True
                    length = int(input("Array size: "))
                    array = [random.randint(0, 100) for i in range(length)]
                    start = time.time()
                    array.sort()
                    end = time.time()
                    # subarrays = self.createSubArrays(array=array)
                    # self.StartAction(action=action, array=subarrays)
                    print("Standard sort", end - start)
                case _:
                    print("Command not found!")

    def Client(self):
        print(self.ip, self.port)
        # создаем UDP-сокет
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # разрешаем отправку широковещательных пакетов
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # устанавливаем адрес и порт широковещательной рассылки
        # привязываем сокет к адресу и порту
        server_socket.bind(('0.0.0.0', self.port))
        # слушаем порт
        # получаем сообщения
        while True:
            data, addr = server_socket.recvfrom(self.buffer)  # получаем сообщение и адрес отправителя
            self.server = addr[0]
            data = pickle.loads(data)
            print("Получено сообщение от {0}: {1}".format(addr, data))  # выводим данные
            match data["Action"]:
                case "Auth":
                    if self.GPU is None:
                        self.setSpecs()
                    server_socket.sendto(pickle.dumps({"Name": self.host, "Status": True, "PC": self.MyComputer()}),
                                         (self.server, self.port))
                case "BE":
                    print("Command BE - BotNet stopped!")
                    exit(6)
                case "S":
                    array = self.TCP_GET(port=self.reserved_port)
                    # if self.GPU is not None:
                    # if ["RTX", "GTX"] in self.GPU["Info"]:
                    #     array = Sort.sort_gpu_cuda()
                    # else:
                    #     array = Sort.sort_gpu(array)
                    # if self.CPU["cores"] >= 2:
                    #     array = Sort.merge_sort_parallel(array)
                    # else:
                    array = Sort.merge_sort(array)
                    print("Sorted: ", len(array))
                    server_socket.sendto(pickle.dumps({"Action": "W", "PKG": len(array)}), (self.server, self.port))
                    self.TCP_SEND(ip=self.server, port=self.reserved_port, array=array)
                case "B":
                    Id = int(data["Id"])
                    x = int(data["Range"])
                    print(x, Id)
                    t = (x * (Id - 1), x * Id)
                    f = Brute(pw=data["PSW"])
                    f = f.brute(abs(t[1]), abs(t[0]))
                    server_socket.sendto(pickle.dumps(f), (self.server, self.port))
                case "M":
                    print(f"{addr[0]} send {data}")
                case _:
                    print(f"Unknown command from {addr[0]}")

    def TCP_SEND(self, port, ip, array):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Send To{ip, port}")
        s.connect((ip, port))
        s.sendall(pickle.dumps(array))
        s.shutdown(socket.SHUT_WR)  # закрывает отсылку данных в канал связи
        s.close()

    def TCP_GET(self, port):
        print("Getting:", self.ip, port)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", port))
            s.listen()
            while True:
                (s_socket, address) = s.accept()
                print(f"Connected by {address}")
                data = b""
                while True:
                    chunk = s_socket.recv(1024)
                    if not chunk:
                        break
                    data += chunk
                data = pickle.loads(data)
                return data


# Похожие функции FIndbots SendBots
