
#
# to run: uwsgi --http :8000 --wsgi-file _helloworld.py
#
# to check: localhost:8000
#

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    # shows ALL request parameters in a heap 
    keys = env.keys()
    out = ""
    for i in keys:
        out += "<strong>{0}</strong> | {1} <br>".format(i, env[i])
    
    return ["Hello World<hr>", out]
