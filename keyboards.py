from aiogram.types import ParseMode, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import mysql
markup_requestTelNum = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)

markup_requestLocation = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Отправить свою локацию 🗺️', request_location=True)
)

markup_requespos = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Водитель')
).add(KeyboardButton('Оператор'))

markup_Driver_main = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Просмотреть мои документы')).add(
    KeyboardButton('Простомотреть мои автомобили')).add(
    KeyboardButton('Просмотреть сотрудников'))

markup_OP_main = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Просмотреть сотрудников')).add(
    KeyboardButton('Простомотреть документы')).add(
    KeyboardButton('Просмотреть автомобили')).add(
    KeyboardButton('Загрузить документы'))

markup_OP_loadDockDrivers = InlineKeyboardMarkup()
for users in mysql.users('3'):
    markup_OP_loadDockDrivers.add(InlineKeyboardButton(text=users['name'],callback_data='load_dock:{0}'.format(users['id'])))
markup_OP_loadDockDrivers.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))

markup_Ruk = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Посмотреть')
).add(KeyboardButton('2')).add(KeyboardButton('3'))

keyboard = InlineKeyboardMarkup()
url_button = InlineKeyboardButton(text="555", callback_data='hjgsk')
keyboard.add(url_button)