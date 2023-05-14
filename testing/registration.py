import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service = Service(executable_path=r"C:\Users\anush\Desktop\mini project\BeautyParlour\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Navigate to the registration page
driver.get("http://127.0.0.1:8000/register")

# Locate the input fields and input test data
username_field = driver.find_element(By.NAME, "username")
username_field.send_keys("testuser2")

first_name_field = driver.find_element(By.NAME, "first_name")
first_name_field.send_keys("test")

last_name_field = driver.find_element(By.NAME, "last_name")
last_name_field.send_keys("user")

email_field = driver.find_element(By.NAME, "email")
email_field.send_keys("testuser2@example.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("testpassword")

confirm_password_field = driver.find_element(By.NAME, "cpassword")
confirm_password_field.send_keys("testpassword")

# Submit the registration form
confirm_password_field.send_keys(Keys.RETURN)

# Wait for the page to load and check for the presence of a success message
dashboard_element = driver.find_element(By.XPATH, '/html/body/div/form/center/input')
if dashboard_element:
    print("Registration successful!")
else:
    print("Registration failed.")

# Close the browser
driver.quit()
