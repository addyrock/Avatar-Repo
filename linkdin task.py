import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# Configuration
USERNAME = 'ahmedfarooq3200012@gmail.com'
PASSWORD = 'ga3323700012'
CSV_INPUT_FILE = 'D:\\Testing Folder\\linkdin\\profiles.csv'   # Input CSV file path
EXCEL_OUTPUT_FILE = 'scraped_profiles.xlsx'  # Output Excel file path
  # Change to your chromedriver path
options = webdriver.ChromeOptions()

# Initialize the WebDriver
driver = webdriver.Chrome()

# Prepare lists to store the scraped data
data_list = []
error_list = []

try:
    # Go to LinkedIn login page
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)

    # Log in to LinkedIn
    username_input = driver.find_element(By.ID, 'username')
    password_input = driver.find_element(By.ID, 'password')
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(2)

    # Read profiles from CSV with specified encoding
    try:
        profiles_df = pd.read_csv(CSV_INPUT_FILE, encoding='ISO-8859-1')  # Change 'ISO-8859-1' if necessary
    except Exception as e:
        print(f"Error reading CSV: {e}")
        driver.quit()
        exit()

    # Loop through each profile in the CSV
    for index, row in profiles_df.iterrows():
        profile_url = row['profile_url']

        # Navigate to the profile URL directly
        driver.get(profile_url)
        time.sleep(3)  # Allow time for the profile to load

        # Initialize variables to catch the scraped data
        profile_data = {'Profile URL': profile_url, 'Name': '', 'Headline': '', 'Skills': '', 'Profile Picture': '', 'Error': ''}

        try:
            # Scrape the name
            name = driver.find_element(By.CSS_SELECTOR, 'h1').text
            profile_data['Name'] = name

            # Scrape the headline
            headline = driver.find_element(By.CSS_SELECTOR, 'h2').text
            profile_data['Headline'] = headline

            # Scrape the profile picture
            profile_picture = driver.find_element(By.CSS_SELECTOR, 'div.profile-photo img').get_attribute('src')
            profile_data['Profile Picture'] = profile_picture

            # Scrape the skills
            skills_elements = driver.find_elements(By.CSS_SELECTOR, 'span.pv-skill-category-entity__name')
            skills = [skill.text for skill in skills_elements]
            profile_data['Skills'] = ', '.join(skills)

        except Exception as e:
            profile_data['Error'] = str(e)

        # Append the profile data to the list
        data_list.append(profile_data)

    # Create a DataFrame to store the results
    results_df = pd.DataFrame(data_list)

    # Save the results to an Excel file
    results_df.to_excel(EXCEL_OUTPUT_FILE, index=False)

except Exception as e:
    print(f"An error occurred during the process: {e}")

finally:
    driver.quit()
    print(f"Scraping completed. Results saved to {EXCEL_OUTPUT_FILE}.")