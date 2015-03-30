
#
# to run: uwsgi --http :8000 --wsgi-file _helloworld.py
#
# to check: localhost:8000
#

# or just 'sudo service gunicorn start / restart
def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])

    # keys = env.keys() # shows ALL request parameters in a heap
    keys = ["REQUEST_METHOD", "PATH_INFO", "QUERY_STRING"]
    out = ""
    for i in keys:
        out += "<strong>{0}:</strong> {1}<br>\n".format(i, env[i])

    return ["Hello World<hr>\n", out]
