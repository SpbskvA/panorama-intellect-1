from django.forms import *

class ArticleOffer(Form):
    name = CharField(max_length=200)
    info = CharField(widget=Textarea)
    image = CharField(max_length=200)
