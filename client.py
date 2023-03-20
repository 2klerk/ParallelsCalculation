import socket
import threading
from Title import waitingClient


def getCom(com):
    l = {}
    for i in com:
        t = i.split(':')
        l[t[0]] = t[1]
    return l


def Action(msg):
    print(msg["Action"])
    match msg["Action"]:
        case "Brute":
            print("Bruting")
            # Получение разделённого промежутка
            # m = int(msg["Range"])
            # t = [m * (id - 1), m * id]
            t = msg["Range"].split("-")
            brute(int(t[0]), int(t[1]))


def connect(HOST, client):
    msg = ""
    client.connect(HOST)
    print("Connect to", HOST)
    while True:
        data = client.recv(50)
        msg += data.decode()
        print(data)
        if msg == "wait" or not len(data):
            break
    # print(msg)
    msg = msg.split("\n")
    msg = getCom(msg)
    Action(msg)


def brute(a, b):
    f = False
    psw = 12356731
    for i in range(a, b):
        if psw == i:
            f = True
            break
    if f:
        print("Found")
    else:
        print("Not found")


if __name__ == '__main__':
    HOST = (socket.gethostname(), 8080)
    # HOST = ("localhost", 10000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # waitingClient()
    connect(HOST, client)
