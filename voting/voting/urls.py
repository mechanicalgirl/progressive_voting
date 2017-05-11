from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^',       include('federal.urls'),  name='federal'),
    url(r'^admin/', include(admin.site.urls)),
]
