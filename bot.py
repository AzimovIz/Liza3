import asyncio
import random
import sqlite3
import sys
import threading
import os
import time

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware



if 'tk.py' not in os.listdir():
    with open('tk.py', 'w') as file:
        file.write('tk = ')
    print('ERROR, write aiogram api-key in tk.py')
    exit()


from utils import States
from texts import *
from pars import *
from tk import tk
import kb
from conf import *
#from mytrello import MyTrello
from funcs import *
#from COM import MyDevises #arduino remote in development






bot = Bot(token=tk)
dp = Dispatcher(bot, storage=MemoryStorage())

#trello = MyTrello()

#device = [MyDevises('0', 'heater')]

@dp.callback_query_handler(lambda callback_query: True, state='*')
async def callback_inline(callback_query, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    if str(await state.get_state()) == 'States:rmkard':
        conector = sqlite3.connect(f'org/{callback_query.from_user.id}.db')
        cursor = conector.cursor()
        cursor.execute('SELECT * FROM kard')
        kards = cursor.fetchall()
        for i in kards:
            if callback_query.data == i[0]:
                cursor.execute(f'DELETE FROM kard WHERE id = "{i[0]}"')
                conector.commit()
                await bot.send_message(callback_query.from_user.id, f'Карта "{i[2]}" удалена')
                await state.finish()

    if callback_query.data == 'btnfun':
        inline_btn = InlineKeyboardMarkup().add(InlineKeyboardButton('React', callback_data='btnrct'),)
        #inline_btn.add(InlineKeyboardButton('Notes', callback_data='btnnts'),)
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=f'Список функций', reply_markup=inline_btn)

    if callback_query.data == 'exit':
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text='Меню настроек:', reply_markup=kb.inline_btn_set)


    if callback_query.data in ['btnrct', 'btnrct-', 'btnrct+', 'btnrct--', 'btnrct++', 'btnrctad', 'btnrctms',]:

        conector = sqlite3.connect(database)
        cursor = conector.cursor()
        cursor.execute('SELECT * FROM pic WHERE sended = "False"')
        id_f = cursor.fetchall()
        if callback_query.data == 'btnrct':
            pass

        if callback_query.data == 'btnrct-' or callback_query.data == 'btnrct--':
            if callback_query.data == 'btnrct-':
                timers['react'] = timers['react'] - 1
            if callback_query.data == 'btnrct--':
                timers['react'] = timers['react'] - 5
            if timers['react'] < 2:
                timers['react'] = 2

        if callback_query.data == 'btnrct+' or callback_query.data == 'btnrct++':
            if callback_query.data == 'btnrct+':
                timers['react'] = timers['react'] + 1

            if callback_query.data == 'btnrct++':
                timers['react'] = timers['react'] + 5

        if callback_query.data == 'btnrctms':
            if len(testr):
                testr.pop(-1)

        if callback_query.data == 'btnrctad':
            if len(testr):
                new_id = testr[-1]+1
            else:
                new_id = 0
            testr.append(new_id)
            dp._loop_create_task(react(new_id))

        text = f'React\n' \
                f'Количесво картинок: {len(id_f)}\n' \
                f'Текущее время задержки: {timers["react"]}\n' \
                f'Количество потоков: {len(testr)}(Рек. 1)'

        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=text, reply_markup=kb.inline_btn_rct)


    if callback_query.data in ['btnnts', 'btnnts-', 'btnnts+', 'btnnts--', 'btnnts++', 'btnntsad', 'btnntsms',]:

        num_notes = 0
        edit = True
        if callback_query.data == 'btnnts':
            pass

        if callback_query.data == 'btnnts-' or callback_query.data == 'btnnts--':
            if callback_query.data == 'btnnts-':
                timers['notes'] = timers['notes'] - 1
            if callback_query.data == 'btnnts--':
                timers['notes'] = timers['notes'] - 5
            if timers['notes'] < 2:
                timers['notes'] = 2
                edit = False

        if callback_query.data == 'btnnts+' or callback_query.data == 'btnnts++':
            if callback_query.data == 'btnnts+':
                timers['notes'] = timers['notes'] + 1

            if callback_query.data == 'btnnts++':
                timers['notes'] = timers['notes'] + 5


        if callback_query.data == 'btnntsms':
            if len(testn):
                testn.pop(-1)

        if callback_query.data == 'btnntsad':
            if len(testn):
                new_id = testn[-1]+1
            else:
                new_id = 0
            testn.append(new_id)
            dp._loop_create_task(notes(new_id))

        text = f'Notes\n' \
               f'Время цикла: {timers["notes"]}\n' \
               f'Количество заметок: {num_notes}\n' \
               f'Количество потоков: {len(testn)}(Рек. 1)'

        if edit:
            await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                        text=text, reply_markup=kb.inline_btn_nts)


    if callback_query.data in ['notearc', 'notead2', 'notead5', 'notead10', 'notead24']:
        text = callback_query.message.text
        text_ = str(text[(text.rfind('т: ') + 3):])

        if callback_query.data == 'notearc':
            trello.comleter(text_)
            await callback_query.message.delete()
        else:
            trello.uptime(text_,hours=int(callback_query.data[(callback_query.data.rfind('d') + 1):]))

    if callback_query.data in ['adurl',]:
        await bot.send_message(callback_query.from_user.id, "Введи новый URL\nИли список URLов через 'энтер'",
                               reply_markup=InlineKeyboardMarkup().add(kb.inline_btn_ex))
        await States.adurl.set()

    if callback_query.data in ['adpic',]:
        await bot.send_message(callback_query.from_user.id, "Кидай картинки)",
                               reply_markup=InlineKeyboardMarkup().add(kb.inline_btn_ex))
        await States.adpic.set()

    if callback_query.data in ['rmurl',]:
        conector = sqlite3.connect(database)
        cursor = conector.cursor()
        cursor.execute(f"SELECT * from urls")
        urls = cursor.fetchall()
        inline_btn_url = InlineKeyboardMarkup()
        for i in range(len(urls)):
            inline_btn_url.add(InlineKeyboardButton(urls[i][0], callback_data=urls[i][0]))

        await bot.send_message(callback_query.from_user.id, "Список урлов:", reply_markup=inline_btn_url)

    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    cursor.execute(f"SELECT * from urls")
    urls = cursor.fetchall()
    for i in range(len(urls)):
        if callback_query.data == urls[i][0]:
            try:
                cursor.execute(f'DELETE FROM urls WHERE url = "{urls[i][0]}"')
                conector.commit()

                cursor.execute(f"SELECT * from urls")
                urls = cursor.fetchall()
                inline_btn_url = InlineKeyboardMarkup()
                for i in range(len(urls)):
                    inline_btn_url.add(InlineKeyboardButton(urls[i][0], callback_data=str(urls[i][0])))

                await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                            message_id=callback_query.message.message_id,
                                            text="Список урлов:",
                                            reply_markup=inline_btn_url)

                await bot.send_message(callback_query.from_user.id,
                                       f"URL: {callback_query.data} удален!",
                                       disable_web_page_preview=True)
            except Exception as er:
                await bot.send_message(callback_query.from_user.id,
                                       f"URL: {callback_query.data} НЕ удален!\nОшибка: {er}",
                                       disable_web_page_preview=True)


@dp.message_handler(state='*', commands=['start'])
async def start_command(message):
    await bot.send_message(message.chat.id, "Привет")

'''
@dp.message_handler(state='*', commands=['notes'])
async def start_command(message):
    inline_btns_n = InlineKeyboardMarkup()
    for i in trello.get_notes():
        inline_btns_n.add(InlineKeyboardButton(f'{i[0]}', callback_data=f'{i[0]}'))
    await bot.send_message(message.chat.id, "Список заметок", reply_markup=inline_btns_n)'''


@dp.message_handler(state='*', commands=['set_pic'])
async def set_p(message):
    if str(message.from_user.id) in msg['adm']:
        conector = sqlite3.connect(database)
        cursor = conector.cursor()
        try:
            cursor.execute(f"INSERT INTO chanels VALUES (?, ?)",
                           (str(message.chat.id), 'pic'))
            conector.commit()
            await bot.send_message(message.chat.id, "Теперь сдесь будут картинки)")
            await logging(f'Чат {message.chat.title} добавлен для картинок.')
        except:
            cursor.execute("SELECT * FROM chanels")
            id_f = cursor.fetchall()
            for i in range(len(id_f)):
                if id_f[i][0] == str(message.chat.id):
                    id_ft = id_f[i][1]
                    try:
                        cursor.execute(f"UPDATE chanels SET dest = (?) WHERE id = {str(message.chat.id)}", (id_ft+' pic',))
                        conector.commit()
                        await bot.send_message(message.chat.id, "Теперь сдесь будут ещё и картинки)")
                        await logging(f'Чат {message.chat.title} добавлен для картинок.')
                    except:
                        await bot.send_message(message.chat.id, "Что то пошло не так(")
                        await logging(f'Ошибка. Чат {message.chat.title} НЕ добавлен для картинок.')
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['set_log'])
async def set_l(message):
    if str(message.from_user.id) in msg['adm']:
        conector = sqlite3.connect(database)
        cursor = conector.cursor()
        try:
            cursor.execute(f"INSERT INTO chanels VALUES (?, ?)",
                           (str(message.chat.id), 'log'))
            conector.commit()
            await bot.send_message(message.chat.id, "Теперь сдесь будут логи)")
            await logging(f'Чат {message.chat.title} добавлен для логирования.')
        except:
            cursor.execute("SELECT * FROM chanels")
            id_f = cursor.fetchall()
            for i in range(len(id_f)):
                if id_f[i][0] == str(message.chat.id):
                    id_ft = id_f[i][1]
                    try:
                        cursor.execute(f"UPDATE chanels SET dest = (?) WHERE id = {str(message.chat.id)}",
                                       (id_ft + ' log',))
                        conector.commit()
                        await bot.send_message(message.chat.id, "Теперь сдесь будут ещё и логи)")
                        await logging(f'Чат {message.chat.title} добавлен для логирования.')
                    except:
                        await bot.send_message(message.chat.id, "Что то пошло не так(")
                        await logging(f'Ошибка. Чат {message.chat.title} НЕ добавлен для логирования.')
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['set_note'])
async def set_n(message):
    if str(message.from_user.id) in msg['adm']:
        conector = sqlite3.connect(database)
        cursor = conector.cursor()
        try:
            cursor.execute(f"INSERT INTO chanels VALUES (?, ?)",
                           (str(message.chat.id), 'note'))
            conector.commit()
            await bot.send_message(message.chat.id, "Теперь сдесь будут заметки)")
            await logging(f'Чат {message.chat.title} добавлен для заметок.')
        except:
            cursor.execute("SELECT * FROM chanels")
            id_f = cursor.fetchall()
            for i in range(len(id_f)):
                if id_f[i][0] == str(message.chat.id):
                    id_ft = id_f[i][1]
                    try:
                        cursor.execute(f"UPDATE chanels SET dest = (?) WHERE id = {str(message.chat.id)}", (id_ft+' note',))
                        conector.commit()
                        await bot.send_message(message.chat.id, "Теперь сдесь будут ещё и заметки)")
                        await logging(f'Чат {message.chat.title} добавлен для заметок.')
                    except:
                        await bot.send_message(message.chat.id, "Что то пошло не так(")
                        await logging(f'Ошибка. Чат {message.chat.title} НЕ добавлен для заметок.')
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['adapter'])
async def apdapter(message):
    if str(message.from_user.id) in msg['adm']:
        chats = [False, False]
        await logging(f'Запущена функция адаптации.')
        if os.path.isfile(database):
            await bot.send_message(message.chat.id, "Подключаю базу данных!")
            conector = sqlite3.connect(database)
            cursor = conector.cursor()
            cursor.execute("SELECT * FROM chanels")
            id_f = cursor.fetchall()
            for i in range(len(id_f)):
                if 'log' in id_f[i][1]:
                    chats[0] = True
                if 'pic' in id_f[i][1]:
                    chats[1] = True
        else:
            await bot.send_message(message.chat.id, "Создаю базу данных!")
            dab = open(database, "w+")
            dab.write("")
            dab.close()
            conector = sqlite3.connect(database)
            cursor = conector.cursor()
            for i in db:
                try:
                    cursor.execute(db[i])
                    conector.commit()
                    await bot.send_message(message.chat.id, f'Таблица {i} создана!')
                except:
                    await bot.send_message(message.chat.id, f'Таблица {i} Не создана!\nПробую ещё раз.')
                    try:
                        cursor.execute(db[i])
                        conector.commit()
                        await bot.send_message(message.chat.id, f'Таблица {i} создана!')
                    except:
                        await bot.send_message(message.chat.id, f'Таблица {i} Не создана!\nПридется вручную...')

        if os.path.isdir('pic'):
            await bot.send_message(message.chat.id, f'Папка для картинок обнаружена!')
        else:
            await bot.send_message(message.chat.id, f'Создаю папку для картинок')
            os.makedirs('pic')
        if (not chats[0]) and (not chats[1]):
            await bot.send_message(message.chat.id, 'Все готово)\nОтправь куданибудь /set_pic, там буду присылать картинки с react\'а\nОтправь куданибудь /set_log, буду присылать туда логи')
        if (not chats[0]) and (chats[1]):
            await bot.send_message(message.chat.id, 'Все готово)\nОтправь куданибудь /set_log, буду присылать туда логи')
        if (chats[0]) and (not chats[1]):
            await bot.send_message(message.chat.id, 'Все готово)\nОтправь куданибудь /set_pic, там буду присылать картинки с react\'а')
        await logging(f'Адаптация завершена.')
    else:
        await bot.send_message(message.chat.id, "Лох, сначала сделай себе админку!")


@dp.message_handler(state='*', commands=['tpic']) #-1001303466328
async def tpic(message):
    if str(message.from_user.id) in msg['adm']:
        await sender()
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['test'])
async def test(message):
    if str(message.from_user.id) in msg['adm']:
        await logging('Запущенно тестирование')
        for i in tests:
            for g in range(len(tests[i])):
                tests[i][g] = 1
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['search'])
async def search(message):
    text = message.get_args()
    print(text)
    if len(text):
        info = wiki_search(str(text))
        if info:
            #gen_ogg(str(info))
            await bot.send_message(message.chat.id, f'Нашла: {info[0]}')
            #await bot.send_voice(message.chat.id, voice=types.InputFile(f'media/file.ogg'))
        else:
            await bot.send_message(message.chat.id, f'Не нашла ничего, попробуй синонимы или уточни.')
    else:
        await States.search.set()
        await bot.send_message(message.chat.id, f'Что искать?')

'''
@dp.message_handler(state='*', commands=['voice'])
async def voice(message):
    await logging('Голосовая ф-я активирована')
    text = message.get_args()
    if text not Null:
        gen_ogg(str(text))
        await bot.send_voice(message.chat.id, voice=types.InputFile(f'media/file.ogg'))
'''

@dp.message_handler(state='*', commands=['settings'])
async def settings(message):
    if str(message.from_user.id) in msg['adm']:
        await bot.send_message(message.chat.id,f'Меню настроек:', reply_markup=kb.inline_btn_set)
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')



@dp.message_handler(state='*', commands=['get_db'])
async def get_db(message):
    if str(message.from_user.id) in msg['adm']:
        await logging(f'Отправка .db')
        await bot.send_document(message.from_user.id, document=types.InputFile('data.db'))
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['some'])
async def some(message):
    if str(message.from_user.id) in msg['adm']:
        await bot.send_message(message.from_user.id, comands)
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')

@dp.message_handler(state='*', commands=['sql'])
async def sql_edit(message):
    if str(message.from_user.id) in msg['adm']:
        conector = sqlite3.connect(database)
        cursor = conector.cursor()
        zap = message.get_args()
        try:
            cursor.execute(zap)
            conector.commit()
            await bot.send_message(message.chat.id, f'Запрос выполнен успешно')
        except Exception as er:
            await bot.send_message(message.chat.id, f'Запрос не выполнен!\n'
                                                    f'Ошибка {er}')

    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')

@dp.message_handler(state='*', commands=['get_log'])
async def get_log(message):
    if str(message.from_user.id) in msg['adm']:
        await logging(f'Отправка логов')
        await bot.send_document(message.from_user.id, document=types.InputFile('nohup.out'))
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['test_url', 'add_url'])
async def url_work(message):
    if str(message.from_user.id) in msg['adm']:
        if message.get_command()[1:] == 'test_url':
            s1 = smart_dw(message.get_args(), test=True)
            await bot.send_message(message.chat.id, f'Количество найденых картинок: {len(s1)}')
            if len(s1) > 5:
                pics = types.MediaGroup()
                for i in range(5):
                    pics.attach_photo(s1[i], f'<a href="{s1[i]}">Orig</a>', parse_mode="HTML")
                try:
                    await bot.send_media_group(message.chat.id, media=pics)
                except:
                    await bot.send_message(message.chat.id, f'Попытка отправить не удалась...')
            else:
                print(s1)
        if message.get_command()[1:] == 'add_url':
            s1 = smart_dw(message.get_args(), test=True)
            await bot.send_message(message.chat.id, f'Количество найденых картинок: {len(s1)}')
            for i in s1:
                print(i)
                threads_ = threading.Thread(target=dw, args=(i,))
                threads_.start()

    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['adnotes'])#state=States.st0
async def adnotes(message):
    if str(message.from_user.id) in msg['adm']:
        await logging(f'Начало создания заметки.')
        text = message.get_args()
        if text:
            if adnote(text):
                await bot.send_message(message.chat.id, f'Заметка создана!')
        else:
            await States.adnot.set()
            await bot.send_message(message.chat.id, f'Напиши заметку так:\n'
                                                    f'ВРЕМЯ(завтра/через х дней)\n'
                                                    f'Текст заметки')
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


@dp.message_handler(state='*', commands=['education'])#state=States.st0
async def education(message):
    if str(message.from_user.id) in msg['adm']:
        await logging(f'Добавление текста в обучение')
        text = message.get_args()
        if text:
            await logging(f'Не доделано!! 565656')
        else:
            await States.education.set()
            await bot.send_message(message.chat.id, f'Пиши фразы через "энтер"\n', reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, f'У тебя нет права использовать эту команду\n'
                                                f'Вопросы к @farirus')


'''
@dp.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'{message.chat.id}_{int(time())}.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)'''


@dp.message_handler(state=States.education)
async def education(message, state: FSMContext):
    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    try:
        for i in message.text.split('\n'):
            cursor.execute(f"INSERT INTO texts VALUES (?, ?)",
                           (i.split('-')[0],i.split('-')[1]))
            conector.commit()
            await bot.send_message(message.chat.id, f'текст: {i} добавлен!')
    except:
        cursor.execute('''CREATE TABLE "texts" (
	"textin"	TEXT,
	"textans"	TEXT
)''')
        conector.commit()
        await education(message=message, state=state)

    await state.finish()


@dp.message_handler(state=States.search)
async def state_case_met(message, state: FSMContext):
    info = wiki_search(str(message.text))
    if info[0]:
        pics = types.MediaGroup()
        for i in range(6):
            if info[1][i].endswith('svg'):
                pass
            else:
                pics.attach_photo(info[1][i], f'<a href="{info[1][i]}">Orig</a>', parse_mode="HTML")
        #gen_ogg(str(info))
        await bot.send_message(message.chat.id, f'Нашла: {info[0]}')
        await bot.send_media_group(message.chat.id, media=pics)
        #await bot.send_voice(message.chat.id, voice=types.InputFile(f'media/file.ogg'))
        await state.finish()
    else:
        await bot.send_message(message.chat.id, f'Не нашла ничего, попробуй синонимы или уточни.')



@dp.message_handler(state=States.adurl)
async def state_case_met(message, state: FSMContext):
    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    urls = message.text.split('\n')
    for i in range(len(urls)):
        try:
            cursor.execute(f"INSERT INTO urls VALUES (?)",
                           (str(urls[i]),))
            conector.commit()
            await bot.send_message(message.chat.id, f'URL: {urls[i]} добавлен!',
                                   disable_web_page_preview=True)
            await asyncio.sleep(2)
        except Exception as er:
            await bot.send_message(message.chat.id, f'URL: {urls[i]} не добавлен\nОшибка {er}',
                                   disable_web_page_preview=True)
            await asyncio.sleep(2)

    await state.finish()

@dp.message_handler(state=States.adpic)
async def state_case_met(message, state: FSMContext):
    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    urls = message.text.split('\n')
    for i in range(len(urls)):
        try:
            cursor.execute(f"INSERT INTO pic VALUES (?,?)",
                           (str(urls[i]), 'False'))
            conector.commit()
            await bot.send_message(message.chat.id, f'pic: {urls[i]} добавлен!',
                                   disable_web_page_preview=True)
            await asyncio.sleep(2)
        except Exception as er:
            await bot.send_message(message.chat.id, f'pic: {urls[i]} не добавлен\nОшибка {er}',
                                   disable_web_page_preview=True)
            await asyncio.sleep(2)

    await state.finish()



@dp.message_handler(state=States.adnot)
async def state_case_met(message, state: FSMContext):
    try:
        if adnote(message.text):
            await bot.send_message(message.chat.id, f'Заметка создана!')
        else:
            await bot.send_message(message.chat.id, f'Заметка не создана!(см. логи)')
    except Exception as er:
        await bot.send_message(message.chat.id, f'Заметка не создана!\nОшибка: {er}')
    await logging(f'Заметка создана!')


    await state.finish()


@dp.message_handler(state='*')
async def state_case_met(message, state: FSMContext):
    text = str(message.text).split('\n')

    if text[0].lower() in org:
        if os.path.isfile(f'org/{message.from_user.id}.db'):
            conector = sqlite3.connect(f'org/{message.from_user.id}.db')
            cursor = conector.cursor()
        else:
            conector = sqlite3.connect(f'org/{message.from_user.id}.db')
            cursor = conector.cursor()

            cursor.execute('''CREATE TABLE "hist" (
	                        "id"	TEXT NOT NULL UNIQUE,
	                        "id1"	TEXT,
	                        "id2"	TEXT,
	                        "time"	TEXT,
                        	"summ"	TEXT,
                        	"comment"	TEXT
                            );''')
            conector.commit()
            cursor.execute('''CREATE TABLE "kard" (
	                        "id"	TEXT NOT NULL UNIQUE,
	                        "summ"	TEXT,
	                        "name"	TEXT NOT NULL,
	                        "names"	TEXT
                            );''')
            conector.commit()
            await asyncio.sleep(2)

        if text[0].lower() == 'новая карта':
            try:
                cursor.execute('SELECT * FROM kard')
                kards = cursor.fetchall()
                if len(kards):
                    cursor.execute(f"INSERT INTO kard VALUES (?, ?, ?, ?)",
                                   (str(len(kards)), str(text[3]), str(text[1]), str(text[2])))
                    conector.commit()
                else:
                    cursor.execute(f"INSERT INTO kard VALUES (?, ?, ?, ?)",
                                   ('0', str(text[3]), str(text[1]), str(text[2])))
                    conector.commit()
                await asyncio.sleep(1)
                await bot.send_message(message.from_user.id, f'Карта добавлена!')
            except:
                await asyncio.sleep(1)
                await bot.send_message(message.from_user.id, f'Ошибка введенных данных!')

        if text[0].lower() == 'расход':
            cursor.execute('SELECT * FROM kard')
            kards = cursor.fetchall()
            for i in kards:
                if (text[1] in i[2]) or (text[1] in i[3]):
                    try:
                        cursor.execute(f'UPDATE kard SET summ = "{str(float(i[1]) - float(text[2]))}" WHERE id = "{i[0]}"')
                        conector.commit()
                        cursor.execute('SELECT * FROM hist')
                        hist = cursor.fetchall()
                        if text[2] == text[-1]:
                            comment = 'False'
                        else:
                            comment = text[-1]

                        cursor.execute(f"INSERT INTO hist VALUES (?, ?, ?, ?, ?, ?)",
                                       (str(len(hist)), str(i[0]), 'False', str(text[2]),
                                        str(time.strftime( '%H:%M %d.%m.%y, %a', time.localtime(time.time()))),
                                        comment))
                        conector.commit()
                        await asyncio.sleep(1)
                        await bot.send_message(message.from_user.id, f'Расход учтен!')
                        return()
                    except:
                        await asyncio.sleep(1)
                        await bot.send_message(message.from_user.id, f'Ошибка введенных данных!')
                        return()
            await asyncio.sleep(1)
            await bot.send_message(message.from_user.id, f'Карта не найдена')


        if text[0].lower() == 'доход':
            cursor.execute('SELECT * FROM kard')
            kards = cursor.fetchall()
            for i in kards:
                if (text[1] in i[2]) or (text[1] in i[3]):
                    try:
                        cursor.execute(
                            f'UPDATE kard SET summ = "{str(float(i[1]) + float(text[2]))}" WHERE id = "{i[0]}"')
                        conector.commit()
                        cursor.execute('SELECT * FROM hist')
                        hist = cursor.fetchall()
                        if text[2] == text[-1]:
                            comment = 'False'
                        else:
                            comment = text[-1]

                        cursor.execute(f"INSERT INTO hist VALUES (?, ?, ?, ?, ?, ?)",
                                       (str(len(hist)), 'False', str(i[0]), str(text[2]),
                                        str(time.strftime('%H:%M %d.%m.%y, %a', time.localtime(time.time()))),
                                        comment))
                        conector.commit()
                        await asyncio.sleep(1)
                        await bot.send_message(message.from_user.id, f'Доход учтен!')
                        return ()
                    except:
                        await asyncio.sleep(1)
                        await bot.send_message(message.from_user.id, f'Ошибка введенных данных!')
                        return ()
            await asyncio.sleep(1)
            await bot.send_message(message.from_user.id, f'Карта не найдена')

        if text[0].lower() == 'удалить карту':
            try:
                name = text[1]
                cursor.execute('SELECT * FROM kard')
                kards = cursor.fetchall()
                for i in kards:
                    if name in f'{i[2]}{i[3]}':
                        cursor.execute(f'DELETE FROM kard WHERE id = "{i[0]}"')
                        conector.commit()
                        await bot.send_message(message.from_user.id, f'Карта "{i[2]}" удалена')

            except:
                cursor.execute('SELECT * FROM kard')
                kards = cursor.fetchall()
                kard_btn = InlineKeyboardMarkup()
                for i in kards:
                    kard_btn.add(InlineKeyboardButton(f'Имя: "{i[2]}", Баланс: {i[1]}', callback_data=i[0]))
                await bot.send_message(message.from_user.id, f'Нажми на карту для её удаления:',
                                       reply_markup=kard_btn)
                await States.rmkard.set()

        if text[0].lower() == 'перевод':
            pass

        if text[0].lower() == 'отменить операцию':
            pass

        if text[0].lower() == 'pass':
            pass
    elif str(message.text).startswith('http'):
        await bot.send_photo(message.from_user.id, str(message.text))




@dp.message_handler(content_types=types.ContentTypes.VOICE)
async def voice_message_handler(message):

    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = "voice/"
    await bot.download_file(file_path, "123.mp3")



@dp.message_handler(content_types=["new_chat_members"])
async def on_join(message):
    await message.delete()


@dp.channel_post_handler()
async def new_post(message):
    text = message.text
    if text.startswith('/'):
        if text[1:] == 'set_pic':
            await set_p(message)
        if text[1:] == 'set_log':
            await set_l(message)
        if text[1:] == 'set_note':
            await set_n(message)


async def adnote(text):
    try:
        note = text.split('\n')
        time_ = filter(note[0])
        trello.create_note(note[1], time_)
        await logging(f'Заметка создана!')
        return(True)
    except Exception as er:
        await logging(f'Заметка не создана!\nОшибка: {er}')
        return(False)


async def get_some_pic(t):
    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    cursor.execute('SELECT * FROM pic WHERE sended = "False"')
    id_f = cursor.fetchall()
    '''try:
        for i in range(len(id_f)):
            for j in range(i+1,len(id_f)-i):
                first = id_f[i][0]
                second = id_f[j][0]
                if (str(first[(first.rfind('-') + 1):]) in second) and (first != second):
                    await logging(f'Нашла похожее: \n'
                                  f'1 - {first}\n'
                                  f'2 - {second}')
                    await deleter([second,])
    except:
        pass'''
    pic = id_f[t][0]
    #print(pic)
    return(pic)


async def logging(text):
    if not os.path.isfile(database):
        return
    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    cursor.execute("SELECT * FROM chanels")
    id_f = cursor.fetchall()
    log_chat = []
    for i in range(len(id_f)):
        if 'log' in id_f[i][1]:
            log_chat.append(id_f[i][0])
    for i in log_chat:
        await bot.send_message(i, f'[LOG] {text}', disable_web_page_preview=True)


async def notes(id):
    if not os.path.isfile(database):
        return
    await logging(f'Notes id: {id} запущен')
    conector = sqlite3.connect(database)
    cursor = conector.cursor()

    while True:
        for i in range(60*timers['notes']):
            await asyncio.sleep(1)
            if tests['notes'][id]:
                notes_ = trello.get_notes()
                num = 0
                for i in notes_:
                    num = num + len(i)
                await logging(f'Notes c id {id} работает\n'
                              f'Время задержки: {timers["notes"]}\n'
                              f'Активных заметок: {num}')# {notes_no_archive}')
                tests['notes'][id] = 0
            if len(testn) < id+1:
                await logging(f'Notes id: {id} отключен')
                return
        await logging(f'Запущен новый цикл Notes с id: {id} ')

        note_ = trello.get_notes()
        cursor.execute("SELECT * FROM chanels")
        id_f = cursor.fetchall()
        note_chat = []
        for i in range(len(id_f)):
            if 'note' in id_f[i][1]:
                note_chat.append(id_f[i][0])
        for i in note_chat:
            for j in note_[0]:#На 25.06.21 в 12:00
                try:
                    await bot.send_message(i,f'На {j[1]}\n'
                                                f'Текст: {j[0]}', reply_markup=kb.inline_btn_note)
                except:
                    await bot.send_message(i, f'-Без времени-\n'
                                              f'Текст: {j[0]}', reply_markup=kb.inline_btn_note)
            for j in note_[1]:
                await bot.send_message(i,f'-Без времени-\n'
                                            f'Текст: {j[0]}', reply_markup=kb.inline_btn_note)
        await logging(f'Заметки отправлены Notes с id: {id} ')


async def react(id):
    await logging(f'React id: {id} запущен')
    threads = threading.Thread(target=downloader)
    threads.start()

    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    while True:
        for i in range(60*int(timers['react'])):
            await asyncio.sleep(1)
            if tests['react'][id]:
                cursor.execute('SELECT * FROM pic WHERE sended = "False"')
                id_f = cursor.fetchall()
                await logging(f'React c id {id} работает\n'
                              f'Время задержки: {timers["react"]}\n'
                              f'Количество картинок: {len(id_f)}')
                tests['react'][id] = 0

            if len(testr) < id+1:
                await logging(f'React id: {id} отключен')
                return

        cursor.execute('SELECT * FROM pic WHERE sended = "False"')
        id_f = cursor.fetchall()

        timers['react'] = abs(300 - len(id_f)) / 2
        if len(id_f) > 250:
            timers['react'] = 5

        await logging(f'Запущен новый цикл React с id: {id}')
        await sender()

async def sender():
    await logging(f'Запущена функция отправки картинок')
    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    cursor.execute("SELECT * FROM chanels")
    id_f = cursor.fetchall()
    pic_chat = []
    for i in range(len(id_f)):
        if 'pic' in id_f[i][1]:
            pic_chat.append(id_f[i][0])
    for i in pic_chat:
        await asyncio.sleep(1)
        pic_to_remoove = []
        while len(pic_to_remoove) < 6:
            pic = await get_some_pic(len(pic_to_remoove))
            if pic in pic_to_remoove:
                pass
            else:
                pic_to_remoove.append(pic)

        try:
            del pics
        except:
            pass

        pics = types.MediaGroup()
        for j in pic_to_remoove:
            if j.endswith('gif') or j.endswith('webm'):
                # bot.sendPhoto(msg['chat']['id'], (open(filepath, "rb")))
                try:
                    await bot.send_animation(i, j, caption=f'<a href="{j}">Orig</a>', parse_mode="HTML")
                    await asyncio.sleep(1)
                except Exception as er:
                    await logging(f'Не удалось отправить гифку {j}\n'
                                  f'Ошибка: {er}\n')
                    if 'Wrong' in str(er):
                        await deleter([j, ])
            else:
                new_pic = j.replace('post/', 'post/full/')
                pics.attach_photo(new_pic, f'<a href="{new_pic}">Orig</a>', parse_mode="HTML")
            await asyncio.sleep(1)
        ## my channel
        try:
            await bot.send_media_group(i, media=pics)
            await asyncio.sleep(1)
            await logging(f'Картинки успешно отправлены')
            await deleter(pic_to_remoove)
        except Exception as er:
            await asyncio.sleep(1)
            await logging(f'Не удалось отправить картинки\n'
                          f'Ошибка: {er}\n'
                          f'Запускаю по одной')
            for j in pic_to_remoove:
                try:
                    try:
                        await bot.send_photo(i, j.replace('post/', 'post/full/'),
                                             caption=f'''<a href='{j.replace('post/', 'post/full/')}'>Orig</a>''',
                                             parse_mode="HTML")
                        await asyncio.sleep(1)
                        await deleter([j, ])
                    except:
                        await logging(f'картинка {j} - фул фейл')
                        await bot.send_photo(i, j, caption=f'<a href="{j}">Orig</a>', parse_mode="HTML")
                        await asyncio.sleep(1)
                        await deleter([j, ])
                except Exception as er:
                    await logging(f'Не удалось отправить картинкy {j}\n'
                                  f'Ошибка: {er}')
                    if 'Wrong' in str(er):
                        await deleter([j, ])

    threads = threading.Thread(target=downloader)
    threads.start()

    cursor.execute('SELECT * FROM pic WHERE sended = "False"')
    id_f = cursor.fetchall()
    await logging(f'Завершена функция отправки картинок\n'
                  f'Осталось картинок: {len(id_f)}\n'
                  f'Время задержки: {timers["react"]}')


async def deleter(pic_to_remoove):
    conector = sqlite3.connect(database)
    cursor = conector.cursor()
    for j in pic_to_remoove:
        if j.startswith('http'):
            try:
                cursor.execute(f"UPDATE pic SET sended = 'True' WHERE name = '{j}'")
                conector.commit()
                #print(f'Удалила {j}')
            except Exception as er:
                await logging(f'Не удалось удалить картинку {j}\n'
                              f'Ошибка: {er}\n')
        else:
            try:
                await asyncio.sleep(1)
                os.remove(f'pic/{j}')
            except Exception as er:
                await logging(f'Не удалось удалить картинку {j}\n'
                              f'Ошибка: {er}\n')




if __name__ == '__main__':
    executor.start_polling(dp)