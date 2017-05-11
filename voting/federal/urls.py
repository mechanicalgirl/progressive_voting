from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                             views.home,           name='home'),
    url(r'^district/(?P<district>.+)/$',   views.by_district,    name='by_district'),
]
