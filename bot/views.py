from unicodedata import category
from django.shortcuts import render
from telegram import Update
from telegram.ext import CallbackContext
from app.models import *
from .models import *
from .Button import *
state_category = 1
state_product = 2
def start(update:Update, context:CallbackContext):
    user, state = Profile.objects.get_or_create(telegram_id=update.effective_user.id)
    user.first_name = update._effective_user.first_name
    user.last_name = update._effective_user.last_name
    user.save()
    categories = Category.objects.all()
    update.message.reply_html("assalomu alaykum", reply_markup=category_button(categories))
    return state_category


def command_category(update:Update, context:CallbackContext):
    text = update.message.text
    try:
        category = Category.objects.get(name=text)
        products = Products.objects.filter(category=category)
        update.message.reply_photo(open(category.image.url[1:], 'rb'), reply_markup=category_button(products))
    except Exception as e:
        category = Category.objects.get(name=text)
        products = Products.objects.filter(category=category)
        update.message.reply_html("Mahsulatlardan birini tanglang ", reply_markup=category_button(products))
    return 2
def command_product(update:Update, context:CallbackContext):
    text = update.message.text
    try: 
        product = Products.objects.get(name=text)
        update.message.reply_photo(open(product.image.url[1:], 'rb'), caption=f"{product.name}\n" 
        f"{product.description}\n")
    except:
        product = Products.objects.get(name=text)
        update.message.reply_text(f"{product.name}\n" f"{product.description}\n")
