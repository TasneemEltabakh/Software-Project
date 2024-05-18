'''import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestAddToCart():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_addToCart(self):
    self.driver.get("https://badelha.azurewebsites.net/shop-cart")
    self.driver.set_window_size(1552, 880)
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .delete-symbol").click()
    assert self.driver.switch_to.alert.text == "Are you sure you want to delete this item?"
    self.driver.switch_to.alert.accept()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .delete-symbol").click()
    assert self.driver.switch_to.alert.text == "Are you sure you want to delete this item?"
    self.driver.switch_to.alert.accept()'''
  
