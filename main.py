import os
import json
import logging
import time
from urllib.request import Request, urlopen
from urllib.error import URLError

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8611840465:AAGS9FBoZmxhuq2hoTaRwGcC9WqF1Kf9rso")
API_URL = f"https://telegram.org{TOKEN}"

FAQ = {
    "привет": "Привет! Я твой ИИ-ассистент магазина SneakerHead. 🔥 У нас в наличии топовые кроссовки: Nike, Adidas, Jordan! Цены от 5000 до 15000 рублей. Что тебя интересует?",
    "ассортимент": "В наличии есть легендарные Nike Air Force, Jordan 1 Retro и удобные Adidas Yeezy. Какой бренд хочешь посмотреть?",
    "nike": "Nike Air Force 1 — 7 500 руб. Все размеры в наличии! Хочешь оформить заказ? Нажми кнопку 'Заказать кроссовки 👟' снизу!",
    "adidas": "Adidas Yeezy Boost 350 — 12 000 руб. Очень удобные! Хочешь купить? Нажми кнопку 'Заказать кроссовки 👟' снизу!",
    "jordan": "Air Jordan 1 High — 14 900 руб. Классика! Чтобы забронировать свой размер, нажми кнопку 'Заказать кроссовки 👟' снизу!",
    "доставка": "Доставляем по всей стране за 2-4 дня! Примерка перед покупкой бесплатная.",
    "цена": "Цены на наши кроссовки от 5 000 до 15 000 рублей в зависимости от модели. Какая модель интересует?",
}

def send_api_request(method, data):
    url = f"{API_URL}/{method}"
    req = Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except URLError as e:
        logging.error(f"Ошибка API запроса: {e}")
        return None

def handle_update(update):
    if "message" not in update:
        return
    
    message = update["message"]
    chat_id = message["chat"]["id"]
    
    if "text" in message:
        text = message["text"].lower()
        
        if text == "/start":
            reply_markup = {
                "keyboard": [[{"text": "Заказать кроссовки 👟", "request_contact": True}]],
                "resize_keyboard": True
            }
            send_api_request("sendMessage", {
                "chat_id": chat_id,
                "text": "Добро пожаловать в SneakerHead! 👟\n\nЯ твой автоматический ИИ-продавец. Задай мне любой вопрос (например: 'Какие цены?', 'Что в наличии?', 'Какая доставка?').\n\nЕсли готов сделать заказ — просто нажми кнопку снизу!",
                "reply_markup": reply_markup
            })
            return

        response_text = "Отличный вопрос! Наш менеджер уже бежит отвечать, но ты можешь прямо сейчас нажать кнопку 'Заказать кроссовки 👟' снизу, чтобы забронировать скидку и лучшую цену! 🚀"
        for key, value in FAQ.items():
            if key in text:
                response_text = value
                break
                
        send_api_request("sendMessage", {"chat_id": chat_id, "text": response_text})

    elif "contact" in message:
        contact = message["contact"]
        phone = contact["phone_number"]
        name = contact.get("first_name", "Клиент")
        logging.info(f"🔥 НОВЫЙ ЛИД! Имя: {name}, Телефон: {phone}")
        send_api_request("sendMessage", {
            "chat_id": chat_id,
            "text": f"Спасибо, {name}! 🤝 Твоя заявка принята. Наш менеджер свяжется с тобой по номеру {phone} в течение 10 минут для подтверждения заказа и размера!"
        })

def main():
    logging.info("🤖 Бот запускается на чистом Python...")
    offset = 0
    while True:
        try:
            updates = send_api_request("getUpdates", {"offset": offset, "timeout": 30})
            if updates and updates.get("ok") and updates.get("result"):
                for update in updates["result"]:
                    handle_update(update)
                    offset = update["update_id"] + 1
        except Exception as e:
            logging.error(f"Ошибка в главном цикле: {e}")
        time.sleep(1)

if __name__ == '__main__':
    main()
