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
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni tezkor yuklab beraman!"
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
                # Faqat audio turidagi kontentni olamiz
                if result.type == 'audio':
                    # Admin bilan bog'lanish tugmasi
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("👤 Admin bilan bog'lanish", url="https://t.me"))
                    
                    # Ortiqcha kanallar matnini o'chirib, faqat toza audioni yuborish
                    bot.send_audio(
                        chat_id, 
                        result.audio_file_id if hasattr(result, 'audio_file_id') else result.id,
                        caption=f"🎵 Musiqangiz tayyor!\n\n🚀 @Ismoiljanov_7 boti orqali yuklandi.",
                        reply_markup=markup
                    )
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
