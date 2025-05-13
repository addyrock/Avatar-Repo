import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
product_url = 'https://www.pokemoncenter.com/'  # Replace with actual product URL
login_url = 'https://www.pokemoncenter.com/'  # Replace with login URL if required
username = 'your_username'
password = 'your_password'

# Set up Chrome options (headless if you want to run in background)
options = Options()
options.headless = False  # Set to True if you want the browser to run in background

 # Replace with the path to your ChromeDriver
driver = webdriver.Chrome(options=options)

# Open the login page and log in (optional)
driver.get(login_url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
driver.find_element(By.ID, 'username').send_keys(username)
driver.find_element(By.ID, 'password').send_keys(password)
driver.find_element(By.ID, 'login_button').click()

# Wait for login to complete (if login is required)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user-profile')))

# Continuous loop to check for availability and attempt purchase
while True:
    driver.get(product_url)

    try:
        # Check if the product is available (this depends on the website)
        # Example: Look for a button with class 'buy-now'
        buy_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'buy-now')))

        # If the button is found, it means the product is available
        if buy_button.is_displayed():
            print("Product is available! Attempting to buy...")
            buy_button.click()  # Simulate a click to buy the product

            # Wait for the checkout page (you can add more steps to complete checkout)
            time.sleep(5)

            # Confirm purchase (assuming there's a 'Confirm Purchase' button)
            confirm_button = driver.find_element(By.CLASS_NAME, 'confirm-purchase')
            confirm_button.click()

            print("Product purchased successfully!")
            break  # Stop after the purchase

        else:
            print("Product is not available yet. Checking again in 1 minute.")

    except Exception as e:
        print(f"Error: {e}")

    # Wait 1 minute before checking again
    time.sleep(60)

driver.quit()
