#!/usr/bin/env python3
import time
from http.server import HTTPServer
from app.server import Server
from app.services.transactionService import checkTransactionExpire
from apscheduler.schedulers.background import BackgroundScheduler

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(checkTransactionExpire, 'interval', seconds=5)
    scheduler.start()

    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))