from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                            views.home,                name='home'),
    url(r'^preview/$',                    views.home,                name='home_preview'),
    url(r'^json/$',                       views.homejson,            name='home_json'),
    url(r'^state/(?P<state>.+)/$',        views.by_state,            name='by_state'),
    url(r'^district/(?P<district>.+)/$',  views.by_district,         name='by_district'),
    url(r'^reason/$',                     views.by_reason,           name='by_reason'),
    url(r'^reason/(?P<reason>.+)/$',      views.by_reason,           name='by_reason'),
    url(r'^search/$',                     views.search_by_name,      name='search_by_name'),
    # url(r'^get_ids/$',                  views.get_ids,             name='get_ids'),
    url(r'^newcandidates/$',              views.get_new_candidates,  name='get_new_candidates'),
]
