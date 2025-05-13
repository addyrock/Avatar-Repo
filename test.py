from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.wait import WebDriverWait

# Configuration
USERNAME = 'ahmedfarooq3200012@gmail.com'
PASSWORD = 'ga3323700012'
CSV_INPUT_FILE = r'D:\Testing Folder\linkdin\fixed_profiles.csv'   # Input CSV file path
EXCEL_OUTPUT_FILE = r'D:\Testing Folder\linkdin\scraped_profiles.xlsx'  # Output Excel file path
CHROME_DRIVER_PATH = r'path_to_your_chromedriver'  # Update with the path to your ChromeDriver

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

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

        # Search for the profile in LinkedIn search bar
        try:
            driver.execute_script(f"window.open('{profile_url}', '_blank');")
            time.sleep(3)  # Allow the new tab to load

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)
            # search_bar = driver.find_element(By.CSS_SELECTOR, 'input.search-global-typeahead__input')
            # search_bar.clear()
            # search_bar.send_keys(profile_url)
            # search_bar.send_keys(Keys.RETURN)
            # time.sleep(5)  # Allow search results to load
        except Exception as e:
            error_list.append({'Profile URL': profile_url, 'Error': f"Search bar issue: {e}"})
            continue

        # Initialize variables to catch the scraped data
        profile_data = {'Profile URL': profile_url, 'Name': '', 'Location': '', 'Headline': '', 'About Us': '', 'Experience': '', 'Skills': '',  'Education': '', 'Profile Picture': '', 'Error': ''}

        try:
            # Scrape the name
            name = driver.find_element(By.CSS_SELECTOR, 'h1').text
            profile_data['Name'] = name

            # Scrape the headline
            headline = driver.find_element(By.XPATH, "//h2[contains(@class, 'top-card-layout__headline')]").text
            profile_data['Headline'] = headline

            location_per = driver.find_element(By.XPATH,"//div[@class='not-first-middot']/span[1]").text
            profile_data['Location'] = location_per

            # Scrape the profile picture
            time.sleep(5)
            profile_picture = driver.find_element(By.XPATH, "//img[contains(@class, 'top-card__profile-image') and contains(@class, 'lazy-loaded')]").get_attribute('src')
            profile_data['Profile Picture'] = profile_picture

            about = driver.find_element(By.XPATH, "//div[contains(@class, 'core-section-container__content') and contains(@class, 'break-words')]/p").text
            profile_data['About Us'] = about

            # experience = driver.find_element(By.XPATH, "//section[contains(@class, 'experience')]//ul[contains(@class, 'experience__list')]/li").text
            # profile_data['Experience'] = experience
            driver.execute_script(
                "window.scrollTo(500, document.body.scrollHeight);")  # Scroll down to load dynamic content
            time.sleep(3)
            #---------------------------------------experience-----------------------------------------------#
            try:
                experience_items = driver.find_elements(By.XPATH, "//section[contains(@class, 'experience')]//ul[contains(@class, 'experience__list')]/li")
                experiences = []
                for item in experience_items:
                    job_title = item.find_element(By.XPATH, ".//span[@class='experience-item__title']").text
                    company_name = item.find_element(By.XPATH, ".//span[@class='experience-item__subtitle']").text
                    date_range = item.find_element(By.XPATH, ".//span[contains(@class, 'date-range')]").text
                    location_elements = item.find_elements(By.XPATH,
                                                           ".//p[contains(@class, 'experience-item__meta-item')]")
                    location = location_elements[-1].text if location_elements else "N/A"
                    experiences.append(f"{job_title} at {company_name} ({date_range}, {location})")
                profile_data['Experience'] = "\n".join(experiences)
            except Exception:
                profile_data['Experience'] = "Experience not found"
                # ---------------------------------------experience-----------------------------------------------#



                # # Print details
                # print(f"Job Title: {job_title}")
                # print(f"Company Name: {company_name}")
                # print(f"Date Range: {date_range}")
                # print(f"Location: {location}")
                # print("-" * 40)

            # education= driver.find_element(By.XPATH,"//li[contains(@class, 'pvs-list__paged-list-item') and contains(@class, 'pvs-list__item') and contains(@class, 'pvs-list__item--line-separated')]
            # //a[contains(@href, 'linkedin.com/company')]//span[contains(@class, 't-14')]").text
            # profile_data['Education'] = education
            driver.execute_script(
                "window.scrollTo(500, document.body.scrollHeight);")  # Scroll down to load dynamic content
            time.sleep(3)
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'education')]")))
            #
            # education_items = driver.find_elements(By.XPATH,
            #                                        "//section[contains(@class, 'education')]//ul[contains(@class, 'education__list')]/li")
            #
            # education_details = []
            # for item in education_items:
            #     try:
            #         school_name = item.find_element(By.XPATH, ".//span[contains(@class, 'education-item__title')]").text
            #     except Exception:
            #         school_name = "School name not found"
            #
            #     try:
            #         degree = item.find_element(By.XPATH, ".//span[contains(@class, 'education-item__subtitle')]").text
            #     except Exception:
            #         degree = "Degree not found"
            #
            #     try:
            #         date_range = item.find_element(By.XPATH, ".//span[contains(@class, 'date-range')]").text
            #     except Exception:
            #         date_range = "Date range not found"
            #
            #     try:
            #         additional_info_elements = item.find_elements(By.XPATH,
            #                                                       ".//p[contains(@class, 'education-item__meta-item')]")
            #         additional_info = additional_info_elements[
            #             -1].text if additional_info_elements else "Additional info not found"
            #     except Exception:
            #         additional_info = "Additional info not found"
            #
            #     education_details.append(f"{degree} from {school_name} ({date_range}, {additional_info})")
            #
            # profile_data['Education'] = "\n".join(education_details)

            #--------------------------------------------------#
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'education')]"))
            # )
            # all_education_details = []
            #
            # # Get profile name or identifier
            # try:
            #     profile_name = driver.find_element(By.XPATH,  "//title").text
            #     profile_data['Profile Name'] = profile_name# Adjust if a profile name element is available
            # except Exception:
            #     profile_name = "Profile Name Not Found"
            #
            # # Find all education list items
            # education_items = driver.find_elements(By.XPATH, "//section[contains(@class, 'education')]//ul[contains(@class, 'education__list')]/li")
            # profile_data['Skills'] = education_items
            # # Extract education details
            # for item in education_items:
            #     try:
            #         school_name = item.find_element(By.XPATH, "//section[contains(@class, 'education')]//ul[contains(@class, 'education__list')]/li").text
            #         profile_data['Institute Name'] = school_name
            #     except Exception:
            #         school_name = "School name not found"
            #
            #     try:
            #         degree = item.find_element(By.XPATH, ".//li[contains(@class, 'profile-section-card') and contains(@class, 'education__list-item')]").text
            #         profile_data['Degree'] = degree
            #     except Exception:
            #         degree = "Degree not found"
            #
            #     try:
            #         date_range = item.find_element(By.XPATH, ".//span[contains(@class, 'date-range')]").text
            #         profile_data['Date Range'] = date_range
            #     except Exception:
            #         date_range = "Date range not found"
            #
            #     # Append data with profile name
            #     all_education_details.append({
            #         "Profile Name": profile_name,
            #         "Institue Name": school_name,
            #         "Degree": degree,
            #         "Date Range": date_range
            #     })
            #
            # print("hello")
            #---------------------------------------#
            #---------------------------education--------------------------------#

            try:
                # Wait for the education section to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'education__list-item')]"))
                )
                # Locate all education items
                education_items = driver.find_elements(By.XPATH, "//li[contains(@class, 'education__list-item')]")
                education = []

                for item in education_items:
                    # Extract details for each education entry
                    try:
                        university_name = item.find_element(By.XPATH, ".//h3/a").text
                    except:
                        university_name = "N/A"

                    try:
                        associated_institute_or_degree = item.find_element(By.XPATH, ".//h4/span[1]").text
                    except:
                        associated_institute_or_degree = "N/A"

                    try:
                        degree_or_field = item.find_element(By.XPATH, ".//h4/span[@data-section='educations']").text
                    except:
                        degree_or_field = "N/A"

                    try:
                        date_range = item.find_element(By.XPATH, ".//span[contains(@class, 'date-range')]").text
                    except:
                        date_range = "N/A"

                    # Append each education entry as a dictionary (or customize as needed)
                    education.append({
                        "University": university_name,
                        "Institute/Degree": associated_institute_or_degree,
                        "Field of Study": degree_or_field,
                        "Date Range": date_range
                    })

                # Store the education details in the profile_data dictionary
                profile_data['Education'] = education
            except Exception as e:
                # Handle any errors gracefully
                profile_data['Education'] = f"Education not found. Error: {str(e)}"

            # Print all education entries (for debugging)
            for edu in profile_data['Education']:
                print(
                    f"{edu['University']} - {edu['Institute/Degree']} ({edu['Field of Study']}) [{edu['Date Range']}]")

            #----------------------------------education---------------------------#
            # Wait for the education section to be present before extracting data

            driver.execute_script("window.scrollTo(500, document.body.scrollHeight);")  # Scroll down to load dynamic content
            time.sleep(3)  # Wait for the skills section to load
            skills_elements = driver.find_elements(By.CSS_SELECTOR, '.pv-skill-category-entity__name-text')
            skills = [skill.text for skill in skills_elements if skill.text]
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
