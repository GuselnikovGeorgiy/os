import socket
import os
import multiprocessing as mp
import struct
import _thread
import threading
import psutil 
import subprocess
import sys


#погуглить асинхронный сокет 
print_lock = threading.Lock()

def get_swap_info():
    try:
        swap = psutil.swap_memory().free
        return swap
    except Exception as e:
        print(f"Ошибка получения информации о файле подкачки: {e}")
        return None

def get_used_memory(data):
    power = {"1": [1024 ** 0, "Б"],
            "2": [1024 ** 2, "Мб"],
            "3": [1024 ** 3, "Гб"]}
    try:
        mem = psutil.virtual_memory().used
        return f"{round(mem / power[data[2]][0], 3)} {power[data[2]][1]}"
    except Exception as e:
        print(f"Ошибка получения информации об используемой памяти: {e}")
        return None

def threaded(conn):
    with conn:
        data = conn.recv(4096).decode("utf-8")
        print(f"Message from client {data}")
        client_id = data
        conn.send("Соединение с Сервером 2 установлено!".encode("utf-8"))
        while True:
            data = conn.recv(4096).decode("utf-8")
            if not data:
                break
            
            if data[0] == "1":
                swap_info = get_swap_info()
                if swap_info is not None:
                    conn.send(f"Сервер 2: Количество свободных байтов подкачки:\n{swap_info} Б\n".encode("utf-8"))
                else:
                    conn.send(f"Сервер 2: Ошибка получения информации о файле подкачки.\n".encode("utf-8"))
            elif data[0] == "2":
                used_mem = get_used_memory(data)
                if used_mem is not None:
                    conn.send(f"Сервер 2: Объем использованной физической памяти:\n{used_mem}\n".encode("utf-8"))
                else:
                    conn.send(f"Сервер 2: Ошибка получения информации о физической памяти.\n".encode("utf-8"))
            else:
                conn.send("Недопустимая опция.".encode("utf-8"))    
        
    print_lock.release()




def main():
    host = 'localhost'
    port = 8081
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    with sock as s:
        #Принимаем подключение и слушаем сокет
        try:
            s.bind((host, port))
        except socket.error as err:
            if err.errno == socket.errno.EADDRINUSE:
                print("Сервер 2 уже запущен...")
                sys.exit(1)

        s.listen(5)
        while True:
            print(f"Сервер 2 ожидает подключения на {host}:{port}")
            conn, addr = s.accept()

            print_lock.acquire()
            _thread.start_new_thread(threaded, (conn,))
        

if __name__ == "__main__":
    main()
