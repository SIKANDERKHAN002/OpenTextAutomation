import pytest
import logging
from selenium import webdriver
from allure_commons.types import AttachmentType
from selenium.webdriver.support.events import EventFiringWebDriver,AbstractEventListener
import os
from pytest_metadata.plugin import metadata_key
from datetime import datetime
import allure
from utilities.readProperties import ReadConfig



@pytest.fixture()
def setUp(request,browser_platform):
    baseenv = ReadConfig.get('execution_env')
    browser,platform = browser_platform

    if baseenv == "remote":
        options = {
            "chrome": webdriver.ChromeOptions,
            "edge": webdriver.EdgeOptions,
            "firefox": webdriver.FirefoxOptions
        }
        platform_mapping = {"windows": "WIN10", "mac": "MAC", "linux": "LINUX"}
        platform_name = platform_mapping.get(platform)
        opt = options[browser]()
        opt.add_experimental_option("detach",True) if browser in ["chrome","edge"] else None
        opt.platform_name = platform_name
        driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",options=opt)
    elif baseenv == "local":
       if browser == 'edge':
           options = webdriver.EdgeOptions()
           options.add_experimental_option("detach", True)
           driver = webdriver.Edge(options=options)
           print("Launching Edge browser.........")
       elif browser == 'firefox':
           options = webdriver.FirefoxOptions()
           driver = webdriver.Firefox(options=options)
           print("Launching Firefox browser.........")
       else:
           options = webdriver.ChromeOptions()
           options.add_experimental_option("detach", True)
           driver = webdriver.Chrome(options=options)
           print("Launching Chrome browser.........")
           
        # Wrap original driver with EventFiringWebDriver
    event_driver = EventFiringWebDriver(driver, WebDriverLogger())

    # If using class-based tests
    request.cls.driver = event_driver
    yield driver
    event_driver.quit()
    

# CLI argument hook
def pytest_addoption(parser):
   parser.addoption("--browser",default="chrome")
   parser.addoption("--os",default="linux")
   
   
# Fixture to fetch browser option
@pytest.fixture()
def browser_platform(request):
   browser =  request.config.getoption("--browser")
   os =  request.config.getoption("--os")
   return browser, os


@pytest.hookimpl(tryfirst=True,hookwrapper=True)  #capture screenshot on failure
def pytest_runtest_makereport(item,call):
    """
    Pytest hook: Captures a screenshot automatically when a test case fails.
    """
    outcome = yield
    
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("setUp")  
        
        if driver:
            
            #Define the directory where screenshots will be stored 
            screenshot_dir = os.path.dirname(os.path.abspath(os.getcwd()))+ "//screenshots//"
            print(screenshot_dir)
            # Create directory if it doesn't exist
            os.makedirs(screenshot_dir,exist_ok=True)
            
            #capture the screenshot with the test name as the file name
            driver.save_screenshot(f"{screenshot_dir}{item.name}.png")
            allure.attach(
                driver.get_screenshot_as_png(), name=f"{item.name}", attachment_type=AttachmentType.PNG
            )


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_FILE = os.path.join(base_path,"logs","test_logging.log")


# ------------------------------  Logging SetUp ---------------------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filemode='a'
)



logger = logging.getLogger()


# ---------------- Selenium Event Listener ---------------- #
class WebDriverLogger(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        logger.info(f"Navigating to: {url}")

    def after_navigate_to(self, url, driver):
        logger.info(f"Navigation complete: {url}")

    def before_click(self, element, driver):
        try:
            logger.info(f"Clicking element: {element.tag_name} -> {element.get_attribute('outerHTML')[:100]}")
        except Exception as e:
            logger.warning(f"Click action error: {e}")

    def after_click(self, element, driver):
        logger.info("Click action completed")

    def before_change_value_of(self, element, driver):
        try:
            logger.info(f"Changing value of element: {element.get_attribute('name') or element.tag_name}")
        except Exception:
            pass

    def after_change_value_of(self, element, driver):
        logger.info("Value changed successfully")

    def on_exception(self, exception, driver):
        logger.error(f"Exception occurred: {exception}")



@pytest.hookimpl(optionalhook=True)
def pytest_configure(config):
    config.option.htmlpath = ( os.path.abspath(os.getcwd()) + "\\reports\\" + datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ".html")


@pytest.fixture(scope="function", autouse=True)
def log_test_start_end(request):
    logger.info(f"===== START TEST: {request.node.name} =====")
    yield
    logger.info(f"===== END TEST: {request.node.name} =====")
    

# Hook 1: Configure report path and add custom metadata
@pytest.hookimpl(optionalhook=True)
def pytest_configure(config):
    # config.option.htmlpath = (
    #         os.path.abspath(os.getcwd()) + "\\reports\\" + datetime.now().strftime("%d-%m-%Y %H-%M-%S") + ".html"
    # )
    config.stash[metadata_key]['Project Name'] = 'Pytest_Automation'
    config.stash[metadata_key]['Module Name'] = 'Register_Login_Search'
    config.stash[metadata_key]['Tester Name'] = 'SIKANDER'


# Hook 2: Remove default metadata
@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("Python", None)
    metadata.pop("Plugins", None)    