import telebot
from telebot import types
import yt_dlp
import os
import glob

TOKEN = "8961484963:AAFWzNThapXfIE0X2iaDylqm08NO6dDZMq8"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni to'liq holatda yuklab beraman!"
    )

@bot.message_handler(content_types=['text'])
def search_and_send_audio(message):
    query = message.text.strip()
    status_msg = bot.send_message(message.chat.id, f"⏳ '{query}' qidirilmoqda va to'liq yuklanmoqda...")
    
    ydl_opts = {
        'format': 'ba[ext=m4a]/ba/b',
        'outtmpl': f'downloads/{message.chat.id}_%(id)s.%(ext)s',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': True
    }
    
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            
            search_pattern = f"downloads/{message.chat.id}_*"
            files = glob.glob(search_pattern)
            
            if files:
                audio_file_path = files[0]
                
                if 'entries' in info:
                    video_title = info['entries'][0].get('title', query)
                else:
                    video_title = info.get('title', query)
                
                inline_markup = types.InlineKeyboardMarkup()
                btn_owner = types.InlineKeyboardButton(text="👤 Admin bilan bog'lanish", url="https://t.me/Ismoiljanov_7")
                inline_markup.add(btn_owner)
                
                with open(audio_file_path, 'rb') as audio:
                    bot.send_audio(
                        chat_id=message.chat.id,
                        audio=audio,
                        title=video_title,
                        performer="Music Bot",
                        caption=f"🎵 Musiqangiz to'liq holda tayyor!\n\n🚀 @music_1_maktab_bot orqali yuklandi.",
                        reply_markup=inline_markup
                    )
                
                if os.path.exists(audio_file_path):
                    os.remove(audio_file_path)
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ Kechirasiz, musiqani topib bo'lmadi.", message.chat.id, status_msg.message_id)
                
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        bot.edit_message_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.", message.chat.id, status_msg.message_id)

print("Musiqa yuklovchi bot ishga tushdi...")
bot.infinity_polling()
