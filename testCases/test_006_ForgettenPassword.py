
from pageObjects.LoginPage import LoginPage
from pageObjects.HomePage import  HomePage
from utilities.readProperties import ReadConfig
import time
import  pytest

class Test_ForgottenPassword:
    base_URL = ReadConfig.get("baseURL")
    
    @pytest.mark.smoke
    def test_forgettonPassword(self,setUp):
        self.driver = setUp
        self.driver.get(self.base_URL)
        self.driver.maximize_window()
        
        self.driver.implicitly_wait(10)
              
        self.lg = LoginPage(self.driver)
        self.hm = HomePage(self.driver)
        
        self.hm.clickMyAccount()
        self.driver.implicitly_wait(5)
        self.lg.clickLinkLogin()
        self.lg.forgottenPassword(self)
        time.sleep(10)   