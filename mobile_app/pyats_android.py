
import logging
import time
from pyats import aetest
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.appium_service import AppiumService
log = logging.getLogger(__name__)


###################################################################
###                     TESTCASES SECTION                       ###
###################################################################

class tc_android_calculator(aetest.Testcase):
    @aetest.setup
    def prepare_testcase(self, section):
        """ Testcase Setup section """
        log.info("Preparing the test")
        # Make sure python client is installed "pip install Appium-Python-Client"
        # Make sure appium is installed 'npm install -g appium'
        self.appium_service = AppiumService()
        # By default appium starts server at port 4723.
        # You can pass port as argument in AppiumService to change it.
        self.appium_service.start()
        log.info(self.appium_service.is_running)

        # Following is desired capabilities for Android app
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0'
        desired_caps['automationName'] = 'androidautomator'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'com.android.calculator2'
        desired_caps['appActivity'] = 'com.android.calculator2.Calculator'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        
        # Following is example of testing iOS app
        # desired_caps['platformName'] = 'iOS'
        # desired_caps['platformVersion'] = '11.0'
        # desired_caps['automationName'] = 'iosautomator'
        # desired_caps['deviceName'] = 'iPhone 7'
        # desired_caps['app'] = '/path/to/my.app'

    # First test section
    @ aetest.test
    def pass_check(self):
        no_7 = self.driver.find_element(value="digit_7", by=By.ID)
        no_7.click();
        plus = self.driver.find_element(value="op_add", by=By.ID)
        plus.click();
        no_4 = self.driver.find_element(value="digit_4", by=By.ID)
        no_4.click();
        equalTo = self.driver.find_element(value="eq", by=By.ID)
        equalTo.click();
        results = self.driver.find_element(value="formula", by=By.ID)
        result_value = results.get_attribute('text')
        if result_value == '11':
            self.passed('Value is 11')
        else:
            self.failed('Value is not 11')

    # Second test section
    @ aetest.test
    def failure_check(self):
        no_7 = self.driver.find_element(value="digit_7", by=By.ID)
        no_7.click();
        plus = self.driver.find_element(value="op_add", by=By.ID)
        plus.click();
        no_4 = self.driver.find_element(value="digit_4", by=By.ID)
        no_4.click();
        equalTo = self.driver.find_element(value="eq", by=By.ID)
        equalTo.click();

        results = self.driver.find_element(value="formula", by=By.ID)
        result_value = results.get_attribute('text')
        if result_value == '12':
            self.passed('Value is 12')
        else:
            self.failed('Value is not 12')

    @aetest.cleanup
    def clean_testcase(self):
        log.info("Pass testcase cleanup")
        # Close app
        self.driver.quit()
        # Stop Appium Service
        self.appium_service.stop()

if __name__ == '__main__': # pragma: no cover
    aetest.main()