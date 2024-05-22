from .base_page.py import BasePage
from ..resources.locators import LoginPageLocators  
from ..resources.locators import HomePageLocators
from selenium.webdriver.support.ui import WebDriverWait

class LoginPage(BasePage):
    def login(self, username, password):
        self.find_element(LoginPageLocators.USERNAME).send_keys(username)
        self.find_element(LoginPageLocators.PASSWORD).send_keys(password)
        self.find_element(LoginPageLocators.LOGIN_BUTTON).click()
        return HomePage(self.driver)
    
    