from datetime import datetime as tm

msg = {'hello': 'Привет)',
    'start': 'message',
    'adm': '1060835059 609310432',
    'notes': 'Запомни запомни заметка Заметка Запись запись Будильник будильник',
    }

filt = {
    'next_d': 'завтра',
    'nnext_d':'послезавтра',
    'n_day': 'через',
}

org = {
    'новая карта',
    'расход',
    'доход',
    'перевод',
    'удалить карту',
    'отменить операцию',
    'pass',
}

comands = '''
/train - запустить тренировку
/get_log - получить nohup.output
/test_url - проверить может ли парситься сайт
/add_url - добавить картинки из url в базу 
'''


def filter(text):
    text = text.lower()
    if ('послезавтра' in text) or ('после завтра' in text):
        t = tm.now()
        print(tm.isoformat(t))
        t = t.replace(day=t.day + 2)
        return(t)
    elif 'завтра' in text:
        t = tm.now()
        print(tm.isoformat(t))
        t = t.replace(day=t.day + 1)
        return(t)
    elif text.startswith('через'):
        texts = text.split(' ')
        if texts[1] == 'неделю':
            t = tm.now()
            print(tm.isoformat(t))
            t = t.replace(day=t.day + 7)
            return (t)
        num = int(texts[1])
        if texts[2] in ['дней','день','дня']:
            t = tm.now()
            print(tm.isoformat(t))
            t = t.replace(day=t.day + num)
            return (t)
        if texts[2] in ['недель','неделю','недели']:
            t = tm.now()
            print(tm.isoformat(t))
            t = t.replace(day=t.day + num*7)
            return (t)
    else:
        return(text)

db = { 'chanels': 'CREATE TABLE "chanels" ("id"	TEXT NOT NULL UNIQUE,"dest"	TEXT);',
    'pic': 'CREATE TABLE "pic" ("name" TEXT NOT NULL UNIQUE,	"sended" TEXT);',
    'notes': 'CREATE TABLE "notes" ("time" TEXT NOT NULL, "time_r" TEXT, "text" TEXT, "archived" TEXT);',
    'urls': 'CREATE TABLE "urls" ("url" TEXT NOT NULL UNIQUE);',
    'texts': 'CREATE TABLE "texts" ("textin" TEXT, "textans" TEXT);'
    }
'''
adnotes - Создание заметки (trello)
home - Управление домом
settings - Настройки
search - Поиск по вики
tpic - Отправить картинки
test - Проверка функций
education - Добавление слов
get_db - Отправить базу данных
adapter - Досоздание файлов и папок
some - Другие команды
train
get_log
test_url
add_url
'''

#F@19gg_#check