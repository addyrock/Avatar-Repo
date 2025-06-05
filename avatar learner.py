import time

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


@pytest.fixture(scope="module")
def setup():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--headless')  # Uncomment if you want to run in headless mode

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    yield driver


def take_screenshot(driver, step_name):
    driver.save_screenshot(f"{step_name}.png")



def blink_element(driver, element, duration=1, iterations=3):
    """Blinks a Selenium Webdriver element"""
    original_style = element.get_attribute('style')
    highlight_style = "background: yellow; border: 5px solid red;"

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)

    for _ in range(iterations):
        apply_style(highlight_style)
        time.sleep(duration / (2 * iterations))
        apply_style(original_style)
        time.sleep(duration / (2 * iterations))

def test_title_verification(setup):
    driver = setup
    driver.get("https://avatar.nuewma.com/")
    expected_title = "Avatar"
    actual_title = driver.title
    assert actual_title == expected_title, f"Test Failed: Title is '{actual_title}' but expected '{expected_title}'"
    print( "Actual Title is '{AvatarCoachApp}' but expected '{Avatar}'")
    take_screenshot(driver, 'title_verification')


def login(driver, username, password):
    username_field = driver.find_element(By.XPATH, "//input[@placeholder='Your Email']")
    password_field = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    login_button = driver.find_element(By.XPATH, "//input[@value='SIGN IN']")


    blink_element(driver, username_field)
    username_field.send_keys(username)
    blink_element(driver, password_field)
    password_field.send_keys(password)
    blink_element(driver, login_button)
    login_button.click()


# def test_login_blank_field(setup):
#     driver = setup
#     time.sleep(1)
#     empty_username = ""
#     empty_password = ""
#     login(driver, empty_username, empty_password)
#
#     try:
#         WebDriverWait(driver, 1).until(EC.alert_is_present())
#         alert = driver.switch_to.alert
#         assert "Please fill out this " in alert.text
#         alert.accept()
#     except TimeoutException:
#         pass
#     take_screenshot(driver, 'login_blank_field')
#
# def test_user_name_empty(setup):
#     driver = setup
#     time.sleep(1)
#     empty_username = ""
#     valid_password = "123456@abc"
#     login(driver, empty_username, valid_password)
#     try:
#         error_message = WebDriverWait(driver, 5).until(
#             EC.presence_of_element_located((By.XPATH, "//div[@class='error']"))
#         )
#         assert error_message.is_displayed()
#         take_screenshot(driver, "Email is required.")
#         print("Login Test Passed: Unsuccessful login displayed error message")
#     except Exception as e:
#
#         pytest.fail(f"Login Test Failed: No error message displayed for unsuccessful login. Exception: {e}")
#
#     take_screenshot(driver, 'Empty_user_name')
#
# def test_only_password_empty(setup):
#     driver = setup
#     time.sleep(1)
#     username = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
#     username.clear()
#     valid_username = "QA_USER"
#     empty_password = ""
#     login(driver, valid_username, empty_password)
#
#     try:
#         WebDriverWait(driver, 3).until(EC.alert_is_present())
#         alert = driver.switch_to.alert
#         assert "Please fill out this field" in alert.text
#         alert.accept()
#     except TimeoutException:
#         pass
#     take_screenshot(driver, 'Empty_Password')
#
# def test_wrong_credentials(setup):
#     driver = setup
#     username = driver.find_element(By.XPATH, "//input[@placeholder='Your Email']")
#     username.clear()
#     invalid_username = "QA_USER1"
#     invalid_password = "12345@"
#     login(driver, invalid_username, invalid_password)
#     time.sleep(2)
#     try:
#         WebDriverWait(driver, 3).until(EC.alert_is_present())
#         alert = driver.switch_to.alert
#         assert "Password must be between 8 and 25 characters" in alert.text
#         alert.accept()
#     except TimeoutException:
#         pass
#     take_screenshot(driver, 'Invalid_Credentials')

def test_valid_Credential(setup):
    driver = setup
    time.sleep(1)
    username = driver.find_element(By.XPATH, "//input[@placeholder='Your Email']")
    username.clear()
    username = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    username.clear()
    valid_username = "devops15@gmail.com"
    valid_password = "123456"
    login(driver, valid_username, valid_password)
    time.sleep(2)
    assert "Sucsessfully logged in"
    take_screenshot(driver, 'Sucsessfully log in')

    time.sleep(3)

def test_profile(setup):
    driver = setup
    pro_link = driver.find_element(By.XPATH,"//div[@class='name-div']")
    blink_element(driver,pro_link)
    pro_link.click()
    time.sleep(5)

def test_profile_pic(setup):
    driver = setup
    time.sleep(2)
    first_name=driver.find_element(By.XPATH,"//input[@placeholder='First Name']")
    blink_element(driver,first_name)
    first_name.clear()
    first_name.click()
    time.sleep(2)
    last_name = driver.find_element(By.XPATH, "//input[@placeholder='Last Name']")
    blink_element(driver, last_name)
    last_name.clear()
    last_name.click()
    time.sleep(2)
    num_show=driver.find_element(By.XPATH,"//input[@placeholder='Your Phone Number']")
    blink_element(driver,num_show)
    num_show.clear()
    num_show.click()
    time.sleep(2)
    pro_click = driver.find_element(By.XPATH, "//input[@value='Submit']")
    blink_element(driver, pro_click)
    pro_click.click()
    time.sleep(8)
    driver.find_element(By.XPATH, "//button[normalize-space()='OK']").click()
    time.sleep(10)
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )
    file_path = "D:\Testing Folder\\1.jpg"
    file_input.send_keys(file_path)
    take_screenshot(driver, 'File_Upload')
    time.sleep(5)
    first_name = driver.find_element(By.XPATH, "//input[@placeholder='First Name']")
    blink_element(driver, first_name)
    first_name.clear()
    first_name.send_keys("devops16")
    time.sleep(2)
    last_name = driver.find_element(By.XPATH, "//input[@placeholder='Last Name']")
    blink_element(driver, last_name)
    last_name.clear()
    last_name.send_keys("Learner")
    time.sleep(2)
    num_show = driver.find_element(By.XPATH, "//input[@placeholder='Your Phone Number']")
    blink_element(driver, num_show)
    num_show.clear()
    num_show.send_keys("72729988")
    time.sleep(2)
    pro_click = driver.find_element(By.XPATH,"//input[@value='Submit']")
    blink_element(driver,pro_click)
    pro_click.click()
    time.sleep(8)
    driver.find_element(By.XPATH, "//button[normalize-space()='OK']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//button[normalize-space()='OK']").click()
    time.sleep(10)