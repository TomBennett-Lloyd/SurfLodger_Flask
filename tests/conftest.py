from werkzeug.serving import make_server
from selenium.webdriver.support.ui import WebDriverWait
from flaskr import create_app
from threading import Thread
from flask import Flask
import pytest
import os

dir_path = os.path.abspath('./')
#set keysFile for testing and ensure it doesn't already exist
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
def realKey():
    #path to live keys file to get the valid key
    keysFile = os.path.join(dir_path, 'instance\\keys.txt')
    realKey = ""
    if os.path.isfile(keysFile):
        with open(keysFile, 'r') as keys:
            line = keys.readline().split(":")
            if line[0] == "places":
                realKey = line[1]

    if realKey == "":
        realKey = "Please use the App to set up your key"
    yield realKey

@pytest.fixture
def app():
    app = create_app(config)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setupDriver(request):
    start_server()#start the built in web server in separate thread
    from selenium import webdriver
    driver = webdriver.Chrome(os.path.abspath('chromedriver/chromedriver.exe'))
    request.instance.driver = driver
    driver.get('http://localhost:5000/home') #navigate to the homepage
    driver.wait = WebDriverWait(driver, 10, poll_frequency=1) #init the waiter
    yield driver
    tearDown(driver)#stop the threads after test


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
    app = create_app(config)
    ...
    server = ServerThread(app)
    server.start()


def stop_server():
    global server
    server.shutdown()

def tearDown (driver):
    driver.close()
    stop_server()
    
