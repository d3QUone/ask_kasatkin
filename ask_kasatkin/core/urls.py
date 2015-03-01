from django.conf.urls import patterns, url
from core.views import index_page, register, validate_registration

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', index_page, name='home'),
    url(r'register/$', register, name='register'),
    url(r'validate/$', validate_registration, name='validate'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
