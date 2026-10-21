import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# TOKENINGIZ
TOKEN = "8961484963:AAFWzNThapXfIE0X2iaDylqm08NO6dDZMq8"
bot = telebot.TeleBot(TOKEN)

print("Musiqa yuklovchi bot ishga tushdi...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Salom {message.from_user.first_name}! 🎵\n\nMusiqa nomini yozing, men uni topib beraman!"
    )

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ '{query}' qidirilmoqda...")

    try:
        # Telegramning o'shbu ommaviy music botlari orqali qidirish
        results = bot.get_inline_bot_results("@lybot", query)
        
        if results and results.results:
            # Birinchi topilgan audioni olamiz
            audio_result = None
            for res in results.results:
                if res.type == 'audio':
                    audio_result = res
                    break
            
            if audio_result:
                # Admin tugmasi
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("👤 Admin bilan bog'lanish", url="https://t.me/Ismoiljanov_7"))
                
                # Audioni to'g'ridan-to'g'ri jo'natish
                bot.send_audio(
                    chat_id,
                    audio_result.audio_url,
                    title=audio_result.title,
                    performer=getattr(audio_result, 'performer', 'Music Bot'),
                    caption=f"🎵 Musiqangiz tayyor!\n\n🚀 @Ismoiljanov_7 boti orqali topildi.",
                    reply_markup=markup
                )
                bot.delete_message(chat_id, status_msg.message_id)
                return

        bot.edit_message_text("❌ Kechirasiz, bu nom bo'yicha musiqa topilmadi. Boshqa nom yozib ko'ring.", chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Xatolik: {e}")
        bot.edit_message_text("❌ Qidirish vaqtida xatolik yuz berdi. Qaytadan urinib ko'ring.", chat_id, status_msg.message_id)

bot.infinity_polling()
