# Generated by Django 2.1.1 on 2018-10-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='createTime',
            field=models.DateField(max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='endTime',
            field=models.DateField(max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.BooleanField(default=True, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='version',
            name='createtime',
            field=models.DateField(max_length=20),
        ),
        migrations.AlterField(
            model_name='version',
            name='description',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='version',
            name='endtime',
            field=models.DateField(max_length=20),
        ),
        migrations.AlterField(
            model_name='version',
            name='release',
            field=models.BooleanField(default=False, verbose_name='release'),
        ),
    ]
