import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@pytest.mark.usefixtures("setupDriver")
class Test_keyAdder:
    def test_addKey(self):
        self.driver.get('http://localhost:5000/home')
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30, poll_frequency=1)
        testKeys = [
            ["test", "error"],
            ["AIzaSyA1VBx0F3gr2YPK4KeS7ym6kMbNRUOZOB1", "error"],
            ["AIzaSyA1VBx0F3gr2YPK4KeS7ym6kMbNRUOZOB8", "success"]
        ]
        for key in testKeys:
            self.addKey(key)

    def addKey(self, key):
        self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='places']")))
        self.driver.find_element_by_name("places").send_keys(key[0])
        self.driver.find_element_by_xpath("//form[@id='APIKeyForm']/button[@type='submit']").click()
        self.wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "alert-"+key[1])))
        driver.implicitly_wait(10)


@pytest.mark.usefixtures("setupDriver")
class Test_locationSearch:
    def test_addKey(self):
        self.driver.get('http://localhost:5000/home')
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 30, poll_frequency=1)
        testLocations = [
            "Bantham",
            "Newquay",
            "Rhosneigr"
        ]
        for location in testLocations:
            self.search(location)

    def search(self, location):
        self.wait.until(EC.visibility_of_element_located(
            (By.ID , "txtLocation")))
        self.driver.find_element_by_xpath(
            "//button[@class = close and ../h5[text()='Map Key']]").click()
        searchBar = self.driver.find_element_by_id("txtLocation")
        searchBar.send_keys(location)
        searchBar.send_keys(Keys.DOWN)
        searchBar.send_keys(Keys.TAB)
        self.driver.find_element_by_xpath(
            "//form[@id='searchForm']/button[@type='submit']").click()
        self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[text()='"+location+"']")))
        self.driver.find_element_by_xpath("//button[@class = btn-info and ../span[text()='"+location+"']]").click()
        driver.implicitly_wait(10)
