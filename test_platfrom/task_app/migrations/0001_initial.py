# Generated by Django 2.1.1 on 2018-12-19 01:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('cases', models.TextField(default='', max_length=1000)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('error', models.IntegerField(default=0, verbose_name='错误用例个数')),
                ('failures', models.IntegerField(default=0, verbose_name='失败用例个数')),
                ('skipped', models.IntegerField(default=0, verbose_name='跳过用例个数')),
                ('tests', models.IntegerField(default=0, verbose_name='总用例数个数')),
                ('run_time', models.FloatField(default=0, verbose_name='运行时长')),
                ('result', models.TextField(default='', verbose_name='详细结果')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_app.Task')),
            ],
        ),
    ]
