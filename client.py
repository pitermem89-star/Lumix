import socket
import threading
import sys

# Запрашиваем имя перед подключением
nickname = input("Введите ваш никнейм: ")
if not nickname.strip():
    print("Никнейм не может быть пустым!")
    sys.exit()

# Создаем сокет и подключаемся к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Если тестируешь на одном устройстве — оставляй 127.0.0.1. 
# Если сервер на другом девайсе, впиши туда его IP.
SERVER_IP = '127.0.0.1' 
PORT = 55555

try:
    client.connect((SERVER_IP, PORT))
except Exception as e:
    print(f"Не удалось подключиться к серверу: {e}")
    sys.exit()

def receive_messages():
    """Поток для постоянного приема сообщений от сервера"""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "GET_NICK":
                client.send(nickname.encode('utf-8'))
            else:
                # Очищаем текущую строку ввода в консоли перед выводом нового сообщения
                print(f"\r{message}\n{nickname}: ", end="")
        except:
            print("\n[!] Соединение с сервером потеряно.")
            client.close()
            break

def send_messages():
    """Поток для отправки сообщений на сервер"""
    while True:
        try:
            text = input(f"{nickname}: ")
            if text.strip(): # Не отправляем пустые строки
                full_message = f"{nickname}: {text}"
                client.send(full_message.encode('utf-8'))
        except:
            break

# Запускаем параллельные потоки
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True # Поток закроется автоматически при выходе из программы
receive_thread.start()

send_messages()
