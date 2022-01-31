import logging
import config
import mysql
import keyboards as kb
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.executor import start_polling
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

logging.basicConfig(level=logging.INFO)
bot = config.bot  # Задаем настройки для бота
dp = Dispatcher(bot, storage=MemoryStorage())  # Передаем настройки в диспетчер
dp.middleware.setup(LoggingMiddleware())  # Включаем логирование


class reg(StatesGroup):  # Статусы-состояния-шаги
    notReg = State()
    notRegNum = State()
    notRegPos = State()
    registred = State()
    driver = State()
    oper = State()
    operloaddock = State()
    checkDock = State()


r = reg.registred
rd = reg.driver
ro = reg.oper
docData = {}


@dp.message_handler()  # Ловим первое сообщение пользователя и присваевам статус-шаг
async def start(message: types.Message):
    if mysql.checkUser(message.chat.id) == None:
        await reg.notReg.set()
        await bot.send_message(message.chat.id, 'Здравствуйте, вас нет в базе, перед использование бота необходимо '
                                                'зарегестрироватся, пожалуйста введите ФИО')
    else:
        if mysql.checkUser(message.chat.id)['groupmember'] == 2:
            await ro.set()
            key = kb.markup_OP_main
        else:
            await rd.set()
            key = kb.markup_Driver_main
        await bot.send_message(message.chat.id,
                               'Добро пожаловать {0}!'.format(mysql.checkUser(message.chat.id)['name']),
                               reply_markup=key)


@dp.message_handler(state=reg.notReg, regexp='^.*?\s.*?\s.*?$')
async def fio(message: types.Message, state: FSMContext):
    await message.reply("Отправте номер телефона.", reply_markup=kb.markup_requestTelNum)
    async with state.proxy() as data:
        data['name'] = message.text
    await reg.notRegNum.set()


@dp.message_handler(state=reg.notRegNum, content_types=["contact"])
async def fio(message: types.Message, state: FSMContext):
    await message.reply("Выберите должность", reply_markup=kb.markup_requespos)
    async with state.proxy() as data:
        data['contact'] = message.contact.phone_number
    await reg.notRegPos.set()


@dp.message_handler(state=reg.notRegNum)
async def fio(message: types.Message):
    await message.reply("Отправте свой контакт!", reply_markup=kb.markup_requestTelNum)
    await reg.notRegNum.set()


@dp.message_handler(state=reg.notReg)
async def errorFIO(message: types.Message):
    await message.reply('пожалуйста введите ФИО\n(Например: Иванов Иван Иванович)')


@dp.message_handler(lambda message: message.text not in ["Водитель", "Оператор"], state=reg.notRegPos)
async def takePos(message: types.Message):
    await message.reply("Выберите должность", reply_markup=kb.markup_requespos)


@dp.message_handler(state=reg.notRegPos)  # Завершаем регистрацию
async def finreg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pos'] = message.text
    if data['pos'] == 'Водитель':
        pos = 3
        await rd.set()
    else:
        pos = 2
        await ro.set()
    mysql.AddUserDB(message.chat.id, str(data['name']).replace('\n', '').strip(), pos,
                    data['contact'])  # Вносим пользователя в базу
    if mysql.checkUser(message.chat.id)['groupmember'] == 2:
        await ro.set()
        key = kb.markup_OP_main
    else:
        await rd.set()
        key = kb.markup_Driver_main
    await message.reply('Благодарим за регистрацию', reply_markup=key)


@dp.callback_query_handler(lambda c: c.data in 'cancel', state=('*'))  # ловим нажатие кнопки "Отмена"
async def cancel(callback_query: types.CallbackQuery):
    if mysql.checkUser(callback_query.from_user.id)['groupmember'] == 2:
        await ro.set()
        key = kb.markup_OP_main
    else:
        await rd.set()
        key = kb.markup_Driver_main


@dp.message_handler(lambda message: message.text == 'Загрузить документы', state=ro)  # загрузка документов
async def loadDoc(message: types.Message):
    await reg.operloaddock.set()
    await bot.send_message(message.chat.id, "Выберите сотрудника", reply_markup=kb.markup_OP_loadDockDrivers)


@dp.message_handler(state=reg.operloaddock, content_types=["text"])
async def pickDriver(message: types.Message):
    await bot.send_message(message.chat.id, 'Выберите водителя:', reply_markup=kb.markup_OP_loadDockDrivers)


@dp.callback_query_handler(lambda c: 'load_doc' in c.data, state=reg.operloaddock)
async def loadDock(callback_query: types.CallbackQuery):
    docData['id'] = (str(callback_query.data).split(':')[1])
    await bot.send_message(callback_query.from_user.id, 'Зазгрузите документ!')


@dp.message_handler(state=reg.operloaddock, content_types=["document"])  # Завершение загрузки
async def echo(message: types.Message):
    await ro.set()
    docData['name'] = message.document.file_name
    docData['tgID'] = message.document.file_id
    mysql.AddDocDB(docData['id'], docData['name'], docData['tgID'])  # пишем документ в базу
    await bot.send_message(message.chat.id, 'Документ успешно загружен!', reply_markup=kb.markup_OP_main)


# Просмотр документов оператором
@dp.message_handler(lambda message: message.text == 'Простомотреть документы', state=ro)
async def checkDock(message: types.Message):
    await reg.checkDock.set()
    await bot.send_message(message.chat.id, 'Выберите водителя:', reply_markup=kb.markup_OP_loadDockDrivers)


@dp.callback_query_handler(lambda c: 'load_doc' in c.data, state=reg.checkDock)
async def checkDock(callback_query: types.CallbackQuery):
    docData['id'] = (str(callback_query.data).split(':')[1])
    markup_OP_CheckDocs = InlineKeyboardMarkup()
    for docs in mysql.checkDocIDdriver(docData['id']):
        markup_OP_CheckDocs.add(
            InlineKeyboardButton(text=docs['name'], callback_data='doc:{0}'.format(docs['id'])))
    markup_OP_CheckDocs.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    await ro.set()
    await bot.send_message(callback_query.from_user.id, 'Выберите документ:', reply_markup=markup_OP_CheckDocs)


@dp.callback_query_handler(lambda c: 'doc:' in c.data, state=('*'))
async def loadDock(callback_query: types.CallbackQuery):
    docData['id'] = (str(callback_query.data).split(':')[1])
    await bot.send_document(callback_query.from_user.id, mysql.checkDocID(docData['id'])['tgID'])


@dp.message_handler(lambda message: message.text == 'Просмотреть сотрудников', state=ro)
async def allusers(message: types.Message):
    userlist = ''
    for users in mysql.allusers():
        if users['groupmember'] == 2:
            pos = 'Оператор'
        else:
            pos = 'Водитель'
        userlist = userlist + '{0}\n{1}\n{2}\n***************\n'.format(pos, users['name'], users['Contacts'])
    await bot.send_message(message.chat.id, userlist, reply_markup=kb.markup_OP_main)


@dp.message_handler(lambda message: message.text == 'Просмотреть сотрудников', state=rd)
async def allusers(message: types.Message):
    userlist = ''
    for users in mysql.allusers():
        if users['groupmember'] == 2:
            pos = 'Оператор'
        else:
            pos = 'Водитель'
        userlist = userlist + '{0}\n{1}\n{2}\n***************\n'.format(pos, users['name'], users['Contacts'])
    await bot.send_message(message.chat.id, userlist, reply_markup=kb.markup_Driver_main)


@dp.message_handler(lambda message: message.text == 'Просмотреть автомобили', state=ro)
async def allcars(message: types.Message):
    carslist = ''
    for cars in mysql.allcars():
        carslist = carslist + '{0}\n{1}\nДата последнего ТО: {2}\nВодитель\n{3}\n***************\n'.format(cars['name'],
                                                                                                           cars[
                                                                                                               'gosNom'],
                                                                                                           cars[
                                                                                                               'lastTO'],
                                                                                                           mysql.checkUser(
                                                                                                               cars[
                                                                                                                   'idDriver'])[
                                                                                                               'name'])
    await bot.send_message(message.chat.id, carslist, reply_markup=kb.markup_OP_main)


@dp.message_handler(lambda message: message.text == 'Простомотреть мои автомобили', state=rd)
async def allusers(message: types.Message):
    carslist = ''
    for cars in mysql.carsDriver(message.chat.id):
        carslist = carslist + '{0}\n{1}\n{2}\nВодитель\n{3}\n***************\n'.format(cars['name'], cars['gosNom'],
                                                                                       cars['lastTO'], mysql.checkUser(
                cars['idDriver'])['name'])
    if carslist != '':
        await bot.send_message(message.chat.id, carslist, reply_markup=kb.markup_Driver_main)
    else:
        await bot.send_message(message.chat.id, 'Нет автомобилей', reply_markup=kb.markup_Driver_main)


@dp.message_handler(lambda message: message.text == 'Просмотреть мои документы', state=rd)
async def checkDock(message: types.Message):
    markup_OP_CheckDocs = InlineKeyboardMarkup()
    for docs in mysql.checkDocIDdriver(message.chat.id):
        markup_OP_CheckDocs.add(
            InlineKeyboardButton(text=docs['name'], callback_data='doc:{0}'.format(docs['id'])))
    markup_OP_CheckDocs.add(InlineKeyboardButton(text='Отмена', callback_data='cancel'))
    await bot.send_message(message.chat.id, 'Выберите документ:', reply_markup=markup_OP_CheckDocs)


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
