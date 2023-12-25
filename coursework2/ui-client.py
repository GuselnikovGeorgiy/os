import random
import socket
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time
import os


def create_id():
    return os.getpid()

def run_gui(root, client_id):

    def get_time():
        current_time = datetime.now().time()
        return current_time.strftime("%H:%M:%S")

    def clear_combobox():
        server_combobox['values'] = ()
        server_combobox.set("")

    def change_combobox(server_num):
        server_combobox['values'] = ()
        if server_num == 1:
            values = ('1. Название используемого видеоадаптера', 
                    '2. Размер клиентской области')
        else:
            values = ('1. Количество свободных байтов файла подкачки', 
                    '2.1 Объем используемой физической памяти (байты)',
                    '2.2 Объем используемой физической памяти (мегабайты)',
                    '2.3 Объем используемой физической памяти (гигабайты)')
        server_combobox['values'] = values
        server_combobox.set(values[0])
        
    def close_connection():
        try:
            selected_mode = server_combobox.get()
            if selected_mode != "":
                clear_combobox()
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                console_text.insert(tk.END, f"{get_time()} Отключение от Сервера... Закрытие сокета...\n")
        except Exception as e:
            console_text.insert(tk.END, f"{get_time()} Ошибка при закрытии сокета: {e}\n")
    
    def connect_to_server(server_num):
        global sock 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        console_text.insert(tk.END, f"{get_time()} Подключение к серверу {server_num}...\n")
        host = '0.0.0.0'
        port = 8079 + server_num
        try:
            sock.connect((host, port))
            handshake = f'{client_id}'.encode("utf-8")
            change_combobox(server_num)
            sock.send(handshake)
            data = sock.recv(1024)
            console_text.insert(tk.END, f"{get_time()} Сообщение от сервера:\n{data.decode('utf-8')}\n") # успешное подключение...
        except Exception as e:
            print(e)
            console_text.insert(tk.END, f"{get_time()} Не удалось подключится к серверу {server_num}\n")
            clear_combobox()
        

    def make_request():
        selected_mode = server_combobox.get()
        if selected_mode != "":
            console_text.insert(tk.END, f"{get_time()} Отправка запроса на Cервер:\n{selected_mode}\n")
            sock.send(selected_mode.encode("utf-8"))
            data = sock.recv(4096).decode("utf-8")
            console_text.insert(tk.END, f"{get_time()} Данные от сервера:\n{data}\n")
    
    # Создание основного окна
    root.title(f"Клиентское приложение pid:{client_id}")
    root.geometry("1200x600")
    root.resizable(False, False)

    # Левая зона
    left_frame = ttk.Frame(root, padding=10)
    left_frame.grid(row=0, column=0, sticky="nsew")

    left_label = ttk.Label(left_frame, text="Взаимодействие с сервером:")
    left_label.grid(row=0, column=0, pady=10)

    connect_button1 = ttk.Button(left_frame, text="Подключиться к серверу 1", command=lambda: connect_to_server(1))
    connect_button1.grid(row=1, column=0, pady=10)

    connect_button2 = ttk.Button(left_frame, text="Подключиться к серверу 2", command=lambda: connect_to_server(2))
    connect_button2.grid(row=2, column=0, pady=10)

    Combobox_label = ttk.Label(left_frame, text="Взаимодействие с сервером:")
    Combobox_label.grid(row=3, column=0, pady=5)

    server_combobox = ttk.Combobox(left_frame)
    server_combobox.grid(row=4, column=0, pady=20)
    server_combobox['state'] = 'readonly'
    server_combobox.configure(width=52)

    send_button = ttk.Button(left_frame, text="Отправить запрос", command=lambda: make_request())
    send_button.grid(row=5, column=0, pady=5)

    close_conn_button = ttk.Button(left_frame, text="Отключиться от Сервера", command=lambda: close_connection())
    close_conn_button.grid(row=6, column=0, pady=5)

    # Правая зона
    right_frame = ttk.Frame(root, padding=10)
    right_frame.grid(row=0, column=2, sticky="nsew")

    console_label = ttk.Label(right_frame, text="Консоль:")
    console_label.grid(row=0, column=2, pady=5)

    console_text = tk.Text(right_frame, height=30, width=90, bg='white')
    console_text.grid(row=1, column=2, pady=5)
    
    clear_button = ttk.Button(right_frame, text="Очистить консоль", command=lambda: console_text.delete(1.0, tk.END))
    clear_button.grid(row=2, column=2, pady=5)
    
    

    # Растягивание ячеек для адаптивности
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)


def main():
    client_id = create_id()
    root = tk.Tk()
    run_gui(root, client_id)
    root.mainloop()

if __name__ == "__main__":
    main()
