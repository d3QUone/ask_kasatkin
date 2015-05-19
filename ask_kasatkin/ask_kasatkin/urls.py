from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static
#import debug_toolbar

urlpatterns = patterns('',
    url(r'^', include('core.urls', namespace='core')),
    url(r'^', include('user_profile.urls', namespace='user_profile')),
    #url(r'^__debug__/', include(debug_toolbar.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)