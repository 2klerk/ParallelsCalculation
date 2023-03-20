import socket
import threading
from Title import titleServer
import keyboard

# Переменная для того чтобы проводить операции сервера над клиентами
clients = []
action = "N"


# функция для обработки каждого соединения в отдельном потоке
def handle_client(connection, client_address, message):
    print(f'Подключился клиент {client_address}')

    # отправляем сообщение клиенту
    connection.send(message)

    # закрываем соединение
    connection.close()
    print(f'Отключился клиент {client_address}')


def startCon(s, ex1):
    global action
    while True:
        print('Ожидание подключения...')
        connection, client_address = s.accept()
        clients.append(len(clients) + 1)
        print(clients,"Id:"+str(clients[len(clients)-1]), "Action "+action)
        # запускаем обработку соединения в отдельном потоке
        if action == "c":
            print("Отправка...")
            client_thread = threading.Thread(target=handle_client, args=(connection, client_address, ex1))
            client_thread.start()
        else:
            print("Command not found")


def Action():
    global action
    titleServer()
    action = str(input())
    if action == "e":
        exit(2)


def startAction():
    # ex1 = b'Id:1\nAction:Brute\nRange:0-12356735'
    ex1 = b'Id:1\nAction:Message\nMessage:PrivetBuba'
    HOST = (socket.gethostname(), 8080)
    # HOST = ("localhost", 8080)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(HOST)
    s.listen(5)
    # Принимаем соединения
    server_thread = threading.Thread(target=startCon, args=(s, ex1))
    action_thread = threading.Thread(target=Action())
    action_thread.start()
    server_thread.start()


if __name__ == '__main__':
    startAction()
