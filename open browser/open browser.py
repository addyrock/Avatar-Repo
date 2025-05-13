import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure Selenium
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

  # Replace with your chromedriver path
driver = webdriver.Chrome(options=options)

# Open the website
try:
    driver.get("https://www.pokemoncenter.com")
    time.sleep(10)
    driver.find_element(By.XPATH,"//input[@id='search-mobile']").send_keys("shirt")
    time.sleep(30)
    # Perform actions on the site
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    driver.quit()
