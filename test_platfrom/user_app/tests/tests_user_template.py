from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
import time
# Create your tests here.
#django unit test
class UserTemplateTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.live_server_url="http://127.0.0.1:8000"

    def test_01login_success(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/'))
        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys('user1')
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys('user1123456')
        self.selenium.find_element_by_id('btn').click()
        time.sleep(3)
        proS=self.selenium.find_element_by_id('project').get_attribute('class')
        self.assertIn('active',proS),"test_01login_success fail "

    def test_02login_success(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/'))
        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys('user1')
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys('123456')
        self.selenium.find_element_by_id('btn').click()
        time.sleep(1)
        exp="username or password is not invalid"
        content=self.selenium.find_element_by_tag_name('font').text
        self.assertIn(exp,content),"test_02login_success fail "
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()