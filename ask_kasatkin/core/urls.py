from django.conf.urls import patterns, url
from core.views import index_page, show_login, validate_login, register, validate_register, \
    self_settings, update_settings, self_logout, new_question, add_new_question, test, question_thread, \
    add_new_answer, all_by_tag

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', index_page, name='home'),
    url(r'^login/$', show_login, name='login'),
    url(r'^validate_login/$', validate_login, name='validate_login'),
    url(r'^register/$', register, name='register'),
    url(r'^validate_register/$', validate_register, name='validate_register'),
    url(r'^settings/$', self_settings, name='settings'),
    url(r'^update_settings/$', update_settings, name='validate_settings'),
    url(r'^add/$', new_question, name='create_question'),  # do this in front-end later
    url(r'^save_question/$', add_new_question, name='save_question'),
    url(r'^logout/$', self_logout, name='logout'),
    url(r'^test/$', test),
    url(r'^question/(?P<qid>\d+)/$', question_thread, name='question'),
    url(r'^add_new_answer/$', add_new_answer, name='add_new_answer'),

    url(r'^tag/(?P<tag_n>\w+)/$', all_by_tag, name='all_by_tag'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
