from django.conf.urls import patterns, include, url
#from django.contrib import admin

urlpatterns = patterns('',
    #url(r'^admin_panel/', include(admin.site.urls)),  # doesn't work
    url(r'^', include('core.urls', namespace='core')),
    url(r'^', include('user_profile.urls', namespace='user_profile')),
)
