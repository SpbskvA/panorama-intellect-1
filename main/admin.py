from django.contrib import admin
from .models import Article, OfferedArticle, Subscriber, Suggestion
from django.utils.safestring import mark_safe

admin.site.site_header = "Администрационная панель"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name','htmlimage','date')
    list_display_links = ('name','htmlimage',)
    fields = ('name', 'info', 'image', 'date', 'htmlimage')
    readonly_fields = ('date','htmlimage')

    def htmlimage(self, object):
        return mark_safe(f'<img src = "{object.image}" style = "height: 50px;">')

    htmlimage.short_description = "Картинка"

    save_on_top = True

class OffArticleAdmin(admin.ModelAdmin):
    list_display = ('name','date','htmlimage','is_accepted')
    list_display_links = ('name','htmlimage')
    list_editable = ('is_accepted',)
    fields = ('name', 'info', 'image', 'date', 'htmlimage')
    readonly_fields = ('date','htmlimage')

    def htmlimage(self, object):
        return mark_safe(f'<img src = "{object.image}" style = "height: 50px;">')

    htmlimage.short_description = "Картинка"

    save_on_top = True

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('tgid','subdate')

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('message','date')

# Register your models here.
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(OfferedArticle, OffArticleAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
