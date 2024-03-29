from django.db.models import *
import telebot as tb
from django.conf import settings
bot = tb.TeleBot(settings.TELEGRAM_KEY)

class Suggestion(Model):
    message = TextField(verbose_name = "Предложение")
    date = DateField(auto_now_add = True, verbose_name = "Дата предложения")

    class Meta:
        ordering = ['-date']
        verbose_name = "Предложение"
        verbose_name_plural = "Жалобы и предложения"

# Create your models here.
class Subscriber(Model):
    tgid = TextField(unique = True, verbose_name = "Телеграм ID")
    subdate = DateField(auto_now_add = True, verbose_name = "Дата подписки")

    class Meta:
        ordering = ["-subdate","-id"]
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

class Article(Model):
    name = TextField(verbose_name = "Заголовок")
    info = TextField(verbose_name = "Информация")
    image = TextField(verbose_name = "Картинка")
    date = DateField(auto_now_add = False, verbose_name = "Дата")

    def save(self, *args, **kwargs):
        new = False
        if self.id == None:
            new = True
        try:
            super().save(*args, **kwargs)
        except Exception as ex:
            print(f"### CANNOT SAVE THE ARTICLE <EXCEPTION>:<{ex}> ###")
        else:
            if settings.ENABLE_NOTIFICATIONS and new:
                for user in Subscriber.objects.all():
                    bot.send_photo(int(user.tgid), self.image, 'На сайте "Панорама Интеллект" вышел новый пост😎:\n"{}"\nПодробнее -> https://panorama-intellect.me/'.format(self.name))

    class Meta:
        ordering = ["-date","-id"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

class OfferedArticle(Model):
    name = TextField(verbose_name = "Заголовок")
    info = TextField(verbose_name = "Информация")
    image = TextField(verbose_name = "Картинка")
    date = DateField(auto_now_add = True, verbose_name = "Дата")
    is_accepted = BooleanField(default = False, verbose_name = "Опубликовано?")

    def save(self, *args, **kwargs):
        if self.is_accepted:
            try:
                Article(name = self.name, info = self.info, image = self.image, date = self.date).save()
            except Exception as ex:
                print(f"### CANNOT PUSH THE ARTICLE <EXCEPTION>:<{ex}> ###")
            else:
                self.delete()
        else:
            self.is_accepted = False
            super().save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        ordering = ["-date","-id"]
        verbose_name = "Предложенная новость"
        verbose_name_plural = "Предложенные новости"
