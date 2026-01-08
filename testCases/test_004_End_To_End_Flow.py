from pageObjects.HomePage import HomePage
from pageObjects.AccountRegistrationPage import AccountRegistrationPage
from pageObjects.LoginPage  import LoginPage
from utilities.randomString import random_string_generator
from utilities.readProperties import ReadConfig
from pageObjects.MyAccountPage import MyAccountPage
from utilities import randomString
from pageObjects.LogoutPage import LogoutPage
import time
import  pytest

class Test_EndToEnd:
    baseURL =  ReadConfig.get('baseURL')
    email =    randomString.random_string_generator()
    #user =    ReadConfig.get('email')
    password = ReadConfig.get('password')
    
    @pytest.mark.regression
    @pytest.mark.sanity
    def test_004_End_To_End_Flow(self,setUp):
        
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
        email = self.email+"@gmail.com"
        self.repage.setEmail(email)
        self.repage.setTelephone("656667777")
        self.repage.setPassword(self.password)
        time.sleep(5)
        self.repage.setConfirmPassword(self.password)
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
        time.sleep(10) 
        #------------------------------------------------------- Acccount Created ------------------------------------------------
        
        
        self.ma = MyAccountPage(self.driver)
        
        self.ma.clickLogout()
        self.lop = LogoutPage(self.driver)
        self.lop.clickContinue()
        
        assert self.hp.isHomePageExists(), "Logout failed or did not return to home page"
         

        self.driver.implicitly_wait(10)
        self.hp.clickMyAccount()
        self.hp.clickLogin()
        
        self.lp = LoginPage(self.driver)
        self.lp.setEmail(email)
        self.lp.setPassword(self.password)
        self.lp.clickLogin()
        
        time.sleep(5)
        
        self.targetElement = self.lp.isMyAccountPageExists()
        if self.targetElement == True:
            assert True
        else:
            assert False    
        time.sleep(5)    