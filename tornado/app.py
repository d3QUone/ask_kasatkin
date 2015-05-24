# coding: utf8

from tornado import websocket, web, ioloop
import json

subs = {}

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self, channel_id):
        if channel_id:
            if channel_id not in subs:
                subs[channel_id] = []
            if self not in subs[channel_id]:
                subs[channel_id].append(self)
    def on_close(self):
        for i in subs.keys():
            if self in subs[i]:
                subs[i].remove(self)
                break


class ApiHandler(web.RequestHandler):
    @web.asynchronous
    def post(self, *args):
        self.finish()
        channel_id = self.get_argument("channel")
        data = json.dumps({
                "id": self.get_argument("id"),
                "text": self.get_argument("text"),
                "avatar": self.get_argument("avatar"),
                "nickname": self.get_argument("nickname")
            })
        if channel_id in subs:
            for c in subs[channel_id]:
                c.write_message(data)

if __name__ == '__main__':
    app = web.Application([
        (r'/ws/([0-9]*)$', SocketHandler),
        (r'/push', ApiHandler),
    ])
    app.listen(8888)
    ioloop.IOLoop.instance().start()
