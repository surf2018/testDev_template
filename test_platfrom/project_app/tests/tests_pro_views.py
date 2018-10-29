from django.test import TestCase,Client
from django.contrib.auth.models import User
from ..models.project_models import Project,Version
import csv
from ddt import ddt,data,unpack
import time
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
class ProViewsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('test01','test01@1.com','123456')
        Project.objects.create(id=1, name='pt', description='pt_test project', createTime='2018-10-26', status=1,
                               endTime='2018-10-31')
        Version.objects.create(id=2,version='1.0.1',description = "1.0.1_pt",release=0,createtime = "2018-10-20",
                                endtime="2018-10-31",Criticalbugs=1,Majorbugs=1,project_id=1)
        self.client=Client()
        name = 'test01'
        pwd = '123456'
        datas = {'username': name, 'password': pwd}
        self.client.post('/user/login_action/', data=datas)
        time.sleep(1)
    def test_01proDashboard(self):
        response=self.client.get('/project/dashboard/?type=plist')
        statusConde=response.status_code
        content=(response.content).decode('utf-8')
        self.assertEqual(statusConde,200)
        self.assertIn("项目列表",content)
        self.assertTemplateUsed(response,'project/broadcast.html')
    def test_02addprojectPage(self):
        response = self.client.post('/project/dashboard/?type=pcreate')
        statusConde = response.status_code
        content = (response.content).decode('utf-8')
        self.assertEqual(statusConde, 200)
        self.assertIn("新建项目", content)
        self.assertTemplateUsed(response, 'project/broadcast.html')

    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\project_app\\tests\\pro_data.csv"))
    @unpack
    def test_03addProject(self,name,des,ctime,stat,etime):
        datas = {"name":name, "description":des,"createTime":ctime,"status":stat,"endTime": etime}
        response = self.client.post('/project/createP_action/',data=datas)
        statusConde = response.status_code
        pro=Project.objects.get(name=name)
        self.assertEqual(statusConde, 302),"test_03addProject fail"
        self.assertEqual(len(pro),1),"test_03addProject fail"

    def test_04editPojectPage(self):
        response=self.client.get('/project/editProject/1/?type=editp')
        statusConde=response.status_code
        content=response.content.decode('utf-8')
        exp_pro="编辑pt项目"
        self.assertEqual(statusConde,200)
        self.assertIn(exp_pro,content),"test_04editPojectPage fail"
        self.assertTemplateUsed(response,'project/broadcast.html'),"test_04editPojectPage fail"

    @data(*get_data("D:\\PycharmProjects\\testDev_template\\test_platfrom\project_app\\tests\\pro_data.csv"))
    @unpack
    def test_05editProject(self,name,des,ctime,stat,etime):
        result=0
        datas = {"name":name, "description":des,"createTime":ctime,"status":stat,"endTime": etime}
        response = self.client.post('editP_action/1/',data=datas)
        statusConde = response.status_code
        # content = (response.content).decode('utf-8')
        project=Project.objects.get(id=1)
        if(project.name==name and project.description==des and project.createTime==ctime and project.endTime==etime and project.status==stat):
            reuslt=1
        self.assertEqual(statusConde, 302),"test_05editProject fail"
        self.assertEqual(result,1),"test_05editProject fail"

    def test_06addProjectVersionPage(self):
        response = self.client.get('/project/createVersion/1/pt/vcreate/')
        statusConde = response.status_code
        content = response.content.decode('utf-8')
        exp_title="创建pt项目版本"
        self.assertEqual(statusConde, 200), "test_06addProjectVersionPage fail"
        self.assertEqual(exp_title,content),"test_06addProjectVersionPage fail"
    def test_07queryProVersion(self):
        response = self.client.get('project/dashboard?type=vlist&pname=pt&pid=1')
        statusConde = response.status_code
        exp_title="pt版本列表"
        content = response.content.decode('utf-8')
        self.assertEqual(statusConde, 200), "test_07queryProVersion fail"
        self.assertEqual(exp_title,content),"test_07queryProVersion fail"
    def test_08searchPro(self):
        response = self.client.get('project/dashboard?type=vlist&pname=pt&pid=1')
        statusConde = response.status_code
        exp_title = "pt版本列表"
        content = response.content.decode('utf-8')
        self.assertEqual(statusConde, 200), "test_08searchPro fail"
        self.assertEqual(exp_title, content), "test_08searchPro fail"
    def test_09delProject(self):
        response = self.client.get('/project/delProject/1')
        statusConde = response.status_code
        pro=Project.objects.filter(id=1).delete()
        self.assertEqual(statusConde, 302), "test_09delProject fail"
        self.assertEqual(len(pro), 0), "test_09delProject fail"

    def test_10logout(self):
        response = self.client.get('/user/logout/')
        statusConde = response.status_code
        self.assertEqual(statusConde, 302), "test_10logout fail"