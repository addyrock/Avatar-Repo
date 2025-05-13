import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')
# List of profile URLs to scrape (replace with actual URLs)
profile_urls = [
    "https://www.linkedin.com/in/saziya-praveen-875739315/",
    "https://www.linkedin.com/in/neyazuddin-ansari-b00447291/"
]

# List to store education details with profile data
time.sleep(15)
all_education_details = []

# Loop through each profile
for profile_url in profile_urls:
    driver.get(profile_url)

    # Wait for the education section to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'education')]"))
    )

    # Get profile name or identifier
    try:
        profile_name = driver.find_element(By.XPATH, "//title").text  # Adjust if a profile name element is available
    except Exception:
        profile_name = "Profile Name Not Found"

    # Find all education list items
    education_items = driver.find_elements(By.XPATH, "//section[contains(@class, 'education')]//ul[contains(@class, 'education__list')]/li")

    # Extract education details
    for item in education_items:
        try:
            school_name = item.find_element(By.XPATH, ".//h3").text
        except Exception:
            school_name = "School name not found"

        try:
            degree = item.find_element(By.XPATH, ".//h4").text
        except Exception:
            degree = "Degree not found"

        try:
            date_range = item.find_element(By.XPATH, ".//span[contains(@class, 'date-range')]").text
        except Exception:
            date_range = "Date range not found"

        # Append data with profile name
        all_education_details.append({
            "Profile Name": profile_name,
            "School Name": school_name,
            "Degree": degree,
            "Date Range": date_range
        })

# Save data to Excel
df = pd.DataFrame(all_education_details)
df.to_excel("D:\\Testing Folder\\linkdin\\education_details_per_profile.xlsx", index=False)
print("Education details saved to 'education_details_per_profile.xlsx'")

# Close WebDriver
driver.quit()
