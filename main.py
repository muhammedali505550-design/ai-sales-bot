import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8611840465:AAGS9FBoZmxhuq2hoTaRwGcC9WqF1Kf9rso")

FAQ = {
    "привет": "Привет! Я твой ИИ-ассистент магазина SneakerHead. 🔥 У нас в наличии топовые кроссовки: Nike, Adidas, Jordan! Цены от 5000 до 15000 рублей. Что тебя интересует?",
    "ассортимент": "В наличии есть легендарные Nike Air Force, Jordan 1 Retro и удобные Adidas Yeezy. Какой бренд хочешь посмотреть?",
    "nike": "Nike Air Force 1 — 7 500 руб. Все размеры в наличии! Хочешь оформить заказ? Нажми кнопку 'Заказать кроссовки 👟' снизу!",
    "adidas": "Adidas Yeezy Boost 350 — 12 000 руб. Очень удобные! Хочешь купить? Нажми кнопку 'Заказать кроссовки 👟' снизу!",
    "jordan": "Air Jordan 1 High — 14 900 руб. Классика! Чтобы забронировать свой размер, нажми кнопку 'Заказать кроссовки 👟' снизу!",
    "доставка": "Доставляем по всей стране за 2-4 дня! Примерка перед покупкой бесплатная.",
    "цена": "Цены на наши кроссовки от 5 000 до 15 000 рублей в зависимости от модели. Какая модель интересует?",
}

def start(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Заказать кроссовки 👟", request_contact=True)]], 
        resize_keyboard=True
    )
    update.message.reply_text(
        "Добро пожаловать в SneakerHead! 👟\n\nЯ твой автоматический ИИ-продавец. Задай мне любой вопрос (например: 'Какие цены?', 'Что в наличии?', 'Какая доставка?').\n\nЕсли готов сделать заказ — просто нажми кнопку снизу!",
        reply_markup=reply_markup
    )

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    response = "Отличный вопрос! Наш менеджер уже бежит отвечать, но ты можешь прямо сейчас нажать кнопку 'Заказать кроссовки 👟' снизу, чтобы забронировать скидку и лучшую цену! 🚀"
    
    for key, value in FAQ.items():
        if key in text:
            response = value
            break
            
    update.message.reply_text(response)

def handle_contact(update: Update, context: CallbackContext):
    contact = update.message.contact
    phone = contact.phone_number
    name = contact.first_name
    print(f"🔥 НОВЫЙ ЛИД! Имя: {name}, Телефон: {phone}")
    update.message.reply_text(
        f"Спасибо, {name}! 🤝 Твоя заявка принята. Наш менеджер свяжется с тобой по номеру {phone} в течение 10 минут для подтверждения заказа и размера!"
    )

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(MessageHandler(Filters.contact, handle_contact))
    
    print("🤖 Бот успешно запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
