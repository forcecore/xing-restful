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

import test_config as config


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
        result = result["OutBlock"]

        odata = {
            "open": int(result["open"]),
            "high": int(result["high"]),
            "low": int(result["low"]),
            "close": int(result["price"]),
            "volume": int(result["volume"])
        }
        print("Response to client:")
        print(odata)
        self.write(odata)


class MarketOrderHandler(RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print("MarketOrderHandler: incoming")
        print(data)

        assert data['OrdQty'] != 0
        bnstpcode = 2 if data['OrdQty'] < 0 else 1 # 2 for sell, 1 for buy.
        data['OrdQty'] = abs(data['OrdQty'])

        q = xing.xaquery.Query("CSPAT00600")
        result = q.request(
            {
                "InBlock1": {
                    "AcntNo": data["AcntNo"],
                    "InptPwd": config.account["pass"],
                    "IsuNo": data["IsuNo"],
                    "OrdQty": data["OrdQty"],
                    "OrdPrc": 0, # 0 for market order
                    "BnsTpCode": bnstpcode, # "1" for sell, "2" for buy
                    "OrdprcPtnCode": "03", # "00": limit order, "03" market, "61" jang jeon shi gan oe
                    "MgntrnCode": "000", # margin trading code
                    "LoanDt": "", # Dae chool date
                    "OrdCndiTpCode": "0" # order condition code, Nil, TOC, FOK stuff.
                }
            },
            {
                "OutBlock1": ("RecCnt",),
                "OutBlock2": ("RecCnt",)
            }
        )

        print("Response to client:")
        print(result)
        self.write(result)


class LimitOrderHandler(RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print("LimitOrderHandler: incoming")
        print(data)

        assert data['OrdQty'] != 0
        bnstpcode = "2" if data['OrdQty'] < 0 else "1" # 2 for sell, 1 for buy.
        if data['OrdQty'] < 0:
            data['OrdQty'] *= -1

        q = xing.xaquery.Query("CSPAT00600")
        result = q.request(
            {
                "InBlock1": {
                    "AcntNo": data["AcntNo"],
                    "InptPwd": config.account["pass"],
                    "IsuNo": data["IsuNo"],
                    "OrdQty": data["OrdQty"],
                    "OrdPrc": data["OrdPrc"], # 0 for market order
                    "BnsTpCode": bnstpcode, # "1" for sell, "2" for buy
                    "OrdprcPtnCode": "00", # "00": limit order, "03" market, "61" jang jeon shi gan oe
                    "MgntrnCode": "000", # margin trading code
                    "LoanDt": "", # Dae chool date
                    "OrdCndiTpCode": "0" # order condition code, Nil, TOC, FOK stuff.
                }
            },
            {
                "OutBlock1": ("RecCnt",),
                "OutBlock2": ("RecCnt",)
            }
        )

        print("Response to client:")
        print(result)
        self.write(result)


def make_app():
    urls = [
        ("/price", PriceHandler),
        ("/market", MarketOrderHandler),
        ("/limit", LimitOrderHandler)
    ]
    return Application(urls, debug=True)


def shutdown():
    print("Logging out")
    session.logout()


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
    tornado.autoreload.add_reload_hook(shutdown)
    print("Starting server")

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        shutdown()
