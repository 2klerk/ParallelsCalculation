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
    return msg

# функция для обработки каждого соединения в отдельном потоке
def sendData(connection, client_address, message):
    print(f'Подключился клиент {client_address}')

    # отправляем сообщение клиенту
    connection.send(message)

    # закрываем соединение
    connection.close()
    print(f'Отключился клиент {client_address}')