# Generated by Django 2.1.1 on 2018-10-14 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0015_project_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='project',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Version',
        ),
    ]