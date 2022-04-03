from django.urls import path
from . import views

urlpatterns = [
    path('', views.newspage, name='newspage'),
    path('main.html', views.newspage, name='newspage'),
    path('offer', views.offerpage, name='offerpage'),
	path('warning', views.warning, name='usermode'),
	path('requirements', views.requirements, name='requirements'),
	path('donate', views.donate, name='donate'),
	path('confirmation', views.confirmation, name='confirmation'),
	path('suggest', views.suggest, name='suggest'),
	path('previewoffers', views.previewoffers, name='previewoffers'),
	# path('about', views.about, name='usermode'),
]
