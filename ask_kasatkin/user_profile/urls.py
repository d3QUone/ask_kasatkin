from django.conf.urls import patterns, url
from user_profile.views import show_login, validate_login, register, validate_register, self_settings, update_settings, self_logout

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^login/$', show_login, name='login'),
    url(r'^logout/$', self_logout, name='logout'),
    url(r'^validate_login/$', validate_login, name='validate_login'),
    url(r'^signup/$', register, name='register'),
    url(r'^validate_register/$', validate_register, name='validate_register'),
    url(r'^settings/$', self_settings, name='settings'),
    url(r'^update_settings/$', update_settings, name='validate_settings'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
