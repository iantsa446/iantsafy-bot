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
        bot.send_message(
            chat_id,
            "Faly miarahaba anao!"

            "🔒 Ampidiro azafady ny teny miafina: **iantsafybot12**"
        )
    else:
        show_main_options(chat_id)

@bot.message_handler(func=lambda msg: msg.text == confirmation_code)
def confirm_user(msg):
    chat_id = msg.chat.id
    confirmed_users.add(chat_id)
    bot.send_message(chat_id, "✅ Teny miafina nekena. Afaka manohy ianao.")
    show_main_options(chat_id)

def show_main_options(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("/simple", "/script")
    bot.send_message(
        chat_id,
        "⏩ Safidio aloha ny fomba tianao:"
"➡️ /simple — Torolalana tsotra"
"➡️ /script — Kaody feno amin'ny Python",
        reply_markup=markup
    )

@bot.message_handler(commands=['simple', 'script'])
def offer_language_options(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("/mg", "/fr")
    bot.send_message(
        message.chat.id,
        "🌍 Safidio amin'ny fiteny inona no tianao handefasana izany:",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, lambda msg: forward_to_display(message, msg.text))

def forward_to_display(original, lang):
    user_lang[original.chat.id] = 'mg' if lang == '/mg' else 'fr'
    cmd = original.text.replace("/", "")
    if cmd == "simple":
        send_simple(original)
    else:
        send_script(original)



def send_simple(message):
    lang = user_lang.get(message.chat.id, 'fr')
    if lang == 'mg':
        text = (
            "\u1F680 Torolalana tsotra hanombohana:\n"
            "1. Mamoròna OpenAI account\n"
            "2. Maka API Key\n"
            "3. Script python tsotra:\n"
            "```python\n"
            "import openai\n"
            "openai.api_key = 'KEY'\n"
            "res = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{\"role\": \"user\", \"content\": \"Salama\"}])\n"
            "print(res.choices[0].message.content)\n"
            "```"
        )
    else:
        text = (
            "\u1F680 Guide simple:\n"
            "1. Crée un compte OpenAI\n"
            "2. Copie ta clé API\n"
            "3. Utilise ce code:\n"
            "```python\n"
            "import openai\n"
            "openai.api_key = 'clé'\n"
            "res = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{\"role\": \"user\", \"content\": \"Bonjour\"}])\n"
            "print(res.choices[0].message.content)\n"
            "```"
        )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['script'])
def send_script(message):
    lang = user_lang.get(message.chat.id, 'fr')
    msg = {
        'mg': "\U0001F4DC *Kaody feno amin'ny Python:*\n```bash\npip install openai python-dotenv\n```\n.env:\n```env\nOPENAI_API_KEY=sk-...\n```\nscript:\n```python\nimport os, openai\nfrom dotenv import load_dotenv\nload_dotenv()\nopenai.api_key = os.getenv(\"OPENAI_API_KEY\")\n...\n```",
        'fr': "\U0001F4DC *Code complet Python:*\n```bash\npip install openai python-dotenv\n```\n.env:\n```env\nOPENAI_API_KEY=sk-...\n```\nscript:\n```python\nimport os, openai\nfrom dotenv import load_dotenv\nload_dotenv()\nopenai.api_key = os.getenv(\"OPENAI_API_KEY\")\n...\n```"
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
