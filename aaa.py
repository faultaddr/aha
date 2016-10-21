# -*- coding:utf-8 -*-
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Firefox()
driver.get("http://www.baidu.com")
#assert("百度" in driver.title)
elem = driver.find_element_by_name("wd")
elem.send_keys("selenium")
elem.send_keys(Keys.RETURN)
#assert "百度" in driver.title
driver.close()
driver.quit()
driver = None