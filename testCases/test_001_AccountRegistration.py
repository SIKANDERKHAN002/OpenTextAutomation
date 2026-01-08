from pageObjects.HomePage import HomePage
from pageObjects.AccountRegistrationPage import AccountRegistrationPage
from utilities import randomString
import  time
import pytest
from utilities.readProperties import ReadConfig
import allure



@allure.severity(allure.severity_level.CRITICAL)
class Test_001_AccountReg:
    #baseURL = "https://tutorialsninja.com/demo/index.php?route=common/home"
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
        time.sleep(5)
        self.repage.setLastName("Canedy")
        self.repage.setEmail(self.email+"@gmail.com")
        self.repage.setTelephone("656667777")
        self.repage.setPassword("ReadConfig.get('password')")
        time.sleep(5)
        self.repage.setConfirmPassword("ReadConfig.get('password')")
        time.sleep(2)
        self.repage.setPrivacyPolicy()
        self.repage.clickContinue()
        time.sleep(2)
        self.confmsg  = self.repage.getconfirmationmsg()
        print(self.confmsg)
        time.sleep(2)
        print("-----------------------------------------------------------------------------------------------------------------")
        if self.confmsg   == "Your Account Has Been Created!":
            assert   True
        else:
            assert   False    
            