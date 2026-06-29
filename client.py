import asyncio
import websockets
import sys

async def receive_messages(websocket, nickname):
    """Постоянное чтение сообщений от сервера"""
    try:
        async for message in websocket:
            if message == "AUTH_REQ_NICK":
                # Если сервер просит ник, отправляем его
                await websocket.send(nickname)
            else:
                # Очищаем строку ввода в консоли и выводим новое сообщение
                print(f"\r{message}\n{nickname}: ", end="")
    except websockets.exceptions.ConnectionClosed:
        print("\n[!] Соединение с сервером потеряно.")
    except Exception as e:
        print(f"\n[!] Ошибка получения данных: {e}")

async def send_messages(websocket, nickname):
    """Постоянный опрос консоли и отправка сообщений"""
    loop = asyncio.get_event_loop()
    try:
        while True:
            # Читаем ввод из консоли асинхронно, чтобы не блокировать получение сообщений
            message = await loop.run_in_executor(None, sys.stdin.readline)
            message = message.strip()
            if message:
                await websocket.send(message)
    except Exception as e:
        print(f"[!] Ошибка отправки данных: {e}")

async def main():
    nickname = input("Введите ваш никнейм для LUMIX: ").strip()
    if not nickname:
        print("Никнейм не может быть пустым!")
        return

    # Локальный адрес для тестов: 'ws://127.0.0.1:55555'
    # Когда задеплоишь на Render, замени адрес на свою ссылку вида: 'wss://твой-проект.onrender.com'
    server_uri = "ws://127.0.0.1:55555"
    
    print(f"[*] Подключение к серверу LUMIX по адресу {server_uri}...")
    
    try:
        async with websockets.connect(server_uri) as websocket:
            print("[+] Успешно подключено!")
            
            # Запускаем две задачи параллельно: прием и отправку
            receive_task = asyncio.create_task(receive_messages(websocket, nickname))
            send_task = asyncio.create_task(send_messages(websocket, nickname))
            
            # Ждем, пока одна из задач не завершится (например, при обрыве связи)
            await asyncio.wait([receive_task, send_task], return_when=asyncio.FIRST_COMPLETED)
    except Exception as e:
        print(f"[!] Не удалось подключиться к серверу: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Выход из мессенджера LUMIX.")
        sys.exit()
      
