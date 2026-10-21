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
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni to'liq holatda topib yuklab beraman!"
    )

@bot.message_handler(content_types=['text'])
def search_and_send_audio(message):
    query = message.text.strip()
    chat_id = message.chat.id
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda va yuklanmoqda...")
    
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': f'downloads/{chat_id}_%(id)s.%(ext)s',
        'default_search': 'scsearch5',
        'noplaylist': True,
        'quiet': True,
        'ignoreerrors': True
    }
    
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
            if not info or ('entries' in info and not info['entries']):
                bot.edit_message_text("❌ Kechirasiz, bu nom bo'yicha musiqa topilmadi.", chat_id, status_msg.message_id)
                return

            entries = info.get('entries', [info])
            selected_entry = None
            
            for entry in entries:
                if entry:
                    title = entry.get('title', '').lower()
                    if 'join' not in title and 'channel' not in title and 'bot' not in title:
                        selected_entry = entry
                        break
            
            if not selected_entry:
                selected_entry = entries[0]

            ydl.download([selected_entry['webpage_url']])
            
            search_pattern = f"downloads/{chat_id}_*"
            files = glob.glob(search_pattern)
            
            if files:
                audio_file_path = files[0]
                video_title = selected_entry.get('title', query)
                uploader = selected_entry.get('uploader', 'Music Bot')
                
                inline_markup = types.InlineKeyboardMarkup()
                btn_owner = types.InlineKeyboardButton(text="👤 Admin bilan bog'lanish", url="https://t.me/Ismoiljanov_7")
                inline_markup.add(btn_owner)
                
                with open(audio_file_path, 'rb') as audio:
                    bot.send_audio(
                        chat_id=chat_id,
                        audio=audio,
                        title=video_title,
                        performer=uploader,
                        caption=f"🎵 Musiqangiz to'liq holda tayyor!\n\n🚀 @music_1_maktab_bot orqali yuklandi.",
                        reply_markup=inline_markup
                    )
                
                if os.path.exists(audio_file_path):
                    os.remove(audio_file_path)
                bot.delete_message(chat_id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ Kechirasiz, bu musiqani yuklab bo'lmadi.", chat_id, status_msg.message_id)
                
    except Exception as e:
        print(f"Xatolik: {e}")
        bot.edit_message_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

    finally:
        base_name = f"downloads/{chat_id}_"
        for f in glob.glob(base_name + '*'):
            if os.path.exists(f):
                os.remove(f)

print("Musiqa yuklovchi bot ishga tushdi...")
bot.infinity_polling()
