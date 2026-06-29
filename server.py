import asyncio
import websockets
import os

# Хранилище для активных подключений: {websocket: nickname}
CLIENTS = {}

async def broadcast(message):
    """Отправка сообщения всем подключенным пользователям"""
    if CLIENTS:
        # Создаем список задач на отправку для каждого клиента
        await asyncio.gather(*[client.send(message) for client in CLIENTS])

async def handle_client(websocket):
    """Обработка соединения конкретного клиента"""
    print(f"[+] Новое подключение: {websocket.remote_address}")
    
    try:
        # Первым делом запрашиваем никнейм
        await websocket.send("AUTH_REQ_NICK")
        nickname = await websocket.recv()
        
        if not nickname or nickname.strip() == "" or nickname == "AUTH_REQ_NICK":
            nickname = f"User_{websocket.remote_address[1]}"
            
        CLIENTS[websocket] = nickname
        print(f"[v] Пользователь {websocket.remote_address} зарегистрирован как: {nickname}")
        
        # Оповещаем всех о новом участнике
        await broadcast(f"🚀 {nickname} ворвался в чат LUMIX!")
        await websocket.send("Добро пожаловать в LUMIX! Начните общение.\n--------------------------------")

        # Основной цикл приема сообщений от этого клиента
        async for message in websocket:
            if message.strip():
                full_message = f"{nickname}: {message}"
                await broadcast(full_message)
                
    except websockets.exceptions.ConnectionClosed:
        print(f"[-] Соединение закрыто удаленно: {websocket.remote_address}")
    except Exception as e:
        print(f"[!] Ошибка при работе с клиентом: {e}")
    finally:
        # Если клиент отключился — удаляем его из базы и оповещаем чат
        if websocket in CLIENTS:
            nickname = CLIENTS[websocket]
            del CLIENTS[websocket]
            await broadcast(f"📢 System: {nickname} покинул чат LUMIX.")
        print(f"[-] Клиент {websocket.remote_address} полностью отключен.")

async def main():
    # Render передает порт в переменную окружения PORT. Если тестируем локально — берем 55555
    port = int(os.environ.get("PORT", 55555))
    # Хост обязательно 0.0.0.0, чтобы принимать внешние запросы
    host = "0.0.0.0"
    
    print(f"[*] Сервер LUMIX (WebSockets) запускается на {host}:{port}...")
    
    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()  # Запускает бесконечный цикл ожидания

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Сервер LUMIX остановлен.")
