# RESTful interface provider for Xing API

I have many stuff in my Linux machine but Xing API only allows a Windows server.
As you know, deep learning or machine learning, back test are much easier on
Linux machines.

The program will run on Windows,
get process requests from Linux machines thorugh the RESTful API,
and connect to the broker with Xing API.


## Requirements

* tornado (for server)
* xing-plus: https://github.com/sculove/xing-plus
* pip install xing-plus


## main.py, the server

Run this on the Windows machine.
The server will listen to 5000 port for clients.
DO NOT run this in public places.
You must only use the script behind firewall!


## sample_client.py

This scipt shows you how to use the server.
