import socket
import os
import multiprocessing as mp
import _thread
import threading
import subprocess
import sys
from psutil import Process

print_lock = threading.Lock()

def get_video_adapter_info():
    try:
        res = subprocess.run(['inxi', '-G'], capture_output=True, text=True, check=True)
        return res.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения информации о видеоадаптере: {e}")
        return None

def get_window_size(client_id):
    try:
        res = subprocess.run(['wmctrl', '-lpG'], capture_output=True, text=True, check=True)
        output = res.stdout.split("\n")
        for line in output:
            if client_id in line:
                window_info = line.split()
                return f"Размер клиентской области: {window_info[5]}x{window_info[6]}" if len(window_info) > 5 else None
        return None
    except subprocess.CalledProcessError as e:
        print(f"Ошибка получения информации о клиентской области: {e}")
        return None

def threaded(conn):
    with conn:
        
        data = conn.recv(4096).decode("utf-8")
        print(f"Message from client {data}")
        client_id = data
        conn.send("Соединение с Сервером 1 установлено!".encode("utf-8"))
        while True:
            data = conn.recv(4096).decode("utf-8")
            if not data:
                break
            if data[0] == "1":
                video_info = get_video_adapter_info()
                if video_info is not None:
                    conn.send(f"Сервер 1: Информация о видеоадаптере:\n{video_info}\n".encode("utf-8"))
                else:
                    conn.send(f"Сервер 1: Ошибка получения информации о видеоадаптере.\n".encode("utf-8"))
            elif data[0] == "2":
                win_size = get_window_size(client_id)
                if win_size is not None:
                    conn.send(f"Сервер 1: Информация о клиентской области:\n{win_size}\n".encode("utf-8"))
                else:
                    conn.send(f"Сервер 1: Ошибка получения информации о клиентской области.\n".encode("utf-8"))
            else:
                conn.send("Недопустимая опция.\n".encode("utf-8"))
            
    print_lock.release()
       

def main():
    host = 'localhost'
    port = 8080
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.  SO_REUSEADDR, 1)

    with sock as s:
        #Принимаем подключение и слушаем сокет
        try:
            s.bind((host, port))
        except socket.error as err:
            if err.errno == socket.errno.EADDRINUSE:
                print("Сервер 1 уже запущен...")
                sys.exit(1)
        s.listen(5)
        while True:
            print(f"Сервер 1 ожидает подключения на {host}:{port}")
            conn, addr = s.accept()
            
            # unlock thread
            print_lock.acquire()
            _thread.start_new_thread(threaded, (conn,))

        
if __name__ == "__main__":
    main()
