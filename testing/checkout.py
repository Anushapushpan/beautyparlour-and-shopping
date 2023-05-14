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
driver.get("http://127.0.0.1:8000/ShoppingApp/makeup/blue-heaven-hyperstay-matte-mystic-maroon-05/")


time.sleep(5)
# Locate the username and password fields and input the credentials
product_field = driver.find_element(By.NAME, "product")
product_field.send_keys("blue heaven hyperstay matte - mystic maroon-05")
#
# lname_field = driver.find_element(By.NAME, "lname")
# lname_field.send_keys("user")
#
# email_field = driver.find_element(By.NAME, "email")
# email_field.send_keys("testuser@gmail.com")
#
# mobile_field = driver.find_element(By.NAME, "phone")
# mobile_field.send_keys("6999999999")
#
# address_field = driver.find_element(By.NAME, "address")
# address_field.send_keys("test user")
#
# city_field = driver.find_element(By.NAME, "city")
# city_field.send_keys("kollam")
#
# state_field = driver.find_element(By.NAME, "state")
# state_field.send_keys("Kerala")
#
# country_field = driver.find_element(By.NAME, "country")
# country_field.send_keys("India")
#
# pincode_field = driver.find_element(By.NAME, "pincode")
# pincode_field.send_keys("666666")
# Submit the login form
product_field.send_keys(Keys.RETURN)

time.sleep(5)
# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[1]/a')
if dashboard_element:
    print("product added successful!")
else:
    print("Payment failed.")


# Close the browser
driver.quit()