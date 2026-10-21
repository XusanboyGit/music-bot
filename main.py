import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8961484963:AAFWzNThapXfIE0X2iaDylqm08NO6dDZMq8"
bot = telebot.TeleBot(TOKEN)

print("Musiqa boti muvaffaqiyatli ishga tushdi...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yoki ijrochini yozing, men uni topib beraman!"
    )

@bot.message_handler(func=lambda message: True)
def search_and_send_music(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda...")

    try:
        # Jamendo ommaviy ochiq API orqali qidirish (serverga yuklama tushirmaydi va block bo'lmaydi)
        url = f"https://api.jamendo.com/v3.0/tracks/?client_id=56d32708&format=json&limit=1&search={query}"
        response = requests.get(url).json()

        if response.get('results') and len(response['results']) > 0:
            track = response['results'][0]
            audio_url = track['audio']
            title = track['name']
            performer = track['artist_name']

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("👤 Admin bilan bog'lanish", url="https://t.me/Ismoiljanov_7"))

            bot.send_audio(
                chat_id,
                audio_url,
                title=title,
                performer=performer,
                caption=f"🎵 Musiqangiz tayyor!\n\n🚀 @music_1_maktab_bot orqali topildi.",
                reply_markup=markup
            )
            bot.delete_message(chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Kechirasiz, bu nom bo'yicha musiqa topilmadi. Boshqa nom yozib ko'ring.", chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        bot.edit_message_text("❌ Qidiruvda xatolik bo'ldi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

bot.infinity_polling()
