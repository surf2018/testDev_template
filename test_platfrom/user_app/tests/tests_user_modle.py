from django.test import TestCase
from django.contrib.auth.models import User

class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(username='test01',email='test01@1.com')
    def test_user_01create(self):
        User.objects.create(username='test02',email='test02@2.com')
        #queyr
        user=User.objects.get(username='test02')
        name=user.username
        email=user.email
        self.assertEqual(name,'test02'),"test_user_create fail:username diff"
        self.assertEqual(email,"test02@2.com"),"test_user create fail:email diff"
    def test_user_02query(self):
        user=User.objects.get(username='test01')
        name=user.username
        email=user.email
        print("name:"+name+" email:"+email)
        self.assertEqual(name,"test01"),"test_user_query fail:username diff"
        self.assertEqual(email,"test01@1.com"),"test_user_query fail:email diff"
    def test_user_03update(self):
        oldName='test01'
        oldEmail='test01@1.com'
        updateName="test03"
        updateEmail='test03@3.com'
        User.objects.filter(username=oldName).update(username=updateName,email=updateEmail)
        #query update
        user=User.objects.get(username=updateName)
        name=user.username
        email=user.email
        #query oldName,oldEmail
        user2=User.objects.filter(username=oldName)
        self.assertEqual(name,'test03'),"test_user_update fail:name can't find"
        self.assertEqual(email,"test03@3.com"),"test_user_update fail:name can't find"
        self.assertEqual(len(user2),0),"test_user_update fail: can query oldname"
    def test_user_04del(self):
        #query
        user=User.objects.get(username='test01')
        if(user.username=='test01' and user.email=='test01@1.com'):
            #delete
            User.objects.get(username='test01').delete()
            #query
            user=User.objects.filter(username='test01')
            self.assertEqual(len(user),0),"test_user_del fail: can query deleted record"
        else:
            result=0
            self.assertEqual(result,0),"test_user_del fail:can't find test01"
