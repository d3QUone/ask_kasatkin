
#
# to run: uwsgi --http :8000 --wsgi-file helloworld.py
#
# to check: localhost:8000
#

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/plain')])
    return ["Hello World"]
