import os
import requests
import telebot
from youtube_search import YoutubeSearch

# BOT TOKENINGIZ
TOKEN = "8981526249:AAFgRy_t3DFIiRYRYzYWgJ3ZhdZfe0exRZY"
bot = telebot.TeleBot(TOKEN)

print("Musiqa yuklovchi bot muvaffaqiyatli ishga tushdi...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni yuklab beraman!"
    )

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda...")

    try:
        # YouTube qidiruv tizimi (Blokirovkasiz oddiy matnli qidiruv)
        results = YoutubeSearch(query, max_results=1).to_dict()
        
        if results:
            video_id = results[0]['id']
            track_title = results[0]['title']
            
            bot.edit_message_text(f"🚀 '{track_title}' Telegram'ga yuklanmoqda...", chat_id, status_msg.message_id)

            # Ochiq va cheklovsiz yuklash API xizmati
            api_url = f"https://vexdw.org{video_id}"
            download_response = requests.get(api_url).json()
            
            if download_response.get("status") == "success":
                audio_url = download_response["data"]["link"]
                
                # Audio faylni server xotirasiga vaqtincha yuklab olish
                audio_data = requests.get(audio_url).content
                file_name = f"{chat_id}_music.mp3"
                
                with open(file_name, "wb") as f:
                    f.write(audio_data)

                # Telegram'ga to'g'ridan-to'g'ri yuborish
                with open(file_name, "rb") as audio_file:
                    bot.send_audio(
                        chat_id, 
                        audio_file, 
                        title=track_title, 
                        performer="Music Bot",
                        caption=f"🎵 {track_title}\n\n🚀 Bot muvaffaqiyatli yukladi!"
                    )

                # Ishlatib bo'lingan vaqtinchalik faylni o'chirish
                if os.path.exists(file_name):
                    os.remove(file_name)
                    
                bot.delete_message(chat_id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ Musiqani yuklab olish havolasini yaratishda xatolik bo'ldi. Boshqa nom yozing.", chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Kechirasiz, bunday nomli musiqa topilmadi.", chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Xatolik: {e}")
        bot.edit_message_text("⚠️ Musiqani qidirishda ichki xatolik yuz berdi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

bot.infinity_polling()
