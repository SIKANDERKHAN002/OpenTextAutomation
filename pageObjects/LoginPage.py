from selenium.webdriver.common.by import By

class LoginPage:
    txt_email_xpath = "//input[@id='input-email']"
    txt_login_password = "//input[@id='input-password']"
    btn_login_xpath = "//input[@value='Login']"
    msg_myaccount_xpath = "//h2[text()='My Account']"
    lnk_forgotten_xpath = "(//a[text()='Forgotten Password'])[2]"
    lnk_Login_xpath = "//a[text()='Login']"
    txt_forgot_password_email = "//legend[text()='Your E-Mail Address']/following-sibling::div/div/input"
    button_continue_forgotten = "//input[@type='submit']"
    InnerText_Confirmation = "//div[text()='An email with a confirmation link has been sent your email address.']"
    InnerText_NotFound    = "//div[normalize-space()='Warning: The E-Mail Address was not found in our records, please try again!']"
    
    
    def __init__(self,driver):
        self.driver = driver
        
    def setEmail(self,email):
        self.driver.find_element(By.XPATH,self.txt_email_xpath).send_keys(email)

    def setPassword(self,pwd):
        self.driver.find_element(By.XPATH,self.txt_login_password).send_keys(pwd) 
        
    def clickLogin(self):
        self.driver.find_element(By.XPATH,self.btn_login_xpath).click()        
    
    def isMyAccountPageExists(self):
        try:
            return self.driver.find_element(By.XPATH,self.msg_myaccount_xpath).is_displayed()
        except:
            return False  
        
        
    def forgottenPassword(self):
        self.driver.find_element(By.XPATH,self.lnk_forgotten_xpath).click()
                 
    def clickLinkLogin(self):
        self.driver.find_element(By.XPATH,self.lnk_Login_xpath).click()
    
    def setTextEmail(self,forgotten_password_email):
        self.driver.find_element(By.XPATH,self.txt_email_xpath).send_keys(forgotten_password_email)
    
    def clickContinue(self):
        self.driver.find_element(By.XPATH,self.button_continue_forgotten).click()
        
    def validateEmailMessage(self):
        textData = self.driver.find_element(By.XPATH,self.InnerText_Confirmation).text    
        print(textData)
                
        
    def validateEmailMessageNotFound(self):
        textData = self.driver.find_element(By.XPATH,self.InnerText_NotFound).text    
        print(textData)    
        