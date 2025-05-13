from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.wait import WebDriverWait

# Configuration
USERNAME = 'your_username'
PASSWORD = 'your_password'
CSV_INPUT_FILE = r'D:\Testing Folder\linkdin\fixed_profiles.csv'  # Input CSV file path
EXCEL_OUTPUT_FILE = r'D:\Testing Folder\linkdin\scraped_profiles.xlsx'  # Output Excel file path
 # Update with the path to your ChromeDriver

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
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
    time.sleep(3)

    # Read profiles from the CSV
    try:
        profiles_df = pd.read_csv(CSV_INPUT_FILE, encoding='ISO-8859-1')
        if 'profile_url' not in profiles_df.columns:
            raise ValueError("The CSV file does not contain a 'profile_url' column.")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        driver.quit()
        exit()

    # Loop through each profile in the CSV
    for index, row in profiles_df.iterrows():
        profile_url = row.get('profile_url', '').strip()
        if not profile_url:
            error_list.append({'Index': index, 'Error': 'Missing profile URL'})
            continue

        try:
            driver.execute_script(f"window.open('{profile_url}', '_blank');")
            time.sleep(3)  # Allow the new tab to load
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(30)

            # Initialize profile data
            profile_data = {'Profile URL': profile_url, 'Name': '', 'Location': '', 'Headline': '', 'About Us': '', 'Experience': '', 'Skills': '', 'Education': '', 'Profile Picture': '', 'Error': ''}

            # Scrape basic profile information (Name, Location, etc.)
            profile_data['Name'] = driver.find_element(By.CSS_SELECTOR, 'h1').text
            profile_data['Headline'] = driver.find_element(By.XPATH, "//h2[contains(@class, 'top-card-layout__headline')]").text
            profile_data['Location'] = driver.find_element(By.XPATH, "//div[@class='not-first-middot']/span[1]").text
            profile_data['Profile Picture'] = driver.find_element(By.XPATH, "//img[contains(@class, 'top-card__profile-image') and contains(@class, 'lazy-loaded')]").get_attribute('src')
            profile_data['About Us'] = driver.find_element(By.XPATH, "//div[contains(@class, 'core-section-container__content') and contains(@class, 'break-words')]/p").text

            # Scrape experience
            experience_items = driver.find_elements(By.XPATH, "//section[contains(@class, 'experience')]//ul[contains(@class, 'experience__list')]/li")
            experiences = [f"{item.find_element(By.XPATH, './/span[@class=\'experience-item__title\']').text} at {item.find_element(By.XPATH, './/span[@class=\'experience-item__subtitle\']').text}" for item in experience_items]
            profile_data['Experience'] = "\n".join(experiences)

            # Scrape education
            education_items = driver.find_elements(By.XPATH, "//section[contains(@class, 'education')]//ul[contains(@class, 'education__list')]/li")
            education_details = [f"{item.find_element(By.XPATH, './/span[contains(@class, \'education-item__title\')]').text} ({item.find_element(By.XPATH, './/span[contains(@class, \'date-range\')]').text})" for item in education_items]
            profile_data['Education'] = "\n".join(education_details)

            # Capture all skills
            driver.execute_script("window.scrollTo(0, 2000);")  # Scroll down to make sure the skills section is visible
            time.sleep(3)  # Allow the page to load
            try:
                show_all_skills_button = driver.find_element(By.XPATH, "//a[@id='navigation-index-Show-all-12-skills']")
                if show_all_skills_button:
                    show_all_skills_button.click()
                    time.sleep(5)  # Allow the skills to load
            except Exception:
                pass  # No "Show all skills" button found, continue

            skills_elements = driver.find_elements(By.CSS_SELECTOR, '.pv-skill-category-entity__name-text')
            skills = [skill.text for skill in skills_elements if skill.text]
            profile_data['Skills'] = ', '.join(skills)

            # Append profile data to the list
            data_list.append(profile_data)

        except Exception as e:
            profile_data['Error'] = str(e)
            data_list.append(profile_data)

    # Create a DataFrame to store the results
    results_df = pd.DataFrame(data_list)

    # Save the results to an Excel file
    results_df.to_excel(EXCEL_OUTPUT_FILE, index=False)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
    print(f"Scraping completed. Results saved to {EXCEL_OUTPUT_FILE}.")
