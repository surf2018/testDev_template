from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver import Chrome
from django.contrib.auth.models import User
from ..models.project_models import Project
from ..models.module_models import Module
import time
from ddt import ddt,data,unpack
import csv

# Create your tests here.
# django unit test
def get_data(file_name):
    # print("file_name"+str(file_name))
    # create an empty list to store rows
    rows = []
    # open the CSV file
    data_file = open(file_name, "r")
    # create a CSV Reader from CSV file
    reader = csv.reader(data_file)
    # skip the headers
    next(reader, None)
    # add rows from reader to list
    for row in reader:
        rows.append(row)
    return rows
@ddt
class modTemplateTestCase(StaticLiveServerTestCase):
    @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.selenium = Chrome()
    #     cls.selenium.implicitly_wait(10)
    #     # cls.live_server_url="http://127.0.0.1:8000"
    def setUp(self):
        User.objects.create_user(username='test01', email='test01@1.com', password='123456')
        Project.objects.create(id=1, name='pt', description='pt_test project', createTime='2018-10-26', status=1,
                               endTime='2018-10-31')
        Project.objects.create(id=2, name='pt2', description='pt2_test project', createTime='2018-10-29',status=1,endTime='2018-11-30')
        Module.objects.create(id=1,name="mod_test",description='mod_test description', createTime='2018-10-29 02:29:24', endTime='2018-10-30 02:25:37',project_id=1)
        self.selenium = Chrome()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/user/'))
        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys('test01')
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys('123456')
        self.selenium.find_element_by_id('btn').click()
        time.sleep(3)
        self.selenium.find_element_by_css_selector('li#module a').click()
        time.sleep(1)
    def test_00ModleHomePage(self):
        #click mod manager
        pageTitle=self.selenium.find_element_by_css_selector("h1.page-header").text
        print("pageTitle:"+pageTitle)
        exp_title="模块列表"
        modtList = self.selenium.find_elements_by_css_selector('tbody#modlist tr')
        modInfo=[]
        result=0
        for mod in modtList:
            modname = mod.find_element_by_id('modname').text
            modesp = mod.find_element_by_id('moddesp').text
            modctime = mod.find_element_by_id('modctime').text
            modetime = mod.find_element_by_id('modetime').text
            modpro = mod.find_element_by_id('modpro').text
            if (modname == 'mod_test'):
                modInfo=[modname, modesp, modctime, modetime, modpro]
                break
        print("modInfo:"+str(modInfo))
        if (pageTitle == exp_title and modInfo[0] == 'mod_test' and modInfo[1] == "mod_test description" and modInfo[2] == "2018-10-29 02:29:24" and modInfo[3] == "2018-10-30 02:25:37" and modInfo[4] == "pt"):
            result = 1
        self.assertEqual(result, 1), "test_00ModleHomePage fail"
    def test_01addModlePage(self):
        # click create button
        self.selenium.find_element_by_id('create-button').click()
        time.sleep(1)
        title = self.selenium.find_element_by_css_selector('h1.page-header').text
        exp_title = "新建模块"
        username = self.selenium.find_element_by_css_selector('li#navbar_user a').text
        exp_user = 'test01'
        flag = 0
        try:
            self.selenium.find_element_by_css_selector('form#modform')
            flag = 1
        except:
            pass
        if (title == exp_title and username == exp_user and flag == 1):
            result = 1
        self.assertEqual(result, 1), "test_01addModlePage fail"
    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\project_app\\tests\\mod_data.csv"))
    @unpack
    def test_02addModule(self,name,des,ctime,etime,proid,proname):
        modInfo=[]
        result=0
        self.selenium.find_element_by_id('create-button').click()
        # create form
        self.selenium.find_element_by_id("id_name").clear()
        time.sleep(0.5)
        self.selenium.find_element_by_id("id_name").send_keys(name)
        time.sleep(0.5)
        self.selenium.find_element_by_id('id_description').clear()
        self.selenium.find_element_by_id('id_description').send_keys(des)
        time.sleep(0.5)
        self.selenium.find_element_by_id('id_createTime').clear()
        self.selenium.find_element_by_id('id_createTime').send_keys(ctime)
        time.sleep(1)
        self.selenium.find_element_by_id('id_endTime').clear()
        self.selenium.find_element_by_id('id_endTime').send_keys(etime)
        #select project
        js="$(\"#id_project\").val('"+proid+"');"
        self.selenium.execute_script(js)
        time.sleep(1)
        # click submit button
        self.selenium.find_element_by_name('submit').click()
        time.sleep(1)
        modList = self.selenium.find_elements_by_css_selector('tbody#modlist tr')
        for mod in modList:
            modname = mod.find_element_by_id('modname').text
            moddesp = mod.find_element_by_id('moddesp').text
            modctime = mod.find_element_by_id('modctime').text
            modetime = mod.find_element_by_id('modetime').text
            modpro = mod.find_element_by_id('modpro').text
            if (modname == name):
                modInfo=[modname, moddesp, modctime, modetime, modpro]
                break
        print("proInfo:"+str(modInfo))
        print(name,des,ctime,etime,proname)
        if (modInfo[0] == name and modInfo[1] == des and modInfo[2] == ctime and modInfo[3] == etime and modInfo[4] == proname):
            result = 1
        self.assertEqual(result, 1), "test_02addProject fail"
    def test_03addModNull(self):
        proInfo = []
        self.selenium.find_element_by_id('create-button').click()
        # click submit button
        self.selenium.find_element_by_name('submit').click()
        time.sleep(3)
        title=self.selenium.find_element_by_css_selector("h1.page-header").text
        exp_title="新建模块"
        self.assertIn(exp_title, title), "test_03addModNull fail"
    def test_04editModPage(self):
        #click edit
        modname="mod_test"
        flag=0
        modList = self.selenium.find_elements_by_css_selector('tbody#modlist tr')
        for mod in modList:
           modn = mod.find_element_by_id('modname').text
           if(modn==modname):
               mod.find_element_by_id('modedit').click()
               time.sleep(1)
               break
        #get title
        title=self.selenium.find_element_by_css_selector("h1.page-header").text
        exp_title="编辑模块"
        try:
            self.selenium.find_element_by_id("modeditform")
            flag=1
        except:
            pass
        self.assertIn(exp_title, title), "test_04editModPage fail"
        self.assertEqual(flag,1),"test_04editProPage fail"
    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\\project_app\\tests\\mod_data.csv"))
    @unpack
    def test_05editMod(self,name,des,ctime,etime,proid,proname):
        modname = 'mod_test'
        flag = 0
        modList = self.selenium.find_elements_by_css_selector('tbody#modlist tr')
        for mod in modList:
            modn = mod.find_element_by_id('modname').text
            if (modn == modname):
                mod.find_element_by_id('modedit').click()
                break
        self.selenium.find_element_by_id("id_name").clear()
        time.sleep(0.5)
        self.selenium.find_element_by_id("id_name").send_keys(name)
        time.sleep(0.5)
        self.selenium.find_element_by_id('id_description').clear()
        self.selenium.find_element_by_id('id_description').send_keys(des)
        time.sleep(0.5)
        self.selenium.find_element_by_id('id_createTime').clear()
        self.selenium.find_element_by_id('id_createTime').send_keys(ctime)
        time.sleep(1)
        self.selenium.find_element_by_id('id_endTime').clear()
        self.selenium.find_element_by_id('id_endTime').send_keys(etime)
        time.sleep(1)
        #check project name
        # select project
        js = "$(\"#id_project\").val('" + proid + "');"
        self.selenium.execute_script(js)
        time.sleep(1)
        # click submit button
        self.selenium.find_element_by_name('submit').click()
        time.sleep(1)
        modInfo=[]
        #check project list
        modList = self.selenium.find_elements_by_css_selector('tbody#modlist tr')
        for mod in modList:
            modn = mod.find_element_by_id('modname').text
            if (modn == name):
                moddesp = mod.find_element_by_id('moddesp').text
                modctime = mod.find_element_by_id('modctime').text
                modetime = mod.find_element_by_id('modetime').text
                modpro=mod.find_element_by_id("modpro").text
                modInfo=[modn,moddesp,modctime,modetime,modpro]

                break
        print("modInfo:"+str(modInfo))
        print(name,des,ctime,etime,proname)
        if (modInfo[0] == name and modInfo[1] == des and modInfo[2] == ctime and modInfo[3] == etime and modInfo[4] == proname):
            result = 1
        self.assertEqual(result, 1), "test_05editMod fail"

    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\\project_app\\tests\\mod_search_data.csv"))
    @unpack
    def test_07searchMod(self,searchText):
        print("running test_07searchMod")
        result=1
        self.selenium.find_element_by_id("modsearchText").clear()
        time.sleep(0.5)
        self.selenium.find_element_by_id("modsearchText").send_keys(searchText)
        time.sleep(1)
        self.selenium.find_element_by_id('search').click()
        time.sleep(1)
        modList = self.selenium.find_elements_by_css_selector('tbody#modlist tr')
        for mod in modList:
            modn = mod.find_element_by_id('modname').text
            moddes = mod.find_element_by_id('moddesp').text
            modp = mod.find_element_by_id('modpro').text
            if(searchText not in modn and  searchText not in moddes and searchText not in modp):
                result=0
                break
        self.assertEqual(result,1),"test_06searchMod fail"

    def test_08delMod(self):
        delmn='mod_test'
        result=1
        modList = self.selenium.find_elements_by_css_selector('tbody#modlist tr')
        for mod in modList:
            modn = mod.find_element_by_id('modname').text
            if(modn==delmn):
                mod.find_element_by_id('moddel').click()
                alert=self.selenium.switch_to_alert()
                time.sleep(1)
                prompt=alert.text
                if("确定删除"+modn+"模块？" in prompt):
                    alert.accept()
                    time.sleep(1)
                    break
        modList = self.selenium.find_elements_by_css_selector('tbody#modlist tr')
        for mod in modList:
            modn = mod.find_element_by_id('modname').text
            if(modn==delmn):
                result=0
                break
        self.assertEqual(result,1),"test_08delMod fail"

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
