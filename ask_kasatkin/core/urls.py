from django.conf.urls import patterns, url
from core.views import index_page, show_login, validate_login, register, validate_register

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', index_page, name='home'),
    url(r'^login/$', show_login, name='login'),
    url(r'^validate_login/$', validate_login, name='validate_login'),
    url(r'^register/$', register, name='register'),
    url(r'^validate_register/$', validate_register, name='validate_register'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
