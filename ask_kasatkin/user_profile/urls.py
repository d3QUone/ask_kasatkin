from django.conf.urls import patterns, url
from user_profile.views import do_login, do_logout, register, self_settings

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^login/$', do_login, name='login'),
    url(r'^logout/$', do_logout, name='logout'),
    url(r'^signup/$', register, name='register'),
    url(r'^settings/$', self_settings, name='settings'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
