from werkzeug.serving import make_server
from flaskr import create_app
from threading import Thread
from flask import Flask
import pytest
import os

dir_path = os.path.abspath('./')
keysFile = os.path.join(dir_path, 'instance\\testKeys.txt')
try:
    os.remove(keysFile)
except:
    pass

config = {
    'TESTING':True,
    'SECRET_KEY' : 'dev',
    'JSFILES' : ["external/JQuery/jquery-3.3.1.min.js",
               "external/Bootstrap/js/bootstrap.min.js",
               "js/testingMethods.js"],
    'API_KEYS_FILE': keysFile
}

@pytest.fixture
def app():
    app = create_app(config)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setupDriver(request):
    #start_server()
    from selenium import webdriver
    driver = webdriver.Chrome(os.path.abspath('chromedriver/chromedriver.exe'))
    request.instance.driver = driver
    yield
    tearDown(driver)


class ServerThread(Thread):

    def __init__(self, app):
        Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


def start_server():
    global server
    app = create_app()
    ...
    server = ServerThread(app)
    server.start()


def stop_server():
    global server
    server.shutdown()

def tearDown (driver):
    driver.close()
    stop_server()
    
