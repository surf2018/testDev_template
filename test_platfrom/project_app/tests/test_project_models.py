from django.test import TestCase
from ..models.project_models import Project,Version
from ..models.module_models import Module
import time
from datetime import datetime,timedelta
class ProjectTestCase(TestCase):
    def setUp(self):
        Project.objects.create(id=1,name='pt',description='pt_test project',createTime='2018-10-26',status=1,endTime='2018-10-31')
    def test_pro_01create(self):
        result=0
        Project.objects.create(id=2,name='pt1', description='pt1_test project', createTime='2018-10-26', status=1,
                               endTime='2018-10-31')
        # queyr
        pro = Project.objects.get(id=2)
        name = pro.name
        desp = pro.description
        createtime=pro.createTime.strftime("%Y-%m-%d")
        status=pro.status
        endtime=pro.endTime.strftime("%Y-%m-%d")
        print(name,desp,createtime,status,endtime)
        if(name == 'pt1' and desp == "pt1_test project" and createtime == '2018-10-26' and status == True and endtime == '2018-10-31'):
            result=1
        self.assertEqual(result, 1), "test_pro_01create fail"

    def test_pro_02query(self):
        result=0
        pro = Project.objects.get(name='pt')
        name = pro.name
        desp = pro.description
        createtime = pro.createTime.strftime("%Y-%m-%d")
        status = pro.status
        endtime = pro.endTime.strftime("%Y-%m-%d")
        if ( name == 'pt' and desp == "pt_test project" and createtime == '2018-10-26' and status == True and endtime == '2018-10-31'):
            result = 1
        self.assertEqual(result, 1), "test_pro_02query fail"

    def test_pro_03update(self):
        oldName = 'pt'
        newName='pt_new'
        newdesp="pt_test project_new"
        newstatus=0
        result=0
        Project.objects.filter(name=oldName).update(name=newName,description=newdesp,status=newstatus)
        # query update
        pro = Project.objects.get(name=newName)
        name = pro.name
        description = pro.description
        status=pro.status
        #query old
        pro2=Project.objects.filter(name=oldName)
        if(name==newName and description==newdesp and status==newstatus and len(pro2)==0):
            result=1
        self.assertEqual(result,1),"test_pro_03update fail"
    def test_pro_04del(self):
        # query
        pro = Project.objects.get(name='pt')
        if (pro.name == 'pt' and pro.id==1):
            # delete
            Project.objects.get(id=1).delete()
            # query
            pro = Project.objects.filter(id=1)
            self.assertEqual(len(pro), 0), "test_pro_04del fail: can query deleted record"
        else:
            result = 0
            self.assertEqual(result, 0), "test_pro_04del fail:can't find test01"

class moduleTestCase(TestCase):
    def setUp(self):
        Project.objects.create(id=1, name='pt', description='pt_test project', createTime='2018-10-26', status=1,
                               endTime='2018-10-31')
        Project.objects.create(id=2, name='pt2', description='pt2_test project', createTime='2018-10-31', status=1,
                               endTime='2018-11-30')
        Module.objects.create(id=1, name='mod_t', description='mod_test project', createTime='2018-10-26',
                               endTime='2018-10-31',project_id=1)

    def test_mod_01create(self):
        Module.objects.create(id=2, name='mod_t1', description='mod_test1 project', createTime='2018-10-26',
                               endTime='2018-10-31',project_id=1)
        # queyr
        mod = Module.objects.get(id=2)
        name = mod.name
        desp = mod.description
        createtime = mod.createTime.strftime("%Y-%m-%d")
        endtime = mod.endTime.strftime("%Y-%m-%d")
        pid=mod.project_id
        if (name == 'mod_t1' and desp == "mod_test1 project" and createtime == '2018-10-26' and endtime == '2018-10-31' and pid==1):
            result = 1
        self.assertEqual(result, 1), "test_mod_01create fail"

    def test_mod_02query(self):
        mod = Module.objects.get(name='mod_t',id=1)
        name = mod.name
        desp = mod.description
        createtime = mod.createTime.strftime("%Y-%m-%d")
        endtime = mod.endTime.strftime("%Y-%m-%d")
        pid=mod.project_id
        if (
                name == 'mod_t' and desp == "mod_test project" and createtime == '2018-10-26' and endtime == '2018-10-31' and pid==1):
            result = 1
        self.assertEqual(result, 1), "test_mod_02query fail"

    def test_mod_03update(self):
        newName = 'mod_t_new'
        newdesp = "mod_t_new test"
        newpid=2
        result = 0
        Module.objects.filter(id=1).update(name=newName, description=newdesp, project_id=newpid)
        # query update
        mod = Module.objects.get(id=1)
        name = mod.name
        description = mod.description
        pid=mod.project_id
        # query old
        mod2 = Module.objects.filter(name='mod_t')
        if (name == newName and description == newdesp and pid==newpid and len(mod2) == 0):
            result = 1
        self.assertEqual(result, 1), "test_mod_03update fail"

    def test_mod_04del(self):
        # query
        mod = Module.objects.get(id=1)
        if (mod.name == 'mod_t' and mod.id == 1):
            # delete
            Project.objects.get(id=1).delete()
            # query
            pro = Project.objects.filter(id=1)
            self.assertEqual(len(pro), 0), "test_mod_04del fail: can query deleted record"
        else:
            result = 0
            self.assertEqual(result, 0), "test_mod_04del fail:can't find test01"


class VersionTestCase(TestCase):
    def setUp(self):
        Project.objects.create(id=1, name='pt', description='pt_test project', createTime='2018-10-26', status=1,
                               endTime='2018-10-31')
        Project.objects.create(id=2, name='pt2', description='pt2_test project', createTime='2018-10-31', status=1,
                               endTime='2018-11-30')
        Version.objects.create(id=1, version='ver_t', description='ver_test project', createtime='2018-10-26', release=1,
                              endtime='2018-10-31',Criticalbugs='1',Majorbugs='1',project_id=1)

    def test_ver_01create(self):
        Version.objects.create(id=2, version='ver_t1', description='ver1_test project', createtime='2018-10-26', release=1,
                              endtime='2018-10-31',Criticalbugs='1',Majorbugs='1',project_id=1)
        # queyr
        ver = Version.objects.get(id=2)
        name = ver.version
        desp = ver.description
        createtime = ver.createtime.strftime("%Y-%m-%d")
        endtime = ver.endtime.strftime("%Y-%m-%d")
        pid = ver.project_id
        release=ver.release
        Cbugs=ver.Criticalbugs
        Mbugs=ver.Majorbugs
        if (name=='ver_t1', desp=='ver1_test project', createtime=='2018-10-26', release==1,
        endtime=='2018-10-31', Cbugs=='1', Mbugs=='1', pid==1):
            result=1
        self.assertEqual(result, 1), "test_mod_01create fail"

    def test_ver_02query(self):
        result=0
        ver = Version.objects.get(id=1)
        name = ver.version
        desp = ver.description
        createtime = ver.createtime.strftime("%Y-%m-%d")
        endtime = ver.endtime.strftime("%Y-%m-%d")
        pid = ver.project_id
        release=ver.release
        Cbugs=ver.Criticalbugs
        Mbugs=ver.Majorbugs
        if (name=='ver_t', desp=='ver_test project', createtime=='2018-10-26', release==1,endtime=='2018-10-31',Cbugs=='1',Mbugs=='1',pid==1):
            result = 1
        self.assertEqual(result, 1), "test_mod_02query fail"

    def test_ver_03update(self):
        newName = 'ver_t_new'
        newdesp = "ver_t_new test"
        newpid = 2
        newCbugs='2'
        newMbugs='2'
        newrelease=0
        result = 0
        ctime='2018-11-01'
        etime='2018-11-30'
        Version.objects.filter(id=1).update(version=newName, description=newdesp, project_id=newpid,Criticalbugs=newCbugs,Majorbugs=newMbugs,release=newrelease,createtime=ctime,endtime=etime)
        # query update
        ver = Version.objects.get(id=1)
        name = ver.version
        description = ver.description
        pid = ver.project_id
        Cbugs=ver.Criticalbugs
        Mbugs=ver.Majorbugs
        release=ver.release
        createtime=ver.createtime.strftime("%Y-%m-%d")
        endtime=ver.endtime.strftime("%Y-%m-%d")
        # query old
        ver2 = Module.objects.filter(name='ver_t')
        print(name,description,pid,Cbugs,Mbugs,release,createtime,endtime)
        if (name == newName and description == newdesp and pid == newpid and Cbugs==newCbugs and Mbugs==newMbugs and release==False and createtime==ctime and endtime==etime and len(ver2) == 0):
            result = 1
        self.assertEqual(result, 1), "test_mod_03update fail"

    def test_ver_04del(self):
        # query
        ver=Version .objects.get(id=1)
        if (ver.version == 'ver_t' and ver.id == 1):
            # delete
            Version.objects.get(id=1).delete()
            # query
            ver = Version.objects.filter(id=1)
            self.assertEqual(len(ver), 0), "test_ver_04del fail: can query deleted record"
        else:
            result = 0
            self.assertEqual(result, 0), "test_ver_04del fail:can't find test01"