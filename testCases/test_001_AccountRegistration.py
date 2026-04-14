from pageObjects.HomePage import HomePage
from pageObjects.AccountRegistrationPage import AccountRegistrationPage
from utilities.readProperties import ReadConfig
from utilities import randomString
import pytest
import allure
import time



@allure.severity(allure.severity_level.CRITICAL)
class Test_001_AccountReg:
    baseURL = ReadConfig.get('baseURL')
    email = randomString.random_string_generator()
    @pytest.mark.regression
    @pytest.mark.sanity
    def test_account_reg(self,setUp):
        self.driver = setUp
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.hp = HomePage(self.driver)
        self.hp.clickMyAccount()
        self.hp.clickRegister()
        self.repage = AccountRegistrationPage(self.driver)
        self.repage.setFirstName("John")
        self.repage.setLastName("Canedy")
        self.repage.setEmail(self.email+"@gmail.com")
        self.repage.setTelephone("656667777")
        self.repage.setPassword("ReadConfig.get('password')")
        self.repage.setConfirmPassword("ReadConfig.get('password')")
        self.repage.setPrivacyPolicy()
        self.repage.clickContinue()
        self.confmsg  = self.repage.getconfirmationmsg()
        print(self.confmsg)
        if self.confmsg   == "Your Account Has Been Created!":
            assert   True
        else:
            assert   False    
            