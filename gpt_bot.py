import telebot
import openai

openai.api_key = "OPENAI_API_KEY"
bot = telebot.TeleBot("TELEGRAM_BOT_TOKEN")

# Fitahirizana fiteny sy validation
user_lang = {}
confirmed_users = set()
confirmation_code = "iantsafybot12"

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    if chat_id not in confirmed_users:
        bot.send_message(chat_id,
            "🔐 Mba ampidiro ny **code d'accès** alohan'ny hanombohana:\n"
            "_(ampidiro mivantana: iantsafybot12)_")
    else:
        send_language_choice(chat_id)

@bot.message_handler(func=lambda msg: msg.text == confirmation_code)
def confirm_user(msg):
    chat_id = msg.chat.id
    confirmed_users.add(chat_id)
    bot.send_message(chat_id, "✅ Code confirmé avec succès !")
    send_language_choice(chat_id)

def send_language_choice(chat_id):
    bot.send_message(chat_id,
        "✨ Tongasoa! / Bienvenue!\n"
        "Safidio ny fiteninao / Choisis ta langue :\n"
        "➡️ /mg — Malagasy\n"
        "➡️ /fr — Français\n\n"
        "🛠️ Safidy:\n"
        "• /simple — Guide tsotra hanombohana\n"
        "• /script — Kaody feno sy ohatra")

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
        bot.send_message(message.chat.id,
            "🚀 *Manomboka amin’ny bot OpenAI tsotra*\n\n"
            "1. Sokafy ny [https://platform.openai.com](https://platform.openai.com)\n"
            "2. Maka API Key ➜ [API Keys](https://platform.openai.com/account/api-keys)\n"
            "3. Apetraho amin'ny script Python tsotra:\n"
            "```python\nimport openai\nopenai.api_key = 'API-NAO'\n"
            "val = input('Ianao: ')\nres = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': val}])\n"
            "print(res.choices[0].message.content)\n```", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id,
            "🚀 *Démarrer un bot OpenAI simplement*\n\n"
            "1. Crée ton compte : [https://platform.openai.com](https://platform.openai.com)\n"
            "2. Récupère ta clé ➜ [API Keys](https://platform.openai.com/account/api-keys)\n"
            "3. Utilise ce script simple:\n"
            "```python\nimport openai\nopenai.api_key = 'ta_clé'\n"
            "msg = input('Toi : ')\nres = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role': 'user', 'content': msg}])\n"
            "print(res.choices[0].message.content)\n```", parse_mode="Markdown")

@bot.message_handler(commands=['script'])
def send_script(message):
    lang = user_lang.get(message.chat.id, 'fr')
    if lang == 'mg':
        bot.send_message(message.chat.id,
            "📜 *Torolalana hamoronana bot OpenAI amin'ny Python:*\n\n"
            "1. Mametraka modules:\n```bash\npip install openai python-dotenv\n```\n"
            "2. Mamorona `.env`:\n```env\nOPENAI_API_KEY=\"API-nao\"\n```\n"
            "3. Kaody fototra:\n```python\nimport openai, os\nfrom dotenv import load_dotenv\n"
            "load_dotenv()\nopenai.api_key = os.getenv(\"OPENAI_API_KEY\")\n"
            "while True:\n    val = input(\"Ianao: \")\n    if val == 'exit': break\n"
            "    res = openai.ChatCompletion.create(model=\"gpt-3.5-turbo\", messages=[{\"role\": \"user\", \"content\": val}])\n"
            "    print(\"Bot:\", res.choices[0].message.content)\n```\n"
            "4. Alefaso:\n```bash\npython assistant.py\n```", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id,
            "📜 *Créer un assistant OpenAI avec Python:*\n\n"
            "1. Installe les libs:\n```bash\npip install openai python-dotenv\n```\n"
            "2. Crée un `.env`:\n```env\nOPENAI_API_KEY=\"ta_clé\"\n```\n"
            "3. Code:\n```python\nimport openai, os\nfrom dotenv import load_dotenv\n"
            "load_dotenv()\nopenai.api_key = os.getenv(\"OPENAI_API_KEY\")\n"
            "while True:\n    msg = input(\"Toi: \")\n    if msg == 'exit': break\n"
            "    res = openai.ChatCompletion.create(model=\"gpt-3.5-turbo\", messages=[{\"role\": \"user\", \"content\": msg}])\n"
            "    print(\"Bot:\", res.choices[0].message.content)\n```\n"
            "4. Lance-le:\n```bash\npython assistant.py\n```", parse_mode="Markdown")

@bot.message_handler(func=lambda msg: True)
def chat(msg):
    if msg.chat.id not in confirmed_users:
        return

    lang = user_lang.get(msg.chat.id, 'fr')
    system_message = {
        'mg': "Ianao dia assistant IA mahay miteny malagasy amin'ny fomba mazava, misy emoji, mahay manazava tsara.",
        'fr': "Tu es un assistant IA parlant français, clair, sympa et précis, avec des emojis."
    }

    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message[lang]},
                {"role": "user", "content": msg.text}
            ]
        )
        rep = res.choices[0].message.content
        bot.reply_to(msg, rep)
    except Exception as e:
        bot.reply_to(msg, f"⚠️ Erreur: {e}")

bot.polling()
