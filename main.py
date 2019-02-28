"""
The server program that provides RESTful API

https://github.com/luapz/pyTrader : Some API usage

If you have any wonders in TR field values, see XingAPI_Sample.

pip install xing-plus
"""

import tornado
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import pandas as pd

import time
import xing
import xing.xasession
import pythoncom

import smoke_test_config as config


class PriceHandler(RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        q = xing.xaquery.Query("t1102")
        result = q.request(
            {
                "InBlock": {
                    "shcode": data["shcode"]
                }
            },
            {
                "OutBlock": ("open", "high", "low", "price", "volume")
            }
        )
        print(result)
        self.write(result)


def make_app():
    urls = [
        ("/price", PriceHandler)
    ]
    return Application(urls, debug=True)


session = xing.xasession.Session()


if __name__ == "__main__":
    # On run, prepare xing binding
    session = xing.xasession.Session()
    running = session.login(config.server, config.user)
    print("Logging in")

    #while running:
    #    session.heartbeat()
    #    pythoncom.PumpWaitingMessages()
    #    time.sleep(3)

    app = make_app()
    app.listen(5000)
    print("Starting server")

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        print("Logging out")
        session.logout()