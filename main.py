import os
import re
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# SIZNING BOT TOKENINGIZ
TOKEN = "8981526249:AAFgRy_t3DFIiRYRYzYWgJ3ZhdZfe0exRZY"
bot = telebot.TeleBot(TOKEN)

print("Musiqa yuklovchi bot muvaffaqiyatli ishga tushdi...")

# /start buyrug'i bosilganda
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni Telegram'ning o'ziga yuklab beraman!"
    )

# Har qanday matn kelganda avtomatik musiqa qidirib, yuklab, Telegram'da yuborish
@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' Telegram'ga yuklanmoqda, iltimos kuting...")

    # Yuklab olish uchun vaqtinchalik papka sozlamalari
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    output_template = f"downloads/{chat_id}_%(title)s.%(ext)s"
    
    # yt-dlp sozlamalari
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': output_template,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
            
        # downloads papkasidan ushbu foydalanuvchiga tegishli faylni qidiramiz
        files = os.listdir("downloads")
        user_file = None
        for f in files:
            if f.startswith(f"{chat_id}_"):
                user_file = f
                break

        if user_file:
            file_path = os.path.join("downloads", user_file)
            
            # Sarlavhadan chat_id va kengaytmani tozalaymiz
            clean_title = re.sub(r'^\d+_\s*', '', user_file)
            clean_title = os.path.splitext(clean_title)[0]

            # Tugma qo'shish
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("👤 Admin bilan bog'lanish", url="https://t.me"))

            # Musiqani Telegram'ga yuborish
            with open(file_path, 'rb') as audio:
                bot.send_audio(
                    chat_id, 
                    audio, 
                    title=clean_title, 
                    performer="Music Bot",
                    caption="🎵 Musiqangiz tayyor!\n\n🚀 @Ismoiljanov_7 boti orqali yuklandi.",
                    reply_markup=markup
                )
                
            # Vaqtinchalik faylni o'chiramiz
            os.remove(file_path)
            bot.delete_message(chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Kechirasiz, musiqani yuklashda xatolik bo'ldi. Boshqa nom yozing.", chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        bot.edit_message_text("⚠️ Musiqa topilmadi yoki yuklash imkoni bo'lmadi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

# Botni doimiy o'chmasdan ishlashini ta'minlovchi kod (Polling)
bot.infinity_polling()
