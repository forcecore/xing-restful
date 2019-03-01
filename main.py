"""
The server program that provides RESTful API

http://sculove.github.io/xing-plus/xing.html#module-xing.xasession : xing-plus manual

https://github.com/sculove/xing-plus-app : xing-plus example app from the author

If you have any wonders in TR field values, see XingAPI_Sample.
"""

import tornado
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

import xing
import xing.xasession

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


class OrderHandler(RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print("OrderHandler: incoming")
        print(data)

        assert data['OrdQty'] != 0
        bnstpcode = 2 if data['OrdQty'] < 0 else 1 # 2 for sell, 1 for buy.
        data['OrdQty'] = abs(data['OrdQty'])

        # price == 0 means Market order, code 03. Otherwise, limit order of code 00.
        ord_prc_ptn_code = "03" if data['OrdPrc'] == 0 else "00"

        q = xing.xaquery.Query("CSPAT00600")
        result = q.request(
            {
                "InBlock1": {
                    "AcntNo": data["AcntNo"],
                    "InptPwd": config.user["account_passwd"],
                    "IsuNo": data["IsuNo"],
                    "OrdQty": data["OrdQty"],
                    "OrdPrc": data['OrdPrc'], # 0 for market order
                    "BnsTpCode": bnstpcode, # "1" for sell, "2" for buy
                    "OrdprcPtnCode": ord_prc_ptn_code, # "00": limit order, "03" market, "61" jang jeon shi gan oe
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
        ("/order", OrderHandler),
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

    app = make_app()
    app.listen(5000)
    tornado.autoreload.add_reload_hook(shutdown)
    print("Starting server")

    try:
        IOLoop.instance().start()
    except KeyboardInterrupt:
        shutdown()
