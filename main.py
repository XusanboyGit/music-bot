import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# YANGI BOT TOKENINGIZ
TOKEN = "8961484963:AAFWzNThapXfIE0X2iaDylqm08NO6dDZMq8"
bot = telebot.TeleBot(TOKEN)

print("Musiqa yuklovchi bot muvaffaqiyatli ishga tushdi...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yoki ijrochini yozing, men uni yuklab beraman!"
    )

@bot.message_handler(func=lambda message: True)
def search_and_send_audio(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda va yuklanmoqda...")
    output_filename = f"{chat_id}_music.mp3"

    # yt-dlp sozlamalari
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1:',
        'outtmpl': output_filename.replace('.mp3', '.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                video_info = info['entries'][0]
            else:
                video_info = info
            
            title = video_info.get('title', query)
            uploader = video_info.get('uploader', 'Music Bot')

        # Admin bilan bog'lanish tugmasi
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("👤 Admin bilan bog'lanish", url="https://t.me/Ismoiljanov_7"))

        # Audioni yuborish
        with open(output_filename, "rb") as audio_file:
            bot.send_audio(
                chat_id, 
                audio_file, 
                title=title,
                performer=uploader,
                caption=f"🎵 Musiqangiz tayyor!\n\n🚀 @Ismoiljanov_7 boti orqali yuklandi.",
                reply_markup=markup
            )
        
        bot.delete_message(chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Xatolik: {e}")
        bot.edit_message_text("❌ Kechirasiz, bu nom bo'yicha musiqa topilmadi yoki yuklashda xatolik yuz berdi.", chat_id, status_msg.message_id)

    finally:
        # Vaqtinchalik fayllarni o'chirish
        if os.path.exists(output_filename):
            os.remove(output_filename)
        base_name = f"{chat_id}_music"
        for ext in ['.webm', '.m4a', '.mp3']:
            f_path = base_name + ext
            if os.path.exists(f_path):
                os.remove(f_path)

bot.infinity_polling()
