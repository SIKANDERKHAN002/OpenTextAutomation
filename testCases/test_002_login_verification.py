from pageObjects.HomePage import HomePage
from pageObjects.AccountRegistrationPage import AccountRegistrationPage
from pageObjects.LoginPage  import LoginPage
from utilities.randomString import random_string_generator
from utilities.readProperties import ReadConfig
import time
import pytest

class Test_Login:
    """
    Test class for login functionality.

    This class verifies whether a registered user can successfully
    log in to the application using valid credentials.
    """
    
    baseURL = ReadConfig.get('baseURL')
    user = ReadConfig.get('email')
    password = ReadConfig.get('password')
    @pytest.mark.sanity
    def test_login(self,setUp):
        """
        Test Case: Verify User Login

        Description:
        Verify that a registered user can successfully log in using
        valid email and password.

        Test Steps:
        1. Launch application URL
        2. Click on My Account
        3. Click on Login
        4. Enter valid email address
        5. Enter valid password
        6. Click Login button
        7. Verify My Account page is displayed

        Expected Result:
        User should be successfully logged in and My Account page should be displayed.
        """
        
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
        self.targetElement = self.lp.isMyAccountPageExists()
        
        if self.targetElement == True:
            assert True
        else:
            assert False    