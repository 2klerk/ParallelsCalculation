import socket
from Logic import getData, sendFromClient
import pickle

def getCom(com):
    l = {}
    for i in com:
        t = i.split(':')
        l[t[0]] = t[1]
    return l

# fail to ban
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
            print(Id, t)
            return brute(int(t[0]), int(t[1]))
        case "Message":
            return "Hello bro"


def connect(HOST, client, choice, msg=""):
    if not choice:
        msg = getData(client, HOST)
        msg = msg.split("|")
        return getCom(msg)
    else:
        information = pickle.dumps({msg["Id"]: Action(msg)})
        sendFromClient(information, HOST, client)


def brute(a, b):
    f = -1
    psw = 12356731
    for i in range(a, b):
        if psw == i:
            f = i
            break
    return f


if __name__ == '__main__':
    # 192.168.0.188
    HOST = (socket.gethostname(), 8080)
    # HOST = ("localhost", 10000)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # waitingClient()
    msg = connect(HOST, client, False)
    # connect(HOST, client, True, msg)
