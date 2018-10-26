from django.test import TestCase,Client
from django.contrib.auth.models import User
# Create your tests here.
#django unit test
class UserViewsTest(TestCase):
    def setUp(self):
        User.objects.create_user('test01','test01@1.com','123456')
        self.client=Client()
    def test_01index(self):
        response=self.client.get('/user/')
        statusConde=response.status_code
        content=(response.content).decode('utf-8')
        self.assertEqual(statusConde,200)
        self.assertIn("User login",content)
        self.assertTemplateUsed(response,'user/index.html')
    def test_02lLoginAction_wrong(self):
        name='test01'
        pwd='1234567'
        prompt="username or password is not invalid"
        datas ={'username':name,'password':pwd}
        response=self.client.post('/user/login_action/',data=datas)
        statusConde=response.status_code
        content=response.content.decode('utf-8')
        self.assertEqual(statusConde,200)
        self.assertIn(prompt,content),"test_02lLoginAction_wrong"
        self.assertTemplateUsed(response,'user/index.html')
    def test_03LoginAction_null(self):
        datas ={'username':'','password':''}
        response=self.client.post('/user/login_action/',data=datas)
        statusConde=response.status_code
        content=response.content.decode('utf-8')
        exp_pro="name or password should not be empty"
        self.assertEqual(statusConde,200)
        self.assertIn(exp_pro,content),"test_02lLoginAction_wrong"
        self.assertTemplateUsed(response,'user/index.html')
    def test_04LoginAction_success(self):
        #query
        user=User.objects.get(username='test01')
        name=user.username
        passwd='123456'
        datas={'username':name,'password':passwd}
        response=self.client.post("/user/login_action/",data=datas)
        statusCode=response.status_code
        self.assertEqual(statusCode,302),"test_04LoginAction_success fail"