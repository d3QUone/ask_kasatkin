from django.conf.urls import patterns, url
from core.views import index_page, register, validate_registration

urlpatterns = patterns('',
    url(r'^$', index_page, name='home'),
    url(r'^register/$', register, name='register'),
    url(r'^validate/$', validate_registration, name='validate'),
)
