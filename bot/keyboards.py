from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


start_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]],
                               resize_keyboard=True)


gender_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Ищем мужские 👨🏻')],
                                          [KeyboardButton(text='Ищем женские 👩🏻')]], 
                             resize_keyboard=True)


output_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Вперед 🔎')],
                                          [KeyboardButton(text='Сбросить 🔙')]],
                                resize_keyboard=True)
