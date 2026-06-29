import socket
import threading

# Настройки подключения (для тестов на одном устройстве оставляем localhost)
HOST = '0.0.0.0'  # Слушать все доступные сетевые интерфейсы
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Списки для хранения активных клиентов и их никнеймов
clients = []
nicknames = []

def broadcast(message, current_client=None):
    """Отправка сообщения всем пользователям, кроме автора (опционально)"""
    for client in clients:
        try:
            # Можно отправлять всем, но для красоты чата шлем абсолютно каждому
            client.send(message)
        except:
            # Если отправка не удалась, клиент скорее всего отключился
            remove_client(client)

def remove_client(client):
    """Безопасное удаление клиента при отключении"""
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        broadcast(f"📢 System: {nickname} покинул чат.".encode('utf-8'))
        nicknames.remove(nickname)
        print(f"[-] Клиент {nickname} отключился.")

def handle_client(client):
    """Постоянный поток для чтения сообщений от конкретного клиента"""
    while True:
        try:
            # Принимаем сообщение (максимум 1024 байта)
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break
            # Пересылаем сообщение всем остальным
            broadcast(message)
        except:
            remove_client(client)
            break

def main():
    print("[*] Сервер LUMIX запущен и ждет пользователей...")
    while True:
        client, address = server.accept()
        print(f"[+] Новое подключение с адреса: {str(address)}")

        # Запрашиваем никнейм у клиента при первом коннекте
        client.send("GET_NICK".encode('utf-8'))
        try:
            nickname = client.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            clients.append(client)

            print(f"[v] Пользователь зарегистрирован как: {nickname}")
            
            # Оповещаем всех внутри чата
            broadcast(f"🚀 {nickname} ворвался в чат!".encode('utf-8'))
            client.send("Добро пожаловать в LUMIX! Начните общение.\n--------------------------------".encode('utf-8'))

            # Запускаем отдельный поток для этого пользователя
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        except:
            client.close()

if __name__ == "__main__":
    main()
      
