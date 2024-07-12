import os
import logging
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()

# Configuration
DELTA_URL = "https://www.delta.com/"
USERNAME = os.getenv("DELTA_USERNAME")
PASSWORD = os.getenv("DELTA_PASSWORD")
LAST_NAME = os.getenv("DELTA_LAST_NAME")
CHROME_PROFILE_PATH = os.path.expanduser(
    "~/Library/Application Support/Google/Chrome/Default")  # Change 'Default' to your specific profile if needed

# Ensure spaces in the path are correctly handled
CHROME_PROFILE_PATH = f'"{CHROME_PROFILE_PATH}"'

# Configure logging to print to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

# Set the SSL_CERT_FILE environment variable to use certifi's CA bundle
os.environ['SSL_CERT_FILE'] = certifi.where()

def wait_for_element(driver, by, value, timeout=30):
    for _ in range(timeout):
        try:
            element = driver.find_element(by, value)
            if element.is_displayed() and element.is_enabled():
                return element
        except:
            pass
        time.sleep(1)
    raise Exception(f"Element with {by}={value} not found after {timeout} seconds")

def login(driver):
    logging.info("Navigating to Delta homepage")
    driver.get(DELTA_URL)
    time.sleep(5)  # Allow some time for the page to load

    logging.info("Clicking the login button")
    login_button = wait_for_element(driver, By.ID, 'login-modal-button')
    login_button.click()

    logging.info("Waiting for the login modal to appear")
    username_field = wait_for_element(driver, By.XPATH, '//input[@aria-label="SkyMiles Number Or Username*"]')
    password_field = wait_for_element(driver, By.XPATH, '//input[@aria-label="Password*"]')

    logging.info("Entering username")
    username_field.send_keys(USERNAME)

    logging.info("Entering password")
    password_field.send_keys(PASSWORD)



    try:
        logging.info("Submitting login form")
        password_field.send_keys(Keys.RETURN)
        # # Locate the login button using its class name and click it
        # login_button = wait_for_element(driver, By.CLASS_NAME, 'loginModal-button')
        # login_button.click()

        # Check for the presence of the alert
        try:
            alert_present = driver.find_element(By.XPATH, '//idp-form-alert')
            if alert_present.is_displayed():
                logging.error("Error: Login failed due to form alert presence.")
                return
        except:
            logging.info("Login successful!")

    except Exception as e:
        logging.error(f"Login failed: {e}")


def main():
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-data-dir={CHROME_PROFILE_PATH}')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = uc.Chrome(options=options)

    login(driver)
    logging.info("The end")

    # Keep the browser open for 5 minutes
    # driver.quit()
    time.sleep(3000)


if __name__ == "__main__":
    main()