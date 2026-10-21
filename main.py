import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8961484963:AAFWzNThapXfIE0X2iaDylqm08NO6dDZMq8"
bot = telebot.TeleBot(TOKEN)

print("Bot musicale avviato correttamente...")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Ciao {message.from_user.first_name}! 🎵\n\nScrivi il nome di qualsiasi canzone o artista e la troverò per te!"
    )

@bot.message_handler(func=lambda message: True)
def search_and_send_music(message):
    query = message.text.strip()
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, f"⏳ Ricerca di '{query}' in corso...")

    try:
        # Ricerca tramite API Deezer (supporta tutti i brani famosi e commerciali)
        search_url = f"https://api.deezer.com/search?q={query}&limit=1"
        response = requests.get(search_url).json()

        if response.get('data') and len(response['data']) > 0:
            track = response['data'][0]
            audio_url = track['preview']  # Anteprima audio MP3 di alta qualità
            title = track['title']
            performer = track['artist']['name']

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("👤 Contatta l'Amministratore", url="https://t.me/Ismoiljanov_7"))

            bot.send_audio(
                chat_id,
                audio_url,
                title=title,
                performer=performer,
                caption=f"🎵 La tua musica è pronta!\n\n🚀 Scaricato tramite @music_1_maktab_bot",
                reply_markup=markup
            )
            bot.delete_message(chat_id, status_msg.message_id)
        else:
            bot.edit_message_text("❌ Nessun brano trovato con questo nome. Prova con un altro nome.", chat_id, status_msg.message_id)

    except Exception as e:
        print(f"Errore: {e}")
        bot.edit_message_text("❌ Si è verificato un errore durante la ricerca. Riprova.", chat_id, status_msg.message_id)

bot.infinity_polling()
