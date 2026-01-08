from pageObjects.HomePage import HomePage
from pageObjects.AccountRegistrationPage import AccountRegistrationPage
from pageObjects.LoginPage  import LoginPage
from utilities.randomString import random_string_generator
from utilities.readProperties import ReadConfig
import time
import  pytest

class Test_Login:
    baseURL = ReadConfig.get('baseURL')
    user = ReadConfig.get('email')
    password = ReadConfig.get('password')
    @pytest.mark.sanity
    def test_login(self,setUp):
        self.driver = setUp
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.hp = HomePage(self.driver)
        self.hp.clickMyAccount()
        self.hp.clickLogin()
        self.lp = LoginPage(self.driver)
        self.lp.setEmail(self.user)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        time.sleep(20)
        self.targetElement = self.lp.isMyAccountPageExists()
        
        if self.targetElement == True:
            assert True
        else:
            assert False    