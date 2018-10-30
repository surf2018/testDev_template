from django.test import TestCase,Client
from django.contrib.auth.models import User
from ..models.project_models import Project
from ..models.module_models import Module
import csv
from ddt import ddt,data,unpack
import time
from datetime import datetime,timedelta
# Create your tests here.
#django unit test
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
class ModViewsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test01','test01@1.com','123456')
        Project.objects.create(id=1, name='pt', description='pt_test project', createTime='2018-10-26', status=1,
                               endTime='2018-10-31')
        Project.objects.create(id=2, name='pt2', description='pt2_test project', createTime='2018-10-26', status=1,
                               endTime='2018-10-31')
        Module.objects.create(id=1, name="mod_test", description='mod_test description',
                              createTime='2018-10-29 02:29:24', endTime='2018-10-30 02:25:37', project_id=1)
        self.client=Client()
        name = 'test01'
        pwd = '123456'
        datas = {'username': name, 'password': pwd}
        self.client.post('/user/login_action/', data=datas)
        time.sleep(1)
    def test_01modDashboard(self):
        response=self.client.get('/module/modulelist/?type=mlist')
        statusConde=response.status_code
        content=(response.content).decode('utf-8')
        self.assertEqual(statusConde,200)
        self.assertIn("模块列表",content)
        self.assertTemplateUsed(response,'project/module.html')
    def test_02addmodPage(self):
        response = self.client.post('/module/modulelist/?type=mcreate')
        statusConde = response.status_code
        content = (response.content).decode('utf-8')
        self.assertEqual(statusConde, 200)
        self.assertIn("新建模块", content)
        self.assertTemplateUsed(response, 'project/module.html')

    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\project_app\\tests\\mod_data.csv"))
    @unpack
    def test_03addModule(self,mname,mdes,mctime,metime,proid,proname):
        datas = {"name":mname, "description":mdes,"createTime":mctime,"endTime": metime,"project":proid}
        response = self.client.post('/module/createM_action/',data=datas)
        statusConde = response.status_code
        mod=Module.objects.get(name=mname)
        self.assertEqual(statusConde, 302),"test_03addModule fail"
        self.assertEqual(mod.name,mname),"test_03addModule fail"

    def test_04editModulePage(self):
        response=self.client.get('/module/editModule/1/')
        statusConde=response.status_code
        content=response.content.decode('utf-8')
        exp_pro="编辑模块"
        self.assertEqual(statusConde,200)
        self.assertIn(exp_pro,content),"test_04editModulePage fail"
        self.assertTemplateUsed(response,'project/module.html'),"test_04editModulePage fail"

    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\project_app\\tests\\mod_data.csv"))
    @unpack
    def test_05editModule(self,mname,mdes,mctime,metime,proid,proname):
        result=0
        datas = {"name": mname, "description": mdes, "createTime": mctime, "endTime": metime, "project": proid}
        response = self.client.post('/module/editM_action/1/',data=datas)
        statusConde = response.status_code
        mod=Module.objects.get(id=1)
        cur_pid=str(mod.project_id)
        if(mod.name==mname and mod.description==mdes and cur_pid==proid):
            result=1
        self.assertEqual(statusConde, 302),"test_05editModule fail"
        self.assertEqual(result,1),"test_05editModule fail"

    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\\project_app\\tests\\mod_search_data.csv"))
    @unpack
    def test_06searchModle(self,searchText):
        response = self.client.get('/module/searchm/?search='+searchText)
        statusConde = response.status_code
        exp_title = "模块列表"
        content = response.content.decode('utf-8')
        self.assertEqual(statusConde, 200), "test_06searchModle fail"
        self.assertIn(exp_title, content), "test_06searchModle fail"
    def test_07delModule(self):
        response = self.client.get('/module/delModule/1/')
        statusConde = response.status_code
        mod=Module.objects.filter(id=1)
        self.assertEqual(statusConde, 302), "test_07delModule fail"
        self.assertEqual(len(mod), 0), "test_07delModule fail"
