"""
Make request to restful API of my Xing bridge server
"""
import requests

# To connect from your Linux machine to Windows machine!
price_url = "http://192.168.0.33:5000/price"
order_url = "http://192.168.0.33:5000/order"


def get_price(shcode):
    """
    shcode: symbol, in string. e.g., "233740".
    """
    data = {
        "shcode": shcode
    }
    resp = requests.post(price_url, json=data)
    print("get_price:", shcode)
    print(resp.status_code)
    print(resp.json())
    return resp.json()


def market_order(account_num, isu_no, qty):
    """
    account_num: string of account number to run transaction on.
    isu_no: Symbol for buying the stock. == shcode, usually.
    qty: quantity. If below 0, it is a sell order.
    """
    return limit_order(account_num, isu_no, qty, 0)


def limit_order(account_num, isu_no, qty, price):
    """
    account_num: string of account number to run transaction on.
    isu_no: Symbol for buying the stock. == shcode, usually.
    qty: quantity. If below 0, it is a sell order.
    price: limit price. 0 means market order.
    """
    data = {
        "AcntNo": account_num,
        "IsuNo": isu_no,
        "OrdQty": qty,
        "OrdPrc": price
    }
    resp = requests.post(order_url, json=data)
    print("limit_order:", isu_no, qty, price)
    print(resp.status_code)
    print(resp.json())
    return resp.json()


if __name__ == "__main__":
    account_num = "12345678910"
    market_order(account_num, "233740", 10)
    limit_order(account_num, "233740", -5, 13000)
