
from utilities.readProperties import ReadConfig
from selenium.webdriver.common.by import By
import time
import  pytest
import  requests



class Test_Broken_Links:
    base_URL = ReadConfig.get('baseURL')
    
    @pytest.mark.regression
    @pytest.mark.sanity
    def test_broken_Links(self,setUp):
        self.driver = setUp
        self.driver.get(self.base_URL)
        self.driver.maximize_window()
        
        self.driver.implicitly_wait(10)
        link_all = self.driver.find_elements(By.TAG_NAME,"a")
        print(f" Likns ==>  {link_all}")
        
        time.sleep(10)
        
        broken_Link = 0
        counter = 1 
        for data in link_all:
            url = data.get_attribute("href")
            
            if url and url.startswith("http"):
               try:
                   # Use requests to send a HEAD request (more efficient than GET as it only retrieves headeaders"
                   # allow_redirects = True ensures we follow redirects and check the final destination 
                   response = requests.head(url,timeout=5)
                   if response.status_code >= 400:
                       print(f"[BROKEN] Status Code: {response.status_code}")
                       broken_Link+=1                      
               except   requests.exceptions.RequestException as e:
                     print(f"{counter}\t {data_Item}")
                     broken_Link+=1
                     #list_Count.append(data_Item)
                     #time.sleep(5)        
                     #print(f"Count is ==> \t {len(list_Count)}" )
        
        
        if broken_Link == 0:
            print("All Links are valid")
        else:
            print(f"\n Total broken links found: {broken_Link}")    
        