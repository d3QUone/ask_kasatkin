# long pooling test

import sys
from requests import *

r = put("http://vksmm.info/publish/?cid={0}".format(sys.argv[1]))
print "PUT"
print r.text

r = post("http://vksmm.info/publish/?cid={0}&qid={1}".format(sys.argv[1], 100))
print "POST"
print r.text