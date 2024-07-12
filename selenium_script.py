import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
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
CHROME_PROFILE_PATH = os.path.expanduser(
    "~/Library/Application Support/Google/Chrome/Default")  # Change 'Default' to your specific profile if needed

# Ensure spaces in the path are correctly handled
CHROME_PROFILE_PATH = f'"{CHROME_PROFILE_PATH}"'

# Configure logging to print to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])


def login(driver):
    logging.info("Navigating to Delta homepage")
    driver.get(DELTA_URL)
    wait = WebDriverWait(driver, 300)  # Increase timeout to 20 seconds

    # Wait until the page is fully loaded
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    logging.info("Done Navigating to Delta homepage")

    # Print the current URL
    current_url = driver.current_url
    logging.info(f"Current URL: {current_url}")

    logging.info("Clicking the login button")
    login_button = wait.until(EC.element_to_be_clickable((By.ID, 'login-modal-button')))
    login_button.click()

    logging.info("Waiting for the login modal to appear")
    username_field = wait.until(
        EC.presence_of_element_located((By.XPATH, '//input[@aria-label="SkyMiles Number Or Username*"]')))
    password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Password*"]')))

    logging.info("Entering username")
    username_field.send_keys(USERNAME)

    logging.info("Entering password")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.RETURN)

    # logging.info("Entering last name")
    # last_name_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Last Name*"]')))
    # last_name_field.send_keys(LAST_NAME)


    logging.info("Submitting login form")
    try:
        # Locate the login button using its class name and click it
        login_button = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'loginModal-button'))
        )
        login_button.click()
        logging.info("Login successful!")

    except Exception as e:
        logging.error(f"Login failed: {e}")


def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("start-maximized")
    # Set the user agent to a standard Chrome user agent string
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")

    chrome_options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
    # Remove headless option to see if that helps with access denied issue
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Enable CDP and set headers
    cdp_session = driver.execute_cdp_cmd('Network.enable', {})
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "Dnt": "1",
        "Priority": "u=0, i",
        "Referer": "https://www.google.com/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Dtpc": "8$18628754_245h13vPCPCIWSEFFUAWITRVMUFBHIISJCJAWND-0e0",
    }

    def set_header(headers):
        driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {'headers': headers})

    set_header(headers)

    login(driver)

    # Keep the browser open for 5 minutes
    time.sleep(300)
    logging.info("Keeping the browser open for 5 minutes")
    driver.quit()


if __name__ == "__main__":
    main()
    # print out the .env variables
    # print(USERNAME, PASSWORD, LAST_NAME)