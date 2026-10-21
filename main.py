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
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni tezkor va cheklovsiz yuklab beraman!"
    )

@bot.message_handler(func=lambda message: True)
def search_and_send_audio(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda...")

    try:
        # Telegram ichki musiqa bazasidan qidirish (@music bot tizimi orqali)
        inline_results = bot.get_inline_bot_results("music", query)
        
        audio_found = False
        if inline_results and inline_results.results:
            for result in inline_results.results:
                # Faqat audio (audio yoki document) turidagi faylni qidiramiz
                if result.type == 'audio' or hasattr(result, 'audio_url'):
                    # Admin tugmasi
                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("👤 Admin", url="https://t.me"))
                    
                    # Topilgan audioni foydalanuvchiga to'g'ridan-to'g'ri ulashamiz
                    bot.send_audio(
                        chat_id, 
                        result.audio_url if hasattr(result, 'audio_url') else result.input_message_content.message_text,
                        caption=f"🎵 '{query}' qidiruvi bo'yicha topildi.\n\n🚀 @Ismoiljanov_7 boti orqali uzatildi.",
                        reply_markup=markup
                    )
                    audio_found = True
                    break
            
            if audio_found:
                bot.delete_message(chat_id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ Kechirasiz, ushbu nom bo'yicha audio fayl topilmadi. Boshqa nom yozib ko'ring.", chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Afsuski, qidiruv natijasi bo'sh chiqdi. Nomni aniqroq yozing.", chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Xatolik: {e}")
        bot.edit_message_text("⚠️ Qidiruv tizimida vaqtinchalik muammo bo'ldi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

bot.infinity_polling()
