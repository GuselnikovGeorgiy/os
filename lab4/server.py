import pickle
import socket
import os
import multiprocessing as mp
from multiprocessing import shared_memory
import numpy as np
import struct



#Считаем определитель
def calculate_det(shm_name: str, fifo_path: str, size: int, res: mp.Queue()):
    
    data = mp.shared_memory.SharedMemory(name=shm_name)
    matrix = np.ndarray(shape=(size, size), dtype='float64', buffer=data.buf)

    det = np.linalg.det(matrix)
    print(f"Определитель матрицы равен = {det}")

    res.put(det)

    with open(fifo_path, "wb") as f:
        f.write(struct.pack('f', det))

    data.close()



#Считаем обратную матрицу методом Гаусса
def calculate_inverse(shm_name: str, fifo_path: str, size: int):

    with open(fifo_path, "rb") as f:
        det_bytes = f.read(4)
        det = struct.unpack('f', det_bytes)[0]

    if det == 0.0:
        print("Матрица вырожденная, обратной матрицы не существует.")
        return

    data = mp.shared_memory.SharedMemory(name=shm_name)
    matrix = np.ndarray(shape=(size, size), dtype='float64', buffer=data.buf)

    augmented_matrix = np.hstack([matrix, np.eye(size)])

    for i in range(size):
        #Приведение к единичной диагональной матрице
        pivot = augmented_matrix[i, i]
        augmented_matrix[i, :] /= pivot

        for j in range(size):
            if i != j:
                ratio = augmented_matrix[j, i]
                augmented_matrix[j, :] -= ratio * augmented_matrix[i, :]

    inverse_matrix = augmented_matrix[:, size:]
    inverse_matrix = np.round(inverse_matrix, decimals=2)
    
    print("Обратная матрица:")
    for row in inverse_matrix:
        print(" ".join(map(str, row)))

    np.copyto(np.frombuffer(data.buf, dtype='float64'), inverse_matrix.reshape((size*size,)))
    
    data.close()



def main():
    #Создаем серверный сокет
    host = '127.0.0.1'
    port = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    with sock as s:
        #Принимаем подключение и слушаем сокет
        s.bind((host, port))
        s.listen()
        print(f"Сервер ожидает подключения на {host}:{port}")
        conn, addr = s.accept()

        with conn:
            #Считываем матрицу
            print(f"Подключено к {addr}")
            data = conn.recv(4096)
            matrix_data = np.array(pickle.loads(data))
            
            matrix_size = len(matrix_data)
            print("Получена матрица от клиента:")
            for row in matrix_data:
                print(" ".join(map(str, row)))
            
            #Сохраняем матрицу в разделяемую память
            shm_name = "MyMemory"
            matrix_shm = shared_memory.SharedMemory(name=shm_name, create=True, size=matrix_data.nbytes)
            matrix = np.ndarray(shape=matrix_data.shape, dtype=matrix_data.dtype, buffer=matrix_shm.buf)
            matrix[:] = matrix_data[:]

            #Создаем именованый канал для обмена данными между процессами
            fifo_path = "determinant_channel"
            try:
                if os.path.exists(fifo_path):
                    os.remove(fifo_path)  

                print(f"Создан именованный канал '{fifo_path}'.")
                os.mkfifo(fifo_path)
            except OSError:
                print("Ошибка при создании канала")
                return


            #Получим значение определителя из дочернего потока
            det = mp.Queue()

            #Первый процесс - вычисление определителя
            det_process = mp.Process(target=calculate_det, args=(shm_name, fifo_path, matrix_size, det))
    
            #Второй процесс - вычисление обратной матрицы
            inv_process = mp.Process(target=calculate_inverse, args=(shm_name, fifo_path, matrix_size))
            
            det_process.start()
            inv_process.start()
        
            det_process.join()
            inv_process.join()

            if det.get() == 0.0:
                conn.send("Определитель равен нулю. Обратной матрицы не существует.".encode('utf-8'))
                matrix_shm.close()
                matrix_shm.unlink()
                os.unlink(fifo_path)
                return

            matrix_shm = shared_memory.SharedMemory(name=shm_name)
            matrix = np.ndarray(shape=matrix_data.shape, dtype=matrix_data.dtype, buffer=matrix_shm.buf)
            
            print("Передаю матрицу на клиент...")
            result = ""
            for row in matrix:
                result += " ".join(map(str, row)) + "\n"
                
            conn.send(f"Обратная матрица:\n{result}".encode('utf-8'))   

            matrix_shm.close()
            matrix_shm.unlink()
            os.unlink(fifo_path)
           

if __name__ == "__main__":
    main()
