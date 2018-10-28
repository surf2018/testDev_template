from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver import Chrome
from django.contrib.auth.models import User
import time
# Create your tests here.
#django unit test
class UserTemplateTest(StaticLiveServerTestCase):
    @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.selenium = Chrome()
    #     cls.selenium.implicitly_wait(10)
    #     # cls.live_server_url="http://127.0.0.1:8000"
    def setUp(self):
        User.objects.create_user(username='test01',email='test01@1.com',password='123456')
        self.selenium=Chrome()
        self.selenium.implicitly_wait(10)
    def test_01login_success(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/'))
        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys('test01')
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys('123456')
        self.selenium.find_element_by_id('btn').click()
        time.sleep(3)
        proS=self.selenium.find_element_by_id('project').get_attribute('class')
        userName=self.selenium.find_element_by_css_selector('li#navbar_user a').text
        self.assertIn('active',proS),"test_01login_success fail"
        self.assertEqual(userName,"test01"),"test_01login_success fail"

    def test_02login_fail(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/user/'))
        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys('user1')
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys('123456')
        self.selenium.find_element_by_id('btn').click()
        time.sleep(1)
        exp="username or password is not invalid"
        content=self.selenium.find_element_by_tag_name('font').text
        self.assertIn(exp,content),"test_02login_fail"
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()