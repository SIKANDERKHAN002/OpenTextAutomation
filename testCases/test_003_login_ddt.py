from   pageObjects.LoginPage import LoginPage
from   pageObjects.HomePage import HomePage
from   pageObjects.MyAccountPage import MyAccountPage
from   utilities.readProperties import ReadConfig
from   utilities  import XLUtils
import time
import os
import pytest

class Test_001_AccountReg:
    baseURL = ReadConfig.get('baseURL')
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_path,'testData','Tutorialninja_LoginData.xlsx')
    @pytest.mark.sanity
    def test_account_reg(self,setUp):
        lst_status = []
        self.rows = XLUtils.getRowCount(self.path,sheetName="Sheet1")
        self.driver = setUp
        self.driver.get(self.baseURL)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.hp = HomePage(self.driver)
        self.lp = LoginPage(self.driver)
        self.ma = MyAccountPage(self.driver)
        time.sleep(10)
        for r in range(2,self.rows+1):
            self.hp.clickMyAccount()
            self.hp.clickLogin()
            self.email = XLUtils.readData(self.path,"Sheet1",r,1)
            self.password = XLUtils.readData(self.path,"Sheet1",r,columnno=2)
            self.exp = XLUtils.readData(self.path,"Sheet1",r,columnno=3)
            self.lp.setEmail(self.email)
            self.lp.setPassword(self.password)
            self.lp.clickLogin()
            time.sleep(2)
            self.targetpage = self.lp.isMyAccountPageExists()
            print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
            print(self.targetpage)
            
            if self.exp == 'Valid':
                if self.targetpage == True:
                   lst_status.append('Pass')
                   time.sleep(2)
                   self.ma.clickLogout()
                else:
                   lst_status.append('Fail')
            elif self.exp == "Invalid":
                if  self.targetpage ==True:
                    time.sleep(2)
                    lst_status.append('Fail')
                    self.ma.clickLogout()
                else:
                    lst_status.append('Pass')
                     
            if 'Fail' in lst_status:
                assert False
            else:
                assert True
                                                        
                