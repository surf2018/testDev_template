# Generated by Django 2.1.1 on 2018-10-02 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0010_auto_20181002_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='createtime',
            field=models.CharField(default='', max_length=20),
        ),
    ]
