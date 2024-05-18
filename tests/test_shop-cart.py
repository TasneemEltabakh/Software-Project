import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class TestCartPRomocode():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_cartPRomocode(self):
    self.driver.get("https://badelha.azurewebsites.net/Login")
    self.driver.set_window_size(820, 663)
    self.driver.find_element(By.NAME, "email").click()
    self.driver.find_element(By.NAME, "email").send_keys("")
    self.driver.find_element(By.NAME, "pass").click()
    self.driver.find_element(By.NAME, "pass").send_keys("2263")
    self.driver.find_element(By.CSS_SELECTOR, ".login100-form-btn").click()
    self.driver.get("https://badelha.azurewebsites.net/shop-cart")
    self.driver.set_window_size(787, 864)
    total_Pice= self.driver.find_element(By.NAME, "total_price").text
    self.vars["total_price"] = self.driver.find_element(By.NAME, "total_price").text
    print("{}".format(self.vars["total_price"]))
    self.driver.find_element(By.NAME, "promo_code").click()
    self.driver.find_element(By.NAME, "promo_code").send_keys("zewail")
    WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.NAME, "total_price")))
    discounted_price= self.driver.find_element(By.NAME, "total_price").text
    self.vars["discounted_price"] = self.driver.find_element(By.NAME, "total_price").text
    print("{}".format(self.vars["discounted_price"]))
    assert discounted_price<total_Pice
  
