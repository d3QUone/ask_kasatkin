from django.conf.urls import patterns, url
from techno_rating.views import index

urlpatterns = patterns('',
    url(r'^techno_rating/$', index, name='techno'),
)
