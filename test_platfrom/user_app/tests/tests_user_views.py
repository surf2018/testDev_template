from django.test import TestCase,Client
from django.contrib.auth.models import User

# Create your tests here.
#django unit test
class UserViewsTest(TestCase):
    def setUp(self):
        self.client=Client()
        User.objects.create(username='test01')
    def test_01index(self):
        response=self.client.get('/user/')
        statusConde=response.status_code
        content=response.text
        self.assertEqual(statusConde,200)
        self.assertIn("测试平台",content)
        self.assertTemplateUsed(response,'"user/index.html')
    def test_02lLoginAction_normal(self):
        response=self.client.post('/user/login_action/')
        statusConde=response.status_code
        content=response.text
        self.assertEqual(statusConde,200)
        self.assertIn("测试平台",content)
        self.assertTemplateUsed(response,'"user/index.html')
    def test_03LoginAction_null(self):
    def test_04LoginAction_wrongName(self):
    def test_05LoginAction_noRegister(self):
    def test_06Logout(self):