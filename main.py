import random
import telebot
import configparser
from telebot import types
from googletrans import Translator
from db import WordsDatabase
from variants import Variants

config = configparser.ConfigParser()
config.read('settings.ini')
TOKEN = config['BOT']['TOKEN']

bot = telebot.TeleBot(TOKEN)
database = WordsDatabase(name=config['DATABASE']['NAME'],
                         user=config['DATABASE']['USER'],
                         password=config['DATABASE']['PASSWORD'])
variants = Variants()
translator = Translator()


class ChatStateManager:
    def __init__(self):
        self.current_words = {}

    def set_words(self, chat_id, target_word, other_words):
        self.current_words[chat_id] = [target_word, other_words]

    def get_target_word(self, chat_id):
        try:
            return self.current_words.get(chat_id)[0]
        except (KeyError, TypeError):
            return None

    def get_other_words(self, chat_id):
        try:
            return self.current_words.get(chat_id)[1]
        except (KeyError, TypeError):
            return None


chat_state_manager = ChatStateManager()


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово ➖'
    NEXT = 'Дальше ⬆️'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_photo(chat_id, open('images/monkey_education.jpg', 'rb'))
    bot.send_message(chat_id, 'Привет!👋 Давай вместе учить испанский!📚')
    bot.send_message(chat_id, 'Введи /help для просмотра доступных команд ⚙️')


@bot.message_handler(commands=['help'])
def send_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Доступные команды:\n/start\n/help\n/cards')


@bot.message_handler(commands=['cards'])
def create_cards(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    chat_id = message.chat.id
    if not database.cycle:
        bot.send_message(chat_id, f'Ты прошёл весь круг, давай закрепим!👏')
        database.cycle = True
    if not database.remaining_main_words.get(chat_id) and not database.remaining_user_words.get(chat_id):
        database.get_remaining_words(chat_id)
    word_data = database.get_random_word(chat_id)
    russian_word = word_data[0][0]
    target_word = word_data[0][1]
    target_word_btn = types.KeyboardButton(target_word)
    other_words = word_data[1]
    chat_state_manager.set_words(chat_id, target_word, other_words)
    other_words_btns = [types.KeyboardButton(word) for word in other_words]
    buttons = [target_word_btn] + other_words_btns
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.ADD_WORD)
    add_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    delete_word_btn = types.KeyboardButton(Command.NEXT)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)
    bot.send_message(chat_id, f'Переведи слово "{russian_word}"',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)


@bot.message_handler(func=lambda message: chat_state_manager.
                     get_other_words(message.chat.id) and message.text in chat_state_manager.
                     get_other_words(message.chat.id) or message.text == chat_state_manager.
                     get_target_word(message.chat.id))
def message_reply(message):
    chat_id = message.chat.id
    current_target_word = chat_state_manager.get_target_word(chat_id)
    current_other_words = chat_state_manager.get_other_words(chat_id)
    if current_target_word and message.text == current_target_word:
        bot.send_message(chat_id, "Правильно!👍")
        create_cards(message)
    if message.text in current_other_words:
        bot.send_message(chat_id, "Неправильно, попробуй ещё раз!❌")


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Введи русское слово')
    bot.register_next_step_handler(msg, process_added_word)


def process_added_word(message):
    word_to_add = message.text.capitalize()
    chat_id = message.chat.id
    if word_to_add not in database.get_all_words(chat_id):
        translation = translator.translate(word_to_add, dest='spanish').text
        database.fill_table_users_words(word_to_add, translation, chat_id)
        word_id = database.get_user_word_id(word_to_add, chat_id)
        translations = variants.choose_variants()
        database.fill_table_users_words_variants(word_id, translations)
        bot.send_message(chat_id, f'Слово "{word_to_add}" успешно добавлено')
    else:
        bot.send_message(chat_id, f'Слово "{word_to_add}" уже есть')
        add_word(message)


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Какое слово нужно удалить?')
    bot.register_next_step_handler(msg, process_deleted_word)


def process_deleted_word(message):
    chat_id = message.chat.id
    word_to_delete = message.text.capitalize()
    if word_to_delete not in database.get_user_words(chat_id):
        bot.send_message(chat_id, 'Данное слово удалить нельзя')
        delete_word(message)
    else:
        database.delete_user_word(word_to_delete, chat_id)
        bot.send_message(chat_id, f'Слово {word_to_delete} успешно удалено')


if __name__ == '__main__':
    print('Start telegram bot...')
    bot.polling()
