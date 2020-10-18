from AmizoneAPI import amizone_api
import config
import telebot
from telebot import types
bot = telebot.TeleBot(config.TOKEN)
amizone_api.login(config.amizone_id, config.amizone_password)
@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('sticker.webp','rb')
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	mon = types.KeyboardButton('Monday')
	tue = types.KeyboardButton('Tuesday')
	markup.add(mon, tue)
	bot.send_sticker(message.chat.id, sti)
	bot.send_message(message.chat.id, 'Попал к Мохиту? Не завидую(', reply_markup = markup)
	#bot.send_message(message.chat.id, amizone_api.getTimeTable('Monday'))
@bot.message_handler(content_types=['text'])
def otvetka(message):
	if message.chat.type == 'private':
		if message.text == 'Monday':
			bot.send_message(message.chat.id, amizone_api.getTimeTable('Monday'))
		elif message.text == 'Tuesday':
			bot.send_message(message.chat.id, amizone_api.getTimeTable('Tuesday'))
		else:
			bot.send_message(message.chat.id, 'Неизвестная команда')
bot.polling(none_stop=True)

input()