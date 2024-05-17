import pytest
from selenium import webdriver

driver=webdriver.Edge()

driver.get("https://classroom.google.com/h")

driver.quit()