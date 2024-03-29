﻿from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import os
from .models import Article, OfferedArticle, Subscriber, Suggestion
from .forms import ArticleOffer
import telebot as tb
from telebot import types
import threading as td
from django.conf import settings
from requests import get
from random import randint
bot = tb.TeleBot(settings.TELEGRAM_KEY)

def getcat(deep=0):
    if deep > 10:
        return "https://forum.exbo.ru/assets/files/2021-02-09/1612862122-945296-hf-qs6u00hw.jpeg"
    source = get("https://aws.random.cat/view/{}".format(randint(1,1000))).text
    if "id=\"cat" in source:
        return source.split("src=\"")[1].split("\"")[0]
    else:
        return getcat(deep+1)

@bot.message_handler(commands=["start"])
def start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    if Subscriber.objects.filter(tgid = str(message.chat.id)).exists():
        unsub=types.KeyboardButton("Отписаться")
        markup.add(unsub)
        bot.send_message(message.chat.id, 'Привет, дорогой подпищик!👾\nЕсли тебе надоели наши посты можешь отписаться от рассылки',  reply_markup=markup)
    else:
        sub=types.KeyboardButton("Подписаться")
        markup.add(sub)
        bot.send_message(message.chat.id, 'Приветствуем тебя!👾\nТут ты можешь подписаться на рассылку о новых постах',  reply_markup=markup)

@bot.message_handler(content_types=["text"])
def handler(message):
    unsubmk=types.ReplyKeyboardMarkup(resize_keyboard=True)
    unsub=types.KeyboardButton("Отписаться")
    unsubmk.add(unsub)
    submk=types.ReplyKeyboardMarkup(resize_keyboard=True)
    sub=types.KeyboardButton("Подписаться")
    submk.add(sub)
    if message.text.strip().lower() == 'подписаться':
        if Subscriber.objects.filter(tgid = str(message.chat.id)).exists():
            bot.send_message(message.chat.id, "Ты уже подписан!🙂", reply_markup = unsubmk)
        else:
            try:
                Subscriber(tgid = str(message.chat.id)).save()
            except Exception as ex:
                print('При подписке пользователя с id:{} что то пошло не так:\n{}'.format(message.chat.id, ex))
            bot.send_message(message.chat.id, "Подписка оформлена!😎", reply_markup = unsubmk)
    elif message.text.strip().lower() == 'отписаться':
        if Subscriber.objects.filter(tgid = str(message.chat.id)).exists():
            try:
                Subscriber.objects.get(tgid = str(message.chat.id)).delete()
            except Exception as ex:
                print('При отписке пользователя с id:{} что то пошло не так:\n{}'.format(message.chat.id, ex))
            bot.send_message(message.chat.id, "Рассылка остановлена👌", reply_markup = submk)
        else:
            bot.send_message(message.chat.id, "Ты и не был подписан🙃", reply_markup = submk)
    else:
        try:
            source = get("https://aws.random.cat/view/{}".format(randint(1,1000))).text
            if Subscriber.objects.filter(tgid = str(message.chat.id)).exists():
                bot.send_photo(message.chat.id, getcat(), '', reply_markup = unsubmk)
            else:
                bot.send_photo(message.chat.id, getcat(), '', reply_markup = submk)
        except Exception as ex:
            print(ex)

polling = False
def plg():
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        plg()

def newspage(request):
    global polling
    if not polling:
        try:
            td.Thread(target = plg, name = "polling").start()
            polling = True
        except Exception as ex:
            print(ex)

    if request.method == "POST":
        part = request.POST["search_request"]
        articles = [article for article in Article.objects.all() if part.lower() in article.name.lower()]
    else:
        articles = Article.objects.all()

    if articles == []:
        articles = [Article(name = "По вашему запросу ничего не нашлось...😑", info = "", image = "https://http.cat/404", date = "-_-")]

    data = {
        "articles" : articles,
        "thispage" : 'http://{}'.format(request.META['HTTP_HOST']),
    }

    return render(request, 'main/main.html', data)

def offerpage(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ArticleOffer(request.POST)
        # check whether it's valid:
        if form.is_valid():
            OfferedArticle(name = form.cleaned_data['name'], image = form.cleaned_data['image'], info = form.cleaned_data['info'], is_accepted = False).save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/main.html')
    return render(request, 'main/offer.html')

def previewoffers(request):
    if request.user.is_staff:
        data = {
            "articles" : OfferedArticle.objects.all()
        }
        return render(request, 'main/previewoffers.html', data)
    else:
        return HttpResponseRedirect('/main.html')

def onoffnotify(request):
    if request.user.is_staff:
        if request.method == "GET" and request.GET.get('status'):
            if request.GET['status'] == '1':
                settings.ENABLE_NOTIFICATIONS = True
                print("### TELEGRAM NOTIFICATIONS ENABLED ###")
            elif request.GET['status'] == '0':
                settings.ENABLE_NOTIFICATIONS = False
                print("### TELEGRAM NOTIFICATIONS DISABLED ###")
        return render(request, 'main/onoffnotify.html', {'status' : settings.ENABLE_NOTIFICATIONS})
    else:
        return HttpResponseRedirect('/main.html')

def warning(request):
	return render(request, 'main/warning.html')

def donate(request):
	return render(request, 'main/donate.html')

def requirements(request):
	return render(request, 'main/requirements.html')

def confirmation(request):
	return render(request, 'main/confirmation.html')

def suggest(request):
    if request.method == 'POST':
        msg = request.POST['suggestion']
        try:
            Suggestion(message = msg).save()
        except Exception as ex:
            print(ex)
        return HttpResponseRedirect('/main.html')
    return render(request, 'main/suggest.html')
# def about(request):
# 	return render(request, 'main/about.html')
