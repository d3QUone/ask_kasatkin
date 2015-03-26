from django.conf.urls import patterns, url
from core.views import index_page, new_question, add_new_question, test, question_thread, add_new_answer, all_by_tag

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^test/$', test),
    url(r'^$', index_page, name='home'),
    url(r'^add/$', new_question, name='create_question'),  # do this in front-end later
    url(r'^save_question/$', add_new_question, name='save_question'),
    url(r'^question/(?P<qid>\d+)/$', question_thread, name='question'),
    url(r'^add_new_answer/$', add_new_answer, name='add_new_answer'),
    url(r'^tag/(?P<tag_n>\w+)/$', all_by_tag, name='all_by_tag'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
