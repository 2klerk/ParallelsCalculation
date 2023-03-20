import socket
import threading
from Title import titleServer
from Logic import sendData

# Переменная для того чтобы проводить операции сервера над клиентами
clients = {}
action = "N"
maxUsers = 3


# Присваиваем каждому подючённому клиенту свой id
def editDict(connection, client_address, ex1):
    clients[(len(clients) + 1)] = [connection, client_address[0], client_address[1]]
    message = "".join(["Id:" + str(len(clients)), ex1])
    return message.encode()

#Ввод команд для клиента
def enteringCommand():
    command = str(input("Action:"))
    match command:
        case "Brute":
            message = "|Action:Brute|"
            title = "Range:"
            x = str(int(input(title))//maxUsers)
            return "".join([message, title+x])
        case "Message":
            title = "Message"
            x = str(input(title+":"))
            return "".join(["|Action:Message|", title+":"+x])

def startCon(s, ex1):
    global action
    while True:
        if len(clients) == maxUsers:
            break
        print('Ожидание подключения...')
        connection, client_address = s.accept()
        message = editDict(connection, client_address, ex1)
        # запускаем обработку соединения в отдельном потоке
        print("Отправка...")
        client_thread = threading.Thread(target=sendData, args=(connection, client_address, message))
        client_thread.start()


def Action():
    global action
    titleServer()
    action = str(input())
    # keyboard.wait('q')
    action = 'c'

    # if action == "e":
    #     exit(2)



def startAction(ex1):
    HOST = (socket.gethostname(), 8080)
    # HOST = ("localhost", 8080)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(HOST)
    s.listen(5)
    # Принимаем соединения
    server_thread = threading.Thread(target=startCon, args=(s, ex1))
    # action_thread = threading.Thread(target=Action())
    # action_thread.start()
    server_thread.start()


if __name__ == '__main__':
    # ex1 = enteringCommand()
    x = 12356738//maxUsers
    ex1 = "|Action:Brute|Range:"+str(x)
    print("Your command: "+ex1)
    startAction(ex1)
