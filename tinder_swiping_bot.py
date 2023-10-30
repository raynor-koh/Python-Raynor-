from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

EMAIL = ""
PASSWORD = ""

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://tinder.com/")
time.sleep(1)

login_button = driver.find_elements(By.CLASS_NAME, "l17p5q9z")[2]
login_button.click()
time.sleep(1)

login_facebook = driver.find_element(By.XPATH, '//*[@id="u787367660"]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button')
login_facebook.click()
time.sleep(1)

base_window = driver.window_handles[0]
facebook_login = driver.window_handles[1]
driver.switch_to.window(facebook_login)
print(driver.title)

credentials = driver.find_elements(By.CLASS_NAME, "inputtext._55r1.inputtext.inputtext")
email = credentials[0]
password = credentials[1]
email.send_keys(EMAIL)
password.send_keys(PASSWORD)
password.send_keys(Keys.ENTER)

driver.switch_to.window(base_window)
print(driver.title)
time.sleep(5)

#Allow location
allow_location_button = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
allow_location_button.click()

#Disallow notifications
notifications_button = driver.find_element(By.XPATH, '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
notifications_button.click()

#Allow cookies
cookies = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div/div[1]/button')
cookies.click()

for n in range(100):

    #Add a 1 second delay between likes.
    time.sleep(1)

    try:
        print("called")
        like_button = driver.find_element(By.XPATH,
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_button.click()

    #Catches the cases where there is a "Matched" pop-up in front of the "Like" button:
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, ".itsAMatch a")
            match_popup.click()

        #Catches the cases where the "Like" button has not yet loaded, so wait 2 seconds before retrying.
        except NoSuchElementException:
            time.sleep(2)

driver.quit()
