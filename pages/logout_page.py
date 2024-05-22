from .base_page import BasePage
from ..resources.locators import LogoutPageLocators
from .login_page import LoginPage

class LogoutPage(BasePage):
    def logout(self):
        self.find_element(LogoutPageLocators.LOGOUT_BUTTON).click()
        return LoginPage(self.driver)
    
    def confirm_logout(self):
        self.find_element(LogoutPageLocators.CONFIRM_LOGOUT_BUTTON).click()
        return LoginPage(self.driver)