import os
import re
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# BOT TOKENINGIZ
TOKEN = "8981526249:AAFgRy_t3DFIiRYRYzYWgJ3ZhdZfe0exRZY"
bot = telebot.TeleBot(TOKEN)

print("Musiqa yuklovchi bot muvaffaqiyatli ishga tushdi...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni Telegram'ga yuklab beraman!"
    )

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda va yuklanmoqda...")

    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    output_template = f"downloads/{chat_id}_%(title)s.%(ext)s"
    
    # Kengaytirilgan va xavfsiz yt-dlp sozlamalari
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': output_template,
        # Blokirovkadan qochish uchun standart brauzer parodiyasi
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
            
        files = os.listdir("downloads")
        user_file = None
        for f in files:
            if f.startswith(f"{chat_id}_"):
                user_file = f
                break

        if user_file:
            file_path = os.path.join("downloads", user_file)
            
            # Fayl nomidan chat_id ni tozalash
            clean_title = re.sub(r'^\d+_\s*', '', user_file)
            clean_title = os.path.splitext(clean_title)[0]

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("👤 Admin", url="https://t.me"))

            # Faylni audio qilib yuborish
            with open(file_path, 'rb') as audio:
                bot.send_audio(
                    chat_id, 
                    audio, 
                    title=clean_title, 
                    performer="Music Bot",
                    caption="🎵 Musiqangiz tayyor!\n\n🚀 @Ismoiljanov_7 boti orqali yuklandi.",
                    reply_markup=markup
                )
                
            os.remove(file_path)
            bot.delete_message(chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Fayl yuklandi, ammo tizimdan topilmadi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

    except Exception as e:
        # Xatolik panel logida ko'rinishi uchun konsolga chiqaramiz
        print(f"!!! YUKLASHDA XATOLIK: {str(e)}")
        bot.edit_message_text(f"⚠️ Yuklashda xatolik bo'ldi.\nSabab: {str(e)[:50]}...", chat_id, status_msg.message_id)

bot.infinity_polling()
