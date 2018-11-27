import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os



@pytest.mark.usefixtures("setupDriver")
class Test_keyAdder:
    def test_addKey(self,realKey):
        testKeys = [
            ["test", "error"],
            ["AIzaSyA1VBx0F3gr2YPK4KeS7ym6kMbNRUOZOB1", "error"],
            [realKey, "success"]
        ]
        for key in testKeys:
            self.addKey(key)

    def addKey(self, key):
        #populate the field with the test key and wait for the expected result
        self.driver.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='places']")))
        input = self.driver.find_element_by_name("places")
        input.send_keys(key[0])
        self.driver.find_element_by_xpath("//form[@id='APIKeyForm']/button[@type='submit']").click()
        self.driver.wait.until(
            EC.visibility_of_element_located((By.ID, key[1])))
        #if can't find the alert with expected result test will fail, no need to assert
        time.sleep(8)#wait for page to auto reload and check that it has done so
        


@pytest.mark.usefixtures("setupDriver")
class Test_locationSearch:
    def test_locationSearch(self):
        
        self.driver.wait.until(EC.visibility_of_element_located(
            (By.ID, "txtLocation")))
        
        self.closeMapKey()

        testLocations = [
            "Bantham",
            "Newquay",
            "Rhosneigr",
            "50.28, -3.87"
        ]

        for location in testLocations:
            self.search(location)

    def search(self, location):
        
        self.fillInAutocomplete(location, "txtLocation")
        #if the autocomplete fails to generate a location and marker the following test
        #will fail to find the element and fail the test
        self.searchForLocations(location)
    
    def fillInAutocomplete (self,location,id):
        #search for the location using the google places autocomplete
        searchBar = self.driver.find_element_by_id(id)
        searchBar.clear()
        searchBar.send_keys(location)
        searchBar.click()#to get the autocomplete to generate the results ddl
        time.sleep(1)#wait for it to generate
        searchBar.send_keys(Keys.DOWN)#move down into the suggestions
        time.sleep(1)#wait for it to register the selection
        searchBar.send_keys(Keys.TAB)#tab out of searchbar to complete the change event
        time.sleep(1)#wait for that to complete then submit the search
        self.driver.find_element_by_xpath(
            "//form[@id='searchForm']/div/div/button[@type='submit']").click()
    
    def closeMapKey (self):
        #close map key that appears on load, if dosen't appear and dissapear test will fail
        self.driver.find_element_by_xpath(
            "//button[@class='close' and ../h5[text()='Map Key']]").click()
        self.driver.wait.until(EC.invisibility_of_element((By.ID, 'MapKey')))

    def searchForLocations (self,location):
        #use button on marker to search for lodgings
        self.driver.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[text()='"+location+"']")))
        self.driver.find_element_by_xpath("//button[../span[text()='"+location+"']]").click()
        time.sleep(5)#allow time to visually assert result
    
