from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^match/$', views.match, name='match'),
]
