import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# BOT TOKENINGIZ
TOKEN = "8981526249:AAFgRy_t3DFIiRYRYzYWgJ3ZhdZfe0exRZY"
bot = telebot.TeleBot(TOKEN)

print("Musiqa yuklovchi bot yangi tizimda muvaffaqiyatli ishga tushdi...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni tezkor va cheklovsiz yuklab beraman!"
    )

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda...")

    try:
        # Bevaqt YouTube blokirovkalaridan qochish uchun ochiq Musiqa API qidiruvi
        search_url = f"https://apple.com{requests.utils.quote(query)}&media=music&limit=1"
        response = requests.get(search_url).json()

        if response.get("resultCount", 0) > 0:
            track = response["results"][0]
            audio_url = track["previewUrl"]  # Musiqa fayli havolasi
            track_name = track["trackName"]
            artist_name = track["artistName"]

            bot.edit_message_text(f"🚀 '{track_name}' Telegram'ga yuklanmoqda...", chat_id, status_msg.message_id)

            # Audio faylni yuklab olish
            audio_data = requests.get(audio_url).content
            file_name = f"downloads/{chat_id}_music.mp3"
            
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            with open(file_name, "wb") as f:
                f.write(audio_data)

            # Admin tugmasi
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("👤 Admin", url="https://t.me"))

            # Telegram'ga audio qilib yuborish
            with open(file_name, "rb") as audio_file:
                bot.send_audio(
                    chat_id, 
                    audio_file, 
                    title=track_name, 
                    performer=artist_name,
                    caption=f"🎵 {artist_name} - {track_name}\n\n🚀 @Ismoiljanov_7 boti orqali yuklandi.",
                    reply_markup=markup
                )

            os.remove(file_name)
            bot.delete_message(chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Kechirasiz, bunday nomli musiqa topilmadi. Boshqa nom yozib ko'ring.", chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Xatolik: {e}")
        bot.edit_message_text("⚠️ Musiqani yuklashda muammo bo'ldi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

bot.infinity_polling()
