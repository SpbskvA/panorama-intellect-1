from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import os
from .models import Article, OfferedArticle, Subscriber, Suggestion
from .forms import ArticleOffer
import telebot as tb
from telebot import types
import threading as td
bot = tb.TeleBot('5144005351:AAF17je1fLUroxiFt_PAPyuwo9cE01UQq1o')

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
        if Subscriber.objects.filter(tgid = str(message.chat.id)).exists():
            bot.send_message(message.chat.id, message.text, reply_markup = unsubmk)
        else:
            bot.send_message(message.chat.id, message.text, reply_markup = submk)
polling = False

def plg():
    bot.polling(none_stop=True, interval=0)


def newspage(request):
    if request.scheme == 'http' and request.META['HTTP_HOST'] != 'localhost:8000' and request.META['HTTP_HOST'] != '127.0.0.1:8000':
        return redirect('https://{}'.format(request.META['HTTP_HOST']))
    global polling
    if not polling:
        try:
            td.Thread(target = plg, name = "polling").start()
            polling = True
        except Exception as ex:
            print(ex)
    data = {
        "articles" : Article.objects.all(),
        "thispage" : 'https://{}'.format(request.META['HTTP_HOST'])
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
