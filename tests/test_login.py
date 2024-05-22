from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver
driver = webdriver.Chrome()  # or use webdriver.Firefox(), etc. depending on your browser
driver.maximize_window()

# URL to be tested
url = "https://planidea.netlify.app/"

try:
    # Navigate to the URL
    driver.get(url)

    # Wait until the login form is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login-form"))  # Adjust the locator as needed
    )

    # Find the username and password input fields
    username_field = driver.find_element(By.ID, "username")  # Adjust the locator as needed
    password_field = driver.find_element(By.ID, "password")  # Adjust the locator as needed

    # Enter login credentials
    username = "testuser"
    password = "testpassword"
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Find and click the login button
    login_button = driver.find_element(By.ID, "login-button")  # Adjust the locator as needed
    login_button.click()

    # Wait for the next page to load and check if login was successful
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dashboard"))  # Adjust the locator as needed
    )

    # Check if login was successful by verifying the presence of an element on the dashboard
    dashboard_element = driver.find_element(By.ID, "dashboard")  # Adjust the locator as needed
    if dashboard_element:
        print("Login successful")
    else:
        print("Login failed")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
