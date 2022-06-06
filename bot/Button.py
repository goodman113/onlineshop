from .views import *
from telegram import ReplyKeyboardMarkup, KeyboardButton
def category_button(categories):
    button = []
    res = []
    for i in categories:
        res.append(i.name)
        if len(res)==2:
            button.append(res)
            res = []
    if len(res)>0:
        button.append(res)
    return ReplyKeyboardMarkup(button, resize_keyboard=True,input_field_placeholder="categoriyalardan birini tanlang")