from flaskr import create_app
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
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope="class")
def driver_init(request):
    from selenium import webdriver
    web_driver = webdriver.Chrome('chromedriver/chromedriver.exe')
    request.cls.driver = web_driver
    yield
    web_driver.close()


@pytest.mark.usefixtures("driver_init")
class BaseTest:
    pass

class Test_setKey_form (BaseTest):
    def addKey(self, key):
        wait = WebDriverWait(self.driver, 3)
        self.driver.get("http://localhost/setKey")
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='places']"))).sendKeys(key[0])
        self.driver.findElement(By.CSS_SELECTOR, "#APIKeyForm > button[type = 'submit']").click()
        wait.until(EC.visibility_of_element_located(By.CSS_SELECTOR,"div.alert"))
        assert self.driver.findElement(By.CSS_SELECTOR, "div.alert-"+key[1])

    def test_addKey(self):
        testKeys = [
            ["test","error"],
            ["AIzaSyA1VBx0F3gr2YPK4KeS7ym6kMbNRUOZOB1", "error"],
            ["AIzaSyA1VBx0F3gr2YPK4KeS7ym6kMbNRUOZOB8", "success"]
        ]
        for key in testKeys:
            self.addKey(key)
