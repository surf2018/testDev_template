from django.apps import AppConfig
from settings import BASE_DIR

class TaskAppConfig(AppConfig):
    name = 'task_app'

#配置路径
BASE_PATH=BASE_DIR.replace('\\','/')
TASK_PATH=BASE_PATH+"/resources/tasks"
TASK_RUN_PATH=BASE_PATH+"/task_app/extend/run_test.py"
REPORT_PATH=TASK_PATH+"/report"


if __name__ =="__main__":
    print(TASK_PATH)
    print(TASK_RUN_PATH)