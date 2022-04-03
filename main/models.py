from django.db.models import *

import telebot as tb
bot = tb.TeleBot('5144005351:AAF17je1fLUroxiFt_PAPyuwo9cE01UQq1o')

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
    date = DateField(auto_now_add = True, verbose_name = "Дата")

    def save(self, *args, **kwargs):
        if not Article.objects.filter(id = self.id).exists():
            for user in Subscriber.objects.all():
                bot.send_photo(int(user.tgid), self.image, 'На сайте "Панорама Интеллект" вышел новый пост😎:\n"{}"\nПодробнее -> https://panorama-intellect.me/'.format(self.name))
        super().save(*args, **kwargs)

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
            Article(name = self.name, info = self.info, image = self.image, date = self.date).save()
            self.delete()
        else:
            self.is_accepted = False
            super().save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        ordering = ["-date","-id"]
        verbose_name = "Предложенная новость"
        verbose_name_plural = "Предложенные новости"
