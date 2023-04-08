def getData(client, HOST):
    msg = ""
    client.connect(HOST)
    print("Connect to", HOST)
    while True:
        data = client.recv(50)
        msg += data.decode()
        print(data)
        if not len(data):
            break
    client.close()
    return msg


def sendFromClient(information, HOST, client):
    print(f'Подключился к серверу {client}')
    # client.connect(HOST)
    client.send(information)
    client.close()
    print(f'Передал данные серверу {client}')


# функция для обработки каждого соединения в отдельном потоке
def sendData(connection, client_address, message):
    print(f'Подключился клиент {client_address}')

    # отправляем сообщение клиенту
    connection.send(message)
    # закрываем соединение
    # connection.shutdown()
    connection.close()
    # accepting(connection)
    print(f'Отключился клиент {client_address}')

def accepting(s):
    # global result
    while True:
        # client_socket, address = s.accept()
        print("Accepted", s)
        data = s.recv(1024)
        print(data)
        if not len(data):
            break