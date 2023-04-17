import pickle
import socket

class Tools:
    def subPackets(data):
        chunk_size = 1024

        # Получение байтового представления контейнера
        data_bytes = pickle.dumps(data)

        # Разделение данных на части
        chunks = [data_bytes[i:i + chunk_size] for i in range(0, len(data_bytes), chunk_size)]

        return
    def unpackPackets():
        full_data_bytes = b''
        while True:
            chunk, _ = sock.recvfrom(chunk_size)
            full_data_bytes += chunk
            if len(chunk) < chunk_size:
                # Приняли все данные
                break

        full_data = pickle.loads(full_data_bytes)