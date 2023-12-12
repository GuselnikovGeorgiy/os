import pickle
import socket
import os
import multiprocessing as mp
from multiprocessing import shared_memory
import numpy as np
import struct
import _thread
import threading
import subprocess
from psutil import Process

print_lock = threading.Lock()

def get_video_adapter_info():
    try:
        res = subprocess.run(['inxi', '-G'], capture_output=True, text=True, check=True)
        return res.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения информации о видеоадаптере: {e}")
        return None

def threaded(conn):
    with conn:
        data = conn.recv(4096).decode("utf-8")
        print(f"Message from client {data}")
        video_info = get_video_adapter_info()


        if video_info is not None:
            conn.send(f"Сервер 1: информация о видеоадаптере:\n{video_info}".encode("utf-8"))
        else:
            conn.send(f"Сервер 1: ошибка получения информации о видеоадаптере.")


        conn.send("Hello client, i have received your message!".encode("utf-8"))
    print_lock.release()
       

def main():
    host = 'localhost'
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.  SO_REUSEADDR, 1)

    with sock as s:
        #Принимаем подключение и слушаем сокет
        s.bind((host, port))
        s.listen(5)
        while True:
            print(f"Сервер ожидает подключения на {host}:{port}")
            conn, addr = s.accept()
            print(addr)

            pid = Process(conn.fileno()).pid
            print(f"pid: {pid}")
            
            # unlock thread
            print_lock.acquire()
            _thread.start_new_thread(threaded, (conn,))

        
if __name__ == "__main__":
    main()
