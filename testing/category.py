import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service = Service(executable_path=r"C:\Users\anush\Desktop\mini project\BeautyParlour\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:8000/login")
# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "username")
username_field.send_keys("admin")
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("1234")
# Submit the category form
password_field.send_keys(Keys.RETURN)
driver.get("http://127.0.0.1:8000/admin/ShoppingApp/category/add/")
time.sleep(5)
name_field = driver.find_element(By.NAME, "name")
name_field.send_keys("test")
slug_field = driver.find_element(By.NAME, "slug")
slug_field.send_keys("test")
description_field = driver.find_element(By.NAME, "description")
description_field.send_keys("test")
# Submit the form
description_field.send_keys(Keys.RETURN)
# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div/section/div/div/form/div/div[2]/div/div/div[1]/input')
if dashboard_element:
    print("Category added")
    print("Test successful!")
else:
    print("Test failed.")
# Close the browser
driver.quit()