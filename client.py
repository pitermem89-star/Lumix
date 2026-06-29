import asyncio
import threading
import sys
import random
from kivy.lang import Builder
from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
import websockets

# Графическая разметка интерфейса на языке KV (стиль LUMIX)
KV = '''
MDScreen:
    md_bg_color: 0.05, 0.05, 0.08, 1  # Очень темный кастомный фон

    MDBoxLayout:
        orientation: 'vertical'
        padding: [10, 20, 10, 10]
        spacing: 10

        # Верхняя панель (Хедер мессенджера)
        MDBoxLayout:
            size_hint_y: None
            height: "50dp"
            md_bg_color: 0.1, 0.1, 0.15, 1
            padding: [15, 0, 15, 0]
            radius: [12, 12, 12, 12]
            
            MDLabel:
                text: "LUMIX MESSENGER"
                theme_text_color: "Custom"
                text_color: 0.0, 0.8, 1.0, 1  # Неоновый голубой
                font_style: "H6"
                bold: True
                halign: "left"
                valign: "center"

        # Основной экран чата (Скролл с сообщениями)
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            bar_width: "4dp"

            MDBoxLayout:
                id: chat_logs
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 8
                padding: [5, 10, 5, 10]

        # Нижняя панель ввода сообщений
        MDBoxLayout:
            size_hint_y: None
            height: "60dp"
            spacing: 10
            padding: [5, 5, 5, 5]

            MDTextField:
                id: message_input
                hint_text: "Напишите сообщение..."
                mode: "rectangle"
                multiline: False
                size_hint_x: 0.85
                text_color_focus: 0.7, 0.3, 1.0, 1  # Фиолетовый фокус
                hint_text_color_focus: 0.7, 0.3, 1.0, 1
                line_color_focus: 0.0, 0.8, 1.0, 1   # Неоновый голубой при вводе
                on_text_validate: app.send_message_from_ui()

            MDIconButton:
                icon: "send"
                theme_icon_color: "Custom"
                icon_color: 0.0, 0.8, 1.0, 1
                md_bg_color: 0.1, 0.1, 0.15, 1
                size_hint_x: 0.15
                on_release: app.send_message_from_ui()
'''

# Кастомный элемент сообщения чата
class ChatMessage(MDBoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = "45dp"
        self.padding = [12, 8, 12, 8]
        self.radius = [10, 10, 10, 10]
        
        # Разделение цветов: системные сообщения или обычный текст
        if text.startswith("🚀") or text.startswith("📢"):
            self.md_bg_color = [0.15, 0.15, 0.2, 0.4]
        else:
            self.md_bg_color = [0.12, 0.12, 0.18, 1]

        from kivymd.uix.label import MDLabel
        lbl = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.95, 1],
            font_style="Subtitle2",
            valign="center"
        )
        self.add_widget(lbl)


class LumixApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        # Генерируем случайный никнейм для теста
        self.nickname = f"User_{random.randint(100, 999)}"
        
        self.websocket = None
        self.loop = None
        
        # Запускаем фоновый поток для работы с сетью WebSockets
        threading.Thread(target=self.start_async_loop, daemon=True).start()
        
        return Builder.load_string(KV)

    def start_async_loop(self):
        """Запуск асинхронного цикла для обработки веб-сокетов"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.network_handler())

    async def network_handler(self):
        """Слушатель сервера Render в реальном времени"""
        # ВСТАВЬ СЮДА СВОЮ ССЫЛКУ С RENDER (ОБЯЗАТЕЛЬНО С wss:// В НАЧАЛЕ)
        uri = "wss://lumix-oub9.onrender.com"
        
        self.append_message_to_ui(f"[*] Подключение к LUMIX ({self.nickname})...")
        
        try:
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                self.append_message_to_ui("[+] Успешно подключено!")
                
                async for message in websocket:
                    if message == "AUTH_REQ_NICK":
                        await websocket.send(self.nickname)
                    else:
                        self.append_message_to_ui(message)
        except Exception as e:
            self.append_message_to_ui(f"[!] Ошибка сети: {e}")

    def append_message_to_ui(self, text):
        """Безопасное добавление сообщения на экран из любого потока"""
        Clock.schedule_once(lambda dt: self._add_message_widget(text))

    def _add_message_widget(self, text):
        box = self.root.ids.chat_logs
        box.add_widget(ChatMessage(text=text))

    def send_message_from_ui(self):
        """Отправка сообщения из текстового поля ввода"""
        input_field = self.root.ids.message_input
        text = input_field.text.strip()
        
        if text and self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.send(text), self.loop)
            input_field.text = ""  # Очищаем поле ввода


if __name__ == "__main__":
    LumixApp().run()
