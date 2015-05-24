from tornado import websocket, web, ioloop
import json

cl = []

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    def open(self):
        if self not in cl:
            cl.append(self)
    def on_close(self):
        if self in cl:
            cl.remove(self)

class ApiHandler(web.RequestHandler):
    @web.asynchronous
    def get(self, *args):
        self.finish()        
        data = json.dumps({
                "id": self.get_argument("id"),
                "avatar": self.get_argument("avatar"),
                "rating": self.get_argument("rating"),
                "text": self.get_argument("text"),
                "nickname": self.get_argument("nickname")
            })
        for c in cl:
            c.write_message(data)


if __name__ == '__main__':
    app = web.Application([
        (r'/ws', SocketHandler),
        (r'/api', ApiHandler),
    ])
    app.listen(8888)
    ioloop.IOLoop.instance().start()
