from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Test_008:
    def test_Random(self):      
      # 1. Setup Browser Options
      chrome_options = Options()
      # chrome_options.add_argument("--headless") # Run without a window if needed

      # 2. Define the Hub URL (The one you asked about)
      grid_url = "http://localhost:4444/wd/hub"

      try:
        # 3. Connect to the Selenium Grid
        print(f"Connecting to Hub at {grid_url}...")
        driver = webdriver.Remote(
                 command_executor=grid_url,
                 options=chrome_options
             )

        # 4. Perform Automation
        driver.get("https://www.google.com")
    
        # Use Explicit Wait to ensure the search box is ready
        wait = WebDriverWait(driver, 10)
        print(driver.title)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

        # Type and press Enter
        search_box.send_keys("Python Dictionary methods" + Keys.RETURN)

        # 5. Extract data from the results page
        # Wait for results to load and grab the first header
        first_result = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
        print(f"First Result Title: {first_result.text}")

      except Exception as e:
       print(f"An error occurred: {e}")

      finally:
       # 6. Always close the session to free up Grid resources
       if 'driver' in locals():
           time.sleep(3) # Short pause to see the result
           driver.quit()
           print("Browser closed and session ended.")
      #This i will remove from here
      print("HELLO NEED TO REMOVE")     
      print("ADDED HERE TO TEST")
      print("ADDED ONE MORE HERE ON 26th")
      print("ADDED ONE MORE COMMENT 28th")
      print("Experimental")