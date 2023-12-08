import pickle
import socket
            

#Получаем матрицу от пользователя
def get_matrix() -> list:
    while True:
        try:
            size = int(input("Введите размер квадратной матрицы: "))
            break
        except ValueError:
            pass

    matrix = []
    print("Построчно через пробел введите элементы матрицы:")

    for i in range(size):
        while True:
            try:
                row = list(map(float, input(f"{i+1}: ").split(" ")))
                break
            except ValueError:
                pass
        
        if len(row) > size:
            row = row[:size]
        if len(row) < size:
            row += [0.0] * (size-len(row))
        matrix.append(row)

    print("\nВведенная матрица:")
    for row in matrix:
        print(" ".join(map(str, row)))

    return matrix

#Отправляем матрицу на сервер
def send_matrix(matrix: list):
    host = '127.0.0.1'
    port = 12345
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            serialized_matrix = pickle.dumps(matrix)
            s.sendall(serialized_matrix)
            data = s.recv(1024)

        print(f"Сообщение от сервера:\n{data.decode('utf-8')}")
    except:
        print("Не удалось подключится к серверу :(")


if __name__ == "__main__":
    matrix = get_matrix()
    send_matrix(matrix)
