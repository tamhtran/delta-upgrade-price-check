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
import re

# Load environment variables
load_dotenv()

# Configuration
DELTA_URL = "https://www.delta.com/"
DELTA_TRIPS_URL = "https://www.delta.com/mytrips/findPnrList"
USERNAME = os.getenv("DELTA_USERNAME")
PASSWORD = os.getenv("DELTA_PASSWORD")
LAST_NAME = os.getenv("DELTA_LAST_NAME")
FIRST_NAME = os.getenv("DELTA_FIRST_NAME")  # Ensure this is set in your .env file
CONFIRMATION_NO = os.getenv("DELTA_CONFIRMATION_NO")  # This is the GGCEZC variable
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

    logging.info("Submitting login form")
    password_field.send_keys(Keys.RETURN)

    # Check for the presence of the alert
    try:
        alert_present = driver.find_element(By.XPATH, '//idp-form-alert')
        if alert_present.is_displayed():
            logging.error("Error: Login failed due to form alert presence.")
            return False
    except:
        logging.info("Login successful!")
        return True


def check_upgrade_price(driver):
    logging.info("Navigating to My Trips page")
    driver.get(DELTA_TRIPS_URL)
    time.sleep(5)  # Allow some time for the page to load

    logging.info("Waiting for the trips details form to appear")
    confirmation_field = wait_for_element(driver, By.XPATH, '//input[@aria-label="Confirmation Number"]')
    first_name_field = wait_for_element(driver, By.XPATH, '//input[@aria-label="First Name"]')
    last_name_field = wait_for_element(driver, By.XPATH, '//input[@aria-label="Last Name"]')

    logging.info("Entering confirmation number")
    confirmation_field.send_keys(CONFIRMATION_NO)

    logging.info("Entering first name")
    first_name_field.send_keys(FIRST_NAME)

    logging.info("Entering last name")
    last_name_field.send_keys(LAST_NAME)

    logging.info("Submitting the form")
    last_name_field.send_keys(Keys.RETURN)

    # Wait for the page to load and the price to be visible
    logging.info("Waiting for the upgrade prices to be visible")
    price_elements = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="td-miles-column_info"]'))
    )

    # Extract and log all prices and flight details found
    results = []
    for element in price_elements:
        price_data = element.find_element(By.CLASS_NAME, 'td-miles-column_milesData').text
        flight_data = element.find_element(By.CLASS_NAME, 'td-miles-column_flightText').text

        price_match = re.search(r'\$([0-9,]+\.\d{2})', price_data)
        flight_match = re.search(r'([A-Z]{3}) - ([A-Z]{3})', flight_data)

        if price_match and flight_match:
            price = price_match.group(1)
            departure = flight_match.group(1)
            destination = flight_match.group(2)
            result = f"{price} USD for flight {departure} - {destination}"
            results.append(result)
            logging.info(f"Found: {result}")
        else:
            logging.warning(f"Data not found in text: {element.text}")

    logging.info(f"Total results found: {len(results)}")
    for result in results:
        logging.info(result)


def main():
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-data-dir={CHROME_PROFILE_PATH}')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = uc.Chrome(options=options)

    if login(driver):
        check_upgrade_price(driver)

    # Keep the browser open for 5 minutes
    time.sleep(300)
    logging.info("Keeping the browser open for 5 minutes")
    driver.quit()


if __name__ == "__main__":
    main()