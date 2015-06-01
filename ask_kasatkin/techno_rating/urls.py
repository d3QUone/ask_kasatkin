from django.conf.urls import patterns, url
from techno_rating.views import index

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^techno_rating/$', index, name='techno'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
