import pickle
import socket
import sys



# добавить псевдослучайный id при инициализации.
def main():
    attempts = 0
    while True:
        try:
            chose_server = int(input("Выберите сервер для подключения: "))
            break
        
        except ValueError:
            attempts += 1
            if attempts > 5:
                print("Request timed out")
                sys.exit(1)
    


    if chose_server == 1:
        host = 'localhost'
        port = 8080
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(socket.AF_INET)
                s.connect((host, port))
                message = 'Подключение клиента к серверу 1'.encode("utf-8")
                s.sendall(message)
                data = s.recv(1024)

            print(f"Сообщение от сервера:\n{data.decode('utf-8')}")
        except:
            print("Не удалось подключится к серверу :(")


    elif chose_server == 2:
        host = 'localhost'
        port = 8081
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                message = 'Подключение клиента к серверу 1'.encode("utf-8")
                s.sendall(message)
                data = s.recv(1024)
                print(f"Сообщение от сервера:\n{data.decode('utf-8')}")
                mode = input("Ответ: ")
                s.send(mode.encode("utf-8"))
                data = s.recv(1024)


            print(f"Сообщение от сервера:\n{data.decode('utf-8')}")
        except:
            print("Не удалось подключится к серверу :(")

if __name__ == "__main__":
    main()
