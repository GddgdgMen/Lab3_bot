import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from groq import Groq

client = Groq(
    api_key="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"
)
API_Token = '7425953231:AAEe4g4wbadfNkdSVpi8Uu-mf8tK4QM9Qu8'

def get_groq_response(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-70b-8192",
    )

    return str(chat_completion.choices[0].message.content)

bot = telebot.TeleBot(API_Token)

# Start command with main menu
@bot.message_handler(commands=['start'])
def send_welcome(message):
    main_menu(message)

# Main menu function
def main_menu(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Student Info", callback_data="student"),
        InlineKeyboardButton("Technologies", callback_data="tech"),
        InlineKeyboardButton("Contact", callback_data="contact"),
        InlineKeyboardButton("Ask Groq", callback_data="groq")
    )
    bot.send_message(
        message.chat.id,
        "Welcome! Please choose an option:",
        reply_markup=markup
    )

# Handle inline button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "student":
        send_submenu(call, "Svirskyi Anton IM-12")
    elif call.data == "tech":
        send_submenu(call, "*Technologies:* Front-end, Back-end", parse_mode="Markdown")
    elif call.data == "contact":
        send_submenu(call, "tel: 093 687 8762, e-mail: antonsvirskyi@gmail.com")
    elif call.data == "groq":
        ask_groq_menu(call)
    elif call.data == "back":
        main_menu(call.message)

# Submenu function with "Back" button
def send_submenu(call, text, parse_mode=None):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Back", callback_data="back"))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup,
        parse_mode=parse_mode
    )

# Groq submenu to accept user input
def ask_groq_menu(call):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Back", callback_data="back"))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Send me your query for Groq:",
        reply_markup=markup
    )
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_groq_query)

# Process user input for Groq
def process_groq_query(message):
    response = get_groq_response(message.text)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Back", callback_data="back"))
    bot.send_message(
        message.chat.id,
        f"Groq Response:\n{response}",
        reply_markup=markup
    )

# Echo other text messages
@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_all(message):
    response = get_groq_response(message.text)
    bot.send_message(message.chat.id, str(response))

bot.polling()
