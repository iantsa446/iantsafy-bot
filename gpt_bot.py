import telebot
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

user_lang = {}
confirmed_users = set()
confirmation_code = "iantsafybot12"

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if chat_id not in confirmed_users:
        bot.send_message(chat_id, "🔐 Mba ampidiro ny **code d'accès**: iantsafybot12")
    else:
        send_language_choice(chat_id)

@bot.message_handler(func=lambda msg: msg.text == confirmation_code)
def confirm_user(msg):
    chat_id = msg.chat.id
    confirmed_users.add(chat_id)
    bot.send_message(chat_id, "✅ Code confirmé avec succès !")
    send_language_choice(chat_id)

def send_language_choice(chat_id):
    bot.send_message(chat_id, "\u2728 Tongasoa! / Bienvenue!\n➡️ /mg — Malagasy\n➡️ /fr — Français\n🛠️ Safidy: /simple | /script")

@bot.message_handler(commands=['mg'])
def set_lang_mg(message):
    user_lang[message.chat.id] = 'mg'
    bot.reply_to(message, "✅ Hiteny amin'ny teny **malagasy** aho.")

@bot.message_handler(commands=['fr'])
def set_lang_fr(message):
    user_lang[message.chat.id] = 'fr'
    bot.reply_to(message, "✅ Je vais parler en **français**.")

@bot.message_handler(commands=['simple'])
def send_simple(message):
    lang = user_lang.get(message.chat.id, 'fr')
    if lang == 'mg':
        bot.send_message(message.chat.id, "🚀 Torolalana tsotra hanombohana:\n1. Mamoròna OpenAI account\n2. Maka API Key\n3. Script python tsotra:\n```python\nimport openai\nopenai.api_key = 'KEY'\nres = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{{"role": "user", "content": "Salama"}}])\nprint(res.choices[0].message.content)\n```", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "🚀 Guide simple:\n1. Crée un compte OpenAI\n2. Copie ta clé API\n3. Utilise ce code:\n```python\nimport openai\nopenai.api_key = 'clé'\nres = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{{"role": "user", "content": "Bonjour"}}])\nprint(res.choices[0].message.content)\n```", parse_mode="Markdown")

@bot.message_handler(commands=['script'])
def send_script(message):
    lang = user_lang.get(message.chat.id, 'fr')
    msg = {
        'mg': "📜 *Kaody feno amin'ny Python:*\n```bash\npip install openai python-dotenv\n```\n.env:\n```env\nOPENAI_API_KEY=sk-...\n```\nscript:\n```python\nimport os, openai\nfrom dotenv import load_dotenv\nload_dotenv()\nopenai.api_key = os.getenv(\"OPENAI_API_KEY\")\n...\n```",
        'fr': "📜 *Code complet Python:*\n```bash\npip install openai python-dotenv\n```\n.env:\n```env\nOPENAI_API_KEY=sk-...\n```\nscript:\n```python\nimport os, openai\nfrom dotenv import load_dotenv\nload_dotenv()\nopenai.api_key = os.getenv(\"OPENAI_API_KEY\")\n...\n```"
    }
    bot.send_message(message.chat.id, msg[lang], parse_mode="Markdown")

@bot.message_handler(func=lambda msg: True)
def chat(msg):
    if msg.chat.id not in confirmed_users:
        return
    lang = user_lang.get(msg.chat.id, 'fr')
    sys_msg = {
        'mg': "Ianao dia assistant IA manampy amin'ny teny malagasy.",
        'fr': "Tu es un assistant IA qui répond clairement en français."
    }
    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": sys_msg[lang]},
                {"role": "user", "content": msg.text}
            ]
        )
        rep = res.choices[0].message.content
        bot.reply_to(msg, rep)
    except Exception as e:
        bot.reply_to(msg, f"⚠️ Error: {e}")

bot.polling()
