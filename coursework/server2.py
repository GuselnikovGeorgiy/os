import pickle
import socket
import os
import multiprocessing as mp
import struct
import _thread
import threading
from psutil import Process

import subprocess

#погуглить асинхронный сокет 
print_lock = threading.Lock()

def threaded(conn):
    with conn:
        data = conn.recv(4096).decode("utf-8")
        print(f"Message from client {data}")
        swap_info = get_swap_info()
        
        select_mode = conn.send(f"Выберите единицы измерения для вывода используемой физической памяти:\n1: Байты\n2: Мегабайты\n3: Гигабайты\n".encode("utf-8"))
        type = int(conn.recv(1024))
        
        power = {1: 1024 ** 0, 
                2: 1024 ** 2, 
                3: 1024 ** 3}

        if swap_info is not None:
            swap = str(swap_info / power[type])
            conn.send(f"Сервер 2: количество свободных байтов подкачки:\n{swap}\n".encode("utf-8"))
        else:
            conn.send(f"Сервер 2: ошибка получения информации о файле подкачки.\n".encode("utf-8"))

            
        conn.send("Hello client, i have received your message!".encode("utf-8"))
    print_lock.release()


def get_swap_info():
    try:
        with open('/proc/meminfo', 'r') as mem_file: # cat /proc/meminfo | grep -i 'swapfree'
            lines = mem_file.readlines()
            for line in lines:
                
                if line.startswith('SwapFree:'):
                    return int(line.split()[1]) * 1024
    except Exception as e:
        print(f"Ошибка получения информации о файле подкачки: {e}")
        return None

def main():
    host = 'localhost'
    port = 8081
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    with sock as s:
        #Принимаем подключение и слушаем сокет
        s.bind((host, port))
        s.listen(5)
        while True:
            print(f"Сервер ожидает подключения на {host}:{port}")
            conn, addr = s.accept()
            pid = Process(conn.fileno()).pid
            print(f"pid: {pid}")

            print_lock.acquire()
            _thread.start_new_thread(threaded, (conn,))
        

if __name__ == "__main__":
    main()
