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
username_field.send_keys("anusha12")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("12345678")

# Submit the login form
password_field.send_keys(Keys.RETURN)


# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h4[contains(text(), 'Appointment Info')]")
if dashboard_element:
    print("Login successful!")
else:
    print("Login failed.")


# Close the browser
driver.quit()