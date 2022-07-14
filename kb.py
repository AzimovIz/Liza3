from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_ex = InlineKeyboardButton('Выход', callback_data='exit')
inline_btn_adurl = InlineKeyboardButton('+URL', callback_data='adurl')
inline_btn_rmurl = InlineKeyboardButton('-URL', callback_data='rmurl')
inline_btn_adpic = InlineKeyboardButton('+pics', callback_data='adpic')

inline_btn_rct = InlineKeyboardMarkup()#.row(InlineKeyboardButton('--', callback_data='btnrct--'),
                                       #     InlineKeyboardButton('-', callback_data='btnrct-'),
                                       #     InlineKeyboardButton('+', callback_data='btnrct+'),
                                       #     InlineKeyboardButton('++', callback_data='btnrct++'),)
inline_btn_rct.add(InlineKeyboardButton('Удалить поток', callback_data='btnrctms'),
                   InlineKeyboardButton('Добавить поток', callback_data='btnrctad'))
inline_btn_rct.row(inline_btn_rmurl, inline_btn_adurl)
inline_btn_rct.add(inline_btn_adpic, inline_btn_ex )

inline_btn_nts = InlineKeyboardMarkup().row(InlineKeyboardButton('--', callback_data='btnnts--'),
                                            InlineKeyboardButton('-', callback_data='btnnts-'),
                                            InlineKeyboardButton('+', callback_data='btnnts+'),
                                            InlineKeyboardButton('++', callback_data='btnnts++'),)
inline_btn_nts.add(InlineKeyboardButton('Удалить поток', callback_data='btnntsms'),
                   InlineKeyboardButton('Добавить поток', callback_data='btnntsad'))
inline_btn_nts.add(inline_btn_ex)

inline_btn_note = InlineKeyboardMarkup().row(InlineKeyboardButton('Готово', callback_data='notearc'))
inline_btn_note.row(InlineKeyboardButton('+2 часа', callback_data='notead2'),
                    InlineKeyboardButton('+5 часов', callback_data='notead5'),
                    InlineKeyboardButton('+10 часов', callback_data='notead10'),
                    InlineKeyboardButton('+сутки', callback_data='notead24'),)

inline_btn_set = InlineKeyboardMarkup().add(InlineKeyboardButton('Функции', callback_data='btnfun'),
                                            InlineKeyboardButton('Сервер', callback_data='btnsr'),
                                            InlineKeyboardButton('Arduino', callback_data='btnard'),
                                            InlineKeyboardButton('Комнаты/ус-ва', callback_data='btnrooms'), )
