from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver import Chrome
from django.contrib.auth.models import User
from ..models.project_models import Project
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
class proTemplateTestCase(StaticLiveServerTestCase):
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
        self.selenium = Chrome()
        self.selenium.implicitly_wait(10)
        self.selenium.get('%s%s' % (self.live_server_url, '/user/'))
        username_input = self.selenium.find_element_by_id("username")
        username_input.send_keys('test01')
        password_input = self.selenium.find_element_by_id("password")
        password_input.send_keys('123456')
        self.selenium.find_element_by_id('btn').click()
        time.sleep(3)
    def test_00ProjectHomePate(self):
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        proInfo=[]
        result=0
        for pro in projectList:
            pron = pro.find_element_by_id('pname').text
            prodesp = pro.find_element_by_id('pdesp').text
            pctime = pro.find_element_by_id('pctime').text
            petime = pro.find_element_by_id('pendtime').text
            pstat = pro.find_element_by_id('pstat').text
            if (pron == 'pt'):
                proInfo=[pron, prodesp, pctime, petime, pstat]
                break
        print("proinfo:"+str(proInfo))
        if (proInfo[0] == 'pt' and proInfo[1] == "pt_test project" and proInfo[2] == "2018-10-26" and proInfo[3] == "2018-10-31" and proInfo[4] == "True"):
            result = 1
        self.assertEqual(result, 1), "test_02test_01addProject fail"
    def test_01addProjectPage(self):
        # click create button
        self.selenium.find_element_by_id('create-button').click()
        time.sleep(1)
        title = self.selenium.find_element_by_css_selector('h1.page-header').text
        exp_title = "新建项目"
        username = self.selenium.find_element_by_css_selector('li#navbar_user a').text
        exp_user = 'test01'
        flag = 0
        try:
            self.selenium.find_element_by_css_selector('form#cpro')
            flag = 1
        except:
            pass
        if (title == exp_title and username == exp_user and flag == 1):
            result = 1
        self.assertEqual(result, 1), "test_01addProjectPage fail"
    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\project_app\\tests\\pro_data.csv"))
    @unpack
    def test_02addProject(self,name,des,ctime,stat,etime):
        proInfo=[]
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
        if (stat=="False"):
            js = "$('#id_status').attr('checked',false)"
            self.selenium.execute_script(js)
        elif(stat=='True'):
            js="$('#id_status').attr('checked',true)"
            self.selenium.execute_script(js)
        time.sleep(1)
        self.selenium.find_element_by_id('id_endTime').clear()
        self.selenium.find_element_by_id('id_endTime').send_keys(etime)
        # click submit button
        self.selenium.find_element_by_name('submit').click()
        time.sleep(1)
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        for pro in projectList:
            pron = pro.find_element_by_id('pname').text
            prodesp = pro.find_element_by_id('pdesp').text
            pctime = pro.find_element_by_id('pctime').text
            petime = pro.find_element_by_id('pendtime').text
            pstat = pro.find_element_by_id('pstat').text
            if (pron == name):
                proInfo=[pron, prodesp, pctime, pstat, petime]
                break
        print("proInfo:"+str(proInfo))
        if (proInfo[0] == name and proInfo[1] == des and proInfo[2] == ctime and proInfo[3] == stat and proInfo[4] == etime):
            result = 1
        self.assertEqual(result, 1), "test_02addProject fail"
    def test_03addProjectNull(self):
        proInfo = []
        self.selenium.find_element_by_id('create-button').click()
        # click submit button
        self.selenium.find_element_by_name('submit').click()
        time.sleep(3)
        title=self.selenium.find_element_by_css_selector("h1.page-header").text
        exp_title="新建项目"
        self.assertIn(exp_title, title), "test_03addProjectNull fail"
    def test_04editProPage(self):
        #click edit
        pname="pt"
        flag=0
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        for pro in projectList:
           pron = pro.find_element_by_id('pname').text
           if(pron==pname):
               pro.find_element_by_id('editp').click()
               time.sleep(1)
               break
        #get title
        title=self.selenium.find_element_by_css_selector("h1.page-header").text
        exp_title="编辑"+pname+"项目"
        try:
            self.selenium.find_element_by_id("editPro")
            flag=1
        except:
            pass
        self.assertIn(exp_title, title), "test_04editPro fail"
        self.assertEqual(flag,1),"test_04editProPage fail"
    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\\project_app\\tests\\pro_editdata.csv"))
    @unpack
    def test_05editPro(self,name,des,ctime,stat,etime):
        pname = "pt"
        flag = 0
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        for pro in projectList:
            pron = pro.find_element_by_id('pname').text
            if (pron == pname):
                pro.find_element_by_id('editp').click()
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
        flag = self.selenium.find_element_by_id('id_status').get_attribute('checked')
        if (flag!=stat.lower()):
            js = "$('#id_status').attr('checked',"+stat.lower()+")"
            self.selenium.execute_script(js)
        time.sleep(1)
        self.selenium.find_element_by_id('id_endTime').clear()
        self.selenium.find_element_by_id('id_endTime').send_keys(etime)
        time.sleep(0.5)
        self.selenium.find_element_by_name('submit').click()
        time.sleep(1)
        proInfo=[]
        #check project list
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        for pro in projectList:
            pron = pro.find_element_by_id('pname').text
            if (pron == name):
                prodesp = pro.find_element_by_id('pdesp').text
                pctime = pro.find_element_by_id('pctime').text
                petime = pro.find_element_by_id('pendtime').text
                pstat = pro.find_element_by_id('pstat').text
                proInfo=[pron,prodesp,pctime,petime,pstat]
                break
        print("proInfo:"+str(proInfo))
        if (proInfo[0] == name and proInfo[1] == des and proInfo[2] == ctime and proInfo[3] == etime and proInfo[4] == stat):
            result = 1
        self.assertEqual(result, 1), "test_05editPro fail"

    def test_06searchPro(self):
        result=1
        self.selenium.find_element_by_id("pro_searchtext").clear()
        time.sleep(0.5)
        search_text='pt'
        self.selenium.find_element_by_id("pro_searchtext").send_keys(search_text)
        self.selenium.find_element_by_id('search').click()
        time.sleep(1)
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        for pro in projectList:
            pron = pro.find_element_by_id('pname').text
            prodesp = pro.find_element_by_id('pdesp').text
            if(search_text in pron and  search_text not in prodesp):
                result=0
                break
        self.assertEqual(result,1),"test_06searchPro fail"
    def test_07createVersionPage(self):
        name='pt'
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        for pro in projectList:
            pron = pro.find_element_by_id('pname').text
            if (pron == name):
                pro.find_element_by_id("pcreatel").click()
                time.sleep(1)
                break
        title=self.selenium.find_element_by_css_selector("h1.page-header").text
        exp_title="创建"+name+"项目版本"
        self.assertIn(exp_title,title),"test_07createVersionPage fail"

    def test_08delPro(self):
        delpn='pt'
        result=1
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        for pro in projectList:
            pron = pro.find_element_by_id('pname').text
            if(pron==delpn):
                pro.find_element_by_id('delp').click()
                alert=self.selenium.switch_to_alert()
                time.sleep(1)
                prompt=alert.text
                if("确定删除"+delpn+"项目" in prompt):
                    alert.accept()
                    time.sleep(1)
                    break
        projectList = self.selenium.find_elements_by_css_selector('tbody#prolist tr')
        for pro in projectList:
            pron = pro.find_element_by_id('pname').text
            if(pron=="pt"):
                result=0
                break
        self.assertEqual(result,1),"test_08delPro fail"

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
