import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# BOT TOKENINGIZ
TOKEN = "8981526249:AAFgRy_t3DFIiRYRYzYWgJ3ZhdZfe0exRZY"
bot = telebot.TeleBot(TOKEN)

print("Musiqa yuklovchi bot muvaffaqiyatli ishga tushdi...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni ortiqcha reklamalarsiz yuklab beraman!"
    )

@bot.message_handler(func=lambda message: True)
def search_and_send_audio(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda...")

    try:
        # Telegram musiqa bazasidan inline qidiruv
        inline_results = bot.get_inline_bot_results("music", query)
        
        audio_sent = False
        if inline_results and inline_results.results:
            for result in inline_results.results:
                # Obyekt ichidan haqiqiy audio URL manzilini qidiramiz
                audio_url = None
                if hasattr(result, 'audio_url') and result.audio_url:
                    audio_url = result.audio_url
                elif hasattr(result, 'content_url') and result.content_url:
                    audio_url = result.content_url
                
                if audio_url:
                    bot.edit_message_text(f"🚀 '{query}' reklamalardan tozalanmoqda va yuklanmoqda...", chat_id, status_msg.message_id)
                    
                    # Audioni server xotirasiga vaqtincha yuklab olamiz (Bu reklamani butunlay o'chiradi)
                    audio_data = requests.get(audio_url).content
                    file_name = f"{chat_id}_clean_music.mp3"
                    
                    with open(file_name, "wb") as f:
                        f.write(audio_data)
                    
                    # Admin bilan bog'lanish tugmasi
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("👤 Admin bilan bog'lanish", url="https://t.me"))
                    
                    # Yangi toza fayl sifatida Telegram'ga yuklaymiz
                    with open(file_name, "rb") as audio_file:
                        bot.send_audio(
                            chat_id, 
                            audio_file, 
                            title=query,
                            performer="Music Bot",
                            caption=f"🎵 Musiqangiz tayyor!\n\n🚀 @Ismoiljanov_7 boti orqali yuklandi.",
                            reply_markup=markup
                        )
                    
                    # Vaqtinchalik faylni o'chirish
                    if os.path.exists(file_name):
                        os.remove(file_name)
                        
                    audio_sent = True
                    break
            
            if audio_sent:
                bot.delete_message(chat_id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ Kechirasiz, bu nom bo'yicha audio fayl topilmadi. Boshqa nom yozing.", chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Afsuski, hech narsa topilmadi. Qo'shiq nomini aniqroq yozing.", chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Xatolik: {e}")
        bot.edit_message_text("⚠️ Qidiruvda muammo bo'ldi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

bot.infinity_polling()
s
