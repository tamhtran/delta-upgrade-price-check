import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DELTA_URL = "https://www.delta.com/"
USERNAME = os.getenv("DELTA_USERNAME")
PASSWORD = os.getenv("DELTA_PASSWORD")
LAST_NAME = os.getenv("DELTA_LAST_NAME")


def login(driver):
    driver.get(DELTA_URL)
    wait = WebDriverWait(driver, 10)

    # Locate and click the login button
    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login-modal-button')))
    login_button.click()

    # Wait for the modal to appear and find the username, last name, and password fields
    username_field = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@aria-label="SkyMiles Number Or Username*"]')))
    last_name_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Last Name*"]')))
    password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Password*"]')))

    # Enter username, last name, and password
    username_field.send_keys(USERNAME)
    last_name_field.send_keys(LAST_NAME)
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # Check for successful login (adjust the selector for a post-login element)
    try:
        wait.until(EC.presence_of_element_located(
            (By.ID, 'post-login-element-id')))  # Replace with an actual element ID visible after login
        print("Login successful!")
    except Exception as e:
        print(f"Login failed: {e}")


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    try:
        login(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()