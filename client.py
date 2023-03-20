import socket
from Logic import getData


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
            Id = int(msg["Id"])
            x = int(msg["Range"])
            t = (x * (Id-1), x * Id)
            print(Id,t)
            return brute(int(t[0]), int(t[1]))
        case "Message":
            return "Hello bro"


def connect(HOST, client):
    msg = getData(client, HOST)
    msg = msg.split("|")
    msg = getCom(msg)
    print(Action(msg))
    # client.send(Action(msg).encode())


def brute(a, b):
    f = -1
    psw = 12356731
    for i in range(a, b):
        if psw == i:
            f = i
            break
    return f


if __name__ == '__main__':
    HOST = (socket.gethostname(), 8080)
    # HOST = ("localhost", 10000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # waitingClient()
    connect(HOST, client)
