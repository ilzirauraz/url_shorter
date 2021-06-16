from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('url_shorter/', views.shorten_url, name='shortenurl'), 
    path('<subpart>/', views.redirect_by_short_link, name='redirect'),
]