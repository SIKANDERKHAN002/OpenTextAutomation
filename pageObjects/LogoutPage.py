from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pageObjects.HomePage import HomePage

class LogoutPage:
    btn_continue_xpath = "//a[normalize-space()='Continue']"
    
    def __init__(self,driver):
        self.driver = driver
    
    def clickContinue(self):
        try:
            self.driver.find_element(By.XPATH,self.btn_continue_xpath).click()
            return  HomePage(self.driver)
        except TimeoutException as e:
            print("Continue button not clickable:",str(e))
            return None    